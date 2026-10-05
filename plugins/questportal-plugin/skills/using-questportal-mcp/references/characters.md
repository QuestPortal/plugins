# Character creation

`questportal_create_character` treats placement and sheet foundation as
independent inputs.

## Placement

- `kind=player` creates a standalone character owned by the authenticated user.
  Do not supply `campaignId`.
- `kind=npc` requires an owned campaign and creates the GM-owned character
  hidden from players.
- `kind=claimable` requires an owned campaign and creates a visible GM-owned
  premade character that players can later claim in Quest Portal.

The MCP never accepts an owner or user ID. A campaign player cannot create NPC
or claimable characters.

## Foundation

- `source=empty` uses the universal character sheet.
- `source=template` requires a `templateId` returned by
  `questportal_list_character_templates`.
- `source=coc7` uses the canonical enhanced Call of Cthulhu 7e template. Do not
  supply a `templateId`.

Template discovery returns published, enhanced, and authenticated-user-owned
templates only. Pass `nextCursor` unchanged while `hasMore` is true.

## Retry and result handling

Generate one stable idempotency key for the intended creation and reuse it only
for exact retries. On `CHARACTER_CREATION_IN_PROGRESS`, wait briefly and retry
with the same inputs and key. On `IDEMPOTENCY_KEY_CONFLICT`, compare the intended
request; do not change keys merely to bypass the conflict.

The result is a compact summary and Quest Portal URL. It intentionally omits
raw sheet and Yjs state.

# Character discovery and metadata

Use `questportal_list_characters` without `campaignId` to list standalone
characters owned by the authenticated user. Supply a `campaignId` to list the
campaign characters visible to that account. Pass `nextCursor` unchanged while
`hasMore` is true. Each result reports whether the account can update it.

`questportal_update_character` changes only the supplied `name`, `tagline`, or
campaign `visibility`. Omit `campaignId` for standalone characters. Standalone
visibility cannot be changed. Use an empty string to clear a tagline. Ownership,
placement, claimability, system, template, and lifecycle status cannot be
changed through the public MCP.

# Character portraits

Use `questportal_update_character_portrait` to replace the portrait of an
active character that reports `permissions.canUpdate=true`. Omit `campaignId`
for a standalone character and supply it for a campaign character.

Send canonical base64 JPEG, PNG, or WebP bytes with the matching `contentType`.
Remote URL imports and clearing or removing a portrait are not supported. Use
one stable idempotency key for the intended character and bytes, and reuse it
only for an exact retry. If `replayed=true`, the existing immutable upload was
reused; the character update was still safely applied. The result includes the
portrait URL and character URL without exposing raw storage or sheet state.

# Ordinary rich-text sheet tabs

Use `questportal_get_character_sheet` first without `tabId` to get a compact
visible-tab manifest. Ordinary `note` tabs include a revision and whether the
authenticated account may edit them. Supply `tabId` to read one note tab as
`QuestPortalCharacterSheetTab/v1` content.

Use `questportal_update_character_sheet` with the complete updated tab content
and the revision returned by the read. An `updated` result means that exact
content was stored. `already_applied` makes exact retries safe. On `conflict`,
read the tab again before deciding how to reconcile. A `merged` result means a
concurrent collaborative edit was preserved; read the tab again to inspect the
combined content.

Custom tabs are discoverable but their structured state is not returned or
writable through these generic tools. Smart-sheet state is not supported. The
tools do not expose raw Yjs updates. Character claiming, deletion, and
archiving also remain outside the public MCP.

# Legacy CoC7 structured sheets

Use `questportal_get_coc7_character_sheet` for a character created from the
legacy enhanced CoC7 foundation. It returns bounded characteristics, skills,
conditions, weapon selections, editable custom weapon definitions, and a
revision. It intentionally omits raw Firestore data. Read ordinary CoC7 note
tabs separately with `questportal_get_character_sheet`.

Read immediately before calling `questportal_update_coc7_character_sheet` and
supply `expectedRevision`. Patch only the intended sections:

- Characteristics use exact `objectId` values and may change `score`,
  `maxScore`, or both.
- Skills use exact `objectId` values and may change `baseScore`, `score`,
  `visible`, or any combination.
- Conditions use the exact returned `name` and an `active` boolean.
- `weaponIds` is the complete selected-weapon list. Use
  `questportal_list_coc7_weapons` for official IDs and the sheet read for
  character-specific custom IDs.
- `customSkills` creates or edits a custom skill's name, score, and visibility.
  A new custom skill requires `score`. When editing a formula-backed custom
  skill, omit `score` and change only its name or visibility; structured
  `scoreRoll` values remain read-only.
- `customWeapons` creates or edits the same bounded definition fields as the
  CoC editor: name, damage, range, attacks per round, extra attacks,
  ammunition, malfunction, and associated skill. Selection remains controlled
  by `weaponIds`.

For a new custom definition, generate one stable unique ID beginning with
`cthulhu-custom-item-`, using only letters, digits, `_`, `.`, `:`, or `-` after
the prefix. Reuse that ID for every exact retry. For edits, use the exact ID
returned by the sheet read. A custom weapon may reference a custom skill created
in the same update. Custom-definition deletion remains outside this tool.

## Rules-aware dependent-value blueprint

The update tool stores literal values and does not run a CoC rules engine. When
creating, importing, or intentionally changing the relevant core values,
calculate the affected numeric dependent fields and include them in the same
revision-fenced update:

- Hit Points maximum is `floor((CON + SIZ) / 10)`. For a new character without
  recorded damage, set both HP `score` and `maxScore` to that value. For an
  existing character, preserve current damage unless the user asks otherwise.
- Build comes from `STR + SIZ`: up to 64 is -2; 65–84 is -1; 85–124 is 0;
  125–164 is 1; 165–204 is 2; 205–284 is 3; 285–364 is 4; 365–444 is 5;
  445–524 is 6; above 524 add one Build per additional started block of 80.
- Movement Rate starts at 8, is 7 when both DEX and STR are below SIZ, and is 9
  when both are above SIZ. If a known age is at least 40, reduce it by one at
  40 and by one more for each additional decade, to a minimum of 1.
- Magic Points maximum is `floor(POW / 5)`. For a new character without spent
  points, set current MP to the same value; preserve spent MP on ordinary
  updates.
- Initial Sanity normally follows POW, capped at 99. Do not reset an existing
  investigator's current Sanity merely because POW changes.
- Dodge base is `floor(DEX / 2)`. Update `baseScore`; update the current score
  only when creating/importing or when the user's requested change requires it.
- Luck is independent and should come from the requested or imported value.

Use exact IDs returned by the read instead of assuming IDs from the labels.
Structured `scoreRoll` values remain read-only; Damage Bonus is the notable
legacy structured characteristic that uses one. Do not replace it with an
invented numeric score.

Roll buttons and modifier widgets belong in ordinary rich-text tabs. CoC7 note
tabs accept the same `rollButton` and `modifierWidget` nodes and formula syntax
as Quest Portal notes through `questportal_update_character_sheet`; creating a
widget stores the control but does not execute a roll.

## Generation and import composition

Do not look for a separate generation or import tool. Compose the supported
operations: create the CoC7 character, read its structured sheet, calculate or
extract the requested values, apply one coherent structured update, then add
any narrative content or roll widgets through ordinary rich-text tabs. For an
import, preserve the source values and ask about anything unreadable instead of
inventing it.

An `updated` result means the patch was committed. `already_applied` makes an
exact retry safe. On `conflict`, read again and reapply only the user's intended
changes. Smart sheets remain unsupported.
