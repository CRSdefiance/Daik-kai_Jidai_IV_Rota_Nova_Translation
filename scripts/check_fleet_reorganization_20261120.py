"""Bind the Fleet Setup decision branches and the stored debt-warning lead."""

from collections import Counter
from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3

from scripts import checkpoint_fleet_debt_disband_20261115 as disband
from scripts import observe_fleet_reorganization_20261120 as run
from scripts.checkpoint_pending_shared_native_20261115 import branch_hits, components
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.native_call_abi_v764 import call
from scripts.replay_lil_ceramics_wrap_20261111 import photos
from scripts.verify_personal_gameplay_v841 import get_machine
from dk4tool.dialogue.font_audit import GameAsciiFont


base, current, ROOT = run.current.base, run.current, run.ROOT
ARM, COMMON, CLEAN = current.stage.ARM, current.stage.COMMON, current.stage.CLEAN
BOOK = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
OUTPUT = BOOK / "fleet_reorganization_scope_20261120_v1.json"
DISBAND_SCOPE = BOOK / "fleet_disband_shortfall_20261120_v1.json"
BASE, ENTRY = 0x02000000, 0x0205A388
PICKER, TRANSFER, QUESTION, ORDERS = 0x0205A4B4, 0x020A4C9C, 0x0205466C, 0x0208AB88
DEBT_SINK = 0x0203FA9C
CHOICES = ((64, False, False), (57, False, False), (57, True, False), (57, True, True))
REASON = {
    280: ("Choose which fleet to reorganize.", "The short instruction identifies the operation and prepares the player to select an existing fleet."),
    283: ("The players are asked whether to change the reorganized fleet's orders.", "The direct question follows the fleet edit and prepares both responses without implying that any orders already changed."),
}
STATES = (9640, 10840, 13540, 16240, 16540, 16840)
HOLDS = ((11440, 280), (14140, 280), (13240, 283), (15940, 283), (12940, None), (15640, None))


def source_scope(clean, active):
    ja, arm = [image.read_file(ARM) for image in (clean, active)]
    spans = ((0x5A27C, 0x5A528), (0x3FA9C, 0x3FAA0), (0x3CC80, 0x3CCD0))
    assert all(ja[lo:hi] == arm[lo:hi] for lo, hi in spans)
    assert arm[DEBT_SINK-BASE:DEBT_SINK-BASE+4] == bytes.fromhex("1eff2fe1")
    assert unpack_from("<I", arm, 0x5A4B0) == (283,)
    # The only aligned call to the no-op comes from Disband after the original
    # wallet lookup. The call receives the selected fleet index in r0.
    targets = {DEBT_SINK}
    matches = []
    for image in (clean, active):
        refs = [(name, pc, mode) for name, address, raw in components(image.rom)
                for pc, _, mode in branch_hits(raw, address, targets)]
        assert refs == [("ARM9 section 0", 0x0205A31C, "arm_bl")]
        matches.append(refs[0])
    assert arm[0x5A318:0x5A31C] == bytes.fromhex("0600a0e1")  # mov r0, r6
    return dict(exact_dependencies=[dict(start=BASE+lo, end=BASE+hi, sha256=current.batch.digest(arm[lo:hi]))
                                    for lo, hi in spans], sole_direct_clean_and_current_calls=matches,
                original_debt_stub=DEBT_SINK, original_immediate_return=True)


