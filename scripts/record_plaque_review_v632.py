"""Archive current review sheets, preserve18 open items, save guide candidates."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.review_current_plaques_v632 import CAP, ROM, ROOT, SOURCE
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/plaque_review_v632_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V632 Plaques')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V627 Plaques')
KEY = 'fresh_V627_all18_original_plaque_review_packet_v632'


def main():
    proof_path = ROOT / 'current_plaque_review_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/review_current_plaques_v632.py').read_bytes())
    assert len(proof['all18_current_native_review_entries']) == 18
    assert all(r['fully_completed'] is False for r in proof['all18_current_native_review_entries'])
    assert len(proof['all17_independent_complete_font_masks']) == 17
    assert sha(ROM.with_suffix('.xdelta').read_bytes()) == 'fb4b3acb17f69174a53759c8ab74053737eade38c11d5cdee6c7d0afe3062966'
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    for source in (DOC, Path(__file__), Path('scripts/review_current_plaques_v632.py'), proof_path,
                   ROM.with_suffix('.manifest.json')):
        checked_copy(source, ARCHIVE / source.name)
    for source in ROOT.glob('*.png'):
        checked_copy(source, ARCHIVE / source.name)
    archived, guide_shots = [], []
    for label, folder in (('ORIGINAL_JAPANESE_V574', SOURCE), ('V627_ENGLISH', CAP)):
        report_path = folder / 'capture_report.json'
        report = read(report_path)
        checked_copy(report_path, ARCHIVE / (label + '_capture_report.json'))
        shots = {s['frame']: s for s in report['frames_captured']}
        for frame in (4300, 6300, 6700, 7100):
            shot = shots[frame]
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(shot['path'], target)
            record = {'path': str(target), 'sha256': shot['PNG_sha256'], 'frame': frame,
                      'ROM_sha256': report['ROM_sha256'], 'unmodified_capture': True,
                      'historical_source_run': label.startswith('ORIGINAL'),
                      'no_synthetic_RAM_ROM_or_inventory_fixtures': True}
            archived.append(record)
            if label == 'V627_ENGLISH':
                guide_target = GUIDE / f'V627_{frame:06d}_UNMODIFIED_NATIVE.png'
                checked_copy(shot['path'], guide_target)
                guide_shots.append({**record, 'path': str(guide_target)})
    save(GUIDE / 'provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'screenshots': guide_shots,
        'source_report': str(CAP / 'capture_report.json'), 'source_report_sha256': proof['new_current_capture_report_sha256'],
        'ordinary_saved_game_UI_not_new_acquisition_or_pristine_New_Game': True,
        'publication_approved': False, 'user_visual_review_pending': True})
    save(ARCHIVE / 'provenance.json', {
        'verification_checkpoint': 'V632', 'candidate_sha256': proof['candidate_sha256'],
        'screenshots': archived, 'current_run_new_original_run_historical': True,
        'two_review_sheets_and36_native_crops_separately_labeled': True,
        'user_visual_review_pending': True, 'all18_original_entries_incomplete': True,
        'publication_approved': False, 'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'status': 'current_all18_native_packet_verified_user_review_pending_all_entries_open',
        'fresh7100_frame_ordinary_saved_game_UI_no_synthetic_fixtures': True,
        'all17_complete_font_masks_and14272_material_bevel_letter_pixels_exact': True,
        'three_complete_hint_planes3552_pixels_exact_current_V581_tile': True,
        'original_source_runtime_stat_labels_and_header_shown_honestly': True,
        'wood_restoration_uncertainty_retained_not_hidden_pixel_recovery_claimed': True,
        'two_source_current_sheets_all18_reviewable': True, 'user_visual_review_pending': True,
        'all18_original_plaques_incomplete_all22_historical_objects_retained': True,
        'broader_context_and_graphics_material_gates_open': True,
        'archive': str(ARCHIVE), 'guide_candidate_archive': str(GUIDE),
        'unmodified_current_screenshots': 4, 'unmodified_original_screenshots': 4,
        'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        before = data.copy()
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in before.items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V632: fresh V627 all18 plaque review packet and guide candidates'
    text = '''

A new7100-frame ordinary saved-game cold boot repeats the original14-action
plaque schedule without fixtures. All17 complete font masks and14272 static
material/bevel/letter pixels pass. Three complete Equipped Items/Weapon/Blue Oak
Shield planes match3552 pixels using the corrected V581 tile. Actual original
Japanese runtime stat labels and header are paired with current V627 captures
in two4x review sheets. Wording/context retained;hidden grain remains documented
reconstruction. All18 entries stay incomplete;user material/border review remains
pending rather than inferred from tests. Eight current/original full captures,
36 native crops,sheets and proof archived on E;four ordinary current screens also
saved as guide candidates with provenance. No ROM,patch,registry or release
pointer changes. All22 historical scopes/other audit entries exact;broader
graphics and variants remain open. Full goal active. See
[V632 checkpoint](plaque_review_v632_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print('V632:2 sheets/36 crops/8 native screenshots archived;4 guide candidates;three audits updated;all18/22 scopes open and exact.')


if __name__ == '__main__':
    main()
