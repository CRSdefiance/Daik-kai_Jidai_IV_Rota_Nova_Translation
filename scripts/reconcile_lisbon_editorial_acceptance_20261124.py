"""Carry the editorial inventory from Maria's captured-ship checkpoint to Lisbon."""

from itertools import pairwise
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.formats.ilnk import IlnkContainer
from scripts import reconcile_maria_capture_acceptance_20261124 as anchor
from scripts import register_lisbon_roster_galley_20261124 as current
from scripts import register_tripoli_hodram_warning_20261124 as tripoli
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


tunis, yard = anchor.tunis, anchor.tunis.yard
ROOT = anchor.ROOT
OUT = ROOT / "editorial_acceptance_after_lisbon_20261124.json"
ARM, COMMON = current.ARM, current.COMMON
ARCHIVES = (*tunis.ROUTES, tunis.HELP)
OPEN = (284, 318, 750, 751, 752)


def lineage(first_hash, last_hash):
    paths = Path("releases").glob("all_routes_editorial_20261124_*_candidate/verification/registered_release_verification.json")
    packages = {}
    for path in paths:
        receipt = read(path)
        packages[receipt["candidate_sha256"]] = path.parents[1].name.removeprefix("all_routes_editorial_").removesuffix("_candidate"), receipt
    chain, seen = [], set()
    while last_hash != first_hash:
        assert last_hash not in seen
        seen.add(last_hash)
        step, receipt = packages[last_hash]
        chain.append(step)
        last_hash = receipt["predecessor"]["candidate_sha256"]
    return [packages[first_hash][0], *reversed(chain)]


def compare(previous, new):
    parent, _, _, before_image = previous
    release, review, evidence, image = new
    for key in ("candidate", "candidate_sha256", "registry_sha256", "manifest_sha256"):
        assert parent[key] == release["predecessor"][key]
    for key in ("registered_manifest_entries", "passing_release_checks"):
        assert release[key] == parent[key] + 1
    for key in ("accepted_layers", "canonical_sha256", "clean_input_sha256"):
        assert release[key] == parent[key]
    before, after = map(yard.assets, (before_image, image))
    assert before.keys() == after.keys()
    changed = {path for path in before if before[path] != after[path]}
    registered = set(release["changed_internal_files"])
    assert changed == registered and changed <= {ARM, COMMON, tripoli.STORY}, (release["profile"], changed, registered)
    if COMMON in changed:
        old, new = (yard.common_rows(files[COMMON], files[ARM]) for files in (before, after))
        revised = {int(row["message_ID"]) for row in review["records"]
                   if row["decision"] == "revision" and row["file_path"] == COMMON}
        affected = {a.message_id for a, b in zip(old, new, strict=True) if a.text != b.text}
        assert affected == revised and not affected.intersection(OPEN)
    else:
        affected = set()
    tripoli_command = None
    if tripoli.STORY in changed:
        assert release["profile"] == tripoli.PROFILE and changed == {tripoli.STORY}
        old_blocks, new_blocks = (IlnkContainer.parse(files[tripoli.STORY]).blocks for files in (before, after))
        assert [i for i, (old_block, new_block) in enumerate(zip(old_blocks, new_blocks, strict=True))
                if old_block != new_block] == [tripoli.build.BLOCK]
        source = NdsImage.open(CLEAN).read_file(tripoli.STORY)
        tripoli_command = yard.story_review(tripoli.STORY, tripoli.build.BLOCK, source, before[tripoli.STORY],
                                           after[tripoli.STORY], review, evidence[1])
    for path in changed:
        image.replace_file(path, before[path])
    try:
        assert sha256(image.rom.save()).hexdigest() == parent["candidate_sha256"]
    finally:
        for path in changed:
            image.replace_file(path, after[path])
    return dict(profile=release["profile"], candidate_sha256=release["candidate_sha256"],
                exact_predecessor_inverse=True, changed_files=sorted(changed),
                changed_COMMON_IDs=sorted(affected), verified_tripoli_warning=tripoli_command,
                verified_review_gates=len(review["records"]), evidence=evidence)


