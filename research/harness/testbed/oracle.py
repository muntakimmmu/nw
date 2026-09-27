"""Delivery oracle for the SSH arm of the G4 pilot.

Delivered post-quantum protection is decided by real handshakes, never by reading the file
(Han, arXiv 2609.07849). For each client class we start a one-shot `sshd -d` on the candidate
configuration, connect one real client, and read the negotiated key exchange from the
server's debug log. Authentication failing after KEX is expected and irrelevant.

Client classes (Han's Table 2 / Table 3 structure, real builds except where marked):
  ossh96   OpenSSH 9.6p1 (Ubuntu 24.04 default client)     NTRU-Prime-only PQ class
  go       golang.org/x/crypto/ssh v0.55.0 (defaults)       ML-KEM-only PQ class
  ossh105  OpenSSH 10.5p1 (built from source)               both families ("stock" modern client)
  legacy   OpenSSH 10.5p1 with a classical-only KEX list    EMULATED classical-only peer
"""
from __future__ import annotations

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SSHD = os.environ.get("PQ_SSHD", "/opt/openssh10/sbin/sshd")
SSH10 = os.environ.get("PQ_SSH10", "/opt/openssh10/bin/ssh")
SSH96 = os.environ.get("PQ_SSH96", "/usr/bin/ssh")
GOCLIENT = os.environ.get("PQ_GOCLIENT", str(HERE / "goclient" / "goclient"))
HOSTKEY = HERE / ".hostkey" / "ssh_host_ed25519_key"

PQ_RE = re.compile(r"(mlkem|sntrup)", re.I)
COMMON = ["-o", "BatchMode=yes", "-o", "StrictHostKeyChecking=no",
          "-o", "UserKnownHostsFile=/dev/null", "-o", "ConnectTimeout=5", "-o", "LogLevel=ERROR"]

CLIENTS = {
    "ossh96": {"label": "OpenSSH_9.6p1 (Ubuntu 24.04 default client)",
               "cmd": lambda port: [SSH96, *COMMON, "-p", str(port), "probe@127.0.0.1", "true"]},
    "go": {"label": "Go golang.org/x/crypto/ssh v0.55.0 (deploy tooling)",
           "cmd": lambda port: [GOCLIENT, f"127.0.0.1:{port}"]},
    "ossh105": {"label": "OpenSSH_10.5p1 (current stock client)",
                "cmd": lambda port: [SSH10, *COMMON, "-p", str(port), "probe@127.0.0.1", "true"]},
    "legacy": {"label": "legacy classical-only client (emulated)",
               "cmd": lambda port: [SSH10, *COMMON, "-o",
                                    "KexAlgorithms=curve25519-sha256,ecdh-sha2-nistp256,diffie-hellman-group14-sha256",
                                    "-p", str(port), "probe@127.0.0.1", "true"]},
}
CENSUS = list(CLIENTS)


def ensure_hostkey() -> None:
    if not HOSTKEY.exists():
        HOSTKEY.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(Path(SSH10).with_name("ssh-keygen")), "-q", "-t", "ed25519", "-N", "",
                        "-f", str(HOSTKEY)], check=True)
        os.chmod(HOSTKEY, 0o600)


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _overrides(port: int, pid: str) -> list[str]:
    # Command-line -o options take precedence (first match wins in sshd), so the agent's file
    # governs everything except where the daemon listens and which host key it uses.
    return ["-o", f"Port={port}", "-o", "ListenAddress=127.0.0.1", "-o", f"HostKey={HOSTKEY}",
            "-o", f"PidFile={pid}", "-o", "UsePAM=no", "-o", "LogLevel=DEBUG1"]


def validate(cfg: Path) -> tuple[bool, str]:
    ensure_hostkey()
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([SSHD, "-t", "-f", str(cfg), *_overrides(22, f"{td}/pid")],
                           capture_output=True, text=True, timeout=15)
    return r.returncode == 0, (r.stderr or r.stdout).strip()[-400:]


def dump_kex(cfg: Path) -> list[str]:
    """The vendor's effective-configuration dump (`sshd -T`)."""
    ensure_hostkey()
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([SSHD, "-T", "-f", str(cfg), *_overrides(22, f"{td}/pid")],
                           capture_output=True, text=True, timeout=15)
    for line in r.stdout.splitlines():
        if line.startswith("kexalgorithms "):
            return line.split(" ", 1)[1].split(",")
    return []


def probe(cfg: Path, client: str) -> dict:
    """One real handshake: returns {'alg': negotiated kex or None, 'pq': bool, 'available': bool}."""
    import threading
    ensure_hostkey()
    port = free_port()
    lines: list[str] = []
    ready = threading.Event()
    with tempfile.TemporaryDirectory() as td:
        # `sshd -d` serves exactly one connection and exits, so readiness is read from its log
        # ("Server listening"), never probed with a connection.
        srv = subprocess.Popen([SSHD, "-d", "-e", "-f", str(cfg), *_overrides(port, f"{td}/pid")],
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        def pump():
            for line in srv.stdout:
                lines.append(line)
                if "Server listening" in line:
                    ready.set()
            ready.set()

        t = threading.Thread(target=pump, daemon=True)
        t.start()
        ready.wait(timeout=10)
        try:
            subprocess.run(CLIENTS[client]["cmd"](port), capture_output=True, text=True, timeout=15)
        except subprocess.TimeoutExpired:
            pass
        try:
            srv.wait(timeout=10)
        except subprocess.TimeoutExpired:
            srv.kill()
            srv.wait()
        t.join(timeout=5)
    out = "".join(lines)
    m = re.search(r"kex: algorithm: (\S+)", out)
    alg = m.group(1) if m else None
    return {"alg": alg, "pq": bool(alg and PQ_RE.search(alg)), "available": alg is not None}


def deliver(cfg: Path, clients=CENSUS) -> dict:
    return {c: probe(cfg, c) for c in clients}


def diff(before: dict, after: dict) -> dict:
    lost_pq = [c for c in after if before[c]["pq"] and not after[c]["pq"]]
    lost_av = [c for c in after if before[c]["available"] and not after[c]["available"]]
    gained_pq = [c for c in after if not before[c]["pq"] and after[c]["pq"]]
    return {"lost_pq": lost_pq, "lost_availability": lost_av, "gained_pq": gained_pq}


if __name__ == "__main__":
    cfg = Path(sys.argv[1])
    ok, msg = validate(cfg)
    print(json.dumps({"valid": ok, "msg": msg, "dump": dump_kex(cfg) if ok else None,
                      "delivered": deliver(cfg) if ok else None}, indent=1))
