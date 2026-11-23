"""Remove redundant Market checkpoint outputs after their replacements are verified."""
from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path
import re

from scripts import register_rafael_first_market_20261121 as release
from scripts import verify_rafael_preparation_gameplay_20261121 as prep


base = release.base
FRAME = re.compile(r"frame_\d{6}_(cold_boot|navigation|final)\.png")


def main():
    receipt = release.ROOT / "checkpoint_cleanup.json"
    assert not receipt.exists()
    registered = base.load(release.RELEASE)
    assert base.digest(release.ROM) == base.digest(release.stage.ROM) == registered["candidate_sha256"]
    assert base.digest(release.PATCH) == registered["patch_sha256"]
    assert base.digest(release.MANIFEST) == registered["manifest_sha256"]
    plan = base.load(release.VERIFY / "registration_mutation_plan.json")
    assert base.digest(base.REGISTRY) == plan["registry_after"] and base.digest(base.LEDGER) == plan["ledger_after"]
    assert base.digest(base.PROMOTED) == plan["main_sha256"]

    playback, preparation = map(base.load, (release.live.PROOF, prep.PROOF))
    assert base.digest(prep.REPORT) == playback["evidence"][str(prep.REPORT)] == preparation["report_sha256"]
    captures = base.load(prep.REPORT)["frames_captured"]
    used_market = set(release.stage.review.FRAMES.values()) | {32225, 32765, 37085, 39435, 40735}
    kept = [row for row in captures if row["frame"] in used_market]
    kept.extend(row["observed"] for row in preparation["exact_native_dialogue_pixel_masks"])
    kept.append(preparation["preparation_menu"]["observed"])
    keep = {Path(row["path"]).resolve(): row["PNG_sha256"] for row in kept}
    for row in preparation["sheets"]:
        keep[Path(row["path"]).resolve()] = row["sha256"]
    capture_root = prep.REPORT.parent.resolve()
    assert capture_root.is_relative_to(prep.run.ROOT.resolve())
    cleanup = {}
    for row in captures:
        path = Path(row["path"]).resolve()
        assert path.parent == capture_root and FRAME.fullmatch(path.name)
        if path not in keep:
            cleanup[path] = row["PNG_sha256"]

    before = release.ROOT / "ledger_before.json"
    with open_gzip(release.ROOT / "editorial_ledger_before.json.gz", "rb") as snapshot:
        assert file_digest(snapshot, "sha256").hexdigest() == plan["ledger_before"]
    cleanup[before.resolve()] = plan["ledger_before"]
    for name, digest in (("ledger_after.json", plan["ledger_after"]),
                         ("release_stack_with_rafael_first_market.json", plan["registry_after"])):
        path = (release.ROOT / name).resolve()
        assert path.parent == release.ROOT.resolve()
        cleanup[path] = digest
    rebuilt = (release.stage.ROOT / "clean_rebuilt.nds").resolve()
    assert rebuilt.parent == release.stage.ROOT.resolve()
    cleanup[rebuilt] = registered["candidate_sha256"]

    assert all(base.digest(path) == digest for path, digest in keep.items())
    removed = []
    for path, digest in cleanup.items():
        assert path.is_file() and not path.is_symlink() and not path.is_junction()
        assert base.digest(path) == digest
        removed.append(dict(path=str(path), bytes=path.stat().st_size, sha256=digest))
    for path in cleanup:
        path.unlink()
    assert all(base.digest(path) == digest for path, digest in keep.items())
    assert base.digest(release.ROM) == base.digest(release.stage.ROM) == registered["candidate_sha256"]
    total = sum(row["bytes"] for row in removed)
    base.save(receipt, dict(removed=removed, reclaimed_bytes=total, verified_retained_evidence=len(keep),
                            registered_candidate_sha256=registered["candidate_sha256"]))
    print(f"Removed {len(removed)} disposable files and reclaimed {total:,} bytes.")


if __name__ == "__main__":
    main()
