from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

from dk4tool import __version__
from dk4tool.insert.fixed_length import replace_fixed
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.hashing import hash_bytes, hash_file
from dk4tool.rom.manifest import build_manifest
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.ascii_scan import scan_ascii
from dk4tool.scan.compression_probe import decompress_lz10, is_lz10
from dk4tool.scan.entropy import shannon_entropy
from dk4tool.scan.sjis_scan import scan_sjis
from dk4tool.scan.utf16_scan import scan_utf16le
from dk4tool.script.arm9_profiles import export_profile_rows, profile_names
from dk4tool.script.export_csv import write_script_csv
from dk4tool.script.import_csv import read_script_csv
from dk4tool.script.mesfile import analyze_mesfile, export_mesfile_rows, rebuild_mesfile
from dk4tool.script.validate import normalize_encoding, validate_rows


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def command_info(args: argparse.Namespace) -> None:
    image = NdsImage.open(args.rom)
    print(json.dumps({**image.metadata(), **hash_file(args.rom)}, ensure_ascii=False, indent=2))


def command_manifest(args: argparse.Namespace) -> None:
    write_json(args.out, build_manifest(NdsImage.open(args.rom)))


def command_extract_files(args: argparse.Namespace) -> None:
    root = args.out.resolve()
    for _, rom_path, data in NdsImage.open(args.rom).iter_files():
        destination = (root / rom_path.lstrip("/")).resolve()
        if root not in destination.parents:
            raise ValueError(f"unsafe ROM path: {rom_path}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)


def command_resave(args: argparse.Namespace) -> None:
    NdsImage.open(args.rom).save(args.out)


def scan_image(
    image: NdsImage,
    aggressive: bool,
    includes: list[str] | None = None,
    max_hits_per_file: int = 20_000,
) -> dict[str, object]:
    results = []
    for file_id, path, data in image.iter_files():
        if includes and not any(fnmatch.fnmatchcase(path, pattern) for pattern in includes):
            continue
        scan_data = data
        compression = None
        error = None
        if is_lz10(data):
            try:
                scan_data = decompress_lz10(data)
                compression = "lz10"
            except ValueError as caught:
                error = str(caught)
        minimum_score = 0.0 if aggressive else 0.8
        sjis_all = [
            hit.to_dict()
            for hit in scan_sjis(scan_data, aggressive=aggressive)
            if hit.score >= minimum_score
        ]
        sjis_ranges = [
            (hit["offset"], hit["offset"] + hit["length"])
            for hit in sjis_all
        ]
        utf16_all = [
            hit.to_dict()
            for hit in scan_utf16le(scan_data, aggressive=aggressive)
            if hit.score >= minimum_score
            and not any(
                hit.offset < sjis_end and hit.offset + hit.length > sjis_start
                for sjis_start, sjis_end in sjis_ranges
            )
        ]
        ascii_all = [hit.to_dict() for hit in scan_ascii(scan_data)]
        truncated = any(
            len(hits) > max_hits_per_file for hits in (sjis_all, utf16_all, ascii_all)
        )
        sjis = sjis_all[:max_hits_per_file]
        utf16 = utf16_all[:max_hits_per_file]
        ascii_hits = ascii_all[:max_hits_per_file]
        score = round(
            min(1.0, sum(hit["score"] for hit in sjis + utf16) / max(1, len(sjis + utf16))),
            3,
        )
        results.append(
            {
                "id": file_id,
                "file_path": path,
                "file_size": len(data),
                "scan_size": len(scan_data),
                "entropy": round(shannon_entropy(data), 6),
                "compression": compression,
                "compression_error": error,
                "sjis_hits": sjis,
                "utf16_hits": utf16,
                "ascii_hits": ascii_hits,
                "hits_truncated": truncated,
                "score": score,
            }
        )
    if includes:
        existing_paths = {item["file_path"] for item in results}
        for path, data in image.iter_components():
            if path in existing_paths or not any(
                fnmatch.fnmatchcase(path, pattern) for pattern in includes
            ):
                continue
            sjis = [
                hit.to_dict()
                for hit in scan_sjis(data, aggressive=aggressive)
                if hit.score >= (0.0 if aggressive else 0.8)
            ][:max_hits_per_file]
            utf16 = [
                hit.to_dict()
                for hit in scan_utf16le(data, aggressive=aggressive)
                if hit.score >= (0.0 if aggressive else 0.8)
            ][:max_hits_per_file]
            results.append(
                {
                    "id": None,
                    "file_path": path,
                    "file_size": len(data),
                    "scan_size": len(data),
                    "entropy": round(shannon_entropy(data), 6),
                    "compression": None,
                    "compression_error": None,
                    "sjis_hits": sjis,
                    "utf16_hits": utf16,
                    "ascii_hits": [
                        hit.to_dict() for hit in scan_ascii(data)
                    ][:max_hits_per_file],
                    "hits_truncated": len(sjis) >= max_hits_per_file
                    or len(utf16) >= max_hits_per_file,
                    "score": round(
                        sum(hit["score"] for hit in sjis + utf16)
                        / max(1, len(sjis + utf16)),
                        3,
                    ),
                }
            )
    results.sort(key=lambda item: (-item["score"], item["file_path"]))
    return {"mode": "aggressive" if aggressive else "conservative", "files": results}


def write_scan_summary(path: Path, report: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        columns = [
            "file_path",
            "file_size",
            "entropy",
            "sjis_hits",
            "utf16_hits",
            "ascii_hits",
            "lz10_detected",
            "score",
            "notes",
        ]
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for item in report["files"]:
            writer.writerow(
                {
                    "file_path": item["file_path"],
                    "file_size": item["file_size"],
                    "entropy": item["entropy"],
                    "sjis_hits": len(item["sjis_hits"]),
                    "utf16_hits": len(item["utf16_hits"]),
                    "ascii_hits": len(item["ascii_hits"]),
                    "lz10_detected": item["compression"] == "lz10",
                    "score": item["score"],
                    "notes": item["compression_error"] or "",
                }
            )


def command_scan(args: argparse.Namespace) -> None:
    report = scan_image(
        NdsImage.open(args.rom),
        args.mode == "aggressive",
        args.include,
        args.max_hits_per_file,
    )
    write_json(args.out, report)
    summary = args.out.with_name("scan_summary.csv")
    write_scan_summary(summary, report)


def _stable_id(path: str, offset: int, raw: bytes) -> str:
    digest = hashlib.sha1(path.encode() + b"\0" + str(offset).encode() + b"\0" + raw).hexdigest()
    return "DK4_" + digest[:12].upper()


def command_extract_script(args: argparse.Namespace) -> None:
    image = NdsImage.open(args.rom)
    report = scan_image(
        image,
        args.mode == "aggressive",
        args.include,
        args.max_hits_per_file,
    )
    file_data = {path: data for _, path, data in image.iter_files()}
    file_data.update(dict(image.iter_components()))
    rows: list[dict[str, object]] = []
    metadata = []
    for item in report["files"]:
        if item["compression"]:
            continue  # decompressed insertion requires recompression and is intentionally deferred
        data = file_data[item["file_path"]]
        candidates = sorted(
            item["sjis_hits"] + item["utf16_hits"],
            key=lambda hit: (-hit["score"], hit["offset"], -hit["length"]),
        )
        selected = []
        occupied: list[tuple[int, int]] = []
        for hit in candidates:
            start, end = hit["offset"], hit["offset"] + hit["length"]
            if any(start < used_end and end > used_start for used_start, used_end in occupied):
                continue
            selected.append(hit)
            occupied.append((start, end))
        for hit in sorted(selected, key=lambda value: value["offset"]):
            raw = data[hit["offset"] : hit["offset"] + hit["length"]]
            row_id = _stable_id(item["file_path"], hit["offset"], raw)
            rows.append(
                {
                    "id": row_id,
                    "file_path": item["file_path"],
                    "container_path": "",
                    "encoding": hit["encoding"],
                    "source_offset": hit["offset"],
                    "source_length": hit["length"],
                    "source_hex": raw.hex().upper(),
                    "japanese": hit["decoded"],
                    "english": "",
                    "status": "untranslated",
                    "context": "",
                    "speaker": "",
                    "notes": f"confidence={hit['score']}",
                    "max_bytes": hit["length"],
                    "allow_expand": "false",
                    "pointer_group": "",
                    "control_profile": "default",
                    "wrap_width": 32,
                }
            )
            metadata.append(
                {
                    "id": row_id,
                    "file_path": item["file_path"],
                    "source_offset": hit["offset"],
                    "source_length": hit["length"],
                    "terminator": hit["terminator"],
                    "raw_bytes": raw.hex().upper(),
                    "encoding": hit["encoding"],
                    "decoded": hit["decoded"],
                    "control_codes": [],
                    "pointer_refs": [],
                    "block_id": None,
                    "max_bytes": hit["length"],
                    "allow_expand": False,
                    "in_compressed_file": False,
                    "compression": None,
                }
            )
    rows.sort(key=lambda row: (row["file_path"], row["source_offset"], row["id"]))
    metadata.sort(key=lambda row: (row["file_path"], row["source_offset"], row["id"]))
    write_script_csv(args.out, rows)
    write_json(args.out.with_name("script_meta.json"), {"entries": metadata})


def command_extract_arm9_profile(args: argparse.Namespace) -> None:
    image = NdsImage.open(args.rom)
    rows = export_profile_rows(image.read_file("/__arm9__.bin"), args.profile, args.with_drafts)
    write_script_csv(args.out, rows)


def command_extract_mesfile(args: argparse.Namespace) -> None:
    image = NdsImage.open(args.rom)
    data = image.read_file(args.file_path)
    rows = export_mesfile_rows(data, args.file_path)
    write_script_csv(args.out, rows)
    write_json(
        args.out.with_name("mesfile_meta.json"),
        {
            "file_path": args.file_path,
            "source_sha256": hash_bytes(data)["sha256"],
            **analyze_mesfile(data),
        },
    )


def command_validate_script(args: argparse.Namespace) -> None:
    issues = validate_rows(read_script_csv(args.script))
    print(json.dumps([issue.to_dict() for issue in issues], ensure_ascii=False, indent=2))
    if any(issue.severity == "error" for issue in issues):
        raise SystemExit(1)


def command_insert_script(args: argparse.Namespace) -> None:
    rows = read_script_csv(args.script)
    issues = validate_rows(rows)
    errors = [issue for issue in issues if issue.severity == "error"]
    if errors:
        print(json.dumps([issue.to_dict() for issue in errors], ensure_ascii=False, indent=2))
        raise SystemExit(1)
    image = NdsImage.open(args.rom)
    by_path: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row["english"]:
            by_path.setdefault(row["file_path"], []).append(row)
    if args.mode == "ilnk":
        for path, changes in by_path.items():
            image.replace_file(path, rebuild_mesfile(image.read_file(path), changes))
        image.save(args.out)
        return
    for path, changes in by_path.items():
        data = image.read_file(path)
        occupied: list[tuple[int, int]] = []
        for row in sorted(changes, key=lambda item: int(item["source_offset"])):
            offset = int(row["source_offset"])
            length = int(row["source_length"])
            if any(offset < end and offset + length > start for start, end in occupied):
                raise ValueError(f"{row['id']}: replacement overlaps another row")
            expected = bytes.fromhex(row["source_hex"])
            if data[offset : offset + length] != expected:
                raise ValueError(f"{row['id']}: source bytes do not match the supplied ROM")
            replacement = row["english"].encode(normalize_encoding(row["encoding"]))
            data = replace_fixed(data, offset, length, replacement)
            occupied.append((offset, offset + length))
        image.replace_file(path, data)
    image.save(args.out)


def command_compare(args: argparse.Namespace) -> None:
    left = NdsImage.open(args.clean)
    right = NdsImage.open(args.modified)
    left_files = {path: data for _, path, data in left.iter_files()}
    right_files = {path: data for _, path, data in right.iter_files()}
    left_files.update(dict(left.iter_components()))
    right_files.update(dict(right.iter_components()))
    paths = sorted(set(left_files) | set(right_files))
    changes = []
    for path in paths:
        before, after = left_files.get(path), right_files.get(path)
        if before != after:
            changes.append(
                {
                    "path": path,
                    "status": "added" if before is None else "removed" if after is None else "changed",
                    "before": None if before is None else {"size": len(before), **hash_bytes(before)},
                    "after": None if after is None else {"size": len(after), **hash_bytes(after)},
                }
            )
    report = {
        "clean": {"path": str(args.clean), **hash_file(args.clean)},
        "modified": {"path": str(args.modified), **hash_file(args.modified)},
        "file_count_equal": len(left_files) == len(right_files),
        "changed_files": changes,
    }
    write_json(args.out, report)


def command_make_xdelta(args: argparse.Namespace) -> None:
    make_xdelta(args.clean, args.modified, args.out)
    manifest = {
        "game": "Daikoukai Jidai IV / Rota Nova DS",
        "patch_version": __version__,
        "source_rom_sha256": hash_file(args.clean)["sha256"],
        "modified_rom_sha256": hash_file(args.modified)["sha256"],
        "patch_sha256": hash_file(args.out)["sha256"],
        "created_at": datetime.now(UTC).isoformat(),
        "tool_version": __version__,
        "notes": "Generated locally. Do not distribute ROM.",
    }
    write_json(args.out.with_name("release_manifest.json"), manifest)


def command_apply_xdelta(args: argparse.Namespace) -> None:
    manifest_path = args.patch.with_name("release_manifest.json")
    manifest = None
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        expected_source = manifest.get("source_rom_sha256")
        actual_source = hash_file(args.clean)["sha256"]
        if expected_source and actual_source.lower() != expected_source.lower():
            raise ValueError(
                "source ROM SHA-256 does not match release manifest: "
                f"expected {expected_source}, found {actual_source}"
            )
    apply_xdelta(args.clean, args.patch, args.out)
    if manifest:
        expected_target = manifest.get("modified_rom_sha256")
        actual_target = hash_file(args.out)["sha256"]
        if expected_target and actual_target.lower() != expected_target.lower():
            raise ValueError(
                "rebuilt ROM SHA-256 does not match release manifest: "
                f"expected {expected_target}, found {actual_target}"
            )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="dk4tool")
    root.add_argument("--version", action="version", version=__version__)
    commands = root.add_subparsers(dest="command", required=True)

    def output_command(name: str, function, first: str = "rom") -> argparse.ArgumentParser:
        command = commands.add_parser(name)
        command.add_argument(first, type=Path)
        command.add_argument("--out", type=Path, required=True)
        command.set_defaults(function=function)
        return command

    info = commands.add_parser("info")
    info.add_argument("rom", type=Path)
    info.set_defaults(function=command_info)
    output_command("manifest", command_manifest)
    output_command("extract-files", command_extract_files)
    output_command("resave", command_resave)
    scan = output_command("scan", command_scan)
    scan.add_argument("--mode", choices=("conservative", "aggressive"), default="conservative")
    scan.add_argument(
        "--include",
        action="append",
        help="Only scan matching internal POSIX paths; may be repeated (for example /data/SC*.DK4)",
    )
    scan.add_argument("--max-hits-per-file", type=int, default=20_000)
    extract = output_command("extract-script", command_extract_script)
    extract.add_argument("--mode", choices=("conservative", "aggressive"), default="conservative")
    extract.add_argument(
        "--include",
        action="append",
        help="Only export matching internal POSIX paths; may be repeated",
    )
    extract.add_argument("--max-hits-per-file", type=int, default=20_000)
    arm9_profile = output_command("extract-arm9-profile", command_extract_arm9_profile)
    arm9_profile.add_argument("--profile", choices=profile_names(), default="all")
    arm9_profile.add_argument(
        "--with-drafts",
        action="store_true",
        help="Populate English cells with the profile's draft translations",
    )
    mesfile = output_command("extract-mesfile", command_extract_mesfile)
    mesfile.add_argument("--file-path", default="/COMMON/MESFILE.DK4")
    validate = commands.add_parser("validate-script")
    validate.add_argument("script", type=Path)
    validate.set_defaults(function=command_validate_script)
    insert = commands.add_parser("insert-script")
    insert.add_argument("rom", type=Path)
    insert.add_argument("script", type=Path)
    insert.add_argument("--out", type=Path, required=True)
    insert.add_argument("--mode", choices=("fixed", "ilnk"), default="fixed")
    insert.set_defaults(function=command_insert_script)
    compare = commands.add_parser("compare")
    compare.add_argument("clean", type=Path)
    compare.add_argument("modified", type=Path)
    compare.add_argument("--out", type=Path, required=True)
    compare.set_defaults(function=command_compare)
    create_patch = commands.add_parser("make-xdelta")
    create_patch.add_argument("clean", type=Path)
    create_patch.add_argument("modified", type=Path)
    create_patch.add_argument("--out", type=Path, required=True)
    create_patch.set_defaults(function=command_make_xdelta)
    apply_patch = commands.add_parser("apply-xdelta")
    apply_patch.add_argument("clean", type=Path)
    apply_patch.add_argument("patch", type=Path)
    apply_patch.add_argument("--out", type=Path, required=True)
    apply_patch.set_defaults(function=command_apply_xdelta)
    return root


def main(argv: list[str] | None = None) -> int:
    try:
        args = parser().parse_args(argv)
        args.function(args)
        return 0
    except (OSError, RuntimeError, ValueError, KeyError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
