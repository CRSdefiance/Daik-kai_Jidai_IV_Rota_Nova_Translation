"""Clear disposable files from the original Stockholm and registered fleet runs."""
from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path
import re

from scripts import register_numbered_fleet_spacing_20261121 as fleet
from scripts import verify_stockholm_december_20261121 as stockholm


base = fleet.base
FRAME = re.compile(r"frame_\d{6}_(cold_boot|navigation|final)\.png")


def main():
    receipt = fleet.ROOT / "checkpoint_cleanup.json"
    assert not receipt.exists()
    town_proof, map_proof, prepared, release, startup = map(base.load,(
        stockholm.OUTPUT,fleet.live.PROOF,fleet.stage.PROOF,fleet.RELEASE,fleet.STARTUP))
    assert base.digest(fleet.ROM) == base.digest(fleet.stage.ROM) == release["candidate_sha256"]
    assert base.digest(fleet.PATCH) == release["patch_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    verified_drive = base.load(fleet.ROOT / "drive_latest_build_receipt.json")
    assert verified_drive["readback_verified"] and verified_drive["sha256"] == release["candidate_sha256"]
    retained = [*town_proof["calendar_and_voyage_holds"],*town_proof["separate_Tavern_tutorial_frames"],
        *[p["observed"] for p in town_proof["complete_fur_exchange"]],town_proof["Square_return"],
        *map_proof["observations"]]
    routes = [
        (stockholm.REPORT,town_proof["evidence"][str(stockholm.REPORT)]),
        (fleet.live.replay.REPORT,map_proof["evidence"][str(fleet.live.replay.REPORT)]),
        (fleet.STARTUP_CAPTURE,startup["evidence"][str(fleet.STARTUP_CAPTURE)]),
    ]
    manual = fleet.stage.play.ROOT / "capture/capture_report.json"
    routes.append((manual,prepared["evidence"][str(manual)]))
    auto = fleet.stage.play.ROOT / "auto_move/capture/capture_report.json"
    routes.append((auto,None))
    remove = {}
    for path,digest in routes:
        if digest:
            assert base.digest(path) == digest
        report = base.load(path)
        root = path.parent.resolve()
        assert root.is_relative_to(fleet.stage.play.ROOT.resolve()) or root.is_relative_to(fleet.EVIDENCE.resolve())
        assert report["frames"] > 0 and not report["callback_errors"]
        if path == fleet.STARTUP_CAPTURE:
            # Future registered helpers check every frame in the startup manifest.
            retained.extend(report["frames_captured"])
        if path == auto:
            assert report["frames"] == 9140
            retained.extend(f for f in report["frames_captured"] if f["frame"] in (5760,6370,8230,8820))
        keep_paths = {Path(row["path"]).resolve() for row in retained}
        for shot in report["frames_captured"]:
            image=Path(shot["path"]).resolve()
            assert image.parent == root and FRAME.fullmatch(image.name)
            if image not in keep_paths:
                remove[image] = shot["PNG_sha256"]
        donor = report["battery_save_preloaded"]
        assert base.digest(donor["source"]) == donor["source_sha256"]
        clone = Path(donor["destination"]).resolve()
        assert clone.parent == root / "saves" and clone.suffix.lower()==".dsv"
        if clone.is_file() and base.digest(clone)==donor["source_sha256"]:
            remove[clone]=donor["source_sha256"]
    for shot in retained:
        assert base.digest(shot["path"]) == shot["PNG_sha256"]

    mutation = base.load(fleet.VERIFY / "registration_mutation_plan.json")
    for name,path,digest in (
        ("release_stack_with_numbered_fleet_spacing.json",base.REGISTRY,mutation["registry_after"]),
        ("ledger_after.json",base.LEDGER,mutation["ledger_after"]),
    ):
        assert base.digest(path)==digest
        duplicate=(fleet.ROOT/name).resolve()
        assert duplicate.parent==fleet.ROOT.resolve()
        remove[duplicate]=digest
    ledger=(fleet.ROOT/"ledger_before.json").resolve()
    with open_gzip(fleet.ROOT/"editorial_ledger_before.json.gz","rb") as snapshot:
        assert file_digest(snapshot,"sha256").hexdigest() == mutation["ledger_before"]
    assert ledger.parent==fleet.ROOT.resolve()
    remove[ledger]=mutation["ledger_before"]
    rebuilt=(fleet.EVIDENCE/"clean_rebuilt.nds").resolve()
    assert rebuilt.parent==fleet.EVIDENCE.resolve()
    remove[rebuilt]=release["candidate_sha256"]
    files = []
    for path,digest in remove.items():
        assert path.is_file() and not path.is_symlink() and not path.is_junction()
        assert base.digest(path)==digest
        files.append(dict(path=str(path),sha256=digest,bytes=path.stat().st_size))
    for path in remove:
        path.unlink()
    assert base.digest(fleet.ROM) == release["candidate_sha256"]
    assert all(base.digest(row["path"])==row["PNG_sha256"] for row in retained)
    total=sum(row["bytes"] for row in files)
    base.save(receipt,dict(reclaimed_bytes=total,removed=files,retained_review_frames=len(retained)))
    print(f"Removed {len(files)} disposable files and reclaimed {total:,} bytes.")


if __name__ == "__main__":
    main()
