# Examples and acceptance cases

These examples describe expected behavior. Native host acceptance remains unrun;
use synthetic drafts and clean them up after an authorized test.

| Request | Expected behavior |
| --- | --- |
| “Create Sir Rowan with Sword 15 and Loyalty 16.” | Use `create_character` or `create_knight` with a fresh requestId, skill ID `sword` and the intended Passion fields. Confirm choices; report prepared versus loaded/saved separately. |
| “Sword 15 against my rival's 12, with their −5 modifier.” | One `roll_check` with `value:15`, `statistic:"skill"`, `opponent:{value:12,modifier:-5}`. Report both dice and `resolution`, not just own success. |
| “Roll critical horse damage; my mount has 5d6, plus 2.” | `roll_damage` with `formula:"horse+2"`, `horseDamageDice:5`, `critical:"weapon"`. The contract expands to 5d6+2+4d6; no knight damage-point adjustment. |
| “Roll my weapon damage.” | Obtain current sheet/values if missing. Do not accept illustrative `wd` defaults as the user's damage. |
| “Apply that wound and give me Glory.” | Explain the roll did not mutate the sheet. Establish table-approved consequences, request fresh Attach and use `revise_character` for the explicit changes, or guide manual edits. No automatic consequence or invented Glory tool. |
| “Find my knight from another computer.” | Request Attach/exported JSON. No server lookup, sync or replacement creation. |

See [tool contracts](tool-contracts.md) for executable argument shapes and
[workflows](workflows.md) for session recovery. Native gates include installation,
populated single/batch creation, partial failures, replay and stale revisions,
Attach, JSON round-trip, storage/reload, physical mobile and
real host session callbacks. A local mock or standalone browser does not prove them.

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
