# Core rules and implemented actions

These are original summaries for the 2024 revision. Consult the
[official glossary](https://www.dndbeyond.com/sources/dnd/br-2024/rules-glossary)
and [SRD 5.2.1](https://www.dndbeyond.com/srd) for exceptions and exact wording.

## Tests and combat

A d20 test adds the relevant bonus and compares against a DC or, for an attack,
AC. Advantage uses the higher of two d20s; Disadvantage uses the lower. They
cancel when both apply. Natural 1/20 rules differ between attacks, death saves
and ordinary checks/saves. Critical attack damage doubles dice, not flat bonuses.

Combat uses initiative, movement and actions; Bonus Actions require a granting
rule and Reactions require a trigger. The DM resolves targets, cover, timing and
situational effects. A generic attack or damage roll is not a complete turn.

## Runtime behavior

`roll_check` needs the complete applicable `modifier`, a `kind` and optional
`mode`/known DC; use shared values. Death saves use DC 10. Initiative returns
no pass/fail verdict. `roll_damage` accepts bounded formulas and optional critical
dice. Both return results without mutating the draft. See [workflows](workflows.md)
for exact handling, result display and retries.

The sheet has explicit controls for damage/healing, slots, concentration,
Heroic Inspiration, feature uses, death saves and rests. Use those controls to
change state; do not infer a mutation from a chat roll. Death-save natural 1/20
state changes belong to the sheet action. Manually entered effects can still
require table adjudication.

The implemented Short Rest action refreshes Pact Magic and configured short-rest
resources. Spending a Hit Die is separate and belongs to its class. Long Rest
restores HP, all Hit Dice, ordinary slots and Pact Magic; it clears temporary HP,
resets death saves, reduces exhaustion by one and recovers configured resources.
Manual-recovery resources remain manual. Rest eligibility, duration and
interruptions must be resolved at the table first; a button is not proof of an
eligible rest. These are source-verified implementation details, not an exhaustive
class-feature rules engine.

For this edition, exhaustion reduces d20 tests by twice the level and Speed by
five feet per level; it does not reduce spell save DC. Keep each spell's casting
class/ability and attack bonus distinct. Choosing a spell or weapon from a picker
does not automatically enforce its effect or weapon mastery.
