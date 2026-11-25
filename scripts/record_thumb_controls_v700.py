"""Record bounded Thumb leads and actual unmapped I/O without closing UI gaps."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_person_gender_v698 import CAP
from scripts.run_person_gender_v698 import ROOT as PERSON_ROOT
from scripts.trace_thumb_controls_v700 import ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V700 Thumb controls and replay IO')
DOC = Path('docs/thumb_controls_v700_checkpoint.md')
KEY = 'bounded_Thumb8527_literal_seeds_no_new_control_parent_exact_V698_unmapped_IO_v700'
SOURCES = ('scripts/trace_thumb_controls_v700.py', 'scripts/diagnose_person_prefix_io_v700.py',
    'scripts/record_thumb_controls_v700.py', 'scripts/verify_thumb_controls_archive_v700.py',
    'scripts/trace_control_aliases_v688.py', 'scripts/replay_person_gender_v698.py')
REGISTER_HEADER = Path('work/analysis/ending_gpu_state_v630/desmume-95b4d79/desmume/src/registers.h')


def main():
    pp, ip = ROOT / 'proof.json', ROOT / 'native_IO_diagnostic.json'
    proof, io, pre = read(pp), read(ip), read(ROOT / 'preflight.json')
    assert proof['analyzer_sha256'] == sha(Path('scripts/trace_thumb_controls_v700.py').read_bytes())
    assert io['diagnostic_sha256'] == sha(Path('scripts/diagnose_person_prefix_io_v700.py').read_bytes())
    assert io['replayer_sha256'] == sha(Path('scripts/replay_person_gender_v698.py').read_bytes())
    assert io['source_preflight_sha256'] == sha((PERSON_ROOT / 'preflight.json').read_bytes())
    assert all(not v['owner_candidates'] for v in proof['versions'].values())
    totals = {n: sum(r['Thumb_literal_seed_candidates'] for r in v['sections']) for n, v in proof['versions'].items()}
    assert totals == {'source': 3996, 'current': 4531}
    controls = proof['controls']
    assert len(controls['original_ARM946_Thumb_native_controls']) == 3
    assert len(controls['negative_chain_boundaries']) == 3 and len(controls['exact20_byte_owner_boundary_controls']) == 6
    assert len(io['unmapped_accesses']) == 1 and io['unmapped_accesses'][0]['address'] == 0x04000204
    assert io['failure'] == read(PERSON_ROOT / 'native_flag0_call1_failure.json')
    header = REGISTER_HEADER.read_text(encoding='utf-8')
    assert '#define REG_EXMEMCNT 0x04000204' in ' '.join(header.split())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'IO_diagnostic': str(ip), 'IO_diagnostic_sha256': sha(ip.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'all8527_Thumb_literal_seeds_bounded_constant_chains_no_new_owner_lead': True,
        'three_native_full_register_CPSR_PC_RAM_calibrations_three_negatives_six_boundaries_pass': True,
        'V698_first_stop_is_original_unmapped_halfword_read_of_DS_EXMEMCNT_04000204': True,
        'no_IO_value_invented_no_prefix_equivalence_or_production_defect_claim': True,
        'six_control_contexts_dynamic_aliases_and_V694_suffix_gap_remain_open': True,
        'all18_plaques_incomplete22_historical_scopes_and_full_goal_preserved': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V700: bounded Thumb control paths and the first replay I/O failure'
    addition = (
        'Previous goal turn made progress with V698/V699. The previously excluded '
        'Thumb path adds8527 literal seeds across761472 clean/887198 current '
        'halfword positions. Up to24 constant instructions per seed yield no new '
        'Confirm/Frame owner. Three native full-register/CPSR/PC/4MiB calibrations, '
        'three negative boundaries and six exact20-byte owner controls pass; '
        'initial SVC/system SP/LR calibration error retained and corrected. Dynamic '
        'pointers/cross-call/other readers remain open; no new ordinary control '
        'or GPU credit. An unchanged V698 replay with non-substituting invalid-read '
        'observation reproduces its exact first stop at020E31E4 reading two bytes '
        'from04000204. Original clean/current literal and retained core header bind '
        'this to DS EXMEMCNT I/O absent from the standalone mapping. No I/O value '
        'invented,production defect inferred,prefix equivalence or V694 suffix '
        'clearance claimed. All18 plaques incomplete,22 historical scopes exact '
        'and broader graphics/older checks/acceptance open. V692/patch/registry/'
        'pointers unchanged; evidence on E,no guide promotion/commit/push. Full '
        'goal active. See [V700 checkpoint](thumb_controls_v700_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC, REGISTER_HEADER):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    external = {}
    ep = CAP / 'person_gender_v698_screen1_flag0_observed/observer/events.json'
    for path in (ep, PERSON_ROOT / 'proof.json', PERSON_ROOT / 'native_flag0_call1_failure.json'):
        external[str(path)] = sha(path.read_bytes())
    for row in read(ep)['rows']:
        if row['call'] == 1:
            for field in ('RAM', 'DTCM', 'ITCM'):
                path = Path(row[field])
                assert sha(path.read_bytes()) == row[field + '_sha256']
                external[str(path)] = row[field + '_sha256']
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external,
        'bounded_lead_search_and_failure_diagnostic_not_new_gameplay_or_GPU': True, 'full_goal_complete': False})
    print('V700 bounded Thumb search and exact replay I/O stop recorded; six actual control contexts remain open.', flush=True)


if __name__ == '__main__':
    main()
