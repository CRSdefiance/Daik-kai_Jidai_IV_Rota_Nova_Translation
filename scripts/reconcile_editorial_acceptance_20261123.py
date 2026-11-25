"""Recheck editorial acceptance evidence against the registered Online Card Copy ROM."""

import json
from collections import Counter
from hashlib import file_digest, sha256
from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.inventory_native_common_calls import direct_bl_target


RELEASES = Path("releases")
PACKAGE = RELEASES / "all_routes_editorial_20261123_online_card_copy_candidate"
CHECKPOINTS = Path("translations/editorial_checkpoints")
OUT = CHECKPOINTS / "shared_display_20261123/editorial_acceptance_20261123.json"
PRIORITY = CHECKPOINTS / "tavern_nearby_town_wrap_20261123/priority_story_reviews.json"
SHARED = OUT.with_name("shared_editorial_coverage_20261123.json")
DRIVE = CHECKPOINTS / "online_card_copy_20261123/drive_latest_build_receipt.json"
FACTION = CHECKPOINTS / "SharedText_20261110_v1/faction_information_visibility_20261115_v1.json"
ARM, COMMON, HELP = "/__arm9__.bin", "/COMMON/MESFILE.DK4", "/COMMON/HELP.DK4"
BASE = 0x02000000
GATES = {"source", "context", "localization", "naturalness", "formatting"}
ROUTES = (6887, 5356, 6720, 5129)


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    with Path(path).open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def reference(path):
    return {"path": Path(path).as_posix(), "sha256": digest(path)}


def priority_bindings(clean, installed):
    prior = read(PRIORITY)
    counts = Counter()
    for row in prior["records"]:
        asset, block = row["file_path"], row["block"]
        source = row["source_reference"]
        approved = row["approved_reference"]
        assert sha256(clean[asset][block]).hexdigest() == source["block_sha256"]
        raw = installed[asset][block]
        assert sha256(raw).hexdigest() == approved["block_sha256"]
        offset = approved["command_offset"]
        command = bytes.fromhex(approved["exact_command_hex"])
        assert raw[offset:offset + len(command)] == command
        assert set(row["review"]) == GATES and all(row["review"].values())
        counts[asset, block] += 1
    assert sum(counts.values()) == 416
    assert counts["/data/SC0.DK4", 49] == 61 and counts["/data/SC0.DK4", 84] == 131
    assert {block for (asset, block) in counts if asset == "/data/SC1.DK4"} == set(range(61, 71))
    assert prior["historical_difference_counts"] == {
        "exact_at_intake": 128, "spacing_at_intake": 1, "logical_difference_at_intake": 95,
    }
    return {"ledger": reference(PRIORITY), "exact_source_and_approved_blocks": 416,
            "groups": prior["entry_counts"], "hodram_comparison": prior["historical_difference_counts"]}


def native_row(clean, current, label, slot, literal, caller, sink, meaning):
    raw = label.encode("cp932") + b"\0"
    assert all(arm[slot:slot + len(raw)] == raw for arm in (clean, current))
    assert all(unpack_from("<I", arm, literal) == (BASE + slot,) for arm in (clean, current))
    assert clean[caller:caller + 8] == current[caller:caller + 8]
    instruction = unpack_from("<I", current, caller + 4)[0]
    assert direct_bl_target(instruction, BASE + caller + 4) == BASE + sink
    return {"source_Japanese": label, "source_meaning": meaning, "ARM9_offset": slot,
            "clean_and_current_hex": raw.hex(), "literal_offset": literal,
            "call_offset": caller + 4, "callee_address": BASE + sink,
            "ordinary_gameplay_confirmed": False}


