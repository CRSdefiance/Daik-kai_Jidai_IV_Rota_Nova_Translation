"""Check cumulative V366 integration, clean patch and final-candidate replays."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/equipment_release_v366')
ROM = Path('out/all_routes_combined_v366_candidate.nds')


def files(image):
    return {n: d for _, n, d in image.iter_files()} | dict(image.iter_components())


def frame_match(old_path, new_path, digest):
    old = json.loads((old_path / 'capture_report.json').read_text())
    new = json.loads((new_path / 'capture_report.json').read_text())
    assert new['ROM_sha256'] == digest and new['cold_boot'] and not new['savestate_loaded']
    before = {r['frame']: r for r in old['frames_captured']}
    after = {r['frame']: r for r in new['frames_captured']}
    assert before.keys() == after.keys()
    assert all(Image.open(before[f]['path']).tobytes() == Image.open(after[f]['path']).tobytes() for f in after)
    return len(after)


def main():
    manifest = json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    parent = json.loads(Path('out/all_routes_combined_v360_candidate.manifest.json').read_text(encoding='utf-8'))
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest
    assert manifest['profile'] == 'all-routes-unified-v366'
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    assert manifest['base_sha256'] == parent['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    stack = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    previous, current = stack['profiles']['all-routes-unified-v360'], stack['profiles']['all-routes-unified-v366']
    assert all(current[k] == v for k, v in previous.items() if k not in ('note', 'description'))
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    old, new = files(NdsImage.open('out/all_routes_combined_v360_candidate.nds')), files(NdsImage.open(ROM))
    assert [n for n in old if old[n] != new[n]] == ['/__arm9__.bin']
    assert new['/__arm9__.bin'] == Path('work/analysis/equipment_wrap_v365/research_arm9.bin').read_bytes()
    assert (ROOT / 'patch_reconstruction.nds').read_bytes() == ROM.read_bytes()
    for caption in (b'Continue', b'New Game', b'Options', b'Grand Race', b'Extras', b'Gallery'):
        assert caption in new['/__arm9__.bin']
    long_frames = frame_match(Path('work/emulation_v193/equipment_long_v365'),
                              Path('work/emulation_v193/equipment_long_v366'), digest)
    start_frames = frame_match(Path('work/emulation_v193/commodity_new_game_v360'),
                               Path('work/emulation_v193/equipment_new_game_v366'), digest)
    campaign = json.loads(Path('translations/graphics_completion_campaign_v1.json').read_text(encoding='utf-8'))
    plaques = campaign['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()),
             'exact_clean_patch_reconstruction': True,
             'all470_batches_and_all_V360_stages_retained': True,
             'only_ARM9_changed_from_V360_all_route_graphics_and_COMMON_files_exact': True,
             'final_candidate_ordinary_long_equipment_replay_exact_frames': long_frames,
             'final_candidate_New_Game_replay_exact_frames': start_frames,
             'all18_plaques_incomplete': True, 'status': 'experimental',
             'canonical_promotion': False, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(f'V366: all470 batches/stages, exact clean patch, {long_frames} ordinary equipment and{start_frames} New Game frames verified.')


if __name__ == '__main__':
    main()
