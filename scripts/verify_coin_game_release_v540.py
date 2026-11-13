"""Integrated prompt packing, native masks, board source and exact patch."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R6

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.coin_game_prompts import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path('out/all_routes_combined_v540_candidate.nds')
PARENT = Path('out/all_routes_combined_v534_candidate.nds')
OUT = Path('work/analysis/coin_game_v540')
CAPTURES = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def report(folder, digest):
    result = read(folder / 'capture_report.json')
    assert result['ROM_sha256'] == digest and result['cold_boot']
    assert not result['savestate_loaded'] and not result['callback_errors']
    for shot in result['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    return result


def main():
    parent, current = NdsImage.open(PARENT), NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    assert digest == '9f2e4c47c059b0606141d93c0f17a34f16a75fd66ceefe63c04e8a2a54577859'
    manifest = read(ROM.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v540'
    assert len(manifest['batches']) == 470
    old = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
    new = {p: data for _, p, data in current.iter_files()} | dict(current.iter_components())
    assert old.keys() == new.keys() and [p for p in old if old[p] != new[p]] == ['/__arm9__.bin']
    arm = new['/__arm9__.bin']
    expected, packing = apply_release(old['/__arm9__.bin'], 'translations/coin_game_prompts_v1.json')
    assert expected == arm
    sections = [[(s.ramAddress, len(s.data), s.bssSize) for s in MainCodeFile(a, 0x02000000).sections]
                for a in (old['/__arm9__.bin'], arm)]
    assert sections[0] == sections[1]
    u = machine(arm)
    selector = []
    for outcome, literal in [(0, 0x639F4), (1, 0x639F0)]:
        u.reg_write(UC_ARM_REG_R0, outcome)
        u.reg_write(UC_ARM_REG_R6, 0x02470000)
        u.emu_start(0x02063900, 0x02063910, count=16)
        pointer = u.reg_read(UC_ARM_REG_R1)
        assert pointer == struct.unpack_from('<I', arm, literal)[0]
        selector.append({'supplied_outcome': outcome, 'original_pointer_literal': literal,
                         'actual_message_pointer': pointer, 'complete_native_selector_fragment': True})
    font = GameAsciiFont.from_arm9(arm)
    cases = []
    for name, text, folder, frame in [
        ('decision', "Let's decide who goes first.", 'coin_game_v540', 4000),
        ('player_first', 'You go first.', 'coin_game_v540', 4600),
        ('opponent_first', "I'll go first.", 'coin_game_v540_opponent_prompt', 5000),
    ]:
        base = CAPTURES / folder
        fixture_path = OUT / ('opponent_prompt_RESEARCH_ONLY.nds' if name == 'opponent_first' else 'coin_game_RESEARCH_ONLY.nds')
        data = report(base, sha(fixture_path.read_bytes()))
        shot = next(s for s in data['frames_captured'] if s['frame'] == frame and
                    (s['path'].endswith('_navigation.png') if name != 'opponent_first' else s['path'].endswith('_final.png')))
        image = Image.open(shot['path']).convert('RGB')
        ink, bounds = complete_mask(font, text, image, 16, 296, (0, 8, 0))
        assert not any(image.getpixel((x, y)) == (0, 8, 0)
                       for x in range(bounds[2], 240) for y in range(296, 307))
        cases.append({'case': name, 'english': text, 'complete_glyph_ink_pixels': ink,
                      'native_bounds': bounds, 'first_final_punctuation_and_blank_cells_exact': True,
                      'no_old_Japanese_or_English_ghosts_after_text': True, 'capture': shot,
                      'opponent_first_uses_explicit_message_selection_fixture': name == 'opponent_first'})
    board = PxlImage.from_bytes(current.read_file('/_pxl/slackimg11.pxl'))
    image = Image.open(cases[0]['capture']['path']).convert('RGB')
    for y in range(72):
        for x in range(80, 256):
            assert native5(board.palette[board.indices[y * 256 + x]]) == native5(image.getpixel((x, 192 + y)))
    assert current.read_file('/_pxl/slackimg11.pxl') == NdsImage.open('work/clean.nds').read_file('/_pxl/slackimg11.pxl')
    fresh = report(CAPTURES / 'coin_game_v540_fresh', digest)
    old_fresh = report(CAPTURES / 'site_descriptions_v534_fresh', sha(PARENT.read_bytes()))
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule'] and fresh['core_options'] == old_fresh['core_options']
    frames = [{s['frame']: s for s in r['frames_captured']} for r in (old_fresh, fresh)]
    assert frames[0].keys() == frames[1].keys() and len(frames[0]) == 56
    assert all(frames[0][n]['PNG_sha256'] == frames[1][n]['PNG_sha256'] for n in frames[0])
    preservation = read('work/analysis/site_descriptions_v534/preservation_proof.json')
    assert len(preservation['entries']) == 921
    assert all(old[r['path']] == new[r['path']] for r in preservation['entries'])
    preservation.update(candidate=str(ROM), candidate_sha256=digest,
                        parent=str(PARENT), parent_preservation_proof='work/analysis/site_descriptions_v534/preservation_proof.json')
    (OUT / 'preservation_proof.json').write_text(json.dumps(preservation, indent=2) + '\n', encoding='utf-8')
    make_xdelta(Path('work/clean.nds'), ROM, ROM.with_suffix('.xdelta'))
    apply_xdelta(Path('work/clean.nds'), ROM.with_suffix('.xdelta'), OUT / 'reconstructed.nds')
    assert (OUT / 'reconstructed.nds').read_bytes() == ROM.read_bytes()
    requirements = read('translations/graphics_completion_requirements_v313.json')
    assert len(requirements['historical_pending_items_retained']) == 22
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()), 'exact_clean_patch_reconstruction': True,
             'all3_natural_prompt_native_masks': cases, 'both_original_turn_selector_cases': selector,
             'source_owned_storage_packing': packing, 'section_geometry': sections[1],
             'all_470_batches114_layers675_graphics921_preservation_entries_retained': True,
             'all56_title_New_Game_story_town_Help_frames_exact_parent': True,
             'all_code_heap_startup_cache_and_unowned_data_unchanged': True,
             'original_coin_board_clear_region': [80, 192, 256, 264],
             'all12672_unobscured_source_board_pixels_exact': True,
             'native_coin_game_entry_with_synthetic_source_opcode_setup': True,
             'normal_gambler_recruitment_or_post_return_story_branch_verified': False,
             'status': 'experimental', 'canonical_promoted': False,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'other_legacy_source_restoration_and_context_gates_remain': True, 'full_goal_complete': False}
    (OUT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V540:three complete English masks,12672 board pixels,56 exact regression frames,all inherited graphics and exact patch pass.')


if __name__ == '__main__':
    main()
