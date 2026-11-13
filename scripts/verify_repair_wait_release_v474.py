"""Registered combined release, actual repair glyphs, matched regressions and patch."""

import json
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.repair_wait_wrap import apply_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text
from scripts.verify_fleet_release_v375 import files

ROOT = Path('work/analysis/repair_wait_v474')
ROM = Path('out/all_routes_combined_v474_candidate.nds')
PARENT = Path('out/all_routes_combined_v468_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def captures(folder, digest):
    path = Path('work/emulation_v193') / folder / 'capture_report.json'
    report = read(path)
    assert report['ROM_sha256'] == digest and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors']
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    if report.get('battery_save_preloaded'):
        donor = report['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    return path, report


def match(before, after):
    a = {r['frame']: r for r in before['frames_captured']}
    b = {r['frame']: r for r in after['frames_captured']}
    assert a.keys() <= b.keys()
    assert before['scripted_input_schedule'] == after['scripted_input_schedule']
    for frame in a:
        assert a[frame]['PNG_sha256'] == b[frame]['PNG_sha256'], frame
    return sorted(a)


def main():
    digest, parent_digest = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    manifest, old_manifest = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v474'
    assert manifest['base_sha256'] == old_manifest['base_sha256']
    assert manifest['batches'] == old_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old_manifest['required_batches'] and all(manifest['checks'].values())
    registry = Path('translations/release_stack.json')
    assert manifest['release_stack_sha256'] == sha(registry.read_bytes())
    profiles = read(registry)['profiles']
    assert all(profiles['all-routes-unified-v474'][k] == v for k, v in profiles['all-routes-unified-v468'].items()
               if k not in ('note', 'description'))
    previous, current = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert previous.keys() == current.keys()
    assert [p for p in previous if previous[p] != current[p]] == ['/__arm9__.bin']
    target, change = apply_release(previous['/__arm9__.bin'], 'translations/repair_wait_wrap_v1.json')
    assert target == current['/__arm9__.bin']
    native = read(ROOT / 'native_proof.json')
    assert native['target_arm9_sha256'] == sha(target)
    old_path, old = captures('repair_replay_v468', parent_digest)
    new_path, new = captures('repair_replay_v474', digest)
    assert old['scripted_input_schedule'] == new['scripted_input_schedule']
    assert old['battery_save_preloaded']['source_sha256'] == new['battery_save_preloaded']['source_sha256']
    a = {r['frame']: r for r in old['frames_captured']}
    b = {r['frame']: r for r in new['frames_captured']}
    assert a.keys() == b.keys()
    matched = []
    for frame in a:
        if frame <= 12700:
            assert a[frame]['PNG_sha256'] == b[frame]['PNG_sha256'], frame
            matched.append(frame)
    before = Image.open(a[13000]['path']).convert('RGB')
    after = Image.open(b[13000]['path']).convert('RGB')
    assert all(before.getpixel((x, y)) == after.getpixel((x, y))
               for y in range(384) for x in range(256) if not (8 <= x < 253 and 292 <= y < 336))
    font = GameAsciiFont.from_arm9(target)
    masks = [dark_text(font, text, after, (8, 292, 253, 350)) for text in
             ['Repairs will take one day. Please', "wait until they're finished."]]
    assert sum(m['ink_pixels'] for m in masks) == native['complete_native_ink_pixels'] == 611
    assert masks[0]['bounds'][:2] == [22, 296] and masks[1]['bounds'][:2] == [22, 312]
    regressions, reports = [], [(old_path, old), (new_path, new)]
    for old_name, new_name in [('crew_columns_v468_rafael', 'repair_regression_crew_v474'),
                              ('crew_columns_v468_newgame', 'repair_regression_newgame_v474')]:
        old_report_path, old_report = captures(old_name, parent_digest)
        new_report_path, new_report = captures(new_name, digest)
        regressions.append({'old': str(old_report_path), 'new': str(new_report_path),
                            'whole_frames_exact': match(old_report, new_report)})
        reports.extend([(old_report_path, old_report), (new_report_path, new_report)])
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    rebuilt = ROOT / 'exact_clean_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, rebuilt)
    assert rebuilt.read_bytes() == ROM.read_bytes()
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
             'parent': str(PARENT), 'parent_sha256': parent_digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'], 'change': change,
             'all470_inherited_batches_and_every_stage_preserved': True,
             'only_declared_ARM9_dispatch_and20_existing_padding_bytes_change': True,
             'all_graphics_palettes_dimensions_borders_ROUTE_COMMON_HELP_payloads_exact': True,
             'native_proof': str(ROOT / 'native_proof.json'),
             'native_proof_sha256': sha((ROOT / 'native_proof.json').read_bytes()),
             'actual_repair_message_complete_masks': masks,
             'all_outside_repair_text_pixels_exact': True, 'matched_pre_repair_frames': matched,
             'earlier_sailor_columns_and_fresh_game_regressions': regressions,
             'reports': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p, _ in reports],
             'exact_clean_patch_reconstruction': True, 'release_status': 'experimental',
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True,
             'hardware_verification': False, 'full_goal_complete': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V474 actual611 repair glyphs and whole-word wrapping;inherited stack,matched screens and exact clean patch pass.')


if __name__ == '__main__':
    main()
