"""Close one original consumer lead; preserve the unresolved graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_digit_records_v731 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/digit_records_v731_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V731 Decimal sprite writer')
KEY = 'original_80008000_decimal_sprite_writer_classification_v731'
PREVIOUS = 'current_five_category_maximum_equipment_hints_and_Info_composition_v730'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_digit_records_v731.py').read_bytes())
    assert proof['complete_native_writer_cases'] == 128
    assert len(proof['original_transfer_copy_boundaries']) == 4
    assert len(proof['all_three_aligned_ARM_BL_candidates']) == 3
    assert proof['cases_sha256'] == sha((ROOT / 'native_cases.json').read_bytes())
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V730.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    completed = ledger['completed_work_carried_forward']
    remaining = ledger['active_remaining_tasks']
    assert len(completed) == 23 and len(remaining) == 6
    lead = {'id': 'V704-packed-mask-decimal-sprite-writer', 'evidence': str(proof_path),
        'sha256': sha(proof_path.read_bytes()),
        'result': 'Complete native writer creates decimal sprite attributes; original copy wrapper targets07000000. The80008000 constant is not a raw-pixel opacity conversion.',
        'scope': '128 complete writer cases and4 transfer boundaries; no GPU,ordinary comic parent,global unused-art or other-importer closure.'}
    closed = ledger.setdefault('closed_consumer_leads', [])
    assert not any(r['id'] == lead['id'] for r in closed)
    closed.append(lead)
    task = next(r for r in remaining if r['id'] == 'original-comic-playback-and-restoration')
    task['remaining_scope'] += (' V731 closes the V704 packed80008000 writer lead as decimal sprite '
        'attributes,not raw-color import. Carry this source interpretation forward; other original '
        'comic consumer/import paths remain unresolved.')
    assert ledger['completed_work_carried_forward'] == completed
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V730_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V731 original decimal sprite writer classification'
    matrix['current_closed_consumer_lead_v731'] = lead
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), 'closed_consumer_lead': lead,
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V730_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
        'original23_completed_scopes_and_six_remaining_groups_preserved': True,
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
    heading = '## V731: packed-mask decimal sprite writer lead resolved'
    summary = ('Original020F4120 produces decimal tile attributes in02170774,not raw image pixels. '
        'All128 complete native sampled cases match independent decimal-string/record outputs across '
        'whole4MiB RAM with padding/neighbor guards and return ABI; executed code exact clean/current. '
        'Three aligned ARM BL candidates retained. Four original wrapper cases stop before DMA/CPU '
        'copy with07000000 destinations; no hardware/GPU/display credit. V70480008000 lead closed; '
        'original comic viewer/import/geometry/readability remain open. Existing23 completed scopes '
        'and six active groups preserved; original18/22 audit objects exact. No production changes '
        'or new screenshot. E records archive verified; goal active,Online exclusions,marks and '
        'older-record follow-up retained. See [V731 checkpoint](digit_records_v731_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__), ROOT / 'native_cases.json',
                 Path('scripts/verify_digit_records_v731.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'native_record_and_copy_boundary_evidence_not_GPU_or_guide': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V731 recorded:one source lead closed,23 completed scopes/six groups preserved; original18/22 and release/E hashes exact; goal active.')


if __name__ == '__main__':
    main()
