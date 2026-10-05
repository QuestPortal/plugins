# Populated creation and revision examples

These are synthetic examples and expected behavior. All native installed-host
acceptance cases below remain **unrun**. A source/unit test or standalone UI
check does not prove application and local saving inside ChatGPT/Codex.

## One populated investigator

Request: “Create a custom 1920s archivist, Ada Wren, with EDU 80, Library Use 70,
Luck 45 and a missing mentor as her reason to investigate.” Build the remaining
assigned values coherently and label them custom, not budget-verified. A supported
shape is:

```json
{
  "requestId": "ada-creation-001",
  "name": "Ada Wren",
  "occupation": "Archivist",
  "age": 32,
  "pronouns": "she/her",
  "residence": "Boston",
  "birthplace": "Providence",
  "era": "1920s",
  "characteristics": {"STR": 40, "CON": 50, "SIZ": 50, "DEX": 60, "APP": 50, "INT": 70, "POW": 60, "EDU": 80},
  "resources": {"luck": 45},
  "skills": [{"id": "library-use", "value": 70}, {"id": "history", "value": 60}],
  "weapons": [],
  "backstory": {"people": "Her mentor vanished after sending an unsigned index card.", "traits": "Patient with evidence, impatient with secrecy."},
  "inventory": "Notebook, pencils, reading glasses",
  "notes": "Custom assigned pregen; occupation allocation and age adjustments not verified."
}
```

Call `create_investigator` with those top-level fields. Omitted skills retain
base values; omitted HP/MP use derived maxima. A prepared payload is not proof
of loading or local saving. Confirm receipt status from actual sheet evidence.
The request ID above is illustrative: use a fresh ID for another creation.

## Distinct group, partial errors and recovery

Request: “Create five 1920s investigators: an archivist, dockworker, physician,
journalist and mechanic, each with different stats, skills and backstory.”
Use one `create_investigators` call with a fresh `requestId` and five distinct
objects in `investigators`. Vary actual strengths, resources, equipment and hooks;
do not rename one identical template five times. At most 20 members per call.

Check each indexed outcome and later sheet receipt. For an uncertain response,
reuse the same request ID, inputs and order. If member index 2 has an invalid
skill value, correct only that failed member at index 2 under the original ID;
keep successes unchanged. Do not resend successful members as a fresh group.
Expected gate: no duplicates or overwritten manual edits; actionable errors and
accurate prepared/loaded/saved/already-applied reporting.

For “Create 23 distinct investigators”, send batches of **20 and 3** with separate
request IDs. Track outcomes within each batch. If the second batch's index 1
fails, retry that batch's original three positions under its own ID, correcting
only index 1 and keeping its successes identical. Do not replay the first batch
as a new creation. This >20-member acceptance case remains unrun in the host.

## Revision with an exact snapshot

Request: “In the sheet I just attached, increase Ada's Library Use to 75 and
add that she trusts the mechanic; leave everything else alone.”
Read the full current attachment, then call `revise_investigator` with a fresh
request ID, that exact object as `character`, and only the intended `changes`.
Preserve existing backstory content when appending text: a supplied string field
replaces that field, it does not append automatically. Skills merge by ID.

Expected gate: unrelated values remain. Reusing the identical revision is
recognized as already applied. A stale base must not overwrite newer edits:
request fresh Attach and use a new request ID. Do not reconstruct the snapshot
from earlier conversation. An empty weapons array clears weapons, whereas an
empty skills array changes nothing.

## Additional acceptance and negative cases

- Name-only creation remains a neutral starting sheet, not a populated build.
- A hard Spot Hidden 60 check with one bonus die uses `value:60`,
  `difficulty:"hard"`, `modifier:1`; target 30. No Luck/resource mutation.
- Explicit zero current resources must survive creation; derived maxima are not
  writable current-resource fields. Characteristic revisions must not heal.
- Storage blocked, missing Web Locks or competing views must report limitations
  honestly. Test reload only in the same available storage partition; verify JSON
  backup. Do not claim phone/desktop sync.
- A request to retrieve a draft on another computer requires an attachment or
  JSON, not a server lookup. A paid rulebook request is not a plugin capability.
- Real session/event acceptance needs separate authorization and a supported host
  callback/signing secret. Session creation alone proves no subscription.

See [workflows](workflows.md) for exact recovery and security boundaries.
