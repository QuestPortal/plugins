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

## Prepare the sheet

Use `create_character` with a fresh `requestId` and the agreed sheet fields.
For example, a custom starting draft can include
`{ "requestId": "mira-draft-1", "name": "Mira Ash", "abilities": { "intelligence": 16 }, "notes": "Review background and spell choices." }`.
A name-only call remains supported (name up to 100 characters). Defaults do not
complete class, background, species, feat, equipment or spell choices. Supply
complete array entries using the advertised schema when adding classes/spells;
arrays replace, while supported nested objects merge.

Use `create_characters({ requestId, characters: [...] })` for 1–20 distinct builds.
Review per-member errors and retry only as described in [workflows](workflows.md).
After tool preparation, the sheet must confirm loading and local persistence.
Do not substitute JSON in chat for an available creation tool.

The sheet's catalogs and explicit slot/maximum-HP suggestions remain available.
Those helpers do not complete background, species, feat or feature selections.
For a higher-level or multiclass build, review levels, per-class casting ability
and Hit Dice before accepting suggestions.

Ask for Attach when reviewing entered values. Use `revise_character` with that
exact snapshot, a new requestId and intended changes. Preserve complete arrays
when changing one member. Check unfinished choices, accidental defaults and
duplicated effects; recommend JSON backup. A prepared revision is not proof of
application or saving. See [workflows](workflows.md) for conflict and retry rules.
