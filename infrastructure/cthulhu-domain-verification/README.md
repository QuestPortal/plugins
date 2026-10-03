# Call of Cthulhu public pages and domain verification

This Worker serves the OpenAI ownership challenge, a branded walkthrough at `/walkthrough.mp4`, and four static public pages on exact routes: `/about`, `/support`, `/privacy`, and `/terms`. The sheet at `/`, MCP at `/mcp`, and application sessions remain on the existing application Worker. Do not add wildcard routes or replace its custom domain.

Deployed through Cloudflare dashboard on 2026-10-01. `wrangler.json` records the six exact routes. No GitHub deployment integration is configured. HTML source files are review copies; worker.mjs contains the deployed static page bodies. Keep those copies synchronized when editing.

## Verification

- Browser loaded all four public URLs without login; page text and publisher were checked.
- OpenAI imported all four URLs and metadata validation reported No Issues.
- Local handler assertions checked four GET pages, empty HEAD responses, unchanged ownership challenge, and unrelated-path isolation.
- Shell public verification was blocked by sandbox DNS. Browser and OpenAI metadata validation succeeded.
- No session data or database settings were changed; no synthetic session cleanup is required.

## Rollback

Remove only the four added page routes to stop serving the pages. Preserve the original challenge route for domain verification. `worker.previous.mjs` is the pre-page challenge-only handler. Do not deploy that handler while retaining the public page routes unless intentional 404s are desired.

## Walkthrough video

`walkthrough.mp4` is a 23-second silent captioned recording of the standalone guest sheet with Quest Portal branding. `worker.mjs` embeds its bytes and serves GET/HEAD with byte-range support. The about page embeds this route with native video controls. Local assertions covered full/range/invalid-range responses; browser playback reached the end. `worker.before-video.mjs` preserves the previous page deployment. To roll back the video, restore that handler and remove only the video route.

## Source preservation — 2026-10-02

The previously untracked deployed source, HTML/video copies and rollback handlers
are now retained together. No routes, content, credentials or deployments were
changed. Run `node --test infrastructure/cthulhu-domain-verification/worker.test.mjs`
from the repository root for offline exact-route, page-copy, video-byte and
byte-range checks. Earlier browser/deployment statements above are historical
evidence from 2026-10-01, not re-executed production checks. Public account/zone
identifiers and the publicly served ownership challenge are configuration, not
authentication credentials. Never add API tokens or account credentials here.
