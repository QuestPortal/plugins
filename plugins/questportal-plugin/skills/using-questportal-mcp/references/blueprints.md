# Outcome-oriented blueprints

These are adaptable compositions, not automatic checklists. Start from the user's requested outcome and current identifiers. Read only what helps resolve ambiguity or preserve state, and create or mutate only resources the request authorizes.

## Set up a campaign

When the user explicitly wants a new campaign, create it with the intended name and description and a stable idempotency key. Verify the returned campaign when downstream actions depend on its exact state.

Then branch by intent:

- If the user also supplied and authorized profile or cover media, upload it to the new campaign, reuse stable keys on retries, and verify the media URLs. Reposition a cover only if a nondefault crop was requested.
- If initial campaign notes are part of the request, create each with complete initial rich content. Use private visibility by default and campaign visibility only when sharing with members is explicit.
- If the user asked for an invite, explain that the public MCP can inspect safe invite-link metadata but cannot create, reveal, reset, revoke, or distribute an invite URL.

Do not create photos, notes, or a generic campaign merely because they are common setup artifacts. If the user wants a plan or template only, return that without mutations.

## Prepare a session

Resolve the campaign from an exact supplied ID or the accessible campaign list. Use `questportal_list_notes` to find likely session, location, NPC, or recap notes, then get only the notes relevant to the requested preparation.

Choose the smallest supported outcome:

- For a new session note, create the final initial document in one call. A useful shape might include the session H1, goals, scenes, clues, NPCs, and follow-up tasks, but content follows the user's system and brief rather than a fixed template.
- For changes to an existing note, get its current document and revision, preserve everything not being changed, update the complete document, resolve conflict/merge statuses, and verify.
- For a map or handout, settle the destination and placement, get the note, build the candidate insertion, and establish writability before uploading the immutable asset. Then get the latest note again, reapply the insertion as a `CustomImage`, update, and verify. If writability is uncertain, stop before upload and obtain user direction.

Do not automatically make a private preparation note campaign-visible. Do not create speculative notes for every topic mentioned in source material.

## Schedule an upcoming campaign session

Resolve the exact campaign and confirm the authenticated user's owner or player role. Get the campaign schedule before deciding whether the task is a read, an owner-managed schedule change, a personal response, or a calendar export.

For schedule inspection, return the configured rules and bounded upcoming session times. List occurrences when the user needs a stable occurrence ID, the next scheduled time, their own response, calendar revision metadata, or a response roster. A generated occurrence is not a completed session-history record.

For an owner-requested schedule change, get the schedule immediately before writing. Preserve its complete identity, name, rules, start dates, timezone, exceptions, settings, and revision; change only the requested fields. Pass the returned `updatedAt` as `expectedUpdatedAt`, save once, then get the schedule and list occurrences to verify the stored contract and generated times. To create the first schedule after a `not_configured` result, use `expectedUpdatedAt: null`, set both schedule IDs to the campaign ID, set `updatedAt: 0`, and provide the complete intended schedule. On conflict, reread and rebase the requested change instead of resubmitting stale state.

For a response, list occurrences immediately before calling `questportal_set_campaign_schedule_occurrence_response`. Set the authenticated member's own response to `yes`, `no`, or `null`; there is no supported way to respond for another member. Verify the returned response, and read the roster only when the requested outcome needs aggregate or member-level state.

For calendar export, list occurrences and pass one returned ID to `questportal_get_campaign_schedule_occurrence_ics`. Treat the result as a manual-import file. The public MCP does not create external calendar events or provide ongoing synchronization.

Scheduling requires the account's campaign-scheduling preview access. The public MCP cannot delete a schedule, invoke the product's nested AI scheduling assistant, or run a repair/reconciliation operation. See [scheduling.md](scheduling.md) for the full recurrence and revision contract.

## Answer from a campaign library

