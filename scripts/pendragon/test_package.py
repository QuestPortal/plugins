"""Focused regressions for release drift, unsafe inputs, and reproducibility."""

import json
import shutil
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

import package


SOURCE = Path(__file__).resolve().parents[2] / "plugins" / package.NAME


class PendragonPackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="pendragon-package-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / package.NAME
        shutil.copytree(SOURCE, self.source)

    def test_build_is_deterministic_and_preserves_hidden_compatibility_files(self):
        files = package.read_directory(self.source)
        report = package.validate_files(files)
        self.assertEqual(report["version"], "0.1.1")
        first = package.build_zip(files)
        for path in self.source.rglob("*"):
            if path.is_file():
                path.chmod(0o600)
                path.touch()
        second = package.build_zip(package.read_directory(self.source))
        self.assertEqual(first, second)
        archive = self.root / "package.zip"
        archive.write_bytes(first)
        restored = package.read_archive(archive)
        self.assertEqual(restored, files)
        self.assertIn(".codex-plugin/plugin.json", restored)
        self.assertIn(".mcp.json", restored)

    def test_rejects_manifest_version_drift_and_prompt_changes(self):
        files = package.read_directory(self.source)
        compatibility = json.loads(files[".codex-plugin/plugin.json"])
        compatibility["version"] = "0.1.0"
        files[".codex-plugin/plugin.json"] = json.dumps(compatibility).encode()
        with self.assertRaisesRegex(ValueError, "manifest.*differ"):
            package.validate_files(files)
        files = package.read_directory(self.source)
        manifest = json.loads(files["plugin.json"])
        manifest["extensions"]["com.openai"]["interface"]["defaultPrompt"].reverse()
        files["plugin.json"] = json.dumps(manifest).encode()
        with self.assertRaisesRegex(ValueError, "Default prompts changed"):
            package.validate_files(files)

    def test_rejects_source_symlinks_and_unreviewed_files(self):
        (self.source / "assets" / "icon.svg").unlink()
        (self.source / "assets" / "icon.svg").symlink_to(SOURCE / "assets" / "icon.svg")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            package.read_directory(self.source)
        files = package.read_directory(SOURCE)
        files[".env"] = b"synthetic=not-a-secret\n"
        with self.assertRaisesRegex(ValueError, "reviewed Pendragon file list"):
            package.validate_files(files)

    def test_rejects_archive_traversal_and_symlinks_without_extracting(self):
        traversal = self.root / "traversal.zip"
        with zipfile.ZipFile(traversal, "w") as archive:
            archive.writestr(f"{package.NAME}/../escape", "unsafe")
        with self.assertRaisesRegex(ValueError, "escaping path"):
            package.read_archive(traversal)
        self.assertFalse((self.root / "escape").exists())
        symlink = self.root / "symlink.zip"
        with zipfile.ZipFile(symlink, "w") as archive:
            entry = zipfile.ZipInfo(f"{package.NAME}/assets/icon.svg")
            entry.create_system = 3
            entry.external_attr = (stat.S_IFLNK | 0o777) << 16
            archive.writestr(entry, "../../outside.svg")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            package.read_archive(symlink)

    def test_rejects_remote_artwork_and_duplicate_json_keys(self):
        files = package.read_directory(SOURCE)
        files["assets/icon.svg"] = b'<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><image href="https://example.invalid/icon.svg"/></svg>'
        with self.assertRaisesRegex(ValueError, "static local artwork"):
            package.validate_files(files)
        with self.assertRaisesRegex(ValueError, "Duplicate JSON key"):
            package.decode_json('{"version":"0.1.1","version":"0.1.0"}')

    def test_rejects_encoded_svg_declarations_and_css_escape_references(self):
        files = package.read_directory(SOURCE)
        files["assets/icon.svg"] = '<!DOCTYPE svg [<!ENTITY x "hidden declaration">]><svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><title>&x;</title></svg>'.encode("utf-16")
        with self.assertRaisesRegex(ValueError, "UTF-8"):
            package.validate_files(files)
        for attribute in ('style="fill: u\\72l(https://example.invalid/art.svg#x)"', 'fill="u\\72l(https://example.invalid/art.svg#x)"'):
            files["assets/icon.svg"] = f'<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><path d="M0 0" {attribute}/></svg>'.encode()
            with self.assertRaises(ValueError):
                package.validate_files(files)


if __name__ == "__main__":
    unittest.main()
