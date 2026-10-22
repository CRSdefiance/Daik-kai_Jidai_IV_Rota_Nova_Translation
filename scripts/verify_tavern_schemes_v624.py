"""Verify all native Tavern scheme menu crops and retain dialogue defects."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R1,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_scheme_labels import apply_release
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_regional_ui_v616 import full_cells
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_schemes_v624')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v624_candidate.nds')


def receipt(version):
    root = CAP / f'tavern_schemes_v{version}_expert'
    path = root / 'capture_report.json'
    report = read(path)
    assert report['frames'] == 9201 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors']
    fixtures = report['synthetic_strategist_room_assignment_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 3200
    assert len(fixtures[0]['changes']) == 11
    assert fixtures[0]['only_three_room_bytes_one_XP_word_and_one_calendar_word_changed']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_') and k != 'synthetic_strategist_room_assignment_fixtures')
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    shots = {r['frame']: r for r in report['frames_captured']}
    for row in shots.values():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return root, report, shots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def requests(arm, raw, itcm):
    """Replay only rows whose original containing menu is resident and typed."""
    u = machine(arm)
    u.mem_write(BASE, raw)
    u.mem_write(0x01FF8000, itcm)
    renderer = 0x02460000
    u.mem_write(renderer, struct.pack('<I', 0x0215FA94))
    rows = []
    for at in range(0x180000, 0x300000, 4):
        if raw[at:at + 4] != struct.pack('<I', 0x021409E4):
            continue
        parent = struct.unpack_from('<I', raw, at + 0x108)[0]
        if not BASE <= parent < BASE + 0x400000:
            continue
        assert struct.unpack_from('<I', raw, parent - BASE)[0] == 0x021408B4
        rows.append((BASE + at, parent))
    assert rows == [(0x02190BC8 + i * 0x140, 0x02190B04) for i in range(4)]
    result = []

    def trace(uc, address, size, data):
        if address == BASE + 0xD13A4:
            # Selection paint is outside this text submission contract.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        if address == 0x01FF92D8:
            sizep, destp = struct.unpack('<2I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 8))
            result.append({
                'image': uc.reg_read(UC_ARM_REG_R1),
                'source_origin': list(struct.unpack('<2i', uc.mem_read(uc.reg_read(UC_ARM_REG_R3), 8))),
                'size': list(struct.unpack('<2i', uc.mem_read(sizep, 8))),
                'destination_origin': list(struct.unpack('<2i', uc.mem_read(destp, 8)))})
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    handle = u.hook_add(UC_HOOK_CODE, trace)
    for row, _ in rows:
        call(u, 0x52FD0, (row, renderer), instruction_limit=200000)
    u.hook_del(handle)
    assert len(result) == 4
    return result


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v624'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches']) == 470 and all(manifest['checks'].values())
    parent = NdsImage.open('out/all_routes_combined_v623_candidate.nds')
    old_files = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    files = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    assert old_files.keys() == files.keys()
    assert [p for p in old_files if old_files[p] != files[p]] == ['/__arm9__.bin']
    arm, transform = apply_release(old_files['/__arm9__.bin'], 'translations/tavern_scheme_labels_v1.json')
    assert arm == files['/__arm9__.bin']
    old_root, old_run, old_shots, old_receipt = receipt(623)
    root, run, shots, new_receipt = receipt(624)
    assert run['ROM_sha256'] == digest and run['scripted_input_schedule'] == old_run['scripted_input_schedule']
    assert read(root / 'navigation_command_journal.json')['commands_received'] == read(old_root / 'navigation_command_journal.json')['commands_received']
    itcm = (root / 'native_state/arm9_itcm.bin').read_bytes()
    font = GameAsciiFont.from_arm9(arm)
    cases = []
    for frame in (4400, 4800, 5200, 5600, 6400, 6800, 7200, 7600):
        main_menu = frame < 6000
        texts = ['Order Drink', 'Treat Everyone', 'Recruit Crew', 'Schemes'] if main_menu else ['Lure Fleet', 'Forge Papers', 'Bad Rumors', 'Bribe']
        width, left = (84, 86) if main_menu else (72, 92)
        raw = (root / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        reqs = requests(arm, raw, itcm)
        im = Image.open(shots[frame]['path']).convert('RGB')
        for index, (text, req) in enumerate(zip(texts, reqs, strict=True)):
            assert req == {
                'image': 0x022BD79C,
                'source_origin': [0, index * 12] if index < 3 else [120, 0],
                'size': [width, 12], 'destination_origin': [left, 60 + index * 20]}
            flags, words, height, _, pixel_offset = struct.unpack_from('<5I', raw, req['image'] - BASE)
            assert (flags, words, height) == (4, 64, 36)
            sx, sy = req['source_origin']
            x0 = (width - len(text) * 6) // 2
            expected = bytearray(width * 12)
            for n, char in enumerate(text):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[y * width + x0 + n * 6 + x] = 8
            pixels = req['image'] - BASE + pixel_offset
            actual = bytes((raw[pixels + ((sy + y) * 256 + sx + x) // 2] >>
                            (4 * (((sy + y) * 256 + sx + x) % 2))) & 15
                           for y in range(12) for x in range(width))
            assert actual == expected
            dx, dy = req['destination_origin']
            cases.append({'frame': frame, 'original_request': req,
                          'complete_source_view_letters_and_all_blank_cells_exact': True,
                          **full_cells(im, font, text, dx + x0, 192 + dy, (8, 8, 8))})
    equal = [1, 60, 180, 3200, 3600, 4000, 6000, 8000, 8001, 8400, 9200, 9201]
    for frame in equal:
        assert Image.open(shots[frame]['path']).convert('RGB').tobytes() == Image.open(old_shots[frame]['path']).convert('RGB').tobytes()
    market = read(CAP / 'tavern_schemes_v624_market/capture_report.json')
    control = read(CAP / 'plaza_distribution_v623_market/capture_report.json')
    assert market['ROM_sha256'] == digest and market['frames'] == 24100
    assert market['cold_boot'] and not market['savestate_loaded'] and not market['callback_errors']
    assert 'battery_save_preloaded' not in market and not any(v for k, v in market.items() if k.startswith('synthetic_'))
    ms = {x['frame']: x for x in market['frames_captured']}
    cs = {x['frame']: x for x in control['frames_captured']}
    assert ms.keys() == cs.keys() and len(ms) == 19
    for frame, row in ms.items():
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        assert Image.open(row['path']).convert('RGB').tobytes() == Image.open(cs[frame]['path']).convert('RGB').tobytes()
    patch, preservation = read(ROOT / 'patch_proof.json'), read(ROOT / 'preservation_proof.json')
    assert patch['candidate_sha256'] == preservation['candidate_sha256'] == digest
    assert patch['exact_all_byte_reconstruction'] and preservation['current921_format_palette_extent_checks']
    assert preservation['all57_embedded_block_extents_exact']
    save(ROOT / 'release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
        'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'patch_sha256': patch['patch_sha256'],
        'transform': transform, 'complete_four_row_menus_all_eight_selection_states': cases,
        'all32_original_source_views_and_real_framebuffer_masks_pass': True,
        'unowned_source_canvas_pixels_not_assumed_cleared_or_rendered': True,
        'all12_outside_changed_menus_frames_exact_V623': equal,
        'ordinary19_no_fixture_New_Game_Market_frames_exact_V623': sorted(ms),
        'disclosed_Gerhard_room_XP_and_three_day_calendar_fixture': run['synthetic_strategist_room_assignment_fixtures'][0],
        'command_context_followups': [
            {'frame': 6000, 'defect': 'COMMON_MESSAGE_909 wraps inside words in both builds; existing portrait formatter excludes this later message family.'},
            {'frame': 8000, 'defect': 'Separate general scheme-name table still expands Japanese Bribe in both builds; menu table localization does not reach it.',
             'source_pointer_field': 0x0214C60C, 'source_string': 0x0214C530},
            {'remaining_general_scheme_name_pointer_fields': [0x0214C600, 0x0214C604, 0x0214C608, 0x0214C60C],
             'all_four_command_entry_cancel_and_outcome_contexts_still_require_verification': True}],
        'Bribe_reaches_original_faction_choice_and_B_returns_Tavern_menu': True,
        'scheme_family_dialogue_or_all_command_outcomes_not_claimed_complete': True,
        'all470_batches114_accepted_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'reports': [old_receipt, new_receipt], 'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'broader_graphics_material_legacy_village_Confirm_and_miniature_gates_open': True,
        'full_goal_complete': False, 'canonical_promoted': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('V624:5 English labels,32 full native source/GPU masks,12 control frames,19 ordinary screens and exact patch pass;2 dialogue follow-ups remain open.')


if __name__ == '__main__':
    main()
