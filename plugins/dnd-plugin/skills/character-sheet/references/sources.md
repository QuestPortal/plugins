# Authoritative sources: D&D 2024 / SRD 5.2.1

- [Official SRD index](https://www.dndbeyond.com/srd): distinguishes SRD 5.2.1
  (2024 revision) from SRD 5.1 (2014). This package implements the former.
- [SRD 5.2.1 PDF](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf):
  use the creation chapter (printed p. 19), equipment (p. 89), spells (p. 107)
  and glossary (p. 176) for exact 2024 rules and exceptions.
- [Official creation guide](https://www.dndbeyond.com/sources/dnd/br-2024/creating-a-character):
  sequence and 2024 origin choices.
- [Official rules glossary](https://www.dndbeyond.com/sources/dnd/br-2024/rules-glossary):
  tests, critical hits, death saves, exhaustion and rests.
- [Conversion guide](https://media.dndbeyond.com/compendium-images/srd/guide/converting-to-srd-5.2.1.pdf):
  consult for explicit 2014-to-2024 conversions, not an automatic edition switch.
- [Package attribution](../../../NOTICE.md) and
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode): retain the
  SRD attribution. The SRD license does not make every D&D web asset or paid book
  openly licensed.

## Source and rights boundaries

Checked 2026-10-05. These guides use original concise explanations and links;
they do not bundle proprietary rulebooks, adventures, tables or artwork.
A free web page or downloadable quickstart is not automatically an open license.
Do not claim official endorsement, paid-book access or distribution rights from
availability alone. Preserve the package notice and existing rights scope.

## Implementation evidence

[Runtime source at `d640dd0`](https://github.com/QuestPortal/questportal/tree/d640dd0961c485240431b39e1914afa728afb857/apps/dnd-plugin) was compared with this package before editing.
`src/server/mcp.ts` and `src/server/guest-mcp.ts` define tool availability;
`src/domain/` defines schemas/calculations, and `src/ui/` defines local storage,
explicit attachment and Sheet tools. The live connection's advertised schema
controls actual calls. This private source link may require repository access;
the public rules links above do not.

`src/domain/srd/spells.ts` contains 339 catalog rows and `weapons.ts` contains
38 weapon entries. `rules.ts` verifies class-specific casting, class-owned Hit
Dice, rest actions and manual resource boundaries. Catalogs are not full spell
effect automation.
