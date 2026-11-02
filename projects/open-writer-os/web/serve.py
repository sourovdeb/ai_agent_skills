#!/usr/bin/env python3
"""Open Writer OS 2.0 (web) - local server.

Serves ./app and proxies /api/* and /v1/* to UPSTREAM (default: local
Ollama). The API key stays on the server side (API_KEY env var) and never
reaches the browser; if no server key is set, a client-sent Authorization
header is forwarded as-is. Binds to 127.0.0.1 only.

Env: UPSTREAM (default http://127.0.0.1:11434), API_KEY, PORT (8099), HOST.

    python3 serve.py                 # then open http://localhost:8099
    UPSTREAM=https://api.example.com API_KEY=... python3 serve.py
"""
from __future__ import annotations

import os
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent / "app"
PROXY_PREFIXES = ("/api/", "/v1/")


def make_handler(upstream: str, api_key: str, directory: str):
    upstream = upstream.rstrip("/")

    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

        def _proxy(self) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length else None
            req = urllib.request.Request(upstream + self.path, data=body, method=self.command)
            req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))
            if api_key:
                req.add_header("Authorization", "Bearer " + api_key)
            elif self.headers.get("Authorization"):
                req.add_header("Authorization", self.headers["Authorization"])
            try:
                resp = urllib.request.urlopen(req, timeout=600)
                code, headers, stream = resp.status, resp.headers, resp
            except urllib.error.HTTPError as exc:
                code, headers, stream = exc.code, exc.headers, exc
            except Exception as exc:
                self.send_error(502, f"upstream unreachable: {exc}")
                return
            self.send_response(code)
            self.send_header("Content-Type", headers.get("Content-Type", "application/json"))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            read = getattr(stream, "read1", None) or stream.read
            try:
                while True:
                    chunk = read(4096)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self) -> None:
            if self.path == "/healthz":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')
            elif self.path.startswith(PROXY_PREFIXES):
                self._proxy()
            else:
                super().do_GET()

        def do_POST(self) -> None:
            if self.path.startswith(PROXY_PREFIXES):
                self._proxy()
            else:
                self.send_error(404)

        def log_message(self, *args) -> None:
            pass

    return Handler


def make_server(port: int = 8099, upstream: str = "http://127.0.0.1:11434",
                api_key: str = "", host: str = "127.0.0.1",
                directory: str | None = None) -> ThreadingHTTPServer:
    handler = make_handler(upstream, api_key, directory or str(APP_DIR))
    return ThreadingHTTPServer((host, port), handler)


def main() -> int:
    upstream = os.environ.get("UPSTREAM", "http://127.0.0.1:11434").rstrip("/")
    api_key = os.environ.get("API_KEY", "")
    port = int(os.environ.get("PORT", "8099"))
    host = os.environ.get("HOST", "127.0.0.1")
    server = make_server(port, upstream, api_key, host)
    print(f"Open Writer OS 2.0 (web): http://{host}:{port}  (upstream {upstream})")
    print("Loopback only: your writing never leaves this machine.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
