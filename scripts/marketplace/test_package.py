import json
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch
from pathlib import Path

import package


class MarketplaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(package.ROOT / 'plugins', self.root / 'plugins')
        shutil.copytree(package.ROOT / 'codex-plugins', self.root / 'codex-plugins')
        shutil.copytree(package.ROOT / '.agents', self.root / '.agents')
        shutil.copytree(package.ROOT / '.claude-plugin', self.root / '.claude-plugin')
        self.policies = package.decode_json(package.POLICIES.read_bytes())

    def mutate_json(self, path, mutate):
        value = json.loads(path.read_text())
        mutate(value)
        path.write_text(json.dumps(value))

    def test_catalog_and_all_packages(self):
        reports = package.validate_catalog(self.root)
        self.assertEqual({r['name'] for r in reports}, set(self.policies))

    def test_codex_generation_is_exact_and_repeatable(self):
        shutil.rmtree(self.root / 'codex-plugins')
        package.generate_codex_bundles(self.root)
        package.validate_catalog(self.root)
        for name in package.CODEX_PACKAGES:
            source = package.read_directory(self.root / 'plugins' / name, self.policies[name])
            expected = package.codex_files(source)
            self.assertFalse(package.PORTABLE_ONLY_FILES & expected.keys())
            actual = package.read_directory(self.root / 'codex-plugins' / name, {'files': list(expected)})
            self.assertEqual(actual, expected)
        package.generate_codex_bundles(self.root)
        package.validate_catalog(self.root)

    def test_codex_rejects_portable_markers_and_unexpected_files(self):
        for name in package.CODEX_PACKAGES:
            for filename in ['plugin.json', 'mcp.json', '.claude-plugin/plugin.json', 'extra.md']:
                with self.subTest(name=name, filename=filename):
                    path = self.root / 'codex-plugins' / name / filename
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text('{}')
                    with self.assertRaises(ValueError):
                        package.validate_catalog(self.root)
                    with self.assertRaises(ValueError):
                        package.generate_codex_bundles(self.root)
                    path.unlink()
                    if filename.startswith('.claude-plugin/'):
                        path.parent.rmdir()

    def test_codex_rejects_stale_or_missing_copies_and_generator_repairs(self):
        for name in package.CODEX_PACKAGES:
            for filename in self.policies[name]['files']:
                if filename in package.PORTABLE_ONLY_FILES:
                    continue
                path = self.root / 'codex-plugins' / name / filename
                for change in ['stale', 'missing']:
                    with self.subTest(name=name, filename=filename, change=change):
                        if change == 'stale':
                            path.write_bytes(path.read_bytes() + b'\nchanged')
                        else:
                            path.unlink()
                        with self.assertRaises(ValueError):
                            package.validate_catalog(self.root)
                        package.generate_codex_bundles(self.root)
                        package.validate_catalog(self.root)

    def test_codex_generation_adds_new_reviewed_canonical_reference(self):
        name = 'dnd-plugin'
        reference = 'skills/character-sheet/references/new-guide.md'
        (self.root / 'plugins' / name / reference).write_text('New reviewed guide.\n')
        policies = json.loads(json.dumps(self.policies))
        policies[name]['files'].append(reference)
        with patch.object(package, 'policy_for', side_effect=policies.__getitem__):
            package.generate_codex_bundles(self.root)
        self.assertEqual(
            (self.root / 'codex-plugins' / name / reference).read_bytes(),
            (self.root / 'plugins' / name / reference).read_bytes(),
        )

    def test_codex_check_never_repairs_drift(self):
        path = self.root / 'codex-plugins/dnd-plugin/assets/icon.svg'
        path.write_bytes(path.read_bytes() + b'\nstale')
        before = path.read_bytes()
        result = subprocess.run([sys.executable, package.__file__, 'generate-codex', '--check', '--root', str(self.root)], capture_output=True)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(path.read_bytes(), before)

    def test_all_archives_round_trip_deterministically(self):
        for name, policy in self.policies.items():
            with self.subTest(name=name):
                files = package.read_directory(self.root / 'plugins' / name, policy)
                archive = package.build_zip(name, files)
                self.assertEqual(archive, package.build_zip(name, dict(reversed(list(files.items())))))
                path = self.root / (name + '.zip')
                path.write_bytes(archive)
                restored = package.read_archive(path, name, policy)
                self.assertEqual(restored, files)
                package.validate_files(name, restored, policy)

    def test_native_archive_builds_round_trip_and_preserve_portable_archives(self):
        output = self.root / 'artifacts'
        result = subprocess.run([sys.executable, package.__file__, 'build', '--root', str(self.root), '--output-dir', str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list(output.glob('*.zip'))), len(self.policies) + len(package.CODEX_PACKAGES))
        for name in package.CODEX_PACKAGES:
            policy = self.policies[name]
            source = package.read_directory(self.root / 'plugins' / name, policy)
            expected = package.codex_files(source)
            path = output / f"{name}-{policy['version']}-codex.zip"
            self.assertEqual(path.read_bytes(), package.build_zip(name, expected))
            self.assertEqual(package.read_archive(path, name, {'files': list(expected)}), expected)
            portable = output / f"{name}-{policy['version']}.zip"
            self.assertEqual(package.read_archive(portable, name, policy), source)

    def test_every_package_rejects_parity_endpoint_identity_and_missing_files(self):
        for name, policy in self.policies.items():
            original = package.read_directory(self.root / 'plugins' / name, policy)
            changes = [
                ('.codex-plugin/plugin.json', lambda m: m.update(version='99.0.0')),
                ('.claude-plugin/plugin.json', lambda m: m.update(version='99.0.0')),
                ('.claude-plugin/plugin.json', lambda m: m.update(mcpServers='./other.json')),
                ('plugin.json', lambda m: m.update(name='alternate-plugin')),
                ('plugin.json', lambda m: m.update(apps='./.app.json')),
                ('plugin.json', lambda m: m['extensions']['com.openai']['interface'].update(defaultPrompt='changed')),
                ('plugin.json', lambda m: m['extensions']['com.openai']['interface'].update(logo='../escape.svg')),
                ('mcp.json', lambda m: m['mcpServers'][policy['server']].update(url='https://unexpected.example/mcp')),
                ('.mcp.json', lambda m: m['mcpServers'][policy['server']].update(type='streamable-http')),
            ]
            for path, mutate in changes:
                with self.subTest(name=name, path=path):
                    files = dict(original)
                    value = json.loads(files[path]); mutate(value)
                    files[path] = json.dumps(value).encode()
                    with self.assertRaises((ValueError, package.ValidationError)):
                        package.validate_files(name, files, policy)
            files = dict(original); del files['assets/icon.svg']
            with self.assertRaises(ValueError):
                package.validate_files(name, files, policy)

    def test_catalog_rejects_duplicates_alternates_paths_and_bindings(self):
        path = self.root / '.agents/plugins/marketplace.json'
        original = path.read_bytes()
        for mutate in [lambda m: m['plugins'].append(m['plugins'][0]),
                       lambda m: m['plugins'][0].update(name='pendragon2-plugin'),
                       lambda m: m['plugins'][0]['source'].update(path='../escape'),
                       lambda m: m['plugins'][0].update(pluginId='unverified-id')]:
            self.mutate_json(path, mutate)
            with self.assertRaises(ValueError): package.validate_catalog(self.root)
            path.write_bytes(original)
        claude = self.root / '.claude-plugin/marketplace.json'
        original = claude.read_bytes()
        for mutate in [lambda m: m['plugins'].append(m['plugins'][0]),
                       lambda m: m['plugins'][0].update(source='../escape'),
                       lambda m: m['plugins'][0].update(source={'source': 'github', 'repo': 'other/repo'}),
                       lambda m: m['plugins'][0].update(description='changed'),
                       lambda m: m['plugins'].reverse(),
                       lambda m: m.update(owner={'name': 'Someone else'})]:
            self.mutate_json(claude, mutate)
            with self.assertRaises(ValueError): package.validate_catalog(self.root)
            claude.write_bytes(original)
        claude.unlink()
        with self.assertRaises(ValueError): package.validate_catalog(self.root)

    def test_source_rejects_symlinks_untracked_files_and_empty_directories(self):
        source = self.root / 'plugins/dnd-plugin'
        extra = source / 'unreviewed'
        extra.mkdir()
        with self.assertRaises(ValueError): package.validate_catalog(self.root)
        extra.rmdir(); extra.write_text('unexpected')
        with self.assertRaises(ValueError): package.validate_catalog(self.root)
        extra.unlink(); extra.symlink_to(self.root / 'outside')
        with self.assertRaises(ValueError): package.validate_catalog(self.root)
        extra.unlink()
        renamed = self.root / 'actual-dnd'; source.rename(renamed); source.symlink_to(renamed)
        with self.assertRaises(ValueError): package.validate_catalog(self.root)

    def test_archive_rejects_traversal_duplicates_symlinks_and_bombs(self):
        name = 'dnd-plugin'; policy = self.policies[name]
        files = package.read_directory(self.root / 'plugins' / name, policy)
        for mode in ('escape','duplicate','symlink','size','mixed'):
            with self.subTest(mode=mode):
                path = self.root / 'bad.zip'
                with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
                    for i,(filename,data) in enumerate(files.items()):
                        target = name + '/' + filename
                        info = zipfile.ZipInfo(target)
                        if i == 0:
                            if mode == 'escape': info.filename = name + '/../escape'
                            if mode == 'duplicate': info.filename = name + '/' + list(files)[1]
                            if mode == 'symlink': info.external_attr = (stat.S_IFLNK | 0o777) << 16
                            if mode == 'size': data = b'x' * (package.MAX_FILE + 1)
                            if mode == 'mixed': info.filename = filename
                        z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED)
                with self.assertRaises(ValueError): package.read_archive(path,name,policy)

    def test_unsafe_icon_and_skill_references(self):
        name='call-of-cthulhu-plugin';policy=self.policies[name]
        files=package.read_directory(self.root/'plugins'/name,policy)
        for icon in [b'<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><script/></svg>',
                     b'<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" onload="bad()"/>',
                     b'<!DOCTYPE svg [<!ENTITY external SYSTEM "file:///tmp/x">]><svg/>']:
            altered=dict(files);altered['assets/icon.svg']=icon
            with self.assertRaises(ValueError): package.validate_files(name,altered,policy)
        for link in ['../../../../outside.md','file:///tmp/x','missing.md']:
            altered=dict(files);altered['skills/investigator-sheet/SKILL.md']+=f'\n[bad]({link})\n'.encode()
            with self.assertRaises(ValueError): package.validate_files(name,altered,policy)

    def test_cthulhu_review_materials_required(self):
        name='call-of-cthulhu-plugin';policy=self.policies[name]
        original=package.read_directory(self.root/'plugins'/name,policy)
        for mutation in [lambda e:e['review'].pop('demo_recording_url'),lambda e:e['review']['test_cases'].update(positive=[]),lambda e:e['interface'].pop('privacyPolicyURL')]:
            files=dict(original);manifest=json.loads(files['plugin.json']);mutation(manifest['extensions']['com.openai']);files['plugin.json']=json.dumps(manifest).encode()
            with self.assertRaises(ValueError):package.validate_files(name,files,policy)

    def test_questportal_review_materials_required(self):
        name='questportal-plugin';policy=self.policies[name]
        original=package.read_directory(self.root/'plugins'/name,policy)
        for mutation in [lambda e:e['review']['test_cases'].update(negative=[]),lambda e:e['review'].update(commerce=True),lambda e:e['interface'].pop('termsOfServiceURL')]:
            files=dict(original);manifest=json.loads(files['plugin.json']);mutation(manifest['extensions']['com.openai']);files['plugin.json']=json.dumps(manifest).encode()
            with self.assertRaises(ValueError):package.validate_files(name,files,policy)

    def test_secret_rejected_without_echo(self):
        marker='ghp_'+'syntheticNeverValid'*3
        skill=self.root/'plugins/dnd-plugin/skills/character-sheet/SKILL.md'
        skill.write_text(skill.read_text()+'\n'+marker)
        result=subprocess.run([sys.executable,package.__file__,'validate','--root',str(self.root)],capture_output=True,text=True)
        self.assertEqual(result.returncode,1)
        self.assertNotIn(marker,result.stdout+result.stderr)

    def test_duplicate_json_and_oversized_files(self):
        manifest=self.root/'plugins/dnd-plugin/plugin.json'
        original=manifest.read_bytes()
        manifest.write_bytes(original.replace(b'"name":',b'"name":"duplicate", "name":',1))
        with self.assertRaises(ValueError):package.validate_catalog(self.root)
        manifest.write_bytes(b'x'*(package.MAX_FILE+1))
        with self.assertRaises(ValueError):package.validate_catalog(self.root)

    def test_outputs_preserve_existing_work_and_source(self):
        source=self.root/'plugins/dnd-plugin';out=self.root/'out.zip'
        package.helpers.write_output(out,b'first',source)
        package.helpers.write_output(out,b'first',source)
        with self.assertRaises(ValueError):package.helpers.write_output(out,b'second',source)
        with self.assertRaises(ValueError):package.helpers.write_output(source/'bad.zip',b'bad',source)
        link=self.root/'link.zip';link.symlink_to(out)
        with self.assertRaises(ValueError):package.helpers.write_output(link,b'first',source)


if __name__ == '__main__': unittest.main()
