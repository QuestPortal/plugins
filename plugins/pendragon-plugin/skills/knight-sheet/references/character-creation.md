# Create a 6th edition knight

## Establish the table's starting point

Ask for campaign year/location, starting status, concept and the permitted
creation procedure. Use the [6e Core Rulebook](https://www.chaosium.com/pendragon-core-rulebook-hardcover/)
for full generation, or the [Starter Set](https://www.chaosium.com/pendragon-starter-set/)
for its pregenerated starting route. The public wiki is a rules introduction,
not a license to reconstruct all creation tables. Request the user's approved
choices when the needed table is not available.

Work through these areas without inventing culture-specific allocations:

1. Identity and campaign position: name, age, homeland/culture, religion, family,
   lord and obligations. Confirm which choices the campaign actually permits.
2. Characteristics: record SIZ, DEX, STR, CON and APP using the selected method.
   Review the sheet's derived HP, damage, healing and movement plus any explicit
   adjustments; default values are illustrative.
3. Personality: enter Traits and Passions consistent with the approved method.
   Keep base opposed Trait pairs complementary and record any critical bonuses
   separately. Do not award religious or chivalric benefits automatically.
4. Skills and combat: enter approved starting skills, weapon/armor details,
   shield/parry information, mount and equipment. Use the actual mount's damage
   when a horse-based attack is requested.
5. Chronicle: establish family, connections, initial Glory, aspirations and notes
   as directed by the table. Future experience and Winter Phase changes require
   adjudication rather than automatic advancement.

## Prepare a populated draft

Use `create_character` (or retained `create_knight`) with the agreed choices:

```json
{"requestId":"rowan-draft-1","name":"Sir Rowan","skills":[{"id":"sword","value":15}],"passions":[{"id":"loyalty-lord","name":"Loyalty","subject":"Lord","court":"fidelity","value":16}]}
```

Name-only creation remains supported (nonblank name up to 200 characters).
Use `create_characters({ requestId, characters: [...] })` for 1–20 distinct
knights; the legacy `create_knights` alias uses `knights` instead. Supply only
approved choices; defaults do not establish rules legality. Inspect each outcome
and report preparation separately from sheet loading/local saving.

Use **Sheet tools** for JSON backup and explicit Attach. Revise an exact current
attachment with `revise_character` (or `revise_knight`), a fresh requestId and
intended changes. Traits, skills, Passions and weapons merge by ID; other arrays
replace with complete entries. Refer to [workflows](workflows.md) for empty-array,
retry and stale-snapshot rules before changing lists.

A discussed concept, a prepared payload, a loaded sheet and a persisted local
draft are different outcomes. Report only the evidenced outcome. Character
creation budgets, campaign choices and consequences remain with the table.
