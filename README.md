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
provides portable backups, and dice history lasts only for the current view.
There is no persistent server library or roll history. Quest Portal connection
and cloud saving are deferred to v2.

Version 0.2.0 replaces the Sites-managed app dependency with a guest MCP connection.
Refresh the marketplace and update the installed plugin. Existing installations
may need to reconnect after this endpoint change. The package includes portable
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
