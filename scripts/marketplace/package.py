#!/usr/bin/env python3
"""Offline catalog validation and deterministic packaging; never connect or publish."""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import posixpath
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree

from jsonschema import Draft202012Validator, ValidationError

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('battlemap_helpers', ROOT / 'scripts/battlemap/package.py')
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
require = helpers.require
decode_json = helpers.decode_json
POLICIES = Path(__file__).with_name('packages.json')
MAX_FILE = helpers.MAX_FILE_BYTES
MAX_TOTAL = helpers.MAX_PACKAGE_BYTES
SEMVER = helpers.helpers.SEMVER


def policy_for(name):
    policies = decode_json(POLICIES.read_bytes())
    require(name in policies, 'Package identity is not reviewed')
    return policies[name]


def read_directory(root, policy):
    require(not root.is_symlink() and root.is_dir(), 'Package root must be a regular directory')
    allowed = set(policy['files'])
    directories = {str(p) for f in allowed for p in PurePosixPath(f).parents if str(p) != '.'}
    files, total = {}, 0
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Package may not contain symlinks')
        name = path.relative_to(root).as_posix()
        if path.is_dir():
            require(name in directories, 'Unexpected package directory')
            continue
        require(name in allowed and path.is_file(), 'Unexpected or non-regular package file')
        size = path.stat().st_size
        total += size
        require(0 < size <= MAX_FILE and total <= MAX_TOTAL, 'Package exceeds size bound')
        files[name] = path.read_bytes()
    return files


def read_archive(path, name, policy):
    require(not path.is_symlink() and path.is_file(), 'Archive must be a regular file')
    require(path.stat().st_size <= MAX_TOTAL, 'Archive exceeds size bound')
    files, total = {}, 0
    with zipfile.ZipFile(path) as archive:
        entries = archive.infolist()
        require(len(entries) == len(policy['files']), 'Unexpected archive file count')
        for entry in entries:
            require(entry.filename.startswith(name + '/'), 'Archive requires one matching package directory')
            relative = entry.filename[len(name) + 1:]
            require(relative in policy['files'] and relative not in files, 'Unexpected, duplicate or escaping archive path')
            require(stat.S_IFMT(entry.external_attr >> 16) in (0, stat.S_IFREG), 'Non-regular archive entry')
            total += entry.file_size
            require(not entry.is_dir() and 0 < entry.file_size <= MAX_FILE and total <= MAX_TOTAL, 'Archive exceeds size bound')
            require(not entry.flag_bits & 1, 'Encrypted archive entry')
            require(entry.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED), 'Unsupported archive compression')
            files[relative] = archive.read(entry)
    return files


