# QuestPortalRichNote/v1

`questportal_create_note` and `questportal_update_note` accept one complete canonical rich-note envelope. This is a closed interchange contract, not Markdown, HTML, or an open-ended ProseMirror document. Unknown versions, node names, marks, attributes, and extra keys are rejected even if a Quest Portal editor could represent related internal state.

## Required shape

The document must begin with an H1 and include at least one following body block. The text in the first H1 becomes the sidebar title; make it meaningful and keep it within 200 characters. An empty derived title becomes `Untitled`.

```json
{
  "kind": "questportal-rich-note",
  "version": 1,
  "document": {
    "type": "doc",
    "content": [
      {
        "type": "heading",
        "attrs": { "level": 1 },
        "content": [{ "type": "text", "text": "Session 12: The Glass Keep" }]
      },
      {
        "type": "paragraph",
        "content": [
          { "type": "text", "text": "Goal: learn who opened the western gate." }
        ]
      }
    ]
  }
}
```

Create a note with its intended initial document. Do not create a placeholder and update it merely to add content that the creation call already accepts.

## Supported vocabulary

Use exact casing.

- Top-level block nodes allowed in `document.content`: `paragraph`, `heading` (levels 1–4), `blockquote`, `boxText`, `bulletList`, `orderedList`, `codeBlock`, `collectionWidget`, `CustomImage`, `details`, `horizontalRule`, `pointsWidget`, `slotsWidget`, `table`, `taskList`, and `youtube`.
- Container-only nodes: `listItem` belongs inside `bulletList` or `orderedList`; `taskItem` belongs inside `taskList`; `tableRow` belongs inside `table`; `tableCell` and `tableHeader` belong inside `tableRow`; and `detailsSummary` plus `detailsContent` belong inside `details`. Do not place these directly in `document.content`.
- Inline nodes: `text`, `hardBreak`, `InlineImage`, `link-mention`, `slashMention`, `emoji`, `modifierWidget`, and `rollButton`.
- Marks: `bold`, `highlight`, `italic`, `link`, `strike`, `subscript`, `superscript`, and `underline`.

This list identifies the vocabulary; the live tool schema and validation errors remain authoritative for size and field limits. Useful structural rules include:

- List items begin with a paragraph. Task items contain paragraphs.
- Tables contain rows, which contain table cells or headers, which contain block content.
- Collection column `accessorKey` values and row IDs are unique. `id` and unsafe object keys cannot be column accessors, and row cells may use only declared accessors.
- Widget and row identifiers carry state. Preserve them when editing existing content; generate distinct, stable identifiers only for genuinely new widgets or rows.
- A canonical rich note may be readable at a larger size than can be written back in one mutation. If a tool returns `NOTE_TOO_LARGE`, do not split, truncate, or discard content without the user's direction.

## Marks, links, and mentions

A link mark uses the full canonical attribute shape:

```json
{
  "type": "text",
  "text": "Quest Portal guide",
  "marks": [
    {
      "type": "link",
      "attrs": {
        "class": null,
        "href": "https://www.questportal.com/docs",
        "rel": "noopener noreferrer",
        "target": "_blank"
      }
    }
  ]
}
```

Links and image sources accept safe relative or HTTP(S) URLs; link marks may also use `mailto:`. A `_blank` link's `rel` must include both `noopener` and `noreferrer`. YouTube nodes accept HTTPS YouTube or YouTube NoCookie hosts. Do not embed raw HTML or unsafe URL schemes.

`link-mention` supports campaign/private notes, library pages, sheets, hidden sheets, and templates, but the public MCP does not discover every required identifier or character sheet. Preserve existing mentions exactly. Create a mention only when its exact IDs, owner context, type, and title are known from supported context; otherwise use plain text rather than inventing a target.

## Safe update and preservation

`questportal_update_note` is a complete-document replacement with revision-aware collaboration. To change an existing note:

- [ ] **REQUIRED — Read:** Call `questportal_get_note` and retain its complete `richNote` and `revision`.
- [ ] **REQUIRED — Transform minimally:** Copy that document and make the smallest transformation that expresses the user's request.
- [ ] **REQUIRED — Preserve:** Keep every unmodified block, mark, attribute, URL, mention, widget ID, collection row, and ordering detail—even content you would not have authored yourself.
- [ ] **REQUIRED — Replace completely:** Send the complete transformed envelope with the retrieved revision.
- [ ] **REQUIRED — Verify:** Interpret the status, reread, and verify the intended result.

