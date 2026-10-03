import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import test from 'node:test';
import worker from './worker.mjs';

const origin = 'https://cthulhu.questportal.com';
const request = (path, init) => worker.fetch(new Request(origin + path, init));
const video = await readFile(new URL('./walkthrough.mp4', import.meta.url));
const config = JSON.parse(await readFile(new URL('./wrangler.json', import.meta.url)));

test('deployment remains scoped to the six existing exact routes', () => {
  assert.deepEqual(config.routes.map(r => r.pattern).sort(), [
    '/.well-known/openai-apps-challenge', '/about', '/privacy', '/support', '/terms', '/walkthrough.mp4',
  ].map(p => 'cthulhu.questportal.com' + p).sort());
  assert.ok(config.routes.every(r => r.zone_name === 'questportal.com'));
});
for (const page of ['about', 'support', 'privacy', 'terms']) {
  test(`${page} deployed body matches retained HTML; HEAD has no body`, async () => {
    const response = request('/' + page);
    assert.equal(response.status, 200);
    assert.match(response.headers.get('Content-Type'), /^text\/html/);
    assert.equal((await response.text()).trim(), (await readFile(new URL(`./${page}.html`, import.meta.url), 'utf8')).trim());
    assert.equal(await request('/' + page, {method: 'HEAD'}).text(), '');
  });
}
test('unrelated application, MCP and session routes remain outside this handler', () => {
  for (const path of ['/', '/mcp', '/api/sessions', '/about/extra']) assert.equal(request(path).status, 404);
});
test('challenge remains public GET/HEAD only without exposing its value in test output', async () => {
  const get = request('/.well-known/openai-apps-challenge');
  assert.equal(get.status, 200);
  assert.match(get.headers.get('Content-Type'), /^text\/plain/);
  assert.ok((await get.text()).length > 20);
  assert.equal(await request('/.well-known/openai-apps-challenge', {method: 'HEAD'}).text(), '');
  assert.equal(request('/.well-known/openai-apps-challenge', {method: 'POST'}).status, 405);
});
test('embedded walkthrough matches the retained video bytes', async () => {
  const response = request('/walkthrough.mp4');
  assert.equal(response.status, 200);
  assert.deepEqual(Buffer.from(await response.arrayBuffer()), video);
  const head = request('/walkthrough.mp4', {method: 'HEAD'});
  assert.equal(Number(head.headers.get('Content-Length')), video.length);
  assert.equal(await head.text(), '');
});
test('video ranges preserve bytes and reject invalid requests', async () => {
  for (const [range, start, end] of [['bytes=0-31',0,31], ['bytes=32-',32,video.length-1], ['bytes=-16',video.length-16,video.length-1]]) {
    const result = request('/walkthrough.mp4', {headers: {Range: range}});
    assert.equal(result.status, 206);
    assert.deepEqual(Buffer.from(await result.arrayBuffer()), video.subarray(start,end+1));
  }
  for (const range of ['bytes=9999999-', 'bytes=5-2', 'bytes=-0', 'bytes=a-b', 'bytes=0-1,4-5']) {
    assert.equal(request('/walkthrough.mp4', {headers: {Range: range}}).status, 416);
  }
  assert.equal(request('/walkthrough.mp4', {method:'POST'}).status, 405);
});
