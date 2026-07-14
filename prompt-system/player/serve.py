"""Tiny range-capable static server for LOCAL course playback (no publishing).

Why this exists: opening watch.html via file:// fails (browsers block fetch() of the
manifest/cues), and Python's stock `http.server` does NOT support HTTP Range requests, so
video seeking (chapter jumps, quiz skip-ahead) breaks. This serves the project folder with
Range support and opens the player in your browser. Pure standard library — no extra deps.

Usage:  python serve.py            # serves this folder, opens watch.html
        python serve.py 8080       # custom port
"""
from __future__ import annotations

import functools
import http.server
import os
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


class RangeHandler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler + HTTP Range (206) so media seeks correctly."""

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        rng = self.headers.get("Range")
        if not rng:
            return super().send_head()
        path = self.translate_path(self.path)
        if not os.path.isfile(path):
            return super().send_head()
        try:
            unit, _, rangespec = rng.partition("=")
            if unit.strip() != "bytes":
                return super().send_head()
            start_s, _, end_s = rangespec.strip().partition("-")
            size = os.path.getsize(path)
            start = int(start_s) if start_s else 0
            end = int(end_s) if end_s else size - 1
            end = min(end, size - 1)
            if start > end or start >= size:
                self.send_response(416)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return None
            f = open(path, "rb")
            f.seek(start)
            self._range = (start, end)
            self.send_response(206)
            ctype = self.guess_type(path)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.send_header("Content-Length", str(end - start + 1))
            self.end_headers()
            return f
        except (ValueError, OSError):
            return super().send_head()

    def copyfile(self, source, outputfile):
        rng = getattr(self, "_range", None)
        if not rng:
            return super().copyfile(source, outputfile)
        start, end = rng
        remaining = end - start + 1
        chunk = 64 * 1024
        while remaining > 0:
            data = source.read(min(chunk, remaining))
            if not data:
                break
            try:
                outputfile.write(data)
            except (BrokenPipeError, ConnectionResetError):
                break
            remaining -= len(data)

    def log_message(self, *a):           # quiet
        pass


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    handler = functools.partial(RangeHandler, directory=str(ROOT))
    page = "watch.html" if (ROOT / "watch.html").exists() else (
        "index.html" if (ROOT / "index.html").exists() else "")
    for p in range(port, port + 20):
        try:
            httpd = socketserver.ThreadingTCPServer(("127.0.0.1", p), handler)
            break
        except OSError:
            continue
    else:
        print("could not bind a port in range", port, "..", port + 20)
        return
    url = f"http://127.0.0.1:{p}/{page}"
    print(f"Serving {ROOT}\n  -> {url}\nPress Ctrl+C to stop.")
    if os.environ.get("CC_NO_BROWSER") != "1":
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")


if __name__ == "__main__":
    main()
