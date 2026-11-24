"""Reconcile release continuity and the remaining editorial inventory on Deck View."""

from collections import Counter
from pathlib import Path
from types import FunctionType, SimpleNamespace
from xml.etree import ElementTree

from dk4tool.formats.ilnk import IlnkContainer
from scripts import reconcile_lisbon_editorial_acceptance_20261124 as previous
from scripts import register_deck_skill_guidance_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write

yard, tunis = previous.yard, previous.tunis
ARM, COMMON = current.ARM, current.COMMON
OUT = previous.ROOT / "editorial_acceptance_after_deck_skill_20261124.json"
ROOT = OUT.parent
STEPS = ("20261124_lisbon_roster_galley", "20261124_price_info_digits", "20261124_riga_recruitment",
         "20261124_palace_investment_wording", "20261124_cargo_storage_warning", "20261124_deck_skill_guidance")
ARCHIVED = ROOT / "archived_dialogue_current_drafts_20261124.json"
ARCHIVED_CASES = ROOT / "archived_pointer_materialization_20261124.json"
TREND = ROOT / "athens_ordinary_market_trends_20261124.json"
FLEET = ROOT / "riga_port_trend_object_20261124.json"
DRIVE = ROOT / "deck_skill_guidance_drive_20261124.json"
CLEANUP = ROOT / "deck_skill_guidance_cleanup_20261124.json"


def exact_review(release, review, clean, before, after):
    original = tunis.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    old, new = (yard.common_rows(image.read_file(COMMON), image.read_file(ARM)) for image in (before, after))
    exact = []
    for row in review["records"]:
        assert set(row["review"]) == set(GATES) and all(row["review"].values())
        if row.get("file_path") != COMMON:
            continue
        key = row.get("message_ID", row.get("message_id"))
        assert isinstance(key, int)
        for reference_key, entry in zip(("source_reference", "current_reference", "registered_reference"),
                                         (original[key], old[key], new[key]), strict=True):
            reference_data = row[reference_key]
            raw = reference_data.get("exact_hex", reference_data.get("exact_stored_hex", row.get(reference_key.split("_")[0] + "_hex")))
            assert raw == entry.text.hex(), (row["id"], reference_key, release["profile"])
            assert all(reference_data[field] == value for field, value in yard.message_reference(entry).items())
        exact.append(dict(id=row["id"], decision=row["decision"], message_ID=key,
                          source=original[key].text.hex(), previous=old[key].text.hex(), installed=new[key].text.hex()))
    return exact


