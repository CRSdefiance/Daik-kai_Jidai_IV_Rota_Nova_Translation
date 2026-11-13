"""Close the bounded indexed-owner lead without granting display coverage."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.trace_indexed_owners_v738 import ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/indexed_owners_v738_checkpoint.md')
MATRIX = Path('translations/graphics_current_requirements_v1.json')
LEDGER = Path('translations/graphics_current_work_v1.json')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V738 Indexed resource owner leads')
KEY = 'bounded_indexed_resource_owner_lead_v738'
PREVIOUS = 'final_registered_embedded_graphics_copy_preservation_v737'


def main():
    proof_path = ROOT / 'proof.json'
    proof = read(proof_path)
    assert len(proof['versions']) == 2 and len(proof['all21_owner_targets_accounted']) == 21
    for key, filename in (('producer', 'trace_indexed_owners_v738.py'), ('verifier', 'verify_indexed_owners_v738.py')):
        assert proof[key + '_sha256'] == sha((Path('scripts') / filename).read_bytes())
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    before = {name: read(Path('translations') / name) for name in frozen}
    assert all(KEY not in d for d in before.values())
    snapshots = {}
    for live, name in ((MATRIX, 'graphics_requirements_at_V737.json'), (LEDGER, 'graphics_work_at_V737.json')):
        path = ROOT / name
        assert not path.exists()
        path.write_bytes(live.read_bytes())
        snapshots[str(live)] = {'path': str(path), 'sha256': sha(path.read_bytes())}
    assert all(d[PREVIOUS]['current_matrix_sha256'] == snapshots[str(MATRIX)]['sha256'] and
               d[PREVIOUS]['current_work_ledger_sha256'] == snapshots[str(LEDGER)]['sha256']
               for d in before.values())
    ledger, matrix = read(LEDGER), read(MATRIX)
    assert len(ledger['completed_work_carried_forward']) == 28 and len(ledger['active_remaining_tasks']) == 5
    ledger['closed_consumer_leads'].append({
        'id': 'bounded-indexed-AL-resource-owner-lead', 'evidence': str(proof_path),
        'sha256': sha(proof_path.read_bytes()),
        'result': ('One seamap address match needs index102 in a64-byte-object helper. '
                   'Both direct callers supply1; original initialization covers two objects. '
                   'This is not an identified graphics consumer.'),
        'scope': ('21 owner targets,one-variable straight-line AL arithmetic/source tables, '
                  'supplied indices0..255. Current/clean controlled native calibration and '
                  'source prefixes pass. Other domains,unaligned rotations,Thumb variable '
                  'flow,runtime tables,opaque and computed indirect paths remain unverified.')})
    ledger['latest_evidence_checkpoint'] = 'V738 bounded indexed resource owner lead resolved'
    save(LEDGER, ledger)
    field = {'proof': str(proof_path), 'sha256': sha(proof_path.read_bytes()),
             'bounded_indexed_lead_closed_not_ordinary_graphics_context': True,
             'no_completed_graphics_scope_count_increase': True}
    matrix['completed_work_ledger_sha256'] = sha(LEDGER.read_bytes())
    matrix['historical_V737_matrix_snapshot'] = snapshots[str(MATRIX)]
    matrix['latest_evidence_checkpoint'] = ledger['latest_evidence_checkpoint']
    matrix['bounded_indexed_resource_owner_lead_v738'] = field
    save(MATRIX, matrix)
    entry = {'documentation': str(DOC), **field, 'current_matrix': str(MATRIX),
             'current_matrix_sha256': sha(MATRIX.read_bytes()), 'current_work_ledger': str(LEDGER),
             'current_work_ledger_sha256': sha(LEDGER.read_bytes()),
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
        'A new one-variable AL array lead scan covers380736 clean/443599 current aligned words '
        'and21 source-initialized owners with supplied indices0..255. Both versions yield only '
        '020D2ED4:base0231220C+index*64 happens to equal seamap owner02313B8C at102. Both direct '
        'call prefixes supply1; original initialization covers two64-byte objects. Three '
        'native address prefixes and two caller prefixes per ROM pass without RAM changes. '
        'Affine/U32-wrap,indexed-table,PC-return and conservative boundary controls pass; an '
        'index256 native hit explicitly demonstrates the finite analysis limit. All315 owner '
        'initializations/writes/names/code match clean/current. No original display parent, '
        'native scene or global non-use credit. Source-tail transcription corrected to '
        'literal02100498; no ROM fix. The bounded lead is closed;28 completed graphics checks '
        'and five remaining groups unchanged. Original18/22 objects exact; E evidence checked, '
        'production release/art/saves unchanged, goal active. See '
        '[V738 checkpoint](indexed_owners_v738_checkpoint.md).\n')
    DOC.write_text(
        '# V738: bounded indexed resource owner lead\n\n' + summary +
        '\n## Distinct analysis scope\n\n'
        'Earlier searches propagated constants. This scan retains one unknown index through '
        'listed AL arithmetic and immediate left shifts, and inspects initial source tables. '
        'It checks inputs0..255 without claiming that window is an original runtime domain. '
        'Calls, branches, writes to PC, stores, predication, unknown instructions and unsupported '
        'expressions end the tracked chain. Source data can also decode as instructions; leads '
        'are hypotheses until checked. Unaligned load rotation, mutable runtime tables, multiple '
        'unknowns, other integer domains and variable Thumb flows remain outside verification.\n\n'
        'Twenty-one requested owners have exact initialized filenames and FNT paths. Missing '
        'catalogue entries and the historical misplaced Online filenames are listed separately, '
        'not silently given aliases. All315 original resource objects are initialized through '
        'unchanged native code; current/clean names, writes and executed words match.\n\n'
        '## The actual lead\n\n'
        '020D2ECC..020D2ED8 computes0231220C+index*64 and stops before its original tail '
        'target02100498. Supplied0/1/102 witnesses verify that calculation. Index102 reaches '
        'the sea-map owner numerically, but the original two-entry initialization and both '
        'direct caller prefixes provide no such selection. The two calls at020D2EA4/020D2EAC '
        'both supply1. No stored absolute or direct Thumb caller is found in these mapped '
        'source units. Computed indirect callers are not excluded. No renderer is executed.\n\n'
        '## Calibration and limits\n\n'
        'Per ROM, five complete affine native calls include U32 overflow, one indexed-source-table '
        'call returns the supplied owner, and a PC-write control returns before dead arithmetic. '
        'A native index256 hit deliberately lies outside the search window. Four conservative '
        'boundary controls forget values; they do not establish native unreachability. Sixteen '
        'complete control calls plus ten original source prefixes are isolated analysis evidence, '
        'not new gameplay captures. No source/current art, ROM, patch, registry, manifest or '
        'canonical pointer changes. All original consumer/readability requirements remain open.\n',
        encoding='utf-8')
    heading = '## V738: bounded indexed resource owner lead'
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md', 'graphics_remaining_work.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + summary, encoding='utf-8')
    for path in (DOC, MATRIX, LEDGER, Path(__file__), Path('scripts/trace_indexed_owners_v738.py'),
                 Path('scripts/verify_indexed_owners_v738.py')):
        copy(path, ARCHIVE / path.parent.name / path.name)
    for path in ROOT.iterdir():
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.name)
    save(ARCHIVE / 'provenance.json', {
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'isolated_analysis_not_new_gameplay_captures': True, 'publication_approved': False,
        'full_goal_complete': False})
    for path, digest in read(ARCHIVE / 'provenance.json')['files'].items():
        assert sha((ARCHIVE / path).read_bytes()) == digest
    for path, digest in proof['release_hashes_unchanged'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('V738 archived: bounded lead resolved,no display scope closed;28 completed checks/5 remaining groups preserved.', flush=True)


if __name__ == '__main__':
    main()
