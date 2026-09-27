"""E0 (SSH arm): reproduce Han (arXiv 2609.07849) Table 3 with this testbed's real clients."""
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import oracle
STATES = {"reference": "mlkem768x25519-sha256,sntrup761x25519-sha512@openssh.com,curve25519-sha256",
          "ML-KEM withdrawn": "sntrup761x25519-sha512@openssh.com,curve25519-sha256",
          "NTRU withdrawn": "mlkem768x25519-sha256,curve25519-sha256"}
HAN = {"reference": {"ossh96": "N", "ossh105": "M", "go": "M"},
       "ML-KEM withdrawn": {"ossh96": "N", "ossh105": "N", "go": "cl"},
       "NTRU withdrawn": {"ossh96": "cl", "ossh105": "M", "go": "M"}}
short = lambda a: "M" if a and "mlkem" in a else "N" if a and "sntrup" in a else "cl" if a else "none"
ok = True
for name, kex in STATES.items():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "sshd_config"; p.write_text(f"KexAlgorithms {kex}\n")
        d = oracle.deliver(p)
    got = {c: short(d[c]["alg"]) for c in d}
    match = all(got[c] == HAN[name][c] for c in HAN[name])
    ok &= match
    print(f"{name:18s} {json.dumps(got)}  matches Han Table 3: {match}")
print("E0 SSH:", "REPRODUCED" if ok else "MISMATCH")
