"""Offline package, catalog, containment and reproducibility regressions."""

import copy
import io
import json
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import package


SOURCE = Path(__file__).resolve().parents[2] / "plugins" / package.NAME


class BattlemapPackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="battlemap-package-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / package.NAME
        shutil.copytree(SOURCE, self.source)
        self.files = package.read_directory(self.source)

    def update_json(self, name, change):
        value = json.loads(self.files[name])
        change(value)
        self.files[name] = json.dumps(value).encode()

    def archive(self, entries, name="fixture.zip"):
        result = self.root / name
        with zipfile.ZipFile(result, "w") as bundle:
            for entry, data in entries:
                bundle.writestr(entry, data)
        return result

    def test_official_schemas_parity_inventory_and_marketplace_pass_offline(self):
        with patch("socket.socket", side_effect=AssertionError("Validation attempted networking")):
            report = package.validate_files(self.files)
            marketplace = package.validate_marketplace(package.MARKETPLACE)
            claude_marketplace = package.validate_marketplace(package.CLAUDE_MARKETPLACE, kind="claude")
        self.assertEqual(report["version"], json.loads(self.files["plugin.json"])["version"])
        self.assertEqual(len(report["files"]), 9)
        self.assertEqual(claude_marketplace["entry"]["source"], f"./plugins/{package.NAME}")
        self.assertEqual(report["icon"]["width"], 100)
        self.assertEqual(marketplace["entry"]["source"]["path"], f"./plugins/{package.NAME}")
        self.assertEqual(report["schemas"]["plugin"]["sha256"], package.helpers.SCHEMA_HASHES["plugin"])

    def test_both_zip_layouts_are_reproducible_and_byte_match_all_hidden_files(self):
        for layout in ("wrapped", "portable"):
            with self.subTest(layout=layout):
                first = package.build_zip(self.files, layout)
                for path in self.source.rglob("*"):
                    if path.is_file():
                        path.chmod(0o600)
                        path.touch()
                reversed_files = dict(reversed(list(package.read_directory(self.source).items())))
                self.assertEqual(first, package.build_zip(reversed_files, layout))
                archive = self.root / f"{layout}.zip"
                archive.write_bytes(first)
                restored = package.read_archive(archive)
                self.assertEqual(restored, self.files)
                self.assertIn(".codex-plugin/plugin.json", restored)
                self.assertIn(".claude-plugin/plugin.json", restored)
                self.assertIn(".mcp.json", restored)
                with zipfile.ZipFile(io.BytesIO(first)) as bundle:
                    names = bundle.namelist()
                    self.assertEqual(names, sorted(names))
                    self.assertEqual(names[0].startswith(f"{package.NAME}/"), layout == "wrapped")
                    for entry in bundle.infolist():
                        self.assertEqual(entry.date_time, (1980, 1, 1, 0, 0, 0))
                        self.assertEqual(entry.external_attr >> 16, stat.S_IFREG | 0o644)
                        self.assertEqual(entry.compress_type, zipfile.ZIP_STORED)

    def test_official_schema_and_snapshot_integrity_are_enforced(self):
        self.update_json("plugin.json", lambda value: value.update(author="wrong type"))
        with self.assertRaises(package.ValidationError):
            package.validate_files(self.files)
        with patch.dict(package.helpers.SCHEMA_HASHES, {"plugin": "0" * 64}):
            with self.assertRaisesRegex(ValueError, "Pinned plugin schema changed"):
                package.fixed_schema("plugin")

    def test_manifest_identity_prompt_version_and_endpoint_drift_are_rejected(self):
        cases = (
            (".codex-plugin/plugin.json", lambda value: value.update(version="0.0.0"), "manifest.*differ"),
            (".claude-plugin/plugin.json", lambda value: value.update(version="0.0.0"), "Claude manifest.*differ"),
            ("plugin.json", lambda value: value["extensions"]["com.openai"]["interface"]["defaultPrompt"].reverse(), "Default prompts changed"),
            ("plugin.json", lambda value: value.update(name="another-plugin"), "Plugin identity changed"),
            ("mcp.json", lambda value: value["mcpServers"]["battlemap"].update(url="https://example.invalid/mcp"), "endpoint"),
            (".mcp.json", lambda value: value["mcpServers"]["battlemap"].update(type="streamable-http"), "Compatibility MCP"),
            ("mcp.json", lambda value: value["mcpServers"]["battlemap"].update(headers={"Authorization": "synthetic"}), "fields changed"),
        )
        original = dict(self.files)
        for name, change, message in cases:
            with self.subTest(name=name, message=message):
                self.files = dict(original)
                self.update_json(name, change)
                with self.assertRaisesRegex(ValueError, message):
                    package.validate_files(self.files)

    def test_marketplace_requires_one_exact_local_entry_and_unique_names(self):
        original = json.loads(package.MARKETPLACE.read_bytes())
        wrong_source = copy.deepcopy(original)
        entry = next(item for item in wrong_source["plugins"] if item["name"] == package.NAME)
        entry["source"]["path"] = "../escape"
        duplicate = copy.deepcopy(original)
        duplicate["plugins"].append(next(item for item in duplicate["plugins"] if item["name"] == package.NAME))
        missing = copy.deepcopy(original)
        missing["plugins"] = [item for item in missing["plugins"] if item["name"] != package.NAME]
        for catalog in (wrong_source, duplicate, missing):
            path = self.root / "marketplace.json"
            path.write_text(json.dumps(catalog))
            with self.assertRaises(ValueError):
                package.validate_marketplace(path)
        claude = json.loads(package.CLAUDE_MARKETPLACE.read_bytes())
        for change in (lambda c: c["plugins"][0].update(source="../escape"), lambda c: c.update(owner={"name": "Someone else"})):
            altered = copy.deepcopy(claude)
            altered["plugins"] = [next(item for item in altered["plugins"] if item["name"] == package.NAME)]
            change(altered)
            claude_path = self.root / ".claude-plugin" / "marketplace.json"
            claude_path.parent.mkdir(exist_ok=True)
            claude_path.write_text(json.dumps(altered))
            with self.assertRaises(ValueError):
                package.validate_marketplace(claude_path, kind="claude")
        with self.assertRaises(ValueError):
            package.validate_marketplace(package.CLAUDE_MARKETPLACE)
        copied = self.root / "renamed-claude-catalog.json"
        copied.write_bytes(package.CLAUDE_MARKETPLACE.read_bytes())
        self.assertEqual(package.validate_marketplace(copied, kind="claude")["entry"]["source"], f"./plugins/{package.NAME}")
        path.write_text('{"name":"questportal-plugins","name":"duplicate","plugins":[]}')
        with self.assertRaisesRegex(ValueError, "duplicate JSON"):
            package.validate_marketplace(path)

    def test_source_symlinks_unknown_files_empty_directories_and_size_are_rejected(self):
        icon = self.source / "assets/icon.svg"
        icon.unlink()
        icon.symlink_to(SOURCE / "assets/icon.svg")
        with self.assertRaisesRegex(ValueError, "symlinks"):
            package.read_directory(self.source)
        icon.unlink()
        icon.write_bytes(self.files["assets/icon.svg"])
        for name in (".env", "README.md"):
            (self.source / name).write_text("synthetic fixture")
            with self.assertRaisesRegex(ValueError, "unexpected file"):
                package.read_directory(self.source)
            (self.source / name).unlink()
        (self.source / "unreviewed").mkdir()
        with self.assertRaisesRegex(ValueError, "unexpected directory"):
            package.read_directory(self.source)
        (self.source / "unreviewed").rmdir()
        with patch.object(package, "MAX_FILE_BYTES", 20):
            with self.assertRaisesRegex(ValueError, "size bound"):
                package.read_directory(self.source)

    def test_archive_traversal_duplicates_symlinks_mixed_layouts_and_bounds_are_rejected(self):
        original = list(self.files.items())
        for path in ("../escape", "/absolute", f"{package.NAME}/../escape", "assets\\icon.svg"):
            entries = [(path, original[0][1]), *original[1:]]
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "escaping path"):
                package.read_archive(self.archive(entries))
        self.assertFalse((self.root / "escape").exists())
        # Duplicate paths with the same count must not conceal a missing required file.
        duplicate = [(original[1][0], original[0][1]), *original[1:]]
        with self.assertWarns(UserWarning):
            duplicate_path = self.archive(duplicate)
        with self.assertRaisesRegex(ValueError, "duplicate paths"):
            package.read_archive(duplicate_path)
        link = zipfile.ZipInfo(original[0][0])
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        with self.assertRaisesRegex(ValueError, "symlinks"):
            package.read_archive(self.archive([(link, b"../../outside"), *original[1:]]))
        wrapped = [(f"{package.NAME}/{name}", data) for name, data in original]
        wrapped[-1] = original[-1]
        with self.assertRaisesRegex(ValueError, "mixes root"):
            package.read_archive(self.archive(wrapped))
        archive = self.archive(original)
        with patch.object(package, "MAX_FILE_BYTES", 20):
            with self.assertRaisesRegex(ValueError, "entry size"):
                package.read_archive(archive)
        with patch.object(package, "MAX_PACKAGE_BYTES", 20):
            with self.assertRaisesRegex(ValueError, "size bound"):
                package.read_archive(archive)

    def test_contained_onboarding_skills_and_static_svg_are_required(self):
        self.update_json("plugin.json", lambda value: value["extensions"]["com.openai"].update(onboardingSkill="../outside/SKILL.md"))
        with self.assertRaisesRegex(ValueError, "Onboarding reference"):
            package.validate_files(self.files)
        original = package.read_directory(SOURCE)
        for suffix in ("\n[escape](../../outside.md)\n", "\n[remote](https://example.invalid/skill.md)\n", "\n[missing](missing.md)\n"):
            self.files = dict(original)
            self.files["skills/onboarding/SKILL.md"] += suffix.encode()
            with self.assertRaisesRegex(ValueError, "Skill (links|reference)"):
                package.validate_files(self.files)
        self.files = dict(original)
        self.files["skills/onboarding/SKILL.md"] = original["skills/onboarding/SKILL.md"].replace(b"name: onboarding", b"name: another")
        with self.assertRaisesRegex(ValueError, "Skill name/description"):
            package.validate_files(self.files)
        for svg in (
            '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"><image href="https://example.invalid/image.svg"/></svg>',
            '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"><g clip-path="url(https://example.invalid/svg#clip)"/></svg>',
            '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"><g clip-path="url(#missing)"/></svg>',
            '<!DOCTYPE svg [<!ENTITY x "fixture">]><svg xmlns="http://www.w3.org/2000/svg" width="512" height="512"/>',
        ):
            self.files = dict(original)
            self.files["assets/icon.svg"] = svg.encode()
            with self.assertRaises(ValueError):
                package.validate_files(self.files)

    def test_known_credential_material_is_rejected_without_echoing_values(self):
        marker = "ghp_" + "syntheticTokenNeverValid" * 3
        skill = self.source / "skills/onboarding/SKILL.md"
        skill.write_bytes(self.files["skills/onboarding/SKILL.md"] + f"\n{marker}\n".encode())
        result = subprocess.run([sys.executable, str(Path(package.__file__)), "validate", str(self.source)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Possible credential material", result.stderr)
        self.assertNotIn(marker, result.stdout + result.stderr)
        for secret in ("-----BEGIN PRIVATE KEY-----", "secret=synthetic-secret-value", "Bearer " + "synthetic" * 4):
            files = dict(self.files)
            files["skills/onboarding/SKILL.md"] += ("\n" + secret).encode()
            with self.assertRaisesRegex(ValueError, "Possible credential material"):
                package.validate_files(files)

    def test_output_never_overwrites_different_artifacts_or_writes_into_source(self):
        output = self.root / "package.zip"
        package.write_output(output, b"same", self.source)
        package.write_output(output, b"same", self.source)
        with self.assertRaisesRegex(ValueError, "Refusing to overwrite"):
            package.write_output(output, b"different", self.source)
        with self.assertRaisesRegex(ValueError, "outside the source"):
            package.write_output(self.source / "artifact.zip", b"not written", self.source)
        self.assertFalse((self.source / "artifact.zip").exists())
        link = self.root / "link.zip"
        link.symlink_to(output)
        with self.assertRaisesRegex(ValueError, "symlink"):
            package.write_output(link, b"same", self.source)

    def test_cli_build_reports_catalog_and_verifies_written_archive_then_validates_it(self):
        output = self.root / "battlemap.zip"
        report_path = self.root / "report.json"
        result = subprocess.run([
            sys.executable, str(Path(package.__file__)), "build", str(self.source),
            "--output", str(output), "--report", str(report_path),
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(report_path.read_bytes())
        self.assertEqual(report["archive"]["layout"], "wrapped")
        self.assertEqual(report["archive"]["sha256"], package.sha256(output.read_bytes()))
        self.assertEqual(report["marketplace"]["entry"]["name"], package.NAME)
        self.assertEqual(report["claudeMarketplace"]["entry"]["source"], f"./plugins/{package.NAME}")
        self.assertEqual(package.read_archive(output), self.files)
        broken = self.root / "broken-claude.json"
        broken.write_text('{"name":"questportal-plugins","owner":{"name":"Quest Portal"},"plugins":[]}')
        rejected = subprocess.run([sys.executable, str(Path(package.__file__)), "validate", str(self.source), "--claude-marketplace", str(broken)], capture_output=True, text=True)
        self.assertEqual(rejected.returncode, 1)
        missing = subprocess.run([sys.executable, str(Path(package.__file__)), "validate", str(self.source), "--claude-marketplace", str(self.root / "absent.json")], capture_output=True, text=True)
        self.assertEqual(missing.returncode, 1)
        validated = subprocess.run([sys.executable, str(Path(package.__file__)), "validate", str(output)], capture_output=True, text=True)
        self.assertEqual(validated.returncode, 0, validated.stderr)
        self.assertEqual(json.loads(validated.stdout)["archive"]["sha256"], report["archive"]["sha256"])


if __name__ == "__main__":
    unittest.main()
