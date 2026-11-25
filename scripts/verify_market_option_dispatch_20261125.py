"""Bind Market menu variants and Deal exits to the original dispatchers."""

from struct import pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_FP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_SP,
)

from scripts import observe_azores_return_20261123 as azores
from scripts import reconcile_common_observed_callers_20261124 as callers
from scripts import register_seoul_reika_20261125 as current
from scripts import verify_archived_message_storage_20261124 as archive
from scripts import verify_syracuse_trade_cancel_20261124 as syracuse
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = callers.ROOT / "market_option_dispatch_current_20261125.json"
TOWN_MENU, VILLAGE_MENU = 0x0211ACFC, 0x0211AD2C
MENU_ROUTINE, OPTION, CONTRACT = 0x020BA494, 0x020BA3E0, 0x020BA428
CHOOSER, ACTIVE_TOWN, STACK_ENTER, STACK_LEAVE = 0x02051F4C, 0x020B65E4, 0x020C989C, 0x020C987C
DEAL_INPUT, TRADE_COMMIT, RESET, DEAL_BUS = 0x020C2450, 0x020BB3C4, 0x020C25F0, 0x022CF784
SHIP_TRANSFER = 0x020C2B9C
OBJECT, MODEL, STACK = 0x023F1000, 0x023F4000, 0x023EE000
MASK = 0xFFFFFFFF
SPANS = ((0x020BA390, 0x020BA480), (0x020BA484, 0x020BA51C), (TOWN_MENU, VILLAGE_MENU + 0x30),
         (0x020BB238, 0x020BB3A4), (0x020BB3A8, 0x020BB3C4), (TRADE_COMMIT, 0x020BB464),
         (0x020BC22C, 0x020BC258), (0x020BC2AC, 0x020BC2B4), (DEAL_INPUT, RESET),
         (RESET, 0x020C26EC), (0x020C09E0, 0x020C0A24),
         (0x020C539C, 0x020C53AC), (0x0215876C, 0x02158808))


def bytes_at(data, addr, size):
    raw = data[addr - BASE:addr - BASE + size]
    assert len(raw) == size
    return raw


def u32(data, addr):
    return unpack_from("<I", data, addr - BASE)[0]


def source_layout(clean, installed):
    locks = []
    for lo, hi in SPANS:
        raw = bytes_at(clean, lo, hi - lo)
        assert raw == bytes_at(installed, lo, hi - lo), hex(lo)
        locks.append(dict(start=lo, end_exclusive=hi, sha256=sha256(raw).hexdigest()))
    expected = {0x020BA3E0: "cmp r0, #3", 0x020BA3E4: "addls pc, pc, r0, lsl #2",
                0x020BA410: "mov r0, sb", 0x020BA428: "bl #0x2053fe4",
                0x020BA430: "mov r0, sb", 0x020BA434: "bl #0x20bc894",
                0x020BA448: "bl #0x20baf04", 0x020BA4AC: "cmp r0, #0x5a",
                0x020BB310: "ldr r0, [r5, #0x54]", 0x020BB320: "cmp r0, #0",
                0x020C259C: "bl #0x20bb3c4", 0x020C25C8: "bl #0x20c25f0",
                0x020C2588: "bl #0x20c2b9c", 0x020C53A4: "b #0x20c2450",
                0x020BB410: "beq #0x20bc244", 0x020BB444: "blo #0x20bc22c",
                0x020BB450: "bl #0x2053cb0", 0x020BB460: "popeq {r4, r5, r6, r7, r8, sb, sl, fp, pc}"}
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for pc, op in expected.items():
        ins, = decoder.disasm(bytes_at(clean, pc, 4), pc)
        assert f"{ins.mnemonic} {ins.op_str}" == op, (hex(pc), ins.mnemonic, ins.op_str)
    assert u32(clean, 0x020BA514) == VILLAGE_MENU and u32(clean, 0x020BA518) == TOWN_MENU
    contract_key = u32(clean, 0x020BA490)
    assert contract_key == u32(installed, 0x020BA490) == 761
    assert u32(clean, 0x020BC2AC) == 753 and u32(clean, 0x020BC2B0) == 746
    assert u32(clean, 0x020C25EC) == u32(clean, 0x020BB3B4) == DEAL_BUS
    assert u32(clean, 0x02158770 + 0x50) == 0x020C539C
    menu = {}
    for name, address in (("town", TOWN_MENU), ("village", VILLAGE_MENU)):
        rows = []
        for index, (ja, en) in enumerate(zip(("交易", "商業投資", "相場情報"), ("Trade", "Invest", "Market Info"), strict=True)):
            ptr, visible, enabled, flag = unpack_from("<4I", clean, address - BASE + index * 16)
            assert visible == enabled == int(name == "town" or index == 0) and flag == 0
            texts = [bytes_at(image, ptr, 28).split(b"\0")[0] for image in (clean, installed)]
            assert [value.decode("cp932") for value in texts] == [ja, en]
            rows.append(dict(index=index, label_address=ptr, flags=[visible, enabled, flag],
                             source=ja, installed=en, clean_hex=texts[0].hex(), installed_hex=texts[1].hex()))
        menu[name] = dict(address=address, options=rows)
    adjusted = []
    for address, source, target, description in (
        (0x020BA480, 0x0215706C, 0x02143E12, "Localized governor's-office substitution"),
        (0x020BB3A4, 0x25A8, 0x26C8, "Registered Deal frame allocation"),
    ):
        assert (u32(clean, address), u32(installed, address)) == (source, target)
        adjusted.append(dict(address=address, source=source, current=target, role=description))
    return dict(exact_spans=locks, original_contract_key=contract_key, registered_differences=adjusted,
                verified_instructions=expected, menu_tables=menu)


