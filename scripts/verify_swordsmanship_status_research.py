"""Prove actual duel-stat bitmap, numeric bounds, callers and complete pixels."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ordinary_name_fidelity_release import BASE, cstring
from dk4tool.patch.swordsmanship_status_release import BITMAP_WIDTH, formatted
from dk4tool.patch.village_promised_words_release import PREFIX, SUFFIX
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import STACK
from scripts.execute_scene_caption_raster import execute as raster
from scripts.probe_common_copy_arm946_alignment import matrix
from scripts.probe_common_itcm_arena_reservation import initialize as arenas
from scripts.probe_common_itcm_arena_reservation import verify as arena_bounds
from scripts.probe_common_monthly_tribute_preparation import execute as monthly
from scripts.probe_duel_parent_composition import composition
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.probe_movement_notice_callers import caller as movement_caller
from scripts.probe_persistent_name_arm7_boot_overlap import execute as boot
from scripts.verify_ordinary_name_fidelity_research import initialized
from scripts.verify_village_promised_words_research import caller as village_caller


def geometry(source, index):
    machine = initialized(source)
    owner = 0x02460000
    machine.reg_write(UC_ARM_REG_R0, owner)
    machine.reg_write(UC_ARM_REG_R1, index)
    machine.emu_start(BASE + 0xE368, BASE + 0xE3A8, count=1000)
    sp = machine.reg_read(UC_ARM_REG_SP)
    args = list(struct.unpack('<4I', machine.mem_read(sp, 16)))
    # R2=0 and R3=24+index*12 select the backing image origin, not screen position.
    regs = [machine.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
    if (machine.reg_read(UC_ARM_REG_PC) != BASE + 0xE3A8 or sp != STACK - 32
            or args != [BITMAP_WIDTH, 12, 0, 0] or regs != [owner + 0x14, struct.unpack_from('<I', source, 0xE400)[0], 0, 24 + 12 * index]):
        raise ValueError('Actual duel text bitmap constructor geometry differs')
    return {'index': index, 'actual_constructor_stack_arguments': args, 'owner_bitmap_offset': 0x14,
            'source_asset_pointer': regs[1], 'backing_image_origin': regs[2:], 'actual_slot_constructor_executed': True}


def compose(native, slot, mode):
    """CPU preview from native crops; GPU submission itself remains a contract."""
    requests = slot['draw_requests']
    for glyph in native['glyph_events']:
        if glyph['code'] == 32:
            continue
        owners = [r for r in requests if r['source_origin'][0] <= glyph['x']
                  and glyph['x'] + 6 <= r['source_origin'][0] + r['size'][0]]
        if len(owners) != 1:
            raise ValueError('Parent crops split or drop a complete non-space glyph')
    if mode == 16:
        colors = list(struct.unpack('<49152H', native['pixels']))
    else:
        colors = [v for byte in native['pixels'] for v in (byte & 15, byte >> 4)]
    preview = Image.new('RGB', (256, 192))
    preview.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                     for c in colors])
    rectangle = slot['parent_rectangle']
    screen = Image.new('RGB', (256, 192), '#dedede')
    draw = ImageDraw.Draw(screen)
    draw.rectangle((rectangle[0], rectangle[1], rectangle[2] - 1, rectangle[3] - 1), fill='white', outline='black')
    for request in requests:
        x = request['source_origin'][0]
        w, h = request['size']
        # Pillow extends a mutable two-element box into four coordinates.
        # Keep the captured native argument record immutable during preview.
        screen.paste(preview.crop((x, 0, x + w, h)), tuple(request['destination_origin']))
    return screen


def clamp(source):
    result = []
    for value in (-2147483648, -1, 0, 1, 499, 500, 501, 65535, 2147483647):
        machine = initialized(source)
        machine.reg_write(UC_ARM_REG_R4, value & 0xFFFFFFFF)
        machine.emu_start(BASE + 0x7DDFC, BASE + 0x7DE10, count=100)
        expected = min(500, max(0, value))
        if machine.reg_read(UC_ARM_REG_R4) != expected or machine.reg_read(UC_ARM_REG_PC) != BASE + 0x7DE10:
            raise ValueError('Native effective skill clamp differs')
        result.append({'unclamped_signed_skill': value, 'native_clamped_skill': expected})
    return result


def main():
    image = NdsImage.open('out/all_routes_combined_v156_candidate.nds')
    original = image.read_file('/__arm9__.bin')
    source = Path('work/analysis/swordsmanship_status_research_arm9.bin').read_bytes()
    plan = json.loads(Path('work/analysis/swordsmanship_status_plan.json').read_text(encoding='utf-8'))
    if sha(original) != plan['source_arm9_sha256'] or sha(source) != plan['target_arm9_sha256']:
        raise ValueError('Swordsmanship research identities differ')
    font = image.read_file('/GRP/KANJI.FNT')
    parent_composition = composition(source)
    table = struct.unpack_from('<I', source, 0x7E0F0)[0]
    states = []
    for state in (*range(7), 255):
        pointer = struct.unpack_from('<I', source, table - BASE + state * 4)[0] if state < 7 else struct.unpack_from('<I', source, 0x7E0F4)[0]
        states.append((state, cstring(source, pointer - BASE).decode('ascii')))
    unique = [(skill, hp, state, formatted(skill, hp, suffix))
              for skill, hp in ((0, 0), (500, 65535)) for state, suffix in states]
    destination = Path('work/qa/swordsmanship_status_native')
    destination.mkdir(parents=True, exist_ok=True)
    sheet = Image.new('RGB', (1256, len(unique) * 80), 'white')
    draw = ImageDraw.Draw(sheet)
    parent_sheet = Image.new('RGB', (1032, len(unique) * 190), 'white')
    parent_draw = ImageDraw.Draw(parent_sheet)
    cases = []
    for number, (skill, hp, state, value) in enumerate(unique):
        combined = Image.new('RGB', (256, 40), '#dedede')
        for index in (0, 1):
            for mode in (4, 16):
                native = raster(source, value, sword_stats=(skill, hp, state), duel_actor_index=index,
                                surface_size=(BITMAP_WIDTH, 12), kanji_font=font, mode=mode)
                if ([e['code'] for e in native['glyph_events']] != list(value.encode('ascii'))
                        or any(e['x'] < 0 or e['x'] + 6 > BITMAP_WIDTH or e['y'] != 0 for e in native['glyph_events'])
                        or native['pixels'] != expected_pixels(source, font, native['glyph_events'], mode, background=0)):
                    raise ValueError('Duel stats loses glyphs or clips/splits complete numeric/state text')
                cases.append({'duel_actor_index': index, 'mode': mode, 'effective_skill': skill,
                              'hp': hp, 'state': state, 'complete_formatted_text': value,
                              'pixels_sha256': sha(native['pixels']), 'complete_glyphs_bounds_and_independent_pixels': True,
                              'native_owner_slot_caller_hp_state_getters_sprintf_and_renderer_execute': True,
                              'native_stack_and_callee_saved_registers_preserved': native['stack_and_registers_preserved'],
                              'effective_skill_provider_and_bitmap_clear_are_contracts': True})
                composed = compose(native, parent_composition['actor_slots'][index], mode)
                cases[-1]['complete_non_space_glyphs_fit_native_parent_crops'] = True
                cases[-1]['composed_preview_sha256'] = sha(composed.tobytes())
                if mode == 16:
                    rect = parent_composition['actor_slots'][index]['parent_rectangle']
                    combined.paste(composed.crop(tuple(rect)), (rect[0], 0))
                if index == 0 and mode == 16:
                    preview = Image.new('RGB', (256, 192))
                    preview.putdata([(255, 255, 255) if c == 0 else (128, 128, 128) if c == 14 else (0, 0, 0)
                                     for c in struct.unpack('<49152H', native['pixels'])])
                    preview = preview.crop((0, 0, BITMAP_WIDTH, 12)).resize((BITMAP_WIDTH * 8, 48), Image.Resampling.NEAREST)
                    preview.save(destination / f'panel_{number:02d}.png')
                    draw.text((4, number * 80 + 2), f'{number}: skill {skill}, HP {hp}, state {state}', fill='black')
                    sheet.paste(preview, (4, number * 80 + 22))
        composed = combined.resize((1024, 160), Image.Resampling.NEAREST)
        composed.save(destination / f'parent_panel_{number:02d}.png')
        parent_draw.text((4, number * 190 + 2), f'{number}: both actors; skill {skill}, HP {hp}, state {state}', fill='black')
        parent_sheet.paste(composed, (4, number * 190 + 22))
    sheet.save(destination / 'native_sheet.png')
    parent_sheet.save(destination / 'parent_sheet.png')
    common = image.read_file('/COMMON/MESFILE.DK4')
    if common_message_entries(common, original, clean=False) != common_message_entries(common, source, clean=False):
        raise ValueError('Stats research changes inherited COMMON selectors or text')
    movement = [movement_caller(source, common, variant, supply_selector=supply)
                for supply in (None, 0, 1) for variant in range(8)]
    monthly_cases = []
    for parent, selector in ((BASE + 0x53F40, BASE + 0x1189C0), (BASE + 0x53EAC, 0),
                             (BASE + 0x53F40, BASE + 0x1189C4)):
        for amount in (0, 999999, 42949672):
            kwargs = {'word_wrapped': parent == BASE + 0x53F40 and selector == BASE + 0x1189C0,
                      'parent_return': parent, 'selector_table': selector}
            if monthly(original, 'Payment: %s gold coins.', amount, 0x02428000, **kwargs) != monthly(
                    source, 'Payment: %s gold coins.', amount, 0x02428000, **kwargs):
                raise ValueError('Duel extension changes monthly scope or complete text')
            monthly_cases.append({'parent_return': parent, 'selector_table': selector, 'amount': amount,
                                  'exact_output_preserved': True})
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
    old_machine, new_machine = initialized(original), initialized(source)
    names = []
    for index in range(207):
        old, new = ordinary_getter(original, index, old_machine), ordinary_getter(source, index, new_machine)
        if old != new or bytes(old_machine.mem_read(old, 128)).split(b'\0', 1)[0] != bytes(new_machine.mem_read(new, 128)).split(b'\0', 1)[0]:
            raise ValueError('Stats extension changes complete ordinary name')
        names.append({'index': index, 'pointer': new, 'complete_string_preserved': True})
    name_plan = json.loads(Path('work/analysis/ordinary_name_fidelity_plan.json').read_text(encoding='utf-8'))
    owners = []
    for row in name_plan['inherited_pointer_moves']:
        field = row['field']
        old, new = [struct.unpack_from('<I', raw, field)[0] for raw in (original, source)]
        if old != new or bytes(old_machine.mem_read(old, 128)).split(b'\0', 1)[0] != bytes(new_machine.mem_read(new, 128)).split(b'\0', 1)[0]:
            raise ValueError('Stats extension changes complete shared item/name owner')
        owners.append({'field': field, 'pointer': new, 'complete_string_preserved': True})
    inherited_status = []
    for mode in (4, 16):
        kwargs = {'sailing_status': True, 'surface_size': (256, 32), 'kanji_font': font, 'mode': mode}
        old, new = [raster(raw, 'Auto Sail', **kwargs) for raw in (original, source)]
        for key in ('pixels', 'glyph_events', 'sailing_status_draws'):
            if old[key] != new[key]:
                raise ValueError('Stats extension changes inherited sailing status output')
        inherited_status.append({'mode': mode, 'complete_status_pixels_and_arguments_preserved': True})
    code = MainCodeFile(source, BASE)
    initial = arenas(source)
    before = arenas(original)
    if (initial['low'][0] != plan['final_pool_span'][1] or initial['low'][3] != plan['reserved_arena_low']
            or initial['high'] != before['high']
            or any(initial['low'][i] != before['low'][i] for i in range(9) if i not in (0, 3))):
        raise ValueError('Stats native arena reservations differ')
    result = boot(source, bytes(image.rom.arm7), image.rom.arm7RamAddress,
                  plan['copy_entry'], bytes(code.sections[3].data[:-48]))
    if (result['arm7_source_changed_bytes_after_arm9_autoload']
            or not all(row['matches_original'] for row in result['arm7_native_loaded_sections'])
            or not all(result[k] for k in ('repaired_pool_matches_complete_payload',
                                          'repair_returns_with_stack_preserved', 'actual_startup_call_preserves_r0_r3'))):
        raise ValueError('Stats native staging or ARM7 ownership differs')
    proof = {'status': 'research-native-duel-caller-geometry-bounds-and-pixels-pass',
             'source_arm9_sha256': sha(original), 'target_arm9_sha256': sha(source),
             'geometry': [geometry(source, i) for i in (0, 1)], 'effective_skill_clamp': clamp(source),
             'actual_hp_unsigned_halfword_getter': BASE + 0x7E19C, 'native_pixel_cases': cases,
             'native_parent_composition': parent_composition, 'inherited_monthly_scope_cases': monthly_cases,
             'inherited_movement_callers': movement, 'inherited_village_callers': village,
             'inherited_sailing_status_pixels': inherited_status,
             'inherited_names': names, 'inherited_shared_owners': owners,
             'common_selected_entries_preserved': 3668, 'shared_copy_alignment_cases': matrix(source),
             'boot': result, 'native_initial_arenas': initial,
             'resident_arena_bounds': arena_bounds(source, plan['reserved_arena_low']),
             'visual_review': {'complete': False}, 'physical_gameplay_verified': False,
             'limitations': ['Complete effective-skill provider, equipment/crew state are fixtures; native final skill clamp executes separately.',
                             'HP and health-state getters, both indexed owner callers and renderer execute natively.',
                             'Whole bitmap clearing, widget registration, frame/border/secondary art and final GPU submission are contracts.',
                             'Source asset initialization, both indexed slot rectangles/constructors and primary crop dispatch execute natively; previews compose captured crops on the CPU.',
                             'Release integration still pending.',
                             'Not registered or built as a playable ROM.']}
    Path('work/analysis/swordsmanship_status_native_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} native duel owner/caller/getter/formatter/pixel cases; both constructors; nine clamp boundaries; safe boot pass. Research only.')


if __name__ == '__main__':
    main()
