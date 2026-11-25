"""Carry verified selector scopes forward without closing unresolved displays."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_image_modes_v729 import REPORT, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/image_modes_v729_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V729 Image instruction modes')
KEY = 'original_image_instruction_modes0_1_2_selector_boundaries_v729'
PREVIOUS = 'current_minimum_full_stats_plaque_hints_and_complete_restored_screens_v728'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_image_modes_v729.py').read_bytes())
    assert proof['cases'] == 1536
    assert proof['mode1_2_cleanup_then_no_child_cases'] == 1024
    assert proof['mode0_valid0_through217_item_constructor_boundary_cases'] == 436
    assert proof['mode0_218_through255_no_child_cases'] == 76
    assert sha((ROOT / 'cases.json').read_bytes()) == proof['cases_file_sha256']
    assert sha((ROOT / 'executed_source.json').read_bytes()) == proof['executed_source_sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V728.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    identifier = 'original-image-modes0-1-2-selector-lead'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Original image modes0/1/2 selector and cleanup lead',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': '1536 diagnostic streams:1024 mode1/2 no-child cases,436 mode0 item-constructor boundaries and76 rejected indices. No full constructor,frame wait,GPU or ordinary parent credit.',
        'queue_status': 'complete-not-in-active-queue'})
    assert len(ledger['completed_work_carried_forward']) == 22
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'original-comic-playback-and-restoration')
    task['remaining_scope'] += (' V729 closes the mode0/1/2 image-selector lead: mode0 selects an item '
        'window;1/2 have no child. Carry this bounded source proof forward; original comic loading remains open.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V728_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V729 remaining original image-instruction selector modes'
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'modes0_1_2_selector_lead_complete': True, 'original_comic_viewer_display_remains_open': True,
        'diagnostic_inputs_and_constructor_boundary_not_ordinary_scene_or_GPU': True}
    matrix['current_image_mode_selector_lead_v729'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
        'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V728_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
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
    heading = '## V729: original image modes0/1/2 selector lead closed'
    summary = ('All1536 diagnostic operand streams execute original dispatch,decoding and cleanup. '
        'Modes1/2 produce no child in1024 cases; mode0 indices0-217 reach the item-window constructor '
        'in436 cases and218-255 produce no child in76. Executed source bytes,operands,lengths and '
        'neighbor guards pass. No complete item constructor,frame wait,GPU,ordinary parent or global '
        'non-use claim; original comic viewer remains open. V724 research snapshot provenance '
        'explicit; incomplete exploratory continuation receives no display credit. Twenty-two '
        'completed scopes now carry forward outside the six active groups; original18/22 audit '
        'objects preserved. V712 ROM,manifest,patch,registry and canonical unchanged; E records '
        'archive checked. Goal active,Online exclusions,marks and older-record follow-up retained. '
        'See [V729 checkpoint](image_modes_v729_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__), REPORT,
                 ROOT / 'cases.json', ROOT / 'executed_source.json',
                 Path('scripts/verify_image_modes_v729.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'diagnostic_native_selector_records_not_GPU_or_guide_screenshots': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V729 recorded:22 completed scopes outside six active groups; original18/22 exact; E archive verified; goal active.')


if __name__ == '__main__':
    main()
