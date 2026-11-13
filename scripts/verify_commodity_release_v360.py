"""Exact integration/patch inheritance and actual final-candidate gameplay evidence."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/commodity_release_v360')
ROM = Path('out/all_routes_combined_v360_candidate.nds')


def files(image):
    return {n: d for _, n, d in image.iter_files()} | dict(image.iter_components())


def main():
    manifest_path = ROM.with_suffix('.manifest.json')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    old = json.loads(Path('out/all_routes_combined_v342_candidate.manifest.json').read_text(encoding='utf-8'))
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256']
    assert manifest['profile'] == 'all-routes-unified-v360'
    assert manifest['batches'] == old['batches'] and len(manifest['batches']) == 470
    assert manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    parent, target = files(NdsImage.open('out/all_routes_combined_v342_candidate.nds')), files(NdsImage.open(ROM))
    assert [n for n in parent if parent[n] != target[n]] == ['/__arm9__.bin']
    assert target['/__arm9__.bin'] == Path('work/analysis/commodity_cargo_v359/research_arm9.bin').read_bytes()
    assert (ROOT / 'patch_reconstruction.nds').read_bytes() == ROM.read_bytes()
    raw_gate = target['/__arm9__.bin'][0x9F068:0x9F06C]
    assert raw_gate == parent['/__arm9__.bin'][0x9F068:0x9F06C]
    for text in [b'Continue', b'New Game', b'Options', b'Grand Race', b'Extras', b'Gallery']:
        assert text in target['/__arm9__.bin']
    capture = Path('work/emulation_v193/commodity_production_cargo_v360')
    report = json.loads((capture / 'capture_report.json').read_text())
    assert report['ROM_sha256'] == manifest['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    identical = 0
    research = Path('work/emulation_v193/commodity_cargo_v359')
    for p in capture.glob('frame_*.png'):
        previous = research / p.name
        if previous.exists():
            assert Image.open(p).tobytes() == Image.open(previous).tobytes(), p
            identical += 1
    new_game = Path('work/emulation_v193/commodity_new_game_v360/capture_report.json')
    fresh = json.loads(new_game.read_text())
    assert fresh['ROM_sha256'] == manifest['candidate_sha256']
    assert fresh['cold_boot'] and not fresh['savestate_loaded'] and not fresh['callback_errors']
    registry = json.loads(Path('translations/release_stack.json').read_text(encoding='utf-8'))
    inherited = registry['profiles']['all-routes-unified-v342']
    current = registry['profiles']['all-routes-unified-v360']
    assert all(current[k] == v for k, v in inherited.items() if k != 'note')
    for p in ['translations/graphics_completion_campaign_v1.json', 'translations/graphics_visual_audit_v150.json']:
        plaques = json.loads(Path(p).read_text(encoding='utf-8'))['plaque_style_v247']['ongoing_plaque_inventory']
        assert len(plaques) == 18 and all(not x['fully_completed'] for x in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': manifest['candidate_sha256'],
             'manifest': str(manifest_path), 'manifest_sha256': sha(manifest_path.read_bytes()),
             'profile': manifest['profile'], 'base_rom': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch': str(ROM.with_suffix('.xdelta')), 'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()),
             'exact_clean_patch_reconstruction': True, 'all470_batches_and_inherited_stages_retained': True,
             'only_ARM9_changed_from_V342': True, 'Maria_unlock_behavior_unchanged_no_stock_substitutions': True,
             'actual_production_genuine_save_town_market_drag_Cargo_frames_exact_research': identical,
             'production_capture_report': str(capture / 'capture_report.json'),
             'production_capture_report_sha256': sha((capture / 'capture_report.json').read_bytes()),
             'exact_production_New_Game_report': str(new_game), 'New_Game_report_sha256': sha(new_game.read_bytes()),
             'planned_trade_not_completed_purchase': True, 'Price_Info_long_name_uses_documented_supplied_label_fixture': True,
             'status': 'experimental', 'canonical_promotion': False, 'all18_plaques_incomplete': True,
             'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(f'V360:470 inherited batches, exact clean patch, normal New Game and{identical} actual town/market/Cargo frames verified.')


if __name__ == '__main__':
    main()
