"""Verify the shared role-table correction, integrated ROM and actual First Mate."""

import argparse
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.crew_role_labels import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_crew_roles_v326 import CONFIG, ROOT
from scripts.verify_plaque_release_v247 import find_mask
from scripts.verify_portrait_native_pixels_v202 import native5

ROM = Path('out/all_routes_combined_v326_candidate.nds')
PARENT = Path('out/all_routes_combined_v324_candidate.nds')
DONOR = Path('../desmume-0.9.13-win64/Battery/extras_options_sound_common_v6_candidate.dsv')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def fresh_new_game(proof):
    path = Path('work/emulation_v193/crew_roles_v326_new_game/capture_report.json')
    report = read(path)
    parent = read('work/emulation_v193/sail_rotation_v324/capture_report.json')
    assert report['ROM_sha256'] == proof['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 31200 and report['scripted_input_schedule'] == parent['scripted_input_schedule']
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    for number in (1200, 2000, 10800, 14400):
        before = next(row for row in parent['frames_captured'] if row['frame'] == number)
        assert sha(Path(before['path']).read_bytes()) == before['PNG_sha256']
        assert Image.open(before['path']).tobytes() == Image.open(frames[number]['path']).tobytes()
    font = GameAsciiFont.from_arm9((ROOT / 'research_arm9.bin').read_bytes())
    captions = []
    for number in (30400, 30800):
        shot = Image.open(frames[number]['path']).convert('RGB')
        for text, region in [('Rotate', (15, 366, 88, 384)), ('Inspect', (110, 366, 199, 384)),
                             ('Sails', (198, 366, 256, 384))]:
            captions.append({'frame': number, **find_mask(font, text, shot, region)})
    proof.update({'separate_fresh_New_Game_frames': 31200,
                  'separate_fresh_New_Game_report': str(path),
                  'separate_fresh_New_Game_report_sha256': sha(path.read_bytes()),
                  'four_title_character_opening_recruitment_frames_exactV324': True,
                  'retained_full_sailing_caption_masks': captions})


def live(proof):
    report_path = Path('work/emulation_v193/crew_roles_v326/capture_report.json')
    report, previous = read(report_path), read('work/emulation_v193/existing_save_v325/capture_report.json')
    assert report['ROM_sha256'] == proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 17600
    assert report['scripted_input_schedule'] == previous['scripted_input_schedule']
    assert report['battery_save_preloaded']['source_sha256'] == sha(DONOR.read_bytes()) == (
        '28ff98d46e3b2ce1b1d9525059988f18a4ddf0d5bedac9140a183285493fdc2e')
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    font = GameAsciiFont.from_arm9((ROOT / 'research_arm9.bin').read_bytes())
    shot = Image.open(frames[17600]['path']).convert('RGB')
    role = find_mask(font, 'First Mate', shot, (80, 58, 255, 79))
    name = find_mask(font, 'Gerhard Ardelknatts', shot, (80, 20, 255, 55))
    rom = NdsImage.open(ROM)
    batch = read('translations/person_info_graphics_v3.json')
    asset = PxlImage.from_bytes(rom.read_file(batch['file_path']))
    plaques = []
    for number in (5200, 17600):
        image = Image.open(frames[number]['path']).convert('RGB')
        for row in batch['records']:
            left, top, right, bottom = row['plaque_box']
            for y in range(top, bottom):
                for x in range(left, right):
                    assert native5(image.getpixel((x, y))) == native5(asset.palette[asset.indices[y * asset.width + x]])
            plaques.append({'frame': number, 'English': row['text'], 'bounds': row['plaque_box'],
                            'all_pixels_exact': True, 'fully_completed': False})
    original = next(row for row in previous['frames_captured'] if row['frame'] == 17600)
    assert sha(Path(original['path']).read_bytes()) == original['PNG_sha256']
    old = Image.open(original['path']).convert('RGB')
    changed = [(x, y) for y in range(384) for x in range(256) if old.getpixel((x, y)) != shot.getpixel((x, y))]
    assert changed and all(80 <= x < 180 and 58 <= y < 79 for x, y in changed)
    proof.update({'actual_cold_boot_role_display_pending': False, 'actual_First_Mate_mask': role,
                  'actual_Gerhard_complete_name': name, 'actual_20_plaque_instances': plaques,
                  'all_other_pixels_of_same_Gerhard_screen_exact': True,
                  'changed_role_pixels': len(changed), 'capture_report': str(report_path),
                  'capture_report_sha256': sha(report_path.read_bytes()),
                  'source_save_sha256': sha(DONOR.read_bytes()), 'source_save_unchanged': True,
                  'source_save_provenance_unknown': True, 'no_historical_progress_legitimacy_claim': True,
                  'ordinary_Hodram_Stockholm_Continue_Guild_and_Sailor_Info_inputs': True,
                  'observed_Guild_stock': ['Snow-Silk Robe', 'Supreme Loupe', 'map'],
                  'Supreme_Loupe_gift_purchase_not_weapon_or_armor_credit': True,
                  'actual_occupied_Weapon_Armor_and_Auto_Move_still_open': True,
                  'all18_plaques_and_variants_remain_incomplete': True,
                  'low_resolution_Online_images_exempt': True,
                  'documentation': 'docs/crew_roles_v326.md'})
    fresh_new_game(proof)
    for filename in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / filename
        audit = read(path)
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        for entry in audit['plaque_style_v247']['ongoing_plaque_inventory']:
            assert not entry['fully_completed']
            for variant in entry.get('observed_variants', []):
                assert not variant['fully_completed']
        audit['shared_crew_role_labels_v326'] = {**proof, 'proof': str(ROOT / 'release_proof.json')}
        audit['latest_candidate'], audit['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        audit['current_goal_turn_classification'] = 'progress-shared16-crew-role-table-English-and-actual-First-Mate'
        path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    proof_path = ROOT / 'release_proof.json'
    if args.live:
        proof = read(proof_path)
        live(proof)
    else:
        parent, current, clean, canonical = [NdsImage.open(p) for p in (
            PARENT, ROM, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
        before = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
        after = {p: data for _, p, data in current.iter_files()} | dict(current.iter_components())
        assert before.keys() == after.keys()
        assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
        target, plan = apply_release(before['/__arm9__.bin'], clean.read_file('/__arm9__.bin'),
                                     canonical.read_file('/__arm9__.bin'), CONFIG)
        assert target == after['/__arm9__.bin'] == (ROOT / 'research_arm9.bin').read_bytes()
        assert (ROOT / 'v324_reproduction.nds').read_bytes() == PARENT.read_bytes()
        old, new = read(PARENT.with_suffix('.manifest.json')), read(ROM.with_suffix('.manifest.json'))
        assert new['candidate_sha256'] == sha(ROM.read_bytes()) and new['profile'] == 'all-routes-unified-v326'
        assert new['batches'] == old['batches'] and len(new['batches']) == 470
        assert new['required_batches'] == old['required_batches'] and all(new['checks'].values())
        assert new['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
        for path, ids in old['changed_records'].items():
            assert set(ids) <= set(new['changed_records'][path])
        patch = ROM.with_suffix('.xdelta')
        restored = ROOT / 'exact_patch_reconstruction.nds'
        make_xdelta(Path('work/clean.nds'), ROM, patch)
        apply_xdelta(Path('work/clean.nds'), patch, restored)
        assert restored.read_bytes() == ROM.read_bytes()
        proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
                 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
                 'profile': new['profile'], 'canonical_base': new['base_rom'], 'canonical_sha256': new['base_sha256'],
                 'all470_inherited_batches_and_required_layers_retained': True,
                 'full_V324_builder_reproduction_exact': True,
                 'only_one_role_table_address_literal_changes': True,
                 'all_existing_strings_pool_boot_cache_fonts_graphics_routes_and_other_components_exact': True,
                 'exact_clean_patch_reconstruction': True, 'change': plan,
                 'actual_cold_boot_role_display_pending': True,
                 'experimental_user_acceptance_pending': True, 'full_goal_complete': False}
        previous = read('work/emulation_v193/existing_save_v325/capture_report.json')
        (ROOT / 'saved_inputs.json').write_text(json.dumps(previous['scripted_input_schedule'], indent=2) + '\n', encoding='utf-8')
    proof_path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: proof[k] for k in ('candidate_sha256', 'patch_sha256', 'profile', 'actual_cold_boot_role_display_pending')}))


if __name__ == '__main__':
    main()
