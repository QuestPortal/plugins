# Public MCP tool guide

Use this guide to select and sequence tools. The live tool schema remains authoritative for fields, defaults, limits, and structured output.

## Shared rules

Every call requires an authenticated Quest Portal MCP connection. Public documentation reads do not require a campaign, character, Notes, or Scenes scope. Campaign, campaign-schedule, and session-history reads require `campaigns:read`; campaign-library source discovery, search, and context expansion require `library:read` (shown to users under Campaigns access); campaign mutations, complete schedule saves, and the caller's own occurrence-response changes require `campaigns:write`; character template discovery, character listing, rich-text sheet reads, and legacy CoC7 sheet reads require `characters:read`; character creation, metadata updates, portrait replacement, rich-text sheet updates, and legacy CoC7 sheet updates require `characters:write`; note listing, reading, and content search require `notes:read`; note mutations, including sidebar changes and image upload, require `notes:write`; scene and music-catalog reads require `scenes:read`; and scene, scene-bar, and scene-music mutations require `scenes:write`. `questportal_ping` is the connectivity check and does not replace a domain read.

Campaign, campaign-library, campaign-schedule, and session-history reads expose only active campaigns in which the authenticated user is an owner or player. Campaign-library tools additionally omit sources hidden from AI, hidden from a player, configured without library links, unsupported source types, or unavailable under the caller's entitlements. Invite-link reads, campaign mutations, and schedule saves are owner-only. An occurrence response can change only the authenticated member's own response. All scheduling tools require the caller's campaign-scheduling preview access (`canScheduleSessions`). Note reads, searches, and writes require active campaign membership; campaign notes are visible to members, while private notes are visible only to their owner. Note-content search additionally requires the campaign owner's internal-testing access, enabled setting, eligible current Pro access, and a ready index. A not-found-or-inaccessible response deliberately does not reveal which condition applies.

Personal Pro access permits the full supported tool surface, subject to granted scopes, roles, visibility, and feature gates. An enrolled shared-Pro recipient may use only explicitly supported operations in an eligible exact campaign when the server's rollout prerequisites are satisfied. Shared Pro is not blanket access to other campaigns or standalone resources. Creating campaigns and standalone characters requires personal Pro access. See [connection and access](connection-and-access.md) before diagnosing an entitlement failure; a successful connection alone does not prove eligibility for every tool.

Pagination cursors are opaque and bound to their campaign, target, filters, and authenticated session. Pass `nextCursor` unchanged to continue. Pagination is not snapshot-isolated, so concurrent changes can affect later pages. Speech cursors additionally detect regenerated timeline sources. On `INVALID_CURSOR`, restart the affected list or timeline without a cursor; never modify or decode a cursor.

## Tool index