Resolve the exact campaign from a supplied ID or the accessible campaign list. Call `questportal_list_campaign_library_sources` when the user asks what is available, names a source without its exact ID, or expects the answer to use a particular book or PDF. When the user names a source, pass its name or publisher as `query` so discovery filters the full accessible set. If more matching sources are needed, pass `nextCursor` unchanged with the same campaign ID and query until the source is found or `hasMore` is false. If the requested source is listed with `searchable: false`, state that its content is not ready to query; do not silently substitute another source.

Search with `questportal_search_campaign_library` using a focused natural-language question. Pass only the relevant returned `sourceIds` when the user constrained the source; otherwise search the tool's bounded accessible source set. If `sourceSelectionTruncated` is true, narrow to discovered source IDs before treating an empty search as authoritative. Refine once with materially clearer terminology when the first search is weak, but do not broaden beyond the user's source constraint. Retrieval counters help diagnose the authorized pipeline but are not evidence for the answer.

When a relevant search excerpt is too narrow to establish a rule, table, list, or surrounding explanation, call `questportal_read_campaign_library_context`. Reuse the `campaignId` from the search request, pass that result's `sourceId` and opaque `contextToken` unchanged, and request only the adjacent chunks needed. On `INVALID_CONTEXT_TOKEN`, `LIBRARY_SOURCE_VERSION_CHANGED`, or `LIBRARY_CONTEXT_NOT_FOUND`, search again and use only one new result's source ID and token. Do not try to reuse adjacent chunk coordinates or use context expansion merely to reproduce more source text.

Build the answer from the returned excerpts:

- Tie each factual claim to excerpt evidence and cite its exact returned Quest Portal URL near that claim.
- Preserve source distinctions when results from multiple books or PDFs differ, and identify an inference as inference.
- Prefer a concise synthesis over reproducing long excerpts.
- If evidence is empty, incomplete, or conflicting, state what the available sources do and do not establish rather than filling gaps from memory.

Campaign-library reads do not authorize note creation or updates. Do not download raw PDFs, request unrestricted full pages, expose inaccessible source IDs, or use browser automation or private APIs as a fallback.

## Answer from campaign notes

Resolve the exact campaign from a supplied ID or the accessible campaign list. Call `questportal_search_campaign_notes` with one focused natural-language question. Use `visibility: campaign` when the user asks about shared campaign knowledge; use `private` only when the authenticated campaign owner explicitly wants their private notes included. Players cannot expand their access by requesting `all` or `private`.

Build the answer only from returned current excerpts. Cite each supporting result's exact Quest Portal note URL near the claim it supports, distinguish inference, and say when results are empty, weak, or conflicting. Retrieval counts describe the authorized pipeline and are not evidence. Use `questportal_get_note` only when a relevant result must be read in full and that broader accessible-note read is necessary for the user's request; there is no note-context expansion tool.

On `NOTE_CONTENT_SEARCH_DISABLED`, tell the user the campaign owner must enable **Search note contents** in campaign settings. On `NOTE_CONTENT_SEARCH_INDEXING`, retry later. On `NOTE_CONTENT_SEARCH_REQUIRES_PRO`, explain the owner entitlement requirement without making claims about the caller's plan. On `NOTE_CONTENT_SEARCH_UNAVAILABLE`, state that search is not available for the campaign without guessing whether configuration or a transient failure is responsible. Do not work around any of these states by enumerating and reading every note, using browser automation, or calling private APIs.

Searching notes does not authorize a note mutation. Create or update a note only when the user separately asks for that supported write, then follow the normal complete-document, revision, conflict, and verification workflow.

## Review past session history

Resolve the campaign from an exact supplied ID or the accessible campaign list. If the session is not already identified, call `questportal_list_sessions` with the smallest useful limit: one for “latest,” the requested count for a comparison, or bounded pagination until the named session is found. Do not enumerate unrelated history.

Get each selected session before requesting event detail. Use an available curated story as the primary recap and label event-derived conclusions separately. Treat an unavailable or historically unlinked story as normal; never guess a story-note association from timestamps.

