"""Clear obsolete Spanish chapter captures while preserving the tested release."""

from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path

from scripts import register_rafael_spain_20261121 as release


base, stage = release.base, release.stage


def main():
    receipt = release.ROOT / "checkpoint_cleanup.json"
    assert not receipt.exists()
    transaction, manifest, live, visual, drive = map(base.load, (
        release.VERIFY / "registration_mutation_plan.json", release.RELEASE, release.live.PROOF,
        release.EVIDENCE / "visual_review.json", release.ROOT / "drive_latest_build_receipt.json"))
    sha = manifest["candidate_sha256"]
    assert sha == base.digest(release.ROM) == live["candidate_sha256"] == drive["sha256"]
    assert drive["sole_nds_in_folder"] and drive["readback_verified"]
    assert base.digest(base.REGISTRY) == manifest["registry_sha256"] == transaction["registry_after"]
    assert base.digest(base.LEDGER) == transaction["ledger_after"]
    assert base.digest(base.PROMOTED) == transaction["main_sha256"]
    assert base.load(release.PACKAGE / "checksums.json") == release.workflow.package_checksums(release.PACKAGE)
    startup = base.load(manifest["own_registered_startup"])
    retained = {release.ROM: sha, stage.ROM: sha, release.PATCH: manifest["patch_sha256"],
                release.MANIFEST: manifest["manifest_sha256"]}
    retained.update({Path(p): h for p, h in (visual | live["evidence"]).items()})
    for shot in [*(row["observed"] for row in live["holds"] + live["menus"]),
                 live["final_hold"], *startup["exact_matching_frames"], startup["read_only_snapshot"]]:
        retained[Path(shot["path"])] = shot.get("PNG_sha256", shot.get("sha256"))
    assert all(base.digest(path) == h for path, h in retained.items())
    keep = {path.resolve() for path in retained}
    with open_gzip(release.ROOT / "editorial_ledger_before.json.gz", "rb") as archived:
        assert file_digest(archived, "sha256").hexdigest() == transaction["ledger_before"]
    discard = {release.ROOT / name: transaction[key] for name, key in (
        ("ledger_before.json", "ledger_before"), ("ledger_after.json", "ledger_after"),
        ("release_stack_with_rafael_spain.json", "registry_after"))}
    first = stage.ROOT.with_name("staged_v1")
    for capture in (first / "focused_gameplay/capture", first / "startup/capture"):
        report = base.load(capture / "capture_report.json")
        for shot in report["frames_captured"]:
            path = Path(shot["path"])
            assert path.resolve().parent == capture.resolve() and path.suffix == ".png"
            if path.resolve() not in keep:
                discard[path] = shot["PNG_sha256"]
        if donor := report.get("battery_save_preloaded"):
            copy = Path(donor["destination"])
            assert copy.resolve().parent == (capture / "saves").resolve() and copy.suffix == ".dsv"
            assert base.digest(donor["source"]) == donor["source_sha256"]
            if base.digest(copy) == donor["source_sha256"]:
                discard[copy] = donor["source_sha256"]
    roots = [root.resolve() for root in (stage.ROOT.parent, release.ROOT)]
    removed = []
    for path, h in discard.items():
        resolved = path.resolve()
        assert resolved not in keep and any(resolved.is_relative_to(root) for root in roots)
        assert path.suffix in {".json", ".png", ".dsv"} and not path.is_symlink() and not path.is_junction()
        assert base.digest(path) == h
        removed.append(dict(path=str(path), sha256=h, bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(path) == h for path, h in retained.items())
    reclaimed = sum(row["bytes"] for row in removed)
    base.save(receipt, dict(removed=removed, reclaimed_bytes=reclaimed, registered_candidate_sha256=sha,
                            verified_retained_evidence=len(retained)))
    print(f"Removed {len(removed)} redundant files and reclaimed {reclaimed:,} bytes.")


if __name__ == "__main__":
    main()
