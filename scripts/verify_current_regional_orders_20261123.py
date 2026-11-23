"""Bind current fleet-order panels and related combat and port display owners."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from scripts import checkpoint_gallery_options_legacy_20261114 as playback
from scripts import observe_current_regional_orders_20261123 as play
from scripts import probe_regional_policy_wrap_v616 as formatter
from scripts import verify_regional_missions_v617 as geometry
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.probe_button_prompt_native import BASE, VIEW, call, machine
from scripts.verify_current_shared_encounters_20261123 import visual


current, base, town = play.current, play.base, play.current.stage.town
OUTPUT = Path("translations/editorial_checkpoints/shared_display_20261123/regional_orders_and_display_20261123.json")
ROOT = OUTPUT.parent
OLD_CAPTURE = Path("work/analysis/regional_missions_v617/release_proof.json")
OLD_REGIONAL = Path("translations/regional_policy_prompts_manuscript_v1.json")
VOYAGE = ROOT / "additional_voyages_20261123.json"
SQUARE = current.parent
TAVERN = SQUARE.parent
NO_TARGET = Path("work/analysis/no_target_v218/native_proof.json")
NO_TARGET_ARM = NO_TARGET.with_name("English_arm9.bin")
SAILING = Path("releases/all_routes_editorial_20261118_sailing_mode_prose_candidate")
MADEIRA = SAILING / "verification/verified_display_ownership.json"
MODAL = 0x020546B8
ORDERS = {
    127: ("Choose a base city.", "The short instruction states what the selected city will be used for."),
    128: ("You have no contract with that city.", "Contract is the established term and the wording addresses the player directly."),
    129: ("Choose a city for patrol. You must have a contract there.",
          "The first sentence names the order. The second gives the prerequisite for that city."),
    130: ("To dock the fleet, choose a city where you have a contract.",
          "The purpose and prerequisite stay together. Where you have a contract identifies the player's contract."),
    131: ("Choose a city to attack.", "The concise instruction fits the original choice of one city from the map."),
    132: ("You have already signed a contract with that city.",
          "Already explains why the selected city is excluded. The signed contract names the rule the player just encountered."),
    133: ("A faction not at war with you holds a contract with that city.",
          "The rule covers allied and neutral factions. Keeping the status explicit avoids suggesting that it only applies to allies."),
    134: ("That city doesn't have a contract with a faction you're at war with.",
          "The absence of an enemy contract is the reason for this separate rejection."),
}
ORDERS_HELD = ((24600, 131), (26600, 132), (34600, 127))
ASSIGNMENTS = (
    (10200, 0x8AE48, "Patrol orders issued.", "The mandate is a patrol based at the city named on the preceding row."),
    (15800, 0x8AE4C, "Docking orders issued.", "The line confirms the fleet's docking order at the port named just above it."),
    (20600, 0x8AE40, "Area management orders issued.", "The established Manage Area term refers to this fleet's order, with Stockholm as its base."),
    (None, 0x8AE44, "Attack orders issued.", "The separate confirmation states that an order was issued, while the preceding city is its target."),
)


def span(left, right, start, end):
    assert left[start:end] == right[start:end]
    return dict(start=BASE + start, end=BASE + end, sha256=sha256(right[start:end]).hexdigest())


def original_selector(arm, mission, own_share, other_shares):
    """Run original regional branches with controlled contract getter results."""
    u = machine(arm)
    includes_player = any(company == 2 for company, _ in other_shares)
    callbacks = {0x020CB160: VIEW, 0x020397D8: 2, 0x020CB1A8: VIEW + 0x1000, 0x020CB178: VIEW + 0x2000,
                 0x02035320: 2, 0x020B4AA8: own_share, 0x020B4A88: int(includes_player)}
    records, writes = [], []
    relations = dict(other_shares)
    assert len(relations) == len(other_shares) <= 3
    town_object = VIEW + 0x2004 + 5 * 108
    fleet_object = VIEW + 0x1004 + 57 * 132
    for index, (company, _) in enumerate(other_shares):
        u.mem_write(VIEW + 0x3000 + index, bytes((company,)))

    def bridge(cpu, pc, _size, _):
        a = cpu.reg_read(UC_ARM_REG_R0)
        b = cpu.reg_read(UC_ARM_REG_R1)
        if pc == MODAL:
            records.append((a, cpu.reg_read(UC_ARM_REG_LR) - 4))
            result = 0
        elif pc == 0x020B3FE0:
            assert a == town_object and 0 <= b < 3
            result = VIEW + 0x3000 + b if b < len(other_shares) else 0
        elif pc == 0x0203CB30:
            company, rem = divmod(a - VIEW - 4, 76)
            assert not rem and b == 2 and company in relations
            result = relations[company]
        elif pc == 0x02035A24:
            assert a == fleet_object and b == mission and cpu.reg_read(UC_ARM_REG_R2) == 5
            writes.append([57, mission, 5])
            result = 0
        elif pc in callbacks:
            if pc == 0x020B4AA8:
                assert (a, b) == (town_object, 2)
            if pc == 0x020B4A88:
                assert a == town_object
            result = callbacks[pc]
        else:
            return
        cpu.reg_write(UC_ARM_REG_R0, result)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    try:
        call(u, 0x8B010, (mission,))
        instruction = records.copy()
        records.clear()
        call(u, 0x8AE5C, (57, mission, 5))
        result = u.reg_read(UC_ARM_REG_R0)
    finally:
        u.hook_del(hook)
    return dict(mission=mission, supplied_fleet_share=own_share, supplied_contracts=list(other_shares),
        picker_call=instruction, refusal_call=records, assignment_attempt=writes, accepted=bool(result))


def policy_cases(ja, en):
    refs = [span(ja, en, 0x8AE5C, 0x8B07C)]
    rows = []
    selectors = {1: 127, 3: 130, 4: 129, 5: 131}
    addresses = {127: 0x0208B040, 128: 0x0208AF10, 129: 0x0208B050, 130: 0x0208B060,
                 131: 0x0208B070, 132: 0x0208AF2C, 133: 0x0208AFC0, 134: 0x0208AFDC}
    for key, address in addresses.items():
        assert direct_bl_target(unpack_from("<I", ja, address - BASE)[0], address) == MODAL
    for mission, picker in selectors.items():
        cases = ((0, (), 128), (20, (), None)) if mission != 5 else (
            (20, (), 132), (0, (), 134), (0, ((6, 0),), 133), (0, ((6, 1),), 133),
            (0, ((6, 2),), None), (0, ((5, 2), (6, 1)), 133),
            (0, ((3, 2), (5, 2), (6, 2)), None))
        for share, contracts, refusal in cases:
            stock, local = (original_selector(arm, mission, share, contracts) for arm in (ja, en))
            assert stock == local
            assert local["picker_call"] == [(picker, addresses[picker])]
            assert local["refusal_call"] == ([(refusal, addresses[refusal])] if refusal else [])
            assert local["accepted"] == bool(local["assignment_attempt"]) == (refusal is None)
            rows.append(local)
    return dict(code=refs, roles={"1": "Manage Area", "3": "Dock", "4": "Patrol", "5": "Attack Town"},
        input_branch_matrix=rows, all_refusal_and_picker_ids=sorted(addresses),
        controlled_contract_and_relation_returns=True, output_boundary="original modal and assignment receivers")


def c_string(arm, source_field):
    ptr = unpack_from("<I", arm, source_field)[0]
    raw, null, _ = arm[ptr - BASE:ptr - BASE + 128].partition(b"\0")
    assert null and raw
    return dict(pointer_field=source_field, offset=ptr-BASE, address=ptr, text_hex=raw.hex())


def full_dialog(im, font, lines):
    origin = 22 if len(lines) > 1 else 16
    expected = {(origin + x, 297 + i * 16 + y)
                for i, text in enumerate(lines) for x, y in geometry.glyphs(font, text)}
    observed = {(x, y) for y in range(294, 350) for x in range(12, 244)
                if im.getpixel((x, y)) == (0, 8, 0)}
    assert expected and observed == expected, (lines, len(expected - observed), len(observed - expected))
    return dict(lines=lines, origin=[origin, 297], row_stride=16, visible_ink=len(expected), complete_native_mask=True)


def no_target_path(arm):
    earlier = NO_TARGET_ARM.read_bytes()
    prior = base.load(NO_TARGET)
    assert sha256(earlier).hexdigest() == prior["target_arm9_sha256"]
    plan = prior["plan"]
    ranges = [(row["offset"], row["offset"] + 4) for row in plan["code_changes"] if row["offset"] not in (0x8E4, 0xE45DC)]
    # The later cache copy has a different size. Verify the actual resident
    # helpers and data at their shared deployed addresses.
    stock, fresh = [bytes(MainCodeFile(a, BASE).sections[3].data) for a in (earlier, arm)]
    lo = plan["pixel_pointer"] - plan["pool_span"][0]
    hi = plan["pool_span"][1] - plan["pool_span"][0]
    assert stock[lo:hi] == fresh[lo:hi]
    assert sha256(fresh[lo:lo+plan["panel"]["packed_bytes"]]).hexdigest() == plan["panel"]["packed_sha256"]
    code = [span(earlier, arm, lo, hi) for lo, hi in ranges]
    code.extend(span(earlier, arm, lo, hi) for lo, hi in ((0x6FFE0, 0x70084), (0x7B8FC, 0x7B944)))
    return dict(english=plan["panel"]["english"], resident_span=[plan["pixel_pointer"], plan["pool_span"][1]],
        prepared_asset_sha256=plan["panel"]["packed_sha256"], exact_display_code=code,
        text_and_sprite_bodies_exact=True, separate_from_COMMON=True)


def pending_ref(key, source, installed, worklist):
    jp, en = source[key], installed[key]
    reference = town.reference(en)
    assert reference == worklist[key]["installed"]
    return dict(message_ID=key, source_reference=town.reference(jp), current_reference=reference,
        source_hex=jp.text.hex(), current_hex=en.text.hex(), Japanese=jp.text.decode("cp932"),
        installed_English=en.text.decode("cp932"), other_stored_display_paths_pending=True)


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    candidate = release["candidate_sha256"]
    assert base.digest(current.ROM) == candidate and base.digest(base.REGISTRY) == release["registry_sha256"]
    previous = base.load(current.REVIEW)
    assert previous["candidate_sha256"] == candidate
    clean_path = current.stage.CLEAN
    assert base.digest(clean_path) == release["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (clean_path, current.ROM))
    ja, en = (x.read_file(current.ARM) for x in (clean, rom))
    assert current.native.digest(en) == release["target_ARM9_sha256"]
    source = town.common_message_entries(clean.read_file(current.COMMON), ja)
    entries = TAVERN.stage.observed.prior.shared.paired.prior.entries
    installed = entries(rom)
    term, traced, frames = playback.verify_report(play, "regional", release)
    assert len(traced) == term["COMMON_requests"] == 24
    assert {row["message_ID"] for row in traced} == {127, 129, 130, 131, 132}
    for event, copy in zip(traced[::2], traced[1::2], strict=True):
        assert event["PC"] == 0x0205528C and copy == event | {"PC": 0x020534F4}
        assert event["caller_LR"] == 0x020546CC
    rows = {row["message_id"]: row for row in base.load(OLD_REGIONAL)["records"]}
    gates = dict.fromkeys(town.GATES, True)
    font = playback.GameAsciiFont.from_arm9(en)
    u = machine(en)
    u.mem_write(formatter.POOL, bytes(MainCodeFile(en, BASE).sections[3].data[:-48]))
    retentions, panels = [], []
    for key, (english, note) in ORDERS.items():
        jp, now = source[key], installed[key]
        assert rows[key]["source_hex"] == jp.text.hex() and now.text == english.encode("ascii")
        assert b"%" not in jp.text + now.text
        prepared, guarded = formatter.run(u, 0x020546E8, key, english)
        assert guarded and b" ".join(prepared.split()) == now.text
        lines = prepared.decode("ascii").splitlines()
        assert 1 <= len(lines) <= 3 and all(0 < len(line) <= 37 for line in lines)
        row = dict(message_ID=key, english=english, clean_Japanese=jp.text.decode("cp932"),
            source_reference=town.reference(jp), current_reference=town.reference(now),
            installed_reference=town.reference(now), source_hex=jp.text.hex(), current_hex=now.text.hex(),
            source_meaning=rows[key]["source_meaning"], localization_note=note, decision="retention",
            native_layout=lines, native_guarded_wrap=True, review=gates)
        live = [capture for capture, k in ORDERS_HELD if k == key]
        if live:
            n, = live
            im = playback.screen(frames[n])
            assert any(event["message_ID"] == key and 0 < n-event["frame"] < 600 for event in traced)
            row["ordinary_replay_capture"] = frames[n]
            row["full_mask"] = full_dialog(im, font, [line.strip() for line in lines])
            panels.append((f"Regional order notice {key}", im))
        retentions.append(row)

    assignments = []
    earlier = base.load(OLD_CAPTURE)["four_complete_assignment_confirmations"]
    for frame, field, english, note in ASSIGNMENTS:
        left, right = [c_string(arm, field) for arm in (ja, en)]
        assert right["text_hex"] == english.encode("ascii").hex() and right["offset"] == left["offset"]
        row = dict(record_kind="ARM9 regional assignment suffix", english=english,
                   clean_Japanese=bytes.fromhex(left["text_hex"]).decode("cp932"),
                   source_reference=left, current_reference=right, installed_reference=right,
                   localization_note=note, decision="retention",
                   fleet_and_city_inserted_by_original_separate_getters=True)
        if frame:
            shot = frames[frame]
            im = playback.screen(shot)
            row.update(ordinary_replay_capture=shot, full_mask=full_dialog(im, font, ["Manuel Fleet:", "Stockholm", english]),
                       review=gates)
            panels.append((f"Original Stockholm assignment {frame}", im))
        else:
            old, = [case for case in earlier if case["frame"] == 36200]
            assert old["lines"][-1]["English"] == english
            row["historical_assignment_mask"] = old
            row["current_visible_hold_pending"] = True
            row["review"] = gates | {"formatting": False}
        assignments.append(row)

    code = [span(ja, en, 0x8AD58, 0x8AE5C)]
    for path, sha in term["evidence"].items():
        assert base.digest(path) == sha
    evidence = term["evidence"] | {str(p): base.digest(p) for p in (OLD_REGIONAL, OLD_CAPTURE, NO_TARGET, NO_TARGET_ARM, MADEIRA, VOYAGE)}
    worklist = {row["message_ID"]: row for row in previous["shared_consumer_binding"]["records"]}
    records = {key: pending_ref(key, source, installed, worklist) for key in (287, 300, 304)}
    assert len(worklist) == 276
    assert {287, 300, 304}.isdisjoint(row["message_ID"] for row in traced)
    assert base.digest(MADEIRA) == base.load(SAILING / "checksums.json")["verification/verified_display_ownership.json"]
    madeira = base.load(MADEIRA)
    assert madeira["actual_emulator_cases"]["neutral_v2"]["requests"][-1] == 2122
    assert madeira["actual_emulator_cases"]["allied_v2"]["visible_English"] == "There are no targets to attack."
    records[300]["tested_regional_attack_picker"] = 131
    records[304]["tested_regional_exclusions"] = [132, 133, 134]
    records[304]["separate_sailing_no_target"] = no_target_path(en)

    # Reuse the ordinary discovery holds after matching the exact relevant
    # executable and text dependencies from the previous registered build.
    voyage = base.load(VOYAGE)
    assert base.digest(TAVERN.ROM) == voyage["candidate_sha256"]
    old_rom = base.NdsImage.open(TAVERN.ROM)
    old_arm = old_rom.read_file(current.ARM)
    assert [n for n,(a,b) in enumerate(zip(old_arm,en,strict=True)) if a != b] == [current.stage.FIELD + 6]
    assert entries(old_rom)[297] == installed[297] and entries(old_rom)[1296] == installed[1296]
    assert old_rom.read_file("/GRP/KANJI.FNT") == rom.read_file("/GRP/KANJI.FNT")
    records[287]["exact_port_consumer_dependencies"] = [span(ja, en, lo, hi)
        for lo,hi in ((0x78DD0, 0x78DEC), (0x7877C, 0x78798))]
    records[287]["prior_ordinary_port_notice"] = dict(message_ID=297, receipt=str(VOYAGE), sha256=base.digest(VOYAGE))

    sheets = []
    for index in range(0, len(panels), 4):
        path, digest = visual.make_sheet(ROOT / f"regional_orders_{1+index//4}.png", panels[index:index+4])
        sheets.append(dict(path=path, sha256=digest))
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        ordinary_inputs_with_prepared_regional_fleet_save=True, synthetic_during_current_replay=False, hardware=False,
        original_COMMON_requests=traced, records=retentions, assignments=assignments, original_assignment_code=code,
        pending_records=list(records.values()), offline_regional_policy_branches=policy_cases(ja, en),
        historical_neutral_and_allied_sailing=madeira["actual_emulator_cases"],
        pending_stored_entries=276, new_editorial_credit=0, sheets=sheets, evidence=evidence))
    print("Bound six ordinary holds, eight original policy records and the finite regional attack branches.")


if __name__ == "__main__":
    main()