def inspect_native(source, current):
    pirate = native_row(source, current, "海賊", 0x1305F4, 0xBC78, 0xBC40, 0xD5404,
                        "Pirate, the selected opponent's affiliation label.")
    assert source[0xBBFC:0xBC48] == current[0xBBFC:0xBC48]
    assert unpack_from("<I", current, 0xBC08) == (0xE3540015,)
    assert direct_bl_target(unpack_from("<I", current, 0xA63C)[0], BASE + 0xA63C) == BASE + 0xB854
    assert current[0x1305F4:0x1305FC] == bytes.fromhex("8a4391af00000000")
    pirate.update(opponent_affiliation=21, original_owner_entry=BASE + 0xB854,
                  original_owner_caller=BASE + 0xA63C, proposed_English="Pirate", slot_bytes=8,
                  status="Original portrait-panel branch reaches the draw routine. Focused display still required.")
    target = native_row(source, current, "目標街：%s", 0x1370F8, 0x3767C, 0x37664, 0xD5200,
                        "Target city followed by the current mission's destination name.")
    assert source[0x37624:0x37680] == current[0x37624:0x37680]
    assert unpack_from("<I", current, 0x37628) == (0xE3540073,)
    target.update(no_target_city_value=115, original_owner_entry=BASE + 0x37568,
                  status="The legacy fleet panel calls this formatter for a valid destination. DS visibility open.")
    finance = native_row(source, current, "収入額%8lu支出額%8lu投資額%8lu", 0x137118, 0x38E00,
                         0x38DA4, 0xD5200, "Income, expenses and investment, three unsigned values.")
    assert source[0x38D70:0x38E04] == current[0x38D70:0x38E04]
    finance.update(original_owner_entry=BASE + 0x38D28,
                   status="Legacy format is called after the finance getter succeeds. Earlier World Map replay used a separate English panel.")
    previous = read(FACTION)
    assert previous["complete_frames_match"] and len(previous["records"]) == 5
    old_release = read(RELEASES / "all_routes_editorial_20261115_ritual_officiant_labels_candidate"
                       / "verification/registered_release_verification.json")
    assert digest(old_release["candidate"]) == old_release["candidate_sha256"] == previous["candidate_sha256"]
    old = NdsImage.open(old_release["candidate"]).read_file(ARM)
    spans = ((0x3D650, 0x3D940), (0x137914, 0x137964))
    assert all(old[lo:hi] == current[lo:hi] for lo, hi in spans)
    return {"open_original_callers": [pirate, target, finance],
            "five_legacy_faction_fields": {"earlier_visibility_ledger": reference(FACTION),
                "exact_field_and_caller_spans": spans,
                "scope": "Earlier Inn and Fleet Info frame comparison. Other callers and current gameplay remain open."}}


def right_bound(arm, config):
    patches = read(config)["proof"]["patches"]
    sections = {section.ramAddress: section.data for section in MainCodeFile(arm, BASE).sections}
    itcm = patches[0]["offset"] - 0x21C
    for patch in patches:
        offset = patch["offset"]
        expected = bytes.fromhex(patch["after_hex"])
        if itcm <= offset < itcm + 4096:
            assert sections[0x01FFC000][offset - itcm:offset - itcm + len(expected)] == expected
        else:
            assert arm[offset:offset + len(expected)] == expected
    return {"configuration": reference(config), "matched_repair_spans": len(patches)}


