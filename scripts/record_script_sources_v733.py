"""Record actual source checkpoints and a pristine ordinary guide candidate."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.observe_script_sources_v733 import ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.run_script_sources_v733 import CAP
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/script_sources_v733_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V733 Actual script sources')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/Rafael New Game')
KEY = 'actual_ordinary_Rafael_command_source_checkpoints_and_baseline_v733'
PREVIOUS = 'original_SC_cached_parent_handoff_and_first_instruction_read_v732'


def main():
    assert not (GUIDE / 'V712_frame_004000.png').exists()
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    for key, filename in (('runner', 'run_script_sources_v733.py'), ('observer', 'observe_script_sources_v733.py'),
                          ('verifier', 'verify_script_sources_v733.py')):
        assert proof[key + '_sha256'] == sha((Path('scripts') / filename).read_bytes())
    assert proof['actual_native_callback_count'] == 41
    assert len(proof['complete_command_entry_return_pairs']) == 20
    assert proof['all16_complete_RGB_frame_pairs_exact']
    trace = read(proof['trace'])
    assert sha(Path(proof['trace']).read_bytes()) == proof['trace_sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V732.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    identifier = 'current-ordinary-Rafael-command-source-checkpoints'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Current ordinary Rafael opening command-source checkpoints and observer baseline',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'Two4000-frame ordinary cold boots;41 observations/20 full entry-return pairs retain entire6768-byte SC0 block44. All16 whole RGB pairs/final4MiB exact. One in-game input wait has no return credit. Temporary write/restore,other contexts and village triggers remain unproved.',
        'queue_status': 'complete-not-in-active-queue'})
    assert len(ledger['completed_work_carried_forward']) == 24 and len(ledger['active_remaining_tasks']) == 6
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'village-and-environment-contexts')
    task['remaining_scope'] += (' V733 observes20 complete ordinary opening commands with full source '
        'payloads exact at entry/return and no unclassified source. This short Rafael schedule is '
        'complete; do not repeat it as new village coverage. Other actual contexts and image-parent '
        'arguments remain useful leads; temporary write/restore is not excluded by checkpoints.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V732_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V733 actual ordinary command source observations and baseline'
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'current_ordinary_opening_source_checkpoint_scope_complete': True,
        'not_whole_interpreter_readonly_global_use_or_village_trigger_closure': True}
    matrix['current_ordinary_command_sources_v733'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
        'current_matrix_sha256': sha(MATRIX.read_bytes()), 'current_work_ledger': str(LEDGER),
        'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V732_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
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
    heading = '## V733: actual ordinary script-source observations and paired baseline'
    summary = ('Two terminal4000-frame V712 ordinary Rafael New Game cold boots use no save,savestate '
        'or gameplay fixture. Read-only original interpreter callbacks observe21 command entries/20 '
        'returns; all41 full6768-byte SC0 block44 sources match current ROM,with no unclassified input. '
        'Ten native host controls,eight mirror and ten DTCM controls pass; callback CPU-prefix/WRAM/TCM '
        'preservation and restored host slots/core exact. All16 complete RGB pairs/final4MiB match '
        'baseline. One command awaits in-game input at capture end,without return credit or live '
        'process claim. Temporary write/restore,other contexts and original village triggers remain '
        'open. Twenty-four completed scopes carry forward;six groups/original18/22 remain. E audit '
        'archive checked; pristine ordinary guide candidate saved without publication approval. '
        'Release/art/saves unchanged; goal active,exclusions/marks/older-record note retained. '
        'See [V733 checkpoint](script_sources_v733_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for mode in ('baseline', 'observed'):
        folder = CAP / ('script_sources_v733_' + mode)
        report = read(folder / 'capture_report.json')
        copy(folder / 'capture_report.json', ARCHIVE / mode / 'capture_report.json')
        for frame in (2400, 3200, 4000):
            row = next(r for r in report['frames_captured'] if r['frame'] == frame)
            copy(Path(row['path']), ARCHIVE / mode / f'frame_{frame:06d}.png')
    baseline = read(CAP / 'script_sources_v733_baseline/capture_report.json')
    selected = next(r for r in baseline['frames_captured'] if r['frame'] == 4000)
    guide = GUIDE / 'V712_frame_004000.png'
    assert not guide.exists()
    copy(Path(selected['path']), guide)
    save(GUIDE / 'V712_frame_004000.provenance.json', {'file': str(guide), 'sha256': sha(guide.read_bytes()),
        'source_report': proof['reports']['baseline'], 'frame': 4000,
        'candidate_sha256': proof['candidate_sha256'], 'ordinary_cold_boot_no_save_savestate_or_gameplay_fixture': True,
        'unobserved_baseline_original_PNG_not_reconstructed': True,
        'guide_candidate': True, 'publication_approved': False})
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__), Path(proof['trace']),
                 ROOT / 'preflight.json', ROOT / 'source_contract.json', ROOT / 'native_prefix_controls.json',
                 ROOT / 'inputs.json', ROOT / 'baseline_observed_review.png',
                 Path('scripts/run_script_sources_v733.py'), Path('scripts/observe_script_sources_v733.py'),
                 Path('scripts/verify_script_sources_v733.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    for filename in {r['source']['actual_payload_file'] for r in trace['rows']}:
        p = Path(filename)
        copy(p, ARCHIVE / 'actual_resident_payloads' / p.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'ordinary_opening_actual_trace_not_all_contexts_or_village_trigger': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V733 recorded:24 completed scopes,six active groups,original18/22 and release/E hashes exact; ordinary guide candidate copied; goal active.')


if __name__ == '__main__':
    main()
