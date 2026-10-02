---
name: onboarding
description: Introduce Battlemap with one small, persistent tactical encounter and three hands-on actions.
---

Open the Battlemaps library with `open_battlemaps`. Use its empty-argument bootstrap. If the user wants a first encounter, create the sample with `create_scene` and a new command ID, then open the returned scene ID with `open_encounter`. Retry an uncertain creation with the same command ID and identical payload. Do not duplicate scenes merely because a view remounted.

If the host reports authentication is required, use its supported Connect or sign-in flow before retrying. Marketplace installation alone does not grant access to the owner’s library. Do not repeatedly call tools while disconnected, ask for access phrases in chat, or claim a connection is working until a read succeeds.

Teach the sample in three short steps: move Mira, inspect her sight using `query_spatial`, and open the central door using its actual ID and current state token. Let the human manipulate the map directly. Report only changes confirmed by a tool. Coordinates are grid cells measured from a token's top-left corner.

Explain that Player preview filters the canvas, but a GM-authorized conversation may already know hidden information. Geometric sight is not attack legality, illumination, or a complete D&D rules implementation.

If the user wants opponent help, distinguish a one-time command, a proposal, an explicit bounded control grant, and a subscription to future events. Opening the app does not enable automation. Permissions are approved in the authenticated Battlemap window. Do not ask for passwords or tokens in chat.
