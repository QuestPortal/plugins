---
name: using-questportal-mcp
description: Use when an agent must answer product-help questions from Quest Portal documentation; search grounded campaign-note excerpts or discover, search, and expand bounded context from books or PDFs in a campaign library with citations; inspect and manage campaigns, campaign scheduling, characters, session history, campaign media, invite-link metadata, rich notes, scene bars, or complete scene-music workflows through the public MCP; choose or sequence tools; recover from conflicts or retries; or compose supported multi-tool workflows without exceeding the current public surface. Triggers on "Quest Portal MCP", "Quest Portal help", "search my campaign notes", "search my campaign library", "answer from my book", "query my PDF", "schedule our next session", "create a Quest Portal character", "what happened last session", "manage campaign notes", "organize scenes", and "find scene music".
---

# Using Quest Portal MCP

This plugin connects to Quest Portal at `https://mcp.questportal.com/mcp` over Streamable HTTP. Authenticate through the client's browser-based OAuth flow before calling tools. The plugin already includes this skill; no separate skill installation is needed. For connection setup, access requirements, and recovery, read [connection and access](references/connection-and-access.md).

Use the registered `questportal_*` tools as the execution API. Their current schemas define the accepted inputs and outputs; this skill supplies selection, sequencing, domain rules, recovery, and verification.

## Quick Reference

| Need                                                                                      | Reference                                                                  |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Connect, authenticate, understand Pro eligibility, or recover a missing authorization     | [references/connection-and-access.md](references/connection-and-access.md) |
| Choose among tools, understand prerequisites, or recover from tool errors                 | [references/tools.md](references/tools.md)                                 |
| Answer from books or PDFs in an accessible campaign library with exact source links       | [references/blueprints.md](references/blueprints.md)                       |
| Answer from current accessible campaign or private note contents with exact note links    | [references/blueprints.md](references/blueprints.md)                       |
| Review session history, recaps, attendance, dice, map activity, or speech                 | [references/blueprints.md](references/blueprints.md)                       |
| Read or save campaign schedules, list occurrences, respond, or export an ICS file         | [references/scheduling.md](references/scheduling.md)                       |
| Create, preserve, update, link, or add images to rich notes                               | [references/note-content.md](references/note-content.md)                   |
| Create or update standalone, NPC, claimable, template, or CoC characters                  | [references/characters.md](references/characters.md)                       |
| Author formulas stored in note roll controls or widgets                                   | [references/dice-formulas.md](references/dice-formulas.md)                 |
| Compose a supported campaign, session, knowledge-base, note, scene-bar, or roster outcome | [references/blueprints.md](references/blueprints.md)                       |

## Operating approach

- [ ] **REQUIRED — Resolve the target:** Use the narrowest useful read. Use IDs already supplied by the user; list or get resources when the target is ambiguous or current state matters.
- [ ] **REQUIRED — Stay inside the public surface:** Do not substitute private APIs, browser automation, or guessed tool names for unsupported operations.
- [ ] **REQUIRED — Separate help from execution:** Product documentation can explain Quest Portal capabilities that the MCP cannot perform. Use only registered execution tools for actions and cite the canonical documentation URL in help answers.
- [ ] **REQUIRED — Ground campaign-library answers:** Page through accessible-source discovery only as needed, search only the relevant campaign library, expand a relevant hit when its excerpt is insufficient, base the answer on returned excerpts, and cite the exact Quest Portal URLs. State when the available evidence is insufficient.
- [ ] **REQUIRED — Ground campaign-note answers:** Search only the requested campaign and permitted visibility, base the answer on returned current excerpts, and cite the exact Quest Portal note URLs. State when search is disabled, indexing, unavailable during internal testing, or insufficient.
- [ ] **REQUIRED — Preserve authorization boundaries:** Proceed with an ordinary mutation the user clearly requested. Clarify an ambiguous target or destructive intent, and explain when the requested capability is unsupported.
- [ ] **REQUIRED — Prefer one complete creation:** When a creation tool accepts initial content, supply the intended content there instead of creating an empty resource and immediately updating it.
- [ ] **REQUIRED — Preserve retry identity:** Reuse one stable idempotency key for every retry of the same logical creation or upload. Do not change the key to bypass a conflict; use a new key only for a genuinely new action or changed payload that the user still wants.
- [ ] **REQUIRED — Verify meaningful writes:** Reread the changed resource, especially after an ambiguous failure, note update, media write, `merged`, or `already_applied` result.
- [ ] **REQUIRED — Keep session history read-only:** Do not turn a session recap or timeline read into a note creation or update unless the user separately requests that supported write.
- [ ] **REQUIRED — Schedule from current state:** Read a schedule immediately before an owner write and preserve its complete revision-fenced contract. List occurrences immediately before an RSVP or ICS export, bind responses to the caller, and verify meaningful schedule changes with both a schedule read and occurrence list.

For a stale note revision, call `questportal_get_note`, reapply only the intended change to the latest complete document, and retry with the new revision. For `merged`, reread before making another edit. For rate limits, wait for the structured retry time and repeat the original request; preserve its idempotency key. On `AUTHORIZATION_OUT_OF_SYNC`, stop retrying, name the missing scope, and ask the user to reauthorize it. When the client is Codex, follow [Codex OAuth reauthorization](references/tools.md#codex-oauth-reauthorization) so the response includes actionable client steps; retry only after the user completes authorization.

## Boundaries worth checking early

The public MCP does not currently delete or archive campaigns or notes; delete a campaign schedule; invoke the product's nested AI scheduling assistant; expose schedule repair or reconciliation; write to an external calendar; create, reset, revoke, or reveal invite links; manage campaign members; move notes between Campaign and Private visibility; change an existing note's visibility; remove campaign media; write session history or stories; download raw transcripts or campaign-library PDFs; return unrestricted full-page library content; expand adjacent context around a campaign-note search result; edit scene maps, grids, or fog; change scene playing or player visibility; preview, remove, or delete scenes; claim, delete, archive, move, or change ownership of character entities; or execute dice rolls. It can inspect and revision-safely save complete campaign schedules, list generated occurrences and response rosters, set the caller's own response, export manual-import ICS content, search bounded current excerpts from enabled campaign notes, search bounded excerpts and expand a search hit into bounded adjacent context from accessible campaign-library books and PDFs, search and attach catalog music, append newly uploaded MP3 audio, reorder or remove scene soundtrack associations, and update supported character fields, including portraits. Removing scene music does not delete its catalog asset or uploaded Storage object. If an outcome depends on another unsupported operation, state the limitation and continue only with an independently useful supported portion the user authorized.
