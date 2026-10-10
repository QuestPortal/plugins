#!/usr/bin/env python3
"""Validate/build the Pendragon package offline; never install or publish it."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import stat
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from jsonschema import Draft202012Validator, ValidationError

NAME = "pendragon-plugin"
ENDPOINT = "https://pendragon.questportal.com/mcp"
DEFAULT_PROMPTS = [
    "Open my Pendragon knight sheets.",
    "Help me create a Pendragon 6th edition knight.",
]
FILES = (
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
    ".mcp.json",
    "NOTICE.md",
    "assets/icon.svg",
    "mcp.json",
    "plugin.json",
    "skills/knight-sheet/SKILL.md",
    "skills/knight-sheet/references/tool-contracts.md",
    "skills/knight-sheet/references/system-overview.md",
    "skills/knight-sheet/references/character-creation.md",
    "skills/knight-sheet/references/core-rules.md",
    "skills/knight-sheet/references/workflows.md",
    "skills/knight-sheet/references/examples.md",
    "skills/knight-sheet/references/sources.md",
)
SCHEMA_HASHES = {
    "plugin": "0a4aad95ce337878ad38802ebf0daa3fde76abe3f65400c86bcbb1ec0b3ab883",
    "mcp": "6539175bfcdf43085855183e86da40ea94b166547a72b47ae9a0a390516d3acb",
}
MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_PACKAGE_BYTES = 20 * 1024 * 1024
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def decode_json(data):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(data, object_pairs_hook=unique_object)


def fixed_schema(name):
    data = (Path(__file__).parent / "schemas" / f"{name}.schema.json").read_bytes()
    require(sha256(data) == SCHEMA_HASHES[name], f"Pinned {name} schema changed")
    schema = decode_json(data)
    Draft202012Validator.check_schema(schema)
    return schema


def validate_files(files):
    require(set(files) == set(FILES), "Package must contain exactly the reviewed Pendragon file list")
    require(all(0 < len(data) <= MAX_FILE_BYTES for data in files.values()), "Invalid package file size")
    require(sum(map(len, files.values())) <= MAX_PACKAGE_BYTES, "Package exceeds size bound")
    manifest = decode_json(files["plugin.json"])
    mcp = decode_json(files["mcp.json"])
    for name, value in (("plugin", manifest), ("mcp", mcp)):
        Draft202012Validator(fixed_schema(name)).validate(value)
    require(manifest["name"] == NAME, "Plugin identity changed")
    require(SEMVER.fullmatch(manifest.get("version", "")), "Use a stable semantic release version")
    require(manifest.get("author") == {"name": "Quest Portal"}, "Publisher identity changed")
    require(set(manifest.get("extensions", {})) == {"com.openai"}, "Unexpected manifest extension")
    extension = manifest["extensions"]["com.openai"]
    require(set(extension) == {"interface"}, "Unexpected app binding or extension field")
    interface = extension["interface"]
    expected_interface_keys = {
        "displayName", "shortDescription", "longDescription", "developerName",
        "category", "capabilities", "logo", "composerIcon", "defaultPrompt",
    }
    require(set(interface) == expected_interface_keys, "Unexpected or missing interface metadata")
    require(interface["displayName"] == "Pendragon", "Display identity changed")
    require(interface["developerName"] == "Quest Portal", "Developer identity changed")
    require(interface["category"] == "Entertainment", "Existing audience category changed")
    require(interface["capabilities"] == ["Interactive", "Read", "Write"], "Existing capabilities changed")
    require(interface["defaultPrompt"] == DEFAULT_PROMPTS, "Default prompts changed in value, type, or order")
    require(0 < len(interface["shortDescription"]) <= 30, "Subtitle must be 1–30 characters")
    require(isinstance(interface["longDescription"], str) and interface["longDescription"].strip(), "Missing long description")
    require(interface["logo"] == interface["composerIcon"] == "./assets/icon.svg", "Icon reference changed or leaves package")

    compatibility = decode_json(files[".codex-plugin/plugin.json"])
    require(compatibility == {
        "name": manifest["name"], "version": manifest["version"],
        "description": manifest["description"], "author": manifest["author"],
        "skills": "./skills/", "interface": interface, "mcpServers": "./.mcp.json",
    }, "Portable and compatibility manifest identity/version/presentation differ")
    require(decode_json(files[".claude-plugin/plugin.json"]) == {
        "name": manifest["name"], "version": manifest["version"],
        "description": manifest["description"], "author": manifest["author"],
        "homepage": "https://pendragon.questportal.com",
        "keywords": ["pendragon", "tabletop", "rpg", "character-sheet", "dice", "mcp"],
    }, "Portable and Claude manifest identity/version/presentation differ")
    require(mcp["mcpServers"] == {"pendragon-sheets": {"type": "streamable-http", "url": ENDPOINT}}, "Portable MCP endpoint or transport changed")
    require(decode_json(files[".mcp.json"]) == {"mcpServers": {"pendragon-sheets": {"type": "http", "url": ENDPOINT}}}, "Compatibility MCP endpoint or transport differs")

    skill = files["skills/knight-sheet/SKILL.md"].decode("utf8")
    require(skill.startswith("---\n"), "Missing skill YAML frontmatter")
    header, separator, body = skill[4:].partition("\n---\n")
    require(separator and body.strip(), "Missing skill body")
    require(re.search(r"^name: knight-sheet$", header, re.MULTILINE), "Skill name must match directory")
    require(re.search(r"^description: \S.+$", header, re.MULTILINE), "Missing skill trigger description")
    require("references/tool-contracts.md" in body, "Tool-contract reference is not linked")

    icon = files["assets/icon.svg"]
    try:
        icon_text = icon.decode("utf8")
    except UnicodeError as error:
        raise ValueError("SVG must be UTF-8 text") from error
    require("\x00" not in icon_text, "SVG must be UTF-8 text without null characters")
    require("<!DOCTYPE" not in icon_text.upper() and "<!ENTITY" not in icon_text.upper(), "Unsafe SVG declaration")
    svg = ElementTree.fromstring(icon_text)
    require(svg.tag == "{http://www.w3.org/2000/svg}svg", "Expected SVG icon")
    width, height = int(svg.attrib["width"]), int(svg.attrib["height"])
    require(width == height and 48 <= width <= 4096, "Icon must be square and at least 48 pixels")
    for element in svg.iter():
        tag = element.tag.split("}")[-1]
        require(tag in {"svg", "g", "path", "circle", "rect", "line", "polygon", "polyline", "ellipse", "title", "desc"}, "SVG must contain static local artwork only")
        require(set(element.attrib) <= {"width", "height", "viewBox", "fill", "stroke", "stroke-width", "stroke-linejoin", "stroke-linecap", "d", "cx", "cy", "r", "rx", "ry", "x", "y", "x1", "y1", "x2", "y2", "points", "opacity", "fill-opacity", "stroke-opacity"}, "SVG contains an unreviewed attribute (including style or external references)")
        for key, value in element.attrib.items():
            require("\\" not in value and "url(" not in value.lower(), "SVG must not contain CSS escapes or external references")
            if key in {"fill", "stroke"}:
                require(re.fullmatch(r"(?:none|currentColor|#[0-9a-fA-F]{3,8})", value), "SVG paints must be static colors")
    return {
        "status": "valid", "name": NAME, "version": manifest["version"],
        "schemas": {name: {"id": f"https://agent-plugins.org/schemas/1.0.0/{name}.schema.json", "sha256": digest} for name, digest in SCHEMA_HASHES.items()},
        "compatibilityParity": True, "defaultPromptsPreserved": True,
        "endpoint": ENDPOINT, "subtitleCharacters": len(interface["shortDescription"]),
        "icon": {"width": width, "height": height, "sha256": sha256(icon)},
        "files": [{"path": name, "bytes": len(files[name]), "sha256": sha256(files[name])} for name in sorted(files)],
        "boundaries": "Offline package validation only; no endpoint, installation, host, policy, or store approval is claimed.",
    }


def read_directory(root):
    require(root.name == NAME, "Directory name must match pendragon-plugin")
    require(not root.is_symlink(), "Package root may not be a symlink")
    files = {}
    for path in root.rglob("*"):
        require(not path.is_symlink(), "Package may not contain symlinks")
        if path.is_dir():
            continue
        require(path.is_file(), "Package contains a non-regular file")
        require(path.stat().st_size <= MAX_FILE_BYTES, "Package file exceeds size bound")
        files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def read_archive(archive):
    require(archive.stat().st_size <= MAX_PACKAGE_BYTES, "Archive exceeds size bound")
    files = {}
    with zipfile.ZipFile(archive) as bundle:
        for entry in bundle.infolist():
            require(entry.filename.startswith(f"{NAME}/"), "Archive must have one Pendragon directory")
            relative = entry.filename[len(NAME) + 1:]
            require(relative in FILES, "Archive contains an unexpected or escaping path")
            require(relative not in files, "Archive contains duplicate paths")
            require(not stat.S_ISLNK(entry.external_attr >> 16), "Archive may not contain symlinks")
            require(not entry.is_dir() and entry.file_size <= MAX_FILE_BYTES, "Invalid archive entry")
            files[relative] = bundle.read(entry)
    return files


def build_zip(files):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as bundle:
        for name in sorted(files):
            entry = zipfile.ZipInfo(f"{NAME}/{name}", date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            entry.compress_type = zipfile.ZIP_STORED
            bundle.writestr(entry, files[name])
    return output.getvalue()


def write_output(path, data, source):
    require(not path.resolve().is_relative_to(source.resolve()), "Write artifacts outside the source package")
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        require(path.is_file() and path.read_bytes() == data, "Refusing to overwrite a different existing artifact; choose a new output path")
    else:
        with path.open("xb") as output:
            output.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "build"))
    parser.add_argument("source", type=Path, help="Pendragon directory or existing ZIP")
    parser.add_argument("--output", type=Path, help="ZIP output outside source (build only)")
    parser.add_argument("--report", type=Path, help="JSON validation report outside source")
    args = parser.parse_args()
    require(args.source.exists(), "Package source does not exist")
    files = read_directory(args.source) if args.source.is_dir() else read_archive(args.source)
    report = validate_files(files)
    if args.command == "build":
        require(args.source.is_dir() and args.output, "Build requires a source directory and --output")
        archive = build_zip(files)
        write_output(args.output, archive, args.source)
        require(read_archive(args.output) == files, "Archive does not reproduce validated source")
        validate_files(read_archive(args.output))
        report["archive"] = {"file": args.output.name, "bytes": len(archive), "sha256": sha256(archive)}
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
        print(f"Package validation failed: {error}", file=sys.stderr)
        sys.exit(1)
