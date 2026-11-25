"""Carry the Tunis acceptance inventory through the two COMMON-only releases."""

from pathlib import Path
from types import FunctionType

from scripts import reconcile_tunis_editorial_acceptance_20261124 as tunis
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write


ROOT = tunis.OUT.parent
OUT = ROOT / "editorial_acceptance_after_maria_capture_20261124.json"
STEPS = (
    ("20261124_tunis_shop_advice", (), None),
    ("20261124_tunis_palace_refusal", (1148,), "stored_proof.json"),
    ("20261124_maria_captured_ship", (2086,), "stored_proof.json"),
)


def main():
    previous = read(tunis.OUT)
    history = [tunis.yard.load(step) for step, _, _ in STEPS]
    ancestor = history[0][0]
    assert ancestor["candidate_sha256"] == previous["candidate_sha256"]
    clean = NdsImage.open(CLEAN)
    bind_deltas = FunctionType(tunis.exact_deltas.__code__, vars(tunis) | dict(STEPS=STEPS))
    deltas = bind_deltas(clean, history)
    assert all(row["changed_paths"] == [tunis.COMMON] for row in deltas)
    release, _, evidence, image = history[-1]
    assert image.read_file(tunis.ARM) == history[0][3].read_file(tunis.ARM)
    assert digest(REGISTRY) == release["registry_sha256"]
    package = Path(evidence[0]["path"]).parents[1]
    receipts = read(package / "checksums.json")
    assert all(digest(package / path) == expected for path, expected in receipts.items())

    drive = ROOT / "maria_captured_ship_drive_20261124.json"
    receipt = read(drive)
    assert receipt["candidate_sha256"] == receipt["downloaded_sha256"] == release["candidate_sha256"]
    wrap_scan = previous["current_progressive_wrap_scan"]
    assert not wrap_scan["open_flags"]
    write(OUT, dict(
        candidate_sha256=release["candidate_sha256"], predecessor_acceptance=reference(tunis.OUT),
        exact_registered_deltas=deltas, verified_package_hashes=len(receipts),
        drive_readback=reference(drive), accepted_layers=release["accepted_layers"],
        passing_release_checks=release["passing_release_checks"],
        inherited_story_wrap_dispositions=len(wrap_scan["reviewed_flags"]),
        inherited_dependencies="All non-COMMON data, including route archives, name data and ARM9, match the accepted Tunis audit.",
        remaining=previous["remaining"], ordinary_gameplay_added=False,
        ROM_changed=False, new_editorial_credit=0, full_editorial_goal_complete=False,
    ))
    print(f"Verified both registered inverses and {len(receipts)} package hashes. "
          f"{len(wrap_scan['reviewed_flags'])} story wrap decisions carry forward on unchanged route data.")


if __name__ == "__main__":
    main()
