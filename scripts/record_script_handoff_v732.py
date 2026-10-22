"""Carry the original handoff result forward without closing later VM consumers."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_script_handoff_v732 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/script_handoff_v732_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V732 Script handoff')
KEY = 'original_SC_cached_parent_handoff_and_first_instruction_read_v732'
PREVIOUS = 'original_80008000_decimal_sprite_writer_classification_v731'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_script_handoff_v732.py').read_bytes())
    assert proof['two_modes_two_ROM_original_handoff_and_first_read_cases'] == 5228
    assert proof['all2614_clean_current_first_native_word_category_and_mode_pairs_exact']
    assert proof['cases_file_sha256'] == sha((ROOT / 'native_cases.json').read_bytes())
    assert proof['prior_full_file_loader_proof_sha256'] == sha(Path(proof['prior_full_file_loader_proof']).read_bytes())
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in data for data in before.values())
    snapshot = ROOT / 'graphics_requirements_at_V731.json'
    assert not snapshot.exists()
    snapshot.write_bytes(MATRIX.read_bytes())
    old_hash = sha(snapshot.read_bytes())
    assert all(data[PREVIOUS]['current_matrix_sha256'] == old_hash for data in before.values())
    matrix, ledger = read(MATRIX), read(LEDGER)
    assert len(ledger['completed_work_carried_forward']) == 23
    assert len(ledger['active_remaining_tasks']) == 6
    lead = {'id': 'V727-original-cache-to-first-instruction-handoff', 'evidence': str(proof_path),
        'sha256': sha(proof_path.read_bytes()),
        'result': 'All1307 source blocks per ROM pass original cached-parent descriptor setup to first instruction read,with two mode values. No generation/mutation in this handoff; clean/current first words exact.',
        'scope': '5228 native handoff/read cases. Loaded cache object and active-event/scratch-parent inputs supplied; no later opcode mutation,other builder,ordinary village trigger or GPU closure.'}
    leads = ledger.setdefault('closed_consumer_leads', [])
    assert not any(r['id'] == lead['id'] for r in leads)
    leads.append(lead)
    task = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'village-and-environment-contexts')
    task['remaining_scope'] += (' V732 closes original cached-parent handoff generation before the '
        'first opcode handler: all1307 blocks per ROM,two modes,source bytes and first words exact. '
        'Do not repeat the V727 loader or this handoff; later opcode execution,other builders and '
        'separate consumers remain possible leads.')
    save(LEDGER, ledger)
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V731_matrix_snapshot'] = {'path': str(snapshot), 'sha256': old_hash}
    matrix['latest_evidence_checkpoint'] = 'V732 original SC parent handoff and first instruction read'
    matrix['current_closed_consumer_lead_v732'] = lead
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), 'closed_consumer_lead': lead,
        'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
        'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
        'V731_immutable_matrix_snapshot': {'path': str(snapshot), 'sha256': old_hash},
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
    heading = '## V732: original script cache-to-first-read handoff verified'
    summary = ('All1307 SC blocks per ROM bind to V727 exact file-loader outputs. Original cached '
        'parent setup and first instruction reads pass5228 cases across clean/current,two modes. '
        'No SDK or cache-success stub; whole source headers/bodies/padding,cache metadata and tail '
        'guards exact. All2614 first-word/category/mode pairs match. Initial declared-length assumption '
        'corrected for original zero alignment padding; no ROM defect inferred. This closes command '
        'generation in the tested handoff,not later opcode mutation,other builders,ordinary village '
        'triggers or GPU. Existing23 completed scopes/six active groups and original18/22 objects '
        'preserved. V712 release/art/saves unchanged,E records archive verified; goal active,Online '
        'exclusions,marks and older-record note retained. See [V732 checkpoint](script_handoff_v732_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, snapshot, proof_path, Path(__file__), ROOT / 'native_cases.json',
                 Path('scripts/verify_script_handoff_v732.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'isolated_native_handoff_records_not_ordinary_event_GPU_or_guide': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V732 recorded:original handoff lead closed;23 completed scopes/six groups,original18/22 and all release/E hashes exact; goal active.')


if __name__ == '__main__':
    main()
