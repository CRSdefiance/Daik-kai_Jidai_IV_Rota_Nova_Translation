"""Bind the tested DS fleet, voyage, and Quit paths to the current release."""

from pathlib import Path

from scripts import checkpoint_exhibition_quit_warning_20261115 as exhibition
from scripts import register_title_reports_label_20261123 as reports
from scripts import verify_current_regional_orders_20261123 as regional
from scripts.reconcile_legacy_setup_and_recruitment_20261123 import (
    OUT as PREVIOUS, WORKLIST, base, common_message_entries, current, native,
    owned_entries, picture, reference, stored_record, DIRECTORY_OFFSET, TABLE_OFFSET,
)


BASE = 0x02000000
OUT = PREVIOUS.with_name("legacy_fleet_and_quit_paths_20261123.json")
WARNING = OUT.with_name("legacy_warning_paths_20261123.json")
SYRACUSE = OUT.with_name("regional_attack_syracuse_20261123.json")
DISCOVERY = PREVIOUS.parent.parent / "SharedText_20261110_v1/port_discovery_consumers_20261115_v1.json"
FINDINGS = {
    284: "The tested DS Disband shortfall path confirms the closure, explains the shortfall, and docks the ships with three separate COMMON messages.",
    287: "The two stock port-discovery callers pass the selected port name to COMMON 297. The separate lookout exchange retains its excited delivery.",
    300: "The DS regional Attack Town action asks which town to attack through COMMON 131. The tested player-fleet sailing action independently confirms the selected town.",
    304: "Regional Attack Town rejects a contract held by any faction not at war with the player. The tested sailing selector has its own no-target panel.",
    318: "The stock in-game Quit selector loads COMMON 319 for the active-session flag, with positive and cancelled confirmation paths.",
}


def bind_text(row, source, installed):
    key = row["message_ID"]
    assert reference(source[key]) == row["source_reference"]
    assert reference(installed[key]) == row["installed_reference"]
    assert source[key].text.hex() == row["source_hex"]
    assert installed[key].text.hex() == row.get("installed_hex", row.get("current_hex"))
    assert all(row["review"].values()) and row["decision"] == "retention"


def check_pairs(requests, ids):
    assert [row["message_ID"] for row in requests] == [key for key in ids for _ in range(2)]
    for get, copy in zip(requests[::2], requests[1::2], strict=True):
        assert get["PC"] == 0x0205528C and copy == get | {"PC": 0x020534F4}


def check_warning_paths(receipt, ja, en, source, installed, archived):
    disband, quit_path = (receipt[key] for key in ("disband_shortfall", "quit_path"))
    for warning in receipt["stored_warning_leads"]:
        row = archived[warning["message_ID"]]
        for field in ("source_reference", "installed_reference", "source_hex", "installed_hex"):
            assert row[field] == warning[field]
        assert row["source_review"] == warning["draft"] and warning["display_caller_open"]
    assert disband["focused_emulator_test"] and disband["original_inputs"] and not disband["earned_finance"]
    check_pairs(disband["selected_messages"], [280, 281, 285, 281, 285, 286])
    assert disband["verified_return_with_wallet_at_zero"] and not disband["requested_284"]
    assert disband["states"]["11800"]["gold"] == 0
    for panel in disband["held_panels"]:
        bind_text(panel, source, installed)
        assert panel["body_ink"] > 0
        picture(panel["screenshot"])
    start, end = exhibition.HELPER - BASE, exhibition.SELECTOR_END - BASE
    assert ja[start:end] == en[start:end]
    assert [(row["flag"], row["COMMON_argument"]) for row in quit_path["native_selector_cases"]] == [
        (0, None), (1, 319), (2, None), (0x7FFFFFFF, None), (0x80000000, None), (0xFFFFFFFF, None)]
    native_template = quit_path["native_template"]
    assert native_template["native_lookup"] == [319]
    assert bytes.fromhex(native_template["complete_template_hex"]) == installed[319].text + b"\0"
    bind_text(quit_path["retained"], source, installed)
    observed = quit_path["prior_ordinary_quit_and_cancel"]
    assert observed["common_ID"] == 319 and observed["complete_glyph_ink"] > 0
    assert observed["source_reference"] == reference(source[319])
    prior = quit_path["evidence"]
    assert base.digest(prior["path"]) == prior["sha256"]
    proof = base.load(Path(prior["path"]))["normal_quit"]
    assert proof["reused_actual_quit_evidence"] == observed
    assert proof["exact_active_template"]["complete_template_hex"] == native_template["complete_template_hex"]
    earlier_ref, installed_ref = observed["current_reference"], reference(installed[319])
    assert earlier_ref | {"record_index": installed_ref["record_index"]} == installed_ref
    check_pairs(observed["trace"], [319])
    for label in ("confirmation", "cancelled"):
        picture(observed[label])
    return dict(focused_disband_holds=len(disband["held_panels"]), disband_active_ids=[280, 281, 285, 286],
        disband_supplied_finance=True, quit_native_cases=len(quit_path["native_selector_cases"]),
        quit_active_id=319, stock_quit_selector_sha256=native.digest(en[start:end]), quit_ordinary_evidence=True)