def main():
    receipt_path = PACKAGE / "verification/registered_release_verification.json"
    release = read(receipt_path)
    checksums = read(PACKAGE / "checksums.json")

    def packaged(name):
        path = PACKAGE / name
        assert digest(path) == checksums[name]
        return path

    assert receipt_path == packaged("verification/registered_release_verification.json")
    rom = Path(release["candidate"])
    clean_path = Path("work/clean.nds")
    candidate = digest(rom)
    assert candidate == release["candidate_sha256"]
    assert digest(clean_path) == release["clean_input_sha256"]
    assert digest(release["manifest"]) == release["manifest_sha256"]
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    assert digest(packaged("translation.xdelta")) == release["patch_sha256"]
    assert release["clean_input_patch_byte_exact"] and release["whole_parent_inverse_exact"]
    startup = packaged("verification/own_startup_verification.json")
    assert digest(startup) == release["own_registered_startup_sha256"]
    startup_result = read(startup)
    assert startup_result["cold_boot"] and startup_result["candidate_sha256"] == candidate
    assert release["experimental_not_promoted"] and not release["own_registered_startup_pending"]
    drive = read(DRIVE)
    assert drive["sha256"] == candidate and rom.stat().st_size == drive["size_bytes"]
    assert drive["sole_nds_in_folder"] and drive["readback_verified"]

    clean, current = map(NdsImage.open, (clean_path, rom))
    route_path = packaged("verification/current_route_coverage_20261123.json")
    route_proof = read(route_path)
    route_origin = RELEASES / "all_routes_editorial_20261123_hodram_b261_b310_wrap_fixes_candidate"
    route_receipt = route_origin / "verification/registered_release_verification.json"
    route_release = read(route_receipt)
    assert digest(route_receipt) == read(route_origin / "checksums.json")["verification/registered_release_verification.json"]
    assert route_proof["candidate_sha256"] == route_release["candidate_sha256"]
    assert route_proof["registry_sha256"] == route_release["registry_sha256"]
    assert route_proof["manifest_prefix_exact"] and route_proof["exact_credited_clean_positions"] == sum(ROUTES)
    original_routes, installed_routes = {}, {}
    for index, count in enumerate(ROUTES):
        asset = f"/data/SC{index}.DK4"
        record = route_proof["routes"][asset]
        original_routes[asset] = IlnkContainer.parse(clean.read_file(asset)).blocks
        raw = current.read_file(asset)
        installed_routes[asset] = IlnkContainer.parse(raw).blocks
        assert sha256(raw).hexdigest() == record["installed_archive_sha256"] == release[f"target_SC{index}_sha256"]
        assert record["exact_credited_clean_positions"] == count
        census = record["source_census"]
        assert digest(census["path"]) == census["sha256"]
    priority = priority_bindings(original_routes, installed_routes)

    shared = read(SHARED)
    assert shared["candidate_sha256"] == candidate and not shared["remaining_without_scoped_disposition"]
    common = sha256(current.read_file(COMMON)).hexdigest()
    assert common == shared["verified_installed_COMMON_sha256"] == release["target_COMMON_sha256"]
    assert shared["scoped_shared_display_findings"] == 276 and shared["mapped_COMMON"] == 3668
    audit_path = packaged("verification/current_editorial_coverage_audit_20261123.json")
    old_audit = read(audit_path)
    previous_help = old_audit["inventory"]["original_Help"]
    source_help, current_help = (image.read_file(HELP) for image in (clean, current))
    assert [len(IlnkContainer.parse(raw).blocks) for raw in (source_help, current_help)] == [202, 217]
    assert sha256(current_help).hexdigest() == previous_help["installed_sha256"] == release["target_HELP_sha256"]
    source_arm, active_arm = (image.read_file(ARM) for image in (clean, current))
    assert sha256(active_arm).hexdigest() == release["target_ARM9_sha256"]

    result = {"candidate_sha256": candidate, "clean_input_sha256": release["clean_input_sha256"],
              "registered_release": reference(receipt_path), "route_coverage": reference(route_path),
              "route_coverage_origin": reference(route_receipt),
              "exact_credited_clean_story_positions": sum(ROUTES), "priority_reviews": priority,
              "shared_display_ledger": reference(SHARED), "shared_display_dispositions": 276,
              "shared_archived_artwork_identities_still_open": shared["exact_archived_artwork_identities_open"],
              "help_evidence": reference(audit_path), "original_help_topics": 202, "help_continuations": 15,
              "startup_receipt": reference(startup), "registered_patch": reference(release["patch"]),
              "registered_ASCII_right_bound": right_bound(active_arm, release["right_bound_configuration"]),
              "drive_receipt_at_last_verified_upload": reference(DRIVE),
              "native_text_followups": inspect_native(source_arm, active_arm),
              "new_editorial_credit": 0, "new_gameplay": False, "full_editorial_goal_complete": False}
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if OUT.exists():
        assert OUT.read_text(encoding="utf-8") == output
    else:
        OUT.write_text(output, encoding="utf-8", newline="\n")
    print("Rechecked 416 priority decisions, four route archives, the Help archive, and three original UI call paths.")


if __name__ == "__main__":
    main()
