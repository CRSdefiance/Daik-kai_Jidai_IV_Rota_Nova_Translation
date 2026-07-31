from __future__ import annotations

import hashlib
from pathlib import Path


def hash_bytes(data: bytes) -> dict[str, str]:
    return {"sha1": hashlib.sha1(data).hexdigest(), "sha256": hashlib.sha256(data).hexdigest()}


def hash_file(path: str | Path, chunk_size: int = 1024 * 1024) -> dict[str, str]:
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    with Path(path).open("rb") as stream:
        while chunk := stream.read(chunk_size):
            sha1.update(chunk)
            sha256.update(chunk)
    return {"sha1": sha1.hexdigest(), "sha256": sha256.hexdigest()}