def run_with_stubs(cpu, entry, args, stubs):
    calls = []

    def observe(uc, pc, _size, _data):
        if pc not in stubs:
            return
        registers = tuple(uc.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2))
        calls.append((pc, registers))
        uc.reg_write(UC_ARM_REG_R0, stubs[pc])
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, observe)
    try:
        trace = call(cpu, entry - BASE, args, instruction_limit=1000)
    finally:
        cpu.hook_del(hook)
    assert not {callers.GETTER, callers.COPIER} & trace
    return cpu.reg_read(UC_ARM_REG_R0), calls


def options(cpu):
    cases = []
    for port in (0, 89, 90, 113, 114, 115):
        for selection in (0, 1, 2, 3, MASK):
            stub = {ACTIVE_TOWN: port, CHOOSER: selection, STACK_ENTER: 0, STACK_LEAVE: 0}
            result, effects = run_with_stubs(cpu, MENU_ROUTINE, (0,), stub)
            assert [pc for pc, _ in effects] == [STACK_ENTER, ACTIVE_TOWN, CHOOSER, STACK_LEAVE]
            table = VILLAGE_MENU if port >= 90 else TOWN_MENU
            assert effects[0][1][1] == 0x15 and effects[2][1] == (table, 3, 0) and result == selection
            cases.append(dict(supplied_port=port, menu_table=table, supplied_chooser_result=selection, forwarded=result))
    return cases


def routes(cpu):
    cases = []
    options = {0x020BA40C: "Trade", CONTRACT: "Contract refusal", 0x020BA434: "Invest",
               0x020BA448: "Market Info", 0x020BA450: "Back", 0x020BA458: "Default"}
    selectors = {0: None, 1: 0x020BA434, 2: 0x020BA448, 3: 0x020BA450}
    for result in (0, 1, 2, 3, 4, 0x7FFFFFFF, 0x80000000, MASK):
        for share in (0, 1):
            reached = []

            def stop(uc, pc, _size, _data):
                if pc in options:
                    reached.append(pc)
                    uc.emu_stop()

            hook = cpu.hook_add(UC_HOOK_CODE, stop, begin=OPTION, end=0x020BA458)
            try:
                cpu.reg_write(UC_ARM_REG_SP, STACK)
                cpu.reg_write(UC_ARM_REG_R0, result)
                cpu.reg_write(UC_ARM_REG_R7, share)
                cpu.reg_write(UC_ARM_REG_R6, OBJECT)
                cpu.reg_write(UC_ARM_REG_FP, 761)
                cpu.emu_start(OPTION, 0, count=32)
            finally:
                cpu.hook_del(hook)
            target = (0x020BA40C if share else CONTRACT) if result == 0 else selectors.get(result, 0x020BA458)
            assert reached == [target]
            message = None
            if target == CONTRACT:
                message = 761
                assert cpu.reg_read(UC_ARM_REG_R1) == message
            cases.append(dict(supplied_action=result, positive_market_share=bool(share), route=options[target],
                              boundary=target, message_ID=message))
    return cases


