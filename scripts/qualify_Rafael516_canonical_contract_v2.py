"""Qualify the separator-only successor contract against the completed immutable canonical run."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_rafael516_registered_successor_v1 import source as old_source
from scripts.prepare_rafael516_registered_successor_v2 import source as new_source

ROOT=Path('work/analysis/Rafael516_canonical_contract_v2_20261105')
FAILURE=Path('work/analysis/Rafael516_manifest_separator_failure_v1_20261105/failure_analysis.json')
TERMINAL=Path('work/analysis/Rafael516_registered_build_v1_20261105/completion.json')
PREPARER=Path('scripts/prepare_rafael516_registered_successor_v2.py')

if __name__=='__main__':
    assert not ROOT.exists();failure,terminal=map(load,[FAILURE,TERMINAL])
    assert terminal['terminal'] and not terminal['driver_completed_without_exception'] and terminal['all_original_driver_andregistry_bytes_unchanged']
    registry=Path('translations/release_stack.json');assert sha(registry.read_bytes())==terminal['registry_sha256']
    for p,digest in terminal['driver_andcanonical_bytes'].items():assert sha(Path(p).read_bytes())==digest
    expected_path=Path(failure['expected_manifest']);actual_path=Path(failure['canonical_manifest'])
    assert sha(expected_path.read_bytes())==failure['expected_manifest_sha256'] and sha(actual_path.read_bytes())==failure['canonical_manifest_sha256']
    expected,actual=map(load,[expected_path,actual_path]);fixed=deepcopy(expected)
    assert len(expected['batches'])==len(actual['batches'])==672
    mismatches=[i for i,(a,b) in enumerate(zip(actual['batches'],expected['batches'],strict=True)) if a!=b]
    assert mismatches==[670]
    old=expected['batches'][670];new=str(Path(old))
    assert new!=old and new==actual['batches'][670]
    assert Path(old).resolve()==Path(new).resolve() and Path(old).read_bytes()==Path(new).read_bytes()
    fixed['batches'][670]=new
    assert fixed['batches']==actual['batches'] and fixed['required_batches']==actual['required_batches'] and fixed['base_sha256']==actual['base_sha256']
    assert all(fixed[k]==v for k,v in expected.items() if k!='batches') and all(actual['checks'].values())
    stage=Path(failure['canonical_stage']);assert sha(stage.read_bytes())==failure['canonical_stage_sha256']==actual['candidate_sha256']==fixed['expected_candidate_sha256']
    assert new_source==old_source.replace("contract['batches'].extend([prefix_config['manuscript'],str(final)])","contract['batches'].extend([str(Path(prefix_config['manuscript'])),str(final)])")
    ROOT.mkdir(parents=True);path=ROOT/'expected_canonical_manifest_contract_v2.json';save(path,fixed)
    save(ROOT/'qualification.json',dict(original_failure=str(FAILURE),original_failure_sha256=sha(FAILURE.read_bytes()),
        original_terminal=str(TERMINAL),original_terminal_sha256=sha(TERMINAL.read_bytes()),
        canonical_stage=str(stage),canonical_stage_sha256=sha(stage.read_bytes()),canonical_manifest=str(actual_path),canonical_manifest_sha256=sha(actual_path.read_bytes()),
        original_expected_contract=str(expected_path),original_expected_contract_sha256=sha(expected_path.read_bytes()),
        corrected_contract=str(path),corrected_contract_sha256=sha(path.read_bytes()),
        corrected_entry=dict(index=670,before=old,after=new,exact_same_source_manuscript_sha256=sha(Path(new).read_bytes())),
        all672_entries_exact_after_one_host_Path_spelling_correction=True,all_required_batches_base_canonical_checks_andROM_identity_exact=True,
        original_drivers_registry_andfrozen_expected_contract_unchanged=True,canonical_reconstruction_not_repeated=True,
        future_preparer=str(PREPARER),future_preparer_sha256=sha(PREPARER.read_bytes()),future_preparer_only_changes_same_Path_spelling=True,
        corrected_contract_not_yet_registered_for_a_new_build=True,
        no_final_candidate_no_stage_guard_bypass_no_release_orcompletion_credit=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [FAILURE,TERMINAL,expected_path,actual_path,PREPARER,Path(__file__)]}))
    print('Qualified versioned expected contract:all672 entries nowexact tocompleted canonical output;onlyhost Path spelling at670 differs. Originalfixture/registry/drivers preserved;new registration andguarded final-stage continuation still required.')
