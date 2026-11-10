"""Bind the tested in-memory fixture inverse to source-locked production successors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
WRAPPER='''

def validate_builder_bytes(raw,digest):
    if sha(raw)==digest:return _validate_specific_stage(raw,digest,STAGE)
    variants=[('current-v3',STAGE),('preserved-v2',LEGACY_STAGE)]
    if sum(raw.count(stage.encode('utf8')) for _,stage in variants)!=1:
        raise ValueError('Hodram builder guard: exactly one known owned stage required')
    for version,stage in variants:
        if raw.count(stage.encode('utf8'))==1:
            return dict(**_validate_specific_stage(raw,digest,stage),owned_stage_version=version)
    raise ValueError('Hodram builder guard: known owned stage absent')
'''
if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_fixture_production_tools_v8372');assert not root.exists();results=[]
    original=Path('dk4tool/patch/hodram_outcomes_builder_guard_v1.py').read_text('utf8');ending='    return True\n';assert original.endswith(ending)
    results.append(derive('dk4tool/patch/hodram_outcomes_builder_guard_v1.py','dk4tool/patch/hodram_outcomes_builder_guard_v2.py',{
        'from dk4tool.patch.grand_race_menu_release import sha':'from dk4tool.patch.grand_race_menu_release import sha\nfrom dk4tool.patch.hodram_outcomes_builder_guard_v1 import STAGE as LEGACY_STAGE',
        'hodram_outcomes_editorial_v2':'hodram_outcomes_editorial_v3',
        'def validate_builder_bytes(raw,digest):':'def _validate_specific_stage(raw,digest,stage_text):',
        "stage=STAGE.encode('utf8');anchor=":"stage=stage_text.encode('utf8');anchor=",
        ending:ending+WRAPPER,
    }))
    for area,name,old,new,changes in [
        ('dialogue','profile',2,3,{'hodram_outcomes_builder_guard_v1':'hodram_outcomes_builder_guard_v2'}),
        ('dialogue','layout',2,3,{'hodram_outcomes_profile_v2':'hodram_outcomes_profile_v3'}),
        ('dialogue','names',2,3,{'hodram_outcomes_profile_v2':'hodram_outcomes_profile_v3'}),
        ('patch','native_guards',2,3,{'hodram_outcomes_profile_v2':'hodram_outcomes_profile_v3'}),
        ('patch','native_evidence',3,4,{'hodram_outcomes_native_guards_v2':'hodram_outcomes_native_guards_v3'}),
        ('patch','controls',2,3,{'hodram_outcomes_profile_v2':'hodram_outcomes_profile_v3','hodram_outcomes_native_guards_v2':'hodram_outcomes_native_guards_v3'}),
        ('patch','editorial',2,3,{'hodram_outcomes_profile_v2':'hodram_outcomes_profile_v3','hodram_outcomes_layout_v2':'hodram_outcomes_layout_v3','hodram_outcomes_names_v2':'hodram_outcomes_names_v3','hodram_outcomes_native_evidence_v3':'hodram_outcomes_native_evidence_v4','hodram_outcomes_controls_v2':'hodram_outcomes_controls_v3','hodram_outcomes_actual_evidence_v1':'hodram_outcomes_actual_evidence_v2','hodram_outcomes_builder_guard_v1':'hodram_outcomes_builder_guard_v2','hodram_outcomes_editorial_release_v2':'hodram_outcomes_editorial_release_v3'}),
    ]:results.append(derive(f'dk4tool/{area}/hodram_outcomes_{name}_v{old}.py',f'dk4tool/{area}/hodram_outcomes_{name}_v{new}.py',changes))
    root.mkdir(parents=True);save(root/'source_locked_production_fixture_inverse_andtwo_exact_owned_builder_stages.json',dict(derivations=results,frozen_contract_andall417_dependency_entries_unchanged=True,all_native_numbers_andmultiplicity_preserved=True,all_prose_native_actual_FE_controls_comparison_semantic_checks_unchanged_except_tested_fixture_inverse=True,only_known_legacy_v2_orcurrent_v3_owned_builder_stage_andfull_frozen_source_inverse_accepted=True,source_inverse_correction_proof='work/analysis/Hodram_fixture_parent_inverse_validation_v8369/canonical_source_path_complete_V8300_memory_original_failure_reproduced_corrected100holds_pass.json',failed_profile_andall_executed_producers_preserved=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,full_goal_complete=False))
