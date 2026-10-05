# Examples and acceptance cases

These examples describe expected behavior. Native host acceptance remains unrun;
use synthetic drafts and clean them up after an authorized test.

| Request | Expected behavior |
| --- | --- |
| “Create Sir Rowan with Sword 15 and Loyalty 16.” | Call `create_knight` with name only; guide manual skill/Passion entry. Do not claim a populated sheet or pass extra fields. |
| “Sword 15 against my rival's 12, with their −5 modifier.” | One `roll_check` with `value:15`, `statistic:"skill"`, `opponent:{value:12,modifier:-5}`. Report both dice and `resolution`, not just own success. |
| “Roll critical horse damage; my mount has 5d6, plus 2.” | `roll_damage` with `formula:"horse+2"`, `horseDamageDice:5`, `critical:"weapon"`. The contract expands to 5d6+2+4d6; no knight damage-point adjustment. |
| “Roll my weapon damage.” | Obtain current sheet/values if missing. Do not accept illustrative `wd` defaults as the user's damage. |
| “Apply that wound and give me Glory.” | Explain the roll did not mutate the sheet; establish table-approved consequences and guide manual changes. No invented edit or Glory tool. |
| “Find my knight from another computer.” | Request Attach/exported JSON. No server lookup, sync or replacement creation. |

See [tool contracts](tool-contracts.md) for executable argument shapes and
[workflows](workflows.md) for session recovery. Native gates include installation,
name-only creation, Attach, JSON round-trip, storage/reload, physical mobile and
real host session callbacks. A local mock or standalone browser does not prove them.
