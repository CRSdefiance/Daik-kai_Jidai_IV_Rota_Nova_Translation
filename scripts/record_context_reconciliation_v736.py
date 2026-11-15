"""Close the evidence-reconciliation task while preserving all display obligations."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_graphics_contexts_v736 import LEDGER, MATRIX, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.verify_village_wrap_v608 import read, save

KEY = 'current_original18_plaque_and22_requirement_reconciliation_v736'
PREVIOUS = 'current_all24_village_progression_primary_API_requests_v735'
DOC = Path('docs/context_reconciliation_v736_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V736 Current context reconciliation')


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert len(proof['all18_current_plaque_audit_rows']) == 18
    assert len(proof['all22_historical_requirements_explicitly_owned_or_tested_complete']) == 22
    assert len(proof['all26_confirmed_asset_hashes_and_registered_batches_checked']) == 26
    assert len(proof['all13_current_native_condition_selectors']) == 13
    assert sha(Path('scripts/reconcile_graphics_contexts_v736.py').read_bytes()) == proof['verifier_sha256']
    assert sha(MATRIX.read_bytes()) == proof['matrix_before']['sha256']
    assert sha(LEDGER.read_bytes()) == proof['ledger_before']['sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    assert all(d[PREVIOUS]['current_matrix_sha256'] == proof['matrix_before']['sha256'] and
               d[PREVIOUS]['current_work_ledger_sha256'] == proof['ledger_before']['sha256']
               for d in before.values())
    ledger, matrix = read(LEDGER), read(MATRIX)
    removed = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'remaining-context-audit')
    ledger['active_remaining_tasks'].remove(removed)
    final = next(r for r in ledger['active_remaining_tasks'] if r['id'] == 'final-integrated-release-and-acceptance')
    final['remaining_scope'] += (' Retain final sign-off for all18 original plaque/hint entries and '
                                 'historical requirements18/19/21; the entry-by-entry V736 audit '
                                 'binds accepted material and tested contexts without marking the '
                                 'overall entries fully completed.')
    ledger['completed_work_carried_forward'].append({
        'id': 'original18-plaque-and22-historical-requirement-reconciliation',
        'task': 'Current entry-by-entry plaque coverage and ownership of all22 historical requirements',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': ('All26 confirmed asset entries rechecked;18 plaque rows bind source/current crops, '
                  'accepted material and tested states. Crew/condition dependency spans exact current; '
                  '13 native current condition selectors pass. This closes reconciliation only: '
                  'original18 overall objects remain incomplete; final sign-off and four actual '
                  'consumer families remain open.'),
        'queue_status': 'complete-not-in-active-queue'})
    assert len(ledger['active_remaining_tasks']) == 5
    assert len(ledger['completed_work_carried_forward']) == 27
    ledger['completed_scope_count'] = 27
    ledger['latest_evidence_checkpoint'] = 'V736 current18 plaque rows and22 requirement ownership'
    save(LEDGER, ledger)
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
             'all18_overall_entries_still_incomplete_final_review_required': True,
             'historical22_no_orphaned_obligation': True,
             'current_rows': proof['all18_current_plaque_audit_rows']}
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V735_matrix_snapshot'] = proof['matrix_before']
    matrix['latest_evidence_checkpoint'] = ledger['latest_evidence_checkpoint']
    matrix['current_original18_plaque_audit_v736'] = field
    matrix['current_historical22_remaining_work_ownership_v736'] = {
        str(r['historical_item']): r['remaining_work_owners']
        for r in proof['all22_historical_requirements_explicitly_owned_or_tested_complete']}
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
             'current_matrix': str(MATRIX), 'current_matrix_sha256': sha(MATRIX.read_bytes()),
             'current_work_ledger': str(LEDGER), 'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
             'all18_original_incomplete_objects22_historical_requirements_exact': True,
             'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        path = Path('translations') / name
        d = read(path)
        assert d == before[name]
        assert d.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert d.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        for key, ref in (('current_matrix', proof['matrix_before']), ('current_work_ledger', proof['ledger_before'])):
            d[PREVIOUS][key + '_live_path_at_recording'] = d[PREVIOUS][key]
            d[PREVIOUS][key] = ref['path']
        d[PREVIOUS]['immutable_snapshot_bytes_exact_original_recorded_hashes'] = True
        d[KEY] = entry
        save(path, d)
    summary = (
        'All22 historical requirements now have explicit remaining-work owners or a scoped '
        'completed disposition; all26 confirmed asset entries and registered batch references '
        'are hash-checked. All18 current plaque rows bind complete source/current native crops, '
        'natural terminology, accepted V715 material and their tested contexts. The current '
        'audit supersedes pending-material wording in preserved older reports. V657 crew '
        'allocation and V637 condition/skill dependencies match V712;13 complete current '
        'condition selector calls pass with actor-layout inputs and unchanged whole4MiB RAM/ABI. '
        'Prototype state-enum argument corrected to actor-pointer contract; no ROM fix. '
        'No new emulator runs or broad every-actor/fleet/acquisition claim. Reconciliation leaves '
        'the active queue:27 completed checks, four unresolved consumer families plus final '
        'integration/sign-off. Original18 overall objects stay incomplete and all22 historical '
        'objects exact. Existing exclusions, marks and post-goal older-record follow-up retained. '
        'Release/art/saves unchanged. See [V736 checkpoint](context_reconciliation_v736_checkpoint.md).\n')
    lines = ['# V736: current context and plaque reconciliation', '', summary,
             '## Original18 current audit', '',
             '| Screen | Current English | Material/borders | Remaining |',
             '|---|---|---|---|']
    for r in proof['all18_current_plaque_audit_rows']:
        lines.append(f"| {r['screen']} | {r['English']} | User accepted; current bytes exact | Final sign-off; overall incomplete |")
    lines.extend(['', '## Historical requirement ownership', '',
                  '| Historical item | Remaining work owners |', '|---|---|'])
    for r in proof['all22_historical_requirements_explicitly_owned_or_tested_complete']:
        owners = ', '.join(r['remaining_work_owners']) or 'Tested scope complete; limits retained'
        lines.append(f"| {r['historical_item']} | {owners} |")
    lines.extend(['', '## Verification limits', '',
                  'This is an evidence/dependency reconciliation with thirteen isolated current native ',
                  'selector calls, not a new gameplay capture or a claim about every actor, ship, ',
                  'inventory, acquisition, timing or hardware combination. Historical condition and ',
                  'crew-policy runs retain their original ROM and fixture scope. Native selectors ',
                  'receive a guarded actor-layout input and the current V730 exported RAM/string pool. ',
                  'All executed selector instructions match current code; full4MiB RAM and original ',
                  'saved-register/stack ABI remain exact across each call.', '',
                  'Original18 and22 historical objects are preserved unchanged. The current rows ',
                  'carry user material acceptance forward and assign final sign-off; they do not ',
                  'mark those overall objects fully completed. Original comic, small-control, card ',
                  'and legacy consumer work remains open. V712 remains experimental; no canonical ',
                  'promotion, guide/publication approval or full-goal completion is claimed.', ''])
    DOC.write_text('\n'.join(lines), encoding='utf-8')
    heading = '## V736: current18 plaque audit and22 requirement ownership'
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        if name == 'graphics_remaining_work.md':
            _, tail = text.split('## Current requirement matrix', 1)
            intro = ['# Graphics: remaining work', '',
                     'Twenty-seven completed checks carry forward. Four concrete consumer families',
                     'and the final integrated review remain. Completed reconciliation is archived.', '']
            for n, task in enumerate(ledger['active_remaining_tasks'], 1):
                intro.extend([f"{n}. {task['remaining_scope']}", ''])
            intro.extend(['All18 original plaque/hint objects remain in the final audit, incomplete.',
                          'Their accepted material and tested contexts carry forward in the V736 rows.',
                          'The four low-resolution Online bodies remain excluded; preserve approved brown',
                          'marks. Reopen completed checks only for changed dependencies, contradictory',
                          'evidence or required integration gates. Revisit older record-based checks',
                          'after actual full-goal completion. The graphics goal remains active.', '',
                          '## Current requirement matrix' + tail])
            text = '\n'.join(intro)
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, proof_path, Path(proof['matrix_before']['path']),
                 Path(proof['ledger_before']['path']), Path(__file__),
                 Path('scripts/reconcile_graphics_contexts_v736.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    review = read('work/analysis/plaque_review_v714/current_plaque_review_proof.json')
    for row in review['all18_current_native_review_entries']:
        for field in ('source_crop', 'current_crop'):
            path = Path(row[field])
            copy(path, ARCHIVE / 'verified_existing_native_crops' / path.name)
    save(ARCHIVE / 'provenance.json', {
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'reconciliation_and_existing_crops_not_new_gameplay_captures': True,
        'publication_approved': False, 'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V736 recorded:27 carried completed checks;5 remaining groups,original18/22 preserved; release unchanged.', flush=True)


if __name__ == '__main__':
    main()
