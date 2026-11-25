"""Native research scope/ABI/status equivalence and exact source-tail ownership."""

import inspect
import re
import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R9, UC_ARM_REG_R11)

from dk4tool.patch import item_diplomacy_runtime as new
from dk4tool.patch import recruitment_editorial_runtime as bank
from dk4tool.patch import shared_dialogue_runtime as previous
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts import research_scheme_selector_v775 as old_scope
from scripts import verify_recruitment_runtime_v771 as old_status
from scripts.inventory_shipyard_storage_v760 import units
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/item_diplomacy_runtime_v785')
CURRENT = Path('out/all_routes_combined_v783_candidate.nds')


def ownership(rom):
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    lo, hi = new.BOOM, new.BOOM+20
    lead = next(r for r in read('work/analysis/tavern_runtime_v769/padded_allocation_leads_small_NOT_FREE.json')
                if r['lo'] == lo and hi <= r['hi'])
    start = lead['original_string_offset']
    source_record = next(r for r in lead['lead_sources']
        if clean[start:start+len(bytes.fromhex(r['original_source_hex']))] == bytes.fromhex(r['original_source_hex']))
    prefix = arm[start:arm.index(0, start)+1]
    assert prefix[:-1].decode('ascii') == lead['current']
    assert BASE+start+len(prefix) <= lo < hi <= BASE+start+len(bytes.fromhex(source_record['original_source_hex']))
    assert arm[lo-BASE:hi-BASE] == bytes(20)
    # Preserve the whole existing strategist alignment/fallback code, which
    # invalidated the initial no-absolute-reference-only storage lead.
    rejected_lo, rejected_hi = 0x0214C550, 0x0214C564
    assert arm[rejected_lo-BASE:rejected_hi-BASE] != clean[rejected_lo-BASE:rejected_hi-BASE]
    absolute, relative = [], []
    thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for name, base, raw in units(rom)+[('ARM7', rom.rom.arm7RamAddress, bytes(rom.rom.arm7))]:
        for m in re.finditer(rb'(?=(...\x02))', raw, re.S):
            target = int.from_bytes(m.group(1), 'little')
            if lo <= target < hi:
                absolute.append([name, base+m.start(), target])
        for at in range(0, len(raw)-3, 4):
            pc, word = base+at, struct.unpack_from('<I', raw, at)[0]
            if word & 0x0E000000 == 0x0A000000:
                d = word & 0xffffff
                d -= 0x1000000 if d & 0x800000 else 0
                target = pc+8+d*4
                if lo <= target < hi:
                    relative.append(['ARM_branch', name, pc, target])
            if word & 0x0E0F0000 == 0x020F0000 and (word >> 21) & 15 in (2, 4):
                v, rotate = word & 255, ((word >> 8) & 15)*2
                v = ((v >> rotate) | (v << (32-rotate))) & 0xffffffff if rotate else v
                target = pc+8+(v if (word >> 21) & 15 == 4 else -v)
                if lo <= target < hi:
                    relative.append(['ADR', name, pc, target])
        for at in range(0, len(raw)-3, 2):
            a, b = struct.unpack_from('<HH', raw, at)
            if a & 0xF800 != 0xF000 or b & 0xF800 not in (0xE800, 0xF800):
                continue
            i = next(thumb.disasm(raw[at:at+4], base+at), None)
            if i and i.mnemonic in ('bl', 'blx') and i.op_str.startswith('#'):
                target = int(i.op_str[1:], 0) & ~1
                if lo <= target < hi:
                    relative.append(['Thumb_branch', name, base+at, target])
    # Two words of the original coordinate array decode as ARM branches. Bind
    # their classification to the original base literal, unchanged consumer,
    # complete array and actual halfword loads; never ignore a numeric range
    # just because its bytes look like data.
    expected_data_leads = [['ARM_branch', 'section0', 0x02163700, 0x0216DF08],
                           ['ARM_branch', 'section0', 0x02164704, 0x0216DF0C]]
    assert relative == expected_data_leads, relative
    data_lo, data_hi = 0x0216215C, 0x0216515C
    assert arm[data_lo-BASE:data_hi-BASE] == clean[data_lo-BASE:data_hi-BASE]
    assert struct.unpack_from('<I', clean, 0x6AAF4)[0] == data_lo
    assert arm[0x6A774:0x6A898] == clean[0x6A774:0x6A898]
    cpu = machine(arm)
    data_cases = []
    for _, _, at, _ in relative:
        cpu.reg_write(UC_ARM_REG_R4, STACK+0x1000)
        cpu.reg_write(UC_ARM_REG_R5, data_lo)
        cpu.reg_write(UC_ARM_REG_R9, (at-data_lo)//4)
        cpu.reg_write(UC_ARM_REG_R11, STACK+0x1100)
        cpu.emu_start(0x0206A7D4, 0x0206A800, count=32)
        expected = arm[at-BASE:at-BASE+4]
        assert bytes(cpu.mem_read(STACK+0x1000, 4)) == expected
        data_cases.append({'address': at, 'coordinate_pair_hex': expected.hex(),
                           'original_consumer_7D4_800_reads_and_streams_two_halfwords': True})
    assert not absolute, absolute
    crossing = []
    for name, base, raw in units(rom)+[('ARM7', rom.rom.arm7RamAddress, bytes(rom.rom.arm7))]:
        for m in re.finditer(rb'(?=(...\x02))', raw, re.S):
            target = int.from_bytes(m.group(1), 'little')
            if not BASE+start <= target < lo:
                continue
            end = arm.find(b'\0', target-BASE, hi-BASE)
            if end < 0 or BASE+end >= lo:
                crossing.append([name, base+m.start(), target, end])
    assert not crossing, crossing
    assert arm[0x93D28:0x93D6C] == clean[0x93D28:0x93D6C]
    proof = {'span': [lo, hi], 'source_record': source_record,
        'source_record_start': start, 'preserved_active_prefix_hex': prefix.hex(),
        'current_tail_hex': arm[lo-BASE:hi-BASE].hex(),
        'current_absolute_references': absolute,
        'raw_ARM_ADR_Thumb_branch_leads': relative,
        'source_bound_coordinate_data_leads': {'span': [data_lo, data_hi],
            'entire_source_current_array_sha256': sha(arm[data_lo-BASE:data_hi-BASE]),
            'source_current_consumer_sha256': sha(arm[0x6A774:0x6A898]),
            'original_base_literal': 0x0206AAF4, 'native_cases': data_cases},
        'unclassified_incoming_references': [],
        'crossing_Cstrings': crossing,
        'source_bounded_immutable_UI_string_tail_not_generic_zero_padding': True,
        'rejected_old_scheme_storage': {'span': [rejected_lo, rejected_hi],
            'reason': 'V626 active strategist alignment code; no absolute pointer is insufficient ownership evidence.',
            'current_hex': arm[rejected_lo-BASE:rejected_hi-BASE].hex()},
        'other_source_type_strings_and_getter_table_unchanged': True}
    save(ROOT/'source_tail_ownership.json', proof)
    return proof


def scope(arm):
    cpu = machine(arm)
    for at, blob in new.code().items():
        cpu.mem_write(at, blob)
    targets = (0x01FFCF40, LITERAL, bank.COORD, bank.STATUS)
    hooks = [cpu.hook_add(UC_HOOK_CODE, lambda c, p, s, d: c.emu_stop(), begin=t, end=t) for t in targets]
    records = {p: (off, high, set(values)) for p, off, high, values in new.contract_rows()}

    def check(parent, number, queue=0, gift=0):
        regs = {r: 0xA5A50000+i for i, r in enumerate(old_scope.REGS)}
        for r, v in regs.items():
            cpu.reg_write(r, v)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        fields = {0x274: number, 0x27C: queue, 0x270: gift}
        for offset, value in ((0x264, parent), *fields.items()):
            cpu.mem_write(STACK+offset, struct.pack('<I', value))
        cpu.emu_start(bank.ENTRY, STOP, count=10000)
        route = 0x01FFCF40
        if parent in records:
            offset, high, allowed = records[parent]
            value = fields[offset]
            if value >> 16 == high and value & 65535 in allowed:
                n = value & 65535
                route = bank.COORD if not high and n in (842, 1028, 1029) else bank.STATUS if not high and n in (905, 906) else LITERAL
        assert cpu.reg_read(UC_ARM_REG_PC) == route, (hex(parent), number, hex(queue), hex(gift), hex(cpu.reg_read(UC_ARM_REG_PC)), hex(route))
        assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_LR) == STOP
        for reg, value in regs.items():
            expected = parent if reg == old_scope.UC_ARM_REG_R3 and route == 0x01FFCF40 else value
            assert cpu.reg_read(reg) == expected

    count = 0
    try:
        for parent in (0x02053D24, 0x02053DB8):
            for low in range(0x7B20, 0x8490):
                for number in (0, 1072, 1117, 3667):
                    check(parent, number, 0x02110000 | low)
                    count += 1
        for parent in (0x02054014, 0x02053FCC, 0x02053C5C, 0x02053E38):
            for number in range(3668):
                check(parent, number, number, number)
                count += 1
        for low in range(0x65F0, 0x6840):
            check(0x02053C14, 0, gift=0x02110000 | low)
            count += 1
        for parent in (*records, 0, 0xffffffff, 0x12053D24):
            for high in (0, 0x0211, 0x1211, 0xffff):
                for low in (0, 842, 905, 1073, 1117, 0x6610, 0x66F0, 0x7F60, 0x80A0, 0x80B0, 0x8160, 0xffff):
                    value = high << 16 | low
                    check(parent, 1138, value, value)
                    count += 1
    finally:
        for h in hooks:
            cpu.hook_del(h)
    save(ROOT/'scope_proof.json', {'cases': count, 'all_old_and_new_exact_contracts_and_registers_SP_LR_pass': True,
        'role_pointer_stride32_and_queued_stride16_reject_every_tested_between_address': True,
        'pointer_indices_biased_away_from_numeric_coordinate_and_status_routes': True,
        'gate_bytes': 164, 'table_allocation_bytes': 128, 'private_gate_and_suffix_literal_bytes': 168,
        'no_production_ROM_or_gameplay_claim': True})
    print(f'{count} native selector/scope/register cases pass.', flush=True)


