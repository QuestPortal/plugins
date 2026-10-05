# Examples and acceptance cases

These are expected behaviors, not claims that native host acceptance has passed.
Use synthetic drafts and remove them after an authorized host test.

| Request | Expected behavior |
| --- | --- |
| “Create Mira, a level 3 Wizard, and fill in her spells.” | Establish missing choices, then use `create_character` with a fresh requestId and populated fields. Supply complete class/spell entries and preserve casting-class links. Do not infer rules legality or saving from a prepared result. |
| “My attack bonus is +5; roll with advantage against AC 14.” | `roll_check` with `modifier:5`, `kind:"attack"`, `mode:"advantage"`, `dc:14`; report returned dice/total. No slot or resource spend. |
| “Roll my death save.” | If current modifiers are unknown, request them or a snapshot. Use `kind:"death-save"`; DC is 10. Explain that this roll does not update death-save tracks. |
| “I finished a long rest.” | Guide the explicit sheet action after table confirmation; review resources and per-class Hit Dice. Do not call a nonexistent rest tool. |
| “Retrieve the character on my phone.” | No server lookup. Request Attach or exported JSON; do not create a replacement without being asked. |
| “Display that damage roll again.” | Call `show_roll_result` with the exact returned roll; no new random roll. |

Host gates still to run: install/discover canonical and legacy tools, populated
single/batch creation and partial failures, replay and stale revisions, explicit
Attach, JSON round-trip, storage/reload behavior, physical mobile, inline roll
cards and separately authorized session/event delivery with a real callback.
Standalone Chromium checks do not establish these native-host outcomes.

Additional contract cases:

- Create 23 requested characters in batches of 20 and 3 with distinct request IDs.
  Preserve identity/order and report per-index validation failures.
- Repeat an identical delivery after local edits: retain those edits and report
  already applied. Reuse with a changed successful member must reject it.
- Fix a failed batch member at its original index, keeping successful members
  identical; do not duplicate successful drafts in a fresh batch.
- Revise only after explicit current Attach. After an intervening local edit,
  the old snapshot must conflict; request a fresh snapshot and new request ID.
- Submit invalid fields, out-of-range values and malformed event data: report
  errors, preserve current work and never invent a result or reroll to display it.
