"""Verify the complete shared heading in native previews and actual ROM captures."""

from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.ship_info_title_crop import apply_release
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ship_title_v633')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
ROM = Path('out/all_routes_combined_v633_candidate.nds')


def receipt(name, frames, digest=None):
    path = CAP / name / 'capture_report.json'
    run = read(path)
    assert run['frames'] == frames and run['cold_boot'] and not run['savestate_loaded']
    assert not run['callback_errors']
    assert not any(v for k, v in run.items() if k.startswith('synthetic_'))
    if digest:
        assert run['ROM_sha256'] == digest
    donor = run.get('battery_save_preloaded')
    if donor:
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    shots = {r['frame']: r for r in run['frames_captured']}
    for shot in shots.values():
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    return run, shots, {'path': str(path), 'sha256': sha(path.read_bytes())}


def compare_title(old_shot, new_shot, font, text, old_x, old_text):
    old = Image.open(old_shot['path']).convert('RGB')
    new = Image.open(new_shot['path']).convert('RGB')
    expected = {(95 + n * 6 + x, 2 + y) for n, char in enumerate(text)
                for y in range(11) for x in range(6) if font.decode(char).getpixel((x, y))}
    actual = {(x, y) for y in range(2, 14) for x in range(1, 255)
              if new.getpixel((x, y)) == (230, 230, 230)}
    assert actual == expected
    old_expected = {(old_x + n * 6 + x, 2 + y) for n, char in enumerate(old_text)
                    for y in range(11) for x in range(6) if font.decode(char).getpixel((x, y))
                    and old_x + n * 6 + x < 152}
    old_actual = {(x, y) for y in range(2, 14) for x in range(1, 255)
                  if old.getpixel((x, y)) == (230, 230, 230)}
    assert old_actual == old_expected
    differences = {(x, y) for y in range(384) for x in range(256)
                   if old.getpixel((x, y)) != new.getpixel((x, y))}
    assert differences <= expected | old_expected
    # A complete-mask test must reject loss of either word end.
    ink_x = sorted({x for x, _ in expected})
    for edge in (ink_x[0], ink_x[-1]):
        assert {p for p in actual if p[0] != edge} != expected
    return {'complete_current_ink': len(actual), 'old_visible_ink': len(old_actual),
            'changed_pixels': len(differences), 'only_old_new_title_ink_changes': True,
            'every_other_screen_pixel_exact': True, 'missing_first_final_columns_rejected': True}


def main():
    rom, parent = NdsImage.open(ROM), NdsImage.open('out/all_routes_combined_v627_candidate.nds')
    digest, parent_digest = sha(ROM.read_bytes()), sha(parent.source.read_bytes())
    arm, native = apply_release(parent.read_file('/__arm9__.bin'), 'translations/ship_info_title_crop_v1.json')
    assert arm == rom.read_file('/__arm9__.bin')
    before = {p: d for _, p, d in parent.iter_files()} | dict(parent.iter_components())
    after = {p: d for _, p, d in rom.iter_files()} | dict(rom.iter_components())
    assert before.keys() == after.keys()
    assert {p for p in before if before[p] != after[p]} == {'/__arm9__.bin'}
    manifest, prior = read(ROM.with_suffix('.manifest.json')), read(parent.source.with_suffix('.manifest.json'))
    registry = read('translations/release_stack.json')
    assert manifest['candidate_sha256'] == digest and manifest['base_sha256'] == registry['canonical_baseline']['sha256']
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['profile'] == 'all-routes-unified-v633' and all(manifest['checks'].values())
    assert manifest['batches'] == prior['batches'] and len(manifest['batches']) == 470
    assert len(registry['accepted_layers']) == 114
    font = GameAsciiFont.from_arm9(arm)
    old, os, old_receipt = receipt('selection_consumers_v633_current', 5600, parent_digest)
    new, ns, new_receipt = receipt('ship_title_v633_selection_actual', 5600, digest)
    assert old['scripted_input_schedule'] == new['scripted_input_schedule'] and os.keys() == ns.keys()
    ship = compare_title(os[5600], ns[5600], font, ' Ship Info ', 104, ' Ship Info ')
    assert ship['complete_current_ink'] == 98 and ship['old_visible_ink'] == 74
    equal = []
    for frame in sorted(set(os) - {5600}):
        assert Image.open(os[frame]['path']).tobytes() == Image.open(ns[frame]['path']).tobytes()
        equal.append(frame)
    old_market, ms, market_old_receipt = receipt('tavern_recruitment_v627_market', 24100, parent_digest)
    new_market, cs, market_receipt = receipt('ship_title_v633_market', 24100, digest)
    assert 'battery_save_preloaded' not in new_market
    assert ms.keys() == cs.keys() and len(ms) == 19
    assert old_market['scripted_input_schedule'] == new_market['scripted_input_schedule']
    for frame in ms:
        assert Image.open(ms[frame]['path']).tobytes() == Image.open(cs[frame]['path']).tobytes()
    preservation, patch = read(ROOT / 'preservation_proof.json'), read(ROOT / 'patch_proof.json')
    assert preservation['candidate_sha256'] == patch['candidate_sha256'] == digest
    assert preservation['current921_format_palette_extent_checks'] and preservation['all57_embedded_block_extents_exact']
    assert patch['exact_all_byte_reconstruction']
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': patch['patch_sha256'], 'native': native, 'actual_complete_Ship_Info': ship,
             'other_ship_selection_frames_exact_V627': equal,
             'ordinary_no_save_no_fixture_New_Game_story_town_Market_frames_exact_V627': sorted(ms),
             'all_other_ROM_files_and_components_exact_V627': True,
             'all470_batches114_accepted_layers921_graphics57_embedded_extents_retained': True,
             'reports': [old_receipt, new_receipt, market_old_receipt, market_receipt],
             'Refit_actual_context_still_pending': True,
             'all18_plaques_incomplete_all22_historical_scopes_retained': True,
             'full_goal_complete': False, 'canonical_promoted': False,
             'script_sha256': sha(Path(__file__).read_bytes())}
    refit_old = CAP / 'ship_title_v633_shipyard_control' / 'capture_report.json'
    refit_new = CAP / 'ship_title_v633_refit_actual' / 'capture_report.json'
    if refit_old.exists() and refit_new.exists():
        control = read(refit_old)
        r_old, ro, rr_old = receipt('ship_title_v633_shipyard_control', control['frames'], parent_digest)
        r_new, rn, rr_new = receipt('ship_title_v633_refit_actual', control['frames'], digest)
        assert r_old['scripted_input_schedule'] == r_new['scripted_input_schedule']
        anchors = read(ROOT / 'refit_anchors.json')
        title_cases = {}
        for frame in anchors['title_frames']:
            title_cases[frame] = compare_title(ro[frame], rn[frame], font, '   Refit   ', 104, 'Refit')
            assert title_cases[frame]['complete_current_ink'] == 65
        unchanged = []
        for frame in sorted(set(ro) & set(rn) - set(anchors['title_frames'])):
            assert Image.open(ro[frame]['path']).tobytes() == Image.open(rn[frame]['path']).tobytes()
            unchanged.append(frame)
        proof.update({'Refit_actual_context_still_pending': False, 'actual_Refit_titles': title_cases,
                      'Refit_unchanged_other_frames': unchanged})
        proof['reports'].extend([rr_old, rr_new])
    save(ROOT / 'release_proof.json', proof)
    print('Complete actual Ship Info, exact other screens,19 ordinary regressions,full stack and patch pass;Refit pending:',
          proof['Refit_actual_context_still_pending'])


if __name__ == '__main__':
    main()
