"""Refresh private reference/ISA and earlier getter/formatting preservation."""

import re
import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch import item_diplomacy_runtime as runtime
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.inventory_shipyard_storage_v760 import units
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/item_diplomacy_runtime_v785')
CURRENT = Path('out/all_routes_combined_v783_candidate.nds')


def census(rom, spans, private):
    def hit(target):
        return any(lo <= target < hi for lo, hi in spans)
    def internal(at):
        return any(lo <= at < hi for lo, hi in private)
    rows = []
    thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for name, base, raw in units(rom)+[('ARM7', rom.rom.arm7RamAddress, bytes(rom.rom.arm7))]:
        for m in re.finditer(rb'(?=(...\x02))', raw, re.S):
            target = int.from_bytes(m.group(1), 'little')
            if hit(target):
                at = base+m.start()
                rows.append(['absolute', name, at, target, internal(at)])
        for offset in range(0, len(raw)-3, 4):
            word = struct.unpack_from('<I', raw, offset)[0]
            at, target, kind = base+offset, None, None
            if word & 0x0E000000 == 0x0A000000:
                d = word & 0xFFFFFF
                d -= 0x1000000 if d & 0x800000 else 0
                target, kind = at+8+4*d, 'ARM_branch'
            elif word & 0x0E0F0000 == 0x020F0000 and (word >> 21) & 15 in (2, 4):
                value, shift = word & 255, ((word >> 8) & 15)*2
                value = ((value >> shift) | (value << (32-shift))) & 0xffffffff if shift else value
                target = at+8+(value if (word >> 21) & 15 == 4 else -value)
                kind = 'ADR'
            if target is not None and hit(target):
                rows.append([kind, name, at, target, internal(at)])
        for offset in range(0, len(raw)-3, 2):
            a, b = struct.unpack_from('<HH', raw, offset)
            if a & 0xF800 != 0xF000 or b & 0xF800 not in (0xE800, 0xF800):
                continue
            inst = next(thumb.disasm(raw[offset:offset+4], base+offset), None)
            if inst and inst.mnemonic in ('bl', 'blx') and inst.op_str.startswith('#'):
                target = int(inst.op_str[1:], 0) & ~1
                if hit(target):
                    at = base+offset
                    rows.append(['Thumb_BL_BLX', name, at, target, internal(at)])
    return rows


