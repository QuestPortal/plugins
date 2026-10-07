# Quest Portal plugins

Plugin distribution source for Quest Portal. The catalog includes the authenticated
Quest Portal MCP connection, guest character sheets and an owner-only Battlemap
pilot; package availability does not establish host acceptance. See
[release status and remaining gates](docs/release-status.md).

## Import into ChatGPT

In Workspace settings > Plugins > Add > Import marketplace, enter:

- Source: `https://github.com/QuestPortal/plugins`
- Path: leave empty
- Branch, tag, or commit: `main` (or leave empty)

The catalog is at `.agents/plugins/marketplace.json`. Plugin packages are in
`plugins/`, so importing does not require access to any private repository.

## Quest Portal MCP

Connect your Quest Portal account through OAuth at
`https://mcp.questportal.com/mcp`. The [Quest Portal package](plugins/questportal-plugin/README.md)
includes portable and Codex manifests, connection configuration, the Quest Portal
icon, and a structured usage skill covering campaigns, notes, characters, session
history, library search, scenes, music and scheduling.

Personal Pro or eligible campaign-scoped shared Pro access is required; scopes,
roles and feature gates still apply. Scheduling requires preview access, and
note-content search has additional owner-controlled eligibility checks. This
package connects to the account-based service and includes no embedded guest
sheet. See the [MCP research and status record](docs/questportal-mcp-status.md)
for deployment evidence, supported boundaries and unverified host behavior.

## Call of Cthulhu