def validate_files(name, files, policy):
    require(set(files) == set(policy['files']), 'Package inventory differs from reviewed file list')
    require(all(0 < len(v) <= MAX_FILE for v in files.values()) and sum(map(len, files.values())) <= MAX_TOTAL, 'Package exceeds size bound')
    for path, data in files.items():
        text = data.decode('utf8')
        require('\x00' not in text, 'Package text contains null characters')
        require(not any(re.search(p, text) for p in helpers.CREDENTIAL_PATTERNS), 'Possible credential material in package')
    manifest = decode_json(files['plugin.json'])
    mcp = decode_json(files['mcp.json'])
    Draft202012Validator(helpers.fixed_schema('plugin')).validate(manifest)
    Draft202012Validator(helpers.fixed_schema('mcp')).validate(mcp)
    require(set(manifest) == {'$schema', 'name', 'version', 'description', 'author', 'extensions'}, 'Unexpected manifest fields or app binding')
    require(manifest['name'] == name and manifest['author'] == policy['author'], 'Package or publisher identity changed')
    require(manifest['version'] == policy['version'] and SEMVER.fullmatch(manifest['version']), 'Unexpected package version')
    require(set(manifest['extensions']) == {'com.openai'}, 'Unexpected manifest extension')
    extension = manifest['extensions']['com.openai']
    require(set(extension) == set(policy['extensionKeys']), 'Unexpected extension fields or audience change')
    interface = extension['interface']
    require(set(interface) == set(policy['interfaceKeys']), 'Unexpected interface fields')
    for key, expected in policy['identity'].items():
        require(interface.get(key) == expected, 'Presentation identity, capabilities or starter prompts changed')
    require(0 < len(interface['shortDescription']) <= 30 and interface['longDescription'].strip(), 'Missing or oversized presentation')
    for key in ('logo', 'composerIcon', 'logoDark', 'composerIconDark'):
        if key in interface:
            require(interface[key] == './assets/icon.svg', 'Icon path must remain contained and reviewed')
    if 'onboardingSkill' in extension:
        require(extension['onboardingSkill'] == './skills/onboarding/SKILL.md', 'Unexpected onboarding path')
    compatibility = {k: manifest[k] for k in ('name', 'version', 'description', 'author')}
    compatibility.update(skills='./skills/', interface=interface, mcpServers='./.mcp.json')
    if 'onboardingSkill' in extension:
        compatibility['extensions'] = {'com.openai': {'onboardingSkill': extension['onboardingSkill']}}
    require(decode_json(files['.codex-plugin/plugin.json']) == compatibility, 'Portable/Codex manifest parity failed')
    expected = {policy['server']: {'type': 'streamable-http', 'url': policy['endpoint']}}
    require(mcp == {'$schema': 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json', 'mcpServers': expected}, 'Portable endpoint, server identity or transport changed')
    expected[policy['server']]['type'] = 'http'
    require(decode_json(files['.mcp.json']) == {'mcpServers': expected}, 'Codex endpoint or transport changed')
    # Claude Code reads .claude-plugin/plugin.json plus the root .mcp.json and skills/ directory.
    claude = {k: manifest[k] for k in ('name', 'version', 'description', 'author')}
    claude.update(homepage=policy['claude']['homepage'], keywords=policy['claude']['keywords'])
    require(claude['homepage'].startswith('https://') and claude['keywords'] and all(re.fullmatch(r'[a-z0-9][a-z0-9-]*', k) for k in claude['keywords']), 'Invalid Claude homepage or keywords')
    require(decode_json(files['.claude-plugin/plugin.json']) == claude, 'Portable/Claude manifest parity failed')
    for path in policy['files']:
        if not path.endswith('/SKILL.md'):
            continue
        text = files[path].decode('utf8')
        require(text.startswith('---\n'), 'Missing skill frontmatter')
        header, separator, body = text[4:].partition('\n---\n')
        skill = PurePosixPath(path).parent.name
        require(separator and body.strip() and re.search(rf'^name: {re.escape(skill)}$', header, re.M), 'Skill identity or body missing')
        require(re.search(r'^description: \S.+$', header, re.M), 'Missing skill trigger description')
    for path, data in files.items():
        if not path.endswith('.md'):
            continue
        for target in re.findall(r'\]\(([^\s)]+)\)', data.decode('utf8')):
            if target.startswith(('https://', 'http://', '#')):
                continue
            require(not re.match(r'(?:[A-Za-z][\w+.-]*:|/|\\)', target) and '\\' not in target, 'Unsafe package reference')
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(path), target.split('#')[0]))
            require(not resolved.startswith('../') and resolved in files, 'Missing or escaping package reference')
    # Cthulhu artwork uses static fill-rule/clip-rule attributes; validate their values
    # before passing a copy to the existing strict SVG validator.
    icon = files['assets/icon.svg']
    require(b'<!DOCTYPE' not in icon.upper() and b'<!ENTITY' not in icon.upper(), 'Unsafe SVG declaration')
    svg = ElementTree.fromstring(icon)
    for element in svg.iter():
        for key in ('fill-rule', 'clip-rule'):
            if key in element.attrib:
                require(element.attrib.pop(key) in ('evenodd', 'nonzero'), 'Invalid SVG fill rule')
    helpers.validate_icon(ElementTree.tostring(svg))
    if name == 'call-of-cthulhu-plugin':
        for key, suffix in [('websiteURL','about'), ('supportURL','support'), ('privacyPolicyURL','privacy'), ('termsOfServiceURL','terms')]:
            require(interface.get(key) == f'https://cthulhu.questportal.com/{suffix}', 'Cthulhu listing URL missing or changed')
        review = extension['review']
        require(set(review) == {'test_cases', 'commerce', 'commerce_description', 'demo_recording_url'}, 'Unexpected review metadata')
        require(review['commerce'] is False and review['commerce_description'] == 'This plugin involves no payments or purchases.', 'Commerce metadata changed')
        require(review.get('demo_recording_url') == 'https://cthulhu.questportal.com/walkthrough.mp4', 'Cthulhu walkthrough missing')
        cases = review.get('test_cases', {})
        require(len(cases.get('positive', [])) >= 5 and len(cases.get('negative', [])) >= 3, 'Cthulhu review cases missing')
        for case in cases['positive']:
            require(set(case) == {'description', 'prompt', 'tools_triggered', 'expected_behavior'} and all(isinstance(v,str) and v.strip() for v in case.values()), 'Invalid positive review case')
        for case in cases['negative']:
            require(set(case) == {'description', 'prompt'} and all(isinstance(v,str) and v.strip() for v in case.values()), 'Invalid negative review case')
    return {'name': name, 'version': manifest['version'], 'endpoint': policy['endpoint'], 'status': 'valid', 'files': [{'path': p, 'sha256': helpers.sha256(files[p]), 'bytes': len(files[p])} for p in sorted(files)]}


