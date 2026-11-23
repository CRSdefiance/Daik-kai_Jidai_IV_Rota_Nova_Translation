"""Reclaim disposable Alexandria replay captures and non-ROM staging files."""
from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path
import re

from scripts import register_hodram_alexandria_tutorial_20261121 as release


base, stage = release.base, release.stage
CAPTURE_NAME = re.compile(r"frame_\d{6}_(?:cold_boot\.png|arm9_ram\.bin)")
TEST_FILES = {"change.xdelta", "clean.dat", "modified.dat", "rebuilt.dat", "release_manifest.json", "wrong.dat"}


def main():
    target = release.ROOT / "checkpoint_cleanup.json"
    assert not target.exists()
    registered = base.load(release.RELEASE)
    state = base.load(release.VERIFY / "registration_mutation_plan.json")
    drive = base.load(release.ROOT / "drive_latest_build_receipt.json")
    candidate = registered["candidate_sha256"]
    assert drive["sole_nds_in_folder"] and drive["readback_verified"] and drive["sha256"] == candidate
    assert base.digest(base.LEDGER) == state["ledger_after"]
    assert base.digest(base.REGISTRY) == state["registry_after"]
    assert base.digest(base.PROMOTED) == state["main_sha256"]

    keep = {release.ROM: candidate, stage.ROM: candidate, release.PATCH: registered["patch_sha256"],
            release.MANIFEST: registered["manifest_sha256"]}
    for proof in (release.display.PROOF, release.live.PROOF):
        evidence = base.load(proof)
        assert evidence["candidate_sha256"] == candidate
        for sheet in evidence["sheets"]:
            keep[Path(sheet["path"])] = sheet["sha256"]
    gameplay = base.load(release.live.PROOF)
    for evidence in (release.live.replay.REPORT, release.live.replay.BASELINE):
        keep[evidence] = gameplay["evidence"][str(evidence)]
    for row in gameplay["holds"]:
        hold = row["observed"]
        keep[Path(hold["path"])] = hold["PNG_sha256"]

    with open_gzip(release.ROOT / "editorial_ledger_before.json.gz", "rb") as snapshot:
        assert file_digest(snapshot, "sha256").hexdigest() == state["ledger_before"]
    discard = {release.ROOT / name: digest for name, digest in (
        ("ledger_before.json", state["ledger_before"]), ("ledger_after.json", state["ledger_after"]),
        ("release_stack_with_hodram_alexandria_tutorial.json", state["registry_after"]))}
    detail = stage.ROOT / "voyage/R0132_detail.png"
    if detail.is_file():
        discard[detail] = base.digest(detail)
    for version in ("staged", "staged_v2", "staged_v3", "staged_v4"):
        folder = stage.ROOT.parent / version
        assert folder.resolve().parent == stage.ROOT.parent.resolve()
        rom = folder / stage.ROM.name
        digest = base.load(folder / stage.PROOF.name)["candidate_sha256"]
        keep[rom] = digest
        rebuilt = folder / "clean_rebuilt.nds"
        if rebuilt.exists():
            keep[rebuilt] = digest
        for artifact in (folder / "pytest_tmp").glob("test_*/*"):
            if artifact.name in TEST_FILES and artifact.resolve().parent.parent == (folder / "pytest_tmp").resolve():
                discard[artifact] = base.digest(artifact)
        if folder == stage.ROOT:
            continue
        for report_file in folder.glob("*/capture/capture_report.json"):
            report = base.load(report_file)
            assert report["ROM_sha256"] == digest
            for row in report["frames_captured"] + [report["read_only_RAM_snapshot"]]:
                artifact = Path(row["path"])
                if CAPTURE_NAME.fullmatch(artifact.name):
                    assert artifact.resolve().parent == report_file.parent.resolve()
                    discard[artifact] = row.get("PNG_sha256") or row["sha256"]

    assert {p.resolve() for p in keep}.isdisjoint(p.resolve() for p in discard)
    assert all(base.digest(path) == digest for path, digest in keep.items())
    allowed = (release.ROOT.resolve(), stage.ROOT.parent.resolve())
    removed = []
    for path, digest in discard.items():
        assert any(path.resolve().is_relative_to(root) for root in allowed)
        assert path.suffix.lower() != ".nds"
        assert path.is_file() and not path.is_symlink() and not path.is_junction()
        assert base.digest(path) == digest, path
        removed.append(dict(path=str(path), sha256=digest, bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(path) == digest for path, digest in keep.items())
    reclaimed = sum(row["bytes"] for row in removed)
    base.save(target, dict(removed=removed, reclaimed_bytes=reclaimed,
                           registered_candidate_sha256=candidate, retained_checks=len(keep)))
    print(f"Removed {len(removed)} redundant files and reclaimed {reclaimed:,} bytes.")


if __name__ == "__main__":
    main()
