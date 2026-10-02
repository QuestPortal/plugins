#!/usr/bin/env python3
"""Validate/build Battlemap offline from this marketplace; never connect or publish."""

from __future__ import annotations

import argparse
import importlib.util
import io
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree

from jsonschema import Draft202012Validator, ValidationError

# Share the existing pinned schema snapshots and small generic release helpers.
# No code or schemas are downloaded by validation or packaging.
SCRIPTS = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("pendragon_release_helpers", SCRIPTS / "pendragon/package.py")
helpers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helpers)
require = helpers.require
sha256 = helpers.sha256
fixed_schema = helpers.fixed_schema

NAME = "quest-portal-battlemap"
ENDPOINT = "https://quest-portal-battlemap.quest-portal.workers.dev/mcp"
MARKETPLACE = SCRIPTS.parent / ".agents/plugins/marketplace.json"
SKILLS = ("build-map", "onboarding", "run-encounter")
FILES = (
    ".codex-plugin/plugin.json", ".mcp.json", "assets/icon.svg", "mcp.json",
    "plugin.json", *(f"skills/{name}/SKILL.md" for name in SKILLS),
)
DIRECTORIES = {str(parent) for name in FILES for parent in PurePosixPath(name).parents if str(parent) != "."}
DEFAULT_PROMPTS = [
    "Open my battlemaps.",
    "Create a ruined chapel encounter with four heroes and three skeletons.",
    "Help me run the sample encounter.",
]
MAX_FILE_BYTES = helpers.MAX_FILE_BYTES
MAX_PACKAGE_BYTES = helpers.MAX_PACKAGE_BYTES
CREDENTIAL_PATTERNS = (
    r"-----BEGIN (?:[A-Z0-9 ]* )?PRIVATE KEY-----",
    r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    r"\b(?:sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b",
    r"\b(?:Bearer|Basic)\s+[A-Za-z0-9+/_.=-]{16,}",
    r"(?i)\b(?:api[_-]?key|secret|password|access[_-]?token|refresh[_-]?token)\b[\"']?\s*[:=]\s*[\"']?[^\s\"',;}{]{8,}",
)


def decode_json(data):
    try:
        return helpers.decode_json(data)
    except ValueError as error:
        raise ValueError("Invalid JSON encoding or duplicate JSON keys") from error


def write_output(path, data, source):
    require(not path.is_symlink(), "Output may not be a symlink")
    return helpers.write_output(path, data, source)


def validate_marketplace(path):
    require(not path.is_symlink() and path.is_file(), "Marketplace must be a regular local file")
    require(path.stat().st_size <= MAX_FILE_BYTES, "Marketplace exceeds size bound")
    catalog = decode_json(path.read_bytes())
    require(isinstance(catalog, dict) and catalog.get("name") == "questportal-plugins", "Unexpected marketplace identity")
    entries = catalog.get("plugins")
    require(isinstance(entries, list) and all(isinstance(entry, dict) for entry in entries), "Invalid marketplace plugin list")
    names = [entry.get("name") for entry in entries]
    require(all(isinstance(name, str) for name in names) and len(names) == len(set(names)), "Marketplace plugin names must be unique strings")
    matches = [entry for entry in entries if entry.get("name") == NAME]
    require(matches == [{"name": NAME, "source": {"source": "local", "path": f"./plugins/{NAME}"}}], "Marketplace must contain exactly the reviewed local Battlemap entry")
    return {"name": catalog["name"], "entry": matches[0], "sha256": sha256(path.read_bytes())}