def model(arm, raw):
    cases = []
    for fleet_index, apply, change in CHOICES:
        cpu, state = disband.setup(raw, arm, 57)
        wallet = state["wallet"]
        before_gold = bytes(cpu.mem_read(wallet, 4))
        finance = state["finance"] + 0xC
        cpu.mem_write(wallet, pack("<I", 37))
        numeric_debt = pack("<3I", 100_500, 0, 0)
        cpu.mem_write(finance, numeric_debt)
        recorded = []

        def screen(core, pc, _size, _user):
            if pc == PICKER:
                assert core.reg_read(UC_ARM_REG_R1) == 0
                recorded.append(("reorganize_picker", fleet_index))
                core.reg_write(UC_ARM_REG_R0, fleet_index)
            elif pc == TRANSFER:
                work = core.reg_read(UC_ARM_REG_R0)
                assert core.reg_read(UC_ARM_REG_R1) == 0
                ships = unpack_from("<5I", bytes(core.mem_read(work, 20)))
                assert all(0 <= n <= 155 for n in ships) and any(n not in (0, 155) for n in ships)
                # Test the result when the user leaves the same ship in place.
                # The editor's ship-list sentinel is 155; its result array uses zero.
                core.mem_write(work, pack("<5I", *(0 if n == 155 else n for n in ships)))
                recorded.append(("ship_editor_return", apply))
                core.reg_write(UC_ARM_REG_R0, int(apply))
            elif pc == QUESTION:
                assert core.reg_read(UC_ARM_REG_R0) == 283
                recorded.append(("orders_question", 283))
                core.reg_write(UC_ARM_REG_R0, int(change))
            elif pc == ORDERS:
                assert [core.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)] == [57, 1, 0, 0]
                recorded.append(("open_orders", 57))
            else:
                raise AssertionError(f"Unexpected shared-text or payment call at {pc:#x}")
            core.reg_write(UC_ARM_REG_PC, core.reg_read(UC_ARM_REG_LR))

        for pc in (PICKER, TRANSFER, QUESTION, ORDERS, 0x020546B8, 0x0205528C, DEBT_SINK, 0x0203CC80):
            cpu.hook_add(UC_HOOK_CODE, screen, begin=pc, end=pc)
        call(cpu, ENTRY - BASE, (), instruction_limit=200000)
        assert recorded == ([('reorganize_picker', fleet_index)] +
            ([('ship_editor_return', apply)] if fleet_index != 64 else []) +
            ([('orders_question', 283)] if apply else []) + ([('open_orders', 57)] if change else []))
        assert bytes(cpu.mem_read(wallet, 4)) == pack("<I", 37)
        assert bytes(cpu.mem_read(finance, 12)) == numeric_debt
        cases.append(dict(picker_result=fleet_index, apply_ships=apply, edit_orders=change, calls=recorded,
            source_fixture_wallet=int.from_bytes(before_gold, "little"), supplied_gold=37, supplied_fleet_expenses=100500,
            wallet_and_finance_unchanged=True))
    return cases


def native_inputs(report, frame):
    snap, = [r for r in report["read_only_pause_RAM_snapshots"] if r["frame"] == frame]
    raw = Path(snap["path"]).read_bytes()
    assert len(raw) == 0x400000 and snap["read_only_export"] and current.batch.digest(raw) == snap["sha256"]
    return snap, raw


