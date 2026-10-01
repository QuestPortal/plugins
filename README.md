# Quest Portal plugins

Plugin marketplace catalog for Quest Portal.

## Import into ChatGPT

In Workspace settings > Plugins > Add > Import marketplace, enter:

- Source: `https://github.com/QuestPortal/plugins`
- Path: leave empty
- Branch, tag, or commit: `main` (or leave empty)

The catalog is at `.agents/plugins/marketplace.json`.

## Call of Cthulhu

The catalog references `apps/call-of-cthulhu-plugin` on the
`gunni/call-of-cthulhu-plugin` branch of `QuestPortal/questportal`.
That repository is private: the GitHub account importing the marketplace must
have access to it. This public catalog does not make the plugin source public.
Update the catalog ref when the plugin moves to its release branch, before
removing the current branch.

The plugin currently declares a remote MCP server. ChatGPT workspace imports
of plugins declaring MCP servers are currently marked Desktop only.

This catalog does not migrate an existing uploaded plugin or change workspace
installation policies. To migrate an existing plugin, add its workspace plugin
ID as `pluginId` beside the matching entry's `name` and `source` before import.

See [OpenAI's marketplace import documentation](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).