def read_catalog(root, relative, policies):
    path = root / relative
    require(not path.is_symlink() and path.is_file() and path.stat().st_size <= MAX_FILE, 'Invalid catalog file')
    catalog = decode_json(path.read_bytes())
    require(catalog.get('name') == 'questportal-plugins', 'Catalog identity changed')
    entries = catalog.get('plugins')
    require(isinstance(entries, list) and all(isinstance(e, dict) for e in entries), 'Invalid catalog entries')
    require(len(entries) == len(policies) and {e.get('name') for e in entries} == set(policies), 'Missing, duplicate or unreviewed catalog identity')
    return catalog, {e['name']: e for e in entries}


def validate_catalog(root):
    policies = decode_json(POLICIES.read_bytes())
    # Codex/ChatGPT catalog and Claude Code catalog list the same local packages.
    catalog, entries = read_catalog(root, '.agents/plugins/marketplace.json', policies)
    claude_catalog, claude_entries = read_catalog(root, '.claude-plugin/marketplace.json', policies)
    require(set(claude_catalog) == {'$schema', 'name', 'description', 'owner', 'plugins'}, 'Unexpected Claude catalog fields')
    require(claude_catalog['$schema'] == 'https://anthropic.com/claude-code/marketplace.schema.json' and claude_catalog['description'].strip(), 'Claude catalog schema or description changed')
    require(claude_catalog['owner'] == {'name': 'Quest Portal', 'url': 'https://www.questportal.com'}, 'Claude catalog owner changed')
    require([e['name'] for e in catalog['plugins']] == [e['name'] for e in claude_catalog['plugins']], 'Catalog order differs')
    require(not (root / 'plugins').is_symlink(), 'Plugin directory may not be a symlink')
    reports = []
    for name, entry in entries.items():
        require(entry == {'name': name, 'source': {'source': 'local', 'path': f'./plugins/{name}'}}, 'Catalog path, binding or audience changed')
        source = root / 'plugins' / name
        files = read_directory(source, policies[name])
        reports.append(validate_files(name, files, policies[name]))
        manifest = decode_json(files['plugin.json'])
        require(claude_entries[name] == {'name': name, 'source': f'./plugins/{name}', 'description': manifest['description'], 'author': manifest['author'], 'category': 'entertainment', 'homepage': policies[name]['claude']['homepage']}, 'Claude catalog entry, binding or audience changed')
    return reports


def build_zip(name, files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_STORED) as archive:
        for path in sorted(files):
            info = zipfile.ZipInfo(f'{name}/{path}', date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, files[path])
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'build'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    reports = validate_catalog(args.root)
    if args.command == 'build':
        require(args.output_dir is not None, 'Build requires --output-dir')
        require(not args.output_dir.resolve().is_relative_to((args.root / 'plugins').resolve()), 'Write artifacts outside source packages')
        for report in reports:
            name = report['name']
            source = args.root / 'plugins' / name
            policy = policy_for(name)
            files = read_directory(source, policy)
            data = build_zip(name, files)
            path = args.output_dir / f"{name}-{report['version']}.zip"
            helpers.write_output(path, data, source)
            restored = read_archive(path, name, policy)
            require(restored == files, 'Archive differs from source')
            validate_files(name, restored, policy)
            report['archive'] = {'path': str(path), 'sha256': helpers.sha256(data), 'bytes': len(data)}
    elif args.output_dir:
        raise ValueError('--output-dir is only for build')
    print(json.dumps({'packages': reports, 'boundaries': 'Offline only: endpoints are configuration checks, not live discovery. No native-host acceptance, deployment, Events delivery, legal attestation or directory approval is claimed.'}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile, ElementTree.ParseError, ValidationError) as error:
        # JSON/schema failures can include rejected payloads. Do not echo them.
        print('Package validation failed: ' + ('Schema validation failed' if isinstance(error, ValidationError) else 'Invalid package data' if isinstance(error, (KeyError, TypeError, UnicodeError)) else str(error)), file=sys.stderr)
        sys.exit(1)
