"""Verify the current editorial inventory across the four post-Deck releases."""

from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

from dk4tool.formats.ilnk import IlnkContainer
from scripts import reconcile_deck_skill_acceptance_20261124 as deck
from scripts import reconcile_editorial_acceptance_20261123 as editorial
from scripts import reconcile_original_story_packets_20261124 as prepared
from scripts import reconcile_original_wrap_intake_20261124 as wrap
from scripts import reconcile_retail_event_coverage_20261123 as events
from scripts import register_claudio_opening_wrap_20261124 as claudio
from scripts import register_seoul_reika_20261125 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


ROOT = deck.ROOT
OUT = ROOT / "editorial_acceptance_after_seoul_20261125.json"
ARM, COMMON, HELP = deck.ARM, deck.COMMON, deck.tunis.HELP
ROUTES = tuple(f"/data/SC{i}.DK4" for i in range(4))
STEPS = (("20261124_deck_skill_guidance", None), ("20261124_claudio_opening_wrap", None),
         ("20261124_ceuta_contract_refusal", 761), ("20261124_lisbon_purser_refit", 1255),
         ("20261125_seoul_reika", 991))
OPEN_IDS = (284, 318, 750, 751, 752)
DRIVE = ROOT / "seoul_reika_drive_20261125.json"
CLEANUP = ROOT / "seoul_reika_cleanup_20261125.json"
mapped, value = current.template.mapped, current.template.value


def h(raw):
    return sha256(raw).hexdigest()


def proof(path, candidate):
    receipt = read(path)
    assert receipt["candidate_sha256"] == candidate, path
    return receipt


def original_deltas(clean, anchor):
    first = previous = deck.yard.load(STEPS[0][0])
    assert first[0]["candidate_sha256"] == anchor["candidate_sha256"]
    deltas = []
    for step, expected_id in STEPS[1:]:
        successor = deck.yard.load(step)
        release, review, refs, image = successor
        before, after = map(deck.yard.assets, (previous[3], image))
        expected_file = claudio.STORY if expected_id is None else COMMON
        assert before.keys() == after.keys()
        assert [key for key in before if before[key] != after[key]] == release["changed_internal_files"] == [expected_file]
        for name in ("candidate", "candidate_sha256", "manifest_sha256", "registry_sha256"):
            assert release["predecessor"][name] == previous[0][name]
        for name in ("registered_manifest_entries", "passing_release_checks"):
            assert release[name] == previous[0][name] + 1
        for name in ("accepted_layers", "canonical_sha256", "clean_input_sha256", "target_ARM9_sha256"):
            assert release[name] == previous[0][name]
        revised, = [row for row in review["records"] if row["decision"] == "revision"]
        if expected_id is None:
            source, old, new = (IlnkContainer.parse(raw).blocks for raw in
                                 (clean.read_file(expected_file), before[expected_file], after[expected_file]))
            assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == [claudio.BLOCK]
            edits = []
            for row in review["records"]:
                assert row["file_path"] == expected_file and row["block"] == claudio.BLOCK
                a, b, c = (deck.yard.story_command(blocks[claudio.BLOCK], row[key]) for blocks, key in
                            ((source, "source_reference"), (old, "current_reference"), (new, "registered_reference")))
                assert a[:2] == b[:2] == c[:2] and b[:6] == c[:6] and len(b) == len(c)
                assert (b != c) == (row["id"] == revised["id"])
                if b != c:
                    at = row["registered_reference"]["command_offset"]
                    assert new[claudio.BLOCK][:at] + b + new[claudio.BLOCK][at + len(c):] == old[claudio.BLOCK]
                edits.append(dict(id=row["id"], source_hex=a.hex(), previous_hex=b.hex(), installed_hex=c.hex()))
        else:
            old, new = (deck.yard.common_rows(raw[COMMON], raw[ARM]) for raw in (before, after))
            assert [a.message_id for a, b in zip(old, new, strict=True) if a.text != b.text] == [expected_id]
            assert revised["message_ID"] == expected_id and expected_id not in OPEN_IDS
            edits = deck.exact_review(release, review, clean, previous[3], image)
        image.replace_file(expected_file, before[expected_file])
        try:
            assert h(image.rom.save()) == previous[0]["candidate_sha256"]
        finally:
            image.replace_file(expected_file, after[expected_file])
        deltas.append(dict(profile=release["profile"], candidate_sha256=release["candidate_sha256"],
                           exact_predecessor_inverse=True, owned_path=expected_file, revised=revised["id"],
                           distinct_reviewed=len(edits), source_previous_installed=edits, evidence=refs))
        previous = successor
    return first[3], previous, deltas


