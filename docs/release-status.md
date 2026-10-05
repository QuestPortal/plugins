# Selected original packages — release evidence

Updated 2026-10-05. This release reconciles the original Call of Cthulhu,
Pendragon and D&D identities with the existing Battlemap pilot. It adds no umbrella
Quest Portal app and no binding to the separate authenticated `apps/mcp-public`
runtime. Marketplace source availability, runtime deployment, native-host
acceptance and public-directory submission are separate states.

| Package | Package version | Runtime and endpoint | Remaining acceptance |
| --- | --- | --- | --- |
| Call of Cthulhu | 0.4.2 | 0.4.0 verified live; `https://cthulhu.questportal.com/mcp`; package-only guides and review examples | Installed-host review cases, including batch/revision/storage; directory review and attestations remain unrun |
| Original Pendragon | 0.1.3 | 0.1.2 merged and verified live; `https://pendragon.questportal.com/mcp` | Installed-host rendering, Attach/storage, physical mobile, production Events |
| Original D&D | 0.1.1 | 0.1.0 merged and verified live; `https://dnd.questportal.com/mcp` | Installed-host rendering, Attach/storage, physical mobile, production Events |
| Battlemap | 0.1.3 | Runtime 0.1.4 reported separately; `https://map.questportal.com/mcp`; unchanged owner-only pilot | Owner-only OAuth/linking, native UI/downloads, callback Events and physical mobile |

## Current runtime and UI evidence — 2026-10-05

