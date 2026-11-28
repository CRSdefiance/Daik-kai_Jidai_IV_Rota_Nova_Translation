"""Package a verified Switch overlay as source-bound binary deltas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import shutil
from tempfile import TemporaryDirectory

from dk4tool.patch.xdelta import XdeltaError, make_xdelta

from .overlay import digest, rebuild, relative_path, verify


def strip_application_header(path: Path) -> None:
    data = path.read_bytes()
    if data[:4] != b"\xd6\xc3\xc4\0" or len(data) < 5 or data[4] & ~0x05:
        raise ValueError(f"Expected an xdelta encoding with the standard code table: {path.name}")
    flags = data[4]
    if not flags & 0x04:
        return

    # xdelta's optional header contains input and output names. The length
    # follows any secondary-compressor ID and uses big-endian base-128 digits.
    start = 5 + (flags & 1)
    length = 0
    for index in range(start, min(start + 5, len(data))):
        part = data[index]
        length = (length << 7) | (part & 0x7f)
        if part < 0x80:
            end = index + 1 + length
            if end >= len(data):
                break
            header = data[:4] + bytes([flags & ~0x04]) + data[5:start]
            path.write_bytes(header + data[end:])
            return
    raise ValueError(f"Invalid xdelta application header: {path.name}")


def prepare(
    romfs: Path, overlay: Path, inventory: Path, release_dir: Path, version: str,
) -> int:
    release_dir = release_dir.resolve()
    if release_dir.exists():
        raise ValueError(f"Choose a new release directory: {release_dir}")
    verified_overlay = json.loads(inventory.read_text(encoding="utf-8"))
    expected = verified_overlay["mod_files"]
    official_version = verified_overlay["switch_version"]
    if official_version != "1.0.2":
        raise ValueError(f"Expected a verified v1.0.2 overlay, received {official_version}")
    if not expected:
        raise ValueError("The overlay inventory has no payloads")

    release_dir.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".dk4-release-", dir=release_dir.parent) as scratch:
        root = Path(scratch) / "release"
        entries = []
        for raw, checksum in sorted(expected.items()):
            is_ips = raw.startswith("exefs/") and raw.endswith(".ips")
            path = relative_path(raw, "exefs" if is_ips else "romfs")
            original = overlay / path
            verify(original, checksum, f"QA overlay {raw}")
            payload = PurePosixPath("patches") / path
            entry = {"output": raw, "output_sha256": checksum}
            if is_ips:
                target = root / payload
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(original, target)
                entry["format"] = "ips"
            else:
                source = romfs / PurePosixPath(*path.parts[1:])
                payload = payload.with_name(payload.name + ".xdelta")
                target = root / payload
                entry.update(format="xdelta", source_sha256=digest(source))
                make_xdelta(source, original, target)
                strip_application_header(target)
            entry.update(patch=payload.as_posix(), patch_sha256=digest(target))
            entries.append(entry)

        manifest = {
            "schema": 1,
            "release": version,
            "game_version": official_version,
            "title_id": verified_overlay["title_id"],
            "files": entries,
        }
        manifest_path = root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        rebuild(romfs, Path(scratch) / "verified-overlay", manifest_path)
        if release_dir.exists():
            raise ValueError(f"Another build created the release directory: {release_dir}")
        root.rename(release_dir)
    return len(entries)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--romfs", type=Path, required=True)
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True, help="Verified overlay build report")
    parser.add_argument("--release", type=Path, required=True)
    parser.add_argument("--version", required=True)
    args = parser.parse_args()
    try:
        count = prepare(args.romfs, args.overlay, args.inventory, args.release, args.version)
    except (OSError, ValueError, KeyError, XdeltaError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Packaged and round-trip verified {count} overlay patches.")


if __name__ == "__main__":
    main()
