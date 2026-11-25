"""Bind company selectors and the no-dock fallback to the registered Tunis ROM."""

from collections import Counter
from pathlib import Path
from struct import iter_unpack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R2, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_SP

from scripts import observe_fleet_company_inputs_20261124 as observed
from scripts import reconcile_archived_message_reader_20261124 as branch
from scripts import reconcile_fleet_destination_copies_20261123 as copies
from scripts import reconcile_fleet_destination_lists_20261123 as lists
from scripts import reconcile_fleet_headquarters_20261124 as parent
from scripts.audit_fleet_save_backups_20261124 import SLOT_BYTES, backup_slots
from scripts.native_call_abi_v764 import STACK
from scripts.reconcile_fleet_destination_writers_20261123 import BASE, FLEET_STRIDE, code_at, direct_bl_target, get_machine, loaded_components
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = parent.OUT.with_name("fleet_company_and_fallback_current_20261124.json")
ACTOR_CATALOGUE, ACTOR_STRIDE, ACTOR_COUNT = 0x02120B80, 32, 207
ACTOR_ROOT, ACTIVE_ACTOR = 0x022D4344, 0x022D5D24
AFFILIATION, AFFILIATION_SETTER, NONE = 5, 0x0207E950, 21
VALID_COMPANIES = set(range(20)) | {NONE}
PLAYER_COMPANY_LIST = 0x02115260
TRANSFER = 0x02033CCC
STORY_GUARD, STORY_ACCEPT, STORY_REJECT = 0x0202B850, 0x0202B870, 0x0202B8D8
FALLBACK, RANDOM, DESTINATION_SET = 0x02033DD0, 0x020519D4, 0x02035A24
SETTER_CALLS = {0x0202B8C8: "Story affiliation assignment",
    0x0202BBB0: "Join the protagonist's company", 0x0202BDAC: "Leave a company",
    0x02033D28: "Fleet reassignment selected from regular companies",
    0x02033DCC: "Fleet reassignment without a company", 0x0203A5E8: "Disband a company"}
SPANS = ((0x0202B850, 0x0202B8E4), (0x0202BB5C, 0x0202BBB4), (0x0202BD88, 0x0202BDC8),
    (0x0202C780, 0x0202C9E0), (TRANSFER, 0x02033D38), (0x02033DA8, 0x02033E1C),
    (0x02034674, 0x02034688), (0x020352CC, 0x02035370), (DESTINATION_SET, DESTINATION_SET + 12),
    (0x020397D8, 0x0203980C), (0x0203A5A0, 0x0203A604), (AFFILIATION_SETTER, 0x0207E960),
    (0x0207EBAC, 0x0207EBD8), (0x02082FA8, 0x02082FB8), (0x020B1720, 0x020B1760),
    (0x020B28B8, 0x020B2978), (0x020CD9DC, 0x020CDAC4),
    (PLAYER_COMPANY_LIST, PLAYER_COMPANY_LIST + 16))


def direct_sources(image):
    targets = {AFFILIATION_SETTER, TRANSFER}
    found = {entry: [] for entry in targets}
    for label, base, raw in loaded_components(image):
        for index, (word,) in enumerate(iter_unpack("<I", raw[:len(raw) & ~3])):
            address = base + index * 4
            target = direct_bl_target(word, address)
            assert word not in targets and word & ~1 not in targets
            if target in found:
                found[target].append((label, address))
        assert not list(branch.linked_immediates(raw, base, targets)), label
    assert found == {key: [("arm9_section_0", pc) for pc in pcs]
                     for key, pcs in ((AFFILIATION_SETTER, SETTER_CALLS), (TRANSFER, (0x0202C9DC,)))}
    return found


