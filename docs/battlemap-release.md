# Battlemap 0.1.2 marketplace release

This package targets the existing Quest Portal Git marketplace. It is an
owner-only pilot, with one persistent library protected by the separate Battlemap
owner sign-in and OAuth consent. Publishing the package does not authorize other
installers to read or change that library. It does not represent an OpenAI public
directory submission or verified guest/multi-user access.

## Changes

- Tool OAuth metadata and authentication challenges identify the permissions
  needed to connect or upgrade a connection. Events retain separate scopes.
- Model-initiated exports open a download card. The card and embedded editor use
  the host download API after a user action; binary data stays out of model text.
- Partial grid edits preserve omitted settings. Tool schemas document cells,
  movement units, facing and replacement collections, with accurate destructive
  annotations.
- Sign-in returns to the requested scene/panel. Temporary service failures and
  timed-out requests offer explicit recovery without replaying a write.
- Offline package validation and deterministic ZIP builds run in CI. The
  portable and Codex manifests retain the same identity, prompts, icon and
  production MCP endpoint.

## Verification boundary

Package tests validate the official Agent Plugins schemas, all eight source
files, manifest/connection parity, skill references, local marketplace entry,
static icon, bounded archive handling and byte-for-byte ZIP contents. The tool
performs no endpoint calls and does not install, authenticate or publish anything.

The application has focused tests for OAuth challenges in both supported MCP
protocol generations, Events scope upgrades, exact grid patches, launch-time
export results, download denial and teardown, and connection recovery. Local
browser fixtures exercise service failure, timeout, retry and retained sign-in
destinations without credentials or persisted data. Narrow viewport checks and
fake host tests do not establish physical-device or native-host acceptance.

An explicitly approved read-only host check on the preceding deployed Worker
confirmed its version, then received `Authentication required` from preferences
and library tools. No settings, scene summaries or contents were returned. The
existing personal plugin URL also returned `Plugin not found` in that browser,
while Plugin Creator could still read its source. No scenes, grants or
subscriptions were created. The release addresses the discovered authentication
metadata gap; successful host linking remains to be demonstrated.

Authenticated host rendering, successful native downloads, external callback
receipts, idle Queue delivery, host-triggered AI actions and physical iOS/Android
remain unverified. A saved package, deployment, passing CI, and marketplace sync
are separate outcomes; none proves those workflows.

## Install and update

Import `https://github.com/QuestPortal/plugins`, branch `main`, with an empty
path, using the workspace marketplace import flow. Refresh the marketplace and
update Battlemap after this release lands. Complete the host's connection flow
with the authorized Battlemap owner; never put the owner phrase into chat.

The existing personal upload is separate from this Git marketplace entry.
Do not add its ID as a workspace migration ID. The package preserves the
current access model and does not change workspace installation policies.
