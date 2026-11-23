"""Rebind the acceptance evidence to the registered Hodram Elegy candidate."""

from hashlib import sha256
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import reconcile_editorial_acceptance_20261123 as previous
from scripts import reconcile_queued_sailing_hints_20261123 as queued
from scripts import reconcile_retail_event_coverage_20261123 as events
from scripts.seal_shared_text_source_v1 import reference as text_reference
from scripts.stage_azores_wording_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, digest, read, reference, write


RELEASE = queued.RELEASE
PACKAGE = RELEASE.parent.parent
ROOT = queued.OUT.parent
OUT = ROOT / "editorial_acceptance_elegy_20261123.json"
DRIVE = ROOT / "hodram_elegy_drive_20261123.json"
REVIEW = RELEASE.with_name("registered_review.json")
QA = RELEASE.with_name("qa_passed.xml")
OLD_PACKAGE = previous.PACKAGE / "verification"
ROUTE = OLD_PACKAGE / "current_route_coverage_20261123.json"
CREDITED = (6887, 5356, 6720, 5129)


def h(data):
    return sha256(data).hexdigest()


def story_scope(clean, current, old, release):
    event_reg = read(events.REPORT)
    credits = read(ROUTE)
    assert credits["manifest_prefix_exact"] and credits["exact_credited_clean_positions"] == sum(CREDITED)
    assert event_reg["event_to_reviewed_script_block_count"] == 1307
    assert event_reg["bound_prior_town_trend_events"] == 80
    assert event_reg["exact_credited_clean_story_positions"] == sum(CREDITED)
    original_arm, current_arm = [image.read_file(previous.ARM) for image in (clean, current)]
    for start, stop in events.ARCHIVE_LOADER_SPANS:
        assert current_arm[start:stop] == original_arm[start:stop]
    baselines, installed, changed = {}, {}, {}
    rebuilt = {}
    for i, (record, n) in enumerate(zip(event_reg["scopes"], CREDITED, strict=True)):
        path = record["script_file"]
        proof = credits["routes"][path]
        old_script, source_script, installed_script = [image.read_file(path) for image in (old, clean, current)]
        assert h(old_script) == record["installed_script_sha256"] == proof["installed_archive_sha256"]
        assert h(source_script) == record["clean_script_sha256"]
        assert h(installed_script) == release[f"target_SC{i}_sha256"]
        assert proof["exact_credited_clean_positions"] == n
        census = proof["source_census"]
        assert digest(census["path"]) == census["sha256"]
        ev, alt = record["event_file"], record["alternate_story_archive"]
        assert h(current.read_file(ev)) == h(clean.read_file(ev)) == record["clean_and_installed_event_sha256"]
        assert h(current.read_file(alt)) == h(clean.read_file(alt)) == record["alternate_story_archive_sha256"]
        baselines[path], installed[path], old_blocks = [IlnkContainer.parse(raw).blocks for raw in
                                                        (source_script, installed_script, old_script)]
        assert len(baselines[path]) == len(installed[path]) == len(record["event_to_block_mapping"])
        assert sorted(entry[-1] for entry in record["event_to_block_mapping"]) == list(range(len(installed[path])))
        delta = [j for j, (a, b) in enumerate(zip(old_blocks, installed[path], strict=True)) if a != b]
        assert delta == ([16] if i == 1 else [])
        changed[path] = delta
        rebuilt[path] = dict(installed_sha256=h(installed_script), clean_sha256=h(source_script),
                             source_positions=n, event_archive=record["event_file"], changed_blocks=delta,
                             fallback_archive=alt)
    priority = previous.priority_bindings(baselines, installed)

    source = baselines["/data/SC1.DK4"][16]
    active = installed["/data/SC1.DK4"][16]
    story = read(REVIEW)
    assert story["candidate_sha256"] == release["candidate_sha256"]
    assert story["target_SC1_sha256"] == release["target_SC1_sha256"]
    assert len(story["records"]) == 14 and len(story["changed_ids"]) == 2
    for row in story["records"]:
        before, after = row["source_reference"], row["registered_reference"]
        assert before["block_sha256"] == h(source) and after["block_sha256"] == h(active)
        source_raw, target_raw = bytes.fromhex(row["source_hex"]), bytes.fromhex(after["exact_command_hex"])
        source_at, target_at = before["offset"], after["command_offset"]
        assert source[source_at:source_at+len(source_raw)] == source_raw
        assert active[target_at:target_at+len(target_raw)] == target_raw
        assert source_raw[0] == target_raw[5]
        assert set(row["review"]) == previous.GATES and all(row["review"].values())
    return dict(route_credit=reference(ROUTE), event_selector_inventory=reference(events.REPORT),
                four_route_archives=rebuilt, exact_credited_positions=sum(CREDITED),
                exact_retail_event_routes=1307, town_trend_mappings_reused=80,
                rechecked_priority_source_and_installed_bindings=priority, elegy_review=reference(REVIEW),
                other_story_blocks_match_prior=sum(len(v) for v in installed.values()) - sum(map(len, changed.values())))


