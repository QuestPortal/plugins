---
name: run-encounter
description: Run Battlemap encounters with fresh state, selected-token context, deterministic spatial answers, and explicitly bounded AI turns.
---

Read fresh permitted state before every action. Use current selection context to resolve “this token”; if ambiguous, ask a short question rather than guessing an ID. Use `query_spatial` for sight, distances and known reachable paths. Submit complete paths to `move_tokens`; only an applied result is a successful move. Keep success and rejection summaries concise and factual.

Use a new command ID for each new user intent. If a response is lost or the outcome is uncertain, retry the exact command ID and payload. A revised plan after a stale conflict uses a new command ID.

In Propose mode, present the proposed plan and let the human apply it. Do not switch control modes to bypass a proposal, pause, expired grant, or denied action. Manual controls stay available in the authenticated Battlemap window.

For delegated turns, verify the current scene, available turn ID, grant ID, epoch, token/object scope, action budget and expiry. Use `preview_turn_plan` when helpful, then `commit_turn_plan`. Never replace a denied delegated call with an ordinary write tool. A human takeover or pause defeats pending plans. The engine prevents duplicate semantic turns even when event IDs or command IDs differ.

Subscriptions require an explicit user instruction describing the event, scene and intended response. Subscribe separately from the control grant. After an event, reread current state; an old event is not authority to move. Do not trigger AI-to-AI loops. Use either an explicit Ask action or an event subscription for one request, not both. Webhook receipt means received, not that a model action completed.

Do not claim future monitoring works until subscription succeeds. If events or host features are unavailable, direct commands, the library, selection and manual play remain available. Use an explicit user-requested message only; selection changes, dragging, pan and zoom must not start model runs.

Undo is a compensating action with preconditions. It cannot erase knowledge already disclosed or restore a revoked grant. Never describe a live fog reveal as safely reversible.
