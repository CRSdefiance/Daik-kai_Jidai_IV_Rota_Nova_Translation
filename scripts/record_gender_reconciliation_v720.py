"""Close verified gender-display scopes without erasing replay limitations."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_gender_displays_v720 import ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/gender_reconciliation_v720_checkpoint.md')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V720 Gender display reconciliation')
KEY = 'two_original_loose_Marker_parents44_complete_cells_carried_V712_replay_limits_retained_v720'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/reconcile_gender_displays_v720.py').read_bytes())
    assert len(proof['all44_complete_actual_symbol_cells']) == 44
    assert proof['complete_native5_pixel_comparisons'] == 11264
    assert len(proof['historical_reports_rechecked']) == 7
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in frozen}
    assert all(KEY not in d for d in before.values())
    ledger = read(LEDGER)
    identifier = 'two-original-loose-Marker-gender-displays'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Both verified original loose-PXL gender display parents and tested identity8/story-flag9 exception',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': '44 complete actual cells/11264 pixels bound to current unchanged Marker/native code. Embedded consumer and larger standalone replay equivalence remain open; fixture limits preserved.',
        'queue_status': 'complete-not-in-active-queue'})
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'remaining-context-audit')
    task['remaining_scope'] = ('Reconcile the remaining historical requirements without repeating completed visual scopes. '
        'V720 closes the tested two original loose-Marker display parents; their standalone prefix/suffix '
        'equivalence limitations remain documented research limits,not established production graphics defects. '
        'Embedded consumers and unverified contexts remain open. Keep18 original overall audit objects for final reconciliation.')
    save(LEDGER, ledger)
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'two_tested_original_loose_Marker_parents_both_symbols_and_story_exception_display_complete': True,
        'all44_native_cells11264_pixels_current_source_exact': True,
        'source_file_and_original_code_dependencies_unchanged': True,
        'historical_screenshots_not_relabelled_as_new_V712_execution': True,
        'original_V698_failure_V700_IO_diagnostic_and_V694_suffix_limit_retained_not_cleared': True,
        'standalone_replay_failure_not_established_as_production_graphics_defect': True,
        'embedded_copy_unknown_parents_other_graphics_and_final_release_still_open': True,
        'all18_original_incomplete_objects22_historical_requirements_exact': True,
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'release_hashes_unchanged': proof['release_hashes_unchanged'], 'archive': str(ARCHIVE),
        'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == before[name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY] = entry
        save(path, data)
    path = Path('docs/graphics_remaining_work.md')
    text = path.read_text(encoding='utf-8')
    old = ('   distinct from limitations of standalone diagnostic models. The18 overall\n'
        '   plaque entries remain open for final audit bookkeeping; their accepted material\n'
        '   and verified base views do not need another routine review.')
    new = ('   distinct from limitations of standalone diagnostic models. The two tested\n'
        '   loose Marker gender parents are complete (V720); their larger replay limits\n'
        '   remain documented without being called production defects. The18 overall\n'
        '   plaque entries remain open for final audit bookkeeping; accepted material\n'
        '   and verified base views do not need another routine review.')
    assert old in text
    path.write_text(text.replace(old, new), encoding='utf-8')
    heading = '## V720: two actual loose Marker gender display scopes complete'
    summary = ('Current Marker and original helper/update/cache/draw dependencies match V692. Seven historical '
        'reports/PNG identities rechecked; all44 complete16x16 actual cells match current source,11264 native5 '
        'pixels. Sailor Info and Deck personnel cover both symbols and the tested Arcadius identity8/flag9 '
        'exception. Authorized lookup/story fixtures retain their earned-progress and restored-portrait '
        'limits. These visual scopes leave active routine work. V698 unmapped04000204 replay failure and '
        'V694 full-suffix RAM/DTCM gap remain unwaived diagnostic limits,not confirmed production graphics '
        'defects; full-function equivalence is not claimed. Embedded copy/unknown contexts and final goal '
        'work remain open. All18 original objects incomplete,22 historical scopes exact; exclusions/marks '
        'retained. V712/art/patch/registry/canonical unchanged,no new emulator/guide/build/commit/push. '
        'Older record checks remain due after full completion. '
        'See [V720 checkpoint](gender_reconciliation_v720_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, LEDGER, Path('docs/graphics_remaining_work.md'), Path(__file__),
            Path('scripts/reconcile_gender_displays_v720.py'), proof_path):
        copy(path, ARCHIVE / path.parent.name / path.name)
    refs = dict(proof['reused_screenshot_hashes'])
    refs.update({r['path']: r['sha256'] for r in proof['historical_reports_rechecked']})
    refs.update({r['path']: r['sha256'] for r in proof['prior_display_proofs'].values()})
    limit = proof['diagnostic_IO_limit']
    refs[limit['path']] = limit['sha256']
    refs[limit['original_failure']] = limit['original_failure_sha256']
    assert all(sha(Path(p).read_bytes()) == d for p, d in refs.items())
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'checked_external_historical_evidence': refs, 'no_new_native_screenshots': True,
        'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for name in frozen:
        data = read(Path('translations') / name)
        assert data.pop(KEY) == entry and data == before[name]
    assert all(sha(Path(p).read_bytes()) == d for p, d in proof['release_hashes_unchanged'].items())
    print('V720 recorded: twelve completed scopes carried forward; original18/22 exact; archive and external evidence hashes pass.', flush=True)


if __name__ == '__main__':
    main()
