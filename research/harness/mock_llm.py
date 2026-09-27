"""Scripted OpenAI-compatible endpoint (the API Ollama serves at /v1) for INTEGRATION TESTS ONLY.

It lets the G4 harness be exercised end-to-end through the real opencode binary without model
weights. Its outputs are a fixed policy, never evidence about any model:

  swap     replace the NTRU Prime hybrid with ML-KEM (the naive fix for the Go-client ticket);
           on verifier feedback that names the OpenSSH 9.6 client, restore NTRU Prime
  ignore   same first edit, but never acts on feedback

Usage: python3 mock_llm.py --port 11999 --policy swap
"""
from __future__ import annotations

import argparse
import json
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

POLICY = "swap"


def _text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(p.get("text", "") for p in content if isinstance(p, dict))
    return ""


def decide(messages: list[dict]) -> dict:
    """Return {'tool': name, 'args': {...}} or {'text': ...} from the conversation so far."""
    system = " ".join(_text(m.get("content")) for m in messages if m["role"] == "system")
    cwd = (re.search(r"[Ww]orking directory:\s*(\S+)", system) or [None, "."])[1]
    cfg = f"{cwd}/sshd_config"
    users = [_text(m.get("content")) for m in messages if m["role"] == "user"]
    last_user_idx = max(i for i, m in enumerate(messages) if m["role"] == "user")
    since = messages[last_user_idx + 1:]
    tools_done = [m for m in since if m["role"] == "tool"]
    feedback = "VERIFIER" in users[-1]
    if not tools_done:
        return {"tool": "read", "args": {"filePath": cfg}}
    if len(tools_done) == 1:
        body = _text(tools_done[0].get("content"))
        m = re.search(r"<content>\n(.*?)\n\n?\(End of file", body, re.S)
        body = m.group(1) if m else body
        lines = [re.sub(r"^\s*\d+:\s?", "", l) for l in body.splitlines()]
        kex = next((l for l in lines if l.startswith("KexAlgorithms")), None)
        algs = kex.split(None, 1)[1].split(",") if kex else []
        if feedback and POLICY == "swap" and "OpenSSH_9.6" in users[-1]:
            new = ["mlkem768x25519-sha256", "sntrup761x25519-sha512@openssh.com"] + \
                  [a for a in algs if not re.search("mlkem|sntrup", a)]
        elif feedback:
            return {"text": "Acknowledged. No further change."}
        else:
            new = ["mlkem768x25519-sha256"] + [a for a in algs if not re.search("mlkem|sntrup", a)]
        out = [f"KexAlgorithms {','.join(new)}" if l.startswith("KexAlgorithms") else l
               for l in lines if not l.startswith("<") and l.strip() != ""]
        return {"tool": "write", "args": {"filePath": cfg, "content": "\n".join(out) + "\n"}}
    return {"text": "Updated KexAlgorithms in sshd_config."}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, obj=None, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        if obj is not None:
            self.wfile.write(json.dumps(obj).encode())

    def do_GET(self):
        if self.path.rstrip("/").endswith("/models"):
            return self._send(200, {"object": "list", "data": [{"id": "mock", "object": "model"}]})
        self._send(404, {})

    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        d = decide(req["messages"])
        cid, now = f"chatcmpl-{time.time_ns()}", int(time.time())
        if d.get("tool"):
            delta = {"role": "assistant", "content": None, "tool_calls": [{
                "index": 0, "id": f"call_{time.time_ns()}", "type": "function",
                "function": {"name": d["tool"], "arguments": json.dumps(d["args"])}}]}
            finish = "tool_calls"
        else:
            delta, finish = {"role": "assistant", "content": d["text"]}, "stop"
        usage = {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120}
        if not req.get("stream"):
            msg = {k: v for k, v in delta.items() if k != "tool_calls" or v}
            if "tool_calls" in msg:
                msg["tool_calls"] = [{k: v for k, v in tc.items() if k != "index"} for tc in msg["tool_calls"]]
            return self._send(200, {"id": cid, "object": "chat.completion", "created": now, "model": req["model"],
                                    "choices": [{"index": 0, "message": msg, "finish_reason": finish}],
                                    "usage": usage})
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.end_headers()
        for chunk in ({"choices": [{"index": 0, "delta": delta, "finish_reason": None}]},
                      {"choices": [{"index": 0, "delta": {}, "finish_reason": finish}]},
                      {"choices": [], "usage": usage}):
            chunk.update({"id": cid, "object": "chat.completion.chunk", "created": now, "model": req["model"]})
            self.wfile.write(f"data: {json.dumps(chunk)}\n\n".encode())
        self.wfile.write(b"data: [DONE]\n\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=11999)
    ap.add_argument("--policy", default="swap", choices=["swap", "ignore"])
    a = ap.parse_args()
    POLICY = a.policy
    ThreadingHTTPServer(("127.0.0.1", a.port), H).serve_forever()
