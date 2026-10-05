# Examples and acceptance cases

These are expected behaviors, not claims that native host acceptance has passed.
Use synthetic drafts and remove them after an authorized host test.

| Request | Expected behavior |
| --- | --- |
| “Create Mira, a level 3 Wizard, and fill in her spells.” | Explain name-only creation; call `create_character` with name only for the requested draft. Build a plan and guide manual entries and catalog choices. Never report spells applied by chat. |
| “My attack bonus is +5; roll with advantage against AC 14.” | `roll_check` with `modifier:5`, `kind:"attack"`, `mode:"advantage"`, `dc:14`; report returned dice/total. No slot or resource spend. |
| “Roll my death save.” | If current modifiers are unknown, request them or a snapshot. Use `kind:"death-save"`; DC is 10. Explain that this roll does not update death-save tracks. |
| “I finished a long rest.” | Guide the explicit sheet action after table confirmation; review resources and per-class Hit Dice. Do not call a nonexistent rest tool. |
| “Retrieve the character on my phone.” | No server lookup. Request Attach or exported JSON; do not create a replacement without being asked. |
| “Display that damage roll again.” | Call `show_roll_result` with the exact returned roll; no new random roll. |

Host gates still to run: install/discover tools, name-only creation, explicit
Attach, JSON round-trip, storage/reload behavior, physical mobile, inline roll
cards and separately authorized session/event delivery with a real callback.
Standalone Chromium checks do not establish these native-host outcomes.
