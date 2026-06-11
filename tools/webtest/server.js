// Minimal static file server WITH HTTP Range support (206) so <video> can seek —
// Python's http.server doesn't do ranges, which breaks media seeking in tests.
const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const PORT = process.env.PORT || 8731;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json',
  '.mp4': 'video/mp4', '.vtt': 'text/vtt', '.png': 'image/png', '.css': 'text/css',
  '.srt': 'text/plain', '.md': 'text/markdown', '.svg': 'image/svg+xml' };

http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const fp = path.join(ROOT, p);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp) || fs.statSync(fp).isDirectory()) {
    res.writeHead(404); return res.end('404');
  }
  const stat = fs.statSync(fp);
  const type = TYPES[path.extname(fp).toLowerCase()] || 'application/octet-stream';
  const range = req.headers.range;
  const pipe = (stream) => {
    stream.on('error', () => { try { res.destroy(); } catch (e) {} });
    res.on('close', () => stream.destroy());     // client aborted (seek/close) -> don't crash
    stream.pipe(res);
  };
  if (range) {
    const m = /bytes=(\d*)-(\d*)/.exec(range) || [];
    let start = m[1] ? parseInt(m[1], 10) : 0;
    let end = m[2] ? parseInt(m[2], 10) : stat.size - 1;
    if (isNaN(start) || isNaN(end) || start > end || start >= stat.size) {
      res.writeHead(416, { 'Content-Range': `bytes */${stat.size}` }); return res.end();
    }
    res.writeHead(206, { 'Content-Range': `bytes ${start}-${end}/${stat.size}`,
      'Accept-Ranges': 'bytes', 'Content-Length': end - start + 1, 'Content-Type': type });
    pipe(fs.createReadStream(fp, { start, end }));
  } else {
    res.writeHead(200, { 'Content-Length': stat.size, 'Content-Type': type, 'Accept-Ranges': 'bytes' });
    pipe(fs.createReadStream(fp));
  }
}).listen(PORT, () => console.log(`range-server ${ROOT} :${PORT}`))
  .on('error', e => console.error('server error', e && e.message));
process.on('uncaughtException', e => console.error('uncaught', e && e.message));  // never die mid-test
