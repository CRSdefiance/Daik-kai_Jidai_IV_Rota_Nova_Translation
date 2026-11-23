"""Clear verified redundant outputs from the completed dialogue checkpoint."""
from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path
import re

from scripts import register_rafael_mediterranean_dialogue_20261121 as release


base, stage, live = release.base, release.stage, release.live
FRAME = re.compile(r"frame_\d{6}_(?:cold_boot|final)\.png")


def main():
    target = release.ROOT / "checkpoint_cleanup.json"
    assert not target.exists()
    deployed = base.load(release.RELEASE)
    state = base.load(release.VERIFY / "registration_mutation_plan.json")
    candidate = deployed["candidate_sha256"]
    assert base.digest(release.ROM) == base.digest(stage.ROM) == candidate
    assert base.digest(release.PATCH) == deployed["patch_sha256"]
    assert base.digest(release.MANIFEST) == deployed["manifest_sha256"]
    assert base.digest(base.LEDGER) == state["ledger_after"]
    assert base.digest(base.REGISTRY) == state["registry_after"]
    assert base.digest(base.PROMOTED) == state["main_sha256"]
    drive = base.load(release.ROOT / "drive_latest_build_receipt.json")
    assert drive["sole_nds_in_folder"] and drive["readback_verified"] and drive["sha256"] == candidate

    gameplay = base.load(live.PROOF)
    assert gameplay["candidate_sha256"] == candidate
    holds = [row["observed"] for row in gameplay["holds"]] + [row["final_hold"] for row in gameplay["cases"]]
    keep = {Path(row["path"]).resolve(): row["PNG_sha256"] for row in holds}
    for sheet in gameplay["sheets"]:
        keep[Path(sheet["path"]).resolve()] = sheet["sha256"]
    discard = {}
    for case in gameplay["cases"]:
        folder = live.replay.ROOT / f"B{case['block']}"
        report = folder / "capture/capture_report.json"
        root = report.parent.resolve()
        assert root.is_relative_to(live.replay.ROOT.resolve())
        assert base.digest(report) == gameplay["evidence"][str(report)]
        for row in base.load(report)["frames_captured"]:
            path = Path(row["path"]).resolve()
            assert path.parent == root and FRAME.fullmatch(path.name)
            if path not in keep:
                discard[path] = row["PNG_sha256"]

    with open_gzip(release.ROOT / "editorial_ledger_before.json.gz", "rb") as snapshot:
        assert file_digest(snapshot, "sha256").hexdigest() == state["ledger_before"]
    for name, digest in (("ledger_before.json", state["ledger_before"]), ("ledger_after.json", state["ledger_after"]),
                         ("release_stack_with_rafael_mediterranean_dialogue.json", state["registry_after"])):
        path = (release.ROOT / name).resolve()
        assert path.parent == release.ROOT.resolve()
        discard[path] = digest
    rebuilt = (stage.ROOT / "clean_rebuilt.nds").resolve()
    assert rebuilt.parent == stage.ROOT.resolve()
    discard[rebuilt] = candidate
    test_root = (stage.ROOT / "pytest_tmp").resolve()
    assert test_root.parent == stage.ROOT.resolve()
    test_outputs = {"change.xdelta", "clean.dat", "modified.dat", "rebuilt.dat", "release_manifest.json", "wrong.dat"}
    for fixture in test_root.glob("test_*/*"):
        path = fixture.resolve()
        if path.parent.parent == test_root and path.name in test_outputs:
            discard[path] = base.digest(path)
    for case in (*map(str, live.replay.CASES), "startup", "patch"):
        for stream in ("out", "err"):
            log = (stage.review.ROOT / f"{case}.{stream}.log").resolve()
            if log.parent == stage.review.ROOT.resolve() and log.is_file() and log.stat().st_size == 0:
                discard[log] = base.digest(log)

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