| Tool                                                    | Behavior  | Primary use                                                           |
| ------------------------------------------------------- | --------- | --------------------------------------------------------------------- |
| `questportal_ping`                                      | Read-only | Check connection and receive the server revision receipt              |
| `questportal_get_agent_skill`                           | Read-only | Get the canonical public Agent Skill package metadata                 |
| `questportal_search_documentation`                      | Read-only | Find current public product-help pages semantically                   |
| `questportal_get_documentation_page`                    | Read-only | Read one public help page as bounded Markdown                         |
| `questportal_list_campaigns`                            | Read-only | Discover accessible active campaigns and roles                        |
| `questportal_get_campaign`                              | Read-only | Read one campaign's current details and media state                   |
| `questportal_list_campaign_library_sources`             | Read-only | Discover accessible books and PDFs in one campaign library            |
| `questportal_search_campaign_library`                   | Read-only | Search grounded excerpts with exact Quest Portal source links         |
| `questportal_read_campaign_library_context`             | Read-only | Expand one search hit into bounded, version-checked adjacent context  |
| `questportal_list_sessions`                             | Read-only | Discover recent sessions and compact attendance                       |
| `questportal_get_session`                               | Read-only | Read session metadata, recap, and recording availability              |
| `questportal_get_session_timeline`                      | Read-only | Page through normalized session activity and optional speech          |
| `questportal_list_campaign_invite_links`                | Read-only | Page through safe active invite-link metadata for an owned campaign   |
| `questportal_get_campaign_invite_link`                  | Read-only | Read deterministic current active-link metadata and count             |
| `questportal_create_campaign`                           | Mutation  | Create one campaign owned by the authenticated user                   |
| `questportal_update_campaign`                           | Mutation  | Change an owned campaign's name and/or description                    |
| `questportal_get_campaign_schedule`                     | Read-only | Read one campaign's complete configured schedule and revision         |
| `questportal_list_campaign_schedule_occurrences`        | Read-only | List bounded upcoming schedule occurrences                            |
| `questportal_get_campaign_schedule_occurrence_roster`   | Read-only | Read one occurrence's response roster                                 |
| `questportal_save_campaign_schedule`                    | Mutation  | Replace an owned campaign's complete revision-fenced schedule         |
| `questportal_set_campaign_schedule_occurrence_response` | Mutation  | Set the caller's own occurrence response                              |
| `questportal_get_campaign_schedule_occurrence_ics`      | Mutation  | Export one occurrence as manual-import ICS content                    |
| `questportal_update_campaign_profile_photo`             | Mutation  | Replace an owned campaign's profile image                             |
| `questportal_update_campaign_cover_photo`               | Mutation  | Replace an owned campaign's cover image                               |
| `questportal_update_campaign_cover_position`            | Mutation  | Reposition an existing cover image                                    |
| `questportal_list_character_templates`                  | Read-only | Discover templates usable by the authenticated user                   |
| `questportal_create_character`                          | Mutation  | Create a standalone, NPC, or claimable character                      |
| `questportal_list_characters`                           | Read-only | Discover standalone or accessible campaign characters                 |
| `questportal_update_character`                          | Mutation  | Change supported character metadata or campaign visibility            |
| `questportal_update_character_portrait`                 | Mutation  | Replace an editable character's portrait                              |
| `questportal_get_character_sheet`                       | Read-only | List visible tabs or read one ordinary rich-text sheet tab            |
| `questportal_update_character_sheet`                    | Mutation  | Replace one revision-fenced ordinary rich-text sheet tab              |
| `questportal_get_coc7_character_sheet`                  | Read-only | Read bounded legacy CoC7 structured sheet state                       |
| `questportal_list_coc7_weapons`                         | Read-only | Discover canonical legacy CoC7 weapon IDs                             |
| `questportal_update_coc7_character_sheet`               | Mutation  | Patch legacy CoC7 structured state by exact IDs and revision          |
| `questportal_list_notes`                                | Read-only | Discover accessible note metadata in one campaign                     |
| `questportal_get_note`                                  | Read-only | Read one complete canonical rich note and its revision                |
| `questportal_search_campaign_notes`                     | Read-only | Search bounded current note excerpts with exact note links            |
| `questportal_get_note_sidebar`                          | Read-only | Read one ordered Campaign or Private sidebar and its revision         |
| `questportal_create_note`                               | Mutation  | Create one note with complete initial rich content                    |
| `questportal_update_note`                               | Mutation  | Replace one note document with revision-aware conflict handling       |
| `questportal_create_note_folder`                        | Mutation  | Create a folder at a revision-fenced sidebar placement                |
| `questportal_move_note_sidebar_item`                    | Mutation  | Move or reorder an item within one revision-fenced sidebar            |
| `questportal_upload_note_image`                         | Mutation  | Upload an immutable image asset for later insertion into a note       |
| `questportal_search_music`                              | Read-only | Find selectable catalog tracks by mood, setting, creator, or tags     |
| `questportal_get_scene_bar`                             | Read-only | Read an owned campaign's ordered scene and folder hierarchy           |
| `questportal_get_scene`                                 | Read-only | Read editable scene content and its scene-content revision            |
| `questportal_get_scene_soundtrack`                      | Read-only | Read ordered scene music and its independent soundtrack revision      |
| `questportal_create_scene`                              | Mutation  | Create an image-backed scene with complete initial content            |
| `questportal_update_scene`                              | Mutation  | Patch editable scene content while preserving internal state          |
| `questportal_attach_scene_catalog_music`                | Mutation  | Append one current selectable catalog track to a scene                |
| `questportal_reorder_scene_music`                       | Mutation  | Reorder returned soundtrack associations without dropping legacy data |
| `questportal_remove_scene_music`                        | Mutation  | Remove a track association without deleting its underlying asset      |
| `questportal_prepare_scene_music_upload`                | Mutation  | Prepare a bounded direct MP3 upload form                              |
| `questportal_complete_scene_music_upload`               | Mutation  | Verify and append prepared audio to a scene soundtrack                |
| `questportal_create_scene_folder`                       | Mutation  | Create an idempotent top-level folder from a recent bar revision      |
| `questportal_move_scene_bar_item`                       | Mutation  | Reorder an item or move a scene into or out of a folder               |
| `questportal_list_scene_gallery`                        | Read-only | Browse available gallery scenes in stable scene-ID order              |
| `questportal_add_gallery_scene_to_bar`                  | Mutation  | Add an existing gallery scene to an owned campaign's scene bar        |

## Connectivity and campaign reads

### `questportal_ping`

Use it when connection health or the deployed server revision is in doubt. It is safe to repeat, but it returns no user or account identity. When account binding matters, use scoped campaign or note reads and ask the user to confirm the returned resource context. Do not use ping to prove identity, domain access, freshness, or mutation success.

### `questportal_get_agent_skill`

This plugin already includes the usage skill. Use this tool only when the user asks to inspect canonical skill metadata, update their guidance, or configure a separate agent environment. It returns the canonical public Agent Skill package URL, digest, and safe setup workflow; it does not install files itself. Do not install a duplicate skill for normal plugin use. For a separately requested installation, respect the user's project-versus-user scope, preflight an existing installation, never overwrite it without approval, and verify the downloaded archive when possible.

## Product documentation reads

### `questportal_search_documentation`

Use it when the user asks how Quest Portal works and the exact help page is unknown. Search accepts a natural-language query and returns a small set of current documentation snippets, page IDs, root-to-page breadcrumbs, relevance scores, and canonical URLs. Follow with `questportal_get_documentation_page` when a snippet is not enough to answer accurately. An empty result is authoritative for that query: refine it or offer the documentation home rather than inventing an answer. Do not treat a documented product feature as an executable MCP capability.

### `questportal_get_documentation_page`

Use it for the authoritative content of a known documentation page ID. Start without a position. When `nextStartCharacter` is non-null, pass it back with the returned `sourceVersion`; that keeps all chunks on one immutable published version. Restart from the beginning without those continuation values on `DOCUMENTATION_VERSION_UNAVAILABLE`, and search again on `DOCUMENTATION_PAGE_NOT_FOUND`. Cite the returned canonical URL in the answer. Avoid fetching every search result or every chunk once the user's question is answered.

### `questportal_list_campaigns`

Use it to resolve an unspecified campaign, inspect the user's owner/player role, or enumerate all accessible active campaigns through pagination. Avoid it when the user already supplied an exact campaign ID and only that campaign is in scope; `questportal_get_campaign` is narrower. Follow with `questportal_get_campaign` before a state-dependent change. The result excludes inactive or inaccessible campaigns and does not prove ownership beyond the returned role.