def validate_icon(data):
    try:
        text = data.decode("utf8")
    except UnicodeError as error:
        raise ValueError("SVG must be UTF-8 text") from error
    require("\x00" not in text, "SVG must be UTF-8 text without null characters")
    require("<!DOCTYPE" not in text.upper() and "<!ENTITY" not in text.upper(), "Unsafe SVG declaration")
    svg = ElementTree.fromstring(text)
    require(svg.tag == "{http://www.w3.org/2000/svg}svg", "Expected SVG icon")
    width, height = int(svg.attrib["width"]), int(svg.attrib["height"])
    require(width == height and 48 <= width <= 4096, "Icon must be square and at least 48 pixels")
    ids, references = set(), set()
    for element in svg.iter():
        require(element.tag in {f"{{http://www.w3.org/2000/svg}}{tag}" for tag in (
            "svg", "g", "defs", "clipPath", "path", "circle", "rect", "line", "polygon", "polyline", "ellipse", "title", "desc",
        )}, "SVG must contain static local artwork only")
        require(set(element.attrib) <= {
            "width", "height", "viewBox", "fill", "stroke", "stroke-width", "stroke-linejoin", "stroke-linecap",
            "d", "cx", "cy", "r", "rx", "ry", "x", "y", "x1", "y1", "x2", "y2", "points", "opacity",
            "fill-opacity", "stroke-opacity", "id", "clip-path", "transform",
        }, "SVG contains an unreviewed attribute")
        for key, value in element.attrib.items():
            require("\\" not in value, "SVG may not use CSS escapes")
            if key == "clip-path":
                match = re.fullmatch(r"url\(#([A-Za-z][\w-]*)\)", value)
                require(match is not None, "SVG references must be local fragment IDs")
                references.add(match[1])
            else:
                require("url(" not in value.lower(), "SVG references must be local fragment IDs")
            if key == "id":
                require(re.fullmatch(r"[A-Za-z][\w-]*", value) and value not in ids, "Invalid or duplicate SVG ID")
                ids.add(value)
            if key in {"fill", "stroke"}:
                require(re.fullmatch(r"(?:none|currentColor|white|black|transparent|#[0-9a-fA-F]{3,8})", value), "SVG paints must be static colors")
    require(references <= ids, "SVG references an absent fragment")
    return {"width": width, "height": height, "sha256": sha256(data)}