def main():
    start, last = read(anchor.OUT), read(current.RELEASE)
    assert digest(CLEAN) == last["clean_input_sha256"] and digest(REGISTRY) == last["registry_sha256"]
    chain = lineage(start["candidate_sha256"], last["candidate_sha256"])
    assert chain[-1] == "20261124_lisbon_roster_galley"
    deltas = []
    previous = first = yard.load(chain[0])
    for step in chain[1:]:
        new = yard.load(step)
        deltas.append(compare(previous, new))
        previous = new
    release, review, _, image = previous
    assert release == last
    inherited = read(tunis.OUT)
    coverage = inherited["current_coverage"]
    assert coverage["still_open_archived_display_ids"] == list(OPEN)
    assert not inherited["current_progressive_wrap_scan"]["open_flags"]
    archive_hashes = {path: sha256(image.read_file(path)).hexdigest() for path in ARCHIVES}
    unchanged = {path: value for path, value in archive_hashes.items() if path != tripoli.STORY}
    assert all(sha256(first[3].read_file(path)).hexdigest() == value for path, value in unchanged.items())
    tripoli_proof, = [row for row in deltas if row["verified_tripoli_warning"]]
    assert archive_hashes[tripoli.STORY] == read(tripoli.RELEASE)["target_SC1_sha256"]
    assert tripoli_proof["profile"] == tripoli.PROFILE
    arm = image.read_file(ARM)
    assert current.template.right_bound(arm, last["right_bound_configuration"])["matched_repair_spans"] == coverage["ascii_right_bound_spans"] == 8
    commons = current.gameplay.panels.common_rows(image.read_file(COMMON), arm)
    shared = review["shared_consumer_binding"]["records"]
    assert len(commons) == coverage["native_COMMON_slots"] == 3668
    assert len(shared) == coverage["scoped_COMMON_records"] == 276
    assert all(current.gameplay.panels.text_reference(commons[row["message_ID"]]) == row["installed"] for row in shared)
    drive_file = ROOT / "lisbon_roster_galley_drive_20261124.json"
    drive = read(drive_file)
    assert drive["verified"] and drive["sole_nds"]
    assert drive["registered_candidate_sha256"] == drive["readback_sha256"] == last["candidate_sha256"]
    package = current.PACKAGE
    files = read(package / "checksums.json")
    assert all(digest(package / path) == expected for path, expected in files.items())
    suite, = ElementTree.parse(current.VERIFY / "qa_passed.xml").iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "errors", "failures", "skipped")] == [17, 0, 0, 0]
    resource = read(last["manifest"])
    assert resource["release_stack_sha256"] == digest(REGISTRY)
    checks = resource["checks"]
    assert len(checks) == last["passing_release_checks"] == 472 and all(checks.values())
    assert len(resource["batches"]) == last["registered_manifest_entries"] == 1137
    accepted = read(REGISTRY)["accepted_layers"]
    batches = {path.replace("\\", "/") for path in resource["batches"]}
    assert len(accepted) == last["accepted_layers"] == 114
    assert all(row["status"] == "accepted" and
               (row.get("baked_into_baseline") or row["batch"].replace("\\", "/") in batches) for row in accepted)
    write(OUT, dict(
        candidate_sha256=last["candidate_sha256"], base_acceptance=reference(anchor.OUT),
        inherited_inventory=reference(tunis.OUT), exact_registered_deltas=deltas,
        current_story_and_help_archives=archive_hashes, unchanged_story_and_help_archives=unchanged, coverage=coverage,
        inherited_story_wrap_dispositions=start["inherited_story_wrap_dispositions"],
        drive_readback=reference(drive_file), candidate_package=reference(package / "checksums.json"),
        passing_release_checks=len(checks), accepted_layers=len(accepted), verified_package_files=len(files),
        ordinary_missionary_activation_observed=False, open_archived_display_IDs=list(OPEN),
        new_editorial_credit=0, new_gameplay_runs=0, full_editorial_goal_complete=False,
    ))
    print(f"Reconciled {len(deltas)} registered inverses, {len(shared)} active shared references and {len(files)} package files.")


if __name__ == "__main__":
    main()
