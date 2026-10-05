# Authoritative sources: Call of Cthulhu 7e

- [Official rules overview](https://cthulhuwiki.chaosium.com/rules/): introductory
  7e rules and the Keeper/investigator roles.
- [Creating investigators](https://cthulhuwiki.chaosium.com/investigators/): explicitly
  simplified generation; the full Keeper Rulebook/Investigator Handbook offers
  a more detailed method.
- [Characteristics](https://cthulhuwiki.chaosium.com/investigators/step-one-investigator-characteristics.html):
  introductory allocation and half/fifth values; do not substitute the plugin's
  neutral defaults for this procedure.
- [Skill rolls and difficulty](https://cthulhuwiki.chaosium.com/rules/skill-rolls-and-difficulty-levels.html):
  regular/hard/extreme and the consequences of pushing.
- [Combat](https://cthulhuwiki.chaosium.com/rules/combat.html): DEX order,
  fight-back versus Dodge and the prohibition on pushing combat rolls.
- [Official quickstart](https://www.chaosium.com/cthulhu-quickstart/): introductory
  reference, not a redistributable rulebook included in this plugin.
- [Copyright notice](https://cthulhuwiki.chaosium.com/about/trademarks-and-copyrights.html),
  [Chaosium fan-material policy](https://www.chaosium.com/fan-material-policy/) and
  [package notice](../../../NOTICE.md): no broad license grant is inferred.
  Existing commercial permissions, if needed, must be verified separately;
  this documentation update makes no new rights assertion.

## Source and rights boundaries

Checked 2026-10-05. These guides use original concise explanations and links;
they do not bundle proprietary rulebooks, adventures, tables or artwork.
A free web page or downloadable quickstart is not automatically an open license.
Do not claim official endorsement, paid-book access or distribution rights from
availability alone. Preserve the package notice and existing rights scope.

## Implementation evidence

[Runtime source at `d640dd0`](https://github.com/QuestPortal/questportal/tree/d640dd0961c485240431b39e1914afa728afb857/apps/call-of-cthulhu-plugin) was compared with this package before editing.
`src/server/mcp.ts` and `src/server/guest-mcp.ts` define tool availability;
`src/domain/` defines schemas/calculations, and `src/ui/` defines local storage,
explicit attachment and Sheet tools. The live connection's advertised schema
controls actual calls. This private source link may require repository access;
the public rules links above do not.

`src/domain/guest-characters.ts` defines populated inputs, the 1–20 batch bound
and attached-snapshot revisions. Sheet receipts and local storage are separate
from server payload preparation; see [workflows](workflows.md).
