"""Exact shared-header delta, matched small/large ship pixels and full fresh-game regression."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.crew_column_alignment import POINT, apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/analysis/crew_columns_v468')
ROM = Path('out/all_routes_combined_v468_candidate.nds')
PARENT = Path('out/all_routes_combined_v464_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def captures(name, digest):
    path = Path('work/emulation_v193') / name / 'capture_report.json'
    r = read(path)
    assert r['ROM_sha256'] == digest and r['cold_boot'] and not r['savestate_loaded']
    assert not r['callback_errors']
    for row in r['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return path, r


def main():
    digest, parent_digest = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    manifest, old_manifest = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v468'
    assert manifest['base_sha256'] == old_manifest['base_sha256']
    assert manifest['batches'] == old_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old_manifest['required_batches'] and all(manifest['checks'].values())
    registry = Path('translations/release_stack.json')
    assert manifest['release_stack_sha256'] == sha(registry.read_bytes())
    profiles = read(registry)['profiles']
    assert all(profiles['all-routes-unified-v468'][k] == v for k, v in profiles['all-routes-unified-v464'].items()
               if k not in ('note', 'description'))
    previous, current = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert previous.keys() == current.keys()
    assert [p for p in previous if previous[p] != current[p]] == ['/__arm9__.bin']
    expected, transform = apply_release(previous['/__arm9__.bin'], 'translations/crew_column_alignment_v1.json')
    assert expected == current['/__arm9__.bin']
    assert [n for n, (a, b) in enumerate(zip(previous['/__arm9__.bin'], expected)) if a != b] == [POINT]
    font = GameAsciiFont.from_arm9(expected)
    batch = read(Path('translations/assign_sailors_graphics_v5.json'))
    art = PxlImage.from_bytes(current[batch['file_path']])
    cases, report_proofs = [], []
    for suffix, values in [('london', ('39', '39', '124')), ('rafael', ('9', '16', '24'))]:
        old_path, old = captures(f'crew_columns_v464_{suffix}', parent_digest)
        new_path, new = captures(f'crew_columns_v468_{suffix}', digest)
        assert old['frames'] == new['frames'] == 4200
        assert old['scripted_input_schedule'] == new['scripted_input_schedule']
        assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']
        donor = Path(new['battery_save_preloaded']['source'])
        assert sha(donor.read_bytes()) == new['battery_save_preloaded']['source_sha256']
        before = {r['frame']: r for r in old['frames_captured']}
        after = {r['frame']: r for r in new['frames_captured']}
        matched = []
        for n, row in after.items():
            a, b = [Image.open(Path(item['path'])).convert('RGB') for item in (before[n], row)]
            if n < 4000:
                assert a.tobytes() == b.tobytes()
                matched.append(n)
            else:
                assert all(a.getpixel((x, y)) == b.getpixel((x, y))
                           for y in range(384) for x in range(256) if not (116 <= x < 236 and 192 <= y < 204))
        shot = Image.open(after[4200]['path']).convert('RGB')
        labels = [find_mask(font, text, shot, (100, 188, 255, 212)) for text in ('Need', 'Now', 'Max')]
        assert [m['bounds'] for m in labels] == [[136, 192, 160, 203], [178, 192, 196, 203], [214, 192, 232, 203]]
        numbers = [find_mask(font, value, shot, region) for value, region in zip(values,
                   [(138, 206, 162, 227), (178, 206, 198, 227), (208, 206, 234, 227)])]
        assert [m['bounds'][2] for m in numbers] == [160, 196, 232]
        for row in batch['records']:
            x0, y0, x1, y1 = row['plaque_box']
            assert all(tuple(v // 8 for v in shot.getpixel((x, y))) ==
                       tuple(v // 8 for v in art.palette[art.indices[y * art.width + x]][:3])
                       for y in range(y0, y1) for x in range(x0, x1))
        cases.append({'context': suffix, 'complete_headers': labels, 'complete_number_columns': numbers,
                      'all_seven_full_plaque_regions_exact': True, 'all_pixels_outside_header_region_exact': True,
                      'whole_pre_header_frames_exact': matched})
        report_proofs.extend([{'path': str(p), 'sha256': sha(p.read_bytes())} for p in (old_path, new_path)])
    newgame_path, newgame = captures('crew_columns_v468_newgame', digest)
    old_path, old = captures('skill_terms_v464', parent_digest)
    assert newgame['frames'] == 21200 and newgame.get('battery_save_preloaded') is None
    assert newgame['scripted_input_schedule'] == [e for e in old['scripted_input_schedule'] if e['start'] <= 21001]
    prior = {r['frame']: r for r in old['frames_captured'] if 'cold_boot' in r['path']}
    regression = set()
    for row in newgame['frames_captured']:
        assert row['PNG_sha256'] == prior[row['frame']]['PNG_sha256']
        regression.add(row['frame'])
    assert len(regression) == 56
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    rebuilt = ROOT / 'exact_clean_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
             'parent': str(PARENT), 'parent_sha256': parent_digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'all470_inherited_batches_and_every_stage_preserved': True,
             'only_ARM9_shared_header_origin_byte_changes_from_V464': True,
             'transform': transform, 'matched_actual_small_and_large_ship_cases': cases,
             'report_proofs': report_proofs + [{'path': str(newgame_path), 'sha256': sha(newgame_path.read_bytes())}],
             'all56_actual_title_New_Game_story_town_Help_entry_frames_exact': sorted(regression),
             'exact_clean_patch_reconstruction': True,
             'artwork_palettes_dimensions_borders_and_all_route_HELP_COMMON_payloads_exact': True,
             'all18_plaques_incomplete': True, 'all22_historical_requirements_retained': True,
             'armor_weapon_acquisition_and_other_contexts_remain_open': True,
             'release_status': 'experimental', 'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V468:shared headers/numbers align in both ship sizes;14 complete plaques and56 earlier whole frames exact;full stack and clean patch pass.')


if __name__ == '__main__':
    main()
