# Quest Portal directory submission

Prepared 2026-10-14 for the Quest Portal MCP (`https://mcp.questportal.com/mcp`)
and `questportal-plugin` 0.1.2. Nothing has been submitted. This record holds the
answers each portal asks for and the gaps that still block submission. The guest
sheets and Battlemap are separate submissions and are not covered here.

Requirements were read on 2026-10-14 from
[Claude connector submission](https://claude.com/docs/connectors/building/submission),
[Claude plugin submission](https://claude.com/docs/plugins/submit),
[Claude plugin checklist](https://claude.com/docs/plugins/pre-submission-checklist) and
[ChatGPT submission](https://developers.openai.com/apps-sdk/deploy/submission).

## Submissions

| Directory | Type | Source |
| --- | --- | --- |
| Claude | MCP connector | `https://mcp.questportal.com/mcp`, OAuth with dynamic client registration |
| Claude | Plugin bundle | `QuestPortal/plugins`, path `plugins/questportal-plugin`, branch `main` |
| ChatGPT | Plugin with MCP | ZIP from `package.py build` (`questportal-plugin-0.1.2.zip`) |

Claude asks for both the connector and the plugin; the connector listing holds the
server's authentication configuration and can be paired with the plugin.

## Status

| Item | State |
| --- | --- |
| Tool titles and read-only/destructive hints | Present in source for every registered tool; the portals' tool scans confirm |
| OAuth (DCR, PKCE S256, refresh) | Working end to end in Codex on 2026-10-14 |
| Consent rate limiting | Fixed and deployed (`b451e59`, QuestPortal/questportal#10516) |
| Character tools (campaign-empty create loops; sheet read fails on template characters) | **Merged**: QuestPortal/questportal#10520 (`d1bf354`) and the legacy widget contract fix #10521 (`782ec56`); deploy not verified. After deploy: clean up the stuck `reviewer-seed-char-brenna`/`-vell` requests (needs approval), reseed with new keys, and recheck sheet reads for Vell, Brenna and Ada |
| MIT license | In the plugin folder and repository root |
| README (40+ words) | 655 words |
| Website, support, privacy and terms URLs | `www.questportal.com`, `/support`, `/privacy`, `/terms` return 200 |
| ChatGPT review cases | 5 positive, 3 negative in `plugin.json` |
| Public MCP documentation page | **Missing**: no page explains connecting an assistant |
| Privacy policy coverage of agent access | **Unconfirmed**: the policy text does not visibly mention MCP or AI assistants |
| Reviewer account | **Missing** |
| OpenAI domain verification on `mcp.questportal.com` | **Missing**: needs the portal's challenge token |
| Demo recording | **Missing** |
| Release notes | **Missing**: entered at upload |

## Reviewer account

Both directories need a dedicated account, kept available for later reviews:

- Personal Pro access, so every tool is allowed.
- At least one owned campaign with a description, two or more sessions with
  recaps, characters with filled sheets, campaign and private notes, scenes with
  music, and one library source.
- Email and password sign-in with no MFA, email codes or magic links (ChatGPT
  rejects those).
- Not anyone's personal account. Store the credentials in the shared vault.

The ChatGPT review cases assume this data: they list campaigns, summarize the
latest session, read a character sheet, create one note and answer a help question.

## Claude connector listing

| Field | Draft |
| --- | --- |
| Server name (100) | Quest Portal |
| One-liner (200) | Prepare and run your tabletop RPG campaigns in Quest Portal: campaigns, sessions, characters, notes, scenes and music. |
| Categories | Entertainment; Productivity |
| Documentation URL | **Needed** (public MCP page) |
| Privacy policy URL | https://www.questportal.com/privacy |
| Support contact | hi@questportal.com |
| Icon | `plugins/questportal-plugin/assets/icon.svg` |

Description (2,000):

> Quest Portal is a virtual tabletop for running roleplaying games online. Connect
> your Quest Portal account to let Claude work with the campaigns you own or play
> in. Claude can list your campaigns, read session recaps and activity, look up and
> update characters and their sheets, read, search and write campaign notes,
> search your campaign library with links back to the source, build scenes and
> soundtracks, and manage your campaign schedule. Use it to prepare a session from
> last week's recap, draft NPCs and notes, or answer rules questions from your own
> books. Claude acts only with the permissions you approve when you sign in, and
> campaign roles still apply: players see what players can see. Requires a Quest
> Portal account with Pro access.

Use cases: session preparation from recaps and notes; character and NPC
creation; searching campaign notes and library sources; scene and music setup;
scheduling.

Prerequisites: a Quest Portal account with Pro access (the 30-day trial
qualifies). Reads and writes data.

Authentication: OAuth with dynamic client registration. Client ID metadata
documents are also supported.

Data handling: first-party API (Quest Portal's own backend). No personal health
data. No sponsored content.

Compliance: confirm the seven acknowledgements. Of these, check the first-party
API, financial-transaction (none) and AI-media-generation (none) answers.

## Claude plugin data handling

| Question | Answer |
| --- | --- |
| Reads or stores personal data | Reads Quest Portal account content the user authorizes; the plugin stores nothing |
| Sends data to other services | No; only the declared Quest Portal MCP server |
| Retention | The plugin keeps nothing; Quest Portal's privacy policy governs account data |
| Intended for people under 18 | Check against Quest Portal's terms before answering |

## ChatGPT upload

- Build: `python scripts/marketplace/package.py build --output-dir <dir>` and upload
  `questportal-plugin-0.1.2.zip`.
- Authentication: OAuth, registration `dcr`.
- Domain verification: serve the portal's token at
  `https://mcp.questportal.com/.well-known/openai-apps-challenge`. The MCP server
  does not serve that path yet.
- Demo recording: show the five positive cases with the reviewer account.
- Release notes: "First directory release of the Quest Portal plugin: campaign,
  session, character, note, library, scene, music and scheduling tools over OAuth."
