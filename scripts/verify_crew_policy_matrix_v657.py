"""Source-bound ordinary five-ship policy, plaque and complete text evidence."""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_dialogue_palette_v628 import captured_rgb, raster
from scripts.verify_full_fleet_battle_v652 import fleet_models
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_queued_portrait_wrap_v653 import view_replay
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/crew_policy_matrix_v657')
MODEL, PARENT = 0x0218A0E8, 0x0218A0D8
POLICIES = (
    ('Flagship', '旗艦重視', 0x02133A10, 0x206EC, 5500, [89, 9, 9, 9, 9]),
    ('Even', '平均化', 0x02133A00, 0x20674, 9100, [49, 19, 19, 19, 19]),
    ('Minimum', '必要最小', 0x02133A1C, 0x2062C, 7500, [39, 9, 9, 9, 9]),
)


def string(data, address):
    return data[address - BASE:address - BASE + 128].split(b'\0')[0]


def find_complete(font, text, image, region):
    """Search only the declared field; compare every ink and blank font cell."""
    for color, _ in Counter(image.crop(region).get_flattened_data()).most_common(8):
        for y in range(region[1], region[3] - 10):
            for x in range(region[0], region[2] - len(text) * 6 + 1):
                try:
                    ink, bounds = complete_mask(font, text, image, x, y, color)
                except ValueError:
                    continue
                return {'text': text, 'bounds': bounds, 'color': color,
                        'ink_pixels': ink, 'all_ink_and_blank_cells_exact': True}
    raise ValueError(f'No complete field: {text!r} in {region}')


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    folder = Path(pre['output'])
    rp = folder / 'capture_report.json'
    report = read(rp)
    assert report['frames'] == 17500 and report['ROM_sha256'] == pre['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    donor = report['battery_save_preloaded']
    assert donor['copied_byte_exact_before_cold_boot'] and donor['source_sha256'] == pre['donor_sha256']
    shots, raws = {}, {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        if row['frame'] in shots:
            assert Image.open(shots[row['frame']]['path']).tobytes() == Image.open(row['path']).tobytes()
        shots[row['frame']] = row
    for key in ('read_only_capture_RAM_snapshots', 'read_only_pause_RAM_snapshots'):
        for row in report[key]:
            assert row['read_only_export'] and sha(Path(row['path']).read_bytes()) == row['sha256']
            raws[row['frame']] = Path(row['path']).read_bytes()
    assert len(shots) == 40 and len(raws) == 37
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    font = GameAsciiFont.from_arm9(arm)
    assert font.glyphs == GameAsciiFont.from_arm9(original).glyphs
    spans = []
    for lo, hi in ((0x1DCB4, 0x1E304), (0x2062C, 0x20E18), (0xAB18C, 0xAB1FC)):
        assert arm[lo:hi] == original[lo:hi]
        spans.append({'start': BASE + lo, 'end': BASE + hi, 'sha256': sha(arm[lo:hi])})
    table = struct.unpack_from('<I', arm, 0x1E274)[0]
    assert table == struct.unpack_from('<I', original, 0x1E274)[0] == 0x02114EF8
    assert struct.unpack_from('<12I', arm, table - BASE) == (
        0x02133A10, 1, 1, 0, 0x02133A00, 1, 1, 0, 0x02133A1C, 1, 1, 0)
    base = raws[4300]
    assert struct.unpack_from('<I', base, PARENT - BASE)[0] == 0x02133D98
    assert struct.unpack_from('<I', base, MODEL - BASE)[0] == 5
    refs = [struct.unpack_from('<I', base, MODEL - BASE + 4 + i * 8)[0] for i in range(5)]
    assert refs == [s['model'] for s in fleet_models(arm, base, 1)]
    u = machine(arm)
    u.mem_write(BASE, base)
    limits = {}
    for label, fn in (('minimum', 0xAB1C4), ('maximum', 0xAB18C)):
        values = []
        for model in refs:
            call(u, fn, (model,))
            values.append(u.reg_read(UC_ARM_REG_R0))
        limits[label] = values
    assert limits == {'minimum': [39, 9, 9, 9, 9], 'maximum': [124, 24, 24, 24, 24]}
    policy_rows = []
    for name, japanese, address, fn, frame, counts in POLICIES:
        assert string(arm, address).decode('ascii') == name
        assert string(original, address).decode('cp932') == japanese
        u = machine(arm)
        u.mem_write(BASE, base)
        executed = call(u, fn, (MODEL,))
        result = bytes(u.mem_read(MODEL, 48))
        assert result == raws[frame][MODEL - BASE:MODEL - BASE + 48]
        assert [struct.unpack_from('<I', result, 8 + i * 8)[0] for i in range(5)] == counts
        assert struct.unpack_from('<I', result, 44)[0] == 125
        after = bytes(u.mem_read(BASE, len(base)))
        owned = {MODEL - BASE + 8 + i * 8 + b for i in range(5) for b in range(4)}
        changed = [i for i, (a, b) in enumerate(zip(base, after, strict=True)) if a != b]
        assert set(changed) <= owned
        call(u, 0x20D64, (MODEL,))
        assert u.reg_read(UC_ARM_REG_R0) == sum(counts)
        assert all(lo <= v <= hi for lo, v, hi in zip(limits['minimum'], counts, limits['maximum'], strict=True))
        policy_rows.append({'name': name, 'Japanese': japanese, 'menu_label': address,
            'native_allocator': BASE + fn, 'captured_frame': frame, 'counts': counts,
            'fleet_crew': sum(counts), 'total_available_sailors': 125,
            'unassigned': 125 - sum(counts), 'exact_48_byte_model_sha256': sha(result),
            'complete_original_allocator_and_saved_register_ABI_pass': True,
            'only_temporary_allocation_count_bytes_changed': [BASE + i for i in changed],
            'original_summation_getter_matches': True, 'executed_instruction_count': len(executed)})
    ui_frames = (4300, 5500, 7500, 9100, 9900, 10300, 10700, 11100, 11500,
                 12700, 13900, 15100, 16700)
    group = read('translations/source_plaque_grain_v1.json')['files'][0]
    art = PxlImage.from_bytes(rom.read_file(group['file_path']))
    assert len(group['records']) == 7
    plaque_rows, field_rows = [], []
    for frame in ui_frames:
        image = Image.open(shots[frame]['path']).convert('RGB')
        for record in group['records']:
            x0, y0, x1, y1 = record['plaque_box']
            assert all(native5(image.getpixel((x, y))) == native5(art.palette[art.indices[y * art.width + x]])
                       for y in range(y0, y1) for x in range(x0, x1))
            plaque_rows.append({'frame': frame, 'English': record['english'],
                'bounds': record['plaque_box'], 'complete_material_border_letter_pixels': (x1 - x0) * (y1 - y0)})
        counts = [struct.unpack_from('<I', raws[frame], MODEL - BASE + 8 + i * 8)[0] for i in range(5)]
        unassigned = 125 - sum(counts)
        fields = [find_complete(font, str(sum(counts)), image, (88, 18, 128, 36)),
                  find_complete(font, str(unassigned), image, (216, 18, 255, 36)),
                  find_complete(font, '46 days' if unassigned else '28 days', image, (90, 40, 175, 60))]
        for text in ('Need', 'Now', 'Max'):
            fields.append(find_complete(font, text, image, (100, 188, 255, 212)))
        for i, (need, now, maximum) in enumerate(zip(limits['minimum'], counts, limits['maximum'], strict=True)):
            for value, left, right in ((need, 136, 162), (now, 174, 198), (maximum, 208, 234)):
                fields.append(find_complete(font, str(value), image, (left, 206 + 32 * i, right, 227 + 32 * i)))
        field_rows.append({'frame': frame, 'all_complete_fields': fields, 'counts': counts,
                           'unassigned': unassigned, 'conserved_total': sum(counts) + unassigned})
    popup = Image.open(shots[4700]['path']).convert('RGB')
    popup_rows = [find_complete(font, name, popup, (94, 254 + 20 * i, 164, 279 + 20 * i))
                  for i, name in enumerate(('Flagship', 'Even', 'Minimum'))]
    pointer = struct.unpack_from('<I', arm, 0x54450)[0]
    kanji = rom.read_file('/GRP/KANJI.FNT')
    palette = struct.unpack_from('<16H', arm, 0x125A20)
    confirmation = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)[11]
    original_confirmation = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), original, clean=True)[11]
    assert confirmation.text.strip() == b'Does this work?'
    assert original_confirmation.text.decode('cp932') == 'これで、よろしいですか？'
    notices = []
    for frame, text, literal in ((5100, 'Assigned to flagship first.', 0x1E278),
                                 (7100, 'Minimum sailors assigned.', 0x1E280),
                                 (8700, 'Sailors assigned evenly.', 0x1E27C),
                                 (9500, ' Does this work?', None),
                                 (14300, ' Does this work?', None),
                                 (17100, ' Does this work?', None)):
        prepared = string(raws[frame], pointer)
        assert prepared.decode('ascii') == text
        source = None
        if literal:
            address = struct.unpack_from('<I', arm, literal)[0]
            assert address == struct.unpack_from('<I', original, literal)[0]
            assert string(arm, address) == prepared
            source = {'address': address, 'Japanese': string(original, address).decode('cp932')}
        else:
            source = {'COMMON_ID': 11, 'Japanese': original_confirmation.text.decode('cp932')}
        plane, events = raster(arm, kanji, prepared)
        crop = list(Image.open(shots[frame]['path']).convert('RGB').crop((16, 296, 244, 376)).get_flattened_data())
        for index in (14, 15):
            assert {i for i, v in enumerate(crop) if v == captured_rgb(palette[index])} == {i for i, v in enumerate(plane) if v == index}
        visible = [e for e in events if e['code'] not in (0, 10, 13, 32)]
        assert [e['code'] for e in visible] == [ord(c) for c in text if not c.isspace()]
        controls = []
        for event in (visible[0], visible[-1]):
            affected = [i for i, v in enumerate(plane) if v and event['x'] <= i % 228 < event['x'] + 6
                        and event['y'] <= i // 228 < event['y'] + 12]
            assert affected
            erased = bytearray(plane)
            for index in affected:
                erased[index] = 0
            assert any({i for i, v in enumerate(crop) if v == captured_rgb(palette[index])}
                       != {i for i, v in enumerate(erased) if v == index} for index in (14, 15))
            controls.append({'code': event['code'], 'erased_ink_shadow_positions_rejected': len(affected)})
        parents = [a for a in range(0x170000, len(raws[frame]) - 0x90, 4)
                   if struct.unpack_from('<I', raws[frame], a)[0] == 0x021438A0
                   and struct.unpack_from('<2I', raws[frame], a + 0x28) == (228, 48)]
        assert len(parents) == 1
        sp = folder / f'native_state_{frame:06d}/native_state.json'
        state = read(sp)
        state['manifest'] = str(sp)
        native = view_replay(arm, raws[frame], BASE + parents[0], prepared, state)
        notices.append({'frame': frame, 'text': text, 'source': source,
            'whole228x80_ink_shadow_blank_cells_exact': True, 'all_visible_glyphs_in_order': True,
            'first_final_erasure_controls': controls, 'actual_native_view': native,
            'native_state_manifest': str(sp), 'native_state_manifest_sha256': sha(sp.read_bytes())})
    persisted = []
    for frame in (4300, 5500, 7500, 9100, 9900, 12300, 13900, 14700, 15100, 16700, 17500):
        models = fleet_models(arm, raws[frame], 1)
        expected = [89, 9, 9, 9, 9] if 14700 <= frame <= 16700 else [49, 19, 19, 19, 19]
        assert [s['canonical_Hull_Crew'][1] for s in models] == expected
        assert [s['canonical_Hull_Crew'][0] for s in models] == [60, 25, 25, 25, 25]
        persisted.append({'frame': frame, 'original_fleet_getter_models': models})
    assert raws[9500][MODEL - BASE:MODEL - BASE + 48] == raws[9900][MODEL - BASE:MODEL - BASE + 48]
    save(ROOT / 'full_inputs.json', report['scripted_input_schedule'])
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'report': str(rp), 'report_sha256': sha(rp.read_bytes()), 'terminal_frames': 17500,
        'unique_two_screen_captures': len(shots), 'read_only_RAM_frames': len(raws),
        'no_savestate_ROM_RAM_inventory_health_money_or_location_fixture': True,
        'source_bound_controller': PARENT, 'actual_allocation_model': MODEL,
        'original_native_clean_current_code_spans': spans, 'original_menu_table': table,
        'source_minimum_maximum': limits, 'all_three_policy_native_and_actual_models': policy_rows,
        'all_seven_plaques_each_complete_in_thirteen_actual_contexts': plaque_rows,
        'whole_plaque_pixel_comparisons': sum(r['complete_material_border_letter_pixels'] for r in plaque_rows),
        'all_thirteen_actual_numeric_field_sets': field_rows, 'three_complete_popup_labels': popup_rows,
        'six_complete_native_notices_and_confirmation_planes': notices,
        'eleven_original_persisted_fleet_getter_states': persisted,
        'B_cancels_confirmation_without_model_changes': True,
        'Flagship_committed_through_original_X_A_then_reopened_89_9_9_9_9': True,
        'Even_restored_through_original_X_A_49_19_19_19_19': True,
        'ordinary_game_Save_not_requested_no_persistent_cold_reload_claim': True,
        'existing_plaque_packet_asset_identity': read(ROOT / 'existing_packet_current_identity.json'),
        'visual_review': 'Three policy views, notices, all five selections and confirmation reviewed; no new material streak or overlap seen. User approval not inferred.',
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'all18_original_plaques_incomplete22_historical_scopes_retained': True,
        'all_other_gameplay_legacy_card_control_transition_and_acceptance_gates_remain_open': True,
        'full_goal_complete': False,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), Path('scripts/run_crew_policy_matrix_v657.py'))}}
    save(ROOT / 'proof.json', proof)
    print(f'V657: three original policies; {len(plaque_rows)} whole plaques; six complete text planes; Flagship commit/reopen and Even restoration pass.')


if __name__ == '__main__':
    main()