def check_discovery(ja, en, source, installed):
    voyage, calls = map(base.load, (regional.VOYAGE, DISCOVERY))
    assert voyage["candidate_sha256"] == base.load(regional.TAVERN.RELEASE)["candidate_sha256"]
    case = voyage["cases"]["tripoli_arrival"]
    assert case["ordinary_input_only_saved_gameplay"] and "287" not in case["requests_by_id"]
    observed = {r["message_ID"]: r for r in case["holds"] if r["message_ID"] in (1296, 297)}
    assert len(observed) == 2 and observed[297]["observed_lines"] == ["Discovered Crete."]
    assert observed[1296]["screenshot"]["frame"] < observed[297]["screenshot"]["frame"]
    for row in observed.values():
        bind_text(row, source, installed)
        check_pairs(row["requests"], [row["message_ID"]])
        picture(row["screenshot"])
    port_calls = [row for row in calls["offline_native_cases"] if row["message_ID"] == 297]
    assert len(port_calls) == 2
    for row in port_calls:
        start, end = row["first_instruction"] - BASE, row["call_instruction"] + 4 - BASE
        assert ja[start:end] == en[start:end] == bytes.fromhex(row["original_caller_hex"])
        assert row["complete_relevant_instructions_executed"]
    return dict(saved_ordinary_play=True, observed=[observed[1296], observed[297]],
        stock_caller_addresses=[row["first_instruction"] for row in port_calls],
        prior_substitution_tests=114)


