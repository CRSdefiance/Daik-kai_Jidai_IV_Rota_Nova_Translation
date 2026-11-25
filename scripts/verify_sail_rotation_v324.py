"""Verify the complete Rotate candidate, patch and actual cold-boot captions."""

import argparse
import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sail_rotation_caption import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_sail_rotation_v324 import CONFIG, ROOT
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v324_candidate.nds')
PARENT = Path('out/all_routes_combined_v322_candidate.nds')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def live(proof):
    report_path = Path('work/emulation_v193/sail_rotation_v324/capture_report.json')
    report = read(report_path)
    assert report['ROM_sha256'] == proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 31200
    assert report['scripted_input_schedule'] == read('work/analysis/sea_inspect_v322/cold_boot_inputs.json')
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        frames[row['frame']] = row
    font = GameAsciiFont.from_arm9((ROOT / 'research_arm9.bin').read_bytes())
    captions = []
    for number in (30400, 30800):
        image = Image.open(frames[number]['path']).convert('RGB')
        for text, region in [('Rotate', (15, 366, 88, 384)), ('Inspect', (110, 366, 199, 384)),
                             ('Sails', (198, 366, 256, 384))]:
            captions.append({'frame': number, **find_mask(font, text, image, region)})
    info = Image.open(frames[31200]['path']).convert('RGB')
    instructions = [find_mask(font, 'Info Mode', info, (0, 0, 256, 25)),
                    find_mask(font, 'View information about the cities and', info, (0, 25, 256, 49)),
                    find_mask(font, 'ships on screen. Select a target.', info, (0, 40, 256, 70))]
    parent_report = read('work/emulation_v193/sea_inspect_v322/capture_report.json')
    assert parent_report['ROM_sha256'] == sha(PARENT.read_bytes())
    static = []
    for number in (1200, 2000, 10800, 14400):
        original = next(row for row in parent_report['frames_captured'] if row['frame'] == number)
        assert sha(Path(original['path']).read_bytes()) == original['PNG_sha256']
        assert Image.open(frames[number]['path']).tobytes() == Image.open(original['path']).tobytes()
        static.append(number)
    proof.update({'actual_cold_boot_display_pending': False,
                  'actual_complete_Rotate_Inspect_Sails_masks': captions,
                  'Info_Mode_complete_heading_and_instructions': instructions,
                  'unchanged_title_character_opening_recruitment_frames': static,
                  'actual_New_Game_opening_town_and_sailing_exercised': True,
                  'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes()),
                  'animated_sailing_frames_not_claimed_source_identical': True,
                  'all18_plaque_entries_and_Armor_Weapon_variants_remain_incomplete': True,
                  'low_resolution_Online_images_exempt': True,
                  'documentation': 'docs/sail_rotation_v324.md'})
    for name in ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json'):
        path = Path('translations') / name
        audit = read(path)
        assert not audit['user_scope_exceptions']['low_resolution_online_images']['translation_required']
        for entry in audit['plaque_style_v247']['ongoing_plaque_inventory']:
            assert not entry['fully_completed']
            for variant in entry.get('observed_variants', []):
                assert not variant['fully_completed']
        audit['sail_rotation_caption_v324'] = {**proof, 'proof': str(ROOT / 'release_proof.json')}
        audit['latest_candidate'], audit['latest_candidate_sha256'] = str(ROM), proof['candidate_sha256']
        audit['current_goal_turn_classification'] = 'progress-source-faithful-Rotate-caption-integrated-and-live-verified'
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
        before = {p: raw for _, p, raw in parent.iter_files()} | dict(parent.iter_components())
        after = {p: raw for _, p, raw in current.iter_files()} | dict(current.iter_components())
        assert before.keys() == after.keys()
        assert [p for p in before if before[p] != after[p]] == ['/__arm9__.bin']
        target, plan = apply_release(before['/__arm9__.bin'], clean.read_file('/__arm9__.bin'),
                                     canonical.read_file('/__arm9__.bin'), CONFIG)
        assert target == after['/__arm9__.bin'] == (ROOT / 'research_arm9.bin').read_bytes()
        assert (ROOT / 'v322_reproduction.nds').read_bytes() == PARENT.read_bytes()
        old, new = read(PARENT.with_suffix('.manifest.json')), read(ROM.with_suffix('.manifest.json'))
        assert new['candidate_sha256'] == sha(ROM.read_bytes())
        assert new['profile'] == 'all-routes-unified-v324' and all(new['checks'].values())
        assert old['batches'] == new['batches'] and len(new['batches']) == 470
        assert old['required_batches'] == new['required_batches']
        assert new['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
        for path, ids in old['changed_records'].items():
            assert set(ids) <= set(new['changed_records'][path])
        for name in ('arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode',
                     'arm9RamAddress', 'arm9EntryAddress', 'arm7RamAddress', 'arm7EntryAddress'):
            assert getattr(parent.rom, name) == getattr(current.rom, name)
        patch = ROM.with_suffix('.xdelta')
        reconstructed = ROOT / 'exact_patch_reconstruction.nds'
        make_xdelta(Path('work/clean.nds'), ROM, patch)
        apply_xdelta(Path('work/clean.nds'), patch, reconstructed)
        assert reconstructed.read_bytes() == ROM.read_bytes()
        proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
                 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
                 'canonical_base': new['base_rom'], 'canonical_sha256': new['base_sha256'],
                 'profile': new['profile'], 'all470_inherited_batches_and_required_layers_retained': True,
                 'full_V322_builder_reproduction_exact': True,
                 'only_original8_byte_rotation_caption_changes': True,
                 'all_other_graphics_code_routes_COMMON_HELP_fonts_pointers_and_components_exact': True,
                 'exact_clean_patch_reconstruction': True, 'change': plan,
                 'actual_cold_boot_display_pending': True,
                 'experimental_user_acceptance_pending': True, 'full_goal_complete': False}
    proof_path.write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: proof[k] for k in ('candidate_sha256', 'patch_sha256', 'profile',
                                          'actual_cold_boot_display_pending')}))


if __name__ == '__main__':
    main()