def coverage(clean, image, release, review, anchor):
    ledger = read(yard.LEDGER)
    assert ledger["current_integrated_candidate"]["sha256"] == release["candidate_sha256"] and not ledger["full_goal_complete"]
    rows = ledger["contextual_story_natural_dialogue_pass_v1871"]["integrated_record_keys"]
    credits = {(row["file_path"], row["id"]) for row in rows}
    assert len(credits) == len(rows) == ledger["records_editorially_completed"] == 27700
    counts = Counter(path for path, _ in credits)
    assert counts == anchor["coverage"]["historical_credits_by_path"]
    del ledger, rows
    credited = {int(ident.split("_")[-1]) for path, ident in credits if path == COMMON}
    arm = image.read_file(ARM)
    commons = yard.common_rows(image.read_file(COMMON), arm)
    scoped = review["shared_consumer_binding"]
    assert scoped["candidate_sha256"] == release["candidate_sha256"]
    scope = {r["message_ID"]: r for r in scoped["records"]}
    assert len(commons) == 3668 and len(credited) == 3392 and len(scope) == 276
    assert credited.isdisjoint(scope) and credited | scope.keys() == set(range(len(commons)))
    assert all(yard.message_reference(commons[key]) == row["installed"] for key, row in scope.items())

    old_story = {path: IlnkContainer.parse(clean.read_file(path)).blocks for path in tunis.ROUTES}
    new_story = {path: IlnkContainer.parse(image.read_file(path)).blocks for path in tunis.ROUTES}
    assert sum(map(len, old_story.values())) == sum(map(len, new_story.values())) == 1307
    hashes = {path: sha256(image.read_file(path)).hexdigest() for path in previous.ARCHIVES}
    assert hashes == anchor["current_story_and_help_archives"]
    assert all(hashes[path] == release[f"target_SC{index}_sha256"] for index, path in enumerate(tunis.ROUTES))
    assert all(image.read_file(f"/data/EV{i}.DK4") == clean.read_file(f"/data/EV{i}.DK4") for i in range(4))
    priority = tunis.kurushima.genoa.acceptance.priority_bindings(old_story, new_story)
    assert priority == anchor["coverage"]["priority_decisions"] and priority["exact_source_and_approved_blocks"] == 416
    assert len(IlnkContainer.parse(clean.read_file(tunis.HELP)).blocks) == 202
    assert len(IlnkContainer.parse(image.read_file(tunis.HELP)).blocks) == 217
    assert hashes[tunis.HELP] == release["target_HELP_sha256"]

    wraps = read(tunis.OUT)["current_progressive_wrap_scan"]
    now = []
    for path in tunis.ROUTES:
        _, flags = tunis.kurushima.scanner.scan(path, image.read_file(path))
        now.extend(flags)
    assert wraps["open_flags"] == []
    expected = [{key: value for key, value in row.items() if key != "reviewed"} for row in wraps["reviewed_flags"]]
    assert now == expected and len(expected) == anchor["inherited_story_wrap_dispositions"] == 50
    return dict(historical_credits=27700, story_positions=sum(counts[p] for p in tunis.ROUTES),
        historical_credits_by_path=counts, priority_story_decisions=priority, current_story_and_help_sha256=hashes,
        common_total=3668, common_credited=3392, common_scoped=276, original_help_topics=202, current_help_pages=217,
        bound_story_wrap_dispositions=wraps["reviewed_flags"], current_open_story_wrap_flags=[])


def regressions(clean, image, release):
    arm = image.read_file(ARM)
    credit = tunis.kurushima.credit
    credit.runtime_scope["verify_runtime"](arm, release)
    assert current.template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    bound = FunctionType(credit.names.name_bindings.__code__, vars(credit.names) | dict(current=SimpleNamespace(RELEASE=current.RELEASE)))
    names = bound(release, clean.read_file(ARM))
    assert names["original_default_getter_cases"] == 414 and names["checked_clean_and_current_field_slots"] == 621
    return dict(ascii_right_bound_spans=8, Julio=credit.julio_dependency(image, arm),
                Deck=credit.deck_dependencies(image, arm), default_names=names,
                Market_Goods_Info_current_protected_format_and_pointers=True)


def package(release):
    manifest = read(release["manifest"])
    assert manifest["profile"] == release["profile"] and manifest["candidate_sha256"] == release["candidate_sha256"]
    assert manifest["release_stack_sha256"] == release["registry_sha256"] == digest(REGISTRY)
    registry = read(REGISTRY)
    assert registry["profiles"][release["profile"]]["status"] == "experimental"
    batches = {path.replace("\\", "/") for path in manifest["batches"]}
    checks = manifest["checks"]
    assert len(batches) == release["registered_manifest_entries"] == 1142
    assert len(checks) == release["passing_release_checks"] == 477 and all(checks.values())
    accepted = registry["accepted_layers"]
    assert len(accepted) == release["accepted_layers"] == 114
    assert all(row["status"] == "accepted" and
        (row.get("baked_into_baseline") or row["batch"].replace("\\", "/") in batches) for row in accepted)
    startup_path = Path(release["own_registered_startup"])
    startup = read(startup_path)
    assert digest(startup_path) == release["own_registered_startup_sha256"]
    assert startup["candidate_sha256"] == release["candidate_sha256"] and startup["cold_boot"] and not startup["savestate"]
    assert len(startup["exact_matching_frames"]) == 6 and len(startup["original_protected_name_getters"]) == 24
    suite, = ElementTree.parse(current.VERIFY / "qa_passed.xml").iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "errors", "failures", "skipped")] == [17, 0, 0, 0]
    patch_path = current.VERIFY / "clean_patch_proof.json"
    patch = read(patch_path)
    assert patch["byte_exact"] and patch["clean_input_sha256"] == release["clean_input_sha256"] == digest(CLEAN)
    assert patch["candidate"]["sha256"] == patch["rebuilt"]["sha256"] == release["candidate_sha256"]
    assert patch["patch"]["sha256"] == release["patch_sha256"] == digest(release["patch"])
    tracked = read(current.PACKAGE / "checksums.json")
    assert all(digest(current.PACKAGE / path) == expected for path, expected in tracked.items())
    drive = read(DRIVE)
    assert drive["verified"] and drive["sole_nds"]
    assert drive["registered_candidate_sha256"] == drive["readback_sha256"] == release["candidate_sha256"]
    assert read(CLEANUP)["unique_roms_or_donor_saves_removed"] == 0
    return dict(accepted_layers=len(accepted), manifest_entries=len(batches), passing_checks=len(checks), focused_tests=17,
        package_file_hashes=len(tracked), startup=reference(startup_path), patch_round_trip=reference(patch_path),
        sole_drive_readback=reference(DRIVE), cleanup=reference(CLEANUP), experimental_main_acceptance_pending=True)


