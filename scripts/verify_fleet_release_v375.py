"""Exact cumulative inheritance, patch and final-candidate gameplay replays."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/fleet_release_v375')
ROM = Path('out/all_routes_combined_v375_candidate.nds')


def files(image):
    return {n: d for _, n, d in image.iter_files()} | dict(image.iter_components())


def match(old, new, digest):
    before = json.loads((old / 'capture_report.json').read_text())
    after = json.loads((new / 'capture_report.json').read_text())
    assert after['ROM_sha256'] == digest and after['cold_boot'] and not after['savestate_loaded']
    assert not after['callback_errors']
    a = {r['frame']: r for r in before['frames_captured']}
    b = {r['frame']: r for r in after['frames_captured']}
    assert a.keys() == b.keys()
    assert all(Image.open(a[f]['path']).tobytes() == Image.open(b[f]['path']).tobytes() for f in b)
    return len(b)


def main():
    manifest = json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    parent = json.loads(Path('out/all_routes_combined_v366_candidate.manifest.json').read_text(encoding='utf-8'))
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v375'
    assert manifest['base_sha256'] == parent['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    stack = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    old, new = stack['profiles']['all-routes-unified-v366'], stack['profiles']['all-routes-unified-v375']
    assert all(new[k] == v for k, v in old.items() if k not in ('note', 'description'))
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    a, b = files(NdsImage.open('out/all_routes_combined_v366_candidate.nds')), files(NdsImage.open(ROM))
    assert [n for n in a if a[n] != b[n]] == ['/__arm9__.bin']
    assert b['/__arm9__.bin'] == Path('work/analysis/fleet_detail_v374/research_arm9.bin').read_bytes()
    assert (ROOT / 'patch_reconstruction.nds').read_bytes() == ROM.read_bytes()
    captures = {}
    for name, old_name in [('fleet_detail_v375', 'fleet_detail_v374'), ('fleet_sort_v375', 'fleet_sort_v374'),
                           ('fleet_new_game_v375', 'equipment_new_game_v366'), ('fleet_equipment_v375', 'equipment_long_v366')]:
        captures[name] = match(Path('work/emulation_v193') / old_name,
                               Path('work/emulation_v193') / name, digest)
    campaign = json.loads(Path('translations/graphics_completion_campaign_v1.json').read_text(encoding='utf-8'))
    plaques = campaign['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()),
             'all470_batches_and_all_V366_stages_retained': True,
             'only_ARM9_changed_all_other_files_components_and_graphics_exact': True,
             'exact_clean_patch_reconstruction': True, 'actual_exact_final_ROM_replay_frames': captures,
             'actual_evidence': 'work/analysis/fleet_detail_v374/live_proof.json',
             'all18_plaques_incomplete': True, 'older_save_history_unknown': True,
             'normal_equipment_purchase_New_Game_and_saved_fleet_sort_controls_verified': True,
             'weapon_armor_acquired': False, 'status': 'experimental',
             'canonical_promotion': False, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(f'V375: complete inherited stack, exact clean patch and{sum(captures.values())} final-ROM frames pass.')


if __name__ == '__main__':
    main()
