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

Version 0.3.0 adds guest MCP Events and inline roll result widgets to the existing
guest MCP connection. Refresh the marketplace and update the installed plugin to
load the new session and event instructions. MCP Events and inline rendering also
require host support. The package includes portable
`plugin.json`/`mcp.json` and matching Codex compatibility files. ChatGPT installation,
embedding and attachment still need host verification; endpoint deployment alone
does not prove those flows. The prior Site and its records are not migrated.

## Updates

Publish updated distribution files under `plugins/call-of-cthulhu-plugin/` and
update the plugin manifest version when releasing changes. This repository holds
the authoritative source for the catalog, plugin manifest, skills, plugin icon,
and MCP connection. Edit those files here. The private application
repository owns the UI, backend, database, tests, and deployment, and consumes
a pinned public icon during its builds.
Marketplace sync reads updates from this repository's `main` branch.

This catalog does not migrate an existing uploaded plugin or change workspace
installation policies. To migrate an existing plugin, add its workspace plugin
ID as `pluginId` beside the matching entry's `name` and `source` before import.

See [OpenAI's marketplace import documentation](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).