def statuses(arm):
    def make(source, changed=False, raw=None):
        cpu = machine(source)
        if raw is not None:
            cpu.mem_write(BASE, raw)
        if changed:
            for at, blob in new.code().items():
                cpu.mem_write(at, blob)
        return cpu
    source = inspect.getsource(old_status.field_contracts)
    source = source.replace('u.emu_start(runtime.STATUS,STOP', 'u.emu_start(runtime.STATUS|1,STOP')
    source = source.replace('STACK-BASE-32:STACK-BASE', 'STACK-BASE-36:STACK-BASE')
    env = {**old_status.__dict__, 'runtime': bank, 'make': make,
           'ROOT': Path('work/analysis/tavern_recruitment_editorial_v771')}
    exec(compile(source, __file__, 'exec'), env)
    cases = env['field_contracts'](arm)
    assert len(cases) == 140
    save(ROOT/'status_contracts.json', {'cases': cases, 'count': len(cases),
        'all_whole8MiB_guards_original_status_UI_labels_and_registers_SP_LR_exact': True,
        'only_declared_final_field_suffix_and36_stack_bytes_mutable': True,
        'effective_verifier_sha256': sha(source.encode())})
    print('140 complete8MiB status/ABI preservation cases pass.', flush=True)


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    assert sha(arm) == new.SOURCE
    ownership(rom)
    scope(arm)
    statuses(arm)
    patched = bytearray(arm)
    old = bank.assemble()
    assert arm[bank.STATUS-BASE:bank.STATUS-BASE+len(old[bank.STATUS])] == old[bank.STATUS]
    assert arm[bank.STATUS_TAIL-BASE:bank.STATUS_TAIL-BASE+len(old[bank.STATUS_TAIL])] == old[bank.STATUS_TAIL]
    assert arm[bank.PACKED_PHRASES-BASE:bank.PACKED_PHRASES-BASE+24] == old[bank.PACKED_PHRASES]
    plan = read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')
    spans = plan['private_spans']+[[new.BOOM, new.BOOM+20]]
    patches = []
    for at, blob in new.code().items():
        assert any(lo <= at and at+len(blob) <= hi for lo, hi in spans)
        patches.append({'address': at, 'source_hex': arm[at-BASE:at-BASE+len(blob)].hex(), 'target_hex': blob.hex()})
        patched[at-BASE:at-BASE+len(blob)] = blob
    target = bytes(patched)
    before, after = [MainCodeFile(v, BASE) for v in (arm, target)]
    assert len(arm) == len(target) and cache_plan(arm) == cache_plan(target)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in after.sections]
    assert bytes(after.save()) == target
    (ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'runtime_plan.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_ARM9_sha256': sha(arm),
        'research_ARM9_sha256': sha(target), 'patches': patches,
        'all_section_BSS_cache_startup_arena_and123040_byte_staged_payload_geometry_preserved': True,
        'research_only_Guild_bindings_type_phrases_COMMON_registration_and_actual_scenes_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'runtime_sha256': sha(Path(new.__file__).read_bytes()),
        'full_goal_complete': False})
    print('Six typed patches fit existing memory;research ARM9 saved. No playable ROM,prose integration or completion credit.', flush=True)


if __name__ == '__main__':
    main()
