"""Shared helper used by every challenge container to fetch its flag material.

Reads PICOCLONE_SERVER + PICOCLONE_INSTANCE_TOKEN, calls the server for this
instance's encoded blob, and returns (codec, blob). The container embeds the blob;
the plaintext flag is recovered only by solving.
"""

from __future__ import annotations

import os
import sys
import urllib.request
import json


def fetch_material() -> dict:
    server = os.environ["PICOCLONE_SERVER"].rstrip("/")
    token = os.environ["PICOCLONE_INSTANCE_TOKEN"]
    # the instance token encodes the instance id; the server resolves it from the token,
    # but the material route also takes the id in the path — decode it from the JWT payload.
    import base64 as _b64
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    instance_id = json.loads(_b64.urlsafe_b64decode(payload))["instance_id"]
    req = urllib.request.Request(f"{server}/api/instances/{instance_id}/material",
                                 headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


if __name__ == "__main__":
    print(json.dumps(fetch_material()))
