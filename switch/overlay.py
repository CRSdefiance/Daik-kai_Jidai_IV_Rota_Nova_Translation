"""Build a Switch LayeredFS overlay from the v1.0.2 RomFS and release deltas."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shutil
from tempfile import TemporaryDirectory

from dk4tool.patch.xdelta import XdeltaError, apply_xdelta


CURRENT_RELEASE = Path(__file__).resolve().parent / "releases" / "v90" / "manifest.json"
SHA256 = re.compile(r"[a-f0-9]{64}")


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify(path: Path, expected: str, description: str) -> None:
    if not SHA256.fullmatch(expected):
        raise ValueError(f"Invalid SHA-256 for {description}")
    if not path.is_file():
        raise ValueError(f"Missing {description}: {path}")
    observed = digest(path)
    if observed != expected:
        raise ValueError(f"Unexpected SHA-256 for {description}: {observed}")


def relative_path(raw: str, root: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if (
        path.as_posix() != raw
        or "\\" in raw
        or ":" in raw
        or ".." in path.parts
        or len(path.parts) < 2
        or path.parts[0] != root
    ):
        raise ValueError(f"Expected a path below {root}: {raw!r}")
    return path


def load_release(path: Path) -> dict:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest["schema"] != 1 or manifest["game_version"] != "1.0.2":
        raise ValueError("Unsupported Switch release manifest")
    return manifest


def rebuild(romfs: Path, output: Path, manifest_path: Path = CURRENT_RELEASE) -> int:
    romfs = romfs.resolve()
    output = output.resolve()
    if not romfs.is_dir():
        raise ValueError(f"Expected the extracted RomFS directory: {romfs}")
    if output.exists() or output == romfs or romfs in output.parents:
        raise ValueError(f"Choose a new overlay directory outside the original RomFS: {output}")

    manifest = load_release(manifest_path)
    release_dir = manifest_path.resolve().parent
    entries = []
    destinations = set()
    for row in manifest["files"]:
        kind = row["format"]
        if kind not in {"ips", "xdelta"}:
            raise ValueError(f"Unsupported overlay patch format: {kind!r}")
        relative = relative_path(row["output"], "exefs" if kind == "ips" else "romfs")
        key = relative.as_posix().casefold()
        if key in destinations:
            raise ValueError(f"Duplicate overlay path: {relative}")
        destinations.add(key)
        patch = release_dir / relative_path(row["patch"], "patches")
        verify(patch, row["patch_sha256"], f"release patch {relative}")
        source = None
        if kind == "xdelta":
            source = romfs / PurePosixPath(*relative.parts[1:])
            verify(source, row["source_sha256"], f"stock RomFS v1.0.2 file {relative}")
        entries.append((relative, source, patch, row["output_sha256"]))

    if not entries:
        raise ValueError("The release manifest has no overlay files")

    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".dk4-switch-", dir=output.parent) as scratch:
        staging = Path(scratch) / "overlay"
        for relative, source, patch, expected in entries:
            target = staging / relative
            if source is None:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(patch, target)
            else:
                apply_xdelta(source, patch, target)
            verify(target, expected, f"built overlay {relative}")
        if output.exists():
            raise ValueError(f"Another build created the output directory: {output}")
        staging.rename(output)
    return len(entries)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--romfs", type=Path, required=True, help="Your extracted Japanese v1.0.2 RomFS")
    parser.add_argument("--output", type=Path, required=True, help="A new directory for exefs and romfs")
    parser.add_argument("--manifest", type=Path, default=CURRENT_RELEASE)
    args = parser.parse_args()
    try:
        count = rebuild(args.romfs, args.output, args.manifest)
    except (OSError, ValueError, KeyError, XdeltaError) as error:
        parser.exit(1, f"{error}\n")
    print(f"Built and verified {count} overlay files in {args.output.resolve()}")


if __name__ == "__main__":
    main()
