"""CPU-only nominal-name provider prototype; no registered release transform."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census, CURRENT
from scripts.inventory_shipyard_storage_v760 import units
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/item_diplomacy_context_v786')
PRIOR = Path('work/analysis/item_diplomacy_runtime_v785')


def cstring(rom, at):
    for _, base, raw in units(rom):
        if base <= at < base+len(raw):
            return raw[at-base:].split(b'\0', 1)[0]
    raise AssertionError(hex(at))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    base = NdsImage.open(CURRENT)
    source = (PRIOR/'ARM9_RUNTIME_RESEARCH_ONLY.bin').read_bytes()
    previous = read(PRIOR/'runtime_plan.json')
    assert sha(source) == previous['research_ARM9_sha256'] == '288bcbfa29e2cbc6df81326bade9f074c156148cf2c2749ccabc0c570bbba4bf'
    assert sha(CURRENT.read_bytes()) == previous['source_ROM_sha256']
    storage = read(PRIOR/'type_phrase_storage_research.json')
    producer = Path('scripts/research_item_type_storage_v785.py')
    assert storage['producer_sha256'] == sha(producer.read_bytes())
    spans = storage['all132_source_owned_bytes']
    values = storage['proposed110_phrase_bytes']
    assert sum(hi-lo for lo, hi in spans) == 132 and sum(r['bytes'] for r in values) == 110
    changed = bytearray(source)
    patches = []
    for lo, hi in spans:
        before = source[lo-BASE:hi-BASE]
        assert before == base.read_file('/__arm9__.bin')[lo-BASE:hi-BASE]
        changed[lo-BASE:hi-BASE] = bytes(hi-lo)
    for row in values:
        at, raw = row['pointer'], row['text'].encode()+b'\0'
        assert len(raw) == row['bytes']
        changed[at-BASE:at-BASE+len(raw)] = raw
    for lo, hi in spans:
        patches.append({'address': lo, 'source_hex': source[lo-BASE:hi-BASE].hex(),
                        'target_hex': changed[lo-BASE:hi-BASE].hex()})
    for row in values:
        field = 0x14C5E8+row['type']*4
        old = struct.unpack_from('<I', source, field)[0]
        original = next(r for r in storage['scheme_source_labels'] if r['type'] == row['type'])
        assert original['current_pointer'] == old
        struct.pack_into('<I', changed, field, row['pointer'])
        patches.append({'address': BASE+field, 'source_hex': struct.pack('<I', old).hex(),
                        'target_hex': struct.pack('<I', row['pointer']).hex()})
    target = bytes(changed)
    restored = bytearray(target)
    for row in patches:
        at = row['address']-BASE
        raw = bytes.fromhex(row['source_hex'])
        restored[at:at+len(raw)] = raw
    assert bytes(restored) == source
    assert len(target) == len(source) and cache_plan(target) == cache_plan(source)
    code_before, code_after = [MainCodeFile(raw, BASE) for raw in (source, target)]
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in code_before.sections] == [
        (s.ramAddress, len(s.data), s.bssSize) for s in code_after.sections]
    assert bytes(code_after.save()) == target
    # Preserve both getter instructions, the live strategist bridge and RTTI.
    assert target[0x93D28:0x93D6C] == source[0x93D28:0x93D6C]
    for lo, hi in ((0x14C530, 0x14C538), (0x14C550, 0x14C564), (0x14C57C, 0x14C588),
                   (0x14C5A0, 0x14C5E8), (0x14C600, 0x14C638)):
        assert target[lo:hi] == source[lo:hi]
    research = NdsImage.open(CURRENT)
    research.rom.arm9 = target
    reference = NdsImage.open(CURRENT)
    reference.rom.arm9 = source
    before_refs, after_refs = [census(r, spans, []) for r in (reference, research)]
    expected_before = storage['all_current_incoming_reference_leads']
    assert before_refs == expected_before
    expected_after = [list(r) for r in before_refs]
    for row in expected_after:
        if 0x0214C5E8 <= row[2] < 0x0214C600:
            row[3] = values[(row[2]-0x0214C5E8)//4]['pointer']
    assert sorted(after_refs) == sorted(expected_after), after_refs

    # All57 existing village/Deck replacements stay live and complete.
    active = read('work/analysis/shipyard_storage_v760/owned_source_storage.json')['all54_village_and3_Deck_active_replacements_verified']
    for row in active:
        field = row['pointer_field']
        assert struct.unpack_from('<I', target, field)[0] == row['active_pointer']
        assert cstring(research, row['active_pointer']).hex() == row['active_complete_text_hex']

    cpu = machine(target)
    cases = []
    for kind in range(10):
        for fn in (0x93D28, 0x93D5C):
            cpu.mem_write(STACK+0x1000, bytes(16))
            cpu.mem_write(STACK+0x1004, bytes([kind]))
            before = bytes(cpu.mem_read(BASE, 0x800000))
            call(cpu, fn, [STACK+0x1000 if fn == 0x93D28 else kind])
            pointer = cpu.reg_read(UC_ARM_REG_R0)
            text = bytes(cpu.mem_read(pointer, 128)).split(b'\0', 1)[0]
            expected = values[kind]['text'].encode() if kind < 6 else cstring(reference,
                struct.unpack_from('<I', source, 0x14C5E8+kind*4)[0])
            assert text == expected and bytes(cpu.mem_read(BASE, 0x800000)) == before
            cases.append({'type': kind, 'getter': BASE+fn, 'pointer': pointer,
                'text': text.decode('ascii'), 'complete8MiB_and_callee_saved_ABI_pass': True})
    assert len(cases) == 20
    (ROOT/'NOMINAL_PROVIDER_RESEARCH_ONLY.bin').write_bytes(target)
    save(ROOT/'nominal_provider_research.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'source_research_ARM9_sha256': sha(source), 'target_research_ARM9_sha256': sha(target),
        'source_storage_proof_sha256': sha((PRIOR/'type_phrase_storage_research.json').read_bytes()),
        'patches': patches, 'native_getter_cases': cases,
        'all57_active_village_and_Deck_replacements_preserved': True,
        'source_defined_immutable_name_tables_and_retired_constants_only': True,
        'current_reference_leads_only_six_table_owners_and_two_qualified_instruction_pairs': True,
        'all_other_bytes_including_getter_instructions_RTTI_and_old_strategist_code_exact': True,
        'all_section_BSS_pool_cache_startup_arena_geometry_preserved': True,
        'research_only_full_virtual_consumer_and_display_crop_approval_pending': True,
        'no_registered_ROM_COMMON_or_production_formatting_approval': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('20 complete native getter/8MiB/ABI cases: six nominal English names,old types6-9 and57 earlier replacements preserved. Research only;display consumer approval pending.', flush=True)


if __name__ == '__main__':
    main()