### `questportal_get_campaign`

Use it for the current name, description, role, profile/cover URLs, and cover position, or to verify a campaign mutation. It is the normal prerequisite for position changes and ambiguous retries. Do not infer why `CAMPAIGN_NOT_FOUND_OR_INACCESSIBLE` occurred. If the ID may be wrong, list campaigns or ask the user to identify the target.

### `questportal_list_campaign_library_sources`

Use it before answering from a campaign's marketplace books or imported PDFs, especially when the user names a source but has not supplied its ID. It returns only sources available to the authenticated active member after AI visibility, player visibility, source type, and entitlement checks. When looking for a named source, pass its name or publisher as `query`; filtering happens across the full accessible set before pagination. Pass `nextCursor` unchanged with the same campaign ID and query while `hasMore` is true and more matches are needed. `truncated` remains a compatibility alias for `hasMore`. `searchable: false` means the source is visible in the campaign library but its current content is not ready for semantic search. Do not infer that an omitted source is missing rather than hidden, restricted, unsupported, or unentitled. Use the returned source IDs verbatim in a narrowed search.

### `questportal_search_campaign_library`

Use it with a focused natural-language question after resolving the campaign. Omit `sourceIds` to search the bounded accessible searchable set in that campaign, or pass only IDs returned by source discovery when the user names particular sources. If `sourceSelectionTruncated` is true, narrow the request with discovered source IDs before treating an empty result as authoritative. Each result is a bounded excerpt from the current source version with its source, page, section path, relevance score, coordinates, authenticated opaque `contextToken`, and exact Quest Portal URL. The `retrieval` counts describe accessible sources and raw, version-eligible, hydrated, and returned hits; use them for troubleshooting, never as source evidence. Synthesize only claims supported by returned excerpts, cite the exact URLs near the claims they support, and label any inference. If a relevant result lacks enough surrounding context, use `questportal_read_campaign_library_context` with that result's source ID and token. If results are empty, weak, or conflicting, refine the query or state that the campaign-library evidence is insufficient. Do not replace missing evidence with general model knowledge, fetch a raw PDF URL, or attempt unrestricted full-page reads.

### `questportal_read_campaign_library_context`

Use it only after a relevant campaign-library search result needs surrounding material. Reuse the campaign ID from the search request, pass the result's `sourceId` and opaque `contextToken` unchanged, and choose zero to two chunks before and after, defaulting to one each. The token is authenticated, expires, and is bound to the caller, campaign, source, current version, and exact stored published chunk. The tool rechecks active membership, visibility, entitlement, and exact published version and returns at most five stored excerpts with exact links. Cite those links like search results. On `INVALID_CONTEXT_TOKEN`, `LIBRARY_SOURCE_VERSION_CHANGED`, or `LIBRARY_CONTEXT_NOT_FOUND`, search again and retry only with one new result's source ID and token. Adjacent chunks do not carry reusable tokens; do not use their coordinates to walk the page. Context expansion is bounded evidence gathering, not a way to reproduce a full book or PDF.

### `questportal_list_campaign_invite_links`

Use it when the user wants the set or history of active invite-link metadata for an owned campaign. Page with the returned cursor. It returns campaign ID, creation time, and active state only—never an invite ID, bearer token, or usable URL. Do not call it to invite someone, reveal a link, reset or revoke a link, accept an invitation, or manage members; none of those actions is public MCP functionality.

### `questportal_get_campaign_invite_link`

Use it for the deterministic current active-link metadata and active-link count of one owned campaign. It has no invite-link identifier input because it does not expose individual link credentials. Prefer it over listing when the current state/count is the outcome. On `INVITE_LINK_STATE_UNAVAILABLE`, retry later; if it persists, direct the user to Quest Portal support.

## Session-history reads

### `questportal_list_sessions`

Use it when the exact session is unknown, when “latest session” must be resolved, or when the outcome compares multiple sessions. It returns recent sessions in descending start-time order with lifecycle timestamps, duration where known, and compact attendance. Request only the number needed; the live contract accepts 1–25 per page. Pass its opaque cursor unchanged when more history is actually required. Attendance user IDs describe recorded participation in that session, not current campaign membership or a character roster.

### `questportal_get_session`

Use it for one exact authorized session's lifecycle metadata, compact attendance, visible recording state, transcript capability state, and best available curated recap. An available story is authoritative curated material. An unavailable story is normal: it may be disabled, below the duration threshold, pending, or historically unlinked. Never associate a story or note by timestamp, and do not imply that `not_linked` means no recap was ever produced.

Recording `transcriptState` describes processing for that recording; session-level `transcriptAccess` describes whether the caller's capability is currently verified. `transcriptAccess: unavailable` is not proof that the account lacks an entitlement, so retry later rather than telling the user to subscribe or change access. This tool does not return transcript text.

### `questportal_get_session_timeline`

Use it only when event-level evidence is useful. It returns 1–100 normalized chronological events per page. Attendance, scenes, and dice are the default high-signal filters. Select `map` only when map activity matters. Select `speech` only when the user's request actually requires dialogue or transcript evidence; speech remains capability-gated and recording-visibility-gated.

Dice events come from the recorded campaign dice history within the authoritative session time window, not from transcript inference. Hidden rolls are returned only when the caller is the current campaign owner, roller, or character owner. Do not interpret an absent dice event as evidence about a roll the caller is not allowed to see.

Ask for the smallest filter set that answers the question. Do not seek raw event payloads, coordinates, odoo/Agora identifiers, transcript confidence, analytics fields, or storage details through another surface. Treat a timeline-derived synthesis as event-based, distinct from a curated session story. If a speech source changes between pages, the cursor returns `INVALID_CURSOR`; restart the same timeline request without a cursor instead of attempting to splice old and new pages.

