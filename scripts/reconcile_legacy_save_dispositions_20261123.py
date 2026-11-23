"""Verify two original DS save paths without changing the stored legacy copies."""

from scripts import checkpoint_continue_legacy_calls_20261115 as continue_review
from scripts import checkpoint_ending_save_20261120 as ending_review
from scripts.reconcile_opening_label_dispositions_20261123 import (
    OUT as OPENING, WORKLIST, base, common_message_entries, current, native, owned_entries, reference,
)
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET


OUT = OPENING.with_name("legacy_save_dispositions_20261123.json")
ENDING_PLAYBACK = current.REVIEW.with_name("verified_playback.json")


def storage(key, source, installed, inventory, ledger, older):
    entry = inventory[key]
    jp, en = source[key], installed[key]
    assert reference(jp) == entry["source_reference"]
    assert reference(en) == entry["installed_reference"] == ledger[key]["installed"]
    assert ledger[key]["exact_body_retained"]
    assert jp.text.hex() == entry["source_hex"] and en.text.hex() == entry["installed_hex"] == older["current_hex"]
    return dict(message_ID=key, file_path=current.COMMON, source_reference=reference(jp),
        installed_reference=reference(en), clean_Japanese=jp.text.decode("cp932"), clean_hex=jp.text.hex(),
        installed_English=en.text.decode("ascii"), installed_hex=en.text.hex(),
        historical_manuscript_review=entry["earlier_draft"], other_direct_COMMON_consumers_unverified=True)


def main():
    release, review, prior = map(base.load, (current.RELEASE, current.REVIEW, OPENING))
    candidate = release["candidate_sha256"]
    assert base.digest(current.ROM) == review["candidate_sha256"] == prior["candidate_sha256"] == candidate
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    source_arm, arm = (i.read_file(current.ARM) for i in (clean, rom))
    source = common_message_entries(clean.read_file(current.COMMON), source_arm)
    common = rom.read_file(current.COMMON)
    assert native.digest(common) == release["target_COMMON_sha256"]
    assert native.digest(arm) == release["target_ARM9_sha256"]
    installed = owned_entries(common, arm, native.digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    inventory = {r["message_ID"]: r for r in base.load(WORKLIST)["records"]}
    ledger = {r["message_ID"]: r for r in review["shared_consumer_binding"]["records"]}

    previous = base.load(continue_review.OUTPUT)
    case = continue_review
    for lock in previous["verified_code_spans"]:
        lo, hi = (lock[k] - case.BASE for k in ("start", "end"))
        assert source_arm[lo:hi] == arm[lo:hi] and native.digest(arm[lo:hi]) == lock["sha256"]
    sink = case.SINK - case.BASE
    assert source_arm[sink:sink + 4] == arm[sink:sink + 4] == bytes.fromhex("1eff2fe1")
    runtime = case.RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=3)
    offline = [case.branch_execution(runtime, installed, *p["offline_supplied_branch_inputs"])
               for p in previous["controlled_offline_cases"]]
    assert [r["loaded_ids"] for r in offline] == [[111], [112, 111], [112], []]
    assert [r["immediate_no_write_returns"] for r in offline] == [
        r["immediate_no_write_returns"] for r in previous["controlled_offline_cases"]]
    missing = storage(111, source, installed, inventory, ledger, previous["records"][0])
    missing.update(disposition="The native missing-save branch fetches the text and immediately discards it.",
        retention_reason="The existing sentence preserves that game data is absent and unavailable to load.",
        verified_offline_branches=offline, native_runtime=runtime.receipt())

    ending = base.load(ending_review.OUTPUT)
    legacy = storage(119, source, installed, inventory, ledger, ending["legacy_memory_card"])
    visible, = [r for r in ending["records"] if r.get("message_ID") == 316]
    assert visible["source_hex"] == source[316].text.hex() and visible["current_hex"] == installed[316].text.hex()
    assert visible["source_reference"] == reference(source[316])
    assert visible["current_reference"] == reference(installed[316])
    assert all(visible["review"].values())
    lo, hi = (n - case.BASE for n in ending["exact_end_selector_call_span"])
    assert source_arm[lo:hi] == arm[lo:hi]
    assert arm[lo:hi].hex() == "4f0fa0e3db5800eb000050e30200000a04108de20500a0e15c0200eb"
    playback = base.load(ENDING_PLAYBACK)
    assert playback["candidate_sha256"] == candidate and playback["actual_focused_playback"]
    holds = {r["captain"]: r["complete_ending_save_prompt"] for r in playback["records"]}
    assert set(holds) == {"Rafael", "Hodram", "Lil", "Maria"}
    assert all(r["text"] == visible["current_English"] and r["complete_ink_and_blank_cells_exact"] for r in holds.values())
    legacy.update(disposition="The cartridge ending prompt is separately supplied by COMMON 316 on the verified DS path.",
        retained_displayed_prompt=visible, exact_clean_and_current_selector_sha256=native.digest(arm[lo:hi]),
        one_byte_state_fixture_ending_holds=holds)

    before = set(prior["remaining_needing_distinct_disposition"])
    checked = {111, 119}
    assert checked <= before
    base.save(OUT, dict(candidate_sha256=candidate, source_storage_inventory=len(inventory),
        label_dispositions=[missing, legacy], remaining_needing_distinct_disposition=sorted(before - checked),
        new_gameplay_runs=0, new_dialogue_credit=0, global_absence_claim=False,
        evidence={str(p): base.digest(p) for p in (OPENING, WORKLIST, current.RELEASE, current.REVIEW,
            continue_review.OUTPUT, ending_review.OUTPUT, ENDING_PLAYBACK)}))
    print(f"Verified the missing-save and ending-save paths; {len(before - checked)} shared entries remain.")


if __name__ == "__main__":
    main()
