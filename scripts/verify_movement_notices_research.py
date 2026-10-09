"""Verify movement prose, its actual callers, pixels and inherited native state."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.movement_notice_release import SHORTAGES
from dk4tool.patch.ordinary_name_fidelity_release import BASE
from dk4tool.patch.village_promised_words_release import PREFIX, SUFFIX
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, common_message_entries
from scripts import probe_remaining_common_layout as loader
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import STACK
from scripts.execute_scene_caption_raster import execute as raster
from scripts.probe_common_copy_arm946_alignment import arm946_machine, matrix
from scripts.probe_common_itcm_arena_reservation import initialize as arenas
from scripts.probe_common_itcm_arena_reservation import verify as arena_bounds
from scripts.probe_common_monthly_tribute_preparation import execute as monthly
from scripts.probe_common_tribute_modal_pixels import verify as modal_pixels
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.probe_movement_notice_callers import caller
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.verify_ordinary_name_fidelity_research import initialized
from scripts.verify_village_promised_words_research import caller as village_caller


def geometry(source):
    machine = initialized(source)
    parent = 0x02460000
    machine.reg_write(UC_ARM_REG_R4, parent)
    machine.emu_start(BASE + 0x687B0, BASE + 0x687D8, count=1000)
    values = [machine.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
    args = list(struct.unpack('<4I', machine.mem_read(STACK, 16)))
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0x687D8
            or values != [parent + 0x30, 0x022909BC, 0, 0] or args != [256, 32, 0, 0]):
        raise ValueError('Actual sailing bitmap constructor geometry differs')
    return {'actual_constructor_arguments': args, 'source_asset_pointer': values[1],
            'parent_bitmap_offset': 0x30, 'status_cell_origins': [[60, 12], [120, 12]],
            'cell_width': 60, 'full_parent_composition_is_contract': True}


def unavailable(source):
    machine = initialized(source)
    buffers = [struct.unpack_from('<I', source, at)[0] for at in (0x54890, 0x54894)]
    for buffer in buffers:
        machine.mem_write(buffer - 32, b'\xa5' * 320)
    trace = set()
    machine.hook_add(UC_HOOK_CODE, lambda uc, address, size, data: trace.add(address))
    machine.emu_start(BASE + 0x995C8, BASE + 0x5479C, count=100000)
    wanted = b'Automatic travel is unavailable.'
    if not {BASE + 0x5473C, BASE + 0x54774, BASE + 0xCE898, BASE + 0x53914} <= trace:
        raise ValueError('Unavailable modal bypasses its native caller or formatter')
    for buffer in buffers:
        if bytes(machine.mem_read(buffer - 32, 320)) != b'\xa5' * 32 + wanted + b'\0' + b'\xa5' * (287 - len(wanted)):
            raise ValueError('Unavailable modal changes complete text or buffer guards')
    return {'text': wanted.decode('ascii'), 'native_caller_sprintf_and_macro_pass_execute': True,
            'formatted_and_expanded_buffer_canaries_intact': True,
            'native_endpoint': BASE + 0x5479C, 'window_construction_and_input_pending': True}


def scope_case(source, paragraph, parent, table):
    machine = initialized(source)
    template, args, first, second = 0x02423000, 0x02424000, 0x02425000, 0x02426000
    machine.mem_write(template, paragraph.encode('ascii') + b'\0')
    machine.mem_write(first, b'water and food\0')
    machine.mem_write(second, b'automatic travel\0')
    machine.mem_write(args, struct.pack('<2I', first, second))
    machine.mem_write(STACK + 0x264, struct.pack('<I', parent))
    machine.mem_write(STACK + 0x274, bytes(4))
    machine.mem_write(STACK + 0x27C, struct.pack('<I', table))
    for reg, value in ((UC_ARM_REG_R9, template), (UC_ARM_REG_R10, 0x02428000), (UC_ARM_REG_R11, args)):
        machine.reg_write(reg, value)
    buffers = [struct.unpack_from('<I', source, at)[0] for at in (0x5444C, 0x54450)]
    for buffer in buffers:
        machine.mem_write(buffer - 32, b'\xa5' * 320)
    trace = set()
    machine.hook_add(UC_HOOK_CODE, lambda uc, address, size, data: trace.add(address))
    machine.emu_start(BASE + 0x54144, BASE + 0x54164, count=100000)
    expected = paragraph.replace('%s', 'water and food', 1).replace('%s', 'automatic travel', 1).encode('ascii')
    for buffer in buffers:
        if bytes(machine.mem_read(buffer - 32, 320)) != b'\xa5' * 32 + expected + b'\0' + b'\xa5' * (287 - len(expected)):
            raise ValueError('Unrelated portrait path changes complete text or guards')
    if machine.reg_read(UC_ARM_REG_SP) != STACK or BASE + 0x53914 not in trace or 0x01FF9BC8 in trace:
        raise ValueError('Movement scope intercepts an unrelated native macro path')
    return {'paragraph': paragraph, 'parent_return': parent, 'actor_table': table,
            'native_macro_fallback_preserved': True, 'full_buffer_guards_and_stack_preserved': True}


def panel(native):
    result = Image.new('RGB', (256, 192))
    result.putdata([(255, 255, 255) if c == 9 else (128, 128, 128) if c == 14 else (0, 0, 0)
                    for c in struct.unpack('<49152H', native['pixels'])])
    return result.crop((0, 0, 256, 96)).resize((1024, 192), Image.Resampling.NEAREST)


def whole_words(native, text):
    events = [e for e in native['glyph_events'] if e['code'] != 32]
    cursor = 0
    for word in text.split():
        if len({e['y'] for e in events[cursor:cursor + len(word)]}) != 1:
            raise ValueError('Movement native layout splits a word')
        cursor += len(word)


def main():
    image = NdsImage.open('out/all_routes_combined_v155_candidate.nds')
    original, old_common = image.read_file('/__arm9__.bin'), image.read_file('/COMMON/MESFILE.DK4')
    source = Path('work/analysis/movement_notices_research_arm9.bin').read_bytes()
    common = Path('work/analysis/movement_notices_research_common.bin').read_bytes()
    plan = json.loads(Path('work/analysis/movement_notices_plan.json').read_text(encoding='utf-8'))
    if (sha(original) != plan['source_arm9_sha256'] or sha(old_common) != plan['source_common_sha256']
            or sha(source) != plan['target_arm9_sha256'] or sha(common) != plan['target_common_sha256']):
        raise ValueError('Movement prepared identities differ')
    calls = [caller(source, common, i, supply_selector=supply)
             for supply in (None, 0, 1) for i in range(8)]
    failure = unavailable(source)
    scopes = []
    for parent, table in ((BASE + 0x53F40, BASE + 0x1189C0), (BASE + 0x53EAC, 0),
                          (BASE + 0x53F40, BASE + 0x1189C4)):
        for amount in (0, 999999, 42949672):
            wrapped = parent == BASE + 0x53F40 and table == BASE + 0x1189C0
            kwargs = {'word_wrapped': wrapped, 'parent_return': parent, 'selector_table': table}
            if monthly(original, 'Payment: %s gold coins.', amount, 0x02428000, **kwargs) != monthly(
                    source, 'Payment: %s gold coins.', amount, 0x02428000, **kwargs):
                raise ValueError('Movement wrapper changes monthly or unrelated path')
            scopes.append({'parent_return': parent, 'selector_table': table, 'amount': amount, 'exact_output_preserved': True})
    rejected = []
    exact = SHORTAGES[610][0]
    for value, parent, table in ((exact, BASE + 0x53EAC, BASE + 0x118580),
                                (exact, BASE + 0x53DB8, BASE + 0x118584),
                                (exact + 'x', BASE + 0x53DB8, BASE + 0x118580),
                                ('Other %s: %s.', BASE + 0x53DB8, BASE + 0x118580)):
        old = scope_case(original, value, parent, table)
        new = scope_case(source, value, parent, table)
        if old != new:
            raise ValueError('Movement complete-template scope fallback differs')
        rejected.append(new)
    village_plan = json.loads(Path('work/analysis/village_promised_words_plan.json').read_text(encoding='utf-8'))
    village = []
    messages = {r['index']: r for r in village_plan['records'] if r['kind'] == 'MESSAGE'}
    for captain in (4, 19):
        for index, start in ((0, 0x78ADC), (2, 0x78BA0), (3, 0x78BB0)):
            village.append(village_caller(source, start, 0, captain, bytes.fromhex(messages[index]['compiled_hex']).decode('ascii')))
        for row in village_plan['records']:
            if row['kind'] == 'CLUE':
                clue = bytes.fromhex(row['compiled_hex']).decode('ascii')
                village.append(village_caller(source, 0x78B8C, row['index'], captain, PREFIX + clue + SUFFIX, clue=clue))
    font = image.read_file('/GRP/KANJI.FNT')
    unique = list(dict.fromkeys(c['complete_prepared_text'] for c in calls)) + [failure['text']]
    destination = Path('work/qa/movement_notices_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1044, (len(unique) + 1) * 220), 'white')
    draw = ImageDraw.Draw(sheet)
    panels = []
    for index, value in enumerate(unique):
        for mode in (4, 16):
            native = modal_pixels(source, font, value, mode, guarded=True, portrait=index < len(unique) - 1)
            whole_words(native, value)
            panels.append({'index': index, 'mode': mode, 'text': value, 'pixels_sha256': sha(native['pixels']),
                           'complete_glyphs_bounds_independent_pixels_and_whole_words': True})
            if mode == 16:
                preview = panel(native)
                preview.save(destination / f'panel_{index:02d}.png')
                draw.text((10, index * 220 + 2), str(index), fill='black')
                sheet.paste(preview, (10, index * 220 + 20))
    for mode in (4, 16):
        native = raster(source, 'Auto Sail', sailing_status=True, surface_size=(256, 32), kanji_font=font, mode=mode)
        if native['pixels'] != expected_pixels(source, font, native['glyph_events'], mode, background=9):
            raise ValueError('Sailing status native pixels differ from independent decoding')
        if [e['code'] for e in native['glyph_events']] != list(b'Auto SailFast Sail'):
            raise ValueError('Sailing status drops a leading, interior or final glyph')
        # Native six-column ASCII glyphs have a blank last column. With tracking
        # -1 each complete label has nine five-pixel advances, leaving a gap.
        for number in range(2):
            events = native['glyph_events'][number * 9:(number + 1) * 9]
            if [e['x'] for e in events] != list(range(60 + number * 60, 105 + number * 60, 5)) or any(e['y'] != 12 for e in events):
                raise ValueError('Sailing status does not preserve both actual cell origins')
        panels.append({'index': len(unique), 'mode': mode, 'text': 'Auto Sail | Fast Sail',
                       'actual_draws': native['sailing_status_draws'], 'pixels_sha256': sha(native['pixels']),
                       'complete_glyphs_bounds_independent_pixels_and_whole_words': True})
        if mode == 16:
            preview = panel(native)
            preview.save(destination / f'panel_{len(unique):02d}.png')
            draw.text((10, len(unique) * 220 + 2), 'Both sailing status cells', fill='black')
            sheet.paste(preview, (10, len(unique) * 220 + 20))
    sheet.save(destination / 'native_sheet.png')
    before, after = initialized(original), initialized(source)
    names = []
    for index in range(207):
        old, new = ordinary_getter(original, index, before), ordinary_getter(source, index, after)
        if old != new or bytes(before.mem_read(old, 128)).split(b'\0', 1)[0] != bytes(after.mem_read(new, 128)).split(b'\0', 1)[0]:
            raise ValueError('Movement layer changes inherited ordinary name')
        names.append({'index': index, 'pointer': new, 'complete_string_preserved': True})
    inherited = json.loads(Path('work/analysis/ordinary_name_fidelity_plan.json').read_text(encoding='utf-8'))
    owners = []
    for move in inherited['inherited_pointer_moves']:
        field = move['field']
        old, new = [struct.unpack_from('<I', raw, field)[0] for raw in (original, source)]
        if old != new or bytes(before.mem_read(old, 128)).split(b'\0', 1)[0] != bytes(after.mem_read(new, 128)).split(b'\0', 1)[0]:
            raise ValueError('Movement layer changes inherited shared name/item owner')
        owners.append({'field': field, 'pointer': new, 'complete_string_preserved': True})
    old_entries, new_entries = common_message_entries(old_common, original, clean=False), common_message_entries(common, source, clean=False)
    old_blocks, new_blocks = IlnkContainer.parse(old_common).blocks, IlnkContainer.parse(common).blocks
    if (original[DIRECTORY_OFFSET:DIRECTORY_OFFSET + 41 * 4] != source[DIRECTORY_OFFSET:DIRECTORY_OFFSET + 41 * 4]
            or [len(b) for b in old_blocks] != [len(b) for b in new_blocks]
            or [b.count(b'\0') for b in old_blocks] != [b.count(b'\0') for b in new_blocks]):
        raise ValueError('Movement COMMON directory/block/NUL allocations differ')
    for old, new in zip(old_entries, new_entries, strict=True):
        expected = SHORTAGES[new.message_id][0].encode('ascii') if new.message_id in SHORTAGES else old.text
        if new.text != expected or (old.message_id, old.block, old.record_index) != (new.message_id, new.block, new.record_index):
            raise ValueError('Movement layer changes other COMMON selections or loses complete prose')
    copy_cases = []
    factory = loader.machine_for
    loader.machine_for = arm946_machine
    try:
        for entry in new_entries:
            if entry.block == 7:
                for cold in (False, True):
                    copy_cases.append(loader.warm_copy(source, common, entry.message_id, entry.text, cold_cache=cold))
    finally:
        loader.machine_for = factory
    initial, old_initial = arenas(source), arenas(original)
    if (initial['low'][0] != plan['final_pool_span'][1] or initial['low'][3] != plan['reserved_arena_low']
            or initial['high'] != old_initial['high']
            or any(initial['low'][i] != old_initial['low'][i] for i in range(9) if i not in (0, 3))):
        raise ValueError('Movement native arena ownership changes unrelated state')
    code = MainCodeFile(source, BASE)
    boot_result = boot(source, bytes(image.rom.arm7), image.rom.arm7RamAddress,
                       plan['copy_entry'], bytes(code.sections[3].data[:-48]))
    if (boot_result['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(r['matches_original'] for r in boot_result['arm7_native_loaded_sections'])
            or not all(boot_result[k] for k in ('repaired_pool_matches_complete_payload',
                                               'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Movement native boot changes ARM7 or persistent pool')
    proof = {'status': 'pass-native-movement-callers-prose-pixels-preservation-and-safe-boot',
             'source_arm9_sha256': sha(original), 'target_arm9_sha256': sha(source),
             'source_common_sha256': sha(old_common), 'target_common_sha256': sha(common),
             'native_preparation_cases': calls, 'unavailable_modal_caller': failure,
             'inherited_monthly_scope_cases': scopes, 'complete_template_rejection_cases': rejected,
             'inherited_village_callers': village, 'paired_pixel_cases': panels,
             'sailing_bitmap_geometry': geometry(source), 'inherited_names': names,
             'inherited_shared_owners': owners, 'common_selected_entries_verified': len(new_entries),
             'common_changed_ids': list(SHORTAGES), 'common_directory_block_sizes_and_nul_counts_preserved': True,
             'native_block7_warm_cold_arm946_copies': copy_cases, 'shared_copy_alignment_cases': matrix(source),
             'native_initial_arenas': initial, 'resident_arena_bounds': arena_bounds(source, plan['reserved_arena_low']),
             'boot': boot_result, 'visual_review': {'complete': False}, 'physical_gameplay_verified': False,
             'limitations': ['Crew-list contents and actor-source variant are explicit fixtures.',
                             'Intervening portrait widgets and full parent bitmap composition remain contracts.',
                             'Cold filesystem reads and ARM946 alignment model are bounded contracts; physical cold boot remains pending.']}
    Path('work/analysis/movement_notices_native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(calls)} movement callers; {len(village)} inherited village callers; {len(panels)} native pixel cases; {len(copy_cases)} native block7 warm/cold copies; safe boot pass. Visual review pending.')


if __name__ == '__main__':
    main()
