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
The native plugin package includes its manifest, skill, icon, and remote MCP
configuration. The application and backend run on the hosted service; no local
server build is needed. Installation requires access to that hosted service.

ChatGPT workspace imports of plugins declaring MCP servers are currently marked
Desktop only, including this plugin. Publishing this repository does not verify
installation or hosted-service availability.

## Updates

Publish updated distribution files under `plugins/call-of-cthulhu-plugin/` and
update the plugin manifest version when releasing changes. This repository holds
a distribution snapshot; it does not automatically copy development changes.
Marketplace sync reads updates from this repository's `main` branch.

This catalog does not migrate an existing uploaded plugin or change workspace
installation policies. To migrate an existing plugin, add its workspace plugin
ID as `pluginId` beside the matching entry's `name` and `source` before import.

See [OpenAI's marketplace import documentation](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).