Create, edit and roll Call of Cthulhu 7th edition investigator sheets as a guest.
The application runs on Quest Portal's Cloudflare account at
[cthulhu.questportal.com](https://cthulhu.questportal.com), with its public MCP
endpoint at `https://cthulhu.questportal.com/mcp`. No account or local server is
required. Drafts stay in the browser where the host permits, JSON import/export
provides portable backups, and roll results can display inline in chat. Optional
private guest play sessions let an explicitly subscribed chat receive dice events.
Sessions expire after 24 hours and retain up to 1,000 rolls; ending a session
removes its rolls and subscriptions. Unconnected rolls stay in the current view.
There is no server-side investigator library. Quest Portal accounts and cloud
saving are deferred to v2.

Runtime version 0.4.0 adds populated single and batch creation plus revisions of explicitly
attached sheets. Creation uses request IDs to avoid duplicates, reports per-character
validation failures, and distinguishes prepared payloads from the sheet confirming
loading and local saving. Assigned builds are custom, not verified rules-legal.
Refresh the marketplace and update the installed plugin to load the new instructions
and tools. Existing dice and guest play sessions remain available. MCP Events,
inline rendering, embedding and attachment depend on host support; endpoint deployment
alone does not prove those flows. The package includes portable `plugin.json`/`mcp.json`
and matching Codex compatibility files. The prior Site and its records are not migrated.

Package 0.4.1 restores the existing listing/support/legal URLs and
review cases from the separately prepared 0.3 submission without reverting the
0.4 workflows. The older walkthrough does not demonstrate batch/revision or
native-host acceptance. See [metadata reconciliation](docs/cthulhu/reconciliation.md).

## Pendragon

Open, populate, revise and roll Pendragon 6th edition knight sheets as a guest.
The coordinated candidate adds populated single/batch creation and exact
attached-snapshot revisions, while preserving manual editing. The package
is configured for [pendragon.questportal.com](https://pendragon.questportal.com)
and its public MCP endpoint at `https://pendragon.questportal.com/mcp`, using the
same guest workflow and visual conventions as the Call of Cthulhu companion.
The sheet covers attributes, opposed Traits, Passions, skills, combat, mounts,
equipment, family, Glory and Winter Phase notes. Drafts remain in the browser
where supported; JSON import/export provides portable backups, and Attach
explicitly shares current values with ChatGPT. No account, cloud character
library or device sync is required or provided.

Version 0.1.0 includes inline roll cards and optional private guest play sessions.
Sessions expire after 24 hours and retain up to 1,000 rolls; ending a session
removes its rolls and subscriptions. Event monitoring requires an explicit
subscription and a supporting host. Character creation choices, inspiration
consequences and campaign decisions remain with the table. This is a companion
sheet, not a rulebook or an official Chaosium endorsement.

The 0.1.0 backend was deployed on 2026-10-01; its matching package lives under
`plugins/pendragon-plugin/`. The local application passed 197 automated tests,
17 Chromium E2E tests, and 3 runner safety checks, including explicit Attach and
launch replay in a local MCP Apps host harness. Actual ChatGPT installation,
native embedding, and live event delivery still require host verification.

Package version 0.1.1 preserved the existing identity, MCP endpoint, prompts, and
audience while clarifying attachment snapshots, damage inputs, tool errors, and
session recovery. It added an offline package validator and reproducible portable
ZIP builder; see [Pendragon packaging](scripts/pendragon/README.md). This package
update does not itself change the backend or prove native host installation.

Version 0.1.2 aligns with the original runtime improvements: opposed checks
return both dice and partial/tie outcomes; statistic-aware characteristic checks
show success/failure; horse and critical damage use explicit bounded inputs.
The endpoint and tools retain their identities. The matching runtime is deployed
and verified live; native-host and Events acceptance remain unverified. See
[release evidence](docs/release-status.md).

## Battlemap

Build and run persistent tactical encounters with maps, tokens, walls, doors,
fog, initiative and bounded ChatGPT control. Install **Battlemap by Quest Portal**
from this marketplace, then connect it through the host’s OAuth flow. The app is
hosted at [map.questportal.com](https://map.questportal.com), with its MCP endpoint
at `https://map.questportal.com/mcp`.

Version 0.1.3 is an **owner-only pilot**. Access requires the separate Battlemap
owner sign-in and OAuth consent. Marketplace installation does not grant access
to the owner’s encounters; obtain access from the owner before connecting. Do not
paste access phrases or credentials into a conversation.

Version 0.1.3 moves the app and MCP connection to `map.questportal.com`. Refresh
the marketplace and update the plugin, then reconnect through the host’s OAuth
flow. Sign in again when opening the new domain in your browser: browser sessions
and OAuth connections from the previous Worker origin do not transfer. The
existing encounter library stays in the same Cloudflare storage.

The release includes safe creation retries, visual proposal review, explicit fog
reveal confirmation, reconnect recovery and host-mediated `.battlemap` downloads.
Player preview filters the displayed map; it cannot erase GM information already
shared with a conversation. Control grants and future-event subscriptions require
separate approval. Actual host OAuth linking, embedded downloads and live Events
acceptance remain unverified; see [release evidence](docs/battlemap-release.md).

The authoritative package is `plugins/quest-portal-battlemap/`, with portable and
Codex manifests, the MCP connection, three skills and its icon. Validate it and
build reproducible ZIPs using the [offline packaging tool](scripts/battlemap/README.md).
The private application repository owns the runtime, Cloudflare configuration,
storage and deployment. This catalog entry preserves the package name and does
not use a personal plugin ID to claim a workspace migration.

## Dungeons & Dragons

Open, populate, revise and roll D&D 5.5e character sheets for the 2024 revised fifth
edition. The coordinated candidate adds populated single/batch creation and exact
attached-snapshot revisions; class choices still need table-approved values.
The package is configured for [dnd.questportal.com](https://dnd.questportal.com)
and its public MCP endpoint at `https://dnd.questportal.com/mcp`, following the
Call of Cthulhu companion’s guest workflow and interface conventions. Abilities,
skills, combat, spells, features, inventory and character notes use the shared
Quest Portal D&D components.

The original 0.1.0 release adds 339 SRD spell and 38 weapon pickers,
per-class casting, class-owned Hit Dice, and explicit slot/maximum-HP suggestions.
Death-save rolls use DC 10; initiative has no success verdict. The matching
runtime is deployed and verified live; see [release evidence](docs/release-status.md).

Version 0.1.0 includes browser drafts, validated JSON import/export, explicit
Attach-to-chat, d20 and damage dice, inline roll cards and optional private guest
play sessions. No account, cloud character library or device sync is required or
provided. Rules are based on the openly licensed SRD 5.2.1. This is a character
sheet with editable progression choices, not an automatic validator for every
class feature or a substitute for the rulebooks.

Distribution source lives in `plugins/dnd-plugin/`. The private application
repository owns its UI, backend, build and tests. Deployment, marketplace release,
ChatGPT installation, native embedding, Attach and live event delivery are separate
verification steps; package source alone does not establish those host workflows.

## Validate and package

Run the [shared offline validator and archive builder](scripts/marketplace/README.md)
for all catalog packages. It checks source/manifest parity and archive contents;
it does not call production endpoints or establish host acceptance. Alternate
D&D2 and Pendragon2 branches remain available for reference and are not cataloged.

## System guides and current UI

The package instructions now separate tabletop guidance from implemented tools:

| System | Current package | Skill and linked references | Chat creation/edit boundary |
| --- | --- | --- | --- |
| D&D 2024 / SRD 5.2.1 | 0.2.1 candidate | [Character sheet](plugins/dnd-plugin/skills/character-sheet/SKILL.md) | Populated single/batch creation (1–20), exact attached-sheet revisions |
| Call of Cthulhu 7e | 0.4.4 candidate | [Investigator sheet](plugins/call-of-cthulhu-plugin/skills/investigator-sheet/SKILL.md) | Same capabilities through common names and retained investigator aliases |
| Pendragon 6e | 0.2.1 candidate | [Knight sheet](plugins/pendragon-plugin/skills/knight-sheet/SKILL.md) | Populated single/batch creation (1–20), exact attached-sheet revisions |

Each skill links system overview, character creation, core rules, supported
workflows, examples and authoritative sources. D&D includes 339 SRD spells and
38 weapons, class-specific casting, class-owned Hit Dice and explicit rest/resource
controls; it is not a complete build validator. All three use the footer's **Sheet
tools** entry for auxiliary actions such as Attach, JSON backup and Settings.
D&D/CoC have responsive layouts, roll/edit switching and light/dark preferences;
Pendragon is dark-only. Rolls do not automatically spend resources or apply damage.

The candidate standardizes `create_character`, `create_characters` and
`revise_character`, shared delivery/retry semantics and explicit snapshot Attach.
Existing system tool names remain supported. See the
[parity contract](docs/sheet-contract-parity.md) for the before/after matrix and
system-specific merge rules. **These package candidates depend on the coordinated
runtime change; they are not deployed or published by this source PR.** Release
the matching runtime before publishing these package claims. Current connections
must be checked for advertised capabilities. See [release evidence](docs/release-status.md)
for historical live checks and still-unrun native acceptance. Package versions
differ from runtime versions; historical release records above remain for context.

## Updates

Publish updated distribution files under the matching directory in `plugins/`
and update the plugin manifest version when releasing changes. This repository holds
the authoritative source for the catalog, plugin manifest, skills, plugin icon,
and MCP connection. Edit those files here. The private application
repository owns the UI, backend, database, tests, and deployment, and consumes
a pinned public icon during its builds.
Marketplace sync reads updates from this repository's `main` branch.

This catalog does not migrate an existing uploaded plugin or change workspace
installation policies. To migrate an existing plugin, add its workspace plugin
ID as `pluginId` beside the matching entry's `name` and `source` before import.

See [OpenAI's marketplace import documentation](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).