def remaining(image, release):
    archive, pointers, fleet, trend = map(read, (ARCHIVED, ARCHIVED_CASES, FLEET, TREND))
    assert all(receipt["candidate_sha256"] == release["candidate_sha256"] for receipt in (archive, pointers, fleet, trend))
    assert pointers["same_verified_827_sites"]["aligned_callers"] == 827 and not pointers["matches"]
    commons = yard.common_rows(image.read_file(COMMON), image.read_file(ARM))
    open_items = []
    for row in archive["records"]:
        assert row["original_display_ownership_open"] and row["review"]["formatting"] is False
        key = row["message_ID"]
        assert row["installed_reference"]["exact_hex"] == commons[key].text.hex()
        open_items.append(dict(message_ID=key, pending_allocation=row["relocation_required_if_proposal_accepted"],
                               provided_native_preview=row["native_controlled_preview"] is not None))
    assert [row["message_ID"] for row in open_items] == list(previous.OPEN)
    assert not fleet["naturally_produced_Fleet_Info_destination_114_observed"]
    assert trend["ordinary_gameplay"] and all(all(row["review"].values()) for row in trend["records"])
    return dict(archived_COMMON=open_items, archived_drafts=reference(ARCHIVED), current_caller_scope=reference(ARCHIVED_CASES),
        ordinary_Fleet_Info_114_producer_open=True, CAdman_Riga_evidence=reference(FLEET), active_Athens_report=reference(TREND),
        practical_additional_town_and_random_scenes=True)


def main():
    initial, newest = read(previous.OUT), read(current.RELEASE)
    assert previous.lineage(initial["candidate_sha256"], newest["candidate_sha256"]) == list(STEPS)
    clean = NdsImage.open(CLEAN)
    before = yard.load(STEPS[0])
    deltas = []
    for step in STEPS[1:]:
        after = yard.load(step)
        release, review, refs, image = after
        common_compatible = review | {"records": [
            row | {"message_ID": row.get("message_ID", row.get("message_id")), "decision": row.get("wording_decision", row["decision"])}
            if row.get("file_path") == COMMON else row for row in review["records"]]}
        delta = previous.compare(before, (release, common_compatible, refs, image))
        delta["exact_COMMON_reviews"] = exact_review(after[0], after[1], clean, before[3], after[3])
        deltas.append(delta)
        before = after
    release, review, _, image = before
    assert release == newest
    report = dict(candidate_sha256=release["candidate_sha256"], earlier_acceptance=reference(previous.OUT),
        exact_registered_deltas=deltas, coverage=coverage(clean, image, release, review, initial),
        targeted_regressions=regressions(clean, image, release), release_tests=package(release),
        pending=remaining(image, release), new_editorial_credit=0, new_gameplay_runs=0, full_editorial_goal_complete=False)
    write(OUT, report)
    print("Verified five exact registered inverses, current coverage, the user-reported renderer dependencies, and the testing package.")


if __name__ == "__main__":
    main()