def current_story(clean, anchor_rom, image, release, anchor):
    paths = (*ROUTES, HELP)
    blobs = {path: image.read_file(path) for path in paths}
    hashes = {path: h(data) for path, data in blobs.items()}
    for i, path in enumerate(ROUTES):
        assert hashes[path] == release[f"target_SC{i}_sha256"]
    assert hashes[HELP] == release["target_HELP_sha256"]
    assert {p for p in paths if hashes[p] != anchor["coverage"]["current_story_and_help_sha256"][p]} == {claudio.STORY}
    original, installed = ({p: IlnkContainer.parse(rom.read_file(p)).blocks for p in ROUTES} for rom in (clean, image))
    assert sum(map(len, original.values())) == sum(map(len, installed.values())) == 1307
    assert all(image.read_file(f"/data/EV{i}.DK4") == clean.read_file(f"/data/EV{i}.DK4") for i in range(4))
    arm, clean_arm = (rom.read_file(ARM) for rom in (image, clean))
    assert all(arm[lo:hi] == clean_arm[lo:hi] for lo, hi in events.ARCHIVE_LOADER_SPANS)
    priority = editorial.priority_bindings(original, installed)
    assert priority == anchor["coverage"]["priority_story_decisions"]

    packets = proof(prepared.OUT, anchor["candidate_sha256"])
    assert packets["all_source_current_installed_and_review_gates_bound"]
    for packet in packets["packets"]:
        path, block = packet["asset"], packet["block"]
        assert h(original[path][block]) == packet["original_block_sha256"]
        assert h(installed[path][block]) == packet["installed_block_sha256"]
        assert reference(packet["editorial_review"]["path"]) == packet["editorial_review"]
    intake = proof(wrap.OUT, anchor["candidate_sha256"])
    assert len(intake["linked"]) == intake["original_open_count"] == 277 and not intake["unresolved"]
    for item in intake["linked"]:
        path, block = item["intake"]["file_path"], item["intake"]["block"]
        prior, now = item["installed"], installed[path][block]
        offset, raw = prior["command_offset"], bytes.fromhex(prior["exact_command_hex"])
        assert now[offset:offset + len(raw)] == raw
        if h(now) != prior["block_sha256"]:
            assert (path, block) == (claudio.STORY, claudio.BLOCK)
            assert h(IlnkContainer.parse(anchor_rom.read_file(path)).blocks[block]) == prior["block_sha256"]
    flags = [{k: v for k, v in row.items() if k != "reviewed"} for row in anchor["coverage"]["bound_story_wrap_dispositions"]]
    scanner = deck.tunis.kurushima.scanner
    known = [row for row in flags if row["file_path"] == claudio.STORY]
    _, actual = scanner.scan(claudio.STORY, blobs[claudio.STORY])
    assert [flag for flag in actual if flag["block"] != claudio.BLOCK] == [
        flag for flag in known if flag["block"] != claudio.BLOCK]
    assert not [flag for flag in actual if flag["block"] == claudio.BLOCK]
    assert not [flag for flag in known if flag["block"] == claudio.BLOCK]
    return dict(story_and_help_sha256=hashes, story_positions=anchor["coverage"]["story_positions"],
                retail_event_routes=1307, verified_priority=priority,
                verified_packets=reference(prepared.OUT), prepared_texts=packets["prepared_story_texts"],
                distinct_priority_and_prepared_positions=packets["unique_priority_and_prepared_story_positions"],
                verified_wrap_intake=reference(wrap.OUT), carried_wrap_intake=277, active_progressive_flags=len(flags),
                unassigned_progressive_flags_in_scan=0, help_topics=202, help_continuations=15)


