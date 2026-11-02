#!/usr/bin/env python3
"""Mock upstream for offline tests: Ollama-style /api/* and OpenAI-style /v1/*.

Records every request (path, method, Authorization header, body) in
server.requests so tests can assert key handling. Streams a canned reply.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class MockUpstream:
    def __init__(self, port: int = 0, host: str = "127.0.0.1"):
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def _record(self):
                length = int(self.headers.get("Content-Length") or 0)
                body = self.rfile.read(length) if length else b""
                outer.requests.append({
                    "method": self.command,
                    "path": self.path,
                    "authorization": self.headers.get("Authorization"),
                    "body": body.decode("utf-8", "replace"),
                })
                return body

            def _reply(self, payload, ctype="application/json"):
                data = json.dumps(payload).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def do_GET(self):
                self._record()
                if self.path == "/api/tags":
                    self._reply({"models": [{"name": "llama3.2"}, {"name": "mistral"}]})
                elif self.path == "/v1/models":
                    self._reply({"data": [{"id": "gpt-x"}, {"id": "claude-y"}]})
                else:
                    self.send_error(404)

            def do_POST(self):
                self._record()
                if self.path == "/api/chat":
                    chunks = ["Hel", "lo ", "from ", "ollama"]
                    self.send_response(200)
                    self.send_header("Content-Type", "application/x-ndjson")
                    self.end_headers()
                    for c in chunks:
                        line = json.dumps({"message": {"content": c}, "done": False}) + "\n"
                        self.wfile.write(line.encode("utf-8"))
                    self.wfile.write(json.dumps({"done": True}).encode("utf-8") + b"\n")
                elif self.path == "/v1/chat/completions":
                    chunks = ["Hel", "lo ", "from ", "api"]
                    self.send_response(200)
                    self.send_header("Content-Type", "text/event-stream")
                    self.end_headers()
                    for c in chunks:
                        line = "data: " + json.dumps({"choices": [{"delta": {"content": c}}]}) + "\n\n"
                        self.wfile.write(line.encode("utf-8"))
                    self.wfile.write(b"data: [DONE]\n\n")
                else:
                    self.send_error(404)

            def log_message(self, *args):
                pass

        self.requests: list[dict] = []
        self.server = ThreadingHTTPServer((host, port), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        host, port = self.server.server_address[:2]
        return f"http://{host}:{port}"

    def start(self) -> "MockUpstream":
        self.thread.start()
        return self

    def stop(self) -> None:
        self.server.shutdown()
        self.server.server_close()


if __name__ == "__main__":
    mock = MockUpstream(port=8123).start()
    print(f"mock upstream at {mock.url} (Ctrl+C to stop)")
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        mock.stop()