def source_contract(clean, arm, raw):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    spans, ops = [], {}
    for lo, hi in SPANS:
        data = code_at(arm, lo, hi)
        assert data == code_at(clean, lo, hi) == code_at(raw, lo, hi)
        ops.update({ins.address: f"{ins.mnemonic} {ins.op_str}" for ins in decoder.disasm(data, lo)})
        spans.append(dict(start=lo, end=hi, exact_hex=data.hex()))
    expected = {
        0x0202B850: "and r7, r2, #0xff", 0x0202B864: "blt #0x202b8d8", 0x0202B868: "cmp r7, #0x14",
        0x0202B86C: "bge #0x202b8d8", 0x0202B8C4: "mov r1, r7", 0x0202BBA4: "bl #0x20397d8",
        0x0202BBA8: "mov r1, r0", 0x0202BD9C: "mov r1, #0x15", 0x02033DB0: "mov r1, #0x15",
        0x0203A5B0: "mov r5, #0x15", 0x0203A5E4: "mov r1, r5",
        0x0202C788: "mov sb, #0", 0x0202C79C: "mov r4, sb", 0x0202C7F8: "strne r4, [r7, sb, lsl #2]",
        0x0202C800: "add r4, r4, #1", 0x0202C804: "cmp r4, #0x14", 0x0202C808: "blt #0x202c7b4",
        0x0202C870: "strlt r5, [r4, r8, lsl #2]", 0x0202C874: "strlt r6, [r4, r7, lsl #2]",
        0x0202C9B4: "ldreq r8, [fp, r7, lsl #2]", 0x0202C9C8: "cmp r8, #0x15",
        0x0202C9D4: "mov r1, r8", 0x0202C9DC: "bl #0x2033ccc",
        0x02033CD8: "mov r5, r1", 0x02033D24: "mov r1, r5",
        0x02035300: "cmp r4, #0x15", 0x02035314: "mov r0, #0x4c",
        0x02035354: "bl #0x207e958", AFFILIATION_SETTER: "strb r1, [r0, #5]",
        0x0207E958: "ldrb r0, [r0, #5]", 0x0207EBBC: "add r1, r8, #5", observed.AFFILIATION_READ: "bl #0x2046a1c",
        0x02082FB4: "bl #0x207ebac", 0x020CDA2C: "ldrb r1, [r0, #0x1e]", 0x020CDA34: "strb r1, [r5, #5]",
        FALLBACK: "ldrb r2, [r8, #0x3c]", 0x02033DE0: "bl #0x2034674", 0x02033DF0: "mov r0, #8",
        0x02033DF4: "bl #0x20b1720", 0x02033E04: "mov r0, #0x5a", 0x02033E08: "bl #0x20519d4",
        0x02033E14: "mov r1, #9", 0x02033E18: "bl #0x2035a24",
        0x020B1754: "ldr r0, [r1, r0, lsl #2]", 0x020B28CC: "bl #0x20b290c",
        0x020B28EC: "cmp r4, #8", 0x020B28F0: "moveq r0, #1", 0x020B2968: "cmp r5, #0x5a",
    }
    assert all(ops.get(pc) == instruction for pc, instruction in expected.items()), {
        hex(pc): (ops.get(pc), want) for pc, want in expected.items() if ops.get(pc) != want}
    assert unpack_from("<I", arm, 0x020CDAC0 - BASE)[0] == ACTOR_CATALOGUE
    assert unpack_from("<I", arm, 0x02039804 - BASE)[0] == PLAYER_COMPANY_LIST
    return spans


def stock_and_story(clean, arm, raw):
    cpu, call = get_machine(arm, raw)
    assert call(0xCB184) + 4 == ACTOR_ROOT
    assert call(0x7F244) == 3 and call(0x397D8) == 3
    assert unpack_from("<4I", arm, PLAYER_COMPANY_LIST - BASE) == (0, 2, 1, 3)
    stock, initialized = [], []
    for index in range(ACTOR_COUNT):
        offset = ACTOR_CATALOGUE - BASE + ACTOR_STRIDE * index + 0x1E
        allowed = arm[offset]
        assert allowed == clean[offset] == raw[offset] and allowed in VALID_COMPANIES
        actor = ACTOR_ROOT + ACTOR_STRIDE * index
        before = bytes(cpu.mem_read(actor, ACTOR_STRIDE))
        initialized.append(before[AFFILIATION])
        assert before[AFFILIATION] in VALID_COMPANIES
        cpu.mem_write(actor + AFFILIATION, b"\xff")
        call(0xCD9DC, actor, index)
        assert call(0x7E958, actor) == allowed
        cpu.mem_write(actor, before)
        stock.append(allowed)
    assert set(stock) == VALID_COMPANIES

    seen = []

    def boundary(machine, pc, size, data):
        if pc in (STORY_ACCEPT, STORY_REJECT):
            seen.append(pc)
            machine.emu_stop()

    hook = cpu.hook_add(UC_HOOK_CODE, boundary, begin=STORY_ACCEPT, end=STORY_REJECT)
    accepted = []
    try:
        for value in range(256):
            seen.clear()
            cpu.reg_write(UC_ARM_REG_R2, value)
            cpu.emu_start(STORY_GUARD, 0, count=16)
            expected = STORY_ACCEPT if value < 20 else STORY_REJECT
            assert seen == [expected]
            if expected == STORY_ACCEPT:
                assert cpu.reg_read(UC_ARM_REG_R7) == value
                accepted.append(value)
    finally:
        cpu.hook_del(hook)
    return dict(stock_rows=ACTOR_COUNT, catalogue_affiliations=stock, startup_affiliations=initialized,
        protagonist_company_indices=[0, 2, 1, 3], guarded_story_byte_cases=256, admitted_story_targets=accepted)


