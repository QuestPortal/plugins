# Authoritative sources: Pendragon 6e

- [Official rules wiki](https://pendragonwiki.chaosium.com/rules/): introductory
  6e Starter Set basis. It is not an exhaustive Core Rulebook verification.
- [Game system](https://pendragonwiki.chaosium.com/rules/the-game-system.html):
  modified statistics, critical/fumble classification, above-20 values,
  characteristic exceptions and opposed outcomes.
- [Traits and Passions](https://pendragonwiki.chaosium.com/rules/traits-and-passions.html):
  personality, inspiration conditions and consequences.
- [6e Starter Set](https://www.chaosium.com/pendragon-starter-set/): introduction
  and pregenerated starting play.
- [6e Core Rulebook](https://www.chaosium.com/pendragon-core-rulebook-hardcover/):
  authoritative full creation reference. Refer users to their permitted copy
  for culture, religion, family and allocation tables; do not reproduce them.
- [Chaosium fan-material policy](https://www.chaosium.com/fan-material-policy/)
  and [package notice](../../../NOTICE.md): the policy's software restrictions
  mean free quickstarts are not a general plugin license. Existing commercial
  permissions are not verified by this update; no broader rights are claimed.

The 2022 Sword Tournament quickstart was a preview. Do not use it or 5.x creation
tables as a substitute for final 6e rules. The uncataloged Pendragon2 draft is
not the runtime contract of this package.

## Source and rights boundaries

Checked 2026-10-05. These guides use original concise explanations and links;
they do not bundle proprietary rulebooks, adventures, tables or artwork.
A free web page or downloadable quickstart is not automatically an open license.
Do not claim official endorsement, paid-book access or distribution rights from
availability alone. Preserve the package notice and existing rights scope.

## Implementation evidence

[Runtime source at `d640dd0`](https://github.com/QuestPortal/questportal/tree/d640dd0961c485240431b39e1914afa728afb857/apps/pendragon-plugin) was compared with this package before editing.
`src/server/mcp.ts` and `src/server/guest-mcp.ts` define tool availability;
`src/domain/` defines schemas/calculations, and `src/ui/` defines local storage,
explicit attachment and Sheet tools. The live connection's advertised schema
controls actual calls. This private source link may require repository access;
the public rules links above do not.

`ROLL-CONTRACT.md` and [tool contracts](tool-contracts.md) describe the additive
0.1.2 runtime contract; documentation package versions can advance independently.
