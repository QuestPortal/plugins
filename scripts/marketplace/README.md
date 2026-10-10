# Marketplace validation and packaging

This offline tool validates every catalog entry against `packages.json`, the
reviewed inventory of original package identities, versions, prompts, endpoints
and files. It reuses the repository’s pinned Agent Plugins schemas and existing
Battlemap validation helpers. It does not download schemas or call endpoints.

```sh
python3 -m venv /tmp/qp-package-venv
/tmp/qp-package-venv/bin/pip install -r scripts/marketplace/requirements.txt
/tmp/qp-package-venv/bin/python -m unittest discover -s scripts/marketplace -p 'test_*.py'
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
