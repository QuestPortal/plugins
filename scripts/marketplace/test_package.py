import json
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

import package


class MarketplaceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(package.ROOT / 'plugins', self.root / 'plugins')
        shutil.copytree(package.ROOT / '.agents', self.root / '.agents')
        self.policies = package.decode_json(package.POLICIES.read_bytes())

    def mutate_json(self, path, mutate):
        value = json.loads(path.read_text())
        mutate(value)
        path.write_text(json.dumps(value))

    def test_catalog_and_all_packages(self):
        reports = package.validate_catalog(self.root)
        self.assertEqual({r['name'] for r in reports}, set(self.policies))

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

    def test_every_package_rejects_parity_endpoint_identity_and_missing_files(self):
        for name, policy in self.policies.items():
            original = package.read_directory(self.root / 'plugins' / name, policy)
            changes = [
                ('.codex-plugin/plugin.json', lambda m: m.update(version='99.0.0')),
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
