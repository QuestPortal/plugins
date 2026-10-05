# Create a 2024 character

## Establish choices

Ask only for missing choices that affect the build: campaign/starting level,
concept, permitted sources, ability-generation method and whether the user wants
guidance or already has a completed character. Do not invent random rolls or
assume a paid option is included in the SRD.

Use the [official creation chapter](https://www.dndbeyond.com/sources/dnd/br-2024/creating-a-character)
and [SRD 5.2.1](https://www.dndbeyond.com/srd) for the selected options:

1. Choose class and starting level, then background and species. Record roleplaying
   details and languages. In the 2024 rules, background supplies ability-score
   increases and an Origin feat; do not apply 2014 species ability increases.
2. Generate and assign ability scores with the table's agreed method. Apply the
   background's permitted increases and verify the final values.
3. Record class proficiencies, starting equipment, features and any level-dependent
   choices. Confirm prerequisites rather than treating editable fields as validation.
4. Establish HP, AC, saves, skills, attacks and resource uses. Review calculations
   against the chosen class and equipment; editable overrides can change results.
5. For a caster, select permitted spells, assign each to its casting class and
   check preparation and slot rules. Keep Pact Magic separate where appropriate.

## Enter the sheet

Call `create_character({ "name": "Mira Ash" })` for a requested new draft.
**Only name is accepted**, up to 100 characters. Guide the user through roll/edit
switching and manual entry. There is no populated payload, batch tool or revision
tool; do not claim a discussed build has been applied to the draft.

Use the sheet's catalogs to select weapons/spells and its explicit controls to
apply slot or maximum-HP suggestions. Those helpers do not complete background,
species, feat or feature selections. For a higher-level or multiclass build,
review levels, per-class casting ability and Hit Dice before accepting suggestions.

Ask for Attach when reviewing entered values. Check the snapshot for unfinished
choices, accidental defaults and duplicated effects. Record unresolved decisions,
recommend JSON backup and distinguish a reviewed plan from a finished saved sheet.
See [workflows](workflows.md) for storage and attachment boundaries.
