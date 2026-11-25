"""Resolve the two number-format dependencies found in the current caller audit."""

from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP

from dk4tool.patch.inn_numerals_20261119 import BASE, END, HELPER, ITCM, NUMBER, target
from scripts import reconcile_shared_call_inventory_20261123 as scope
from scripts.probe_button_prompt_native import STACK, VIEW, machine
from scripts.seal_shared_text_source_v1 import reference


base, current = scope.base, scope.current
OUT = scope.ROOT / "shared_number_call_followups_20261123.json"
POWER = Path("releases/all_routes_editorial_20261121_power_and_gold_digits_candidate")
CREW = Path("releases/all_routes_editorial_20261120_recruit_crew_candidate")
DECK = scope.BOOK / "deck_assignment_empty_dialogue_tables_20261119_v2.json"


def certified(package, name):
    rel = f"verification/{name}.json"
    path = package / rel
    assert base.digest(path) == base.load(package / "checksums.json")[rel]
    return path, base.load(path)


def local_calls(arm):
    cpu = machine(arm)
    caller, endpoint = 0x020BC14C, 0x020BC154
    cases = []
    for quantity, off in ((1, 0), (105, 0x100), (2147483647, 0x200)):
        pointer = VIEW + off
        cpu.reg_write(UC_ARM_REG_R0, pointer)
        cpu.emu_start(caller, endpoint, count=3)
        assert cpu.reg_read(UC_ARM_REG_PC) == endpoint
        assert (cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1)) == (288, pointer)
        cases.append(dict(number_return_pointer=pointer, example_positive_value=quantity,
                          message_ID=288, argument_pointer=pointer))
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.emu_start(0x02057524, 0x0205752C, count=3)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x0205752C
    assert unpack_from("<I", cpu.mem_read(STACK + 0x28, 4))[0] == 904
    cpu.mem_write(STACK + 0x24, VIEW.to_bytes(4, "little"))
    cpu.reg_write(UC_ARM_REG_R0, VIEW + 0x300)
    cpu.emu_start(0x020575E4, 0x020575F0, count=4)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x020575F0
    assert (cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2)) == (VIEW, 904, VIEW + 0x300)
    return dict(power=cases, volunteers=dict(message_ID=904, original_stack_slot=0x28,
        number_return_pointer=VIEW+0x300, wrapper_call=0x020575F0))


def main():
    assert not OUT.exists()
    release, audited = map(base.load, (current.RELEASE, scope.OUT))
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"] == audited["candidate_sha256"]
    assert base.digest(current.stage.CLEAN) == release["clean_input_sha256"]
    clean, active = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    ja, en = (item.read_file(current.ARM) for item in (clean, active))
    unresolved, = audited["bounded_arguments"]["unresolved_current_windows"]
    assert unresolved["address"] == 0x020BC154 and unresolved["prior_ids"] == [288]
    references = audited["native_dependency_comparisons"]["references"]["changed_dependencies"]
    assert [(x["start"], x["end"]) for x in references] == [(0x02057524, 0x020575F4)]
    source = current.stage.town.common_message_entries(clean.read_file(current.COMMON), ja)
    entries = current.parent.parent.stage.observed.prior.shared.paired.prior.entries(active)
    lock_paths = []
    records = []
    for key, change, start, end, wrapper, package, evidence_field in (
        (288, 0x020BC148, 0x020BC114, 0x020BC158, 0x020546B8, POWER, "original_call_bindings"),
        (904, 0x020575E0, 0x02057524, 0x020575F4, 0x02053DCC, CREW, "calls"),
    ):
        path, installed = certified(package, "staged")
        review_path, review = certified(package, "registered_review")
        lock_paths.extend((path, review_path))
        at = change - BASE
        row, = [x for x in installed[evidence_field] if x.get("number_call", x.get("address")) == change]
        assert ja[at:at+4].hex() == row["original_hex"]
        assert en[at:at+4].hex() == row.get("revised_hex", row.get("current_hex"))
        assert target(ja, at) == NUMBER and target(en, at) == HELPER
        assert target(ja, end-BASE-4) == target(en, end-BASE-4) == wrapper
        assert ja[start-BASE:at] == en[start-BASE:at] and ja[at+4:end-BASE] == en[at+4:end-BASE]
        prose, = [item for item in review["records"] if item["message_ID"] == key]
        jp, actual = source[key], entries[key]
        assert prose["source_hex"] == jp.text.hex() and jp.text.count(b"%s") == actual.text.count(b"%s") == 1
        assert " ".join(actual.text.decode("ascii").split()) == prose["english"]
        assert all(prose["review"].values())
        records.append(dict(message_ID=key, source_reference=reference(jp), installed_reference=reference(actual),
            source_hex=jp.text.hex(), installed_hex=actual.text.hex(), english=prose["english"], decision="retention",
            prior_review=str(review_path), original_choice_and_argument_count_preserved=True,
            localization_note=prose["localization_note"], review=prose["review"]))

    outcome, current_outcome = map(local_calls, (ja, en))
    assert outcome == current_outcome
    helper_source, = [Path(p) for p in base.load(lock_paths[0])["evidence"] if p.endswith("native_wrap.json") or "inn" in p.lower()]
    helper_info = base.load(helper_source)
    section, = [part for part in MainCodeFile(en, BASE).sections if part.ramAddress == ITCM]
    native_helper = bytes(section.data[HELPER - ITCM:END - ITCM])
    assert native_helper.hex() == helper_info["helper_hex"]

    # The normal-assignment exceptions were already proved. Rebind the retail
    # guards for the current build and keep the historical model scope explicit.
    original_deck = base.load(DECK)
    deck_locks = [(start, end) for start, end in ((0x7AD4, 0x7B3C), (0x134BC, 0x134D0), (0x81FA4, 0x81FEC),
                   (0x132C0, 0x132CC), (0x12130, 0x12254), (0x7EF28, 0x7EF68))]
    assert all(ja[lo:hi] == en[lo:hi] for lo, hi in deck_locks)
    assert [row["role"] for row in original_deck["role_assignment_gate"] if not row["assignable"]] == [9, 10, 11, 21, 22, 24]
    for row in original_deck["seat_14_guard"]:
        assert row["accepted_at_original_seat_14_guard"] == [row["captain"]]
    metrics = original_deck["stock_model_evidence"]
    assert metrics["role_cases"] == 154 * 31
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        inherited_full_census_sha256=base.digest(scope.OUT), scoped_number_message_records=records,
        changed_formatter_dependencies_reconciled=[0x020BC154, 0x020575F0], current_local_requests=current_outcome,
        number_helper_register_code_sha256=current.native.digest(native_helper), remaining_changed_bounded_argument_findings=0,
        normal_deck_guard_reuse=dict(code_spans=deck_locks, exact_clean_bytes=True,
            historical_model_slots_checked=metrics["role_cases"], scope="Normal assignment and the original historical stock model snapshot."),
        new_gameplay_runs=0, new_editorial_credit=0, pending_stored_entries=276,
        evidence={str(path): base.digest(path) for path in (scope.OUT, *lock_paths, helper_source, DECK)}))
    print("Verified the original COMMON 288 and 904 selections with both registered width corrections in place.")


if __name__ == "__main__":
    main()
