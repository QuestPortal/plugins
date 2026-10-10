# Quest Portal

Connect ChatGPT, Codex or Claude to your Quest Portal account through the hosted
public MCP server. Prepare campaigns, work with notes and character sheets, organize
scenes and music, and read accessible session history and library sources.

## Connect

Install **Quest Portal** from the Quest Portal plugin marketplace, then use the
host's connection or authentication control to sign in to Quest Portal and
approve the access you need. The plugin includes its usage skill; a separate
skill download or local server is unnecessary.

In Claude Code, run:

```
/plugin install questportal-plugin --marketplace QuestPortal/plugins
```

then authenticate with `/mcp` when prompted. In claude.ai or Claude Desktop, add
`https://github.com/QuestPortal/plugins` as a marketplace under Customize >
Plugins, install `questportal-plugin`, and complete the OAuth prompt.

| Setting        | Value                                                                |
| -------------- | -------------------------------------------------------------------- |
| Package        | `questportal-plugin` · `0.1.1`                                       |
| MCP server key | `questportal`                                                        |
| Endpoint       | `https://mcp.questportal.com/mcp`                                    |
| Transport      | Streamable HTTP (`streamable-http` portable; `http` in Codex/Claude) |
| Authentication | Browser OAuth through `https://auth.questportal.com`                 |
| Usage skill    | [using-questportal-mcp](skills/using-questportal-mcp/SKILL.md)       |

The host manages OAuth discovery, consent and tokens. The package contains no
API key, client secret, account ID or credential headers. Installing a package
does not connect an account or grant access to a campaign.

## Access and capabilities

Personal Pro access supports the full MCP surface, subject to consented scopes,
campaign membership and resource permissions. Eligible users enrolled in shared
Pro can access supported operations within qualifying campaigns; availability
depends on rollout and current campaign access. Campaign creation and standalone
character work require personal Pro. The server's actual access decision is
authoritative. See [connection and access](skills/using-questportal-mcp/references/connection-and-access.md).

The source snapshot used for this package registers 59 tools:

| Workflow         | Supported work                                                                                                  |
| ---------------- | --------------------------------------------------------------------------------------------------------------- |
| Product help     | Search documentation and read bounded pages with canonical links                                                |
| Campaigns        | List/read campaigns; create campaigns; owner updates to name, description and images; invite metadata only      |
| Characters       | Discover templates, create characters, edit supported metadata/portraits, rich-text tabs and legacy CoC7 fields |
| Notes            | Read/create/update rich notes, organize sidebars, upload images and search eligible campaign note contents      |
| Library          | Discover accessible books/PDFs, search bounded excerpts and expand a relevant hit with exact source links       |
| Sessions         | Read session summaries and timelines; speech is opt-in and separately gated                                     |
| Scenes and music | Create/edit scenes, organize folders, search/attach catalog tracks and upload MP3 soundtracks                   |
| Scheduling       | Read/save schedules, view occurrences/rosters, set your own RSVP and export an ICS file for manual import       |

Scheduling requires preview access. Note-content search requires the campaign
owner's internal-testing access, enabled setting, eligible Pro access and a ready
index. ICS export can reconcile internal occurrence state; it does not write to
an external calendar. The usage skill documents exact tool selection, revisions,
idempotency, recovery, citations and permission boundaries.

The MCP does not execute dice rolls, delete campaigns or notes, manage members,
reveal invitation URLs, edit scene maps/fog, change character ownership, or expose
raw transcripts and full library PDFs. Do not infer MCP support from a feature
available elsewhere in the Quest Portal app.

## Status and maintenance

This is a source package for the Git-backed marketplace. Portable
`plugin.json`/`mcp.json`, Codex `.codex-plugin/plugin.json`/`.mcp.json` and the
Claude `.claude-plugin/plugin.json` manifest are kept in sync. It supplies read/write tools and guidance, with no embedded sheet or
Battlemap view.

As researched on 2026-10-05, GitHub recorded successful production deployment of
the public MCP and OAuth services from `d640dd0961c485240431b39e1914afa728afb857`.
The MCP, OAuth and canonical-skill trees at that revision match the researched
main revision `66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4`. This establishes source
and deployment-history alignment, not a new authenticated test or native-host
acceptance. No public-directory submission is included.

Maintain the skill against the canonical server skill, excluding development
evals, and retain the packaged connection/access additions. Server tool schemas
remain authoritative. See the repository's
[research and validation record](https://github.com/QuestPortal/plugins/blob/main/docs/questportal-mcp-status.md)
for evidence and remaining checks; that link becomes available when this change
lands on `main`.
