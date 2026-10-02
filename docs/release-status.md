# Selected original packages — release gates

This branch reconciles the original Call of Cthulhu, Pendragon and D&D identities
with the existing Battlemap pilot. It adds no umbrella Quest Portal app and no
binding to the separate authenticated `apps/mcp-public` runtime. Marketplace
source availability, runtime deployment, native-host acceptance and public-directory
submission are separate states.

| Package | Package candidate | Runtime baseline / alignment | Remaining gates |
| --- | --- | --- | --- |
| Call of Cthulhu | 0.4.1 | 0.4.0 populated creation/revision; package-only metadata restoration | Current installed-host cases, including batch/revision/storage; directory review and attestations remain unrun |
| Original Pendragon | 0.1.2 | Original runtime PR 10470, candidate 0.1.2; opposed/statistic/damage contract inspected locally | Final runtime commit/test evidence, matching deployment, installed-host acceptance |
| Original D&D | 0.1.0 (unreleased) | Original runtime PR 10474; identity/endpoints/schema retained, SRD pickers and explicit suggestions added | Final runtime commit/test evidence, matching deployment, installed-host acceptance |
| Battlemap | 0.1.3 | Runtime 0.1.4 reported separately; package endpoint remains map.questportal.com | Owner-only OAuth/linking, native UI/downloads, callback Events and physical mobile acceptance |

D&D synchronization retains 339 SRD spells, 38 weapons, class-owned spells and
Hit Dice, explicit slot/max-HP suggestions, death-save DC 10 and no initiative
success verdict. Generic roll tools do not mutate character state. SRD 5.2.1
attribution is included. D&D’s SVG now has explicit 128px dimensions; artwork
and package identity are preserved. Its initial 0.1.0 version stays unreleased.

Pendragon package 0.1.2 follows the inspected original runtime schemas: optional
`statistic` and `opponent` on `roll_check`, opponent result and resolution,
`horse`/`horseDamageDice` and `critical: weapon|brawling` on `roll_damage`.
There are no new tool names or endpoints. The runtime also corrects symbolic
subtraction and combined pool bounds, equal-failure ties and the inclusive
unconsciousness boundary. These are candidate source contracts, not a claim
that the live endpoint or native hosts have been verified. Existing guest storage
and explicit Attach boundaries remain intact.

The alternative `gunni/pendragon2-plugin` draft PR 9 and `gunni/dnd2-plugin`
branch (c9a9ae44b8da99c8d60229c077d8fb08707b956e) are preserved for reference.
They are not added to this catalog. Existing user checkout and untracked files
remain untouched. The D&D package integration incorporates draft PR 5 while
preserving main’s Call of Cthulhu, Pendragon and Battlemap entries.

## Validation and acceptance boundary

The shared offline validator checks all catalog packages and deterministically
builds complete archives with per-file hashes and portable/Codex parity. It checks
endpoint configuration only. Regression suites cover malformed manifests,
wrong identities/transports/paths, missing metadata, unsafe SVGs, duplicate ZIP
entries, archive bounds, symlinks, credentials and output preservation. The
retained Cthulhu deployment handler has local route, page-copy and video-range
checks. See `scripts/marketplace/README.md` for reproducible commands.

Installed-host rendering, explicit Attach, local storage/reload behavior, physical
mobile and actual Events callbacks remain **not accepted** for these release
candidates. Shared component/build tests and browser/mock harnesses are useful
runtime evidence but do not satisfy those gates. No production endpoint calls, state writes, authentication changes, runtime
deploys, public submissions or legal attestations were performed by this package
reconciliation. Package merge is authorized only after matching runtime and
required review/CI gates; runtime deployment is owned by the runtime tasks.

Before publishing new package instructions on main, record the matching runtime
commit and version, complete applicable required CI/review, confirm deployment
of the matching contract, and obtain merge/deployment authorization. Record host
checks with the exact host/version, actions, results and limitations. Keep
Battlemap owner-only; catalog import does not grant access to its private library.

Cthulhu’s old 0.3 archive and current 0.4.1 package are reconciled in
[the review-material record](cthulhu/reconciliation.md); old walkthrough and
review cases are preserved without claiming current host acceptance.