All three session tools are read-only. Do not automatically create or update a recap note after reading them. A separate, explicit user request to save material must follow the normal note-write authorization, preservation, and verification workflow.

## Campaign scheduling

See [scheduling.md](scheduling.md) for complete schedule authoring, recurrence, occurrence, RSVP, revision, and manual calendar-import guidance.

### `questportal_get_campaign_schedule`

Use it before any schedule-dependent decision or write. It returns either `configured` with the complete current schedule and `updatedAt` revision, or `not_configured`. Owners and players can read it when campaign scheduling is enabled for their account. Do not infer whether scheduling is disabled, unavailable, or the campaign is inaccessible from a safe error.

### `questportal_list_campaign_schedule_occurrences`

Use it to resolve an upcoming occurrence before reading its roster, changing a response, or exporting it. It returns at most 400 chronological generated occurrences in the next year; these are not session-history records. An empty list can mean there is no configured schedule or no upcoming occurrence in that horizon.

### `questportal_get_campaign_schedule_occurrence_roster`

Use it only after obtaining an occurrence ID from the occurrence list. It returns current member responses and summary counts for that generated occurrence. Treat member IDs and responses as the current roster view, not as evidence of session attendance.

### `questportal_save_campaign_schedule`

Use it only for an authenticated campaign owner who requested a schedule change. Read immediately before writing, preserve the complete schedule, and pass the returned `updatedAt` as `expectedUpdatedAt`. A first schedule uses `expectedUpdatedAt: null`, `id` equal to `campaignId`, and `updatedAt: 0`. The write replaces the complete schedule; omitted rules, exceptions, settings, names, start dates, timezones, or durations are removed rather than preserved. On `CAMPAIGN_SCHEDULE_CONFLICT`, reread, reapply only the requested change, and retry with the new revision if the intent still applies. Verify with another schedule get and occurrence list.

### `questportal_set_campaign_schedule_occurrence_response`

List occurrences immediately before responding and pass one returned occurrence ID. The tool binds the change to the authenticated user; it cannot set another member's response. Use `yes`, `no`, or `null` to clear the response. Verify through the returned roster or a roster read.

### `questportal_get_campaign_schedule_occurrence_ics`

Use it for one occurrence returned by the occurrence list when the user wants a calendar file. The tool returns bounded ICS text and a suggested filename for manual import. It does not connect to or write an external calendar. It may reconcile internal generated-occurrence state, so do not describe it as a purely read-only operation even though it uses `campaigns:read`.

## Campaign mutations

### `questportal_create_campaign`

Use it only when creating a campaign is part of the requested outcome. Supply the intended name and description at creation. Its idempotency key must be stable across retries of that logical creation; the accepted format is 8–128 characters from letters, digits, `.`, `_`, `:`, and `-`. Reusing the key with changed creation content produces an idempotency conflict. Verify with `questportal_get_campaign` when the result is ambiguous or downstream work depends on the new ID. Do not use it as a precursor to a read-only planning request.

### `questportal_update_campaign`

Use it to change only the supplied name and/or description of an owned campaign. Read first when preserving an unspecified field or when the requested target/value is unclear. Repeating the same values is naturally idempotent, but there is no caller-provided idempotency key: after a timeout or ambiguous failure, get the campaign and compare current state before retrying. Verify meaningful changes with `questportal_get_campaign`. It cannot archive, delete, transfer, or change campaign membership.

### `questportal_update_campaign_profile_photo`

Use it to replace an owned campaign's profile image from bytes the user supplied or authorized. Send canonical base64 only, not a data URL or remote URL. Supported media are JPEG, PNG, and WebP; decoded content must be at most 5 MiB, each side at most 8192 pixels, and total area at most 40 megapixels. Keep the same idempotency key for the same campaign, field, and bytes; changed bytes with that key conflict. Follow with `questportal_get_campaign` to verify the new URL. Clearing/removing a photo and importing a remote URL are unsupported.

### `questportal_update_campaign_cover_photo`

Use it under the same byte, format, size, idempotency, and verification rules as the profile-photo tool. Replacing a cover also applies the tool's default cover position. If the user wants a different crop, call `questportal_update_campaign_cover_position` after the upload and verify both together. It cannot remove the cover or fetch a remote image.

### `questportal_update_campaign_cover_position`

Use it only to reposition a cover that already exists. Get the campaign first unless the current cover state is already known. The position contract accepts finite `x`/`y` values from -32768 through 32768 and a positive `width` through 32768; rely on the live schema for exact validation. It does not upload or remove a cover. Verify with `questportal_get_campaign`, especially after an ambiguous failure.

## Character reads and mutations

See [characters.md](characters.md) for the complete character, rich-text sheet, and legacy CoC7 contracts.

### `questportal_list_character_templates`

Use it when `questportal_create_character` will use `source=template` and the exact accessible template ID is not already known. It pages through published, enhanced, and authenticated-user-owned templates in stable ID order. Do not call it for `source=empty` or `source=coc7`.

### `questportal_create_character`

Use it to create one standalone player character or one NPC or claimable character in an owned campaign. Placement (`player`, `npc`, or `claimable`) and foundation (`empty`, `template`, or `coc7`) are independent inputs. Supply one stable idempotency key for the complete intended creation and reuse it only for exact retries.

### `questportal_list_characters`

Omit `campaignId` to list standalone characters owned by the authenticated account, or supply it to list campaign characters visible to that account. Pass `nextCursor` unchanged while `hasMore` is true. Use each result's permissions rather than inferring update access from visibility or role.

### `questportal_update_character`

