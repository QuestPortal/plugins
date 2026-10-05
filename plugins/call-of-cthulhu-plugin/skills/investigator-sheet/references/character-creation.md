# Create an investigator

## Choose the procedure

Establish era, concept/occupation, age, party role and the table's creation method.
The [official simplified guide](https://cthulhuwiki.chaosium.com/investigators/)
provides a fast starting procedure. Full occupation budgets and age adjustments
belong to the Keeper Rulebook/Investigator Handbook method. Do not combine pieces
of these procedures and label the result rules-legal. For quick assigned pregens,
say explicitly that the values are custom and need Keeper approval.

Work through characteristics, occupation/personal skills, current resources,
weapons, equipment and backstory. Make a party complementary: vary investigative,
social, practical and combat strengths, not just names. Use original backstories
and a shared reason to investigate without importing an adventure's secret plot.

## Build supported inputs

Read [workflows](workflows.md) for schema details and retries. For one character,
pass profile/detail fields directly to `create_investigator` with a fresh
`requestId`. For a group, use `{ requestId, investigators: [...] }` with at most
20 members. Larger requests need separate batches and IDs; report every outcome.
Do not wrap a single creation in an unsupported `character` field.

- Supply the eight characteristic values when a populated build is requested.
- Use canonical skill IDs or recognized short IDs; add a specialization using
  its base skill ID and `specialization`. Do not create duplicate skill IDs.
- Link each weapon to an existing skill ID. New weapons need ID, name, skillId
  and damage; avoid ungrounded weapon statistics.
- Set current resources only. Do not send resource maxima. On creation, omitted
  HP/MP use derived maxima, Sanity starts from POW bounded by its maximum, and
  omitted Luck is a neutral **50 placeholder**, not a rolled result. Explicit
  zero stays zero. Supply intended Luck for a completed assigned build.
- Include suitable profile, backstory, inventory and notes. Omitted values are
  neutral defaults, not evidence of a complete investigator.

Dodge and own language initialize from DEX/EDU; other omitted skills use sheet
bases. Check derived HP, MP, Sanity limit, movement, build and damage bonus in the
result. These calculations do not establish budget or age-rule compliance.

## Deliver and revise honestly

Call the actual creation tools for a requested sheet; do not stop at JSON in chat
when populated tools are available. Explain per-member errors and custom-build
status. Tool success means payload prepared. Only sheet evidence establishes
loaded/applied/local-save status. Recommend JSON export if storage is unavailable.

For later changes, obtain a fresh Attach and use `revise_investigator` with the
exact snapshot and only intended changes. Do not construct a base from memory.
Changing characteristics does not heal current HP/MP or reset existing skills.
See the revision and stale-snapshot rules in [workflows](workflows.md).
