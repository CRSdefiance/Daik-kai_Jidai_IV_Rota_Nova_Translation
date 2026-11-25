"""Stage regular digits at the registered Price Info fee formatting call site."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType, SimpleNamespace

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_SP

from dk4tool.patch.yard_numerals_20261124 import BASE, HELPER, ITCM, NUMBER, assemble, cache_plan, compact_helper
from scripts import register_lisbon_roster_galley_20261124 as parent
from scripts import stage_tunis_shop_advice_20261124 as release_checks
from scripts import verify_syracuse_investment_20261124 as observed
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_inn_numerals_native_20261119 import RING, RING_SIZE, normalize, read_cstring
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_yard_numerals_native_20261124 import STACK


ARM, COMMON = parent.ARM, parent.COMMON
ROOT = parent.build.ROOT.with_name("editorial_20261124_price_info_digits")
ROM = ROOT / "Price_Info_Digits_STAGED.nds"
STORED, OUT = ROOT / "stored_proof.json", ROOT / "price_info_digits_review.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
RELEASE = parent.RELEASE
played = SimpleNamespace(RELEASE=RELEASE)
CALL, TAIL, FORMAT = 0x0208A97C, 0x0208A994, 0x0214C04C
FEE = 0x020BB1F4
FIELD = "ARM9_PRICE_INFO_FEE_DIGITS"
NAMES, FEES = ("Syracuse", "St. George's", "Cape of Good Hope"), (0, 50, 200)


def native_quotes(arm, target):
    current = read(RELEASE)
    startup = read(current["own_registered_startup"])
    raw = startup["read_only_snapshot"]
    snapshot = Path(raw["path"]).read_bytes()
    assert sha256(snapshot).hexdigest() == raw["sha256"] and startup["candidate_sha256"] == current["candidate_sha256"]
    offset = CALL - BASE
    assert snapshot[offset:offset + 4] == arm[offset:offset + 4]
    newer = snapshot[:offset] + target[offset:offset + 4] + snapshot[offset + 4:]
    previous, updated = (get_machine(code, state)[0] for code, state in ((arm, snapshot), (target, newer)))
    initial = bytes(previous.mem_read(RING, RING_SIZE))
    assert bytes(updated.mem_read(RING, RING_SIZE)) == initial
    buffer = 0x023F0200
    cases = []
    for index in range(32):
        name, value = NAMES[index % len(NAMES)], FEES[index % len(FEES)]
        if index < 9:
            name, value = NAMES[index // 3], FEES[index % 3]
        output = []
        for cpu in (previous, updated):
            cpu.mem_write(RING, initial[:8] + pack("<I", index) + initial[12:])
            cpu.mem_write(buffer, name.encode("ascii") + bytes(1))
            cpu.reg_write(UC_ARM_REG_R4, buffer)
            cpu.reg_write(UC_ARM_REG_R5, value)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.emu_start(CALL - 4, TAIL, count=15000)
            assert cpu.reg_read(UC_ARM_REG_PC) == TAIL and cpu.reg_read(UC_ARM_REG_SP) == STACK
            addr = cpu.reg_read(UC_ARM_REG_R0)
            assert addr == RING + 12 + ((index + 1) % 32) * 128
            text = read_cstring(cpu, addr)
            assert len(text) < 128
            output.append((text, bytes(cpu.mem_read(RING, RING_SIZE))))
        (old, old_ring), (new, new_ring) = output
        expected = f"{name}: {value} coins".encode("ascii")
        assert old != new and normalize(old) == new == expected
        assert len(new) < len(old)
        permitted = {index, (index + 1) % 32}
        for other in set(range(32)) - permitted:
            lo = 12 + other * 128
            assert old_ring[lo:lo + 128] == new_ring[lo:lo + 128] == initial[lo:lo + 128]
        cases.append(dict(city=name, fee=value, ring_slot=index, previous_hex=old.hex(), installed_hex=new.hex(),
                          bytes_saved=len(old) - len(new)))
    return cases


def stage():
    previous, ordinary = map(read, (RELEASE, observed.OUT))
    assert digest(REGISTRY) == previous["registry_sha256"] and digest(CLEAN) == previous["clean_input_sha256"]
    assert digest(parent.ROM) == ordinary["candidate_sha256"] == previous["candidate_sha256"]
    local_quote = ordinary["local_quote"]
    assert local_quote["exact_source_font_plane"] and local_quote["cp932_full_width_amount"]
    clean, active = map(NdsImage.open, (CLEAN, parent.ROM))
    ja, arm = [image.read_file(ARM) for image in (clean, active)]
    assert sha256(arm).hexdigest() == previous["target_ARM9_sha256"]
    source, current = (code[FORMAT - BASE:].split(bytes(1), 1)[0] for code in (ja, arm))
    assert source.count(b"%s") == current.count(b"%s") == 2 and current == b"%s: %s coins"
    assert unpack_from("<I", arm, 0x208A9C4 - BASE) == (FORMAT,)
    assert all(ja[lo - BASE:hi - BASE] == arm[lo - BASE:hi - BASE] for lo, hi in
               ((0x0208A928, 0x0208A994), (FEE, FEE + 0x44), (NUMBER, NUMBER + 0x7C), (0x020ABFCC, 0x020AC02C)))
    fee_code = arm[FEE - BASE:FEE - BASE + 0x44]
    assert fee_code[12:16] == assemble("mov r4, #200", FEE + 12)
    assert fee_code[20:24] == assemble("moveq r4, #0", FEE + 20)
    assert fee_code[52:56] == assemble("movgt r4, #50", FEE + 52)
    itcm = MainCodeFile(arm, BASE).sections[4]
    helper = compact_helper()
    assert itcm.ramAddress == ITCM and bytes(itcm.data[HELPER - ITCM:HELPER - ITCM + len(helper)]) == helper
    offset = CALL - BASE
    original, replacement = assemble(f"bl {NUMBER}", CALL), assemble(f"bl {HELPER}", CALL)
    assert arm[offset:offset + 4] == original
    target = arm[:offset] + replacement + arm[offset + 4:]
    assert target[:offset] + original + target[offset + 4:] == arm
    assert cache_plan(arm) == cache_plan(target)
    assert parent.template.right_bound(arm, previous["right_bound_configuration"]) == parent.template.right_bound(target, previous["right_bound_configuration"])
    cases = native_quotes(arm, target)
    active.replace_file(ARM, target)
    binary = bytes(active.rom.save())
    active.replace_file(ARM, arm)
    assert sha256(active.rom.save()).hexdigest() == previous["candidate_sha256"]
    ROOT.mkdir(exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == binary
    else:
        with ROM.open("xb") as output:
            output.write(binary)
    candidate = digest(ROM)
    reference_fields = dict(file_path=ARM, format_address=FORMAT, number_call=CALL, arguments=["Town name", "Price Info fee"])
    row = dict(id=FIELD, file_path=ARM, english="Syracuse: 0 coins", speaker="Price Info",
        context="Select a town in Market Info to see the price for viewing its commodity prices.",
        source_meaning="Show the selected town and the exact fee. Viewing the current town is free.",
        localization_note="Keep the current wording and fee amounts. Use the installed regular-digit converter at this single quote call.",
        source_reference=reference_fields | dict(template_hex=source.hex(), number_call_hex=original.hex()),
        current_reference=reference_fields | dict(template_hex=current.hex(), number_call_hex=original.hex()),
        installed_reference=reference_fields | dict(template_hex=current.hex(), number_call_hex=replacement.hex()),
        decision="revision", review=dict.fromkeys(GATES, True))
    write(OUT, dict(candidate_sha256=candidate, inherited_candidate_sha256=previous["candidate_sha256"],
        ordinary_baseline=reference(observed.OUT), records=[row], number_cases=cases,
        exact_fee_selector_code_hex=fee_code.hex(), fee_range=list(FEES), installed_widths_only=True,
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1", review_gates=list(GATES)))
    write(STORED, dict(candidate=str(ROM), candidate_sha256=candidate, predecessor_sha256=previous["candidate_sha256"],
        clean_input_sha256=previous["clean_input_sha256"], target_ARM9_sha256=sha256(target).hexdigest(),
        target_COMMON_sha256=previous["target_COMMON_sha256"], whole_parent_inverse=True, source_preflight=reference(OUT),
        changed_files=[ARM], instruction_changes=[dict(address=CALL, before_hex=original.hex(), after_hex=replacement.hex())]))
    print(f"Staged one Price Info number call. Verified {len(cases)} native quote and ring-slot cases.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("stage", "patch", "startup"))
    action = cli.parse_args().action
    if action == "stage":
        stage()
    else:
        FunctionType(release_checks.release_check.__code__, vars(release_checks) | globals())(read(STORED), action)
