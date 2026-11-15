"""Record current long-hint integration without closing unrelated audit gates."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_long_hints_v730 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/long_hints_v730_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V730 Current long equipment hints')
KEY = 'current_five_category_maximum_equipment_hints_and_Info_composition_v730'
PREVIOUS = 'original_image_instruction_modes0_1_2_selector_boundaries_v729'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_long_hints_v730.py').read_bytes())
    assert proof['runner_sha256'] == sha(Path('scripts/run_long_hints_v730.py').read_bytes())
    assert len(proof['five_category_maximum_hints_and5120_icon_pixels']) == 5
    assert len(proof['three_complete_current_empty_hints']) == 3
    assert len(proof['all50_current_full_static_Info_plaques']) == 50
    assert len(proof['all50_full_skill_labels_and_observed_numeric_fields']) == 50
    assert len(proof['all10_natural_condition_label_masks']) == 10
    assert sum(map(len, proof['all103_current_native_equipment_names_and_widths'].values())) == 103
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V729.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    identifier = 'current-five-maximum-equipment-hint-composition'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Current combined-ROM five category-maximum equipment hints and Info composition',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'One15600-frame current cold boot,103 native names/widths,five occupied and three empty complete hints,5120 icon pixels,50 whole plaques,50 observed skill rows and10 condition masks. Declared inventory fixture; no acquisition/every-state or original18 overall closure.',
        'queue_status': 'complete-not-in-active-queue'})
    assert len(ledger['completed_work_carried_forward']) == 23
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'remaining-context-audit')
    task['remaining_scope'] += (' V730 verifies the current combined-ROM five category-maximum equipment '
        'hints,three empty hints and updated Info plaques; all103 current native names/widths carry '
        'V581 forward. This composition scope is complete and does not need routine repetition.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V729_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V730 current five maximum equipment hints and Info composition'
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'current_five_maximum_and_three_empty_hint_composition_complete': True,
        'inventory_fixture_not_normal_acquisition': True,
        'original18_overall_objects_remain_incomplete': True}
    matrix['current_maximum_equipment_hint_composition_v730'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
        'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V729_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
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
    heading = '## V730: current five longest equipment hints and Info composition'
    summary = ('One terminal15600-frame V712 cold boot uses a protected Maria save copy and a declared '
        'original-transfer inventory fixture. The11-byte fixture replays exactly; shared harness/helper/core '
        'unchanged. All103 current native equipment names/widths equal V581 and selected names remain '
        'category maxima. Five occupied and three empty complete hint papers,5120 icon pixels,50 whole '
        'current Info plaques,50 complete observed skill/value rows and10 condition masks pass. '
        'Current tile exact original donor join; actual screen and full-hint sheet opened. No clipped '
        'first/final letters or border defect found in this scope. Normal acquisition,other actors/states '
        'and original18 overall closure not inferred. Twenty-three completed scopes now carry forward; '
        'six unresolved groups remain. Original18/22 audit objects exact. E fixture archive verified; '
        'V712 ROM/manifest/patch/registry/canonical and original saves unchanged. Goal active,exclusions '
        'and older-record note retained. See [V730 checkpoint](long_hints_v730_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    report = read(CAP / 'capture_report.json')
    for frame in (6200, 7000, 12000, 14800, 15000, 15200, 15400, 15600):
        row = next(r for r in report['frames_captured'] if r['frame'] == frame)
        source = Path(row['path'])
        assert sha(source.read_bytes()) == row['PNG_sha256']
        copy(source, ARCHIVE / 'actual_captures' / f'frame_{frame:06d}.png')
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__), CAP / 'capture_report.json',
                 ROOT / 'preflight.json', ROOT / 'inputs.json', ROOT / 'interactive_commands.json',
                 ROOT / 'current_five_long_hints_review.png', Path('scripts/run_long_hints_v730.py'),
                 Path('scripts/verify_long_hints_v730.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'synthetic_inventory_display_fixture_not_normal_acquisition_or_guide': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V730 recorded:23 completed scopes,six active groups,original18/22 exact,E evidence verified; goal active.')


if __name__ == '__main__':
    main()