def current_common(clean, image, release, review, anchor):
    with mapped(deck.yard.LEDGER) as data:
        scope = value(data, "contextual_story_natural_dialogue_pass_v1871", 1)
        identity = value(data, "current_integrated_candidate", 1)
        assert identity["sha256"] == release["candidate_sha256"] and identity["profile"] == release["profile"]
        assert value(data, "records_editorially_completed", 1) == 27700
        assert value(data, "full_goal_complete", 1) is False
    keys = {(row["file_path"], row["id"]) for row in scope["integrated_record_keys"]}
    assert len(keys) == len(scope["integrated_record_keys"]) == 27700
    assert Counter(path for path, _ in keys) == anchor["coverage"]["historical_credits_by_path"]
    credited = {int(ident.rsplit("_", 1)[1]) for path, ident in keys if path == COMMON}
    arm, raw = image.read_file(ARM), image.read_file(COMMON)
    assert h(raw) == release["target_COMMON_sha256"]
    source = deck.tunis.common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    installed = deck.yard.common_rows(raw, arm)
    shared = review["shared_consumer_binding"]
    assert shared["candidate_sha256"] == release["candidate_sha256"]
    rows = {r["message_ID"]: r for r in shared["records"]}
    earlier = read(editorial.SHARED)
    assert len(rows) == earlier["scoped_shared_display_findings"] == 276
    assert not earlier["remaining_without_scoped_disposition"]
    assert credited.isdisjoint(rows) and credited | rows.keys() == set(range(len(installed)))
    for old in earlier["records"]:
        key = old["message_ID"]
        assert deck.yard.message_reference(source[key]) == old["source_reference"] and source[key].text.hex() == old["source_hex"]
        assert deck.yard.message_reference(installed[key]) == rows[key]["installed"]
        assert installed[key].text.hex() == old["installed_hex"]
    return dict(total=len(installed), contextual_credits=len(credited), scoped_shared=len(rows),
                exact_archived_artwork_identities_open=earlier["exact_archived_artwork_identities_open"],
                prior_evidence=reference(editorial.SHARED), historical_credits=len(keys)), installed


def current_package(release):
    with mapped(Path(release["manifest"])) as data:
        assert value(data, "candidate_sha256", 2) == release["candidate_sha256"]
        assert value(data, "profile", 2) == release["profile"]
        assert value(data, "release_stack_sha256", 2) == release["registry_sha256"] == digest(REGISTRY)
        checks = value(data, "checks", 2)
        batches = {p.replace("\\", "/") for p in value(data, "batches", 2)}
    with mapped(REGISTRY) as data:
        accepted = value(data, "accepted_layers", 2)
        assert value(data, release["profile"], 4)["status"] == "experimental"
    assert len(checks) == release["passing_release_checks"] == 481 and all(checks.values())
    assert len(batches) == release["registered_manifest_entries"] == 1146
    assert len(accepted) == release["accepted_layers"] == 114
    assert all(row["status"] == "accepted" and
               (row.get("baked_into_baseline") or row["batch"].replace("\\", "/") in batches) for row in accepted)
    startup = proof(release["own_registered_startup"], release["candidate_sha256"])
    assert startup["cold_boot"] and not startup["savestate"]
    assert len(startup["exact_matching_frames"]) == 6 and len(startup["original_protected_name_getters"]) == 24
    qa = current.VERIFY / "qa_passed.xml"
    suite, = ElementTree.parse(qa).iter("testsuite")
    assert [int(suite.get(key, "0")) for key in ("tests", "errors", "failures", "skipped")] == [17, 0, 0, 0]
    round_trip = current.VERIFY / "clean_patch_proof.json"
    patch = read(round_trip)
    assert patch["byte_exact"] and patch["clean_input_sha256"] == release["clean_input_sha256"] == digest(CLEAN)
    assert patch["candidate"]["sha256"] == patch["rebuilt"]["sha256"] == release["candidate_sha256"]
    assert patch["patch"]["sha256"] == release["patch_sha256"] == digest(release["patch"])
    plan = read(current.PLAN)
    assert plan["main_sha256"] == digest("translations/promoted_build.json")
    checksums = read(current.PACKAGE / "checksums.json")
    assert all(digest(current.PACKAGE / path) == expected for path, expected in checksums.items())
    drive = read(DRIVE)
    assert drive["verified"] and drive["sole_nds"] and drive["verified_package_files"] == len(checksums)
    assert drive["registered_candidate_sha256"] == drive["readback_sha256"] == release["candidate_sha256"]
    proof(CLEANUP, release["candidate_sha256"])
    return dict(accepted_layers=114, entries=1146, passing_checks=481, focused_tests=reference(qa),
                startup=reference(release["own_registered_startup"]), exact_reconstruction=reference(round_trip),
                drive=reference(DRIVE), cleanup=reference(CLEANUP), checked_package_files=len(checksums), main_promotion_pending=True)