Use it to change only the supplied name, tagline, or campaign visibility of an accessible character. Omit `campaignId` for standalone characters; standalone visibility cannot be changed. It cannot change ownership, placement, claimability, system, template, or lifecycle status.

### `questportal_update_character_portrait`

Use it to replace the portrait of a character whose listing reports `permissions.canUpdate=true`. Send canonical base64 JPEG, PNG, or WebP bytes and reuse one stable idempotency key for exact retries. It cannot import a remote URL or clear an existing portrait.

### `questportal_get_character_sheet`

Call it without `tabId` to get the visible-tab manifest, then with `tabId` to read one ordinary rich-text tab when its content matters. Ordinary tabs use `QuestPortalCharacterSheetTab/v1`; custom tabs are discoverable but their structured state is not returned. Use the dedicated CoC7 tool for legacy CoC7 structured state. Smart-sheet state remains unsupported.

### `questportal_update_character_sheet`

Read the ordinary tab first, minimally transform its complete content, and send the replacement with the returned revision. Handle `conflict`, `merged`, and `already_applied` like note updates and reread after a meaningful change. It cannot update custom-tab or smart-sheet structured state.

### `questportal_get_coc7_character_sheet`

Use it only for a character backed by the legacy enhanced CoC7 foundation. It returns bounded characteristics, skills, conditions, selected weapons, editable custom definitions, and a revision. Read ordinary narrative tabs separately with `questportal_get_character_sheet`.

### `questportal_list_coc7_weapons`

Use it to discover official weapon IDs accepted by the CoC7 update tool. Search by name or ID and pass `nextCursor` unchanged while `hasMore` is true. Character-specific custom weapon IDs come from the character's CoC7 sheet read.

### `questportal_update_coc7_character_sheet`

Read the structured sheet immediately before updating and patch only the requested sections by exact returned IDs and revision. The tool stores literal values rather than running a CoC rules engine, so calculate and include affected dependent numeric values when the requested change requires them. Preserve unsupported structured `scoreRoll` values and use [characters.md](characters.md) for custom-definition and rules-aware update guidance.

## Note reads and mutations

### `questportal_list_notes`

Use it to discover note IDs, titles, visibility, folder paths, and pending-candidate state within one accessible campaign. Filter by all, campaign, or private visibility and paginate through the result when needed. It does not return note bodies. Avoid fetching every body automatically; call `questportal_get_note` only for notes relevant to the requested outcome. Listing cannot move, share, archive, restore, or delete notes.

### `questportal_get_note`

Use it whenever note content matters. It returns the complete current `QuestPortalRichNote/v1` document and the revision required by `questportal_update_note`. It is the mandatory safe base for preserving existing content and resolving a conflict. Reread after meaningful updates, `merged`, `already_applied`, or an ambiguous response. See [note-content.md](note-content.md) for the content contract.

### `questportal_search_campaign_notes`

Use it for a focused natural-language question whose answer may be spread across the current contents of multiple notes in one campaign. It searches only when the campaign owner has internal-testing access, has enabled **Search note contents**, retains eligible Pro access, and the exact index generation is ready. Active players are always restricted to campaign-visible notes; only the campaign owner can search private visibility. Each result is a bounded excerpt with the current note title, visibility, folder path, score, and exact Quest Portal note URL. Treat `retrieval` counts as diagnostics rather than evidence, synthesize only supported claims, cite the exact returned URLs, and state when results are empty or insufficient. There is no adjacent-context tool for note hits; use `questportal_get_note` only when the user needs the complete accessible note and that broader read is proportionate. Do not work around `NOTE_CONTENT_SEARCH_DISABLED`, `NOTE_CONTENT_SEARCH_INDEXING`, `NOTE_CONTENT_SEARCH_REQUIRES_PRO`, or `NOTE_CONTENT_SEARCH_UNAVAILABLE` with bulk note reads, browser automation, or private APIs.

### `questportal_get_note_sidebar`

Use it to read the complete ordered hierarchy and revision for either the Campaign sidebar or the authenticated user's Private sidebar. It is the required immediate precursor to folder creation and item moves because those writes are revision-fenced. Read the same visibility you intend to modify. Do not use one sidebar's revision for the other or infer that an item can move across their visibility boundary.

### `questportal_create_note`

Use it to create one note at the campaign sidebar root with complete initial rich content. The first H1 supplies its sidebar title. Visibility defaults to private; choose campaign visibility only when the user's intent clearly includes sharing with campaign members. Prefer this single creation over a blank note followed by an update. Keep one stable idempotency key for retries; changed campaign, content, or visibility under the same logical key conflicts. Verify by getting the returned note when its content is meaningful to the task. The tool cannot choose a folder or later change visibility.

### `questportal_update_note`

Use it for a deliberate edit to an accessible note. First get the note, minimally transform the complete returned document, and send that complete replacement with its revision. The result means:

- `updated`: the requested document was current when checked; reread to verify the meaningful change.
- `already_applied`: the desired document was already present; treat as success, then reread if the final content matters.
- `conflict`: nothing from this request was applied because the revision was stale. Get the latest note, reapply only the user's intended change, and retry with the new revision.
- `merged`: concurrent content was preserved in a merged document. Get the note and inspect the result before any further update.

Do not retry a stale replacement unchanged against a new revision: that can overwrite intervening work. The tool cannot move, delete, restore, archive, or change visibility. See [note-content.md](note-content.md) for preservation rules.

### `questportal_create_note_folder`

Use it when the user requested a folder in a specific Campaign or Private sidebar. Read that sidebar immediately before writing, then supply its revision, the intended parent and placement, and a stable idempotency key. Reuse that key only for an identical logical folder request; use a new one after deliberately changing title, visibility, parent, or placement. On `conflict`, reread and reconsider the requested placement before retrying. The tool creates no note content and cannot bridge visibility boundaries.

