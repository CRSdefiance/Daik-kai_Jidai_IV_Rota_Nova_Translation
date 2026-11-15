"""Final combined release, complete live English clue and inherited preservation."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.tavern_address_release import apply_release
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text
from scripts.verify_fleet_release_v375 import files

ROM = Path('out/all_routes_combined_v414_candidate.nds')
PARENT = Path('out/all_routes_combined_v408_candidate.nds')
ROOT = Path('work/analysis/tavern_addresses_release_v414')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def captures(name, digest):
    path = Path('work/emulation_v193') / name / 'capture_report.json'
    r = read(path)
    assert r['ROM_sha256'] == digest and r['cold_boot']
    assert not r['savestate_loaded'] and not r['callback_errors']
    frames = {}
    for row in r['frames_captured']:
        p = Path(row['path'])
        assert sha(p.read_bytes()) == row['PNG_sha256']
        if 'cold_boot' in p.name:
            frames[row['frame']] = p
    return path, r, frames


def main():
    digest = sha(ROM.read_bytes())
    m = read(ROM.with_suffix('.manifest.json'))
    pm = read(PARENT.with_suffix('.manifest.json'))
    assert m['candidate_sha256'] == digest and m['profile'] == 'all-routes-unified-v414'
    assert m['base_sha256'] == pm['base_sha256']
    assert m['batches'] == pm['batches'] and len(m['batches']) == 470
    assert m['required_batches'] == pm['required_batches'] and all(m['checks'].values())
    stack = read(Path('translations/release_stack.json'))
    assert m['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert all(stack['profiles'][m['profile']][k] == v for k, v in
               stack['profiles']['all-routes-unified-v408'].items() if k not in ('description', 'note'))
    a, b = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert a.keys() == b.keys()
    assert sorted(k for k in a if a[k] != b[k]) == ['/COMMON/MESFILE.DK4', '/__arm9__.bin']
    common, arm, change = apply_release(a['/COMMON/MESFILE.DK4'], a['/__arm9__.bin'], 'translations/tavern_addresses_v1.json')
    assert common == b['/COMMON/MESFILE.DK4'] and arm == b['/__arm9__.bin']
    assert (ROOT / 'patch_reconstruction.nds').read_bytes() == ROM.read_bytes()
    parent_path, old, of = captures('eligible_tavern_v410', sha(PARENT.read_bytes()))
    current_path, current, cf = captures('tavern_addresses_final_v414', digest)
    assert old['scripted_input_schedule'] == current['scripted_input_schedule']
    assert old['battery_save_preloaded']['source_sha256'] == current['battery_save_preloaded']['source_sha256']
    exact, changed = [], []
    for f in cf:
        if cf[f].read_bytes() == of[f].read_bytes():
            exact.append(f)
            continue
        x, y = Image.open(of[f]).convert('RGB'), Image.open(cf[f]).convert('RGB')
        delta = [(xx, yy) for yy in range(384) for xx in range(256)
                 if x.getpixel((xx, yy)) != y.getpixel((xx, yy))]
        assert all(8 <= xx < 252 and 292 <= yy < 365 for xx, yy in delta), f
        changed.append({'frame': f, 'changed_body_pixels': len(delta)})
    font = GameAsciiFont.from_arm9(arm)
    clue = Image.open(cf[12800]).convert('RGB')
    lines = ['Sir, here\'s a tip: the rare', 'treasure Blue Oak Shield is said to', 'be hidden in N. Sea.']
    masks = [dark_text(font, text, clue, (8, y - 4, 252, y + 15))
             for text, y in zip(lines, (296, 312, 328))]
    assert all(x['bounds'][0] == 22 for x in masks)
    order = dark_text(font, 'Drinks for everyone!', Image.open(cf[11600]).convert('RGB'), (8, 292, 252, 320))
    p, prior_game, pg = captures('local_reputation_new_game_v408_ready', sha(PARENT.read_bytes()))
    q, game, gf = captures('tavern_addresses_new_game_v414', digest)
    assert pg.keys() == gf.keys() and prior_game['scripted_input_schedule'] == game['scripted_input_schedule']
    for f in gf:
        assert gf[f].read_bytes() == pg[f].read_bytes()
    assert len(gf) == 23
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': m['profile'],
             'base_rom': m['base_rom'], 'base_sha256': m['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()), 'exact_clean_patch_reconstruction': True,
             'all470_batches_and_every_V408_stage_retained': True,
             'all_graphics_routes_HELP_ARM7_and_other_components_exact': True,
             'native_proof': 'work/analysis/tavern_addresses_v413/native_proof.json',
             'parent_report': str(parent_path), 'actual_report': str(current_path),
             'actual_report_sha256': sha(current_path.read_bytes()),
             'actual_complete_English_clue_masks': masks, 'all_three_actual_line_origins22': True,
             'actual_natural_order_mask': order, 'unchanged_genuine_frames': exact,
             'body_only_changed_frames': changed, 'all23_New_Game_frames_exact': True,
             'New_Game_report': str(q), 'parent_New_Game_report': str(p), 'change': change,
             'all18_plaques_incomplete': True, 'armor_acquired': False,
             'status': 'experimental', 'canonical_promotion': False, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'V414: complete English aligned clue/order, {len(exact)} unchanged genuine frames, '
          'all23 New Game frames, full inherited stack and exact patch pass.')


if __name__ == '__main__':
    main()
