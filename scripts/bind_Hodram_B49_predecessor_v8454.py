"""Bind exact namespace-only predecessor successors,prior aliases/challenges and current byte-exact positive."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prepare_Hodram_B49_predecessor_v8451 import SPECS
from dk4tool.patch import hodram_outcomes_editorial_v5 as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_predecessor_binding_v8454')
DERIVATION=Path('work/analysis/Hodram_B49_predecessor_tools_v8451/source_equivalence.json')
PRIOR=Path('work/analysis/Hodram_B49_predecessor_binding_v8446b/semantic_binding.json')
POSITIVE=Path('work/analysis/Hodram_outcome_atomic_positive_v8453/one_whole_NDS_commit_exact_reference_andunchanged_precommit_input.json')
GUARD=Path('work/analysis/Hodram_B49_builder_v8452/exact_builder_inverse_cases.json')
if __name__=='__main__':
    assert not ROOT.exists();derivations,prior,positive,guard=map(read,[DERIVATION,PRIOR,POSITIVE,GUARD])
    for (_,_,_,_,changes),d in zip(SPECS,derivations['derivations'],strict=True):
        a,b=Path(d['previous']),Path(d['successor']);assert sha(a.read_bytes())==d['previous_sha256'] and sha(b.read_bytes())==d['successor_sha256'] and checked_text(a.read_text('utf8'),changes)==b.read_text('utf8')
    assert prior['prior_semantic_cases']==50 and len(prior['actual_changed_oldconfig_rejections'])==4 and all(n['rejected'] for n in prior['actual_changed_oldconfig_rejections'])
    assert positive['single_complete_NDS_commit'] and positive['original_object_still_exact_after_commit'] and positive['exact_preserved_registered_v3config_alias_used']
    assert len(guard['positives'])==5 and len(guard['negative_cases'])==16 and all(n['rejected'] for n in guard['negative_cases'])
    old=read('translations/hodram_outcomes_editorial_release_v4.json');new=read(owned.CONFIG)
    assert len(old['dependencies'])==515 and len(new['dependencies'])==524 and all(new['dependencies'][p]==h for p,h in old['dependencies'].items()) and all(new[k]==old[k] for k in old if k!='dependencies')
    assert owned.resolve_config(owned.PRESERVED_CONFIG)==owned.CONFIG and owned.resolve_config(str(Path(owned.PRESERVED_CONFIG).resolve()))==owned.CONFIG and owned.resolve_config(owned.CONFIG)==owned.CONFIG
    from dk4tool.patch.hodram_outcomes_builder_guard_v5 import validate_builder_bytes
    digest=guard['full_original_source_inverse_sha256'];historical=[]
    for name in ['planned_builder.bin','current_builder.bin']:
        path=Path('work/analysis/Hodram_B49_builder_v8431b')/name;historical.append(dict(path=str(path),sha256=sha(path.read_bytes()),proof=validate_builder_bytes(path.read_bytes(),digest)))
    ROOT.mkdir(parents=True);save(ROOT/'semantic_binding.json',dict(derivations=derivations['derivations'],prior_binding=str(PRIOR),prior_binding_sha256=sha(PRIOR.read_bytes()),prior50_semantic_andfour_alias_rejections_reused_by_exact_source_equivalence_not_rerun=True,current_positive=str(POSITIVE),current_positive_sha256=sha(POSITIVE.read_bytes()),new_builder_guard=str(GUARD),new_builder_guard_sha256=sha(GUARD.read_bytes()),new_builder_positives=5,new_builder_rejections=16,historical_builder_forms=historical,all515_prior_dependencies_preserved=True,current_dependency_count=524,exact_preserved_v3_alias_andall_native_semantic_bodies_unchanged=True,no_builder_registry_ROM_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Compatible predecessorv5:7exact source bindings,all515prior pins/524current;full V8377positive,50prior semantic/four alias cases retained,5newbuilderforms16negatives plushistoricalforms pass.No credit.')
