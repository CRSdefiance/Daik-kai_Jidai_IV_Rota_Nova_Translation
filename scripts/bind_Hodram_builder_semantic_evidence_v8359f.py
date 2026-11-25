"""Bind prior semantic rejection evidence only to source-equivalent gates; separately test the new builder guard."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.hodram_outcomes_profile_v2 import contract
from dk4tool.patch.hodram_outcomes_builder_guard_v1 import BUILDER
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_builder_semantic_binding_v8359f')
NEGATIVE=Path('work/analysis/Hodram_outcomes_atomic_challenges_v8356b/actual_changing_semantic_precommit_rejections.json')
DERIVATION=Path('work/analysis/Hodram_outcome_builder_successor_tools_v8359b/original_frozen_contract_andall_semantic_validators_preserved_exact_builder_inverse_successors.json')
POSITIVE=Path('work/analysis/Hodram_outcome_atomic_positive_v8359e/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
GUARD=Path('work/analysis/Hodram_builder_inverse_validation_v8359c/exact_owned_builder_stage_full_inverse_two_positives_eight_changed_builder_rejections.json')
if __name__=='__main__':
    assert not ROOT.exists();negative,derivations,positive,guard=map(read,[NEGATIVE,DERIVATION,POSITIVE,GUARD]);assert negative['negative_count']==50 and negative['all_expected_semantic_guards_match'] and negative['all_protected_files_hash_exact']
    assert all(c['rejected'] and c['commit_calls']==0 and c['actual_input_changes_asserted'] for c in negative['cases'])
    bindings=[]
    for d in derivations['derivations']:
        before,after=Path(d['previous']),Path(d['successor']);a,b=before.read_text('utf8'),after.read_text('utf8');assert sha(before.read_bytes())==d['previous_sha256'] and sha(after.read_bytes())==d['successor_sha256']
        changes={x:y for x,y in [
            ('hodram_outcomes_profile_v1','hodram_outcomes_profile_v2'),('hodram_outcomes_layout_v1','hodram_outcomes_layout_v2'),('hodram_outcomes_names_v1','hodram_outcomes_names_v2'),('hodram_outcomes_native_guards_v1','hodram_outcomes_native_guards_v2'),('hodram_outcomes_native_evidence_v2','hodram_outcomes_native_evidence_v3'),('hodram_outcomes_controls_v1','hodram_outcomes_controls_v2'),('hodram_outcomes_editorial_release_v1','hodram_outcomes_editorial_release_v2')
        ] if x in a}
        if before.name in ['hodram_outcomes_profile_v1.py','hodram_outcomes_editorial_v1.py']:
            changes['from dk4tool.patch.grand_race_menu_release import sha']='from dk4tool.patch.grand_race_menu_release import sha\nfrom dk4tool.patch.hodram_outcomes_builder_guard_v1 import checked_dependency'
        if before.name=='hodram_outcomes_profile_v1.py':changes['if sha(Path(p).read_bytes())!=h:raise ValueError("Native dependency changed:"+p)']='if not checked_dependency(Path(p),h):raise ValueError("Native dependency changed:"+p)'
        if before.name=='hodram_outcomes_editorial_v1.py':changes["require(sha(Path(path).read_bytes())==digest,'dependency:'+path)"]="require(checked_dependency(Path(path),digest),'dependency:'+path)"
        assert checked_text(a,changes)==b
        bindings.append(dict(**d,only_explicit_import_binding_andexact_owned_builder_dependency_reader_changed=True,all_semantic_prose_native_actual_FE_controls_comparison_bodies_unchanged=True))
    assert len(bindings)==7 and len(guard['positives'])==2 and len(guard['negatives'])==8 and all(n['rejected'] for n in guard['negatives'])
    assert positive['single_complete_NDS_commit'] and positive['original_object_still_exact_after_commit'] and len(positive['report']['changed_records'])==6
    frozen=contract();old,new=map(read,['translations/hodram_outcomes_editorial_release_v1.json','translations/hodram_outcomes_editorial_release_v2.json'])
    for key in old:
        if key!='dependencies':assert old[key]==new[key],key
    assert old['dependencies'][str(BUILDER)]==frozen['dependencies'][str(BUILDER)] and str(BUILDER) not in new['dependencies']
    assert all(new['dependencies'][p]==h for p,h in old['dependencies'].items() if p!=str(BUILDER))
    ROOT.mkdir(parents=True);save(ROOT/'50_prior_semantic_rejections_bound_to_unchanged_gates_new_positive_and8_builder_rejections.json',dict(derivations=bindings,prior_semantic_cases=50,prior_semantic_cases_reused_not_rerun=True,prior_semantic_suite=str(NEGATIVE),prior_semantic_suite_sha256=sha(NEGATIVE.read_bytes()),exact_source_equivalence_ofall_semantic_checks=True,unchanged_frozen_contract_andall417_dependency_entries=True,all481_nonbuilder_prior_production_dependency_hashes_preserved=True,only_exact_owned_additive_builder_plus_whole_original_inverse_accepted=True,new_complete_atomic_positive=str(POSITIVE),new_complete_atomic_positive_sha256=sha(POSITIVE.read_bytes()),new_builder_guard_positive_count=2,new_builder_guard_negative_count=8,new_builder_guard_proof=str(GUARD),new_builder_guard_sha256=sha(GUARD.read_bytes()),no_claim_that50_prior_cases_were_rerun_under_successor=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Bound50prior semantic rejections to7source-equivalent successors;new whole-object positive/2builder positives/8changed-builder rejections.All417frozen/481nonbuilderproduction dependencies retained.No duplicate testing claim.')
