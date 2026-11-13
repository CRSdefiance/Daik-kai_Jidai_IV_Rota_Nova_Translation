"""Carry completed village testing forward and keep only unresolved goal work."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_village_request_sweep_v735 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/village_request_sweep_v735_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V735 All village request contexts')
KEY = 'current_all24_village_progression_primary_API_requests_v735'
PREVIOUS = 'current_Ezo_full_arrival_story_password_and_port_request_trace_v734'

REMAINING = {
    'original-comic-playback-and-restoration': (
        'Identify and verify the original comic viewer, loading/import, alpha, geometry and native '
        'readability for21 raw frames/18 captions. Preserve the approved brown marks.'),
    'normal-small-controls': (
        'Identify and verify ordinary parents, palettes and selection states for Confirm, '
        'Pick Cargo, Pick Ship, Done, Rank and Cancel.'),
    'village-and-environment-contexts': (
        'Identify and verify original in-game consumers of the eight village caption cards. '
        'Different story/debug/legacy consumers or other resource routes remain possible.'),
    'legacy-and-embedded-consumers': (
        'Identify and verify remaining ordinary standalone/Porto Estado title, sepia map, '
        'copyright, ship-texture and embedded alias loading/import/crop/composition relationships, '
        'including ordinary parents for slackimg12 and slackimg20.'),
    'remaining-context-audit': (
        'Finish reconciliation of unresolved historical contexts and the18 original overall '
        'plaque/hint audit objects against their latest evidence.'),
    'final-integrated-release-and-acceptance': (
        'Integrate any further graphics corrections through the registered builder, run the '
        'regressions required by those changes, finish audit/progress reconciliation and obtain '
        'user cold-boot acceptance. Rebuild and reconstruct the exact patch if the ROM changes.'),
}


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert len(proof['all23_new_terminal_current_cases']) == 23
    assert proof['all24_tested_arrival_password_development_return_sequences_covered_no8card_requests']
    assert proof['new_complete_native_Town_pixels'] == 23 * 98304
    for kind in ('runner', 'verifier'):
        source = Path('scripts') / f'{"run" if kind == "runner" else "verify"}_village_request_sweep_v735.py'
        assert sha(source.read_bytes()) == proof[kind + '_sha256']
    assert sha(Path('scripts/observe_village_images_v734.py').read_bytes()) == proof['observer_sha256']
    visual = read(ROOT / 'visual_review.json')
    assert visual['reviewed_all24_final_Town_views_and_both_current_reflowed_clues']
    for name, digest in visual['sheets'].items():
        assert sha((ROOT / name).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    snapshots = {}
    for live, filename in ((MATRIX, 'graphics_requirements_at_V734.json'),
                           (LEDGER, 'graphics_work_at_V734.json')):
        path = ROOT / filename
        assert not path.exists()
        path.write_bytes(live.read_bytes())
        snapshots[str(live)] = {'path': str(path), 'sha256': sha(path.read_bytes())}
    assert all(d[PREVIOUS]['current_matrix_sha256'] == snapshots[str(MATRIX)]['sha256'] and
               d[PREVIOUS]['current_work_ledger_sha256'] == snapshots[str(LEDGER)]['sha256']
               for d in before.values())
    ledger, matrix = read(LEDGER), read(MATRIX)
    carried_path = ROOT / 'carried_goal_scope_reconciliation.json'
    carried = read(carried_path)
    assert carried['prior_ledger_sha256'] == sha(LEDGER.read_bytes())
    assert len(carried['all25_completed_evidence_hashes_verified']) == 25
    for row in carried['all25_completed_evidence_hashes_verified']:
        assert sha(Path(row['evidence']).read_bytes()) == row['sha256']
    assert len(ledger['completed_work_carried_forward']) == 25
    for task in ledger['active_remaining_tasks']:
        task['remaining_scope'] = REMAINING[task['id']]
    assert len(ledger['active_remaining_tasks']) == len(REMAINING) == 6
    ledger['completed_work_carried_forward'].append({
        'id': 'all24-ordinary-village-progression-primary-API-request-contexts',
        'task': 'All24 tested village arrival/password/development/return primary-API request contexts',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': ('23 new current V712 runs plus carried paired Ezo V734. All primary API requests '
                  'classified, no eight-card requests in these sequences. New23 whole native Town '
                  'scenes/text fields verified. Authorized coordinate fixtures; not earned travel, '
                  'all stories, global non-use or23 additional baseline pairs.'),
        'queue_status': 'complete-not-in-active-queue'})
    ledger['completed_scope_count'] = 26
    ledger['latest_evidence_checkpoint'] = 'V735 all24 tested ordinary village request contexts'
    save(LEDGER, ledger)
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
             'all24_tested_primary_API_progression_contexts_complete': True,
             'original_card_consumers_and_global_unused_status_still_unresolved': True}
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V734_matrix_snapshot'] = snapshots[str(MATRIX)]
    matrix['latest_evidence_checkpoint'] = 'V735 all24 tested ordinary village request contexts'
    matrix['current_all24_village_request_contexts_v735'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
             'current_matrix_sha256': sha(MATRIX.read_bytes()), 'current_work_ledger': str(LEDGER),
             'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
             'immutable_V734_matrix_and_ledger': snapshots,
             'all18_original_incomplete_objects22_historical_requirements_exact': True,
             'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == before[name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        for key, live in (('current_matrix', MATRIX), ('current_work_ledger', LEDGER)):
            data[PREVIOUS][key + '_live_path_at_recording'] = data[PREVIOUS][key]
            data[PREVIOUS][key] = snapshots[str(live)]['path']
        data[PREVIOUS]['immutable_snapshot_bytes_exact_original_recorded_hashes'] = True
        data[KEY] = entry
        save(path, data)
    counts = proof['new_total_requests']
    requests = sum(counts.values())
    summary = (
        f"23 new terminal V712 runs cover {proof['new_unique_capture_frames']} unique captures and "
        f'{requests} classified primary-API requests ({counts}); paired Ezo V734 carries forward. '
        'All24 tested village arrival/password/development/return sequences are now covered. '
        'No eight-card file/path/range requests or raw/event-still entries in these sequences. '
        'All23 new complete native Town scenes (2260992 pixels), current titles, clue/facility '
        'fields, keyboard prefixes and menus pass. Coordinate-only fixtures replay; original '
        'saves and release files unchanged. Single-line clue-origin verifier assumption corrected '
        'from retained display contracts; no ROM fix. Observer controls carried by exact hashes; '
        'new23 are observed-only, not baseline pairs. Original card consumers/global non-use remain '
        'unresolved. Twenty-six completed checks now carry forward outside six concise remaining '
        'groups; original18/22 objects preserved. E evidence archive verified. Goal active; Online '
        'body exclusions, approved marks and older-record follow-up retained. See '
        '[V735 checkpoint](village_request_sweep_v735_checkpoint.md).\n')
    DOC.write_text(
        '# V735: all24 tested village request contexts\n\n' + summary +
        '\n## Coverage and limits\n\n'
        '- Production remains the registered V712 candidate, SHA-256 `' + proof['candidate_sha256'] + '`.\n'
        '- Every new run cold-boots a protected save copy. Coordinate fixtures own only eight '
        'ship-position bytes; passwords and development use ordinary game inputs. Maria Karibib '
        'uses the previously authorized selection-bypass donor; no earned unlock is claimed.\n'
        '- All filenames pair with original numeric IDs; FAT/source bytes and direct metadata '
        'ranges are checked. These are request-entry observations at the six documented hooks, '
        'not proof of every filesystem route or successful open.\n'
        '- Native final Town traversal repaints both complete 256x192 buffers over poison; '
        'original cached-footer registration/submission is replayed through original APIs. '
        'Both buffers equal actual RGB5 screenshots and LCDC exports. This is a disclosed '
        'component replay, not a whole-scheduler equivalence claim.\n'
        '- The V734 thirty grouped host controls, eight main-memory mirror controls and ten '
        'V733 DTCM precedence controls carry through unchanged source hashes. Ezo retains its '
        'paired baseline; the new23 runs have no new unobserved pair.\n'
        '- Entire input fields, menus and dialogue rectangles include blank cells; all current '
        'Town headers include the five V666 aliases. Two reflowed clues use the current aligned '
        'margin; unchanged single-line clues retain their original 16px origin.\n'
        '- Other story/debug/legacy consumers, original eight-card triggers, ordinary small '
        'control parents, raw comics, and remaining legacy relationships remain open. '
        'No full playthrough, hardware verification, canonical promotion or publication approval.\n'
        '\n## Goal cleanup\n\n'
        'Completed source reviews, galleries, tested plaque/hint compositions and tested village '
        'progression scopes remain in the completed ledger with their evidence. The active six '
        'groups contain only unresolved work. The original eighteen overall plaque/hint objects '
        'remain open as requested. The four low-resolution Online bodies remain excluded.\n',
        encoding='utf-8')
    heading = '## V735: all24 tested village request contexts and remaining-goal cleanup'
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        if name == 'graphics_remaining_work.md':
            start, tail = text.split('## Current requirement matrix', 1)
            assert start.startswith('# Graphics: remaining work')
            lines = ['# Graphics: remaining work', '',
                     'The restored goal continues from verified work. Twenty-six completed checks',
                     'are carried forward with evidence; only the following six groups remain.', '']
            for n, task in enumerate(ledger['active_remaining_tasks'], 1):
                lines.extend([f"{n}. {task['remaining_scope']}", ''])
            lines.extend(['Reopen completed checks only for changed dependencies, contradictory evidence,',
                          'or a required final integration gate. The four low-resolution Online bodies',
                          'remain excluded. Preserve the approved brown marks. After completion, revisit',
                          'the older record-based checks. The full goal remains active.', '',
                          '## Current requirement matrix' + tail])
            text = '\n'.join(lines)
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for result in proof['all23_new_terminal_current_cases']:
        folder = Path(result['report']).parent
        report = read(result['report'])
        captured = {}
        for row in report['frames_captured']:
            captured.setdefault(row['frame'], row)
        for frame, row in captured.items():
            copy(Path(row['path']), ARCHIVE / f"case_{result['index']:02d}" / f'frame_{frame:06d}.png')
        for path in (Path(result['report']), Path(result['journal']), folder / 'run_contract.json',
                     Path(result['requests']['path']), ROOT / f"case_{result['index']:02d}/proof.json",
                     Path(result['native_Town_replay'])):
            copy(path, ARCHIVE / f"case_{result['index']:02d}" / path.name)
    for path in (DOC, MATRIX, LEDGER, proof_path, carried_path, ROOT / 'preflight.json', ROOT / 'cases.json',
                 ROOT / 'visual_review.json', ROOT / 'current_reflowed_clues_review.png',
                 ROOT / 'sweep_result.json', ROOT / 'current24_Town_review_1.png',
                 ROOT / 'current24_Town_review_2.png', Path(__file__),
                 Path('scripts/run_village_request_sweep_v735.py'),
                 Path('scripts/verify_village_request_sweep_v735.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    for snapshot in snapshots.values():
        path = Path(snapshot['path'])
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'original_RAM_and_native_exports_retained_at_report_paths_on_E': True,
        'targeted_location_fixture_tests_not_earned_voyages_or_all_contexts': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert len(read(LEDGER)['completed_work_carried_forward']) == 26
    for name, scope in frozen.items():
        d = read(Path('translations') / name)
        assert d.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert d.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    print('V735 recorded:26 completed checks carried;6 unresolved groups; frozen audit objects and release exact.', flush=True)


if __name__ == '__main__':
    main()
