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

## Create and enter a draft

Call `create_knight({ "name": "Sir Rowan" })` for the requested new draft.
Its strict schema accepts only an optional name, at most 200 characters.
There is **no populated creation, batch or revision tool**. Help the user enter
choices manually in the sheet; do not pass characteristics, Passions or equipment
to `create_knight` or claim those choices were applied by chat.

Use **Sheet tools** for JSON import/export and explicit Attach. When asked to
review a completed knight, use a current attachment or exported JSON, identify
remaining placeholders and check consistency with the selected procedure.
Never infer rules legality from schema acceptance or neutral starting values.

A discussed knight concept, an opened draft, a manually completed sheet and a
persisted local draft are different outcomes. Report only the outcome evidenced
by tools/the sheet; recommend JSON backup. See [workflows](workflows.md).