def validate_files(files):
    require(set(files) == set(FILES), "Package must contain exactly the reviewed Battlemap file list")
    require(all(0 < len(data) <= MAX_FILE_BYTES for data in files.values()), "Invalid package file size")
    require(sum(map(len, files.values())) <= MAX_PACKAGE_BYTES, "Package exceeds size bound")
    for name, data in files.items():
        text = data.decode("utf8")
        require("\x00" not in text, f"Package text contains null characters: {name}")
        require(not any(re.search(pattern, text) for pattern in CREDENTIAL_PATTERNS), f"Possible credential material in {name}")
    manifest, mcp = decode_json(files["plugin.json"]), decode_json(files["mcp.json"])
    for name, value in (("plugin", manifest), ("mcp", mcp)):
        Draft202012Validator(fixed_schema(name)).validate(value)
    require(set(manifest) == {"$schema", "name", "version", "description", "author", "extensions"}, "Unexpected or missing manifest fields")
    require(manifest["name"] == NAME, "Plugin identity changed")
    require(helpers.SEMVER.fullmatch(manifest.get("version", "")), "Use a stable semantic release version")
    require(manifest["description"].strip(), "Missing plugin description")
    require(manifest["author"] == {"name": "Quest Portal", "url": "https://www.questportal.com"}, "Publisher identity changed")
    require(set(manifest["extensions"]) == {"com.openai"}, "Unexpected manifest extension")
    extension = manifest["extensions"]["com.openai"]
    require(set(extension) == {"interface", "onboardingSkill"}, "Unexpected app binding or extension field")
    require(extension["onboardingSkill"] == "./skills/onboarding/SKILL.md", "Onboarding reference must remain contained")
    interface = extension["interface"]
    require(set(interface) == {
        "displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities",
        "defaultPrompt", "brandColor", "brandColorDark", "logo", "composerIcon",
    }, "Unexpected or missing interface metadata")
    require(interface["displayName"] == "Battlemap by Quest Portal" and interface["developerName"] == "Quest Portal", "Display identity changed")
    require(interface["category"] == "Entertainment" and interface["capabilities"] == ["Interactive", "Read", "Write"], "Existing capabilities or category changed")
    require(interface["defaultPrompt"] == DEFAULT_PROMPTS, "Default prompts changed in value, type, or order")
    require(isinstance(interface["shortDescription"], str) and 0 < len(interface["shortDescription"]) <= 30, "Subtitle must be 1–30 characters")
    require(isinstance(interface["longDescription"], str) and interface["longDescription"].strip(), "Missing long description")
    require(interface["brandColor"] == interface["brandColorDark"] == "#34B4E3", "Brand colors changed")
    require(interface["logo"] == interface["composerIcon"] == "./assets/icon.svg", "Icon reference changed or leaves package")
    require(decode_json(files[".codex-plugin/plugin.json"]) == {
        "name": manifest["name"], "version": manifest["version"], "description": manifest["description"], "author": manifest["author"],
        "skills": "./skills/", "extensions": {"com.openai": {"onboardingSkill": extension["onboardingSkill"]}},
        "interface": interface, "mcpServers": "./.mcp.json",
    }, "Portable and compatibility manifest identity/version/presentation differ")
    require(mcp == {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
        "mcpServers": {"battlemap": {"type": "streamable-http", "url": ENDPOINT}},
    }, "Portable MCP endpoint, transport or fields changed")
    require(decode_json(files[".mcp.json"]) == {"mcpServers": {"battlemap": {"type": "http", "url": ENDPOINT}}}, "Compatibility MCP endpoint or transport differs")
    for name in SKILLS:
        path = f"skills/{name}/SKILL.md"
        text = files[path].decode("utf8")
        require(text.startswith("---\n"), "Missing skill YAML frontmatter")
        header, separator, body = text[4:].partition("\n---\n")
        require(separator and body.strip(), "Missing skill body")
        require(re.fullmatch(rf"name: {name}\ndescription: \S[^\n]+", header), "Skill name/description must match its directory without extra frontmatter")
        for reference in re.findall(r"\]\(([^\s)]+)\)", body):
            require(not re.match(r"(?:[A-Za-z][\w+.-]*:|/|\\)", reference), "Skill links must remain in the package")
            target = PurePosixPath(path).parent / reference
            require(".." not in target.parts and "\\" not in reference and str(target) in files, "Skill reference leaves the package or is missing")
    icon = validate_icon(files["assets/icon.svg"])
    return {
        "status": "valid", "name": NAME, "version": manifest["version"],
        "schemas": {name: {"id": f"https://agent-plugins.org/schemas/1.0.0/{name}.schema.json", "sha256": digest} for name, digest in helpers.SCHEMA_HASHES.items()},
        "compatibilityParity": True, "defaultPromptsPreserved": True, "endpoint": ENDPOINT,
        "subtitleCharacters": len(interface["shortDescription"]), "icon": icon,
        "files": [{"path": name, "bytes": len(files[name]), "sha256": sha256(files[name])} for name in sorted(files)],
        "boundaries": "Offline package/marketplace validation only; no endpoint, installation, host, policy or public-directory approval is claimed. Credential-pattern checks cannot prove the absence of every secret.",
    }


def read_directory(root):
    require(root.name == NAME, "Directory name must match quest-portal-battlemap")
    require(not root.is_symlink() and root.is_dir(), "Package root must be a regular directory, not a symlink")
    files = {}
    total = 0
    for path in root.rglob("*"):
        require(not path.is_symlink(), "Package may not contain symlinks")
        name = path.relative_to(root).as_posix()
        if path.is_dir():
            require(name in DIRECTORIES, "Package contains an unexpected directory")
            continue
        require(name in FILES, "Package contains an unexpected file")
        require(path.is_file(), "Package contains a non-regular file")
        size = path.stat().st_size
        total += size
        require(0 < size <= MAX_FILE_BYTES and total <= MAX_PACKAGE_BYTES, "Package exceeds size bound")
        files[name] = path.read_bytes()
    return files


