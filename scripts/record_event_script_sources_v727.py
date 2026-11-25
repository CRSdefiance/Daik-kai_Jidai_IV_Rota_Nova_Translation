"""Record the original route buffer source lead without ordinary-scene credit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.trace_event_script_sources_v727 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/event_script_sources_v727_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V727 Event script sources')
KEY = 'original_route_EV_action_selector_and_complete_SC_buffer_sources_v727'
PREVIOUS = 'current_numeric_CHARA_classification_and_all57_embedded_blocks_accounted_v726'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['producer_sha256'] == sha(Path('scripts/trace_event_script_sources_v727.py').read_bytes())
    assert len(proof['two_ROM_cases']) == 2
    assert all(r['native_selected_action_cases'] == 1312 and r['complete_SC_loads_and_cache_hits'] == 1307
               for r in proof['two_ROM_cases'])
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {n: read(Path('translations') / n) for n in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V726.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    identifier = 'original-route-script-buffer-source-lead'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Original EV action and SC buffer source lead',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': '2624 source-backed action fragments,2614 complete source loads and cache hits. Empty inline sections; no returned generated stream. Other builders,post-load mutation and ordinary contexts remain open.',
        'queue_status': 'complete-not-in-active-queue'})
    village = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'village-and-environment-contexts')
    village['remaining_scope'] += (' V727 closes generation within the original route SC-buffer loader: '
        'all source blocks load exact and route EV inline sections are empty. Do not repeat that lead; '
        'other builders,post-load mutation and independent consumers are not excluded.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V726_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V727 original route action tables and native SC buffer sources'
    matrix['original_route_script_buffer_sources_v727'] = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'all_original_route_action_tables_and_complete_SC_loaders_checked': True,
        'bounded_source_generation_lead_closed_not_global_nonuse_or_normal_scene_proof': True}
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **matrix['original_route_script_buffer_sources_v727'],
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V726_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
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
    heading = '## V727: original route script-buffer source path verified'
    summary = ('Original route EV tables contain1307 SC references and5 null actions per ROM,with empty '
        'inline script sections. Source-backed original selector fragments execute2624 cases across '
        'clean/current; complete native SC loaders and cache hits each pass2614 cases with exact whole '
        'payloads,ABI/source/neighbor guards and source-code bytes. Only SDK file I/O is bridged,with '
        'explicit filename case resolution. No village-card opcode byte candidates in returned scripts. '
        'This closes generation within this buffer loader,not other builders,post-load mutation,ordinary '
        'triggers or global non-use. Probe entry/cache-sentinel/case assumptions corrected before final run. '
        'Twenty completed scopes retained;original18 incomplete objects/22 requirements exact. V712 '
        'ROM/manifest/patch/registry/canonical unchanged,E evidence archive checked,no new GPU/guide '
        'claim. Full goal active,exclusions/marks/older-record note retained. '
        'See [V727 checkpoint](event_script_sources_v727_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__), Path('scripts/trace_event_script_sources_v727.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'native_source_fragment_and_loader_tests_not_normal_events_or_GPU_screenshots': True,
        'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V727 recorded: source-buffer generation lead closed; other native contexts remain open;20 completed scopes; E archive exact.')


if __name__ == '__main__':
    main()
