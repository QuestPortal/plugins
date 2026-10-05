# Connection and access

## Connect the plugin

The plugin's MCP configuration connects to `https://mcp.questportal.com/mcp` using Streamable HTTP. Authentication uses Quest Portal's OAuth issuer at `https://auth.questportal.com` and a browser authorization flow with PKCE. Sign in to the intended Quest Portal account and approve the requested access through the client. Do not ask the user to paste tokens, passwords, or cookies into chat, and do not put secrets in the plugin configuration.

Use the client's plugin or MCP connection controls to authenticate. In Codex, inspect **Settings > MCP servers** and use **Authenticate** for the Quest Portal connection. If using CLI recovery, first discover the actual configured server name with `codex mcp list`; plugin-managed names may differ from manually configured names. In ChatGPT, use the plugin connection's authorization or reconnect control. Do not configure a second server or install another copy of this skill merely to use the plugin.

After authentication:

1. Discover the currently registered `questportal_*` tools. Their schemas are authoritative for names, input fields, limits, and results; this packaged guide does not establish what is deployed or enabled for the account.
2. Use `questportal_ping` when connection health is uncertain. A successful ping proves connectivity and returns a revision receipt; it does not prove identity, domain access, or eligibility for a write.
3. Make the narrowest read that serves the user's request. Prefer an exact supplied campaign ID to listing unrelated campaigns. When the target is unclear, use campaign discovery and the returned owner/player role to resolve it.
4. Read the relevant domain reference before a complex write, preserve its revision and retry rules, and verify the result with the corresponding read.

## Account eligibility and permissions

Personal Quest Portal Pro access supports the full public MCP surface, subject to the OAuth scopes granted, the user's role, resource visibility, and feature gates. Enrolled shared-Pro recipients can use explicitly supported operations only within an eligible exact campaign when the server's rollout prerequisites are satisfied. Do not assume shared-Pro access is available to an account or grants access to every operation. Creating a campaign or a standalone character requires personal Pro access.

Scopes grant permission to request a class of operation; they do not override ownership, membership, or visibility. Campaign data is limited to active campaigns the authenticated user can access. Owner-only operations still require the owner. Campaign-visible notes are available to authorized members; private notes stay within their owner's permitted scope. Include private note content only when the authenticated owner explicitly requests it. Do not infer hidden resources from a safe not-found-or-inaccessible response.

Scheduling additionally requires the account's `canScheduleSessions` preview gate. Campaign-note content search requires the campaign owner's internal-testing access, **Search note contents** setting, eligible Pro access, and a ready index. These features must not be presented as universally available merely because their tools are registered.

For the exact scope mapping, role rules, and tool selection, read [Shared rules](tools.md#shared-rules). For note-search evidence and visibility, read [Blueprints](blueprints.md); for scheduling constraints, read [Scheduling](scheduling.md).

## Recover without bypassing access controls

| Situation                                                     | Next step                                                                                                                                                                                                                               |
| ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Client shows disconnected or unauthenticated                  | Reconnect through the client's connection controls and complete browser sign-in and consent for the intended account. Then retry the relevant read.                                                                                     |
| `AUTHORIZATION_OUT_OF_SYNC` names a missing scope             | Stop retries, state that exact scope, and have the user reauthorize. For Codex, follow [Codex OAuth reauthorization](tools.md#codex-oauth-reauthorization), using the discovered server name. Restarting alone may reuse the old grant. |
| A campaign or resource is not found or inaccessible           | Check the supplied ID or use permitted discovery. Do not guess whether the resource is missing, hidden, or forbidden.                                                                                                                   |
| A Pro, preview, note-search, or visibility gate denies access | Explain the specific returned condition without inferring a subscription state. Continue only with an independently useful supported operation the user requested.                                                                      |
| A request is rate limited, conflicts, or times out            | Follow [Recovery and retry decisions](tools.md#recovery-and-retry-decisions). Preserve retry identity, use current revisions, and read current state before repeating an ambiguous write.                                               |

Reauthorization requires browser consent by the user. Do not revoke grants or run logout on the user's behalf unless they explicitly request that action. Never bypass an authorization, entitlement, visibility, or feature gate with private APIs, browser scraping, copied credentials, or bulk reads.