The source audit fetched plugins main `92971108a84fa3596df6da303143651344c56857`
and verified runtime main `d640dd0961c485240431b39e1914afa728afb857`.
[Runtime PR 10484](https://github.com/QuestPortal/questportal/pull/10484) is the
shared Sheet tools UI update. The following deployment evidence was **supplied by
release task `01a108af-3056-749e-be1e-dc21f1dc20ca`**, not rerun by this package task:

| App | Worker version serving merged `d640dd0` | Traffic |
| --- | --- | --- |
| Pendragon | `6f87e612-7c4f-48d4-a040-57611db7a9ef` | 100% |
| D&D | `d9ff70ce-ab45-4b99-9761-64e2898cd046` | 100% |
| Call of Cthulhu | `0b513fcd-3b5f-4c15-b62a-02b783099621` | 100% |

The release task reports HTTP 200 health and public HTML hashes matching builds.
Live standalone Chromium checks passed for toggle, keyboard, Escape, focus,
outside click, 320px layout, 44px targets and reduced motion. D&D/CoC themes passed;
Pendragon remains dark-only. All three now use the footer **Sheet tools** entry;
D&D/CoC support responsive layouts, roll/edit switching and light/dark preferences.
Evidence report: Library `libfile_37dd65cc22d08191b6f7ee07a5ffc49e` (supplied
identifier, not a new artifact produced by this task).

**Still unrun:** native ChatGPT/Codex embedding and installed-host acceptance,
Attach delivery, storage/reload across host partitions, physical mobile and live
session/Event callbacks. These checks must not be inferred from standalone browser
success. No runtime deployment or production sessions were created for this PR.

## Documentation package changes

Patch package versions are D&D 0.1.1, CoC 0.4.2 and Pendragon 0.1.3. Portable and
Codex manifests advance together; MCP identities, URLs, starter prompts, artwork,
catalog entries, audience and the Battlemap pilot are preserved. This is a source
PR candidate until merged; package version bumps do not indicate publication.

Each existing skill now routes to edition overview, creation, core rules,
workflows, examples and official sources. D&D/Pendragon creation schemas are
strict name-only; completion and later editing happen manually in the sheet.
CoC supports populated creation, 1–20-member batches and exact attached-snapshot
revisions. Tool success is payload preparation, not proof of loading/local saving.
The CoC manifest retains its original cases and adds populated single, distinct
batch/retry, partial-failure and revision/stale-snapshot cases; all installed-host
review cases remain unrun. The older walkthrough is not evidence for them.

Rules are original summaries with official links. D&D attribution is preserved.
Chaosium's free introductory material is not treated as an open license; this
update redistributes no proprietary rulebook text/tables/art and makes no new
rights claim. Existing commercial-license scope is not verified here. Full 6e
Core Rulebook coverage and rules-legal CoC generation are not asserted.

## Historical runtime deployment records — through 2026-10-03

These records were supplied by the runtime/release tasks. The package validator
makes no live endpoint calls. Standalone browser screenshots and matching served
HTML establish the observed deployed build, not native ChatGPT/Codex acceptance.

- **Cthulhu 0.4.0:** source `b376ed45a9a649daa9ffb55b77518fa782c100b1`,
  Worker version `9b049fb0-4516-48f8-bfbc-112dbfdfc943`, deployment
  `10d9b0e8-8888-4516-9f60-f9921756d3f8` at 100% traffic. The release task
  confirmed guest/ok/0.4.0 health. Package 0.4.1 only restores metadata and
  review material; it did not require a runtime redeploy.
- **D&D 0.1.0:** [runtime PR 10474](https://github.com/QuestPortal/questportal/pull/10474)
  merged as `a995965abe76565749c68e02f82ea1ac45612f3f` after
  [CI 37079521856](https://github.com/QuestPortal/questportal/actions/runs/37079521856)
  passed. Worker version `4f633716-6a2b-4b77-af11-4d46eabf1df1`, deployment
  `63e1d876-7f4c-4557-a7c4-dd1322bd0bb2`, created
  `2026-10-03T00:00:20.953247Z`, confirmed at 100% traffic. Served HTML SHA-256
  `7fb68f80203711d3c7caa8194b581b7199e77c32fb7946654aef58211d73cc61`
  matches the merged build. The runtime task reported 212 unit and 26 browser
  tests, typecheck/lint/build passes and three actual live browser screenshots
  without errors or writes outside the synthetic browser-local draft.
- **Pendragon 0.1.2:** [runtime PR 10470](https://github.com/QuestPortal/questportal/pull/10470)
  merged as `62c0a156b7c30104762b000c7e6c67980e029d63`. Worker version
  `27349f9b-0415-448f-9f6e-e168f4e6949e`, deployment
  `a0c1d202-142e-4976-8284-18e86a3605be`, created
  `2026-10-02T23:59:05.091743Z`, confirmed at 100% traffic. Served HTML SHA-256
  `97aa503e4c15223c50e690f9e255e56ebffa1e10737e9221acf98ba7dda8c6ed`
  matches the merged/tested build; health reports guest/ok/0.1.2. The
  [release record](https://github.com/QuestPortal/questportal/pull/10470#issuecomment-5963380055)
  reports 242 unit, 30 Chromium and 3 safety tests plus type/lint/format/build/CI
  passes, live desktop/narrow screenshots, and no production session/event writes.

The shared Cthulhu hard-coded-expiry test-fixture failure was repaired in
[PR 10477](https://github.com/QuestPortal/questportal/pull/10477), merged as
`8ae12b0215be49b49dff4963cffbed8d4478d467`, before the runtime gates completed.
It was not bypassed to release the packages.

## Contract alignment and preservation

D&D retains 339 SRD spells, 38 weapons, class-owned spells and Hit Dice, explicit
slot/max-HP suggestions, death-save DC 10 and no initiative success verdict.
Generic roll tools do not mutate character state. SRD 5.2.1 attribution is
included. The SVG now has explicit 128px dimensions; artwork and identity are
preserved. The deployed runtime pins that icon to package source
`a9fd4f4b94a197d86d6d3e763a5a415458f90a2c`.

Pendragon 0.1.2 follows the
[merged original contract](https://github.com/QuestPortal/questportal/blob/62c0a156b7c30104762b000c7e6c67980e029d63/apps/pendragon-plugin/ROLL-CONTRACT.md):
optional `statistic` and `opponent` on `roll_check`, opponent result and resolution,
`horse`/`horseDamageDice` and `critical: weapon|brawling` on `roll_damage`.
There are no new tool names or endpoints. The runtime corrects symbolic
subtraction and combined pool bounds, equal-failure ties and the inclusive
unconsciousness boundary. Existing guest storage and explicit Attach boundaries
remain intact. Full Core Rulebook verification remains outside the evidence.

The alternative `gunni/pendragon2-plugin` draft PR 9 and `gunni/dnd2-plugin`
branch (c9a9ae44b8da99c8d60229c077d8fb08707b956e) are preserved for reference.
They are not added to this catalog. The existing user checkout and untracked files
remain untouched. [Package PR 5](https://github.com/QuestPortal/plugins/pull/5)
preserves main’s Call of Cthulhu, Pendragon and Battlemap entries while adding
only the selected original D&D package.

## Documentation candidate validation — 2026-10-05

On GunniBook, the package-only change passed 28 Python regression tests
(marketplace 11, Pendragon 6, Battlemap 11) and 9 retained Cthulhu handler tests.
The offline validator accepted all four catalog packages, including unchanged
Battlemap, and checked portable/Codex parity, inventory, identities/endpoints,
frontmatter and contained Markdown links. All three system skills also passed
the skill-authoring frontmatter validator. Two builds produced identical ZIP
hashes for every package; archive validation compares packaged bytes to source.
The reviewed inventories include all 18 new linked references and the retained
Pendragon tool contract. No dependency or generated archive is committed.

An independent reviewer compared the guides and examples to runtime `d640dd0`
and checked the listings/release evidence. No blocking correctness findings
remained. Direct Pendragon contract navigation and a CoC 20+3 batch example were
added; separate Pendragon JSON examples were split into individually valid blocks.
These are offline documentation/package checks. No credentials, live game sessions,
production state changes or new native host acceptance were involved. Draft PR CI
must also pass on the final submitted head before review/merge.

## Historical package validation and remaining gates

The shared offline validator checks every catalog package and deterministically
builds complete archives with per-file hashes and portable/Codex parity. It checks
endpoint configuration only. The 28 Python regression tests cover malformed
manifests, wrong identities/transports/paths, missing metadata, unsafe SVGs,
duplicate ZIP entries, archive bounds, symlinks, credentials and output
preservation. Nine local Cthulhu handler tests check exact routes, page copies
and video bytes/ranges. See `scripts/marketplace/README.md` for commands.
Independent review of package implementation head `523931d` found no substantive
defects; both package CI workflows passed. The subsequent release-documentation
update records the now-completed runtime gates without changing those contracts.

Installed-host rendering, explicit Attach, local storage/reload behavior, physical
mobile and actual Events callbacks remain **not accepted**. Shared component/build
tests, browser/mock harnesses and standalone live screenshots do not satisfy those
gates. Package reconciliation did not perform production endpoint calls, state
writes, authentication changes, runtime deploys, public submissions or legal
attestations. Runtime deployment and live verification were performed separately
under the user’s expanded release authorization.

Keep Battlemap owner-only; catalog import does not grant access to its private
library. Public OpenAI directory submission and legal attestations are not part of
this release. Cthulhu’s old 0.3 archive and 0.4.1 metadata restoration and current 0.4.2 package are reconciled in
[the review-material record](cthulhu/reconciliation.md); its review cases remain
unrun in the installed host and the older walkthrough is not evidence for 0.4
batch/revision behavior.
