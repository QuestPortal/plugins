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

Create, edit, save, and roll Call of Cthulhu 7th edition investigator sheets.
The native plugin package includes its manifest, skill, icon, and a required
reference to the existing Sites-managed Call of Cthulhu app. The application and
backend run on the hosted service; no local server build is needed.

Authentication is managed through the existing app connection, not a separately
configured MCP server. The app must be available to the importing account or
workspace, and users must connect it. A public repository does not grant app access.

Version 0.1.1 replaces the direct MCP declaration with `.app.json`. Refresh the
marketplace and update the installed plugin to receive this change. Host support
and successful tool invocation still need verification; repository publication
alone is not evidence that installation or authentication succeeds.

## Updates

Publish updated distribution files under `plugins/call-of-cthulhu-plugin/` and
update the plugin manifest version when releasing changes. This repository holds
the authoritative source for the catalog, plugin manifest, skills, plugin icon,
and Sites app reference. Edit those files here. The private application
repository owns the UI, backend, database, tests, and deployment, and consumes
a pinned public icon during its builds.
Marketplace sync reads updates from this repository's `main` branch.

This catalog does not migrate an existing uploaded plugin or change workspace
installation policies. To migrate an existing plugin, add its workspace plugin
ID as `pluginId` beside the matching entry's `name` and `source` before import.

See [OpenAI's marketplace import documentation](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).
