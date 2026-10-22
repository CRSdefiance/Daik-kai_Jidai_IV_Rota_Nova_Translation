"""Record current inventory widget evidence while preserving ordinary-context gaps."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_generic_inventory_v724 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/generic_inventory_v724_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V724 Generic inventory graphics')
KEY = 'current_name_atlas_and_press_button_complete_source_widget_fixtures_v724'
PREVIOUS = 'ordinary_Port_Dock_Swap_Ships_four_visible_labels_and_full_native_underlay_v723'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_generic_inventory_v724.py').read_bytes())
    assert proof['preparer_sha256'] == sha(Path('scripts/prepare_generic_inventory_v724.py').read_bytes())
    assert len(proof['two_current_native_widget_cases']) == 2
    assert len(proof['eight_original_text_boundary_cases']) == 8
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in frozen}
    assert all(KEY not in d for d in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V723.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(d[PREVIOUS]['current_matrix_sha256'] == old_hash for d in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    resources = [r['source_path'] for r in proof['two_current_native_widget_cases']]
    assert matrix['current_original_inventory_assets_needing_explicit_native_evidence_reconciliation'] == resources
    for case in proof['two_current_native_widget_cases']:
        row = next(r for r in matrix['original26_confirmed_entries_current_implementation_links'] if r['path'] == case['source_path'])
        assert row['current_whole_file_sha256'] == case['current_file_sha256']
        row['current_native_widget_fixture_evidence_v724'] = {
            'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
            'five_complete_current_images_and_resident_native_getters_verified': True,
            'source_command_substitution_not_ordinary_event_progression': True,
            'ordinary_parent_remains_unidentified': True}
        identifier = f'current-slackimg{case["index"]}-native-widget-fixture'
        assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
        ledger['completed_work_carried_forward'].append({'id': identifier,
            'task': f'Current {case["source_path"]} complete original image-widget fixture',
            'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
            'scope': 'Five whole visible source-image matches,actual owner/view and complete native resident getter. Source-command fixture; original ordinary parent remains open.',
            'queue_status': 'complete-not-in-active-queue'})
    matrix['current_original_inventory_assets_needing_explicit_native_evidence_reconciliation'] = []
    matrix['current_original_inventory_assets_with_unidentified_ordinary_parents'] = resources
    matrix['historical_V723_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V724 current name-atlas and prompt native widget fixtures'
    legacy = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'legacy-and-embedded-consumers')
    legacy['remaining_scope'] += (' The original ordinary parents of slackimg12 and slackimg20 remain unidentified; '
        'their current complete image-widget fixture scopes are now finished under V724.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'two_current_original_inventory_native_widget_links_complete': True,
        'ten_complete_images29560_visible_pixels_and_native_getters_pass': True,
        'eight_original_dialogue_decoder_boundaries_exclude_nearest_false_scene_leads': True,
        'twenty_containers_each_ROM_bounded_kind3_byte_census': True,
        'original_ordinary_parents_unidentified_and_still_in_active_legacy_queue': resources,
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V723_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
        'all18_original_incomplete_objects22_historical_requirements_exact': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == before[name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        previous = data[PREVIOUS]
        previous['matrix_live_path_at_recording'] = previous['current_matrix']
        previous['current_matrix'] = str(snapshot)
        previous['historical_snapshot_bytes_exact_original_recorded_hash'] = True
        data[KEY] = entry
        save(path, data)
    remaining = Path('docs/graphics_remaining_work.md')
    text = remaining.read_text(encoding='utf-8')
    old = 'Two original resources still need explicit native-evidence linkage: slackimg12 and Press a button.'
    new = ('V724 supplies current complete native-widget fixture links for slackimg12 and Press a button. '
        'All four original inventory linkage gaps now have explicit evidence; '
        'the ordinary parents of these last two resources remain open in the legacy/context queue.')
    assert old in text
    remaining.write_text(text.replace(old, new), encoding='utf-8')
    heading = '## V724: current name-atlas and button-prompt native evidence'
    summary = ('Two terminal 5000-frame V712-parent research cold boots verify five complete visible source '
        'images and complete native resident-file getters per resource: 29560 pixels, full letters and bounds. '
        'Only one four-byte original source-image instruction differs per fixture; ordinary scene progression '
        'is not claimed. The name atlas changed since V538, so its old capture was not reused. Twenty source '
        'containers per ROM were scanned; eight native text-decoder boundary cases exclude the nearest exact '
        'route byte matches as prompt-test leads. Current inventory evidence links are reconciled; original '
        'ordinary parents remain in the active legacy queue. Six remaining groups and sixteen completed scopes '
        'are retained, with original18 incomplete objects/22 historical requirements exact. V712 ROM, patch, '
        'manifest, registry and canonical unchanged. Fixture screenshots archived on E, not guide/publication '
        'evidence. Full goal active; exclusions, marks and older-record follow-up preserved. '
        'See [V724 checkpoint](generic_inventory_v724_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for case in proof['two_current_native_widget_cases']:
        frame = next(r for r in case['frames'] if r['frame'] == 3900)
        shot = Path(frame['screenshot']['path'])
        copy(shot, ARCHIVE / f'slackimg{case["index"]}_V712_WIDGET_FIXTURE.png')
        copy(case['capture_report'], ARCHIVE / f'index{case["index"]}_capture_report.json')
        copy(case['fixture_manifest'], ARCHIVE / Path(case['fixture_manifest']).name)
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__),
                 Path('scripts/prepare_generic_inventory_v724.py'), Path('scripts/verify_generic_inventory_v724.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'source_command_fixtures_not_ordinary_scene_or_guide': True, 'publication_approved': False,
        'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V724 recorded: current inventory links complete, ordinary parents open; sixteen completed scopes; archive exact.')


if __name__ == '__main__':
    main()
