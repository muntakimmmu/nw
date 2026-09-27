#!/usr/bin/env bash
# Build the G4 SSH testbed on Ubuntu 24.04 (as root). Idempotent.
#   OpenSSH 9.6p1 client  : Ubuntu package          (NTRU-Prime-only PQ class)
#   OpenSSH 10.5p1        : built from source       (server + both-families client)
#   Go x/crypto/ssh v0.55 : built from module proxy (ML-KEM-only PQ class)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
apt-get install -y -qq build-essential autoconf zlib1g-dev libssl-dev openssh-client golang-go >/dev/null
if [ ! -x /opt/openssh10/sbin/sshd ]; then
  B=$(mktemp -d); git clone -q --depth 1 --branch V_10_5_P1 https://github.com/openssh/openssh-portable "$B/o"
  (cd "$B/o" && autoreconf && ./configure -q --prefix=/opt/openssh10 --sysconfdir=/opt/openssh10/etc \
     --with-privsep-path=/opt/openssh10/empty --without-pam && make -s -j"$(nproc)" && make -s install-nokeys)
fi
mkdir -p /opt/openssh10/empty
id sshd >/dev/null 2>&1 || useradd -r -s /usr/sbin/nologin -d /opt/openssh10/empty sshd
(cd "$HERE/goclient" && go build -o goclient .)
/usr/bin/ssh -V; /opt/openssh10/bin/ssh -V; "$HERE/goclient/goclient" x -Q
