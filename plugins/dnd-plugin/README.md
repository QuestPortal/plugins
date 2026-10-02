# Dungeons & Dragons

Quest Portal’s guest character sheet for D&D 5.5e, the 2024 revision of fifth
edition. This directory is the authoritative distribution source for
`dnd-plugin`, initially version `0.1.0`, in the
[Quest Portal Git marketplace](https://github.com/QuestPortal/plugins).

The separately hosted application is configured at
[dnd.questportal.com](https://dnd.questportal.com), with the MCP endpoint
`https://dnd.questportal.com/mcp`. No local server or Quest Portal account is
required. This package connects to that application; it does not contain or
deploy the application runtime.

## Included workflows

- Open or create an editable character sheet with abilities, skills, combat,
  spells, features, equipment and character notes.
- Keep guest drafts in the current browser storage partition where supported;
  use validated JSON import/export for portable backups. **Attach** explicitly
  shares current values with the supporting chat host.
- Choose from 339 SRD 5.2.1 spells and 38 weapons. Assign spells to casting
  classes; retain each class’s casting ability and Hit Dice. Apply slot and
  maximum-HP suggestions only through explicit sheet controls.
- Roll d20 tests and damage, and display exact returned results inline in
  supporting hosts. Dice tools do not change character resources.
- Optionally share rolls through a private, account-free play session when
  requested. Sessions expire after 24 hours and retain at most 1,000 rolls.
  Event monitoring requires an explicit subscription and host support.

There is no server character library or device sync. Character creation and
progression choices remain editable; the sheet does not validate every class
feature or automate every rule. It uses the openly licensed SRD 5.2.1 and does
not provide paid rulebooks. See [NOTICE.md](NOTICE.md) for attribution.

## Package files

| File                              | Purpose                                                            |
| --------------------------------- | ------------------------------------------------------------------ |
| `plugin.json`                     | Portable Agent Plugins 1.0 identity and listing metadata.          |
| `mcp.json`                        | Portable Streamable HTTP connection to the hosted MCP endpoint.    |
| `skills/character-sheet/SKILL.md` | Character-sheet, dice and private-session instructions.            |
| `assets/icon.svg`                 | Package-owned icon used by both manifests.                         |
| `.codex-plugin/plugin.json`       | Compatibility manifest for clients using the Codex package layout. |
| `.mcp.json`                       | Matching HTTP connection for the compatibility manifest.           |
| `NOTICE.md`                       | SRD attribution and third-party notices.                           |

Preserve the package name, MCP server key `dnd-sheets`, existing starter prompts
and their order. Keep both manifests’ identity, version and presentation in sync.
The MCP files use the same server key and URL; the portable transport spelling
is `streamable-http`, while the compatibility file uses `http`.

The original unreleased package remains `0.1.0`. Its synchronized runtime adds
the SRD pickers and suggestions, forces death-save DC 10, and omits initiative
success verdicts. Generic dice tools report rolls; explicit sheet actions apply
resource and death-save changes. These descriptions are release candidates until
the matching runtime deployment and host checks recorded in the repository’s
`docs/release-status.md` are complete.

## Release through the existing marketplace

1. Prepare and validate the matching application release in Quest Portal’s
   application repository. Runtime code, tests, deployment and Cloudflare
   configuration belong there. Keep its compiled branding pinned to a reviewed
   public revision of this package’s icon.
2. Review this directory’s manifests, skill, connection and assets together.
   Confirm that the hosted endpoint implements the advertised tools and that
   both manifests still describe the actual behavior. The initial unreleased
   package stays at `0.1.0`; later package releases advance both manifest
   versions together.
3. Release the matching hosted runtime before making newly advertised behavior
   available in the marketplace. Publish package changes through the existing
   review process for `QuestPortal/plugins`. The catalog entry is
   `.agents/plugins/marketplace.json`, with source `./plugins/dnd-plugin`;
   marketplace sync reads the repository’s `main` branch.
4. Refresh the marketplace and update or install the package through the host’s
   supported flow. Verify tool discovery, opening and creating a sheet, native
   embedding, explicit Attach, inline dice, and any advertised session/event
   flow in that host. Record anything the host does not support or that remains
   unverified.

A deployed endpoint or a passing browser mock does not establish that
installation, native embedding, Attach or live callback delivery works in
ChatGPT. A source pull request does not publish the marketplace entry. This Git
marketplace release does not require a separate account upload or public
directory submission, and it does not migrate an existing uploaded plugin.

If a separate archive is needed, include this single `dnd-plugin/` directory
with its hidden compatibility files. Write the archive outside this directory
and exclude credentials, local configuration, dependency/build directories,
symlinks and unrelated files.
