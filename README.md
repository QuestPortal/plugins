# Quest Portal plugins

Public plugin marketplace for Quest Portal.

## Import into ChatGPT

In Workspace settings > Plugins > Add > Import marketplace, enter:

- Source: `https://github.com/QuestPortal/plugins`
- Path: leave empty
- Branch, tag, or commit: `main` (or leave empty)

The catalog is at `.agents/plugins/marketplace.json`. Plugin packages are in
`plugins/`, so importing does not require access to any private repository.

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

Version 0.4.0 adds populated single and batch creation plus revisions of explicitly
attached sheets. Creation uses request IDs to avoid duplicates, reports per-character
validation failures, and distinguishes prepared payloads from the sheet confirming
loading and local saving. Assigned builds are custom, not verified rules-legal.
Refresh the marketplace and update the installed plugin to load the new instructions
and tools. Existing dice and guest play sessions remain available. MCP Events,
inline rendering, embedding and attachment depend on host support; endpoint deployment
alone does not prove those flows. The package includes portable `plugin.json`/`mcp.json`
and matching Codex compatibility files. The prior Site and its records are not migrated.

## Pendragon

Create, edit and roll Pendragon 6th edition knight sheets as a guest. The package
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

Package version 0.1.1 preserves the existing identity, MCP endpoint, prompts, and
audience while clarifying attachment snapshots, damage inputs, tool errors, and
session recovery. It adds an offline package validator and reproducible portable
ZIP builder; see [Pendragon packaging](scripts/pendragon/README.md). This package
update does not itself change the backend or prove native host installation.

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