def check_attack(active, ja, en, source, installed):
    policy, syracuse, release = map(base.load, (regional.OUTPUT, SYRACUSE, reports.RELEASE))
    assert policy["candidate_sha256"] == syracuse["candidate_sha256"] == release["candidate_sha256"] == base.digest(reports.ROM)
    old = base.NdsImage.open(reports.ROM)
    assert old.read_file(current.ARM) == en
    assert old.read_file("/GRP/KANJI.FNT") == active.read_file("/GRP/KANJI.FNT")
    old_common = owned_entries(old.read_file(current.COMMON), en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    assert policy["ordinary_inputs_with_prepared_regional_fleet_save"] and not policy["synthetic_during_current_replay"]
    for row in policy["records"]:
        bind_text(row, source, installed)
        assert old_common[row["message_ID"]] == installed[row["message_ID"]]
        if "ordinary_replay_capture" in row:
            assert row["full_mask"]["complete_native_mask"]
            picture(row["ordinary_replay_capture"])
    branches = policy["offline_regional_policy_branches"]
    for ref in branches["code"]:
        start, end = ref["start"] - BASE, ref["end"] - BASE
        assert ja[start:end] == en[start:end] and native.digest(en[start:end]) == ref["sha256"]
    state = [r for r in branches["input_branch_matrix"] if r["mission"] == 5]
    assert all(len(r["picker_call"]) == 1 and r["picker_call"][0][0] == 131 for r in state)
    assert [[call[0] for call in r["refusal_call"]] for r in state] == [[132], [134], [133], [133], [], [133], []]
    bind_text(syracuse | dict(message_ID=133, source_reference=syracuse["source_text_reference"],
        installed_reference=syracuse["installed_text_reference"]), source, installed)
    check_pairs(syracuse["original_paired_requests"], [131, 133, 131])
    assert syracuse["complete_ink"]["complete_native_mask"] and syracuse["original_inputs"]
    shot = syracuse["screenshot"]
    picture(shot | {"PNG_sha256": shot["sha256"]})
    sailing = policy["historical_neutral_and_allied_sailing"]
    assert sailing["neutral_v2"]["requests"][-1] == 2122
    assert all({300, 304}.isdisjoint(row["requests"]) for row in sailing.values())
    for row in sailing.values():
        picture(row["frame"])
    no_target = regional.no_target_path(en)
    assert no_target["english"] == sailing["allied_v2"]["visible_English"]
    archived_no_target, = [row["separate_sailing_no_target"] for row in policy["pending_records"] if row["message_ID"] == 304]
    assert no_target == archived_no_target
    return dict(regional_controls_with_prepared_fleet_save=True, regional_offline_cases=len(branches["input_branch_matrix"]),
        regional_attack_picker_id=131, regional_refusal_ids=[132, 133, 134], syracuse=syracuse["screenshot"],
        separate_historical_sailing=sailing, no_target=no_target)


def main():
    release, review, previous, inventory, warning = map(base.load, (current.RELEASE, current.REVIEW, PREVIOUS, WORKLIST, WARNING))
    assert base.digest(current.ROM) == release["candidate_sha256"] == review["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"] == inventory["clean_sha256"] == warning["clean_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    tavern = regional.TAVERN
    assert base.digest(tavern.ROM) == base.load(tavern.RELEASE)["candidate_sha256"] == warning["candidate_sha256"]
    clean, active, old = map(base.NdsImage.open, (native.CLEAN, current.ROM, tavern.ROM))
    before, after = map(native.files, (old, active))
    assert before.keys() == after.keys()
    differences = sorted(path for path in before if before[path] != after[path])
    assert set(differences) == {f"/FLS/M{n}.fls" for n in range(29, 33)} | {
        "/_pxl/online/Online61.pxl", "/_pxl/online/Online62.pxl", current.COMMON, "/__arm9__.bin"}
    ja, en = (img.read_file(current.ARM) for img in (clean, active))
    common = active.read_file(current.COMMON)
    previous_arm = old.read_file(current.ARM)
    arm_changes = [offset for offset, (a, b) in enumerate(zip(previous_arm, en, strict=True)) if a != b]
    assert arm_changes == [reports.stage.FIELD + 6]
    assert native.digest(en) == release["target_ARM9_sha256"]
    assert native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    previous_common = owned_entries(old.read_file(current.COMMON), previous_arm,
        native.digest(previous_arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    common_changes = [key for key, (a, b) in enumerate(zip(previous_common, installed, strict=True)) if a.text != b.text]
    assert common_changes == [649, 664, 671, 774, 775, 805, 809, 826]
    assert all(previous_common[key] == installed[key] for key in (280, 281, 285, 286, 297, 319, 1296))
    worklist = {r["message_ID"]: r for r in inventory["records"]}
    binding = {r["message_ID"]: r for r in review["shared_consumer_binding"]["records"]}
    open_keys = set(previous["remaining_without_scoped_disposition"])
    assert len(open_keys) == 27 and FINDINGS.keys() <= open_keys and len(worklist) == len(binding) == 276
    rows = {key: stored_record(key, source, installed, worklist, binding) | {"verified_scoped_path": note}
            for key, note in FINDINGS.items()}
    warning_proof = check_warning_paths(warning, ja, en, source, installed, rows)
    discovery_proof = check_discovery(ja, en, source, installed)
    attack_proof = check_attack(active, ja, en, source, installed)
    remaining = sorted(open_keys - rows.keys())
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], source_storage_inventory=len(worklist),
        reviewed_entries=list(rows.values()), remaining_without_scoped_disposition=remaining,
        retained_path_evidence=dict(warnings=warning_proof, discovery=discovery_proof, attack=attack_proof),
        prior_replay_candidate_sha256=warning["candidate_sha256"], distinct_internal_files_since_prior=differences,
        unrelated_title_label_ARM9_byte_offsets=arm_changes, unrelated_COMMON_body_changes=common_changes,
        current_gameplay_replays=0, new_ROM=False, new_editorial_credit=0, hardware=False,
        direct_COMMON_references_remain_tracked=True,
        evidence={str(path): base.digest(path) for path in (PREVIOUS, WORKLIST, WARNING, SYRACUSE,
            regional.VOYAGE, regional.OUTPUT, DISCOVERY, current.RELEASE, current.REVIEW,
            tavern.RELEASE, reports.RELEASE, Path(__file__))}))
    print(f"Verified {len(rows)} further scopes on the current release; {len(remaining)} still await a scoped disposition.")


if __name__ == "__main__":
    main()
