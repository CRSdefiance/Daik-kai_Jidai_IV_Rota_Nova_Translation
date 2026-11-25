"""Save a concrete context question without closing unresolved graphic tasks."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_display_context_packet_v739 import PACKET, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/display_context_packet_v739_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
KEY = 'unresolved_display_context_recognition_packet_v739'
PREVIOUS = 'bounded_indexed_resource_owner_lead_v738'


def main():
    proof_path = ROOT / 'proof.json'
    proof, validation = read(proof_path), read(ROOT / 'packet_validation.json')
    assert proof['entries'] == 49 and proof['decoded_images'] == 98
    assert validation['all102_original_packet_files_hash_checked']
    assert validation['all49_unique_cases_98_full_RGB_files_reopened_exact']
    assert validation['all_HTML_local_image_links_exist_and_cover_exactly98_previews']
    assert sha(Path('scripts/prepare_display_context_packet_v739.py').read_bytes()) == proof['producer_sha256']
    for path, digest in proof['all_packet_file_hashes'].items():
        assert sha((PACKET / path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    snapshots = {}
    for live, name in ((MATRIX, 'graphics_requirements_at_V738.json'), (LEDGER, 'graphics_work_at_V738.json')):
        path = ROOT / name
        assert not path.exists()
        path.write_bytes(live.read_bytes())
        snapshots[str(live)] = {'path': str(path), 'sha256': sha(path.read_bytes())}
    assert all(d[PREVIOUS]['current_matrix_sha256'] == snapshots[str(MATRIX)]['sha256'] and
               d[PREVIOUS]['current_work_ledger_sha256'] == snapshots[str(LEDGER)]['sha256']
               for d in before.values())
    ledger, matrix = read(LEDGER), read(MATRIX)
    assert len(ledger['completed_work_carried_forward']) == 28 and len(ledger['active_remaining_tasks']) == 5
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
             'packet': str(PACKET / 'index.html'),
             'recognition_overview': str(PACKET / 'comic_recognition_overview.png'),
             'all49_source_current_cases_98_complete_decodes': True,
             'original_context_information_requested_not_approval_or_scope_reduction': True,
             'user_response_status': 'pending-no-answer-or-approval-inferred',
             'no_native_display_credit_or_completed_scope_count_increase': True}
    ledger['display_context_lookup_packet_v739'] = field
    ledger['latest_evidence_checkpoint'] = 'V739 concrete unresolved display context lookup packet'
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V738_matrix_snapshot'] = snapshots[str(MATRIX)]
    matrix['latest_evidence_checkpoint'] = ledger['latest_evidence_checkpoint']
    matrix['unresolved_display_context_packet_v739'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
             'current_matrix_sha256': sha(MATRIX.read_bytes()), 'current_work_ledger': str(LEDGER),
             'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
             'all18_original_incomplete_objects22_historical_requirements_exact': True,
             'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        d = read(path)
        assert d == before[name]
        assert d.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert d.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        for key, live in (('current_matrix', MATRIX), ('current_work_ledger', LEDGER)):
            d[PREVIOUS][key + '_live_path_at_recording'] = d[PREVIOUS][key]
            d[PREVIOUS][key] = snapshots[str(live)]['path']
        d[PREVIOUS]['immutable_snapshot_bytes_exact_original_recorded_hashes'] = True
        d[KEY] = entry
        save(path, d)
    summary = (
        'A portable E review packet now contains49 source/current cases and98 complete RGB '
        'decodes:all21 comic/sketch frames,six controls,eight village cards,eight standalone '
        'legacy resources and all six WINFRAME images. Source/current PNG pixels and102 '
        'packet-file hashes/HTML links pass; comic/control recognition sheets were visually '
        'inspected. These are stored-resource previews,not emulator screenshots or native '
        'alpha/geometry/readability evidence. WINFRAME includes one Porto title plus book '
        'materials,Koei logo and original English Hoist the sails; no new translation '
        'obligation is inferred from their inclusion. A concrete original-DS menu/event/save '
        'information question accompanies the comic sheet; response pending,not approval '
        'or exclusion. No source/consumer task closes and completed count stays28/five '
        'remaining groups. Original18/22 objects preserved,ROM/art/patch/registry/saves '
        'unchanged,goal active. See [V739 packet](display_context_packet_v739_checkpoint.md).\n')
    DOC.write_text(
        '# V739: unresolved original display contexts\n\n' + summary +
        '\n## Open the packet\n\n'
        f'- [Source/current index](<{PACKET.as_posix()}/index.html>)\n'
        f'- [Comic/sketch recognition sheet](<{PACKET.as_posix()}/comic_recognition_overview.png>)\n'
        f'- [Six-control recognition sheet](<{PACKET.as_posix()}/control_recognition_comparison.png>)\n\n'
        'The index links every complete original/current PNG. The overview thumbnails are '
        'for recognition; they cannot prove small-text readability. Raw comics are320x240 '
        'stored RGB interpretations. Control palette banks are documented fixture choices, '
        'not identified intended palettes. Other paletted previews use bank0. No runtime '
        'transparency or scene is fabricated. The small crops are enlarged by integer steps.\n\n'
        '## Missing information\n\n'
        'The async question asks where the original DS game displays the pictured comics, '
        'requesting a menu/event name, screenshot or save. Recognition from another version '
        'can be reported without being treated as proof of DS use. An unknown or absent '
        'response will not be converted into an unused-art decision or permission to remove '
        'the native-context requirements. The existing scope is preserved.\n\n'
        'The packet also provides concrete controls/cards/legacy pictures for later context '
        'identification. Previously verified generic-widget, original-reader, native crop and '
        'source-review evidence carries forward. This packet repeats none of those tests as '
        'new gameplay and gives no publication/guide or canonical approval.\n\n'
        '## Remaining goal\n\n'
        'Original comic playback/readability, normal small-control and village-card contexts, '
        'remaining legacy consumers, and final integrated review remain open. The eighteen '
        'overall plaque/hint objects remain incomplete with accepted material recorded. '
        'Four low-resolution Online bodies stay excluded; brown marks remain preserved. '
        'Revisit older record-based checks only after actual full-goal completion.\n',
        encoding='utf-8')
    heading = '## V739: concrete unresolved display-context packet'
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, proof_path, ROOT / 'packet_validation.json',
                 Path(__file__), Path('scripts/prepare_display_context_packet_v739.py')):
        copy(path, PACKET / 'evidence' / path.parent.name / path.name)
    for row in snapshots.values():
        path = Path(row['path'])
        copy(path, PACKET / 'evidence' / path.name)
    save(PACKET / 'provenance.json', {
        'files': {str(p.relative_to(PACKET)).replace('\\', '/'): sha(p.read_bytes())
                  for p in PACKET.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'all_are_decoded_artwork_or_metadata_not_new_native_captures': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(PACKET / 'provenance.json')['files'].items():
        assert sha((PACKET / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V739 recorded:concrete context packet and pending information question; all existing scopes/ROM preserved.', flush=True)


if __name__ == '__main__':
    main()