def shared_and_help(clean, active, prior, release):
    shared = read(previous.SHARED)
    assert shared["scoped_shared_display_findings"] == len(shared["records"]) == 276
    assert not shared["remaining_without_scoped_disposition"]
    arm = active.read_file(previous.ARM)
    source = common_message_entries(clean.read_file(previous.COMMON), clean.read_file(previous.ARM))
    current = common_rows(active.read_file(previous.COMMON), arm)
    assert len(source) == len(current) == 3668
    assert h(active.read_file(previous.COMMON)) == release["target_COMMON_sha256"]
    for row in shared["records"]:
        key = row["message_ID"]
        assert text_reference(source[key]) == row["source_reference"] and source[key].text.hex() == row["source_hex"]
        assert text_reference(current[key]) == row["installed_reference"] and current[key].text.hex() == row["installed_hex"]
    common = dict(scoped_rows=276, exact_source_and_active_native_storage=True, inherited_display_evidence=reference(previous.SHARED),
                  direct_calls_outside_verified_display_scopes_open=shared["other_direct_display_paths_unverified"],
                  exact_archived_artwork_identities_open=shared["exact_archived_artwork_identities_open"])
    ja, en, earlier = [image.read_file(previous.HELP) for image in (clean, active, prior)]
    assert en == earlier and [len(IlnkContainer.parse(arc).blocks) for arc in (ja, en)] == [202, 217]
    help_ref = read(OLD_PACKAGE / "current_editorial_coverage_audit_20261123.json")["inventory"]["original_Help"]
    assert h(en) == help_ref["installed_sha256"] == release["target_HELP_sha256"]
    return common, dict(approved_source_topics=202, installed_parts=217, continuations=15, installed_sha256=h(en))


def check_registered_release():
    release = read(RELEASE)
    candidate = release["candidate_sha256"]
    for path, field in ((release["candidate"], "candidate_sha256"), (CLEAN, "clean_input_sha256"),
                        (release["manifest"], "manifest_sha256"), (REGISTRY, "registry_sha256"),
                        (release["patch"], "patch_sha256"), (release["own_registered_startup"], "own_registered_startup_sha256")):
        assert digest(path) == release[field]
    assert release["clean_input_patch_byte_exact"] and release["whole_parent_inverse_exact"]
    assert release["experimental_not_promoted"] and not release["own_registered_startup_pending"]
    checksums = read(PACKAGE / "checksums.json")
    for filename in checksums:
        assert digest(PACKAGE / filename) == checksums[filename]
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(field, "0")) for field in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    receipt = read(DRIVE)
    assert receipt["nds_files_in_folder"] == 1 and receipt["streamed_readback_exact"]
    assert receipt["candidate_sha256"] == receipt["downloaded_sha256"] == candidate
    startup = read(release["own_registered_startup"])
    assert startup["candidate_sha256"] == candidate and startup["cold_boot"] and not startup["savestate"]
    assert len(startup["exact_matching_frames"]) == 6 and len(startup["original_protected_name_getters"]) == 24
    plan = read(RELEASE.with_name("registration_mutation_plan.json"))
    assert plan["main_sha256"] == digest("translations/promoted_build.json")
    return release


def main():
    release = check_registered_release()
    historical = read(OLD_PACKAGE / "registered_release_verification.json")
    assert digest(historical["candidate"]) == historical["candidate_sha256"]
    clean, active, prior = [NdsImage.open(p) for p in (CLEAN, release["candidate"], historical["candidate"])]
    story = story_scope(clean, active, prior, release)
    common, help_ = shared_and_help(clean, active, prior, release)
    bounds = previous.right_bound(active.read_file(previous.ARM), release["right_bound_configuration"])
    assert bounds["matched_repair_spans"] == 8
    hints = read(queued.OUT)
    assert hints["candidate_sha256"] == release["candidate_sha256"] and hints["admitted_kinds"] == list(range(9))
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], registered_release=reference(RELEASE),
                    focused_tests=reference(QA), startup=reference(release["own_registered_startup"]),
                    exact_clean_input_patch=reference(release["patch"]), verified_Drive_receipt=reference(DRIVE),
                    saved_main_descriptor_verified=True, accepted_layers=release["accepted_layers"],
                    active_ASCII_right_bound=bounds, credited_story=story, shared_dialogue=common,
                    help_archive=help_, sailing_hint_ownership=reference(queued.OUT), new_editorial_credit=0,
                    new_gameplay=False, full_editorial_goal_complete=False))
    print("Current candidate matches 416 priority bindings, 24,092 credited story positions, 276 scoped COMMON findings, and 202 Help topics.")


if __name__ == "__main__":
    main()
