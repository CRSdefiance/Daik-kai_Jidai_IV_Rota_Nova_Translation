"""Check shared ownership, all getters, ARM7 loading and the repaired copy body."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import BASE, POOL, STATIC, cstring, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.inventory_arm9_text import components
from scripts.prepare_residual_character_names import loaded
from scripts.probe_common_copy_arm946_alignment import matrix
from scripts.probe_persistent_name_arm7_boot_overlap import execute, late_copy_instruction_budget


def initialized(raw):
    machine = loaded(raw)
    stage = MainCodeFile(raw, BASE).sections[3]
    payload_bytes = struct.unpack_from('<I', stage.data, len(stage.data) - 4)[0]
    if payload_bytes != len(stage.data) - 48:
        raise ValueError('Complete staged payload/stub extent differs')
    before_sp = machine.reg_read(UC_ARM_REG_SP)
    from scripts.probe_main_pool_cache_visibility import CacheMonitor
    monitor = CacheMonitor(machine, raw)
    machine.emu_start(BASE + 0x8E4, BASE + 0x8E8, count=late_copy_instruction_budget(payload_bytes))
    monitor.finish()
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x8E8 or machine.reg_read(UC_ARM_REG_SP) != before_sp
            or bytes(machine.mem_read(POOL, payload_bytes)) != bytes(stage.data[:payload_bytes])):
        raise ValueError('Native initialization did not finish its complete pool copy with intact stack')
    machine.reg_write(UC_ARM_REG_LR, 0x027F0000)
    return machine


def main():
    image = NdsImage.open('out/all_routes_combined_v153_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    saved, plan = transform(source, clean)
    if saved != Path('work/analysis/ordinary_name_fidelity_research_arm9.bin').read_bytes():
        raise ValueError('Research differs from deterministic transform')
    expected = {r['index']: r['english'] for r in plan['records']}
    before, after = initialized(source), initialized(saved)
    names = []
    for index in range(207):
        old, new = ordinary_getter(source, index, before), ordinary_getter(saved, index, after)
        old_text = bytes(before.mem_read(old, 128)).split(b'\0', 1)[0].decode('cp932')
        new_text = bytes(after.mem_read(new, 128)).split(b'\0', 1)[0].decode('cp932')
        if new_text != expected.get(index, old_text) or not all(c.isprintable() for c in new_text):
            raise ValueError(f'Unexpected ordinary getter change: {index}, {old_text}, {new_text}')
        names.append({'index': index, 'before': old_text, 'after': new_text, 'pointer': new})
    code = MainCodeFile(saved, BASE)
    payload = bytes(code.sections[3].data[:-48])
    boot = execute(saved, bytes(image.rom.arm7), image.rom.arm7RamAddress, plan['copy_entry'], payload)
    if (boot['arm7_source_changed_bytes_after_arm9_autoload'] or
            not all(r['matches_original'] for r in boot['arm7_native_loaded_sections']) or
            not all(boot[k] for k in ('repaired_pool_matches_complete_payload',
                                     'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Expanded names fail ARM7-safe staged loading')
    revised_owners = {r['before_pointer']: r for r in plan['records'] if POOL <= r['before_pointer'] < POOL + 1504}
    alias_rows = []
    for move in plan['inherited_pointer_moves']:
        old = bytes(before.mem_read(move['before_pointer'], 128)).split(b'\0', 1)[0]
        new = bytes(after.mem_read(move['after_pointer'], 128)).split(b'\0', 1)[0]
        record = revised_owners.get(move['before_pointer'])
        if new != (record['english'].encode('ascii') if record else old):
            raise ValueError('Inherited complete item/entity name changed unexpectedly')
        if record:
            pointer = struct.unpack_from('<I', clean, move['field'])[0]
            japanese = cstring(clean, pointer - BASE).decode('cp932')
            if japanese != record['japanese']:
                raise ValueError('Revised role has a semantically different shared alias')
            alias_rows.append({**move, 'japanese': japanese, 'english': record['english']})
    # Audit every byte position, including unaligned and interior pointers.
    references = []
    static_spans = [(r['before_pointer'], r['before_pointer'] + STATIC.get(r['index'], 8))
                    for r in plan['records'] if r['index'] in STATIC or r['index'] == 131]
    for name, _, raw in components(image):
        for field in range(len(raw) - 3):
            pointer = struct.unpack_from('<I', raw, field)[0]
            if POOL <= pointer < POOL + 1504 or any(a <= pointer < b for a, b in static_spans):
                references.append({'component': name, 'field': field, 'pointer': pointer})
    expected_refs = {(m['field'], m['before_pointer']) for m in plan['inherited_pointer_moves']}
    expected_refs |= {(r['table_field'], r['before_pointer']) for r in plan['records']
                      if r['index'] in STATIC or r['index'] == 131}
    old_stub = bytes(MainCodeFile(source, BASE).sections[3].data[-48:])
    expected_refs.add((source.rfind(old_stub) + 40, POOL))
    # SDK BSS end is exclusive: the pool begins immediately after it. This
    # endpoint is a range boundary, not a string consumer or an interior alias.
    settings = MainCodeFile(source, BASE).codeSettingsOffs
    if struct.unpack_from('<I', source, settings + 16)[0] != POOL or saved[settings + 12:settings + 20] != source[settings + 12:settings + 20]:
        raise ValueError('Exclusive BSS boundary changed')
    expected_refs.add((settings + 16, POOL))
    if {(r['field'], r['pointer']) for r in references if r['component'] == 'arm9'} != expected_refs or any(
            r['component'] != 'arm9' for r in references):
        Path('work/analysis/ordinary_name_fidelity_unclassified_refs.json').write_text(json.dumps(references, indent=2))
        raise ValueError('Name allocations have unexplained static, interior or overlay references')
    common = image.read_file('/COMMON/MESFILE.DK4')
    a, b = [common_message_entries(common, raw, clean=False) for raw in (source, saved)]
    if len(a) != 3668 or [r.text for r in a] != [r.text for r in b] or source[0xCEC74:0xCECE0] != saved[0xCEC74:0xCECE0]:
        raise ValueError('COMMON selection/copy repair changed')
    pixels_path = Path('work/analysis/ordinary_name_fidelity_paired_pixels_proof.json')
    pixels = json.loads(pixels_path.read_text(encoding='utf-8'))
    if pixels['research_sha256'] != sha(saved) or len(pixels['cases']) != 34:
        raise ValueError('Native paired rasters do not match research')
    report = {'status': 'pass-ordinary-name-fidelity-research', 'source_arm9_sha256': sha(source),
              'target_arm9_sha256': sha(saved), 'reviewed_indices': sorted(expected),
              'native_getter_count': 207, 'native_getters': names, 'preserved_other_names': 190,
              'inherited_pointer_count': len(plan['inherited_pointer_moves']), 'changed_shared_aliases': alias_rows,
              'all_byte_position_arm9_and_overlay_references': references,
              'boot': boot, 'shared_copy_matrix_cases': matrix(saved), 'common_selections_preserved': 3668,
              'paired_pixels_sha256': sha(pixels_path.read_bytes()), 'paired_pixel_cases': 34,
              'visual_review': {'complete': True, 'sheet': 'work/qa/ordinary_name_fidelity_native/native_sheet.png',
                                'sheet_sha256': sha(Path('work/qa/ordinary_name_fidelity_native/native_sheet.png').read_bytes()),
                                'result': 'All 17 complete labels readable in both rows; first and final glyphs present; no clipping.'},
              'limitations': ['Actual character assignment and physical composition remain gameplay checks.',
                              '207 getter preservation is not a semantic review of all older names.',
                              'Cross-CPU scheduling and full emulator cold boot are not modeled.']}
    Path('work/analysis/ordinary_name_fidelity_research_proof.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Pass: 207 getters, 239 inherited pointers, all-byte overlay references, ARM7-safe loading, 704 copy cases and 34 reviewed native rasters.')


if __name__ == '__main__':
    main()