Call `questportal_get_session_timeline` only for evidence the question needs:

- Keep the default attendance, scene, and dice filters for a general event summary.
- Narrow to attendance and dice for cross-session participation or roll comparisons.
- Add map activity only when movement or scene-map interaction matters.
- Add speech only when the request asks for dialogue, quotations, or transcript-backed evidence—not as background enrichment.

If transcript access is unavailable, retry later or answer from the non-speech evidence with the limitation stated. Do not infer a missing subscription, bypass the public capability check, or request raw transcript data. On `INVALID_CURSOR`, restart that exact timeline without a cursor because its source may have changed.

Session-history reads do not authorize writes. Return the requested summary in conversation unless the user separately asks to save it. If they do, treat that as a distinct note mutation: resolve the destination note, preserve its complete content, and follow the normal conflict and verification workflow.

## Build a campaign knowledge base

First inspect campaign and note metadata so the result complements existing material. Read the notes whose contents affect the proposed organization. Offer a lightweight architecture in prose before writes when the desired boundaries are genuinely ambiguous.

With the user's requested write scope, create or update only the necessary index, location, faction, rules, or session notes. Use complete content at creation, exact note links only when their IDs and mention context are known, and plain text otherwise. Preserve existing widgets and mentions during updates. An index note can provide navigation, but create it only when the user asked for the knowledge base—not as an unsolicited convenience.

If the requested knowledge base includes sidebar organization, read the relevant Campaign or Private sidebar and use its revision to create only the needed folders or place items. Keep organization within that visibility and reread after meaningful changes. The index note remains optional and should be created only when it serves the user's requested outcome.

## Organize existing notes

List all in-scope note metadata through pagination and use titles, visibility, folder paths, and pending-candidate flags to understand the current layout. Read bodies only when content is needed to classify, rename, consolidate, or index them.

Supported organization can include:

- Renaming a note by changing its first H1 through a preservation-safe full update.
- Improving headings, links, or structure inside selected notes while preserving unrelated content.
- Creating an index note or folders when explicitly requested.
- Moving or reordering active items within one Campaign or Private sidebar after a fresh sidebar read.
- Reporting a proposed cross-visibility or destructive arrangement for the user to apply elsewhere.

For sidebar writes, resolve the intended visibility, parent, and relative placement; pass the fresh revision; reread and reconsider after a conflict; and verify the final hierarchy. The public MCP cannot move items between Campaign and Private visibility, change an existing note's visibility, archive, restore, or delete. If “organize” could mean one of those, distinguish the supported changes before mutating.

## Organize a scene bar

Resolve the owned campaign, then call `questportal_get_scene_bar` to capture the complete current hierarchy and revision. Use the returned IDs rather than matching loosely on names. Before writing, translate the requested layout into root items and one-level folder contents: folders can exist only at the root, while scenes can be at the root or inside one folder.

Apply the smallest sequence of changes:

- Create a requested folder with `questportal_create_scene_folder`, a stable idempotency key, and a placement relative to another root item.
- Reorder an existing root item or move a scene into or out of a folder with `questportal_move_scene_bar_item`. Any `before` or `after` reference must be a sibling in the destination.
- To use an existing gallery scene, page `questportal_list_scene_gallery` until the exact scene is found, then read the scene bar immediately before calling `questportal_add_gallery_scene_to_bar`.
- To create a new scene, call `questportal_create_scene` once with its complete initial name, description, required image bytes, and stable idempotency key. It appears at the root end; reread the bar before moving it.

Each successful write changes the scene-bar revision. Reread before the next dependent write rather than reusing the prior revision. On `conflict`, reread, re-resolve IDs and placement against the new hierarchy, and continue only if the original intent still holds. On gallery `already_added`, reread: if the scene is active in the wrong location, move that existing scene instead of trying to add it again. Finish by rereading and checking the exact root order, folder membership, and playing/player-visibility fields that must remain unchanged.