def main():
    plan = read(ROOT/'runtime_plan.json')
    source = NdsImage.open(CURRENT)
    arm = source.read_file('/__arm9__.bin')
    target = (ROOT/'ARM9_RUNTIME_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == plan['source_ARM9_sha256'] == runtime.SOURCE
    assert sha(target) == plan['research_ARM9_sha256']
    assert plan['producer_sha256'] == sha(Path('scripts/verify_item_runtime_v785.py').read_bytes())
    assert plan['runtime_sha256'] == sha(Path(runtime.__file__).read_bytes())
    restored = bytearray(target)
    for row in plan['patches']:
        at = row['address']-BASE
        before, after = map(bytes.fromhex, (row['source_hex'], row['target_hex']))
        assert target[at:at+len(after)] == after and arm[at:at+len(before)] == before
        restored[at:at+len(before)] = before
    assert bytes(restored) == arm
    # All old source type labels, their table, both getters and the V626 code
    # are untouched. New type strings have not yet been installed.
    assert target[0x14C530:0x14C610] == arm[0x14C530:0x14C610]
    assert target[0x93D28:0x93D6C] == arm[0x93D28:0x93D6C]
    owner = read(ROOT/'source_tail_ownership.json')
    start = owner['source_record_start']
    prefix = bytes.fromhex(owner['preserved_active_prefix_hex'])
    assert target[start:start+len(prefix)] == prefix

    ownership_plan = read('work/analysis/recruitment_owned_v772/owned_runtime_plan.json')
    private = ownership_plan['private_spans']
    spans = private+[[runtime.BOOM, runtime.BOOM+20]]
    after_rom = NdsImage.open(CURRENT)
    after_rom.rom.arm9 = target
    before_refs, after_refs = [census(r, spans, private) for r in (source, after_rom)]
    external_before = [r for r in before_refs if not r[-1]]
    external_after = [r for r in after_refs if not r[-1]]
    assert external_before == external_after
    old = read('work/analysis/recruitment_owned_v772/storage_reference_census.json')
    historical = sorted([kind, name, at, to, False]
        for kind, values in old['references'].items()
        if kind in ('absolute', 'ARM_branch', 'ADR', 'Thumb_BL_BLX')
        for name, at, to in values
        if any(lo <= to < hi for lo, hi in private)
        and not any(lo <= at < hi for lo, hi in private))
    # The census precedes V772 installation. Its registered source-guarded
    # dispatcher patch changed precisely this old GATE branch to the bridge.
    rebind = next(r for r in ownership_plan['patches'] if r['address'] == 0x01FFCF3C)
    for name, base, raw in units(source):
        if base <= rebind['address'] < base+len(raw):
            at = rebind['address']-base
            assert raw[at:at+4].hex() == rebind['target_hex']
    old_row = ['ARM_branch', 'section4', 0x01FFCF3C, runtime.GATE, False]
    assert historical.count(old_row) == 1
    historical[historical.index(old_row)][3] = runtime.bank.ENTRY
    historical.sort()
    actual_old_bank = sorted(r for r in external_before
        if any(lo <= r[3] < hi for lo, hi in private))
    assert actual_old_bank == historical, (actual_old_bank, historical)
    save(ROOT/'private_reference_census.json', {'private_spans': private,
        'source_tail': [runtime.BOOM, runtime.BOOM+20],
        'before': before_refs, 'after': after_refs,
        'external_incoming_references_preserved': external_after,
        'earlier_owned_bank_external_contracts_exact': True,
        'documented_V772_dispatcher_rebind': rebind,
        'raw_tail_data_leads_qualified_by_original_consumer': owner['source_bound_coordinate_data_leads'],
        'unclassified_incoming_references': []})

    thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    extents = [(runtime.GATE, runtime.GATE+152),
               (runtime.bank.STATUS, runtime.bank.STATUS+64),
               (runtime.bank.STATUS_TAIL, runtime.bank.STATUS_TAIL+36)]
    instructions = []
    for lo, hi in extents:
        rows = list(thumb.disasm(target[lo-BASE:hi-BASE], lo))
        assert sum(i.size for i in rows) == hi-lo
        assert all(i.size == 2 or i.mnemonic in ('bl', 'blx') for i in rows)
        instructions += [[i.address, i.bytes.hex(), i.mnemonic, i.op_str] for i in rows]
    save(ROOT/'Thumb_ISA_audit.json', {'exact_code_extents': extents,
        'only16bit_Thumb1_and_ARMv5_BL_BLX': True, 'instructions': instructions})

    getter_cases = []
    for label, raw in (('V783', arm), ('research', target)):
        cpu = machine(raw)
        for kind in range(10):
            for fn in (0x93D28, 0x93D5C):
                cpu.mem_write(STACK+0x1000, bytes(16))
                cpu.mem_write(STACK+0x1004, bytes([kind]))
                before = bytes(cpu.mem_read(BASE, 0x800000))
                call(cpu, fn, [STACK+0x1000 if fn == 0x93D28 else kind])
                pointer = cpu.reg_read(UC_ARM_REG_R0)
                value = bytes(cpu.mem_read(pointer, 128)).split(b'\0', 1)[0]
                assert bytes(cpu.mem_read(BASE, 0x800000)) == before
                getter_cases.append({'version': label, 'getter': BASE+fn,
                    'type': kind, 'pointer': pointer, 'text': value.decode('cp932'), 'hex': value.hex()})
    assert [{k:v for k,v in r.items() if k != 'version'} for r in getter_cases[:20]] == [
        {k:v for k,v in r.items() if k != 'version'} for r in getter_cases[20:]]
    assert [r['text'] for r in getter_cases[:20:2]][6:] == ['Lure Fleet', 'Forge Papers', 'Bad Rumors', 'Bribe']
    save(ROOT/'type_getter_preservation.json', {'cases': getter_cases,
        'all40_complete_pointer_text_8MiB_and_callee_saved_ABI_cases_pass': True,
        'type0_through5_remain_Japanese_pending_implementation': True})

    reference = read('work/analysis/dialogue_formatting_user_recheck_v782/COMMON676_677.json')
    entries = common_message_entries(source.read_file('/COMMON/MESFILE.DK4'), target, clean=False)
    cpu = machine(target)
    # Model the unchanged original startup copy before entering the older
    # paragraph path, whose formatter remains in the late pool.
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(target, BASE).sections[3].data[:-48]))
    cases = []
    for row in reference['entries']:
        n = row['id']
        formatted, lines = native_layout(cpu, entries[n].text, n, ())
        assert lines == row['lines'] and formatted.hex() == row['native_formatted_hex']
        cases.append({'id': n, 'lines': lines, 'native_formatted_hex': formatted.hex()})
    save(ROOT/'user676_677_preserved.json', {'cases': cases,
        'scope': 'Research ARM9/native wrapping only; V747 remains the earlier actual scene evidence.'})
    save(ROOT/'preservation_audit.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'research_ARM9_sha256': sha(target), 'only_six_declared_source_guarded_patches': True,
        'all_earlier_external_private_incoming_contracts_preserved': True,
        'old_strategist_code_and_all10_type_labels_and_table_preserved': True,
        'all40_type_getter_cases_pass': True, 'user676_677_repaired_formatting_preserved': True,
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'new_playable_ROM_or_production_dialogue_approval': False})
    print('Private incoming contracts/Thumb ISA,40 original getter cases and repaired676/677 pass;no ROM built.', flush=True)


if __name__ == '__main__':
    main()