def hold_text(img, font, paragraph):
    for x in (16, 22):
        try:
            return font_mask(img, font, paragraph, x, 297, (16, 294, 244, 351), (0, 8, 0))
        except AssertionError:
            pass
    raise AssertionError(paragraph)


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"] and base.digest(CLEAN) == release["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    clean, active = map(base.NdsImage.open, (CLEAN, current.ROM))
    ja, arm = [im.read_file(ARM) for im in (clean, active)]
    scope = source_scope(clean, active)
    old_path = Path(base.load(DISBAND_SCOPE)["original_native_arithmetic_proof"])
    old_proof = base.load(old_path)
    assert all(ja[lo:hi] == arm[lo:hi] for lo, hi in old_proof["exact_clean_native_spans"])

    report_path = ROOT / "capture/capture_report.json"
    trace_path = ROOT / "observer/requests.json"
    report, log = map(base.load, (report_path, trace_path))
    assert report["ROM_sha256"] == release["candidate_sha256"] and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    assert donor["source_sha256"] == base.load(run.PREFIX)["battery_save_preloaded"]["source_sha256"]
    prefix = base.load(ROOT / "prefix_inputs.json")
    assert prefix == [r for r in base.load(run.PREFIX)["scripted_input_schedule"] if r["start"] < run.START]
    verify_schedule = FunctionType(run.navigation.verified_schedule.__code__,
                                   vars(run.navigation) | {"START": run.START})
    applied = verify_schedule(ROOT, prefix, report)
    assert len(applied) == 24 and report["frames"] == STATES[-1]
    assert log["all_host_slots_restored_and_core_file_exact"] and not log["errors"] and not log["mismatches"]
    requests = log["source_requests"]
    counts = Counter(row["message_ID"] for row in requests)
    assert counts == {280: 6, 283: 4} and not counts[284]
    assert [row["message_ID"] for row in requests if row["PC"] == 0x0205528C] == [280, 280, 283, 280, 283]
    assert all({a["PC"], b["PC"]} == {0x0205528C, 0x020534F4} and a["frame"] == b["frame"]
               for a, b in zip(requests[::2], requests[1::2], strict=True))

    evidence = {str(path): base.digest(path) for path in (report_path, trace_path, run.PREFIX, old_path, DISBAND_SCOPE,
        ROOT / "capture/navigation_command_journal.json", ROOT / "observer/source_contract.json")}
    states = []
    for frame in STATES:
        snap, raw = native_inputs(report, frame)
        evidence[snap["path"]] = snap["sha256"]
        _, field = disband.setup(raw, arm, 57)
        _, get = get_machine(arm, raw)
        fleet = field["fleet"]
        slots = [get(0x36C94, fleet + 0xC + 8*i) != 0 for i in range(5)]
        gold = disband.field(raw, field["wallet"])
        assert gold == 897400 and slots == [True, False, False, False, False]
        assert get(0x36914, fleet) == 1
        states.append(dict(frame=frame, company_gold=gold, occupied_slots=sum(slots), fleet_active=True))
    _, raw = native_inputs(report, STATES[0])
    controls = model(arm, raw)

    b = current.batch
    source = b.common_message_entries(clean.read_file(COMMON), ja)
    table = b.owned_entries(active.read_file(COMMON), arm, b.digest(arm[b.DIRECTORY_OFFSET:b.TABLE_OFFSET]))
    quote = 0x152BB0
    assert unpack_from("<I", ja, 0xA5024) == unpack_from("<I", arm, 0xA5024) == (BASE + quote,)
    source_prompt = ja[quote:quote + 32].split(b"\0", 1)[0]
    current_prompt = arm[quote:quote + 32].split(b"\0", 1)[0]
    assert source_prompt.decode("cp932") == "これでよろしいですか？" and current_prompt == b"Is this okay?"
    frames = photos(report)
    font = GameAsciiFont.from_arm9(arm)
    rows = []
    for frame, n in HOLDS:
        shot, image = frames[frame]
        expected = (current_prompt if n is None else table[n].text.strip()).decode("ascii")
        if n is not None:
            assert any(0 < frame - item["frame"] <= 300 and item["message_ID"] == n for item in requests)
        rows.append(dict(frame=frame, message_ID=n, text=expected, complete_glyphs=hold_text(image, font, expected), image=shot))
        evidence[shot["path"]] = shot["PNG_sha256"]
    # Declining goes straight to the same Fleet submenu. Accepting opens the
    # chart with four order choices. Back from the chart returns to that submenu.
    assert frames[10840][1].tobytes() == frames[13540][1].tobytes() == frames[16540][1].tobytes()
    assert frames[16240][1].tobytes() != frames[16540][1].tobytes()
    transitions = {"ordinary_decline_to_Fleet_Setup": 13540, "ordinary_accept_to_orders": 16240,
                   "back_to_Fleet_Setup": 16540, "back_to_Shipyard": 16840}
    for frame in transitions.values():
        evidence[frames[frame][0]["path"]] = frames[frame][0]["PNG_sha256"]
    records = [dict(id=f"COMMON_MESSAGE_{n}", file_path=COMMON, source_reference=b.reference(source[n]),
        current_reference=b.reference(table[n]), source_hex=source[n].text.hex(), current_hex=table[n].text.hex(),
        source_Japanese=source[n].text.decode("cp932"), speaker="System", english=table[n].text.decode("ascii").strip(),
        source_meaning=meaning, localization_note=reason, decision="retention", review=dict.fromkeys(b.GATES, True))
        for n, (meaning, reason) in REASON.items()]
    records.append(dict(id="FLEET_SHIP_EDITOR_CONFIRMATION", file_path=ARM,
        source_reference=dict(offset=quote, pointer_field=0xA5024), current_reference=dict(offset=quote, pointer_field=0xA5024),
        source_Japanese=source_prompt.decode("cp932"), source_hex=source_prompt.hex(), current_hex=current_prompt.hex(),
        speaker="System", english=current_prompt.decode("ascii"), source_meaning="Does the player approve the current ship arrangement?",
        localization_note="The ships and Yes/No choices are still visible. The short confirmation fits the question in the clean Japanese.",
        decision="retention", review=dict.fromkeys(b.GATES, True)))
    pending = next(row for row in base.load(current.precedent.WORKLIST)["records"] if row["message_ID"] == 284)
    assert table[284].text.hex() == pending["current_hex"] and source[284].text.hex() == pending["source_hex"]
    assert b.reference(table[284]) == pending["current_reference"] and b.reference(source[284]) == pending["source_reference"]
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        exact_original_scope=scope, isolated_reorganization_choices_with_shortfall=controls, actual_reorganization_states=states,
        retained_records=records, actual_ready_holds=rows, game_transitions=transitions, actual_requests=requests,
        storage_lead_284=pending, other_possible_callers_open=True, installed_ROM_bytes_changed=False,
        evidence=evidence, new_editorial_credit=0, new_gameplay_runs=1, hardware=False, full_goal_complete=False))
    print("Verified both fleet-orders responses, six complete screens and four isolated shortfall branches.")


if __name__ == "__main__":
    main()
