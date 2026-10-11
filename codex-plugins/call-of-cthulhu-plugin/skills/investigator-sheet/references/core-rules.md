# Core rules and automation boundaries

## Percentile checks

For a [skill check](https://cthulhuwiki.chaosium.com/rules/skill-rolls-and-difficulty-levels.html),
roll d100 against the Keeper's difficulty: regular uses the skill, hard uses
half and extreme uses one-fifth, rounding fractions down. A justified pushed
attempt changes the approach and raises the consequences of failure; do not
silently reroll a failure. Combat rolls cannot be pushed.

The plugin's `roll_check` takes the shared value, difficulty and a modifier from
−2 to +2: positive means bonus dice, negative means penalty dice. These alter
percentile candidates, not the skill by a flat numeric bonus. Read and report
the returned target, roll, outcome and success; never fabricate a critical,
fumble or missing result. See [workflows](workflows.md) for input details.

## Combat and danger

[Combat](https://cthulhuwiki.chaosium.com/rules/combat.html) generally proceeds
in DEX order. A defender's fight-back and Dodge choices resolve ties differently:
fight-back ties favor the attacker, while Dodge ties favor the defender. Compare
success levels under the selected rule. Damage, armor and wounds then need
adjudication; the plugin has no full combat-turn or opposed-combat resolver.
Do not reuse Pendragon's `opponent` parameter here.

`roll_damage` evaluates the supplied formula and damage bonus; it does not apply
injuries. HP tracks injury, MP powers relevant effects, Sanity tracks exposure to
horror, and Luck has its own table-approved uses. The Keeper determines sanity
loss and other consequences. No generic roll spends Luck, applies damage, changes
Sanity or advances an investigator automatically. Guide explicit sheet edits or
use a requested revision with a current attachment.

## Beyond the implemented tools

Pushing eligibility, Luck spending, sanity consequences, combat maneuvers,
healing, development, spells and campaign advancement need the applicable rules
and Keeper decisions. The sheet records relevant values; it is not an automated
Keeper. Ask for the relevant approved rule/choice when missing rather than
inventing a paid-book rule or silently importing Pulp or older-edition behavior.
Use [sources](sources.md) for official entry points and scope.
