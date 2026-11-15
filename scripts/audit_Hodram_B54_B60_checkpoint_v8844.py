"""Independently verify additive progress,inverse preservation andthe82 five-gate decisions."""
import sys
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_checkpoint_v8843')
KEY='Hodram_SC1B54_B60_82_production_policy_reconstruction_native_references_controls_loaders_pending_actual_atomic_release_v8843'
SCOPE='unfinished_editorial_scope_v8843'

if __name__=='__main__':
    mode=sys.argv[1];assert mode in ['stage','verify'];m=read(ROOT/'stage_manifest.json');old=read(ROOT/'ledger_before.json');new=read(ROOT/'ledger_staged.json')
    assert sha((ROOT/'ledger_before.json').read_bytes())==m['ledger_before_sha256'] and sha((ROOT/'ledger_staged.json').read_bytes())==m['ledger_staged_sha256']
    assert set(new)-set(old)=={KEY,SCOPE} and not set(old)-set(new)
    inverse=deepcopy(new);del inverse[KEY];del inverse[SCOPE];inverse['latest_checkpoint']=old['latest_checkpoint']
    assert inverse['research_checkpoints'][:-1]==old['research_checkpoints'];inverse['research_checkpoints']=old['research_checkpoints'];assert inverse==old
    assert new['goal_status']=='active' and not new['full_goal_complete'] and new['current_integrated_candidate']==old['current_integrated_candidate']
    assert [new[k] for k in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed']]==[7237,4492,2745]
    scope=read(new[SCOPE]['path']);assert scope.pop(KEY)==new[KEY] and scope==read(ROOT/'scope_before.json')
    assert sha((ROOT/'scope_before.json').read_bytes())==m['scope_before_sha256'] and sha(Path(new[SCOPE]['path']).read_bytes())==new[SCOPE]['sha256']
    for r in m['documents']:
        before,staged=Path(r['before']).read_bytes(),Path(r['staged']).read_bytes()
        assert sha(before)==r['before_sha256'] and sha(staged)==r['staged_sha256'] and staged[r['prefix_bytes']:]==before
    pending=new[KEY];doc=read(pending['manuscript']);names=read(pending['names']);approval=read(pending['formatting']);actual=read(pending['actual_review'])
    assert pending['new_credit']==0 and not pending['new_registered_ROM'] and pending['research_ROMs_preserved']==13
    validate_natural_dialogue_batch(doc)
    assert len(doc['records'])==len(pending['records'])==82 and doc['revised']==46 and doc['retained']==36
    assert len(names['records'])==10 and all(all(r['review'][k] is True for k in ['source','context','localization','naturalness','formatting']) for r in names['records'])
    completed={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};source_keys={historical_key(r) for r in doc['records']}
    assert len(source_keys)==82 and len(completed)==7237 and not source_keys&completed
    for a,b in zip(doc['records'],pending['records'],strict=True):
        assert all(a[k]==v for k,v in b.items()) and all(a['review'].values()) and a['source_reference'] and a['current_reference'] and a['final_reference']
        assert a['final_hex']==a['stored_hex'] and bytes.fromhex(a['final_hex'])==bytes.fromhex(a['compiled_hex'])+(b' ' if a['compiler_owned_parity_space'] else b'')
        assert a['retention_reason'] if a['decision']=='retention' else a['finding']
    assert (actual['total_runs'],actual['total_frames'],actual['total_holds'])==(14,130014,676)
    assert (actual['total_main_runs'],actual['total_main_frames'],actual['total_main_holds'],actual['total_main_observed_page_occurrences'])==(12,116012,580,129)
    assert len(actual['actual_unique_text_IDs'])==63 and len(actual['offline_only_text_IDs'])==19
    assert set(actual['actual_unique_text_IDs'])|set(actual['offline_only_text_IDs'])=={r['id'] for r in doc['records']}
    assert actual['all27_main_dialogue_transition_andfocused_transition_sheets_directly_viewed'] and len(actual['viewed_sheets'])==27
    assert actual['focused_PRNG_and11later_RGB_pairs_still_differ_andlong_actor_divergence_not_erased'] and actual['main_WRAM_not_saved_by_boundary_native_exports_no_immediate_return_actor_snapshot_claim']
    assert actual['focused_final7001_matches_all_five_components_wholeactors_captain_andrawcalendar']
    for s in actual['viewed_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    assert approval['standard_natural_dialogue_v2_validation_pass'] and approval['all82_five_gates_true'] and approval['warnings']==approval['waivers']==0
    assert names['full_name_shared_de_ownership_deployment_andconsumers_still_open'] and doc['source_macro_counts']==dict(FI=3,FA=4,FO=0)
    for path,digest in {**m['protected_files'],**m['evidence']}.items():assert sha(Path(path).read_bytes())==digest
    production={k:read(p) for k,p in pending['production_proofs'].items()}
    assert set(production)=={'policy','reconstruction','references','native','controls','loaders'}
    assert [production[k]['negative_count'] for k in ['policy','reconstruction','references','native','controls','loaders']]==[625,161,25,12,12,11]
    assert sum(p['negative_count'] for p in production.values())==pending['production_negative_count']==846
    assert len(production['policy']['positive_speech_compilers'])==82 and production['policy']['reused_positive_compilers']==80 and production['policy']['fresh_positive_compilers']==2
    assert production['policy']['reused_negative_cases']==542 and production['policy']['fresh_negative_cases']==83
    assert len(production['reconstruction']['positive_blocks'])==7 and production['reconstruction']['positive_complete_archive_andwhole_NDS']
    assert production['references']['reference_summary']['editorial_references']==82 and production['references']['reference_summary']['commands']==152
    assert production['native']['native_summary']['native_body_pages_recomputed']==167 and production['native']['native_summary']['scoped_style11_nameplanes_recomputed']==10
    assert [production['controls']['native_control_summary'][k] for k in ['independent_final_dispatches','relative_sites','native_relative_cases','raw_query_cases','original_EV1_entries','opaque_structural_decode_pairs','normal_seeded_ends','original_result_channel_cases']]==[82,24,120,6,13,33,175,50]
    assert [production['loaders']['loader_summary'][k] for k in ['native_whole_loads_cache_hits_bound','initial_parent_modes_bound','fresh_parent_cases','exact_reused_parent_cases','original_EV1_actions_bound']]==[325,650,14,636,326]
    for p in production.values():
        assert not p['new_credit'] and not p['full_goal_complete']
        assert all(c['actual_changed_input'] and c['rejected'] and c['diagnostic'] for c in p['negative_cases'])
    from dk4tool.dialogue.hodram_B54_B60_profile_v1 import validate_approved_batch
    validate_approved_batch(doc)
    report=dict(six_production_groups_846_actual_changed_input_rejections_verified=True,stage_manifest_sha256=sha((ROOT/'stage_manifest.json').read_bytes()),whole_prior_ledger_andall_scope_values_inverse_exact=True,
        all_prior_document_bytes_preserved=True,all_counts_completedfamilies_andregistered_release_artifacts_unchanged=True,
        standard_v2_andall82individual_fivegates_source_current_final_refs_pass=True,actual_unique63_offline19_andall_measured_limits_preserved=True,
        total_actual_runs=14,total_actual_frames=130014,new_completion_credit=0,full_goal_complete=False,goal_status='active',
        auditor=str(Path(__file__)),auditor_sha256=sha(Path(__file__).read_bytes()))
    report['pass']=True
    if mode=='stage':
        assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==m['ledger_before_sha256']
        for r in m['documents']:assert sha(Path(r['path']).read_bytes())==r['before_sha256']
        save(ROOT/'independent_staged_audit.json',report);print('Independent V8843 audit passes:whole historical inverses,82fivegate decisions,63actual/19offline,alllimits/registered artifacts preserved.')
    else:
        assert sha(Path('translations/editorial_review_current_v1.json').read_bytes())==m['ledger_staged_sha256']
        for r in m['documents']:assert sha(Path(r['path']).read_bytes())==r['staged_sha256']
        assert sha(Path('docs/editorial_Hodram_B54_B60_v8843.md').read_bytes())==m['checkpoint_doc_sha256']
        report.update(ledger_sha256=m['ledger_staged_sha256'],candidate_sha256=old['current_integrated_candidate']['sha256'],completed=7237,credited_source_prose_anddrafts=7240,next_scope=KEY,
            latest_manuscript=pending['manuscript'],latest_names=pending['names'],production_atomic_registered_cleanpatch_startup_andonceonly82_credit_pending=True)
        save(ROOT/'verified_handoff_v8844.json',report);print('Verified V8843 handoff/current V8778;82fivegate decisions await production/registered integration;counts7,237 unchanged;fullgoalactive.')
