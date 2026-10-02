# Pendragon release package

This small offline tool validates the reviewed Pendragon package and creates a
portable ZIP. It does not deploy, connect to an MCP endpoint, install a plugin,
upload an account plugin, or submit a store listing. The Git marketplace remains
the distribution source. Other Quest Portal plugin packages are not modified.

Use Python 3.9 or newer in a virtual environment:

```sh
python3 -m venv /tmp/pendragon-package-venv
/tmp/pendragon-package-venv/bin/python -m pip install -r scripts/pendragon/requirements.txt
/tmp/pendragon-package-venv/bin/python -m unittest discover -s scripts/pendragon -p 'test_*.py'
/tmp/pendragon-package-venv/bin/python scripts/pendragon/package.py validate plugins/pendragon-plugin
/tmp/pendragon-package-venv/bin/python scripts/pendragon/package.py build plugins/pendragon-plugin --output /tmp/pendragon-plugin-0.1.2.zip --report /tmp/pendragon-plugin-0.1.2-validation.json
/tmp/pendragon-package-venv/bin/python scripts/pendragon/package.py validate /tmp/pendragon-plugin-0.1.2.zip
```

Dependency installation is the only network step. Validation and ZIP building
read local files only. The unchanged Agent Plugins 1.0.0 schemas in `schemas/`
come from the canonical [plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json)
and [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json), retrieved
2026-10-01. Their SHA-256 values are pinned in the tool and included in its report.
The JSON Schema 2020-12 validator performs the official structural validation;
the tool separately checks Plugin Creator's package conventions, compatibility
parity, preserved prompts and identity, endpoint, skill frontmatter, and artwork.

The ZIP contains one `pendragon-plugin/` directory, including hidden Codex
compatibility files. Only the eight explicitly reviewed package files are
accepted. Unrelated files, symlinks, traversal paths, duplicate JSON keys, external
SVG references, version drift, and oversized files are rejected. Archives are
inspected in memory without extracting them. ZIP entries are sorted, have fixed
1980 timestamps and 0644 permissions, and use stored bytes so differing filesystem
timestamps, permissions, or compression-library versions cannot change the ZIP.

Write artifacts outside the source package. A matching existing artifact is
accepted; a different existing file is never overwritten. Choose a new output
path after changing source. Update the reviewed file list and tests deliberately
when adding package files. Refer to the private app's current tool contracts when
editing the skill; validation cannot prove native host behavior or rules coverage.

This package is suitable for source/ZIP delivery and the existing Git marketplace.
No public directory approval, listing URLs, supported countries, policy
attestations, or native-host verification are supplied or inferred by this tool.
