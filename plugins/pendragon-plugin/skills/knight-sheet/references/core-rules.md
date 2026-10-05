# Core rules and implemented resolution

## d20 resolution

Under the [official game-system overview](https://pendragonwiki.chaosium.com/rules/the-game-system.html),
compare a d20 to the modified statistic. Below the target succeeds; matching it
is critical. A natural 20 normally fumbles, except at statistic 20. Above 20,
the excess supplies a critical bonus. Characteristics do not gain extra
critical/fumble benefits. This is not D&D's roll-high-plus-bonus system.

Opposed rolls compare outcomes: a critical beats an ordinary success and two
criticals tie. Otherwise higher successful rolls prevail. A successful loser has
a partial success; a tie can retain failure consequences. Do not equate personal
success with winning an opposition.

The tool implements these classifications and returns a `resolution`. Pass the
actual shared statistic and situational modifier; read the returned verdict
rather than recomputing it from `success`. One `opponent` call rolls both sides.
See [tool contracts](tool-contracts.md) for bounds, above-20/below-zero handling
and examples. Exact runtime behavior is not evidence of full Core Rulebook coverage.

## Personality and campaigns

[Traits and Passions](https://pendragonwiki.chaosium.com/rules/traits-and-passions.html)
make personality and commitments mechanically consequential. Trait pairs express
opposed tendencies. Passion inspiration has prerequisites, limits and consequences;
a successful roll is not blanket permission for arbitrary bonuses. Ask the table
which Passion and affected activity apply, and let the GM resolve the outcome.
The plugin records these values but does not enforce all invocation conditions
or automatically apply inspiration consequences.

## Damage and recovery

The runtime accepts bounded d6 formulas, constants and `wd`, `bd`, `horse` terms.
Supply the shared knight's weapon-damage dice, brawling value and adjustments;
never use illustrative server defaults as character facts. Horse terms require
explicit mount dice. The implemented critical option adds +4d6 for weapon damage
or +2d6 for brawling once; it does not double the total. The complete expanded
pool cannot exceed 60 dice. These are the implemented contract, detailed in
[tool contracts](tool-contracts.md); use [sources](sources.md) for tabletop rules.

A roll does not subtract HP, apply armor, mark experience, award Glory, recover
wounds or advance the Winter Phase. Damage application, combat choices, healing,
family events and annual development remain manual/table-adjudicated workflows.
