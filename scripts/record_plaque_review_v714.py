"""Archive the latest18-plaque source review without closing its open gates."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.review_current_plaques_v714 import CAP, ROM, ROOT, SOURCE
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/plaque_review_v714_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V714 Plaques')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V712 Plaques')
KEY = 'current_V712_all18_plaque_material_source_meaning_native_review_v714'
SCRIPTS = ('prepare_plaque_review_v714', 'run_plaque_review_v714', 'review_current_plaques_v714',
           'review_plaque_meanings_v714', 'record_plaque_review_v714', 'verify_plaque_archive_v714')


def main():
    proof_path, matrix_path = ROOT / 'current_plaque_review_proof.json', ROOT / 'terminology_review.json'
    proof, matrix, pre = read(proof_path), read(matrix_path), read(ROOT / 'preflight.json')
    assert proof['candidate_sha256'] == sha(ROM.read_bytes()) == pre['candidate_sha256']
    assert len(matrix['all18_source_context_and_natural_English_decisions']) == 18
    assert proof['script_sha256'] == sha(Path('scripts/review_current_plaques_v714.py').read_bytes())
    assert matrix['verifier_sha256'] == sha(Path('scripts/review_plaque_meanings_v714.py').read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for name in SCRIPTS:
        path = Path('scripts') / (name + '.py')
        copy(path, ARCHIVE / 'sources' / path.name)
    copy(DOC, ARCHIVE / DOC.name)
    for path in ROOT.iterdir():
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.name)
    shots = []
    for label, folder in (('ORIGINAL_JAPANESE', SOURCE), ('V712_ENGLISH', CAP)):
        report = read(folder / 'capture_report.json')
        copy(folder / 'capture_report.json', ARCHIVE / (label + '_capture_report.json'))
        indexed = {r['frame']: r for r in report['frames_captured']}
        for frame in (4300, 6300, 6700, 7100):
            row = indexed[frame]
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            path = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            copy(row['path'], path)
            if label == 'V712_ENGLISH':
                gp = GUIDE / path.name
                copy(path, gp)
                shots.append({'path': str(gp), 'sha256': row['PNG_sha256'], 'frame': frame,
                    'ROM_sha256': report['ROM_sha256'], 'unmodified_capture': True})
    save(GUIDE / 'provenance.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'screenshots': shots, 'source_report': str(CAP / 'capture_report.json'),
        'ordinary_saved_game_UI_no_live_fixtures_not_pristine_New_Game': True,
        'publication_approved': False, 'user_visual_review_pending': True})
    entry = {'documentation': str(DOC), 'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'source_terminology_matrix': str(matrix_path), 'source_terminology_matrix_sha256': sha(matrix_path.read_bytes()),
        'fresh7100_frame_ordinary_current_run_all17_fonts14272_static_pixels_three3552_pixel_hints': True,
        'all_four_full_two_screen_images_exact_to_previous_review': True,
        'all18_meanings_context_and_natural_English_reviewed_no_wording_change_required': True,
        'both_current_source_sheets_visually_reviewed_no_new_block_or_vertical_seam_identified': True,
        'concealed_source_grain_reconstruction_uncertainty_retained': True,
        'material_feedback_requested_no_response_inferred_all18_entries_open': True,
        'new_goal_Online_body_scope_clarification_pending': True,
        'other_graphics_contexts_restoration_older_record_checks_and_final_acceptance_open': True,
        'archive': str(ARCHIVE), 'guide_candidates': str(GUIDE),
        'ROM_patch_registry_release_pointers_canonical_unchanged': True, 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V714: latest V712 plaque material and terminology review'
    text = ('Fresh7100-frame ordinary saved-game UI produces all18 original/current comparisons. '
        'All17 complete fonts,14272 static pixels and three complete3552-pixel hints pass; all four '
        'whole screens match the earlier V666 review. All18 source meanings and contextual English '
        'are reviewed without wording changes. Both current source sheets and native crops inspected; '
        'no new block or vertical seam identified,concealed grain remains reconstruction. Concrete '
        'material feedback requested; acceptance not inferred. All18 plaques stay incomplete and22 '
        'historical requirements exact. New-goal Online screenshot-body scope clarification pending. '
        'Two sheets,36 crops,eight native screenshots and four unmodified guide candidates saved on E '
        'with provenance. Other normal contexts,legacy/comics,restoration,model gaps and final acceptance '
        'remain open;older record checks retained. V712 ROM/patch/registry/pointers/canonical unchanged. '
        'Full goal active. See [V714 checkpoint](plaque_review_v714_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + text, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    copy(CAP / 'run_contract.json', ARCHIVE / 'current_run_contract.json')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'],
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
            if p.is_file() and p.name != 'provenance.json'},
        'four_guide_candidates': str(GUIDE / 'provenance.json'),
        'all18_incomplete22_scopes_retained': True, 'publication_approved': False,
        'user_material_review_pending': True, 'full_goal_complete': False})
    print('V714 archived current18-plaque source/meaning packet,4 guide candidates and additive audit; goal active.', flush=True)


if __name__ == '__main__':
    main()
