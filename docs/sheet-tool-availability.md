# Sheet tool availability in Codex

D&D 0.2.2 and Call of Cthulhu 0.4.5 change the marketplace packaging to use
Codex's supported native manifest layout. The marketplace keeps the same plugin
identities, MCP server names, endpoints, skills and presentation metadata.

## Cause

Codex 0.162.0 applies an 8,000-byte per-tool and 64,000-byte aggregate model-tool
specification budget to portable Agent Plugins. Tools that do not fit are hidden
from the model even when their MCP server has connected and the interactive sheet
has loaded. This can leave character creation unavailable in chat.

The presence of root `plugin.json` selects the portable format despite the
additional `.codex-plugin/plugin.json` file. The identical tool names on the two
servers are namespaced; they are not a collision. The sheet and roll-card UI
metadata is retained.

References:

- [Supported native plugin layout](https://developers.openai.com/plugins/build/plugins)
- [Codex tool exposure budget](https://github.com/openai/codex/blob/8c0f7011674145da7e10627769fb221c74fbf7a0/codex-rs/core/src/mcp_tool_exposure.rs)
- [Installed plugin attribution](https://github.com/openai/codex/blob/8c0f7011674145da7e10627769fb221c74fbf7a0/codex-rs/core/src/config/mod.rs)

## Distribution

The OpenAI marketplace selects generated `codex-plugins/` bundles containing the
native manifest, `.mcp.json`, skills, artwork and notices. They omit the portable
root manifest. Canonical portable and Claude sources remain in `plugins/`.
CI checks exact file and byte parity so the generated copies cannot silently drift.

New marketplace installs receive the native bundles. Existing installations need
the marketplace refreshed and the plugin updated to these versions. No manual
`mcp_servers` configuration is needed. An independently uploaded older package
must also be updated; this release cannot change another workspace's cached copy.

This release does not change the hosted application or require a Cloudflare deploy.
Rollback is a revert of the marketplace release; that restores the earlier
portable-package behavior and its Codex budget limitation.

## Verification

On 2026-10-11, the installed macOS Codex 0.162.0 binary was tested through its
normal `plugin/install` path with temporary, uniquely named local packages.
Both variants used identical localhost copies of the public D&D/Cthulhu tool
catalogs and server instructions. The native variant omitted the portable root
manifest. Existing manual MCP registrations were disabled only for the diagnostic
subprocess, and separate diagnostic server keys prevented precedence from masking
the result.

| Normal installed format | Sheet tools visible to model | Synthetic budget probes |
| --- | ---: | ---: |
| Portable | 2 of 21 (Cthulhu session tools only) | 0 of 70 |
| Native | 21 of 21 | 70 of 70 |

The local Responses stub requested only a runtime tool inventory. No character,
dice, session, or production write tool was called. The temporary packages were
uninstalled after comparison. The selected-capability-root admission path was
also examined but did not reproduce installed-plugin filtering; it was not used
as release evidence.

Offline regression checks: 17 marketplace tests, 6 Pendragon tests, 11 Battlemap
tests and 9 domain-verification worker tests passed. Seven archives (five portable,
two native) were built and checked against source. Native bundle drift checks and
`git diff --check` passed. These checks cover installation format, catalog routing,
manifest parity and archive integrity; no application runtime code changed.

Credentials: none for the localhost inventory comparison. Synthetic data: temporary
plugin packages only, removed after testing. Production application state changed:
none. Full interactive character creation, embedding, Attach, Events delivery,
other Codex versions, mobile and other hosts were not retested by this packaging
release. Marketplace cache refresh timing is controlled by the host.