def fallback_cases(arm, raw):
    cpu, call = get_machine(arm, raw)
    ports, fleet = call(0xCB178), call(0xCB1A8) + 4
    scratch = 0x023F0300
    count = call(0xB28B8, ports, scratch, 8)
    eligible = list(unpack_from(f"<{count}I", cpu.mem_read(scratch, 4 * count)))
    assert eligible == list(range(86))
    original = bytes(cpu.mem_read(fleet, FLEET_STRIDE))
    results, final_fallback, random_inputs = [], [], []

    def random_bound(machine, pc, size, data):
        random_inputs.append(machine.reg_read(UC_ARM_REG_R0))

    hook = cpu.hook_add(UC_HOOK_CODE, random_bound, begin=RANDOM, end=RANDOM)
    try:
        for value in range(116):
            prepared = bytearray(original)
            prepared[0x3C] = value
            cpu.mem_write(fleet, bytes(prepared))
            cpu.reg_write(UC_ARM_REG_R8, fleet)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            random_inputs.clear()
            cpu.emu_start(FALLBACK, 0x02033E1C, count=200000)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x02033E1C
            destination = cpu.mem_read(fleet + 0x3F, 1)[0]
            if value == 115:
                assert destination in eligible and random_inputs == [len(eligible)]
            else:
                assert destination == value and not random_inputs
            prepared[0x3E:0x40] = bytes((9, destination))
            assert bytes(cpu.mem_read(fleet, FLEET_STRIDE)) == prepared
            results.append(destination)

        # Enter after an empty earlier selector. This exercises the last branch only.
        for _ in range(16):
            cpu.reg_write(UC_ARM_REG_R2, 115)
            cpu.reg_write(UC_ARM_REG_R8, fleet)
            random_inputs.clear()
            cpu.emu_start(0x02033DFC, 0x02033E1C, count=100000)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x02033E1C and random_inputs == [90]
            destination = cpu.mem_read(fleet + 0x3F, 1)[0]
            assert 0 <= destination < 90
            final_fallback.append(destination)
    finally:
        cpu.hook_del(hook)
    return dict(native_docking_input_cases=len(results), destination_by_input=results,
        ordinary_port_list=eligible, isolated_empty_selector_branch_results=final_fallback,
        existing_114_copied_unchanged=True, ordinary_creation_of_114_observed=False)


