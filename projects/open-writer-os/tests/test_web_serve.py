#!/usr/bin/env python3
"""Offline tests for the 2.0 web server (web/serve.py) and mock upstream.

Everything runs on 127.0.0.1 with ephemeral ports; no external network.
"""
from __future__ import annotations

import http.client
import importlib.util
import json
import sys
import threading
import unittest
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


serve = _load("owos_web_serve", PROJECT / "web" / "serve.py")
mock_upstream = _load("owos_mock_upstream", PROJECT / "web" / "tests" / "mock_upstream.py")


class WebServeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.upstream = mock_upstream.MockUpstream().start()

    @classmethod
    def tearDownClass(cls):
        cls.upstream.stop()

    def _start_web(self, api_key: str = ""):
        server = serve.make_server(port=0, upstream=self.upstream.url, api_key=api_key)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        host, port = server.server_address[:2]
        return host, port

    def _request(self, host, port, method, path, body=None, headers=None):
        conn = http.client.HTTPConnection(host, port, timeout=10)
        payload = json.dumps(body).encode() if body is not None else None
        conn.request(method, path, body=payload, headers=headers or {})
        resp = conn.getresponse()
        data = resp.read()
        conn.close()
        lowered = {k.lower(): v for k, v in resp.getheaders()}
        return resp.status, lowered, data

    def test_healthz(self):
        host, port = self._start_web()
        status, _, body = self._request(host, port, "GET", "/healthz")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"ok": True})

    def test_serves_app_index(self):
        host, port = self._start_web()
        status, headers, body = self._request(host, port, "GET", "/")
        self.assertEqual(status, 200)
        self.assertIn(b"Open Writer OS 2.0", body)
        self.assertIn(b"core.js", body)

    def test_serves_static_js(self):
        host, port = self._start_web()
        status, headers, _ = self._request(host, port, "GET", "/core.js")
        self.assertEqual(status, 200)
        self.assertIn("javascript", headers.get("content-type", ""))

    def test_proxy_post_streams_and_server_key_wins(self):
        self.upstream.requests.clear()
        host, port = self._start_web(api_key="server-secret")
        status, _, body = self._request(
            host, port, "POST", "/api/chat",
            body={"model": "m", "messages": [{"role": "user", "content": "hi"}], "stream": True},
            headers={"Content-Type": "application/json", "Authorization": "Bearer client-key"})
        self.assertEqual(status, 200)
        tokens = []
        for line in body.decode().splitlines():
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            if data.get("message", {}).get("content"):
                tokens.append(data["message"]["content"])
        self.assertEqual("".join(tokens), "Hello from ollama")
        req = self.upstream.requests[-1]
        self.assertEqual(req["authorization"], "Bearer server-secret")
        self.assertNotIn("client-key", req["authorization"])

    def test_proxy_forwards_client_key_when_no_server_key(self):
        self.upstream.requests.clear()
        host, port = self._start_web(api_key="")
        status, _, _ = self._request(
            host, port, "POST", "/v1/chat/completions",
            body={"model": "m", "messages": [], "stream": True},
            headers={"Content-Type": "application/json", "Authorization": "Bearer client-key"})
        self.assertEqual(status, 200)
        req = self.upstream.requests[-1]
        self.assertEqual(req["path"], "/v1/chat/completions")
        self.assertEqual(req["authorization"], "Bearer client-key")

    def test_proxy_get_tags(self):
        self.upstream.requests.clear()
        host, port = self._start_web()
        status, _, body = self._request(host, port, "GET", "/api/tags")
        self.assertEqual(status, 200)
        models = [m["name"] for m in json.loads(body)["models"]]
        self.assertEqual(models, ["llama3.2", "mistral"])

    def test_non_proxy_post_is_404(self):
        host, port = self._start_web()
        status, _, _ = self._request(host, port, "POST", "/nope", body={})
        self.assertEqual(status, 404)

    def test_upstream_down_returns_502(self):
        server = serve.make_server(port=0, upstream="http://127.0.0.1:1", api_key="")
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        self.addCleanup(server.server_close)
        host, port = server.server_address[:2]
        status, _, _ = self._request(host, port, "POST", "/api/chat", body={})
        self.assertEqual(status, 502)


if __name__ == "__main__":
    unittest.main()
