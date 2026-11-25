"""Prune only disposable emulator output after validating all retained evidence."""
from argparse import ArgumentParser
from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path
import re

from scripts import replay_athens_london_trends_20261121 as replay
from scripts import verify_athens_london_trends_replay_20261121 as live
from scripts import register_athens_london_trends_20261121 as registration


base = replay.base
FRAME = re.compile(r"frame_\d{6}_(cold_boot|navigation|final)\.png")


def main(stage):
    original = replay.original
    folder = replay.stage.ROOT if stage else original.runs.ROOT
    receipt = folder / "checkpoint_cleanup.json"
    assert not receipt.exists()
    keep, reports = {}, {}
    if stage:
        release, replayed, startup = map(base.load, (registration.RELEASE, live.PROOF, registration.STARTUP))
        assert base.digest(registration.ROM) == release["candidate_sha256"] == replayed["candidate_sha256"]
        assert base.digest(registration.PATCH) == release["patch_sha256"]
        for row in replayed["holds"]:
            capture = row["snapshot"]
            keep[Path(capture["path"]).resolve()] = capture["PNG_sha256"]
        for city in original.CASES:
            reports[replay.replay_paths(city)[1]] = replayed["evidence"][str(replay.replay_paths(city)[1])]
        reports[registration.STARTUP_CAPTURE] = startup["evidence"][str(registration.STARTUP_CAPTURE)]
        for row in startup["exact_matching_frames"]:
            keep[Path(row["path"]).resolve()] = row["PNG_sha256"]
        for row in replayed["sheets"]:
            keep[Path(row["path"]).resolve()] = row["sha256"]
        # Keep explicitly requested control frames in addition to the checked dialogue.
        for report_path in reports:
            report = base.load(report_path)
            planned = set(report["exact_requested_capture_frames"])
            for row in report["frames_captured"]:
                if row["frame"] in planned and row["path"].endswith("_cold_boot.png"):
                    keep[Path(row["path"]).resolve()] = row["PNG_sha256"]
    else:
        original_proof = base.load(original.OUTPUT)
        for run in original_proof["scene_runs"]:
            for row in [*(p["observed"] for p in run["panels"]), *run["calendar_controls"].values()]:
                keep[Path(row["path"]).resolve()] = row["PNG_sha256"]
            for row in run["sheets"]:
                keep[Path(row["path"]).resolve()] = row["sha256"]
        for row in original_proof["stockholm"]["observed"]:
            keep[Path(row["path"]).resolve()] = row["PNG_sha256"]
        for run in [*original_proof["scene_runs"], original_proof["stockholm"]]:
            report = original.runs.ROOT / run["city"] / "capture/capture_report.json"
            reports[report] = run["evidence"][str(report)]

    for path, digest in keep.items():
        assert path.is_relative_to(folder.resolve()) and base.digest(path) == digest
    cleanup = {}
    for report_path, digest in reports.items():
        assert base.digest(report_path) == digest
        report = base.load(report_path)
        assert report["frames"] > 0 and not report["callback_errors"]
        root = report_path.parent.resolve()
        assert root.is_relative_to(folder.resolve())
        for row in report["frames_captured"]:
            path = Path(row["path"]).resolve()
            if path in keep:
                continue
            assert path.parent == root and FRAME.fullmatch(path.name)
            if path.exists():
                cleanup[path] = row["PNG_sha256"]
        donor = report["battery_save_preloaded"]
        assert base.digest(donor["source"]) == donor["source_sha256"]
        clone = Path(donor["destination"]).resolve()
        assert clone.parent == root / "saves" and clone.suffix.lower() == ".dsv"
        if clone.exists() and base.digest(clone) == donor["source_sha256"]:
            cleanup[clone] = donor["source_sha256"]
    if stage:
        rebuilt = replay.stage.ROOT / "clean_rebuilt.nds"
        assert rebuilt.resolve().parent == folder.resolve()
        assert base.digest(rebuilt) == base.digest(replay.stage.ROM) == release["candidate_sha256"]
        cleanup[rebuilt.resolve()] = release["candidate_sha256"]
        mutation = base.load(registration.VERIFY / "registration_mutation_plan.json")
        for duplicate, canonical, digest in (
            ("release_stack_with_athens_london_trends.json", base.REGISTRY, mutation["registry_after"]),
            ("ledger_after.json", base.LEDGER, mutation["ledger_after"]),
        ):
            assert base.digest(canonical) == digest
            path = (registration.ROOT / duplicate).resolve()
            assert path.parent == registration.ROOT.resolve()
            cleanup[path] = digest
        backup = registration.ROOT / "ledger_before.json"
        with open_gzip(registration.ROOT / "editorial_ledger_before.json.gz", "rb") as snapshot:
            assert file_digest(snapshot, "sha256").hexdigest() == mutation["ledger_before"]
        assert backup.resolve().parent == registration.ROOT.resolve()
        cleanup[backup.resolve()] = mutation["ledger_before"]

    removed = []
    for path, digest in cleanup.items():
        assert path.is_file() and not path.is_symlink() and not path.is_junction() and base.digest(path) == digest
        removed.append(dict(path=str(path), sha256=digest, bytes=path.stat().st_size))
    for path in cleanup:
        path.unlink()
    assert all(base.digest(path) == digest for path, digest in keep.items())
    total = sum(row["bytes"] for row in removed)
    base.save(receipt, dict(removed=removed, reclaimed_bytes=total, verified_retained_files=len(keep)))
    print(f"Removed {len(removed)} disposable files and reclaimed {total:,} bytes.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--stage", action="store_true")
    main(parser.parse_args().stage)
