"""Record final embedded-copy protection without granting display-context credit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.verify_graphics_copy_contract_v737 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/graphics_copy_contract_v737_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V737 Final graphics copy preservation')
KEY = 'final_registered_embedded_graphics_copy_preservation_v737'
PREVIOUS = 'current_original18_plaque_and22_requirement_reconciliation_v736'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    for kind, path in (('module', 'dk4tool/graphics/copy_contract.py'),
                       ('builder', 'scripts/build_integrated_release.py'),
                       ('verifier', 'scripts/verify_graphics_copy_contract_v737.py')):
        assert sha(Path(path).read_bytes()) == proof[kind + '_sha256']
    assert len(proof['all12_meaningful_corruption_controls']) == 12
    assert all(r['previous_final_gates_accept'] and r['new_copy_gate_rejects']
               for r in proof['all12_meaningful_corruption_controls'])
    assert proof['complete_rebuild_byte_exact_current_V712']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    snapshots = {}
    for live, filename in ((MATRIX, 'graphics_requirements_at_V736.json'),
                           (LEDGER, 'graphics_work_at_V736.json')):
        path = ROOT / filename
        assert not path.exists()
        path.write_bytes(live.read_bytes())
        snapshots[str(live)] = {'path': str(path), 'sha256': sha(path.read_bytes())}
    assert all(d[PREVIOUS]['current_matrix_sha256'] == snapshots[str(MATRIX)]['sha256'] and
               d[PREVIOUS]['current_work_ledger_sha256'] == snapshots[str(LEDGER)]['sha256']
               for d in before.values())
    ledger, matrix = read(LEDGER), read(MATRIX)
    assert len(ledger['completed_work_carried_forward']) == 27
    ledger['completed_work_carried_forward'].append({
        'id': 'final-registered-embedded-graphics-copy-preservation',
        'task': 'Final preservation gate for five registered graphics copies and their source metadata',
        'evidence': str(proof_path), 'evidence_sha256': sha(proof_path.read_bytes()),
        'scope': ('Five copies across CMMNIMG/SLACKIMG/DSOBJR;12 meaningful late-corruption '
                  'controls fail only the new final gate. Whole470-batch rebuild exact V712. '
                  'Final metadata/palette/prefix preservation and explicit raw19 delegation; '
                  'not original consumers, native readability or visual acceptance.'),
        'queue_status': 'complete-not-in-active-queue'})
    ledger['completed_scope_count'] = 28
    ledger['latest_evidence_checkpoint'] = 'V737 final registered graphics copy preservation'
    assert len(ledger['active_remaining_tasks']) == 5
    save(LEDGER, ledger)
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
             'final_copy_preservation_enforced_in_builder': True,
             'five_registered_copies_three_files': True,
             'original_consumers_and_full_goal_not_inferred': True}
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V736_matrix_snapshot'] = snapshots[str(MATRIX)]
    matrix['latest_evidence_checkpoint'] = ledger['latest_evidence_checkpoint']
    matrix['final_registered_graphics_copy_preservation_v737'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
             'current_matrix_sha256': sha(MATRIX.read_bytes()), 'current_work_ledger': str(LEDGER),
             'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
             'immutable_V736_snapshots': snapshots,
             'all18_original_incomplete_objects22_historical_requirements_exact': True,
             'archive': str(ARCHIVE), 'full_goal_complete': False}
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
        'The final builder now verifies all five registered embedded graphics copies after '
        'later stages: complete Marker/Frame halves, name-entry plaques, Press a button and '
        'the four-bank START/touch prompt. Source allocation/directories/headers, palettes, '
        'unowned blocks and OBJ prefix/suffix/padding are protected; raw19 stays explicitly '
        'delegated to the adjacent final raw-art gate. Twelve in-memory glyph/symbol/palette/'
        'header/Japanese-reversion/bank/padding/prefix and matching-both-copy corruptions pass '
        'the older final checks and fail the new gate. No damaged ROM saved. Legitimate later '
        'Marker/name-gradient changes follow registered source-to-target config chains. '
        'Full470-batch/114-layer registered reproduction is byte-exact V712; previous paths, '
        'records, relocations and checks remain exact. Original manifest/patch/registry/canonical '
        'and art unchanged; reproduction manifest records the added gate. No new gameplay or '
        'consumer/readability credit. Twenty-eight completed checks carry forward; five groups '
        'and original18/22 audit objects remain open/exact. E evidence archive verified; goal '
        'active, exclusions/marks/older-record follow-up retained. See '
        '[V737 checkpoint](graphics_copy_contract_v737_checkpoint.md).\n')
    DOC.write_text(
        '# V737: final registered graphics copy preservation\n\n' + summary +
        '\n## Confirmed gap and correction\n\n'
        'The old final menu, plaque and raw-comic checks accepted a changed embedded Frame '
        'caption pixel. That was a missing final guard, not a discovered defect in the unchanged '
        'V712 ROM. The sync stages already checked their own outputs; a later stage could still '
        'overwrite those copies afterward. The new read-only guard runs after all release stages.\n\n'
        '`dk4tool/graphics/copy_contract.py` derives its families from the selected batches. '
        'It compares all packed pixels against final loose PXLs, reconstructs original unowned '
        'storage and metadata, and independently maps each banked destination byte back to the '
        'logical source pixels. The early sync reference hashes legitimately precede Marker '
        'price/header repairs and name gradients; selected source/target-locked configs provide '
        'the exact transition chains. No final hash is silently exempted.\n\n'
        'The rebuild uses the existing registered `all-routes-unified-v712` profile and all '
        '470 batches/114 accepted layers. It is a reproduction artifact on E, not a new release '
        'or canonical promotion. Its ROM bytes equal the existing candidate, so the existing '
        'exact V712 patch and visual evidence remain applicable; no redundant emulator run is '
        'claimed. Only the reproduction manifest gains the new preservation result.\n\n'
        '## Scope still open\n\n'
        'Original comic playback/readability, ordinary small-control and village-card triggers, '
        'other legacy display relationships, and final user review remain unresolved. These '
        'checks establish preservation, not availability or native display behavior. Original '
        '18 overall plaque/hint objects remain incomplete. Online body exclusions and approved '
        'brown marks are preserved; older record-based review remains due after goal completion.\n',
        encoding='utf-8')
    heading = '## V737: final registered graphics copy preservation'
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        if name == 'graphics_remaining_work.md':
            text = text.replace('Twenty-seven completed checks carry forward.',
                                'Twenty-eight completed checks carry forward.', 1)
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, proof_path, ROOT / 'gap.json', ROOT / 'current_contract.json',
                 ROOT / 'rebuild.log', Path(proof['rebuild_manifest']), Path(__file__),
                 Path('scripts/verify_graphics_copy_contract_v737.py'),
                 Path('scripts/build_integrated_release.py'), Path('dk4tool/graphics/copy_contract.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    for row in snapshots.values():
        path = Path(row['path'])
        copy(path, ARCHIVE / path.name)
    save(ARCHIVE / 'provenance.json', {
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'no_new_gameplay_screenshots_or_damaged_ROMs': True, 'publication_approved': False,
        'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V737 recorded: final copy gate enforced,28 checks carried,production ROM/art exact; original contexts remain open.', flush=True)


if __name__ == '__main__':
    main()