def deal_actions(cpu):
    def bus():
        return tuple(unpack_from("<2I", cpu.mem_read(DEAL_BUS + 0x20, 8)))

    cases = []
    for action, status, expected, wanted_bus in (
        (20, 0, None, (1, MASK)),
        (21, 0, TRADE_COMMIT, (0, 21)),
        (21, 1, TRADE_COMMIT, (1, MASK)),
        (22, 0, SHIP_TRANSFER, (1, MASK)),
        (23, 0, RESET, (0, 23)),
        (24, 0, None, (1, MASK)),
        (MASK, 0, None, (1, MASK)),
    ):
        cpu.mem_write(DEAL_BUS + 0x20, pack("<2I", 1, MASK))
        cpu.mem_write(OBJECT + 0x5F8, pack("<I", MODEL) + b"\x03")
        stubs = {0x020B6618: 0, 0x020B2CD8: 0, TRADE_COMMIT: status, RESET: 0, SHIP_TRANSFER: 0}
        _, effects = run_with_stubs(cpu, DEAL_INPUT, (OBJECT, 0, action), stubs)
        targets = [pc for pc, _ in effects]
        assert targets[:2] == [0x020B6618, 0x020B2CD8]
        assert targets[2:] == ([] if expected is None else [expected]) and bus() == wanted_bus
        assert bytes(cpu.mem_read(OBJECT + 0x5FC, 1)) == b"\0"
        if expected == TRADE_COMMIT:
            assert effects[-1][1][0] == MODEL
        if expected == RESET:
            assert effects[-1][1][:2] == (OBJECT, 1)
        cases.append(dict(action=action, supplied_finish_status=status if action == 21 else None,
                          next_original_boundary=expected, loop_active=wanted_bus[0], exit_value=wanted_bus[1]))
    return cases


def loop_conditions(cpu):
    cases = []
    for phase in (0, 1, 2):
        for active in (0, 1, 2):
            expected = 0x020BB2FC if phase == 1 and active else 0x020BB328
            cpu.mem_write(OBJECT + 0x54, pack("<I", phase))
            cpu.mem_write(DEAL_BUS + 0x20, pack("<I", active))
            stops = {0x020BB2FC, 0x020BB328}

            def stop(uc, pc, _size, _data):
                if pc in stops:
                    uc.emu_stop()

            hook = cpu.hook_add(UC_HOOK_CODE, stop, begin=0x020BB2FC, end=0x020BB328)
            try:
                cpu.reg_write(UC_ARM_REG_R5, OBJECT)
                cpu.reg_write(UC_ARM_REG_R6, DEAL_BUS)
                cpu.emu_start(0x020BB310, 0, count=10)
            finally:
                cpu.hook_del(hook)
            assert cpu.reg_read(UC_ARM_REG_PC) == expected
            cases.append(dict(supplied_session_phase=phase, supplied_loop_active=active,
                              continues_original_input_loop=expected == 0x020BB2FC))
    return cases


def reset_on_back(cpu):
    cases = []
    for good, cargo in ((125, 125), (42, 42), (42, 43)):
        cpu.mem_write(OBJECT + 0x5F8, pack("<I", MODEL))
        stubs = {0x020BAB3C: 0, 0x020BC678: 0, 0x020BCAF4: good, 0x020B6618: OBJECT,
                 0x020B3AE8: 1, 0x020B3A24: cargo, 0x020BA718: 0, 0x020BC5B8: 0}
        _, effects = run_with_stubs(cpu, RESET, (OBJECT, 1), stubs)
        assert [pc for pc, _ in effects[:2]] == [0x020BAB3C, 0x020BC678]
        assert all(args[0] == MODEL for _, args in effects[:2])
        assert [args[1] for pc, args in effects if pc == 0x020BCAF4] == list(range(5))
        updates = [args for pc, args in effects if pc == 0x020BA718]
        assert updates == ([(MODEL, 0, 1)] * 5 if good == cargo == 42 else []), (good, cargo, updates)
        assert effects[-1][0] == 0x020BC5B8 and effects[-1][1][0] == MODEL
        cases.append(dict(supplied_local_good=good, supplied_cargo_good=cargo, restored_entry_calls=len(updates),
                          exited_at_original_model_cleanup=True))
    return cases


