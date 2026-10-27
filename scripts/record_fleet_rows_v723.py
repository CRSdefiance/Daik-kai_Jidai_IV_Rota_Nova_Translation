"""Record the ordinary fleet-row parent with explicit Flagship occlusion scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_fleet_rows_v723 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/fleet_rows_v723_checkpoint.md')
LEDGER = Path('translations/graphics_current_work_v1.json')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V723 Fleet row graphics')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V712 Swap Ships')
KEY = 'ordinary_Port_Dock_Swap_Ships_four_visible_labels_and_full_native_underlay_v723'
PREVIOUS = 'ordinary_Info_Ancient_Map_Treasure_Name_full_heading_original_parent_reopen_return_v722'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_fleet_rows_v723.py').read_bytes())
    assert len(proof['all24_visible_Ship2_to5_masks_and_whole19200_source_pixels_exact']) == 24
    for p, d in proof['release_hashes_unchanged'].items():
        assert sha(Path(p).read_bytes()) == d
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in frozen}
    assert all(KEY not in d for d in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V722.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    previous_sha = sha(snapshot.read_bytes())
    assert all(d[PREVIOUS]['current_matrix_sha256'] == previous_sha for d in before.values())
    matrix = read(MATRIX)
    resource = '/Iseki/dock.pxl'
    pending = matrix['current_original_inventory_assets_needing_explicit_native_evidence_reconciliation']
    assert resource in pending and len(pending) == 3
    matrix['current_original_inventory_assets_needing_explicit_native_evidence_reconciliation'] = [p for p in pending if p != resource]
    row = next(r for r in matrix['original26_confirmed_entries_current_implementation_links'] if r['path'] == resource)
    row['actual_native_context_evidence_v723'] = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'menu': 'Port > Dock > Swap Ships', 'ordinary_original_parent_and_four_visible_labels_verified': True,
        'all_five_labels_verified_in_complete_original_native_underlay': True,
        'Flagship_covered_by_occupied_row_not_claimed_visible_in_capture': True,
        'other_fleet_compositions_and_arrange_parents_not_claimed': True}
    matrix['historical_V722_matrix_snapshot'] = {'path': str(snapshot), 'sha256': previous_sha}
    matrix['latest_evidence_checkpoint'] = 'V723 ordinary Swap Ships fleet-row parent'
    save(MATRIX, matrix)
    ledger = read(LEDGER)
    identifier = 'ordinary-Swap-Ships-fleet-row-parent'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Iseki/dock original Swap Ships parent and tested baseline lettering',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'Four visible labels24 complete masks,full captured source/view/cache and49152-word native underlay with all5 labels. Occupied Flagship not claimed visible; other fleet states/parents remain outside scope.',
        'queue_status': 'complete-not-in-active-queue'})
    save(LEDGER, ledger)
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'ordinary_original_Port_Dock_Swap_Ships_consumer_identified': True,
        'all24_visible_label_masks19200_source_pixels_and_full_native_underlay_pass': True,
        'Flagship_is_source_underlay_evidence_not_a_visible_capture_claim': True,
        'supplied_renderer_fragment_not_full_parent_or_before_overlay_GPU_claim': True,
        'whole_town_return_and_source_donor_preservation_pass': True,
        'two_other_original_inventory_evidence_links_remain': True,
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V722_matrix_immutable_snapshot': {'path': str(snapshot), 'sha256': previous_sha},
        'all18_original_incomplete_objects22_historical_requirements_exact': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        p = Path('translations') / name
        data = read(p)
        assert data == before[name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        previous = data[PREVIOUS]
        assert previous['current_matrix'] == str(MATRIX)
        previous['matrix_live_path_at_recording'] = str(MATRIX)
        previous['current_matrix'] = str(snapshot)
        previous['historical_snapshot_bytes_exact_original_recorded_hash'] = True
        data[KEY] = entry
        save(p, data)
    p = Path('docs/graphics_remaining_work.md')
    text = p.read_text(encoding='utf-8')
    old = 'Three original resources still need explicit native-evidence linkage: slackimg12,Press a button,and Iseki/dock.'
    new = ('V723 identifies Iseki/dock in ordinary Port > Dock > Swap Ships,with occupied-row visibility limits. '
        'Two original resources still need explicit native-evidence linkage: slackimg12 and Press a button.')
    assert old in text
    p.write_text(text.replace(old, new), encoding='utf-8')
    heading = '## V723: ordinary Swap Ships fleet-row parent and native underlay'
    summary = ('One13100-frame ordinary copied-save cold boot identifies Iseki/dock in Port > Dock > Swap Ships, '
        'not the Info Dock Ships/Fleet Info detours. Actual CShipChangeView,full256x192 source and six '
        'complete native cache getters bind the asset. Four visible empty-row labels pass24 complete '
        'font masks and19200 source pixels. Original base-draw fragment writes49152 lower words over '
        'poison,all source-exact,with no output reads-before-write and other-plane guard intact. All5 '
        'source/native-underlay font masks pass; occupied Flagship is covered and not claimed visible. '
        'Supplied captured renderer is a fragment contract,not full parent/before-overlay GPU proof; '
        'wrong owner-list diagnostic retained. Down does not select empty rows; no swaps/saves/fixtures '
        'or changed fleet-state claim. Whole town return and donor pass. Two inventory links remain; '
        'matrix retains V722 snapshot,original18/22 objects exact. V712/art/patch/registry/canonical '
        'unchanged; ordinary E guide candidates not publication approved. Wider goal active. '
        'See [V723 checkpoint](fleet_rows_v723_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        p = Path('docs') / name
        text = p.read_text(encoding='utf-8')
        assert heading not in text
        p.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    report = read(proof['report'])
    shots = {r['frame']: r for r in report['frames_captured']}
    for frame in (9500, 9900, 11900, 13100):
        r = shots[frame]
        p = Path(r['path'])
        assert sha(p.read_bytes()) == r['PNG_sha256']
        copy(p, ARCHIVE / 'Ordinary screenshots' / p.name)
        copy(p, GUIDE / p.name)
    save(GUIDE / 'provenance.json', {'capture_report': proof['report'], 'capture_report_sha256': proof['report_sha256'],
        'candidate_sha256': proof['candidate_sha256'], 'ordinary_inputs_and_unchanged_donor': True,
        'publication_approved': False, 'images': {p.name: sha(p.read_bytes()) for p in GUIDE.glob('*.png')}})
    for p in (DOC, MATRIX, LEDGER, snapshot, Path(__file__), Path('scripts/verify_fleet_rows_v723.py'), proof_path,
            ROOT / 'native_underlay.bin', ROOT / 'executed_inputs.json', Path(proof['report'])):
        copy(p, ARCHIVE / p.parent.name / p.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'native_underlay_is_derived_component_not_a_live_game_frame': True, 'full_goal_complete': False})
    for p, d in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / p).read_bytes()) == d
    for p, d in proof['release_hashes_unchanged'].items():
        assert sha(Path(p).read_bytes()) == d
    print('V723 recorded: ordinary parent/visible labels/native underlay and limits; two evidence links remain;14 completed scopes; E archive checked.', flush=True)


if __name__ == '__main__':
    main()
