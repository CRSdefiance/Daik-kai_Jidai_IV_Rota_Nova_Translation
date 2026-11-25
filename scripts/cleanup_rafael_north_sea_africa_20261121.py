"""Remove redundant captures and registration copies after release verification."""

from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path

from scripts import register_rafael_north_sea_africa_20261121 as release


base, stage = release.base, release.stage


def main():
    receipt = release.ROOT / "checkpoint_cleanup.json"
    assert not receipt.exists()
    mutation, manifest, playback, visual, drive = map(base.load, (
        release.VERIFY / "registration_mutation_plan.json", release.RELEASE,
        release.live.PROOF, release.EVIDENCE / "visual_review.json",
        release.ROOT / "drive_latest_build_receipt.json"))
    candidate = manifest["candidate_sha256"]
    assert candidate == playback["candidate_sha256"] == drive["sha256"]
    assert drive["sole_nds_in_folder"] and drive["readback_verified"]
    assert base.digest(base.LEDGER) == mutation["ledger_after"]
    assert base.digest(base.REGISTRY) == mutation["registry_after"] == manifest["registry_sha256"]
    assert base.digest(base.PROMOTED) == mutation["main_sha256"]
    assert base.load(release.PACKAGE / "checksums.json") == release.workflow.package_checksums(release.PACKAGE)

    root = stage.ROOT.parent.resolve()
    shipment = release.ROOT.resolve()
    retained = {release.ROM: candidate, stage.ROM: candidate, release.PATCH: manifest["patch_sha256"],
                release.MANIFEST: manifest["manifest_sha256"], Path(manifest["own_registered_startup"]):
                manifest["own_registered_startup_sha256"]}
    retained.update({Path(p): sha for p, sha in (visual | playback["evidence"]).items()})
    for shot in [*(row["observed"] for row in playback["holds"]),
                 *(case["final_hold"] for case in playback["cases"])]:
        retained[Path(shot["path"])] = shot["PNG_sha256"]
    startup = base.load(manifest["own_registered_startup"])
    for shot in [*startup["exact_matching_frames"], startup["read_only_snapshot"]]:
        retained[Path(shot["path"])] = shot.get("PNG_sha256", shot.get("sha256"))
    assert all(base.digest(path) == digest for path, digest in retained.items())

    with open_gzip(release.ROOT / "editorial_ledger_before.json.gz", "rb") as archived:
        assert file_digest(archived, "sha256").hexdigest() == mutation["ledger_before"]
    discard = {release.ROOT / name: mutation[key] for name, key in (
        ("ledger_before.json", "ledger_before"), ("ledger_after.json", "ledger_after"),
        ("release_stack_with_rafael_north_sea_africa.json", "registry_after"))}
    keep = {path.resolve() for path in retained}
    first = stage.ROOT.with_name("staged_v1")
    for capture in (first / "focused_gameplay/B55/capture", first / "focused_gameplay/B58/capture",
                    stage.ROOT / "focused_gameplay/B58/capture", first / "startup/capture"):
        report = base.load(capture / "capture_report.json")
        for shot in report["frames_captured"]:
            path = Path(shot["path"])
            assert path.resolve().parent == capture.resolve() and path.suffix == ".png"
            if path.resolve() not in keep:
                discard[path] = shot["PNG_sha256"]
        if capture == first / "startup/capture":
            donor = report["battery_save_preloaded"]
            copy = Path(donor["destination"])
            assert copy.resolve().parent == (capture / "saves").resolve() and copy.suffix == ".dsv"
            assert base.digest(donor["source"]) == donor["source_sha256"]
            if base.digest(copy) == donor["source_sha256"]:
                discard[copy] = donor["source_sha256"]

    removed = []
    for path, sha in discard.items():
        resolved = path.resolve()
        assert resolved not in keep and (resolved.is_relative_to(root) or resolved.is_relative_to(shipment))
        assert path.suffix in {".json", ".png", ".dsv"} and not path.is_symlink() and not path.is_junction()
        assert base.digest(path) == sha
        removed.append(dict(path=str(path), sha256=sha, bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(path) == sha for path, sha in retained.items())
    reclaimed = sum(row["bytes"] for row in removed)
    base.save(receipt, dict(removed=removed, reclaimed_bytes=reclaimed, registered_candidate_sha256=candidate,
                            verified_retained_evidence=len(retained)))
    print(f"Removed {len(removed)} redundant files and reclaimed {reclaimed:,} bytes.")


if __name__ == "__main__":
    main()