def read_archive(path):
    require(not path.is_symlink() and path.is_file(), "Archive must be a regular file, not a symlink")
    require(path.stat().st_size <= MAX_PACKAGE_BYTES, "Archive exceeds size bound")
    files = {}
    with zipfile.ZipFile(path) as bundle:
        entries = bundle.infolist()
        require(len(entries) == len(FILES), "Archive must contain exactly the reviewed file count")
        prefix = f"{NAME}/" if entries[0].filename.startswith(f"{NAME}/") else ""
        total = 0
        for entry in entries:
            require(not prefix or entry.filename.startswith(prefix), "Archive mixes root and enclosing-directory layouts")
            name = entry.filename[len(prefix):]
            require(name in FILES, "Archive contains an unexpected or escaping path")
            require(name not in files, "Archive contains duplicate paths")
            mode = stat.S_IFMT(entry.external_attr >> 16)
            require(mode in (0, stat.S_IFREG), "Archive may not contain symlinks or non-regular files")
            total += entry.file_size
            require(not entry.is_dir() and 0 < entry.file_size <= MAX_FILE_BYTES and total <= MAX_PACKAGE_BYTES, "Invalid archive entry size")
            require(not entry.flag_bits & 1, "Encrypted archive entries are not supported")
            require(entry.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED), "Unsupported archive compression")
            files[name] = bundle.read(entry)
    return files


def build_zip(files, layout="wrapped"):
    require(layout in {"wrapped", "portable"}, "Unknown archive layout")
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as bundle:
        for name in sorted(files):
            entry = zipfile.ZipInfo(f"{NAME}/{name}" if layout == "wrapped" else name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            entry.compress_type = zipfile.ZIP_STORED
            bundle.writestr(entry, files[name])
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "build"))
    parser.add_argument("source", type=Path, help="Battlemap source directory or existing ZIP")
    parser.add_argument("--marketplace", type=Path, default=MARKETPLACE, help="Local marketplace catalog (defaults to this repository)")
    parser.add_argument("--layout", choices=("wrapped", "portable"), default="wrapped", help="Build layout; wrapped matches Plugin Creator, portable has plugin.json at root")
    parser.add_argument("--output", type=Path, help="ZIP output outside source (build only)")
    parser.add_argument("--report", type=Path, help="JSON report outside source")
    args = parser.parse_args()
    marketplace = validate_marketplace(args.marketplace)
    files = read_directory(args.source) if args.source.is_dir() else read_archive(args.source)
    report = validate_files(files)
    report["marketplace"] = marketplace
    if args.command == "build":
        require(args.source.is_dir() and args.output, "Build requires a source directory and --output")
        archive = build_zip(files, args.layout)
        write_output(args.output, archive, args.source)
        restored = read_archive(args.output)
        require(restored == files, "Archive does not reproduce validated source bytes")
        validate_files(restored)
        report["archive"] = {"file": args.output.name, "layout": args.layout, "bytes": len(archive), "sha256": sha256(archive)}
    else:
        require(args.output is None, "--output is only for build")
        if args.source.is_file():
            archive = args.source.read_bytes()
            report["archive"] = {"file": args.source.name, "bytes": len(archive), "sha256": sha256(archive)}
    encoded = (json.dumps(report, indent=2, ensure_ascii=False) + "\n").encode("utf8")
    if args.report:
        write_output(args.report, encoded, args.source)
    print(encoded.decode("utf8"), end="")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile, ElementTree.ParseError, ValidationError) as error:
        # Validation exceptions may contain rejected secret values; never echo them.
        message = "Official schema validation failed" if isinstance(error, ValidationError) else str(error)
        print(f"Package validation failed: {message}", file=sys.stderr)
        sys.exit(1)
