# Battlemap marketplace package

This offline validator and packager works from the public QuestPortal/plugins
checkout. It does not require the private application repository, call the MCP
endpoint, use credentials, install a plugin, deploy, upload, or submit a public
directory listing. The Git marketplace is the distribution source.

Use Python 3.9 or newer in a virtual environment:

```sh
python3 -m venv /tmp/battlemap-package-venv
/tmp/battlemap-package-venv/bin/python -m pip install -r scripts/battlemap/requirements.txt
/tmp/battlemap-package-venv/bin/python -m unittest discover -s scripts/battlemap -p 'test_*.py'
/tmp/battlemap-package-venv/bin/python scripts/battlemap/package.py validate plugins/quest-portal-battlemap
/tmp/battlemap-package-venv/bin/python scripts/battlemap/package.py build plugins/quest-portal-battlemap --output /tmp/quest-portal-battlemap-0.1.2.zip --report /tmp/quest-portal-battlemap-0.1.2-validation.json
/tmp/battlemap-package-venv/bin/python scripts/battlemap/package.py validate /tmp/quest-portal-battlemap-0.1.2.zip
```

Dependency setup is the only network step. Requirements reuse the exact pinned
versions in `scripts/pendragon/requirements.txt`. Validation reuses Pendragon's
unchanged canonical Agent Plugins 1.0.0
[plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and
[MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) snapshots,
retrieved October 1, 2026. Their pinned SHA-256 values and the validated catalog
hash are included in the report. Keep both script directories when copying the
tool. No remote schemas are fetched.

Every command validates the repository's `.agents/plugins/marketplace.json`
entry against the exact package name and contained local path. `--marketplace`
can point to another local catalog for an explicit release checkout. The tool
then checks the official JSON schemas, exact eight-file inventory, portable and
Codex metadata/endpoint parity, preserved default prompts, contained onboarding,
skill frontmatter, and static SVG artwork with contained fragment references.
Unknown files/directories, symlinks, duplicate JSON keys, escaping archive paths,
duplicate ZIP entries and excessive sizes are rejected. Known credential
patterns are rejected without printing their values. This is a bounded check,
not proof that arbitrary text contains no secret; review the source before
shipping it.

The default ZIP contains one `quest-portal-battlemap/` directory, matching Plugin
Creator's enclosing-directory convention. Hidden `.codex-plugin/plugin.json`
and `.mcp.json` are always included. For the PRD's portable root layout:

```sh
/tmp/battlemap-package-venv/bin/python scripts/battlemap/package.py build plugins/quest-portal-battlemap --layout portable --output /tmp/quest-portal-battlemap-0.1.2-portable.zip
```

Both layouts sort entries, fix timestamps to 1980 and permissions to 0644, and
store bytes without compression. Filesystem order, permissions, timestamps and
compression-library versions cannot change the result. Each build reads its ZIP
back without extraction, compares every entry byte-for-byte with the validated
source, and validates the restored package. Existing ZIP validation accepts
either layout without mixing them. Reports include per-file and archive hashes.

Write artifacts outside the source package. A matching existing artifact can be
reused; a different existing file is never overwritten. Update the reviewed
inventory/tests deliberately when adding package files. CI runs the same focused
tests, validates the marketplace package, builds both layouts into temporary
storage, and validates both archives. Generated archives are not committed.

These checks do not establish authenticated ChatGPT behavior, working callbacks,
mobile acceptance, public-directory policy compliance or listing approval.
