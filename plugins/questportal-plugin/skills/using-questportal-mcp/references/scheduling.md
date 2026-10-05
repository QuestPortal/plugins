# Campaign scheduling

Use the campaign-scheduling tools to inspect a configured schedule, list its upcoming generated occurrences, inspect response rosters, save a complete owner-managed schedule, set the authenticated member's own response, or export one occurrence as an ICS file for manual calendar import.

## Access and authorization

Every scheduling tool requires campaign-scheduling preview access for the authenticated Quest Portal account and an active owner or player membership in the target campaign.

- Schedule, occurrence, roster, and ICS reads use `campaigns:read`.
- Complete schedule saves and occurrence-response changes use `campaigns:write`.
- Only the campaign owner can save a schedule.
- Owners and players can read schedules and occurrences and can change only their own occurrence response.

Safe not-found errors do not reveal whether a campaign, schedule, occurrence, role, or feature gate caused the failure. Do not fall back to private APIs or browser automation.

## Read a schedule and its occurrences

Call `questportal_get_campaign_schedule` first. A `configured` result contains the complete schedule, its `expectedUpdatedAt` revision, and bounded upcoming session times. A `not_configured` result is an ordinary empty state.

Call `questportal_list_campaign_schedule_occurrences` when the task needs stable occurrence IDs, the caller's current response, calendar sequence/revision metadata, or the next year of upcoming times. It returns at most 400 chronological occurrences. Generated schedule occurrences are distinct from completed session-history records.

List immediately before calling either occurrence-specific read:

- `questportal_get_campaign_schedule_occurrence_roster` returns the current eligible member roster and response counts. It is not an attendance record.
- `questportal_get_campaign_schedule_occurrence_ics` returns bounded `text/calendar` content and a filename. The user must import it manually; the tool does not connect to an external calendar.

## Complete schedule contract

`questportal_save_campaign_schedule` replaces the complete schedule. Preserve every field that the user did not ask to change.

The schedule includes:

- `id` and `campaignId`, both bound to the target campaign for a new schedule.
- `name`, a non-empty display name.
- `dtStart`, a timezone-aware ISO datetime for the schedule.
- `timezone`, a valid IANA timezone such as `Atlantic/Reykjavik`.
- One to eight `rules`. Each rule supplies a timezone-aware `startDate`, a one-to-24-hour `durationHours`, and one bounded recurrence rule.
- Optional `exceptions.skipDates` and `exceptions.overrides`, each with at most 100 entries. An override identifies the generated `originalStart`, its `newStart`, and the replacement duration.
- `settings.notification` and `settings.syncToCalendar`.
- `updatedAt`, the current revision supplied by Quest Portal.

Recurrence rules may optionally start with `RRULE:` and support `FREQ` values `DAILY`, `WEEKLY`, `MONTHLY`, and `YEARLY`. Supported properties are `FREQ`, `INTERVAL`, `COUNT`, `UNTIL`, `BYDAY`, `BYMONTH`, `BYMONTHDAY`, `BYSETPOS`, and `WKST`. Use one rule per string; do not include line breaks, `DTSTART`, or unsupported properties. `COUNT` and `UNTIL` cannot be combined. Prefer the simplest rule that expresses the requested schedule.

ISO datetimes carry an offset, while the schedule's IANA timezone defines how the recurrence behaves across daylight-saving changes. Preserve both exactly unless the user requested a timezone or start-time change.

Saving `syncToCalendar: true` does not authorize or perform an external calendar insertion through the public MCP. Describe only the schedule state that was saved and use the ICS export when the user wants a calendar artifact.

## Create or change a schedule

For a new schedule:

1. Confirm `questportal_get_campaign_schedule` returns `not_configured`.
2. Set `expectedUpdatedAt` to `null`.
3. Set both `schedule.id` and `schedule.campaignId` to the target campaign ID.
4. Set `schedule.updatedAt` to `0` and provide the complete intended schedule.
5. Save once, then get the schedule and list occurrences to verify the stored fields and generated times.

For an existing schedule:

1. Get it immediately before writing.
2. Copy the complete schedule and change only the fields the user requested.
3. Pass the returned revision as `expectedUpdatedAt`; `schedule.updatedAt` must equal it.
4. Save once, then get the schedule and list occurrences to verify both the stored contract and the generated result.

On `CAMPAIGN_SCHEDULE_CONFLICT`, the schedule changed after it was read. Get it again, reapply only the requested change, and retry with the new revision only if the user's intent still applies. A conflict after a save can also mean the schedule persisted while occurrence reconciliation remains pending, so always read current state before deciding whether to retry.

The public MCP does not delete a schedule, run the product's nested AI schedule assistant, or expose a repair/reconciliation operation.

## Respond to an occurrence

Call `questportal_list_campaign_schedule_occurrences` immediately before responding. Pass one returned occurrence ID to `questportal_set_campaign_schedule_occurrence_response` and set `response` to `yes`, `no`, or `null` to clear it. The authenticated identity is server-bound; there is no input for another member's user ID.

Verify the returned occurrence ID and response. Read the roster as well only when the requested outcome needs the aggregate or visible member state.

If a schedule change removes, moves, or regenerates an occurrence, an older occurrence ID can stop resolving. List again instead of constructing or modifying an occurrence ID.

## Calendar export boundary

Use `questportal_get_campaign_schedule_occurrence_ics` only with an occurrence ID returned by a fresh list. Return or save the exact content as a `.ics` file only when the surrounding agent environment supports that user-requested artifact operation. Otherwise provide the returned content and filename for the user to import.

The ICS operation may reconcile internal generated-occurrence state, so its MCP annotation is not read-only even though it uses the read scope. It does not send invitations, connect a calendar account, create an external event, or promise ongoing synchronization.
