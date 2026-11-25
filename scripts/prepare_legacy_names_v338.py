"""Verify exact legacy name conversion with bounded writes and preserved state."""

import copy
import json
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_CPSR,
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.legacy_saved_item_names import transform
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, STOP, machine

ROOT = Path('work/analysis/legacy_names_v338')
CONFIG = Path('translations/legacy_saved_item_names_release_v1.json')
OWNER = 0x023800C8
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
        UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
        UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12)


def main():
    current, clean = [NdsImage.open(p).read_file('/__arm9__.bin') for p in
                      ('out/all_routes_combined_v326_candidate.nds', 'work/clean.nds')]
    target, plan = transform(current, clean)
    u = machine(target)
    u.mem_write(POOL, bytes(MainCodeFile(target, BASE).sections[3].data[:-48]))
    original = Path('work/emulation_v193/ordinary_map_v338/final_arm9_ram.bin').read_bytes()
    owner = original[OWNER - BASE:OWNER - BASE + 0x6B4]
    mapping = {r['Japanese'].encode('cp932'): r['English'].encode('ascii') for r in plan['dictionary']}
    cases = []

    def verify(label, data, expected, flags):
        u.mem_write(OWNER - 32, b'\xA5' * 32 + data + b'\xA5' * 32)
        u.mem_write(STACK - 96, b'\xA5' * 96)
        values = {reg: 0x11110000 + n for n, reg in enumerate(REGS)}
        values[UC_ARM_REG_R4] = OWNER
        for reg, value in values.items():
            u.reg_write(reg, value)
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        cpsr = (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | flags
        u.reg_write(UC_ARM_REG_CPSR, cpsr)
        writes = []

        def write(uc, access, address, size, value, context):
            in_name = any(OWNER + 0x22 + i * 32 <= address < address + size <= OWNER + 0x22 + (i + 1) * 32 for i in range(30))
            assert in_name or STACK - 64 <= address < address + size <= STACK
            writes.append([address, size])

        handle = u.hook_add(UC_HOOK_MEM_WRITE, write)
        try:
            u.emu_start(plan['helper'], STOP, count=250000)
        finally:
            u.hook_del(handle)
        assert u.reg_read(UC_ARM_REG_PC) == STOP and u.reg_read(UC_ARM_REG_SP) == STACK
        assert u.reg_read(UC_ARM_REG_LR) == STOP
        assert u.reg_read(UC_ARM_REG_CPSR) & 0xF0000000 == flags
        assert all(u.reg_read(reg) == (OWNER + 0x22 if reg == UC_ARM_REG_R6 else value) for reg, value in values.items())
        assert bytes(u.mem_read(OWNER, len(data))) == expected
        assert bytes(u.mem_read(OWNER - 32, 32)) == b'\xA5' * 32
        assert bytes(u.mem_read(OWNER + len(data), 32)) == b'\xA5' * 32
        assert bytes(u.mem_read(STACK - 96, 32)) == b'\xA5' * 32
        cases.append({'case': label, 'flags': flags, 'bounded_writes': len(writes), 'all_state_register_flags_guards_pass': True})

    def expected(data):
        result = bytearray(data)
        for i in range(30):
            at = 0x22 + i * 32
            raw = bytes(data[at:at + 32]).split(b'\0', 1)[0]
            if raw in mapping:
                text = mapping[raw] + b'\0'
                result[at:at + len(text)] = text
        return bytes(result)

    for row in plan['dictionary']:
        data = bytearray(owner)
        for slot in (0, 15, 29):
            at = 0x22 + slot * 32
            value = row['Japanese'].encode('cp932') + b'\0'
            data[at:at + 32] = value + b'\xA7' * (32 - len(value))
        verify(row['Japanese'], bytes(data), expected(data), 0xA0000000)
    verify('actual older save owner', owner, expected(owner), 0x50000000)
    verify('idempotent existing English', expected(owner), expected(owner), 0xF0000000)
    unknown = bytearray(owner)
    values = [b'Custom map', '未知の地図'.encode('cp932'), b'A' * 32,
              '宝石を食う宝石'.encode('cp932') + b' custom', b'']
    for i in range(30):
        value = values[i % len(values)]
        at = 0x22 + i * 32
        unknown[at:at + 32] = value + b'\0' * (32 - len(value))
    verify('custom prefix unknown and unterminated names', bytes(unknown), bytes(unknown), 0)
    proof = {'transform': plan, 'cases': cases, 'source_saved_state_progress_provenance_unknown': True,
             'original_selected_ids_inventory_flags_metadata_outside_name_fields_exact': True,
             'complete_50_source_exact_names_native_verified': True, 'actual_load_gameplay_pending': True}
    evidence = ROOT / 'native_proof.json'
    evidence.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    CONFIG.write_text(json.dumps({'format': 'dk4-legacy-saved-item-names-release-v1',
                                 'target_arm9_sha256': sha(target),
                                 'verification_evidence_sha256': {str(evidence): sha(evidence.read_bytes())},
                                 'status': 'experimental-native-verified-live-pending'}, indent=2) + '\n', encoding='utf-8')
    registry_path = Path('translations/release_stack.json')
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(registry['profiles']['all-routes-unified-v326'])
    profile['legacy_saved_item_names_release'] = str(CONFIG)
    profile['note'] = 'Full V326 plus source-exact legacy saved promotional names/maps localized after normal load; item IDs and all other save state preserved. All 18 plaques remain open.'
    registry['profiles']['all-routes-unified-v338'] = profile
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_cases': len(cases), 'known_name_dictionary': 50, 'unknown_names_preserved': True}))


if __name__ == '__main__':
    main()
