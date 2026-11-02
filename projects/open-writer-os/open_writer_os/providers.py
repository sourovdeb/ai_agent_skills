#!/usr/bin/env python3
"""Model providers for Open Writer OS.

Two backends, both standard-library only:

* ``ollama``    - a local Ollama server (default http://127.0.0.1:11434).
                  Fully offline; no key, no data leaves the machine.
* ``openai``    - any OpenAI-compatible chat-completions endpoint
                  (OpenRouter, Together, Groq, Mistral, a self-hosted
                  llama.cpp server, ...). The API key is read from an
                  environment variable, never stored in project files.

Provider settings live in ``provider.json`` at the project root. They are
plain, non-secret configuration (base URL, model name); secrets stay in
the environment.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_MODEL = "llama3.2"
TIMEOUT_SECONDS = 300


class ProviderError(RuntimeError):
    """Raised when a model call cannot be completed."""


def _post_json(url: str, payload: dict, headers: dict, timeout: int = TIMEOUT_SECONDS) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method="POST")
    request.add_header("Content-Type", "application/json")
    for key, value in headers.items():
        request.add_header(key, value)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise ProviderError(f"provider returned HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ProviderError(f"cannot reach provider at {url}: {exc.reason}") from exc


def _ollama_chat(base_url: str, model: str, messages: list[dict], options: dict) -> str:
    url = base_url.rstrip("/") + "/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": options,
    }
    data = _post_json(url, payload, {})
    message = data.get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise ProviderError("ollama response did not contain message.content")
    return content


def _openai_chat(base_url: str, model: str, messages: list[dict], options: dict,
                 api_key: str, timeout: int) -> str:
    url = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": options.get("temperature", 0.8),
    }
    if "max_tokens" in options:
        payload["max_tokens"] = options["max_tokens"]
    data = _post_json(url, payload, {"Authorization": f"Bearer {api_key}"}, timeout)
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ProviderError(f"unexpected OpenAI-compatible response: {str(data)[:300]}") from exc


def chat(provider: dict, messages: list[dict], options: dict | None = None) -> str:
    """Send a chat-completions style request and return the assistant text.

    ``provider`` is the parsed ``provider.json``:
    ``{"backend": "ollama"|"openai", "base_url": str, "model": str,
       "api_key_env": str (openai only)}``.
    """
    options = options or {}
    backend = provider.get("backend", "ollama")
    model = provider.get("model") or DEFAULT_MODEL
    if backend == "ollama":
        base_url = provider.get("base_url") or DEFAULT_OLLAMA_URL
        return _ollama_chat(base_url, model, messages, options)
    if backend == "openai":
        env_name = provider.get("api_key_env", "OPEN_WRITER_OS_API_KEY")
        api_key = os.environ.get(env_name, "")
        if not api_key:
            raise ProviderError(
                f"environment variable {env_name} is not set; "
                "export your API key before running (it is never stored on disk)"
            )
        base_url = provider.get("base_url") or "https://api.openai.com/v1"
        return _openai_chat(base_url, model, messages, options, api_key,
                            int(options.get("timeout", TIMEOUT_SECONDS)))
    raise ProviderError(f"unknown provider backend: {backend!r}")


def list_ollama_models(base_url: str = DEFAULT_OLLAMA_URL) -> list[str]:
    """Return model names available on a local Ollama server."""
    url = base_url.rstrip("/") + "/api/tags"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, OSError) as exc:
        raise ProviderError(f"cannot reach ollama at {base_url}: {exc}") from exc
    return sorted(m.get("name", "") for m in data.get("models", []) if m.get("name"))
