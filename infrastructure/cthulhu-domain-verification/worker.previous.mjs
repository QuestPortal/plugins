const challengePath = '/.well-known/openai-apps-challenge';
// Public ownership challenge issued for the Call of Cthulhu Marketplace draft.
const challenge = '1CxP6L447tH7FDjy8yrY8D2rVrXJEsL7SwJeBlmuIbQ';

export default {
  fetch(request) {
    if (new URL(request.url).pathname !== challengePath) {
      return new Response('Not found', { status: 404 });
    }
    if (request.method !== 'GET' && request.method !== 'HEAD') {
      return new Response('Method not allowed', {
        status: 405,
        headers: { Allow: 'GET, HEAD' },
      });
    }
    return new Response(request.method === 'HEAD' ? null : challenge, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'no-store',
        'X-Content-Type-Options': 'nosniff',
      },
    });
  },
};
