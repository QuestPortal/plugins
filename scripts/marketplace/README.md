# Marketplace validation and packaging

This offline tool validates every catalog entry against `packages.json`, the
reviewed inventory of original package identities, versions, prompts, endpoints
and files. It reuses the repository’s pinned Agent Plugins schemas and existing
Battlemap validation helpers. It does not download schemas or call endpoints.

```sh
python3 -m venv /tmp/qp-package-venv
/tmp/qp-package-venv/bin/pip install -r scripts/marketplace/requirements.txt
/tmp/qp-package-venv/bin/python -m unittest discover -s scripts/marketplace -p 'test_*.py'
/tmp/qp-package-venv/bin/python scripts/marketplace/package.py generate-codex --check
/tmp/qp-package-venv/bin/python scripts/marketplace/package.py validate
/tmp/qp-package-venv/bin/python scripts/marketplace/package.py build --output-dir /tmp/qp-packages
```

Builds contain exactly one named package directory, including hidden compatibility
files. Entries have fixed timestamps, stable ordering and regular file modes.
Each written ZIP is re-read, compared byte for byte with source files, and validated.
Existing different artifacts are never overwritten; select a fresh output directory
when changing a release candidate. JSON stdout reports per-file hashes and archive
hashes. Archives belong outside `plugins/`; do not commit generated ZIPs.

Checks cover catalog identity/uniqueness for both the Codex catalog
(`.agents/plugins/marketplace.json`) and the Claude catalog
(`.claude-plugin/marketplace.json`), exact local paths, no unverified plugin-ID
bindings, portable/Codex identity/version/interface parity, portable/Claude
(`.claude-plugin/plugin.json`) identity/version/homepage/keyword parity, intentional transport
spellings (`streamable-http` versus `http`), exact endpoint/server names, contained
skill and icon references, static SVG artwork, attribution inventory, Cthulhu review
materials, file/expanded archive bounds, symlinks, and common credential patterns.
Credential patterns cannot prove the absence of every secret. Endpoint validation
checks configuration, not availability, discovery or authentication.

Update the inventory only alongside reviewed package changes. Do not generate it
from arbitrary downloaded packages to make failing validation pass. Versions are
package versions; runtime versions can differ. Existing focused Pendragon and
Battlemap tools remain supported. CI runs their tests alongside the shared suite.

The Claude manifests can also be checked with `claude plugin validate --strict .`
from the repository root; that tool is not part of the offline suite.

`docs/release-status.md` records deployment and native-host gates. A successful
archive build is not release approval or a claim that unrun host cases passed.

## Native Codex sheet bundles

`plugins/` remains canonical for portable archives and Claude. The Codex catalog
selects `codex-plugins/dnd-plugin` and `codex-plugins/call-of-cthulhu-plugin`.
These generated bundles contain exact copies of the native manifest, `.mcp.json`,
skills, artwork, attribution and README where present. They omit the portable
root `plugin.json` and `mcp.json` and the Claude manifest. The absence of the root
portable manifest preserves native Codex package classification.

After a canonical source change, run:

```sh
python scripts/marketplace/package.py generate-codex
python scripts/marketplace/package.py generate-codex --check
```

Generation is deterministic, validates canonical packages before copying, and
rejects unexpected destination files instead of deleting them. `--check`, normal
validation and archive builds all reject missing, extra or stale generated files.
CI checks committed bundles without regenerating them, so drift cannot pass by
silently refreshing CI's checkout. Other packages and portable archive contents
are unaffected by the native bundle selection.

Builds also produce `dnd-plugin-<version>-codex.zip` and
`call-of-cthulhu-plugin-<version>-codex.zip` for manual Codex/ChatGPT uploads.
Use these native ZIPs for Codex/ChatGPT; the un-suffixed ZIPs retain the portable
format for other hosts. Native ZIPs use the same deterministic archive layout and
safe reader, and their restored bytes must equal the reviewed native subset.