Scene content, soundtrack, and bar organization use different revisions. Use `questportal_get_scene` plus `questportal_update_scene` for name, description, or background-image changes; use `questportal_get_scene_soundtrack` plus the catalog-attachment, upload, reorder, or removal tool for music changes; and use the scene bar plus organization tools for placement. The public MCP cannot alter map, grid, or fog; change player visibility; play or preview a scene; remove a scene from the bar; or delete a scene. Removing soundtrack music does not delete the underlying catalog asset or uploaded Storage object.

## Find music for a scene

Use the scene name, description, setting, and intended mood to form a concise `questportal_search_music` query. Search again with one materially different mood, genre, or environment term when the first results are weak; do not fetch large variations merely to create options. Compare the returned names, descriptions, tags, creators, attribution, and streaming status, then present a short set of track IDs with reasons tied to the scene. For monetized use, mention only the exact returned `approvedMonetization` forms. Do not present truncated attribution as complete credit. Searching does not preview music. If the user has already authorized choosing and attaching a suitable result, read the destination soundtrack immediately before calling `questportal_attach_scene_catalog_music` with the selected exact ID and current revision; otherwise present the shortlist and let the user choose. Verify the append with another soundtrack read.

When the user instead supplies or authorizes a new local audio file, resolve the destination scene, prepare the upload with the exact byte length, type, display name, and a stable idempotency key, then submit the binary file directly using the returned multipart form. Get the soundtrack immediately before completion and pass its current revision. After completion, get the soundtrack again and verify that the track was appended while all earlier tracks remain. Stop if the file is not MP3, is over 100 MiB, or cannot be accessed as authorized input. Uploading a new file and attaching a catalog search result are separate capabilities with the same revision-safe append behavior.

For an order change, read the soundtrack and build the full desired list from its exact association IDs. Call `questportal_reorder_scene_music` with every returned `associationId` once, then reread to verify the complete visible order. Association IDs distinguish duplicate legacy uses of the same track; unsupported legacy tracks omitted from the read remain in their current slots. For removal, read first and call `questportal_remove_scene_music` with the exact asset `id`; reread to verify every association carrying it is absent and all remaining tracks kept their relative order. Rebuild the intended mutation after any conflict rather than blindly substituting a newer revision.

## Create or manage a character roster

Resolve the campaign and confirm the authenticated account's role. Use `questportal_list_characters` with the campaign ID to page through the visible current roster. Treat each result's permissions as authoritative; visibility alone does not grant update access.

For an owned campaign, create only the requested NPC or claimable characters. Choose the intended empty, template, or CoC7 foundation, discover a template ID first when needed, and use one stable idempotency key per logical creation. The public MCP cannot create a campaign player character on another user's behalf or assign an owner ID. Verify created characters through the returned summary and a fresh roster read when downstream work depends on their placement or visibility.

For existing characters, apply only supported changes:

- Update a name, tagline, or campaign visibility when the result reports update permission.
- Replace an editable portrait with supplied JPEG, PNG, or WebP bytes and a stable idempotency key.
- Read or update ordinary rich-text sheet tabs with the complete content and current revision.
- Read or revision-safely update supported legacy CoC7 structured fields by exact returned IDs.

The public MCP cannot claim, delete, archive, move, or change ownership, placement, claimability, system, template, or lifecycle status of an existing character. It cannot read or update generic custom-tab state or smart-sheet state. See [characters.md](characters.md) for the complete contracts and retry rules.

If the user explicitly wants a roster represented as campaign knowledge in addition to or instead of product character entities, use note tools. Create a complete roster note, or preserve and update an existing one, using a table or `collectionWidget` for known names, roles, players, status, or other requested fields. Choose campaign visibility only if members should see it, and describe it as a note-based roster. Preserve existing sheet `link-mention` nodes; add one only when every required identifier and owner context is known from supported context.
