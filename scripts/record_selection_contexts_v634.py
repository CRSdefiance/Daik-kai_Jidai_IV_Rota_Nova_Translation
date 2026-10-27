"""Archive new ordinary contexts and add evidence without closing old scopes."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_selection_contexts_v634 import ROOT, SOURCE
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/selection_contexts_v634_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V634 Two ship selection contexts')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V633 Two ship cargo')
KEY = 'ordinary_two_ship_cargo_and_new_bounded_selection_trace_v634'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['script_sha256'] == sha(Path('scripts/verify_selection_contexts_v634.py').read_bytes())
    assert proof['candidate_sha256'] == sha(SOURCE.read_bytes())
    assert not proof['source_tooltip_control_still_pending']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    for source in (DOC, proof_path, ROOT / 'fixture_manifest.json', ROOT / 'ABI_proof.json',
                   ROOT / 'full_inputs.json', ROOT / 'baseline_frame_anchors.json',
                   ROOT / 'ordinary_purchase_funds.json', ROOT / 'diagnostic_limits.json',
                   Path('scripts/prepare_selection_trace_v634.py'),
                   Path('scripts/verify_selection_contexts_v634.py'), Path(__file__)):
        checked_copy(source, ARCHIVE / source.name)
    screenshots, guides = [], []
    for receipt in proof['reports']:
        report_path = Path(receipt['path'])
        assert sha(report_path.read_bytes()) == receipt['sha256']
        run = read(report_path)
        label = report_path.parent.name
        checked_copy(report_path, ARCHIVE / (label + '_capture_report.json'))
        journal = report_path.parent / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        shots = {r['frame']: r for r in run['frames_captured']}
        selected = (19000, 20600, 21800) if label.endswith('_trace') else (
            9400, 19000, 19400, 19800, 20200, 20600, 21000, 21400, 21800, 22200, 22600)
        for frame in selected:
            row = shots[frame]
            target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(row['path'], target)
            record = {'path': str(target), 'frame': frame, 'sha256': row['PNG_sha256'],
                      'ROM_sha256': run['ROM_sha256'], 'unmodified_capture': True,
                      'cold_boot_no_savestate': True, 'no_synthetic_gameplay_fixtures': True,
                      'diagnostic_ROM_observer': label.endswith('_trace')}
            screenshots.append(record)
            if label.endswith('_baseline') and frame in (19000, 19800, 21800):
                destination = GUIDE / f'V633_Two_ship_{frame:06d}_UNMODIFIED_NATIVE.png'
                checked_copy(row['path'], destination)
                guides.append({**record, 'path': str(destination), 'report': str(report_path),
                               'normal_test_session_ship_purchase': True,
                               'final_cargo_setup_not_committed_or_saved': True})
    save(GUIDE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
                                   'screenshots': guides, 'publication_approved': False})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
                                     'screenshots': screenshots, 'guide_candidates': guides,
                                     'native_exports_and_RAM_retained_in_Generated_runs': True,
                                     'publication_approved': False, 'full_goal_complete': False,
                                     'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                                               if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
             'candidate': str(SOURCE), 'candidate_sha256': proof['candidate_sha256'],
             'status': 'new_ordinary_two_ship_contexts_verified_bounded_trace_no_targets',
             'all80_two_screen_frames_exact_between_current_and_diagnostic': True,
             'drawing_calls': proof['drawing_calls'], 'zero_target_records_and_zero_overflow': True,
             'nine_complete_Vestaros_Latina_headings_eight_complete4096_pixel_banners': True,
             'nine_original_cached_resource_bindings_and_source_tooltip_overlap': True,
             'normal_purchase_name_editor_L_R_transfer_finish_confirmation_cancel': True,
             'final_cargo_setup_not_committed_or_saved': True,
             'commodity90_source_fidelity_followup': {'Japanese': '鉄鉱石', 'current': 'Iron',
                                                     'source_meaning': 'iron ore',
                                                     'status': 'legacy_abbreviation_review_and_complete_label_fit_pending'},
             'ordinary_miniature_Confirm_and_broader_graphics_contexts_still_open': True,
             'all18_original_plaques_incomplete_all22_historical_objects_exact': True,
             'production_ROM_patch_registry_or_release_pointers_changed': False,
             'archive': str(ARCHIVE), 'guide_archive': str(GUIDE),
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
        assert all(current[k] == v for k, v in before.items() if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V634: ordinary two-ship cargo and bounded selection trace'
    text = '''

Unchanged V633 now has ordinary second-ship purchase/naming,L/R cargo selection,
temporary transfer and Finish/cancel context coverage. Nine complete ship headings,
eight whole Temporary Storage banners32768 pixels,nine original resource bindings
and the complete confirmation pass. Original-ROM control confirms source tooltip
overlap. A diagnostic-only observer records293091 drawing calls with no target
records or overflow;all80 sampled whole screens match unmodified V633 exactly.
This excludes the declared software-draw shapes in this input path,not global use
or other GPU/embedded consumers. Miniature/Confirm ordinary parents stay open.
Current Iron is source鉄鉱石/iron ore;the old manuscript explicitly defers this
abbreviation's fidelity review. Review and fit complete ore labels next rather
than silently treating legacy flags as final. Production,patch,registry and all
release pointers unchanged. All18/22 scopes exact/open;full graphics goal active.
Evidence and three guide candidates saved on E. See
[V634 checkpoint](selection_contexts_v634_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'V634 archived{len(screenshots)} unmodified screenshots,3 guide candidates;18/22 scopes and every release pointer exact.')


if __name__ == '__main__':
    main()
