"""Verify complete original mission displays, financial bounds and V617 integration."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import (
    SJIS_GLYPH_COUNT,
    SJIS_MAP_OFFSET,
    GameAsciiFont,
    decode_glyph,
)
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.regional_assignment_wrap import transform
from dk4tool.patch.regional_fleet_ordinal_label import transform as ordinal_transform
from dk4tool.patch.regional_fleet_plaques import FILE, RECORDS
from dk4tool.rom.nds import NdsImage
from scripts.native_regional_finance_v617 import ARM, FIELDS, VALUES
from scripts.probe_button_prompt_native import (
    BASE,
    HEADER,
    STACK,
    call,
    machine,
)
from scripts.verify_regional_ui_v616 import full_cells, glyphs, native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/regional_missions_v617')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v617_candidate.nds')
MISSIONS = ((11800, 4, 7, 'Patrol', 'Stockholm is the patrol base.'),
            (17400, 3, 7, 'Dock', 'Stockholm is the port.'),
            (22200, 1, 7, 'Manage Area', 'Stockholm is the base.'),
            (37800, 5, 5, 'Attack Town', 'Hamburg is the target.'))


def receipt(context, frames, digest):
    path = CAP / ('regional_missions_v617_' + context) / 'capture_report.json'
    report = read(path)
    assert report['frames'] == frames and report['ROM_sha256'] == digest
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    shots = {r['frame']: r for r in report['frames_captured']}
    for row in shots.values():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return report, shots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def full_dialog(im, font, lines):
    origin = 22 if len(lines) > 1 else 16
    masks = [full_cells(im, font, text, origin, 296 + i * 16, (0, 8, 0))
             for i, text in enumerate(lines)]
    expected = {(origin + x, 296 + i * 16 + y) for i, text in enumerate(lines)
                for x, y in glyphs(font, text)}
    actual = {(x, y) for y in range(294, 350) for x in range(12, 244)
              if im.getpixel((x, y)) == (0, 8, 0)}
    assert actual == expected
    return {'lines': masks, 'all_lines_same_left_origin': origin,
            'entire_dialog_text_ink_and_blank_cells_exact_no_missing_or_stray_letters': True}


def original_role(im, arm, kanji, font):
    text, x0, y0 = 'Fleet ２ Admiral', 84, 60
    table = struct.unpack_from(f'<{SJIS_GLYPH_COUNT}H', arm, SJIS_MAP_OFFSET)
    code = int.from_bytes('２'.encode('cp932'), 'big')
    digit = decode_glyph(kanji, table.index(code))
    expected, advance = set(), 0
    for ch in text:
        cell, width = (digit, 12) if ch == '２' else (font.decode(ch), 6)
        expected.update((advance + x, y) for y in range(11) for x in range(width) if cell.getpixel((x, y)))
        advance += width
    assert advance == 96
    actual = {(x, y) for y in range(11) for x in range(advance)
              if im.getpixel((x0 + x, y0 + y)) == (230, 230, 230)}
    assert actual == expected
    return {'text': text, 'origin': [x0, y0], 'whole_foreground_nonforeground_field_positions': advance * 11,
            'independent_original_ASCII_and_KANJI_ink_points': len(expected),
            'complete_first_final_letters_and_original_fullwidth_digit': True,
            'full_RGB_background_composition_not_claimed': True}


def native_role_composite(arm, raw, atlas, im):
    """Use original paletted font drawing and its original CP932 shadow pass."""
    u = machine(arm)
    u.mem_write(BASE, raw)
    original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0xD1604:0xD19BC] == original[0xD1604:0xD19BC]
    clean = machine(original)
    assert u.mem_read(0x01FF83AC, 0x21C) == clean.mem_read(0x01FF83AC, 0x21C)
    # Original D1700 literal, shared by ASCII and CP932 drawing; no sampled colours.
    palette_pointer = struct.unpack_from('<I', arm, 0xD181C)[0]
    palette = bytes(u.mem_read(palette_pointer, 32))
    assert palette_pointer == 0x02125A20
    assert palette == original[palette_pointer - BASE:palette_pointer - BASE + 32]
    canvas = struct.pack('<5I', 4, 64, 192, 20, 52) + palette + bytes(24576)
    point, string, style = 0x02460000, 0x02460100, 0x02460200
    assert HEADER + len(canvas) + 16 < point
    u.mem_write(HEADER - 16, b'\xA5' * (len(canvas) + 32))
    u.mem_write(HEADER, canvas)
    u.mem_write(point, struct.pack('<2I', 84, 60))
    u.mem_write(string, 'Fleet ２ Admiral'.encode('cp932') + b'\0')
    u.mem_write(style, bytes(32))
    u.mem_write(STACK, struct.pack('<I', 1))
    executed = call(u, 0xD1604, (style, HEADER, point, string))
    required = {0x020D1604, 0x020D16B4, 0x01FF83AC, 0x020D198C, 0x020D1898}
    assert required <= executed
    assert bytes(u.mem_read(HEADER - 16, 16)) == bytes(u.mem_read(HEADER + len(canvas), 16)) == b'\xA5' * 16
    layer = PxlImage.from_bytes(bytes(u.mem_read(HEADER, len(canvas))))
    assert layer.source[:52] == canvas[:52]
    shadow = [(i % 256, i // 256) for i, value in enumerate(layer.indices) if value == 15]
    assert len(shadow) == 18
    expected = atlas.copy()
    for y in range(60, 72):
        for x in range(84, 180):
            index = layer.indices[y * 256 + x]
            if index:
                colour = tuple((v * 31 + 127) // 255 for v in layer.palette[index][:3])
                expected.putpixel((x, y), colour)
    box = (84, 60, 180, 72)
    assert native5(im).crop(box).tobytes() == expected.crop(box).tobytes()
    outside = [(i % 256, i // 256, value) for i, value in enumerate(layer.indices)
               if value and not (84 <= i % 256 < 180 and 60 <= i // 256 < 72)]
    assert not outside, outside[:20]
    return {'complete_box': list(box), 'all1152_native5_background_foreground_and_shadow_pixels_exact': True,
            'original_18_CP932_shadow_pixels_explain_prior_atlas_only_mismatch': shadow,
            'original_source_palette_pointer': palette_pointer, 'source_palette_sha256': sha(palette),
            'original_ASCII_CP932_lookup_and_shadow_passes_execute': sorted(required),
            'original_renderer_code_palette_and_KANJI_data_preserved': True,
            'supplied_font_canvas_contract_actual_screen_comparison_not_GPU_internal_trace': True}


def main():
    digest = sha(ROM.read_bytes())
    manifest, registry = read(ROM.with_suffix('.manifest.json')), read('translations/release_stack.json')
    assert manifest['profile'] == 'all-routes-unified-v617' and manifest['candidate_sha256'] == digest
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256'] == sha(Path(manifest['base_rom']).read_bytes())
    assert len(manifest['batches']) == 470 and len(registry['accepted_layers']) == 114 and all(manifest['checks'].values())
    parent, current = NdsImage.open('out/all_routes_combined_v616_candidate.nds'), NdsImage.open(ROM)
    old = {p: b for _, p, b in parent.iter_files()} | dict(parent.iter_components())
    new = {p: b for _, p, b in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys() and [p for p in old if old[p] != new[p]] == ['/__arm9__.bin']
    guarded, guard_proof = transform(old['/__arm9__.bin'])
    arm, ordinal_proof = ordinal_transform(guarded)
    assert arm == new['/__arm9__.bin'] and sha(arm) == ARM
    native = read(ROOT / 'native_guarded_assignment_proof.json')
    assert native['guard_transform'] == guard_proof and native['ordinal_transform'] == ordinal_proof
    assert native['all3668_native_ID_dispatch_outputs_exact'] == 3668
    assert len(native['complete_field_variants']) == 112 and len(native['unchanged_other_direct_text_callers']) == 11
    assert len(native['four_original_composed_notifications']) == 4
    assert native['script_sha256'] == sha(Path('scripts/probe_regional_missions_v617.py').read_bytes())
    font, kanji = GameAsciiFont.from_arm9(arm), current.read_file('/GRP/KANJI.FNT')
    actual_run, shots, actual_receipt = receipt('actual', 42600, digest)
    fixture = read('work/analysis/regional_fleet_v615/formed_fixture_manifest.json')
    assert actual_run['battery_save_preloaded']['source_sha256'] == fixture['fixture_sha256']
    assert sha(Path(fixture['fixture']).read_bytes()) == fixture['fixture_sha256']
    assert sha(Path(fixture['original_donor']).read_bytes()) == fixture['original_donor_sha256']
    synthetic = actual_run['synthetic_regional_financial_display_fixtures']
    assert len(synthetic) == 1 and synthetic[0]['display_values'] == VALUES
    assert synthetic[0]['frame'] == 37800 and synthetic[0]['only_three_declared_finance_words_changed']
    assert len(synthetic[0]['changes']) == 12
    assert not actual_run['actual_monthly_or_earned_regional_finances_verified']
    assert not any(v for k, v in actual_run.items() if k.startswith('synthetic_') and k != 'synthetic_regional_financial_display_fixtures')

    def image(frame):
        return Image.open(shots[frame]['path']).convert('RGB')

    confirmations = []
    for frame, city, text in ((10200, 'Stockholm', 'Patrol orders issued.'),
                              (15800, 'Stockholm', 'Docking orders issued.'),
                              (20600, 'Stockholm', 'Area management orders issued.'),
                              (36200, 'Hamburg', 'Attack orders issued.')):
        confirmations.append({'frame': frame, **full_dialog(image(frame), font, ['Manuel Fleet:', city, text])})
    prompts = []
    for frame, message_id, lines in ((24600, 131, ['Choose a city to attack.']),
            (26600, 132, ['You have already signed a contract', 'with that city.']),
            (32200, 134, ["That city doesn't have a contract", "with a faction you're at war with."]),
            (34600, 133, ['A faction not at war with you holds', 'a contract with that city.']),
            (42600, 128, ['You have no contract with that city.'])):
        prompts.append({'frame': frame, 'native_message_ID': message_id, **full_dialog(image(frame), font, lines)})

    atlas = native5(PxlImage.from_bytes(new[FILE]).render())
    resources, missions, pixels = [], [], 0
    for frame, policy, town, label, description in MISSIONS:
        im = image(frame)
        converted = native5(im)
        for _, text, _, box, _, _ in RECORDS:
            assert converted.crop(box).tobytes() == atlas.crop(box).tobytes(), (frame, text)
            pixels += (box[2] - box[0]) * (box[3] - box[1])
        snap = next(r for r in actual_run['read_only_pause_RAM_snapshots'] if r['frame'] == frame)
        raw = Path(snap['path']).read_bytes()
        assert sha(raw) == snap['sha256'] and len(raw) == 0x400000 and raw.find(new[FILE]) >= 0
        u = machine(arm)
        u.mem_write(BASE, raw)
        owner = 0x02313380
        ptr = struct.unpack('<I', u.mem_read(owner + 12, 4))[0]
        assert bytes(u.mem_read(ptr, 64)).split(b'\0')[0] == b'_pxl/chihofleetinfo.pxl'
        call(u, 0xCB1A8, ())
        fleet = u.reg_read(UC_ARM_REG_R0) + 4 + 57 * 0x84
        assert tuple(u.mem_read(fleet + 0x3E, 2)) == (policy, town)
        predicates = []
        for entry in (0x36914, 0x36948, 0x367FC):
            call(u, entry, (fleet,))
            predicates.append(u.reg_read(UC_ARM_REG_R0))
        assert predicates[:2] == [1, 0] and predicates[2]
        resources.append({'frame': frame, 'owner': owner, 'whole_named_resource_resident': BASE + raw.find(new[FILE]),
                          'original_own_main_finance_getters': predicates, 'original_policy_town_bytes': [policy, town],
                          'RAM_sha256': snap['sha256']})
        # Original 8E104..8E114: six pixels per character, right aligned to x256; y180.
        x = 256 - len(description) * 6
        missions.append({'frame': frame, 'source_policy_ID': policy, 'source_town_ID': town,
                         'label': full_cells(im, font, label, 52, 164, (230, 230, 230)),
                         'description': full_cells(im, font, description, x, 180, (0, 255, 0)),
                         'role': original_role(im, arm, kanji, font),
                         'complete_role_composition': native_role_composite(arm, raw, atlas, im)})

    # Exact clean original field-load and draw-position code, independent of observed digit placement.
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x8DFD8:0x8E040] == clean_arm[0x8DFD8:0x8E040]
    finances = [dict(field=key, **full_cells(image(39400), font, str(VALUES[key]), 52, y, (230, 230, 230)))
                for key, y in (('income', 104), ('expenses', 124), ('invested', 144))]
    financial_raw = (CAP / 'regional_missions_v617_actual/frame_039400_arm9_ram.bin').read_bytes()
    address = synthetic[0]['actual_finance_record']
    assert {key: struct.unpack_from('<I', financial_raw, address - BASE + off)[0] for key, off in FIELDS.items()} == VALUES
    for _, _, _, box, _, _ in RECORDS:
        assert native5(image(39400)).crop(box).tobytes() == atlas.crop(box).tobytes()

    market, market_shots, market_receipt = receipt('market', 24100, digest)
    previous = read(CAP / 'regional_ui_v616_market/capture_report.json')
    assert market['scripted_input_schedule'] == previous['scripted_input_schedule']
    assert 'battery_save_preloaded' not in market and not any(v for k, v in market.items() if k.startswith('synthetic_'))
    old_shots = {r['frame']: r for r in previous['frames_captured']}
    assert market_shots.keys() == old_shots.keys() and len(market_shots) == 19
    for frame, row in market_shots.items():
        assert Image.open(row['path']).convert('RGB').tobytes() == Image.open(old_shots[frame]['path']).convert('RGB').tobytes()
    preservation, patch = read(ROOT / 'preservation_proof.json'), read(ROOT / 'patch_proof.json')
    assert preservation['candidate_sha256'] == patch['candidate_sha256'] == digest
    assert preservation['current921_format_palette_extent_checks'] and preservation['all57_embedded_block_extents_exact']
    assert patch['exact_all_byte_reconstruction'] and sha(ROM.with_suffix('.xdelta').read_bytes()) == patch['patch_sha256']
    save(ROOT / 'release_proof.json', {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
         'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'patch_sha256': patch['patch_sha256'],
         'all470_batches114_accepted_layers': True, 'only_ARM9_changes_all_other_files_components_and_art_exact_V616': True,
         'guard_and_ordinal_transforms_exact_native_probe': True, 'four_complete_assignment_confirmations': confirmations,
         'five_actual_instruction_contract_war_notices': prompts, 'four_complete_mission_displays': missions,
         'all5_complete_regional_plaque_pixels_across4_missions': pixels, 'actual_source_resource_and_original_policy_getters': resources,
         'financial_fields_complete_unsigned_9_and10_digit_masks': finances,
         'isolated_12_byte_financial_display_fixture': synthetic[0],
         'actual_monthly_or_earned_finances_not_claimed': True,
         'role_complete_native5_material_foreground_and_original_digit_shadow_composition_passes': True,
         'ordinary19_no_save_no_fixture_New_Game_Market_full_screens_exact_V616': True,
         'all921_graphics57_embedded_formats_palettes_extents_preserved': True,
         'exact_clean_patch_reconstruction': True, 'reports': [actual_receipt, market_receipt],
         'source_donor_saves_unchanged_hardware_and_human_acceptance_not_claimed': True,
         'all18_original_plaques_remain_incomplete_all22_historical_scopes_retained': True,
         'broader_miniature_Confirm_village_card_comic_legacy_movie_and_gameplay_gates_still_open': True,
         'full_goal_complete': False, 'canonical_promoted': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V617:4 confirmations,4 missions,5 notices,complete unsigned financial fields,all5 plaques,19 ordinary screens and exact patch pass.')


if __name__ == '__main__':
    main()