def ordinary_restore(case, release, arm):
    root = observed.ROOT / case
    paths = [root / name for name in ("capture/capture_report.json", "requests.json", "terminal.json", "source_contract.json")]
    capture, trace, terminal, contract = map(read, paths)
    controls, holds, end, previous, donor = observed.schedule(case)
    assert capture["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    assert capture["scripted_input_schedule"] == controls and capture["frames"] == terminal["completed_frames"] == end
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(paths[-1]) and contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {row["PC"] for row in contract["targets"]} == observed.CALLS.keys()
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    inputs = capture["battery_save_preloaded"]
    assert inputs["copied_byte_exact_before_cold_boot"] and digest(inputs["source"]) == donor["source_sha256"]
    rows = trace["rows"]
    assert rows == terminal["caption_calls"] and len(rows) == 2 * (ACTOR_COUNT + 1)
    expected_addresses = [*(ACTOR_ROOT + ACTOR_STRIDE * i for i in range(ACTOR_COUNT)), ACTIVE_ACTOR]
    offsets, values, restore_frames = [], [], set()
    for before, after, address in zip(rows[::2], rows[1::2], expected_addresses, strict=True):
        assert before["phase"] == "before" and after["phase"] == "after"
        assert before["PC"] == observed.AFFILIATION_READ and after["PC"] == before["PC"] + 4
        assert before["owner"] == after["owner"] == address and before["frame"] == after["frame"] < holds[0]
        assert before["saved_byte"] == after["value"] and after["success"] == 1
        offsets.append(before["buffer_offset"])
        values.append(before["saved_byte"])
        restore_frames.add(before["frame"])
    assert len(restore_frames) == 1 and len(set(offsets)) == ACTOR_COUNT + 1 and set(values) <= VALID_COMPANIES
    original = Path(donor["source"]).read_bytes()
    slot_index, = [index for index in range(6) if original[index * SLOT_BYTES:index * SLOT_BYTES + 4] == b"DK4R"
                   and all(original[index * SLOT_BYTES + off] == value for off, value in zip(offsets, values, strict=True))]
    slot = original[slot_index * SLOT_BYTES:(slot_index + 1) * SLOT_BYTES]
    checksum = sum(value if value < 128 else value - 256 for value in slot[8:]) & 0xFFFFFFFF
    assert unpack_from("<I", slot, 4)[0] == checksum
    snapshot, = capture["read_only_capture_RAM_snapshots"]
    raw = Path(snapshot["path"]).read_bytes()
    assert sha256(raw).hexdigest() == snapshot["sha256"] and snapshot["frame"] == holds[0]
    current_hold, = [row for row in capture["frames_captured"] if row["frame"] == holds[0]]
    previous_hold, = [row for row in read(previous)["frames_captured"] if row["frame"] == holds[0]]
    assert current_hold["framebuffer_sha256"] == previous_hold["framebuffer_sha256"]
    assert digest(current_hold["path"]) == current_hold["PNG_sha256"]
    cpu, call = get_machine(arm, raw)
    assert all(call(0x7E958, address) == value for address, value in zip(expected_addresses, values, strict=True))
    fleet = call(0xCB1A8) + 4
    fleet_rows = []
    for index in range(64):
        address = fleet + index * FLEET_STRIDE
        record = bytes(cpu.mem_read(address, FLEET_STRIDE))
        company = call(0x35320, address)
        assert company in VALID_COMPANIES and call(0x352F4, address) == (0 if company == NONE else 0x022D8E68 + 76 * company)
        assert all(0 <= value < 114 or value == 115 for value in (record[0x3C], record[0x3F]))
        fleet_rows.append(dict(index=index, company=company, docking=record[0x3C], destination=record[0x3F]))
    return dict(case=case, restore_frame=next(iter(restore_frames)), actual_town_hold=holds[0],
        donor=reference(donor["source"]), save_slot=slot_index, save_slot_sha256=sha256(slot).hexdigest(),
        restored_affiliations=values, live_Fleet_Info_records=fleet_rows, read_only_snapshot=snapshot,
        matched_ordinary_town_frame=reference(current_hold["path"]), evidence=list(map(reference, paths))), offsets


def existing_backups(offsets):
    audit = read(parent.SAVES)
    totals, counts = Counter(), []
    for prior in audit["backups"]:
        current = backup_slots(Path(prior["path"]), {"affiliation": offsets})
        assert prior["sha256"] == current["sha256"]
        cases = Counter()
        for a, b in zip(prior["slots"], current["slots"], strict=True):
            assert a["status"] == b["status"] and a["sha256"] == b["sha256"]
            if b["status"] == "valid":
                cases.update(bytes.fromhex(b["fields_hex_by_index"]["affiliation"]))
        assert cases.keys() <= VALID_COMPANIES
        totals.update(cases)
        counts.append(dict(backup_sha256=current["sha256"], affiliation_counts=dict(sorted(cases.items()))))
    assert len(counts) == 24 and sum(totals.values()) == audit["slot_states"]["valid"] * len(offsets) == 26000
    return dict(verified_backups=len(counts), valid_slot_copies=audit["slot_states"]["valid"],
        saved_affiliation_bytes=sum(totals.values()), counts=dict(sorted(totals.items())), per_backup=counts,
        original_slot_checks=reference(parent.SAVES))


def writer_inventory(clean, current, arm):
    """Cross-check all aligned sites while keeping the upstream limits visible."""
    prior = copies.prior
    current_links = prior.references(current)[prior.WRITER]
    assert current_links == prior.references(clean)[prior.WRITER]
    assert not current_links["aligned_exact_pointer"]
    copies_proof, list_proof, inputs, ports = map(read, (copies.OUT, lists.OUT, parent.upstream.OUT, parent.PORTS))
    assert current_links == {key: value for key, value in copies_proof["writer_census"].items()}
    for row in list_proof["matched_clean_installed_and_resident_ranges"]:
        assert code_at(arm, row["address"], row["end"]) == bytes.fromhex(row["exact_hex"])
    for group in (inputs["original_and_installed_code"], ports["clean_current_and_resident_code"]):
        for row in group:
            assert code_at(arm, row["start"], row["end"]) == bytes.fromhex(row["exact_hex"])
    for row in copies_proof["copies"]:
        pc = row["call"]
        assert code_at(arm, pc - 12, pc + 4) == bytes.fromhex(row["exact_caller_bytes"])
    categories = {
        "existing destination byte": set(copies.PREEXISTING_DESTINATION),
        "stock fleet row": set(copies.STOCK_CALLS),
        "scheduled agreement target": {prior.SCHEDULED_WRITE},
        "player regional picker": {lists.FLEET_ORDER},
        "story order or existing docking byte": {lists.STORY_ORDER},
        "bounded town lists": {row["call"] for row in list_proof["conditional_list_writer_sites"]},
        "company headquarters byte": set(inputs["original_HQ_company_byte_writers"]),
        "port object converted to index": set(inputs["port_pointer_to_index_writers"]),
        "docking byte or no-dock fallback": {inputs["fallback_docking_slot_writer"]},
        "company dispatch selector": {inputs["dispatch_writer"]},
    }
    calls = {pc for _, pc in current_links["aligned_ARM_BL"]}
    assert len(calls) == sum(map(len, categories.values())) == 27
    assert set.union(*categories.values()) == calls
    return dict(aligned_writer_calls=27, categories={name: sorted(sites) for name, sites in categories.items()},
        source_receipts=list(map(reference, (copies.OUT, lists.OUT, parent.upstream.OUT, parent.PORTS))),
        scope="Exact aligned ARM calls, plus the recorded upstream evidence. Computed or externally supplied field values remain outside this alignment census.")


def main():
    release = read(observed.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    clean, installed = map(NdsImage.open, (CLEAN, release["candidate"]))
    jp, arm = (rom.read_file(parent.ARM) for rom in (clean, installed))
    earlier = read(parent.OUT)
    guild = read(parent.RELEASE)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] == guild["target_ARM9_sha256"]
    assert guild["candidate_sha256"] == earlier["candidate_sha256"]
    startup = read(release["own_registered_startup"])
    assert startup["candidate_sha256"] == release["candidate_sha256"] and startup["cold_boot"] and not startup["savestate"]
    snapshot = startup["read_only_snapshot"]
    raw = Path(snapshot["path"]).read_bytes()
    assert len(raw) == 0x400000 and sha256(raw).hexdigest() == snapshot["sha256"] and snapshot["read_only_export"]
    scopes = source_contract(jp, arm, raw)
    assert direct_sources(clean) == direct_sources(installed)
    stock = stock_and_story(jp, arm, raw)
    fallback = fallback_cases(arm, raw)
    tunis, first = ordinary_restore("tunis", release, arm)
    nagasaki, second = ordinary_restore("nagasaki", release, arm)
    assert first == second
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_source_and_resident_code=scopes,
        original_affiliation_setter_inputs=SETTER_CALLS, original_affiliation_and_dock_checks=stock | fallback,
        real_save_field_offsets_by_actor_then_protagonist=first, ordinary_replays=[tunis, nagasaki],
        destination_writer_inventory=writer_inventory(clean, installed, arm),
        original_save_corpus=existing_backups(first), inherited_exact_ARM9_headquarters_proof=reference(parent.OUT),
        proof_sources=list(map(reference, (observed.RELEASE, release["own_registered_startup"], parent.RELEASE))),
        remaining="The checked saved and stock inputs use companies 0–19 or no company. The dock fallback can copy a stored 114. "
                  "No ordinary production of dock or destination 114 was observed. Indirect providers outside the checked inputs remain open.",
        ROM_changed=False, new_editorial_credit=0))
    print("Verified six company setters, 207 stock actor rows, two ordinary 208-field loads, "
          "26,000 backup affiliation bytes, and 132 focused dock fallback cases.")


if __name__ == "__main__":
    main()
