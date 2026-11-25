"""Registered full release, complete live rumor, preservation and exact patch."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.local_reputation_rumors import apply_release
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text
from scripts.verify_fleet_release_v375 import files

ROM = Path('out/all_routes_combined_v408_candidate.nds')
PARENT = Path('out/all_routes_combined_v388_candidate.nds')
ROOT = Path('work/analysis/local_reputation_release_v408')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def capture(folder, digest):
    path = folder / 'capture_report.json'
    report = read(path)
    assert report['ROM_sha256'] == digest and report['cold_boot']
    assert not report['savestate_loaded'] and not report['callback_errors']
    frames = {}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        if 'cold_boot' in row['path']:
            frames[row['frame']] = Path(row['path'])
    return path, report, frames


def main():
    digest = sha(ROM.read_bytes())
    manifest = read(ROM.with_suffix('.manifest.json'))
    parent_manifest = read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v408'
    assert manifest['batches'] == parent_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent_manifest['required_batches'] and all(manifest['checks'].values())
    assert manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    stack = read(Path('translations/release_stack.json'))
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    before_profile = stack['profiles']['all-routes-unified-v388']
    after_profile = stack['profiles'][manifest['profile']]
    assert all(after_profile[k] == v for k, v in before_profile.items() if k not in ('description', 'note'))
    a, b = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert a.keys() == b.keys()
    assert sorted(k for k in a if a[k] != b[k]) == ['/COMMON/MESFILE.DK4', '/__arm9__.bin']
    common, arm, change = apply_release(a['/COMMON/MESFILE.DK4'], a['/__arm9__.bin'],
                                      'translations/local_reputation_rumors_v1.json')
    assert b['/COMMON/MESFILE.DK4'] == common and b['/__arm9__.bin'] == arm
    assert (ROOT / 'patch_reconstruction.nds').read_bytes() == ROM.read_bytes()
    old_path, old, of = capture(Path('work/emulation_v193/tavern_clues_v403'), sha(PARENT.read_bytes()))
    new_path, new, nf = capture(Path('work/emulation_v193/local_reputation_final_v408_ready'), digest)
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert new['battery_save_preloaded']['source_sha256'] == old['battery_save_preloaded']['source_sha256']
    exact, changed = [], []
    for f in nf:
        if nf[f].read_bytes() == of[f].read_bytes():
            exact.append(f)
        else:
            x, y = Image.open(of[f]).convert('RGB'), Image.open(nf[f]).convert('RGB')
            delta = [(xx, yy) for yy in range(384) for xx in range(256)
                     if x.getpixel((xx, yy)) != y.getpixel((xx, yy))]
            assert f == 20400 and all(8 <= xx < 252 and 292 <= yy < 365 for xx, yy in delta)
            changed.append({'frame': f, 'changed_body_pixels': len(delta)})
    assert changed
    font = GameAsciiFont.from_arm9(arm)
    picture = Image.open(nf[20400]).convert('RGB')
    masks = [dark_text(font, 'Argot of Amsterdam is an', picture, (8, 292, 252, 312)),
             dark_text(font, 'influential local Trader.', picture, (8, 310, 252, 338))]
    assert all(m['bounds'][0] == 22 for m in masks)
    p, old_game, og = capture(Path('work/emulation_v193/conditions_new_game_v388'), sha(PARENT.read_bytes()))
    q, new_game, ng = capture(Path('work/emulation_v193/local_reputation_new_game_v408_ready'), digest)
    assert new_game['scripted_input_schedule'] == old_game['scripted_input_schedule']
    assert og.keys() == ng.keys()
    for f in ng:
        assert ng[f].read_bytes() == og[f].read_bytes()
    assert len(ng) == 23
    plaques = read(Path('translations/graphics_completion_campaign_v1.json'))['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not v['fully_completed'] for v in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base_rom': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()), 'exact_clean_patch_reconstruction': True,
             'all470_batches_and_all_V388_stages_retained': True,
             'all_graphics_routes_HELP_ARM7_overlays_and_other_components_exact': True,
             'native_proof': 'work/analysis/local_reputation_rumors_v404/native_proof.json',
             'actual_rumor_report': str(new_path), 'actual_rumor_report_sha256': sha(new_path.read_bytes()),
             'parent_rumor_report': str(old_path), 'parent_rumor_report_sha256': sha(old_path.read_bytes()),
             'actual_complete_rumor_masks': masks, 'both_actual_lines_left_aligned_at22': True,
             'unchanged_genuine_replay_frames': exact, 'changed_body_only_frames': changed,
             'New_Game_report': str(q), 'all23_New_Game_frames_exact': True,
             'parent_New_Game_report': str(p),
             'change': change, 'status': 'experimental', 'canonical_promotion': False,
             'all18_plaques_incomplete': True, 'weapon_armor_acquired': False, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'V408: complete aligned512-pixel rumor, {len(exact)} unchanged genuine frames, '
          'all23 New Game frames, full inherited stack and exact patch pass.')


if __name__ == '__main__':
    main()
