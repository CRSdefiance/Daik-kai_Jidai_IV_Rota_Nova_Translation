"""Remove validated scratch captures and duplicate release staging files."""
from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path
import re

from scripts import checkpoint_hodram_alexandria_arrival_20261121 as arrival
from scripts import register_alexandria_dialogue_20261121 as release


base, stage, live = release.base, release.stage, release.live
FRAME = re.compile(r"frame_\d{6}_(?:navigation|cold_boot|final)\.png")
RAM = re.compile(r"frame_\d{6}_arm9_ram\.bin")


def main():
    target = release.ROOT / "checkpoint_cleanup.json"
    assert not target.exists()
    registered = base.load(release.RELEASE)
    state = base.load(release.VERIFY / "registration_mutation_plan.json")
    candidate = registered["candidate_sha256"]
    assert base.digest(release.ROM) == base.digest(stage.ROM) == candidate
    assert base.digest(release.PATCH) == registered["patch_sha256"]
    assert base.digest(release.MANIFEST) == registered["manifest_sha256"]
    assert base.digest(base.LEDGER) == state["ledger_after"]
    assert base.digest(base.REGISTRY) == state["registry_after"]
    assert base.digest(base.PROMOTED) == state["main_sha256"]
    drive = base.load(release.ROOT / "drive_latest_build_receipt.json")
    assert drive["sole_nds_in_folder"] and drive["readback_verified"] and drive["sha256"] == candidate

    gameplay, observed, tutorial = map(base.load, (live.PROOF, live.replay.OBSERVED, arrival.OUTPUT))
    assert gameplay["candidate_sha256"] == candidate and gameplay["evidence"][str(live.replay.BASELINE)] == tutorial["report_sha256"]
    assert base.digest(live.replay.BASELINE) == observed["report_sha256"] == tutorial["report_sha256"]
    keep_frames = set(observed["panels"]) | set(observed["controls"].values())
    keep_ram = {7090, 8480, 10450, 36880, 41710}
    keep, discard = {}, {}
    baseline = live.replay.BASELINE.parent.resolve()
    root = live.replay.baseline.ROOT.resolve()
    assert baseline.is_relative_to(root)
    report = base.load(live.replay.BASELINE)
    for frame in report["frames_captured"]:
        path = Path(frame["path"]).resolve()
        assert path.parent == baseline and FRAME.fullmatch(path.name)
        # Preserve the original warnings, recruitment, and every captured tutorial page for the next review.
        retain = frame["frame"] in keep_frames or 11620 <= frame["frame"] <= 28120
        (keep if retain else discard)[path] = frame["PNG_sha256"]
    for record in report["read_only_pause_RAM_snapshots"]:
        path = Path(record["path"]).resolve()
        assert path.parent == baseline and RAM.fullmatch(path.name) and record["read_only_export"]
        (keep if record["frame"] in keep_ram else discard)[path] = record["sha256"]
    first = live.replay.baseline.FIRST_ATTEMPT
    first_capture = (first / "capture").resolve()
    assert first_capture.is_relative_to(first.resolve())
    first_report = base.load(first / "capture/capture_report.json")
    assert first_report["ROM_sha256"] == report["ROM_sha256"] and first_report["frames"] == 15100
    for row in first_report["frames_captured"]:
        path = Path(row["path"]).resolve()
        assert path.parent == first_capture and FRAME.fullmatch(path.name)
        (keep if row["frame"] in {7610, 8210, 12010, 15100} else discard)[path] = row["PNG_sha256"]
    for event in (gameplay["source_native_event"], gameplay["staged_native_event"]):
        snapshot = event["read_only_snapshot"]
        keep[Path(snapshot["path"]).resolve()] = snapshot["sha256"]
    for proofs in (gameplay["unchanged_controls"], gameplay["controls"].values(), (r["after"] for r in gameplay["holds"])):
        for row in proofs:
            keep[Path(row["path"]).resolve()] = row["PNG_sha256"]
    for sheet in gameplay["sheets"]:
        keep[Path(sheet["path"]).resolve()] = sheet["sha256"]

    with open_gzip(release.ROOT / "editorial_ledger_before.json.gz", "rb") as snapshot:
        assert file_digest(snapshot, "sha256").hexdigest() == state["ledger_before"]
    for name, digest in (("ledger_before.json", state["ledger_before"]), ("ledger_after.json", state["ledger_after"]),
                         ("release_stack_with_alexandria_dialogue.json", state["registry_after"])):
        path = (release.ROOT / name).resolve()
        assert path.parent == release.ROOT.resolve()
        discard[path] = digest
    rebuilt = (stage.ROOT / "clean_rebuilt.nds").resolve()
    assert rebuilt.parent == stage.ROOT.resolve()
    discard[rebuilt] = candidate
    test_root = (stage.ROOT / "pytest_tmp").resolve()
    assert test_root.parent == stage.ROOT.resolve()
    test_files = {"change.xdelta", "clean.dat", "modified.dat", "rebuilt.dat", "release_manifest.json", "wrong.dat"}
    for artifact in test_root.glob("test_*/*"):
        path = artifact.resolve()
        if path.parent.parent == test_root and path.name in test_files:
            discard[path] = base.digest(path)
    assert keep.keys().isdisjoint(discard)
    assert all(base.digest(path) == digest for path, digest in keep.items())
    removed = []
    for path, digest in discard.items():
        assert path.is_file() and not path.is_symlink() and not path.is_junction()
        assert base.digest(path) == digest
        removed.append(dict(path=str(path), sha256=digest, bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(path) == digest for path, digest in keep.items())
    total = sum(row["bytes"] for row in removed)
    base.save(target, dict(removed=removed, reclaimed_bytes=total, verified_retained_evidence=len(keep),
                           registered_candidate_sha256=candidate))
    print(f"Removed {len(removed)} redundant files and reclaimed {total:,} bytes.")


if __name__ == "__main__":
    main()
