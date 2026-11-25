"""Preserve the failed registered build and isolate its one exact manifest-list mismatch."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael516_manifest_separator_failure_v1_20261105')
BUILD=Path('work/analysis/Rafael516_registered_build_v1_20261105')
CONFIG=Path('translations/ascii_bounds_Rafael516_release_v1.json')
if __name__=='__main__':
    assert not ROOT.exists()
    terminal,config=map(load,[BUILD/'completion.json',CONFIG])
    assert terminal['terminal'] and not terminal['driver_completed_without_exception']
    assert terminal['all_original_driver_andregistry_bytes_unchanged'] and not terminal['garbage_collection']['errors']
    paths=list(Path('work/r516').rglob('canonical_reconstruction_stage.manifest.json'));assert len(paths)==1
    actual_path=paths[0];stage=actual_path.with_suffix('.nds')
    assert stage.name=='canonical_reconstruction_stage.manifest.nds'
    stage=actual_path.with_name('canonical_reconstruction_stage.nds')
    expected_path=Path(config['parent_manifest']);actual,expected=map(load,[actual_path,expected_path])
    assert sha(stage.read_bytes())==config['parent_ROM_sha256']==actual['candidate_sha256']
    assert all(actual['checks'].values()) and actual['required_batches']==expected['required_batches']
    assert actual['base_sha256']==expected['base_sha256']
    assert actual['release_stack_sha256']==terminal['registry_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(actual['batches'])==len(expected['batches'])==672
    differences=[dict(index=i,actual=a,expected=b) for i,(a,b) in enumerate(zip(actual['batches'],expected['batches'],strict=True)) if a!=b]
    assert differences==[dict(index=670,actual='translations\\rafael_B85_B100_contextual_final_review_v1.json',expected='translations/rafael_B85_B100_contextual_final_review_v1.json')]
    assert [p.replace('\\','/') for p in actual['batches']]==[p.replace('\\','/') for p in expected['batches']]
    assert not Path('out/all_routes_combined_rafael516_20261105_candidate.nds').exists()
    ROOT.mkdir(parents=True)
    save(ROOT/'failure_analysis.json',dict(build_terminal=str(BUILD/'completion.json'),terminal_exit_code=1,
        canonical_stage=str(stage),canonical_stage_sha256=sha(stage.read_bytes()),
        canonical_manifest=str(actual_path),canonical_manifest_sha256=sha(actual_path.read_bytes()),
        expected_manifest=str(expected_path),expected_manifest_sha256=sha(expected_path.read_bytes()),
        canonical_batch_entries=672,canonical_all_checks_pass=True,exact_expected_canonical_ROM_identity=True,
        required_batch_list_andbase_identity_exact=True,manifest_list_differences=differences,
        only_difference_is_one_Windows_separator_in_same_registered_manuscript_reference=True,
        original_failure_original_config_andexpected_contract_all_preserved=True,
        no_final_candidate_no_eight_stage_completion_no_release_orcredit=True,
        next_action='Prepare a source-locked registered continuation from this verified canonical stage with a versioned corrected manifest contract;retain all original stage guards,inverses andstartup checks. Do not rerun the102-minute canonical reconstruction merely for the separator and do not edit the frozen expected contract in place.',
        full_goal_complete=False,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [BUILD/'completion.json',BUILD/'failure_traceback.txt',CONFIG,expected_path,actual_path,Path(__file__)]}))
    print('Isolated one manifest separator mismatch at670/672;canonical ROM exact andall canonical checks pass. No final candidate or credit. Preserve canonical stage for guarded registered continuation.')