### `questportal_move_note_sidebar_item`

Use it to reorder one active note, chapter, or folder or move it into or out of a folder within the same sidebar. Read the selected sidebar immediately before the move and pass its revision. On `conflict`, reread, re-resolve the item, destination, and relative placement, then retry only if that still matches the user's intent. The tool does not change note content or visibility and cannot move a folder into itself or one of its descendants. Verify meaningful organization by rereading the sidebar.

### `questportal_upload_note_image`

Use it only when an image is intended for an existing accessible note. Send canonical base64 JPEG, PNG, or WebP bytes under the same 5 MiB, 8192-pixel-side, and 40-megapixel limits as campaign media. The upload creates an immutable asset but does not edit the note. Keep one stable idempotency key for retries of identical bytes; changed bytes with the same key conflict.

Before upload, get the note, build the complete post-insertion document, and establish that it is safely writable. A successful read alone does not prove this because the read limit is larger than the mutation limit. If the note is large or writability cannot be established confidently, stop before creating the immutable asset and obtain user direction. After upload, get the latest note again, reapply the intended insertion using the returned asset URL as a `CustomImage`, update with that current revision, and get the note again to verify. Upload late: there is no public delete for an unused asset. Remote URL import is unsupported.

## Scene reads and organization

### `questportal_search_music`

Use it to discover tracks that may fit a scene or session from natural-language mood, setting, genre, title, description, creator, or tag terms. Results contain stable catalog track IDs, bounded descriptive metadata, attribution, and streaming-safety status. Treat `unverified` and `not-stream-safe` conservatively. For `monetization-approved`, rely only on the returned `approvedMonetization` values; other monetization forms remain disallowed. Preserve returned attribution when advising the user about streaming, but if `attributionTruncated` is true, do not publish the partial value as complete credit—direct the user to the terms URL or Quest Portal for the full attribution. Refine the query when results are empty or too broad. Search does not preview audio; use `questportal_attach_scene_catalog_music` with an exact returned ID for an authorized attachment.

### `questportal_get_scene`

Use it before updating an active non-folder scene. It returns the editable name, description, background image URL when valid, and a scene-content revision separate from the scene-bar and soundtrack revisions. A truncated legacy description is marked explicitly; updates remain patch-based, so omitted fields are preserved.

### `questportal_get_scene_soundtrack`

Use it to inspect one active scene's ordered audio tracks and obtain the soundtrack revision required by every soundtrack mutation. Each returned track has its asset `id` and a stable `associationId`; use the association ID for reordering so duplicate legacy asset IDs remain distinguishable, and use the asset ID for removal. Read immediately before attaching catalog music, completing an upload, reordering, or removing, and again afterward to verify the intended result. It is independent of scene content and scene-bar revisions and does not expose or change playback state. Unsupported legacy tracks without a safe public URL may be omitted from the returned list.

### `questportal_create_scene`

Use it to create a new root scene with its complete initial name, description, and required background image. Supply canonical base64 JPEG, PNG, or WebP bytes within the live schema limits; remote URLs are unsupported. Reuse one stable idempotency key for retries of the identical logical creation and image bytes. The new scene starts closed to players at the end of the root bar. Get the scene bar afterward before moving it into a folder or changing its order.

### `questportal_update_scene`

Get the scene immediately before updating and pass its revision. Supply only the name, description, or replacement background image fields the user requested; at least one is required. A replacement image follows the same byte and idempotency rules as creation. On `conflict`, get the scene again, reconsider the intended patch, and retry with the new revision only if it still applies. The tool preserves map, grid, fog, music, variants, placement, playing, and player-visibility state. Verify meaningful changes with another get.

### `questportal_prepare_scene_music_upload`

Use it only when the user supplied or authorized a local MP3 file to append to an owned campaign scene. Determine the exact byte length and declared content type, and compute `contentSha256` from the exact file bytes as an unpadded base64url SHA-256 digest. Use one stable idempotency key for that file, scene, name, size, and digest. For `prepared` or `already_prepared`, submit a multipart form `POST` to the returned `uploadUrl` with every returned `formFields` entry unchanged and the binary file in a final field named `file`. For `already_completed`, do not upload again; continue directly to completion with the returned `uploadId`. Do not put audio bytes in MCP JSON, omit signed fields, change the content type, or reuse the policy for another file. The form expires after 15 minutes, accepts exactly the declared byte length up to 100 MiB, and cannot be prepared once the scene has 100 soundtrack tracks. Preparing and uploading creates immutable storage state but does not yet change the scene.

### `questportal_complete_scene_music_upload`

Immediately before completion, call `questportal_get_scene_soundtrack` and use its revision—not the scene-content or scene-bar revision. Complete with the prepared `uploadId`; the tool verifies the stored size, type, ownership metadata, full-file SHA-256 digest, and bounded audio-container framing before appending it. On `conflict`, no soundtrack change was made: use the returned current soundtrack, confirm the append still makes sense, and retry the same upload ID with that revision. `already_applied` is success for a retry. Get the soundtrack afterward and verify the returned track ID, name, order, and URL. Completion appends newly uploaded audio; catalog attachment is a separate tool and neither operation previews tracks.

### `questportal_attach_scene_catalog_music`

Search first and pass one exact current selectable track ID. Read the destination soundtrack immediately before attaching and use its soundtrack revision. The server resolves the authoritative catalog asset rather than trusting caller-supplied metadata and appends it without changing playback or visibility. On `conflict`, reconsider the attachment against the returned current soundtrack before retrying with its revision. `already_attached` is success; do not add a duplicate. Verify with another soundtrack read.

