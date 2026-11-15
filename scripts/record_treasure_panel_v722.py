"""Record a real Ancient Map consumer and update current evidence links."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_treasure_panel_v722 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/treasure_panel_v722_checkpoint.md')
LEDGER = Path('translations/graphics_current_work_v1.json')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V722 Treasure Name')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V712 Ancient Map')
KEY = 'ordinary_Info_Ancient_Map_Treasure_Name_full_heading_original_parent_reopen_return_v722'
PREVIOUS = 'current_full_goal_and22_historical_requirement_matrix_V712_v721'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_treasure_panel_v722.py').read_bytes())
    assert len(proof['four_actual_heading_and_view_cases']) == 4
    assert sum(r['all_visible_header_native5_pixels_exact'] for r in proof['four_actual_heading_and_view_cases']) == 14080
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in frozen}
    assert all(KEY not in d for d in before.values())
    matrix_snapshot = Path('work/analysis/graphics_audit_v721/graphics_current_requirements_at_V721.json')
    assert not matrix_snapshot.exists()
    matrix_snapshot.write_bytes(MATRIX.read_bytes())
    previous_sha = sha(matrix_snapshot.read_bytes())
    assert all(d[PREVIOUS]['matrix_sha256'] == previous_sha for d in before.values())
    matrix = read(MATRIX)
    resource = '/_pxl/mysterymap/mys_hunt_d.pxl'
    pending = matrix['four_original_inventory_assets_needing_explicit_native_evidence_reconciliation']
    assert resource in pending and len(pending) == 4
    # Retain the historical field as recorded, add a current list and a precise
    # override. Its V721 snapshot remains byte-exact and hash-addressable.
    matrix['current_original_inventory_assets_needing_explicit_native_evidence_reconciliation'] = [p for p in pending if p != resource]
    matrix['historical_V721_matrix_snapshot'] = {'path': str(matrix_snapshot), 'sha256': previous_sha}
    row = next(r for r in matrix['original26_confirmed_entries_current_implementation_links'] if r['path'] == resource)
    row['actual_native_context_evidence_v722'] = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'menu': 'Info > Ancient Map', 'ordinary_two_visits_selection_and_return': True,
        'full_heading_cells_source_view_and_original_cache_binding_complete': True,
        'discovered_item_rows_other_mode_not_verified': True}
    matrix['latest_evidence_checkpoint'] = 'V722 ordinary Treasure Name context'
    save(MATRIX, matrix)
    ledger = read(LEDGER)
    identifier = 'ordinary-Ancient-Map-Treasure-Name'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Treasure Name graphic in its original ordinary Info > Ancient Map parent',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'Four full heading masks,whole resident/cache source and view geometry,selection,reopen and whole town return; discovered rows/other mode not claimed.',
        'queue_status': 'complete-not-in-active-queue'})
    save(LEDGER, ledger)
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'actual_ordinary_source_parent_and_complete_Treasure_Name_heading_verified': True,
        'four_holds632_ink_points14080_visible_source_pixels_and8_edge_controls': True,
        'original_focus_overlay_does_not_drop_letters_no_source_pixels_waived': True,
        'whole_reopen_and_whole_final_town_RGB_comparisons_pass': True,
        'source_donor_ROM_art_patch_manifest_registry_canonical_unchanged': True,
        'three_other_original_inventory_evidence_links_remain': True,
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V721_matrix_immutable_snapshot': {'path': str(matrix_snapshot), 'sha256': previous_sha},
        'all18_original_objects_incomplete22_historical_requirements_exact': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == before[name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        previous = data[PREVIOUS]
        assert previous['matrix'] == str(MATRIX)
        previous['matrix_live_path_at_recording'] = str(MATRIX)
        previous['matrix'] = str(matrix_snapshot)
        previous['historical_snapshot_bytes_exact_original_recorded_hash'] = True
        data[KEY] = entry
        save(path, data)
    path = Path('docs/graphics_remaining_work.md')
    text = path.read_text(encoding='utf-8')
    old = 'Four original resources need explicit native-evidence linkage: Treasure Name,slackimg12,Press a button,and Iseki/dock.'
    new = ('V722 verifies Treasure Name in ordinary Info > Ancient Map. Three original resources still need '
        'explicit native-evidence linkage: slackimg12,Press a button,and Iseki/dock.')
    assert old in text
    path.write_text(text.replace(old, new), encoding='utf-8')
    heading = '## V722: ordinary Treasure Name parent,complete letters and return verified'
    summary = ('Two terminal cold boots retain a wrong Extras branch and complete15100-frame ordinary copied-save '
        'navigation. Info > Ancient Map binds actual CMysteryHuntView,whole current PXL cache and256x192 view. '
        'Four complete Treasure Name masks include632 ink points and all blank cells;eight first/final erasure '
        'controls fail. All14080 exposed header pixels match; captured first-row focus geometry explains '
        'three covered blank bottom rows without letter loss or a whole-overlay equivalence claim. Reopened '
        'whole RGB and returned whole town match. No savestate/live gameplay or graphic fixture; donor '
        'unchanged. Current matrix retains a hash-exact V721 snapshot and closes this context; three other '
        'inventory evidence links remain. Original18 incomplete objects/22 scopes exact. V712/patch/art/'
        'registry/canonical unchanged,no build/commit/push. Ordinary guide candidates saved on E,not '
        'publication approved. Wider graphics goal active,exclusions/marks/older-record note retained. '
        'See [V722 checkpoint](treasure_panel_v722_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    report = read(proof['actual_report'])
    shots = {r['frame']: r for r in report['frames_captured']}
    for frame in (9500, 10300, 11100, 13900, 15100):
        row = shots[frame]
        image = Path(row['path'])
        assert sha(image.read_bytes()) == row['PNG_sha256']
        copy(image, ARCHIVE / 'Ordinary native screenshots' / image.name)
        copy(image, GUIDE / image.name)
    save(GUIDE / 'provenance.json', {'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'capture_report': proof['actual_report'], 'capture_report_sha256': proof['actual_report_sha256'],
        'ordinary_copied_save_inputs_no_live_gameplay_fixture': True, 'publication_approved': False,
        'images': {p.name: sha(p.read_bytes()) for p in GUIDE.glob('*.png')}})
    for path in (DOC, MATRIX, LEDGER, matrix_snapshot, Path(__file__), Path('scripts/verify_treasure_panel_v722.py'),
            proof_path, ROOT / 'executed_inputs.json', Path(proof['actual_report'])):
        copy(path, ARCHIVE / path.parent.name / path.name)
    refs = {str(p): sha(p.read_bytes()) for p in CAP.glob('*.bin')}
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'read_only_RAM_exports_already_on_E_checked': refs,
        'normal_native_screenshots_not_reconstructions': True, 'full_goal_complete': False})
    for p, d in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / p).read_bytes()) == d
    for p, d in proof['release_hashes_unchanged'].items():
        assert sha(Path(p).read_bytes()) == d
    print('V722 recorded: original Ancient Map context complete,three evidence-link followups,thirteen completed scopes,ordinary E screenshots/guide provenance verified.', flush=True)


if __name__ == '__main__':
    main()
