# D&D: edition and sheet map

This plugin targets **D&D 5.5e, the 2024 revision of fifth edition**, using
SRD 5.2.1. Do not silently substitute 2014 rules or promise an edition selector.
The adventuring party explores, negotiates and fights; the DM describes the world
and decides when uncertainty requires a roll. The sheet records a character;
it does not replace the DM or supply a complete campaign engine.

| Sheet area | What to establish |
| --- | --- |
| Abilities and skills | Six ability scores, proficiency choices and applicable bonuses |
| Classes | Each class's level, Hit Die, spellcasting ability and feature choices |
| Combat | AC, initiative, speed, HP, temporary HP, conditions and death saves |
| Spells | Casting class, preparation, slots, Pact Magic and concentration |
| Features and resources | Uses, recovery settings, Heroic Inspiration and manual effects |
| Equipment and notes | Weapons, inventory, currency and campaign context |

The implemented pickers contain **339 spells and 38 weapons**, counted from the
runtime catalogs at `d640dd0`. These are editable catalog entries, not every paid
book's content or automatic enforcement of spell/weapon effects. Class-specific
casting and class-owned Hit Dice matter for multiclass characters. Slot and
maximum-HP suggestions apply only when the user explicitly chooses them.

Read [creation](character-creation.md) for the setup sequence,
[core rules](core-rules.md) for adjudication boundaries and
[sources](sources.md) for the edition and implementation provenance.