### `questportal_reorder_scene_music`

Read the soundtrack immediately before reordering, then pass every returned `associationId` exactly once in the complete desired order with that revision. Do not use asset IDs here: duplicate legacy tracks can share one asset ID but have distinct association IDs. Do not omit an association to remove it or introduce one to attach it. On `conflict`, reconstruct the complete desired order from the returned current soundtrack before retrying. `already_applied` is success. The operation preserves legacy soundtrack map keys, track metadata, creator credits, playback, and visibility; legacy tracks omitted from the read because they lack a supported URL stay in their current slots.

### `questportal_remove_scene_music`

Read the soundtrack immediately before removing and pass the exact returned track ID with that revision. On `conflict`, confirm the track should still be removed before retrying against the current soundtrack. `already_removed` is success. The operation removes all soundtrack associations carrying that ID, matching the product editor's legacy duplicate behavior; it does not delete a global catalog asset or an uploaded Storage object, and it does not change playback or visibility.

### `questportal_get_scene_bar`

Use it to inspect an owned campaign's current root order and one-level folder contents. The returned revision fences all organization mutations. Read immediately before a change and again after meaningful writes because every successful organization change produces a new revision. This tool is owner-only and does not return map internals or edit scene content.

### `questportal_create_scene_folder`

Use it to create a top-level folder and place it at the start, end, before, or after another root item. Keep the same idempotency key for retries of the identical request. `already_applied` is success for that logical creation. If the requested name or placement changes, use a new key. A `conflict` means the bar changed after the supplied revision; reread and reapply the user's intended placement. Folders cannot be nested.

### `questportal_move_scene_bar_item`

Use it to reorder root items, reorder scenes within a folder, or move a scene into or out of a folder. Supply `parentFolderId: null` for the root. Placement references must be siblings in the destination after the move; do not use a source sibling as the destination reference unless it remains in that destination. Read first, use its revision, and verify afterward. The operation preserves scene content and player visibility. It cannot nest a folder or move an item between campaigns.

### `questportal_list_scene_gallery`

Use it to discover gallery scene IDs and bounded preview metadata. Results use stable scene-ID order rather than display-name order. Continue with `nextCursor` until the desired scene is found or `hasMore` is false; pass the cursor unchanged. Preview image metadata may be absent for legacy or invalid image values. This is a metadata read, not a campaign change, and it does not search names, descriptions, or tags.

### `questportal_add_gallery_scene_to_bar`

Use it after identifying a gallery scene and reading the destination scene bar. Choose the root or one existing folder plus a sibling placement. The gallery scene ID makes retries naturally idempotent: `already_added` means it is active somewhere in the bar, not necessarily at the requested placement. On `already_added`, reread and use `questportal_move_scene_bar_item` with the new revision if the user requested a different location. On `conflict`, reread before retrying. This tool does not create a new scene, edit gallery content, or duplicate an already-active scene.

## Codex OAuth reauthorization

When a Quest Portal tool returns `AUTHORIZATION_OUT_OF_SYNC` in a local Codex client, tell the user which scope the error says is missing and give them an actionable reauthorization sequence. Restarting Codex alone can reuse the existing OAuth grant, so it may not request newly required scopes.

First resolve the configured server name:

```bash
codex mcp list
```

Then use `codex mcp logout` and `codex mcp login` with the exact name returned.
Replace `ACTUAL_SERVER_NAME` in these templates before running them:

```bash
codex mcp logout "ACTUAL_SERVER_NAME"
codex mcp login "ACTUAL_SERVER_NAME"
```

The package's server key is `questportal`, but the host may give a plugin-managed
connection a different name. If it is not listed by the CLI, use the plugin's
connection controls in the host instead of adding a duplicate server.

Ask the user to approve the scope stated by the MCP error, then restart the MCP server or Codex client and retry the original tool call. The desktop app, CLI, and IDE extension share MCP configuration; the desktop app also exposes server status and `Authenticate` under **Settings > MCP servers**. Do not invent OAuth scope identifiers or tell the user to edit stored credentials manually. Do not run logout or attempt the interactive authorization on the user's behalf unless they explicitly request that action; browser consent remains a user step.

## Recovery and retry decisions