def source_display_and_play(anchor_rom, image, release, installed, anchor):
    arm, old_arm = (rom.read_file(ARM) for rom in (image, anchor_rom))
    assert arm == old_arm and h(arm) == release["target_ARM9_sha256"]
    assert current.template.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    runtime = anchor["targeted_regressions"]
    assert runtime["Market_Goods_Info_current_protected_format_and_pointers"]
    assert runtime["default_names"]["original_default_getter_cases"] == 414
    julio = runtime["Julio"]
    scene = IlnkContainer.parse(image.read_file("/data/SC0.DK4")).blocks[julio["block"]]
    assert h(scene) == julio["block_sha256"]
    deck_asset = runtime["Deck"]
    assert h(image.read_file(deck_asset["asset"])) == deck_asset["asset_sha256"]

    archive_drafts = read(deck.ARCHIVED)["records"]
    assert [row["message_ID"] for row in archive_drafts] == list(OPEN_IDS)
    for row in archive_drafts:
        assert row["original_display_ownership_open"] and row["review"]["formatting"] is False
        assert installed[row["message_ID"]].text.hex() == row["installed_reference"]["exact_hex"]
    current_market = ROOT / "market_option_dispatch_current_20261125.json"
    assert set(proof(current_market, release["candidate_sha256"])["archived_records"]) == {"750", "751", "752"}
    azores = ROOT / "azores_trade_current_20261125.json"
    village = proof(azores, release["candidate_sha256"])
    assert village["ordinary_gameplay"] and len(village["records"]) == 4
    assert all(installed[row["message_ID"]].text.hex() == row["installed_reference"]["exact_hex"]
               for row in village["records"])
    reika = ROOT / "seoul_reika_reply_paired_20261125.json"
    paired = read(reika)
    assert paired["ordinary_gameplay"] and paired["candidate"]["sha256"] == release["candidate_sha256"]
    assert len(paired["matching_navigation_frames"]) == 22
    ranges = ROOT / "saved_fleet_events_current_20261124.json"
    fleet = read(ranges)
    assert len(fleet["ordinary_loads"]) == 2 and fleet["backup_inventory"]["event_type_counts"] == {"11": 3000}
    for span in fleet["source"]["exact_clean_installed_spans"]:
        assert h(arm[span["start"] - editorial.BASE:span["end"] - editorial.BASE]) == span["sha256"]
    return dict(exact_anchor_ARM9=True, inherited_renderer_and_name_proofs=reference(deck.OUT),
                recent_ordinary_play=[reference(azores), reference(reika)], current_market_native_cases=reference(current_market),
                archived_COMMON_display_owners_open=list(OPEN_IDS), archived_drafts=reference(deck.ARCHIVED),
                ordinary_Missionary_destination_trigger_open=True, save_ingress_scope=reference(ranges),
                additional_town_and_random_variants_remain_unvisited=True)


def main():
    release, anchor = map(read, (current.RELEASE, deck.OUT))
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    clean = NdsImage.open(CLEAN)
    anchor_rom, latest, deltas = original_deltas(clean, anchor)
    assert latest[0] == release
    _, review, _, image = latest
    story = current_story(clean, anchor_rom, image, release, anchor)
    common, installed = current_common(clean, image, release, review, anchor)
    package = current_package(release)
    display = source_display_and_play(anchor_rom, image, release, installed, anchor)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], starting_acceptance=reference(deck.OUT),
                    exact_registered_deltas=deltas, story_and_help=story, COMMON=common, release_tests=package,
                    display_and_gameplay=display, new_gameplay_runs=0, new_editorial_credit=0,
                    full_editorial_goal_complete=False))
    print("Verified all four successor inverses, the current story and COMMON inventory, and the Seoul release package.")


if __name__ == "__main__":
    main()