def existing_play(arm, current_rows):
    prior = read(syracuse.OUT)
    assert prior["ordinary_controls"] and prior["archived_IDs_absent_from_these_requests"]
    refs = prior["evidence"]
    assert refs and all(reference(item["path"]) == item for item in refs)
    prior_release = read(syracuse.play.current.RELEASE)
    assert prior["candidate_sha256"] == prior_release["candidate_sha256"] == digest(prior_release["candidate"])
    prior_image = NdsImage.open(prior_release["candidate"])
    prior_arm = prior_image.read_file(archive.ARM)
    assert sha256(prior_arm).hexdigest() == prior_release["target_ARM9_sha256"]
    assert all(bytes_at(prior_arm, lo, hi - lo) == bytes_at(arm, lo, hi - lo) for lo, hi in SPANS)
    prior_rows = archive.common_rows(prior_image.read_file(archive.COMMON), prior_arm)
    observed_ids = sorted({row["message_ID"] for row in prior["native_requests"]})
    assert all(prior_rows[key].text == current_rows[key].text for key in observed_ids)
    village, village_release = map(read, (azores.VISIT, azores.RELEASE))
    assert digest(azores.VISIT) == azores.VISIT_SHA
    assert village["cold_boot"] and not village["savestate_loaded"] and not village["callback_errors"]
    assert not any(value for key, value in village.items() if key.startswith("synthetic_"))
    assert village["ROM_sha256"] == village_release["candidate_sha256"] == digest(village_release["candidate"])
    village_arm = NdsImage.open(village_release["candidate"]).read_file(archive.ARM)
    assert sha256(village_arm).hexdigest() == village_release["target_ARM9_sha256"]
    dependencies = ((MENU_ROUTINE, 0x020BA51C), (VILLAGE_MENU, VILLAGE_MENU + 0x30))
    for lo, hi in dependencies:
        assert bytes_at(village_arm, lo, hi - lo) == bytes_at(arm, lo, hi - lo)
    frames = callers.shots(village, "_navigation.png")
    for frame in (14580, 14860, 15050):
        assert digest(frames[frame]["path"]) == frames[frame]["PNG_sha256"]
    return dict(syracuse=dict(earlier_ordinary_gameplay=reference(syracuse.OUT), scope=prior["scene_scope"],
                              ROM_sha256=prior_release["candidate_sha256"], matched_exact_spans=len(SPANS),
                              exact_installed_bodies=observed_ids),
                azores=dict(earlier_ordinary_gameplay=reference(azores.VISIT), ROM_sha256=village["ROM_sha256"],
                            candidate_exact_menu_dependencies=dependencies,
                            reviewed_frames={frame: frames[frame] for frame in (14580, 14860, 15050)}))


def main():
    rel = read(current.RELEASE)
    assert digest(REGISTRY) == rel["registry_sha256"] and digest(CLEAN) == rel["clean_input_sha256"]
    assert digest(current.ROM) == rel["candidate_sha256"]
    src, rom = (NdsImage.open(path) for path in (CLEAN, current.ROM))
    clean, installed = (image.read_file(archive.ARM) for image in (src, rom))
    assert sha256(installed).hexdigest() == rel["target_ARM9_sha256"]
    old_rows = archive.common_message_entries(src.read_file(archive.COMMON), clean, clean=True)
    new_rows = archive.common_rows(rom.read_file(archive.COMMON), installed)
    prior = read(callers.ROOT / "ceuta_archived_dialogue_current_20261124.json")["archived_records"]
    retained = {}
    for n in (750, 751, 752):
        a, b = old_rows[n], new_rows[n]
        receipt = prior[str(n)]
        assert a.text.hex() == receipt["clean_reference"]["exact_hex"]
        assert b.text.hex() == receipt["installed_reference"]["exact_hex"]
        retained[n] = receipt
    layout = source_layout(clean, installed)
    proofs = []
    for arm in (clean, installed):
        cpu = machine(arm)
        proofs.append(dict(menu_choice_forwarding=options(cpu), market_option_routes=routes(cpu),
                           deal_finish_and_back=deal_actions(cpu), deal_loop_conditions=loop_conditions(cpu),
                           back_reset_boundaries=reset_on_back(cpu)))
    assert proofs[0] == proofs[1]
    write(OUT, dict(candidate_sha256=rel["candidate_sha256"], source_and_installed_layout=layout,
                    same_native_results=proofs[1], archived_records=retained,
                    earlier_live_controls=existing_play(installed, new_rows),
                    ownership_scope="Offline native selector tests with supplied UI decisions and external calls stopped or stubbed at their boundaries. "
                                    "The standard Market and Deal dispatchers expose the listed actions with no restart dialogue on the tested Back route. "
                                    "Other indirect display routes remain open.",
                    new_gameplay_runs=0, ROM_changed=False, new_editorial_credit=0))
    total = sum(map(len, proofs[1].values()))
    print(f"Verified both Market menu tables and {total} original dispatcher cases per ROM.")


if __name__ == "__main__":
    main()