| Signal                                                | Correct response                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RATE_LIMITED`                                        | Wait until the structured `retryAfterSeconds` or `retryAt`, then repeat the original request. Preserve any idempotency key.                                                                                                                                                                                                                              |
| `AUTHORIZATION_OUT_OF_SYNC`                           | Stop blind retries, state the missing scope, and follow [Codex OAuth reauthorization](#codex-oauth-reauthorization) for Codex clients. Otherwise ask the user to reconnect or reauthorize through their client's connection controls. Retry only after authorization changes.                                                                            |
| `CAMPAIGN_NOT_FOUND_OR_INACCESSIBLE`                  | Verify the campaign ID and accessible campaign list without guessing whether it is absent or forbidden.                                                                                                                                                                                                                                                  |
| `CAMPAIGN_SCHEDULING_NOT_ENABLED`                     | Explain that campaign scheduling is not enabled for the authenticated account. Do not try a private API or browser automation fallback.                                                                                                                                                                                                                  |
| `CAMPAIGN_SCHEDULE_NOT_FOUND_OR_INACCESSIBLE`         | Reread the schedule or occurrence list and verify the campaign and occurrence IDs without guessing whether the campaign, schedule, occurrence, role, or capability caused the safe failure.                                                                                                                                                              |
| `CAMPAIGN_SCHEDULE_CONFLICT`                          | Reread the complete schedule, reapply only the requested change, and retry with the latest `updatedAt` only if the intent still applies.                                                                                                                                                                                                                 |
| `LIBRARY_SOURCE_NOT_FOUND_OR_INACCESSIBLE`            | List campaign-library sources again and retry only with a returned source ID. Do not guess whether the requested source is missing, hidden, player-restricted, unsupported, or unentitled.                                                                                                                                                               |
| `INVALID_CONTEXT_TOKEN`                               | Search again and pass one new result's sourceId and contextToken unchanged; do not construct a token or substitute adjacent chunk coordinates.                                                                                                                                                                                                           |
| `LIBRARY_SOURCE_VERSION_CHANGED`                      | Search the same source again and use only one new result's sourceId and contextToken before requesting context.                                                                                                                                                                                                                                          |
| `LIBRARY_CONTEXT_NOT_FOUND`                           | Search again because the prior result token no longer identifies a current chunk; do not guess replacement coordinates.                                                                                                                                                                                                                                  |
| `SESSION_NOT_FOUND_OR_INACCESSIBLE`                   | Verify the campaign/session IDs without guessing whether the session is absent, belongs to another campaign, or is forbidden.                                                                                                                                                                                                                            |
| `CHARACTER_CREATION_TARGET_NOT_FOUND_OR_INACCESSIBLE` | Verify the campaign role or choose a template returned by character-template discovery; do not infer hidden campaign or template state.                                                                                                                                                                                                                  |
| `CHARACTER_CREATION_IN_PROGRESS`                      | Wait briefly, then retry the exact creation with the same idempotency key.                                                                                                                                                                                                                                                                               |
| `NOTE_NOT_FOUND_OR_INACCESSIBLE`                      | Verify the campaign/note IDs and accessible note list without exposing or inferring hidden state.                                                                                                                                                                                                                                                        |
| `NOTE_CONTENT_SEARCH_DISABLED`                        | Explain that the campaign owner must enable **Search note contents** in campaign settings. Do not bulk-read notes as a fallback.                                                                                                                                                                                                                         |
| `NOTE_CONTENT_SEARCH_INDEXING`                        | Retry later; do not fall back to reading every note while the current index is being prepared.                                                                                                                                                                                                                                                           |
| `NOTE_CONTENT_SEARCH_REQUIRES_PRO`                    | Explain that the campaign owner's eligible active Pro access is required; do not infer anything about the caller's own plan or assume shared-Pro eligibility.                                                                                                                                                                                            |
| `NOTE_CONTENT_SEARCH_UNAVAILABLE`                     | State that note-content search is not currently available for that campaign. Do not guess why and do not bypass the server gate.                                                                                                                                                                                                                         |
| `NOTE_CONTENT_SEARCH_RATE_LIMITED`                    | Retry later without changing the query solely to evade the provider limit.                                                                                                                                                                                                                                                                               |
| `TRANSCRIPT_ACCESS_UNAVAILABLE`                       | Keep speech fail-closed. Retry later or continue without speech; do not claim the user lacks an entitlement or attempt a private transcript path.                                                                                                                                                                                                        |
| `INVALID_CURSOR`                                      | Restart the affected list or timeline without a cursor. For speech, the source may have been regenerated between pages.                                                                                                                                                                                                                                  |
| Documentation page/version error                      | Search for the current page on not-found; restart the page without continuation values when its prior version is unavailable.                                                                                                                                                                                                                            |
| Idempotency-conflict response                         | This family includes note `IDEMPOTENCY_CONFLICT`, character and campaign-media `IDEMPOTENCY_KEY_CONFLICT`, and campaign creation's unprefixed “idempotency key was already used” conflict. Do not invent a new key to force the request. Compare the intended logical action and payload; use a new key only for an intentionally new or changed action. |
| Timeout or generic error after a mutation             | Read current state before retrying. If a creation/upload must be retried, use the original stable key.                                                                                                                                                                                                                                                   |
| Note `conflict` or `merged`                           | Reread the complete note; rebase on `conflict`, inspect on `merged`, and verify after the next write.                                                                                                                                                                                                                                                    |
| Sidebar `conflict`                                    | Reread the same visibility's sidebar and re-resolve the intended parent and placement before retrying.                                                                                                                                                                                                                                                   |
| Scene-bar `conflict`                                  | Reread the scene bar, re-resolve the destination folder and sibling placement, then retry with the new revision only if it still matches the user's intent.                                                                                                                                                                                              |
| Scene-content `conflict`                              | Reread the individual scene, reapply only the requested name, description, or image patch, and retry with its new scene revision if the intent still holds.                                                                                                                                                                                              |
| Scene-soundtrack `conflict`                           | Use the returned current soundtrack or call `questportal_get_scene_soundtrack` again, reconstruct only the still-intended attachment, order, or removal, and retry with the current soundtrack revision. Preserve the same upload ID when completing uploaded audio.                                                                                     |
| `MUSIC_CATALOG_TRACK_NOT_FOUND_OR_UNAVAILABLE`        | Search the current catalog again. Use only an exact selectable audio track ID returned by `questportal_search_music`; do not substitute cached metadata or a hidden historical track.                                                                                                                                                                    |
| `MUSIC_UPLOAD_NOT_COMPLETE`                           | Upload the file with the exact returned multipart form URL and fields, then retry completion. Do not prepare a second upload unless the first preparation expired or the intended file changed.                                                                                                                                                          |
| `MUSIC_UPLOAD_EXPIRED`                                | No stored object was available before the signed form expired. Prepare again with a new idempotency key because the prior form is no longer valid. An object uploaded before expiry can still complete afterward, including after a soundtrack-conflict retry.                                                                                           |

Mutation rate limits count attempts as well as logical requests, so fast retries can continue to fail even when an idempotency key is reused. Follow the returned retry timing rather than using a hardcoded delay.
