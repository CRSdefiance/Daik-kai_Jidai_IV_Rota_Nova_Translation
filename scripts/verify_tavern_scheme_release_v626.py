"""Verify the complete cumulative build and actual four-command Tavern flow."""

from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_scheme_context import apply_release as scheme_context
from dk4tool.patch.tavern_strategist_wrap import apply_release as queued_context
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_regional_ui_v616 import full_cells
from scripts.verify_tavern_queued_native_v626 import queued_wrap
from scripts.verify_tavern_schemes_v624 import requests
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_schemes_v626')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v626_candidate.nds')


def main():
    rom = NdsImage.open(ROM)
    arm, common = rom.read_file('/__arm9__.bin'), rom.read_file('/COMMON/MESFILE.DK4')
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v626'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches']) == 470 and all(manifest['checks'].values())
    parent = NdsImage.open('out/all_routes_combined_v624_candidate.nds')
    mapped_common, mapped_arm, stage625 = scheme_context(parent.read_file('/COMMON/MESFILE.DK4'),
                                                         parent.read_file('/__arm9__.bin'),
                                                         'translations/tavern_scheme_context_v1.json')
    mapped_arm, stage626 = queued_context(mapped_arm, 'translations/tavern_strategist_wrap_v1.json')
    assert mapped_common == common and mapped_arm == arm
    old_files = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    new_files = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    assert old_files.keys() == new_files.keys()
    assert {p for p in old_files if old_files[p] != new_files[p]} == {'/__arm9__.bin', '/COMMON/MESFILE.DK4'}
    root = CAP / 'tavern_schemes_v626_expert'
    run = read(root / 'capture_report.json')
    assert run['ROM_sha256'] == digest and run['frames'] == 24801
    assert run['cold_boot'] and not run['savestate_loaded'] and not run['callback_errors']
    fixtures = run['synthetic_strategist_room_assignment_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 3200 and len(fixtures[0]['changes']) == 11
    assert fixtures[0]['only_three_room_bytes_one_XP_word_and_one_calendar_word_changed']
    assert not any(v for k, v in run.items() if k.startswith('synthetic_') and k != 'synthetic_strategist_room_assignment_fixtures')
    donor = run['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    shots = {x['frame']: x for x in run['frames_captured']}
    for shot in shots.values():
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    itcm = (root / 'native_state/arm9_itcm.bin').read_bytes()
    font = GameAsciiFont.from_arm9(arm)
    menus = []
    for frame in (4400, 4800, 5200, 5600, 6400, 6800, 7200, 7600):
        raw = (root / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        main_menu = frame < 6000
        texts = ['Order Drink', 'Treat Everyone', 'Recruit Crew', 'Schemes'] if main_menu else ['Lure Fleet', 'Forge Papers', 'Bad Rumors', 'Bribe']
        width, left = (84, 86) if main_menu else (72, 92)
        reqs = requests(arm, raw, itcm)
        im = Image.open(shots[frame]['path']).convert('RGB')
        for index, (text, req) in enumerate(zip(texts, reqs, strict=True)):
            assert req == {'image': 0x022BD79C, 'source_origin': [0, index * 12] if index < 3 else [120, 0],
                           'size': [width, 12], 'destination_origin': [left, 60 + index * 20]}
            dx, dy = req['destination_origin']
            menus.append({'frame': frame, 'source_request': req,
                          **full_cells(im, font, text, dx + (width - len(text) * 6) // 2, 192 + dy, (8, 8, 8))})
    entries = common_message_entries(common, arm, clean=False)
    dialogues = []
    cases = [
        (6000, 909, 0x02118340, 0x02053DB8, []),
        (8000, 915, 0x02118320, 0x02053DB8, ['Bribe']),
        (8800, 973, 0x02118220, 0x02053DB8, []),
        (9600, 979, 0x02118200, 0x02053D24, ['Lisbon', 'Castor Co.']),
        (10000, 965, 0x02118240, 0x02053DB8, []),
        (12800, 915, 0x02118320, 0x02053DB8, ['Lure Fleet']),
        (13600, 921, 0x02118300, 0x02053DB8, []),
        (14400, 941, 0x021182A0, 0x02053D24, ['Castor Co.', 'Lisbon']),
        (17600, 915, 0x02118320, 0x02053DB8, ['Forge Papers']),
        (18400, 933, 0x021182C0, 0x02053DB8, []),
        (19200, 949, 0x02118280, 0x02053D24, ['Castor Co.', 'Albuquerque']),
        (22800, 915, 0x02118320, 0x02053DB8, ['Bad Rumors']),
        (23600, 927, 0x02117B40, 0x02053DB8, []),
        (24400, 957, 0x02118260, 0x02053D24, ['Lisbon', 'Castor Co.'])]
    for frame, number, table, caller, values in cases:
        text = entries[number].text.rstrip()
        for value in values:
            text = text.replace(b'%s', value.encode('ascii'), 1)
        assert b'%s' not in text
        formatted = queued_wrap(arm, text, caller, table)
        events = []
        pixels = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 80),
                        glyph_events=events, instruction_limit=600000)
        im = Image.open(shots[frame]['path']).convert('RGB')
        differences = [(x, y) for y in range(80) for x in range(228)
                       if bool(pixels[y * 228 + x]) != (im.getpixel((16 + x, 296 + y)) == (0, 8, 0))]
        if text.isascii():
            assert not differences, (frame, number, differences[:5])
        else:
            # Retain this older CP932-I renderer-model discrepancy explicitly.
            # No missing-word/layout clearance or arbitrary pixel waiver follows.
            assert all(c.isascii() or c == 'Ｉ' for c in text.decode('cp932'))
            cells = [(e['x'], e['y']) for e in events if e['code'] == 0x8268]
            assert cells and differences
            assert all(any(x == gx + 6 and gy + 2 <= y <= gy + 10 for gx, gy in cells)
                       for x, y in differences), (frame, differences[:10], cells)
            # The actual I still has its full visible left stroke. Preserve the
            # adjacent-column prediction difference as a separate open check.
            assert all(all(im.getpixel((16 + gx + 5, 296 + gy + y)) == (0, 8, 0)
                           for y in range(2, 10)) for gx, gy in cells)
        dialogues.append({'frame': frame, 'message_id': number, 'source_voice_table': table,
                          'source_parent': caller, 'expanded': text.decode('cp932'),
                          'native_formatted': formatted.decode('cp932'),
                          'all_ASCII_and_non_I_source_pixels_match_real_framebuffer': True,
                          'CP932_I_extra_column_native_prediction_difference_open': differences,
                          'whole_glyph_mask_exact': not differences})
    states = []
    for frame in (6000, 10000, 10400, 14800, 19600, 24800):
        raw = (root / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        u = machine(arm)
        u.mem_write(BASE, raw)

        def get(fn, args=(), cpu=u):
            call(cpu, fn, args)
            return cpu.reg_read(UC_ARM_REG_R0)

        factions = get(0xCB160)
        own = get(0x397D8, (factions,))
        money = get(0x3CCC8, (factions + 4 + own * 0x4C,))
        scheme_root = get(0xCB130)
        active = []
        for index in range(4, 14):
            data = bytes(u.mem_read(scheme_root + 4 + index * 16, 16))
            if data[4] != 11:
                active.append({'slot': index, 'type': data[4], 'whole_source_object_hex': data.hex()})
        states.append({'frame': frame, 'funds': money, 'active_scheme_slots4_to13': active})
    assert states[0]['funds'] == 8371 and states[0]['active_scheme_slots4_to13'] == []
    assert states[1]['funds'] == 8371  # Charge follows closing the original arrangements notice.
    assert all(s['funds'] == 7371 for s in states[2:])
    assert len(states[1]['active_scheme_slots4_to13']) == 1
    assert states[1]['active_scheme_slots4_to13'][0]['type'] == 9
    assert all(s['active_scheme_slots4_to13'] == states[1]['active_scheme_slots4_to13'] for s in states[2:])
    market = read(CAP / 'tavern_schemes_v626_market/capture_report.json')
    previous = read(CAP / 'tavern_schemes_v624_market/capture_report.json')
    assert market['ROM_sha256'] == digest and market['frames'] == 24100
    assert market['cold_boot'] and not market['savestate_loaded'] and not market['callback_errors']
    assert 'battery_save_preloaded' not in market and not any(v for k, v in market.items() if k.startswith('synthetic_'))
    ms, ps = ({x['frame']: x for x in r['frames_captured']} for r in (market, previous))
    assert ms.keys() == ps.keys() and len(ms) == 19
    for frame, shot in ms.items():
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        assert Image.open(shot['path']).convert('RGB').tobytes() == Image.open(ps[frame]['path']).convert('RGB').tobytes()
    native = read(ROOT / 'queued_native_proof.json')
    assert native['candidate_sha256'] == digest and len(native['all_original_scheme_voice_templates_through_both_queued_parent_formats']) == 160
    assert native['script_sha256'] == sha(Path('scripts/verify_tavern_queued_native_v626.py').read_bytes())
    patch, preservation = read(ROOT / 'patch_proof.json'), read(ROOT / 'preservation_proof.json')
    assert patch['candidate_sha256'] == preservation['candidate_sha256'] == digest
    assert patch['exact_all_byte_reconstruction'] and preservation['current921_format_palette_extent_checks']
    assert preservation['all57_embedded_block_extents_exact']
    save(ROOT / 'release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'patch_sha256': patch['patch_sha256'],
        'V625_source_name_and_two_voice_corrections': stage625, 'V626_source_queued_voice_wrapping': stage626,
        'all32_complete_menu_masks': menus, 'fourteen_source_bound_dialogue_cases': dialogues,
        'normal_Bribe_commits_one_type9_scheme_and1000_gold_three_other_commands_cancel': states,
        'native_22008_scope_comparisons115_parent_table_controls160_voice_rasters': str(ROOT / 'queued_native_proof.json'),
        'ordinary19_no_fixture_screens_exact_V624': sorted(ms),
        'disclosed_room_XP_calendar_fixture': fixtures[0],
        'all470_batches114_accepted_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'CP932_I_renderer_model_column_difference_and_897_898_voice_content_remain_open': True,
        'all18_original_plaques_incomplete_all22_historical_scopes_retained': True,
        'full_goal_complete': False, 'canonical_promoted': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V626:32 menu masks,14 source-bound dialogues,normal Bribe commit/3 cancellations,19 ordinary screens and exact patch pass;CP932 model/content follow-ups retained.')


if __name__ == '__main__':
    main()
