# G4 harness: opencode + Ollama agents with real-handshake scoring

This harness tests whether an LLM coding agent editing a real `sshd_config` silently removes post-quantum (PQ) protection for real clients. It then measures how the verifier's **scope** and **feedback form** change that rate, compared with **model scale**.

- Pre-registration: `../manifests/preregistration_G4.md`
- Gate definition: `../paper/PROPOSAL.md` §21

| Part | File |
|---|---|
| Delivery oracle: real `sshd -d` against real clients; reproduces Han's Table 3 (`../gates/E0_ssh.out`) | `testbed/oracle.py`, `testbed/e0_ssh.py` |
| Testbed build (OpenSSH 9.6 / 10.5, Go x/crypto/ssh v0.55) | `testbed/setup_testbed.sh` |
| Agent loop: opencode, sandboxed, with an advisory verifier fed back by resuming the session | `g4.py` |
| Pre-registered analysis and G4 kill rule | `g4_analyze.py` |
| Scripted OpenAI-compatible endpoint, for **plumbing tests only** | `mock_llm.py` |

## Run it

These steps need a machine that can pull Ollama models. A GPU is strongly recommended.

```bash
sudo research/harness/testbed/setup_testbed.sh
npm install -g opencode-ai@1.18.32
OLLAMA_CONTEXT_LENGTH=32768 ollama serve &          # opencode's prompt needs a large context
ollama pull qwen3:1.7b && ollama pull qwen3:4b && ollama pull qwen3:8b
python3 research/harness/g4.py smoke                 # plumbing check through the real opencode binary
python3 research/harness/g4.py run --models qwen3:1.7b,qwen3:4b,qwen3:8b --seeds 2 \
        --out research/manifests/runs/G4.jsonl       # 252 episodes; resumable
python3 research/harness/g4_analyze.py research/manifests/runs/G4.jsonl
```

If Ollama runs on another host, pass `--base-url http://HOST:11434/v1`. The run commands above are relative to the repository root.

## Sandbox

opencode runs with its own `HOME`, and project config, models fetch, sharing and auto-update are all disabled. Its permissions are:
- edit files in the workspace;
- bash limited to `sshd -t` only;
- no web access;
- no external directories.
