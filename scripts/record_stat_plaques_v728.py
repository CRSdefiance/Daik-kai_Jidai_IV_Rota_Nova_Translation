"""Record current stat boundary coverage while retaining original overall audits."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_stat_plaques_v728 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/stat_plaques_v728_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V728 Stat plaque boundaries')
KEY = 'current_minimum_full_stats_plaque_hints_and_complete_restored_screens_v728'
PREVIOUS = 'original_route_EV_action_selector_and_complete_SC_buffer_sources_v727'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_stat_plaques_v728.py').read_bytes())
    assert proof['runner_sha256'] == sha(Path('scripts/run_stat_plaques_v728.py').read_bytes())
    assert len(proof['all111_native_static_plaque_crops']) == 111
    assert len(proof['all_nine_complete_native_hints']) == 9
    assert len(proof['all54_complete_stat_numeric_fields']) == 54
    assert len(proof['all90_complete_skill_labels_and_observed_numeric_fields']) == 90
    assert len(proof['all16_whole_pre_fixture_and_restored_scene_RGB_pairs']) == 16
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V727.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    identifier = 'current-stat-boundary-plaque-and-hint-displays'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Current stat0/100 plaque,number and hint display boundaries',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'Three9500-frame runs,111 whole plaques,9 hints,54 stat fields,90 observed skill rows and16 whole pre/restored pairs. Six-byte fixtures restored; other values/actors/mechanics and18 overall objects remain outside closure.',
        'queue_status': 'complete-not-in-active-queue'})
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'remaining-context-audit')
    task['remaining_scope'] += (' Current stat0/100 plaque/hint boundaries and original-stat restoration '
        'are verified under V728; carry that tested scope forward without reopening it routinely.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V727_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V728 current minimum/full stat plaque displays and restoration'
    matrix['current_original18_plaque_stat_boundaries_v728'] = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'stat0_100_and_tested_hints_complete': True,
        'all18_original_overall_objects_remain_incomplete': True,
        'synthetic_display_states_not_natural_growth_or_all_contexts': True}
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **matrix['current_original18_plaque_stat_boundaries_v728'],
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V727_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
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
    heading = '## V728: current empty/full stat bars and restored plaque screens'
    summary = ('Three terminal9500-frame cold boots use the same controls and protected source-copy save. '
        'Two declared fixtures set only six captain attribute bytes to0/100 and restore them before '
        'reopening. All six4MiB before/after pairs replay exactly; exported GPR/PC/DTCM/ITCM unchanged. '
        'Original saved first name Hodram retained; chosen localization Joakim unchanged. All111 complete '
        'plaque crops,9 full hints,54 attribute fields and90 full observed skill/value rows pass. All16 '
        'whole pre-fixture/restored RGB pairs match the control,including reopening and town return. '
        'Control/0/100 screenshots and comparison opened; no clipping or bar overlap found in this scope. '
        'Original18 overall entries incomplete/22 historical objects exact. Twenty-one completed scopes '
        'carry forward; other original contexts/final review remain open. All captures/evidence on E, '
        'fixtures not guide/publication approved. V712 ROM/manifest/patch/registry/canonical unchanged; '
        'full goal active,exclusions/marks/older-record note retained. '
        'See [V728 checkpoint](stat_plaques_v728_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for mode in ('disabled', 'zero', 'hundred'):
        folder = CAP / ('stat_plaques_v728_' + mode)
        for frame in (6300, 6700, 7100, 7900, 9500):
            copy(folder / f'frame_{frame:06d}_cold_boot.png', ARCHIVE / mode / f'frame_{frame:06d}.png')
        for name in ('capture_report.json', 'fixture_receipts.json', 'run_contract.json'):
            copy(folder / name, ARCHIVE / mode / name)
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__), ROOT / 'preflight.json',
                 ROOT / 'inputs.json', ROOT / 'control_zero_hundred_review.png',
                 Path('scripts/run_stat_plaques_v728.py'), Path('scripts/verify_stat_plaques_v728.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'synthetic_attribute_displays_with_restoration_not_natural_growth_or_guide': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V728 recorded: actual boundary displays and full restoration pass;21 completed scopes; original18/22 audit objects retained; E archive exact.')


if __name__ == '__main__':
    main()
