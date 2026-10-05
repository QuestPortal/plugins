# Quest Portal MCP — research and package status

Researched 2026-10-05 from repository source and GitHub history. This record covers
the authenticated Quest Portal public MCP server maintained by Gummi, and the
`questportal-plugin` package that connects to it. The guest character-sheet
servers, owner-only Battlemap pilot and private internal MCP are separate services.

## Source and deployment evidence

| Evidence                                                  | Observed state                                                                                                                                                                                                                                                        |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Application `main`                                        | [`66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4`](https://github.com/QuestPortal/questportal/commit/66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4)                                                                                                                              |
| Marketplace base                                          | [`46bd7018e0480d6ecef8d1ed6db8725263584de1`](https://github.com/QuestPortal/plugins/commit/46bd7018e0480d6ecef8d1ed6db8725263584de1)                                                                                                                                  |
| Latest completed paired OAuth/public MCP deployment found | [`d640dd0961c485240431b39e1914afa728afb857`](https://github.com/QuestPortal/questportal/commit/d640dd0961c485240431b39e1914afa728afb857), completed 2026-10-05 01:59:20 UTC in [run 37253215772](https://github.com/QuestPortal/questportal/actions/runs/37253215772) |
| Public MCP promotion at deployment time                   | [Job 111585500935](https://github.com/QuestPortal/questportal/actions/runs/37253215772/job/111585500935) recorded 100% traffic to `qp-mcp-public-00267-xes` at 01:59:16 UTC, followed by successful canonical production verification                                 |
| Newer main workflow                                       | [Run 37317123287](https://github.com/QuestPortal/questportal/actions/runs/37317123287) succeeded, but both deploy jobs were skipped; this is not a newer MCP deployment                                                                                               |
| Source alignment                                          | `apps/mcp-public`, `apps/mcp-auth` and `skills/using-questportal-mcp` are identical between the deployed revision and researched main                                                                                                                                 |

The matching public-MCP tree is `609f32a72a565e46affcbf4efa746d0cd01cab17`;
the matching canonical-skill tree is `607c55a308ee0378f77e2e72e264a1403534ff46`.
The deployment record establishes the observed release and traffic assignment
at that time. No current provider inspection, authenticated account flow or
native-host installation was performed for this package change. Linked
application sources and Actions evidence may require Quest Portal repository
access; the distributed package itself has no private-repository dependency.

## Recent Gummi work

These merged changes explain the server's current capabilities. No open MCP PR
by `gummigun` was found during the bounded author/MCP search on this date.

| Merged date (UTC) | Change                                                                                                                                                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2026-09-07        | [#10410 — shared campaign membership benefits](https://github.com/QuestPortal/questportal/pull/10410): campaign-scoped access for qualifying enrolled shared-Pro recipients, filtered discovery and an explicit tool allowlist |
| 2026-09-04        | [#10396 — Core and Pro trial flow](https://github.com/QuestPortal/questportal/pull/10396), including MCP Pro enforcement                                                                                                       |
| 2026-09-03        | [#10394 — character token refresh](https://github.com/QuestPortal/questportal/pull/10394) after portrait updates                                                                                                               |
| 2026-08-27        | [#10376 — complete scene music workflows](https://github.com/QuestPortal/questportal/pull/10376)                                                                                                                               |
| 2026-08-27        | [#10374 — campaign scheduling](https://github.com/QuestPortal/questportal/pull/10374)                                                                                                                                          |
| 2026-08-27        | [#10372 — feature-support guidance](https://github.com/QuestPortal/questportal/pull/10372) and [#10369 — note-search entitlement lookup](https://github.com/QuestPortal/questportal/pull/10369)                                |
| 2026-08-26        | [#10349 — guarded campaign-note search](https://github.com/QuestPortal/questportal/pull/10349)                                                                                                                                 |
| 2026-08-23        | [#10286 — campaign-library retrieval](https://github.com/QuestPortal/questportal/pull/10286)                                                                                                                                   |

## Connection and capability contract

- Endpoint: `https://mcp.questportal.com/mcp`, Streamable HTTP.
- OAuth issuer: `https://auth.questportal.com`, authorization code with PKCE
  S256, resource-bound access tokens, rotating refresh tokens and revocation.
- Browser sign-in and consent belong to the user. No embedded client secret,
  Firebase credential, bearer header or local process is required by the package.
- Scopes cover campaign, character, note and scene reads/writes plus
  `library:read`; `offline_access` supports refresh. The host uses discovery
  and consent rather than a fabricated static authentication block in `mcp.json`.
- All MCP requests require authentication, including discovery and ping. The
  canonical skill ZIP is separately public at
  `https://mcp.questportal.com/agent-skills/using-questportal-mcp.zip`.

The source contains 59 unique tool registrations, matching the canonical skill's
tool index: service/help/skill 4, campaign details/media/invite metadata 9,
scheduling 6, campaign library 3, characters/sheets 10, session history 3,
notes/sidebar/images/search 9, scenes/music 15. Of these, 31 are read-only and
28 are mutations; ICS export may reconcile internal occurrence state.

Authoritative source anchors at the researched revision:

- [Public server and tool surface](https://github.com/QuestPortal/questportal/blob/66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4/apps/mcp-public/README.md)
- [OAuth resource configuration](https://github.com/QuestPortal/questportal/blob/66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4/apps/mcp-public/src/auth-config.ts)
- [Pro and shared-Pro access enforcement](https://github.com/QuestPortal/questportal/blob/66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4/apps/mcp-public/src/mcp-pro-access-operations.ts)
- [Canonical usage skill](https://github.com/QuestPortal/questportal/tree/66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4/skills/using-questportal-mcp)
- [Paired deployment contract](https://github.com/QuestPortal/questportal/blob/66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4/apps/mcp-auth/PRODUCTION_OPERATIONS.md)

## Access and rollout boundaries

Personal Pro supports the complete surface within normal scopes and role checks.
Enrolled shared-Pro recipients can discover tools and use the permitted
campaign-scoped operations only while qualifying access exists in that campaign.
Campaign creation and standalone character work still require personal Pro.
The [shared-membership rollout plan](https://github.com/QuestPortal/questportal/blob/66ac9fa35a3a5a8ebc7018c0594e3e15ee9616a4/docs/plans/shared-membership-access.md)
leaves rollout prerequisites open; source support does not establish universal
enrollment or availability.

Scheduling requires the caller's `canScheduleSessions` preview gate. Note-content
search requires the campaign owner's internal-testing flag, enabled setting,
eligible Pro access and exact ready index. Speech timeline retrieval is opt-in
and independently gated. Permission failures must not be worked around with
private APIs or bulk reads. Invite tools expose metadata, never a usable link.

The plugin makes no claim to execute dice, delete campaigns/notes, manage members,
write external calendars, edit maps/fog, transfer character ownership, or download
raw transcripts/full PDFs. Detailed boundaries and workflows are in the packaged
[usage skill](../plugins/questportal-plugin/skills/using-questportal-mcp/SKILL.md).

## Package and QA record

The package adds a fifth marketplace entry without changing the four existing
plugin identities. It includes portable and Codex manifests/configuration,
existing Quest Portal artwork, a README, attribution, and the canonical skill
with its six domain references plus a new connection/access reference. Package
additions clarify September Pro/shared-Pro behavior and prevent duplicate skill
installation; development evals are excluded.

- **Why / selection:** guard catalog discovery, portable/Codex parity, correct
  authenticated endpoint, complete skill references and archive integrity.
  Use the existing offline marketplace validator and regression suites; source
  comparison checks tool names and access guidance against the implemented API.
- **Platform / environment:** local package files for ChatGPT and Codex; no
  application runtime changes, browser or device consumer.
- **Results:** all 28 existing Python regression tests passed (marketplace 11,
  Pendragon 6, Battlemap 11). The offline validator accepted all five catalog
  packages. The skill-authoring validator passed; all 59 indexed tool names
  matched source registrations and the icon matched its source byte for byte.
  Formatting and whitespace checks passed. Archive generation validates each ZIP
  against the complete source inventory; deterministic round trips are covered by
  the marketplace suite. Independent source review and four workflow dry runs
  found one OAuth server-name example issue, corrected to use the discovered
  connection name and host controls. No remaining actionable issue was found.
- **Credentials:** none for QA; GitHub research used the existing repository
  access. No QA identities or account tokens were retrieved.
- **Data / cleanup:** no campaign data or synthetic production fixtures created.
  Generated validation reports and archives stay outside the repository.
- **Production state changed:** none. No runtime deployment, OAuth grant change,
  workspace import, public-directory submission or live MCP request was performed.
- **Untested:** native ChatGPT/Codex installation, OAuth consent/refresh,
  account-specific tools and entitlements, authenticated reads/writes, iOS/Android
  hosts and current provider traffic. Deployment-history success does not cover
  these acceptance checks.

Run the repository's existing [offline package commands](../scripts/marketplace/README.md)
after edits. Marketplace import/sync distributes source and keeps user account
authorization separate, as described in
[OpenAI's GitHub marketplace guide](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github).
