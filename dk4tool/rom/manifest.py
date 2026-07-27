from __future__ import annotations

from pathlib import PurePosixPath

from dk4tool.scan.entropy import shannon_entropy

from .hashing import hash_bytes, hash_file
from .nds import NdsImage


def build_manifest(image: NdsImage) -> dict[str, object]:
    rom_hashes = hash_file(image.source)
    metadata = image.metadata()
    files = []
    for file_id, path, data in image.iter_files():
        hashes = hash_bytes(data)
        suffix = PurePosixPath(path).suffix.lower()
        files.append(
            {
                "id": file_id,
                "path": path,
                "size": len(data),
                **hashes,
                "extension_guess": suffix,
                "entropy": round(shannon_entropy(data), 6),
            }
        )
    files.sort(key=lambda item: (item["path"], item["id"]))
    return {
        "rom": {
            "sha1": rom_hashes["sha1"],
            "sha256": rom_hashes["sha256"],
            "size_bytes": metadata["size_bytes"],
            "game_title": metadata["game_title"],
            "game_code": metadata["game_code"],
            "maker_code": metadata["maker_code"],
        },
        "files": files,
    }

