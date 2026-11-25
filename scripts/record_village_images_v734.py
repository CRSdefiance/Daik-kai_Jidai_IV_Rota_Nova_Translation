"""Carry the complete Ezo request scope forward, leaving other consumers open."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.observe_village_images_v734 import ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.run_village_images_v734 import CAP
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/village_images_v734_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V734 Ezo image requests')
KEY = 'current_Ezo_full_arrival_story_password_and_port_request_trace_v734'
PREVIOUS = 'actual_ordinary_Rafael_command_source_checkpoints_and_baseline_v733'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    for key, filename in (('runner', 'run_village_images_v734.py'), ('observer', 'observe_village_images_v734.py'),
                          ('verifier', 'verify_village_images_v734.py')):
        assert proof[key + '_sha256'] == sha((Path('scripts') / filename).read_bytes())
    assert proof['actual_request_counts'] == {'direct_range': 4, 'numeric_ID': 55, 'filename': 49}
    assert proof['all48_whole_RGB_pairs_and45_whole4MiB_pause_RAM_pairs_exact']
    assert len(proof['all_seven_exported_final_guest_region_pairs']) == 7
    assert len(proof['all_six_complete_typed_prefixes']) == 6
    assert proof['no_eight_card_path_or_file_ID_or_direct_range_requests_in_this_sequence']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V733.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    identifier = 'current-Ezo-arrival-development-port-request-lifetime'
    assert not any(r['id'] == identifier for r in ledger['completed_work_carried_forward'])
    ledger['completed_work_carried_forward'].append({'id': identifier,
        'task': 'Current complete Ezo arrival/story/password/developed-port request trace',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': 'Two16700-frame runs;108 primary API requests classified,zero eight-card/event-still/raw requests. Typed Kamui/development0-to2 verified;48 whole RGB/45 pause RAM/7 final guest-region pairs exact. Coordinate fixtures only; other villages/story states/global non-use unproved.',
        'queue_status': 'complete-not-in-active-queue'})
    assert len(ledger['completed_work_carried_forward']) == 25 and len(ledger['active_remaining_tasks']) == 6
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'village-and-environment-contexts')
    task['remaining_scope'] += (' V734 closes transient primary-API card requests in the complete Ezo '
        'arrival/story/password/developed-port sequence: none across108 classified requests. Normal '
        'development and current fields verified; do not repeat this Ezo flow without a new target. '
        'Other village/story contexts and separate consumers remain unverified.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V733_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V734 current Ezo full progression and image request lifetime'
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
        'current_complete_Ezo_request_sequence_verified': True,
        'no_card_requests_in_this_sequence_not_global_unused_or_other_context_closure': True}
    matrix['current_Ezo_request_lifetime_v734'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
        'current_matrix_sha256': sha(MATRIX.read_bytes()), 'current_work_ledger': str(LEDGER),
        'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V733_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
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
    heading = '## V734: complete Ezo progression and transient image-request coverage'
    summary = ('Two terminal16700-frame V712 replays reach the original Ezo story,normal Kamui entry '
        'and developed port using only two coordinate fixtures. Fixture receipts/native development '
        '0-to2,six typed prefixes,complete dialogues/menu/title and resident clean-exact town48 pass. '
        'All108 requests classified:49 filenames,55 numeric,4 metadata ranges;zero event-still/raw '
        'entries and no eight-card path/ID/range requests in this sequence. All48 whole RGB/45 pause '
        'RAM/7 final guest-region pairs and exported CPU registers/PC match baseline. Thirty grouped '
        'host controls pass; source/core/shared files exact,slots restored. Unrelated getter assumption '
        'corrected to original TownModel B5630; no game fix. Other villages/story states/global non-use '
        'remain open. Twenty-five completed scopes carry forward;six groups/original18/22 exact. '
        'E fixture archive checked; release/art/saves unchanged,goal active,exclusions/marks/older-record '
        'note retained. See [V734 checkpoint](village_images_v734_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for mode in ('baseline', 'observed'):
        folder = CAP / ('village_images_v734_Ezo_' + mode)
        report = read(folder / 'capture_report.json')
        copied = set()
        for row in report['frames_captured']:
            if row['frame'] not in copied:
                copy(Path(row['path']), ARCHIVE / mode / f"frame_{row['frame']:06d}.png")
                copied.add(row['frame'])
        assert len(copied) == 48
        copy(folder / 'capture_report.json', ARCHIVE / mode / 'capture_report.json')
        copy(folder / 'navigation_command_journal.json', ARCHIVE / mode / 'navigation_command_journal.json')
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__), Path(proof['trace']),
                 ROOT / 'preflight.json', ROOT / 'source_contract.json', ROOT / 'native_prefix_controls.json',
                 ROOT / 'inputs.json', ROOT / 'commands.json', ROOT / 'Ezo_progression_review.png',
                 Path('scripts/run_village_images_v734.py'), Path('scripts/observe_village_images_v734.py'),
                 Path('scripts/verify_village_images_v734.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'coordinate_fixture_actual_progression_and_request_trace_not_earned_travel_or_all_villages': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V734 recorded:complete Ezo request scope;25 completed scopes,six groups,original18/22 and release/E hashes exact; goal active.')


if __name__ == '__main__':
    main()