Never rebuild a rich note from a prose summary: doing so silently loses widgets, links, images, formatting, and concurrent work. Do not change note visibility as part of a content update; the public update tool has no visibility operation.

On `conflict`, the request was not applied. Get the new document and revision, reapply only the intended edit to that version, and retry. On `merged`, concurrent content was preserved; get and inspect the merged document before editing again. `already_applied` is successful, but reread when the exact final content matters. After `updated`, verify meaningful changes with `questportal_get_note` rather than trusting a status alone.

For example, to append a clue, retain the returned envelope and append this block to `document.content`; do not replace the preceding blocks:

```json
{
  "type": "paragraph",
  "content": [
    {
      "type": "text",
      "text": "New clue: the west-gate key bears a glass raven."
    }
  ]
}
```

To rename a note, change the text content of the first H1 while preserving the entire remainder. This changes the derived sidebar title; do it only when renaming is intended.

## Image flow

`questportal_upload_note_image` uploads an immutable asset; it does not change the note. Use the following sequence:

- [ ] **REQUIRED — Preflight the target:** Resolve the exact existing note and intended placement, then call `questportal_get_note` before uploading.
- [ ] **REQUIRED — Establish writability:** Build the complete intended post-insertion document from that response and establish that it is safely writable. A successful read is not sufficient proof: reads allow Yjs documents up to 4 MiB, while note mutations allow only 768 KiB, and the current MCP exposes no exact dry-run or encoded-size field. If the note is large or the candidate's writability cannot be established with confidence, stop before upload, explain the orphaned-asset risk, and obtain user direction.
- [ ] **REQUIRED — Upload once:** Upload canonical base64 JPEG, PNG, or WebP bytes with a stable idempotency key. Do not send a data URL or ask the tool to fetch a remote URL.
- [ ] **REQUIRED — Rebase after upload:** Call `questportal_get_note` again so the insertion uses the latest document and revision, then reapply the intended insertion to that complete document.
- [ ] **REQUIRED — Insert:** Add the returned asset URL as a new `CustomImage` block at the intended position.
- [ ] **REQUIRED — Update and verify:** Call `questportal_update_note`, handle `conflict` or `merged`, then get the note to verify the image and surrounding content.

Use the canonical image attributes. Boolean values and the strings `"true"`/`"false"` are accepted for `share` and `session-story`; use booleans for new content unless preservation requires the existing representation.

```json
{
  "type": "CustomImage",
  "attrs": {
    "alt": "Annotated map of the Glass Keep",
    "session-story": false,
    "share": false,
    "src": "https://returned.questportal.asset/example",
    "title": "Glass Keep map"
  }
}
```

Use `InlineImage` only when the image is intentionally embedded in inline content; newly uploaded standalone art normally belongs in `CustomImage`. `share` is image metadata, not note visibility. Upload only when insertion is intended because the public MCP cannot delete an orphaned uploaded asset.

## Roll controls and structured collections

An inline roll button uses `formula`, `id`, and `text` attributes. Formula strings are stored by the note contract but are not executed or fully semantically validated by MCP. Use [dice-formulas.md](dice-formulas.md) and do not imply that creating the node performs a roll.

Ordinary character-sheet tabs use a different outer envelope,
`QuestPortalCharacterSheetTab/v1`, but the same closed document vocabulary.
This includes `rollButton`, `modifierWidget`, and collection widgets on
universal, template-based, and CoC7 note tabs. Preserve complete tab content and
use the tab revision exactly as you would for a note update.

```json
{
  "type": "paragraph",
  "content": [
    {
      "type": "rollButton",
      "attrs": {
        "formula": "1d20+5",
        "id": "glass-keep-perception",
        "text": "Perception"
      }
    }
  ]
}
```

For compact structured data, `collectionWidget` columns declare their accessors and each row supplies a unique `id`. A simple roster-like collection is valid rich-note content:

```json
{
  "type": "collectionWidget",
  "attrs": {
    "columns": [
      { "accessorKey": "name", "header": "Name", "minSize": 120 },
      { "accessorKey": "role", "header": "Role", "minSize": 120 }
    ],
    "data": [
      {
        "id": "roster-mira",
        "name": { "type": "text", "value": "Mira Vale" },
        "role": { "type": "text", "value": "Scout" }
      }
    ],
    "headerhidden": false,
    "name": "Roster"
  }
}
```

This represents note content only. It does not create or update Quest Portal character entities.
