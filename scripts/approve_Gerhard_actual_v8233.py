"""Approve five surname-revisit formats and one owned name asset for frozen-policy review; no integration credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_actual_approval_v8233')
OLD=Path('translations/gerhard_surname_consistency_manuscript_v1.json')
OUT=Path('translations/gerhard_surname_consistency_manuscript_v2.json')
PLAN=Path('work/analysis/Gerhard_layout_v8205/5_automatic_Lil_plans_full_native_width.json')
OWNERSHIP=Path('work/analysis/Gerhard_name_ownership_v8203/current12_byte_surname_owned_original20_contains_protected_Blades.json')
NATIVE=Path('work/analysis/Gerhard_pages_v8206/5_complete_native_paragraphs5_pages20_compiled_alignments.json')
STORED=Path('work/analysis/Gerhard_stored_v8209/5_stored_bodies4_fresh16_reused_alignments5_exact_viewed_pages.json')
RELOC=Path('work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json')
CONTROL=Path('work/analysis/Gerhard_final_controls_v8214/5_final_dispatches51_controls30_raw_evaluations150_seeded_ends.json')
REFERENCE=Path('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
CALLERS=Path('work/analysis/Gerhard_reference_census_v8223/all225_commands44_relative_sites_five_revisions_EV2_entries_shipped_callers.json')
MODELS=Path('work/analysis/Gerhard_actual_models_v8226/five_previous_body_planes_revised_exact_reuses_three_header_consumers.json')
ACTUAL=Path('work/analysis/Gerhard_actual_v8229/six_paired_runs_actual_five_surname_bodies_headers_conditions_andnormal_returns.json')
COMPARE=Path('work/analysis/Gerhard_actual_comparison_v8230b/three_actual_pairs_scene_timing_RNG_final_components_later_RGB_scope.json')
FOCUS=Path('work/analysis/Gerhard_intro_actual_focus_v8232/exact_intro_replay8_RAM_phases_bounded_later_state_andRNG_differences.json')
ASSESSMENT=(
 'Allfive revised one-page surname paragraphs andthree relevant progressive speaker labels pass actual complete first/internal/final native glyph masks:30 complete body holds and262 relevant name holds across thepaired previous/revisedEnglish tests. '
 'Allfive before/after body/name crops were directly viewed. Native model sheets2,actual changed-body sheets5,later-state sheets3 andfocused phase sheet1 were directly viewed,with exact source PNG composition verified. '
 'The full initialized B27 script selects35of51 speeches andreturns[0,0]at12415 inbothversions;its16unvisited conditional speeches include theintroduction. '
 'It later entersSC0B44 withcaptain0/party0 inbothversions. That artificial entry/tail isnot naturalStockholm activation,Lilroute continuity,earned progress orproduction-scene reachability proof. '
 'The full initialized B74 script selects75of79 speeches,including allthree corrected surname bodies and30Gerhard speaking entries,retains theoriginal menu/defaultoption0 andreturns[0,0]at22255 inbothversions. '
 'Four otherB74 speeches remainunvisited;option1 isnot individually selected. '
 'The additional B27 eight-speech introduction display fixture covers bothremaining corrected bodies;it keeps theoriginal speeches andclosingzero-skip/end,butdoesnot execute theoriginal outercondition orremaining fullB27 effects. '
 'Its normalreturns are5695previous/5694revised. No runtimecondition,result,flag,party,roster,funds,seed orcontroller retiming wasforced. '
 'All selected native results,text memberships,choice result andUIrequest words agree across eachpair. Upper-scene/portrait matches117samples (34fullB27,75fullB74,8focusedintro);onefullB27 speech lacks acommon held screenshot. '
 'Gerhard headerwidth/text intentionallychanges from120px includingflush to108px;all262 relevant nameholds matchcomplete native ink. Other tested headers remainexact. '
 'Measured command-comparison/duration-difference counts are1/0 forfullB27,74/19 forfullB74 and8/2 forfocusedintro. Do not claim identical timing orRNG phase. '
 'FullB27 later328RGBsamples andfullB74 later164RGBsamples allmatch;their finalfive queried components,wholeactors andPRNGseeds agree. FullB27 finalcaptain0 is acontextlimitation,not aLilcontinuity pass. '
 'Focusedintro later29of106RGBsamples differ;finalstate/tasks/calendar agree,butmodels,persistentobjects,wholeactors andRNGdiffer. '
 'Exact same-ROM/input/horizon focusedrepeats reproduce every observerrow exceptoutputpaths,all8 selected framebuffers andfinal wholeRAM perversion. '
 'First7RAMsamples3970/4330/4810/5770/6310/9730/10510 have equalqueriedstate/models/persistentobjects/tasks/calendar/wholeactors. RNGvalues differat9730and10510. '
 'At12000 sampled differences comprise2fleetbytes,150actorbytes and54townbytes;calendar ticks535/[0,11,7]previous versus534/[0,11,6]revised. Atfinal12001 rawcalendars both535/[0,11,7]. Rawdates remainuninterpreted. '
 'These arebounded fixture observations,not every-frame causality,futureoutcome orfull simulation equivalence. Preserve alltiming/RNG/component/byte/RGB/fixture limits forlater older-record technicalre-audit. '
 'No concrete corrected-name clipping,dropped glyph,unintended page,changedcommand,missingoriginalchoice ornormal-return defect remains in thetested scope. '
 'Formatting mayproceed to frozenpolicy,independentatomicproduction andregistered cumulative integration. Allfive speeches were already revised-and-integrated,so this correction adds no duplicate source/prose/completed/revised/retained credit. '
 'The original name20-byte allocation isnot whollyowned now:writeonly12bytes andpreserve separatelyreferenced Blades8bytes andallpointerfields. '
 'RegisteredV8172/mainV4701 areunchanged;all207 names/roles/aliases andfullcatalogue/customname UI,broad four-story/sharedtown-shop/random/Help/remainingprose/retrospectivewrap review remainopen. '
 'Pending28 Hodram bodies andtheir six-name manuscript retainseparate formatting/actual/registered gates;do not grantthose gates fromthis Lil test.'
)
if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    old,plan,ownership,native,stored,reloc,control,reference,callers,models,actual,comparison,focus=map(read,[OLD,PLAN,OWNERSHIP,NATIVE,STORED,RELOC,CONTROL,REFERENCE,CALLERS,MODELS,ACTUAL,COMPARE,FOCUS])
    assert len(old['records'])==5 and len(old['name_records'])==1 and not actual['unresolved']
    assert actual['complete_body_holds']==30 and actual['relevant_name_holds']==262 and actual['new_actual_frames']==152006
    assert focus['total_Gerhard_scene_frames_including_replay']==176008 and focus['new_actual_frames']==24002
    assert focus['all_same_ROM_input_horizon_observer_rows_selected_framebuffers_andfinal_RAM_reproduce_exactly_perversion']
    assert comparison['actual_sha256']==focus['actual_sha256']==sha(ACTUAL.read_bytes()) and focus['comparison_sha256']==sha(COMPARE.read_bytes())
    assert sorted(actual['complete_changed_body_IDs_revised'])==sorted(r['id'] for r in old['records'])
    assert stored['relocation_sha256']==control['relocation_sha256']==sha(RELOC.read_bytes()) and callers['all225_source_current_target_commands44_relative_sites_bound_to_research_ROM']
    assert reference['full_ROM_inverse_recovers_every_parent_byte'] and len(reference['all20_Adernkatz_consumers'])==20
    assert ownership['current_owned_name_span']['bytes']==12 and ownership['protected_neighbor']['text']=='Blades' and not ownership['interior_name_literal_pointer_references']
    cg={ (g['scope'],g['block']):g for g in comparison['groups'] }
    assert [(len(cg[k]['command_comparison_differences']),len(cg[k]['duration_differences'])) for k in [('whole',27),('whole',74),('intro-display',27)]]==[(1,0),(74,19),(8,2)]
    assert all(g['all_UI_request_words_equal'] and not g['upper_scene_portrait_RGB_difference_IDs'] and not g['unchanged_actor_header_RGB_difference_IDs'] for g in comparison['groups'])
    assert sum(len(g['selected_scene_andportrait_pairs']) for g in comparison['groups'])==117
    for key,count in [(('whole',27),328),(('whole',74),164)]:
        g=cg[key];assert g['later_sample_count']==count and not g['later_RGB_differences'] and all(g['five_native_component_equality'].values()) and g['whole_actors_equal']
        assert g['final_PRNG_seeds'][0]==g['final_PRNG_seeds'][1]
    g=cg['intro-display',27];assert len(g['later_RGB_differences'])==29 and g['later_sample_count']==106
    assert g['five_native_component_equality']==dict(state=True,models=False,persistent_objects=False,tasks=True,calendar=True) and not g['whole_actors_equal']
    assert all(all(r['component_equality'].values()) for r in focus['sampled_comparisons'][:7])
    assert {k:v['changed_bytes'] for k,v in focus['sampled_comparisons'][-1]['bounded_native_model_andpersistent_byte_differences'].items() if v['changed_bytes']}==dict(fleet=2,all207_actors_and_current_captain=150,all90_towns=54)
    sheets=models['review_sheets']+actual['actual_review_sheets']+comparison['review_sheets']+[focus['review_sheet']];assert len(sheets)==11
    viewed=[]
    for s in sheets:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];viewed.append(dict(**s,directly_viewed=True))
    updated=deepcopy(old)
    for row,p in zip(updated['records'],plan['records'],strict=True):
        assert row['id']==p['id'] and row['source_hex']==p['source_hex'] and row['english']==p['logical_English']
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
        assert row['already_editorially_completed'] and row['previous_credit_classification']=='revised-and-integrated'
        assert row['raw_storage_comparison_paragraph'].replace('Ardelknatts','Adernkatz')==row['english'].replace('{MACRO:FI}','FI')
        assert not any(i['severity'] in ['error','warning'] for i in p['base_QA']['issues'])
        s=next(r for r in stored['records'] if r['id']==row['id']);observations=[dict(scope=g['scope'],version=g['version'],block=g['block'],speech=r) for g in actual['groups'] for r in g['speeches'] if r['id']==row['id']]
        assert {o['version'] for o in observations}=={'parent_English','revised_English'} and all(o['speech']['complete_holds'] for o in observations)
        assert {o['scope'] for o in observations}==({'intro-display'} if row['block']==27 else {'whole'})
        row.update(compiled_hex=p['encoded_hex'],formatted_markup=p['formatted_markup'],planned_English_markup=p['planning_record']['english'],native_page_count=1,
            final_stored_hex=s['stored_hex'],final_reference=s['target_reference'],compiler_owned_parity_space=s['compiler_owned_parity_space'],
            qa_waivers=[],qa_waiver_reason=None,all_original_QA_issues=p['base_QA']['issues'],actual_display_observations=observations,
            current_effective_body_dispatch_not_yet_verified=False,current_effective_body_dispatch_andcatalogue_pending=False,
            final_formatting_approval='Complete native andactual body/name masks,safe generatedwraps,fullstored parity/inverses/control maps;tested scope andlater fixture limits recorded in8233.')
        row['review']['formatting']=True
    name=updated['name_records'][0];assert name['current_hex']==ownership['current_owned_name_span']['current_hex'] and name['target_hex']==ownership['current_owned_name_span']['target_hex']
    name.update(review=dict(source=True,context=True,localization=True,naturalness=True,formatting=True),
        source_meaning='Actor16 family nameアーデルンカッツ;one identity across thecomplete295-speech source contexts,without importing biography ornew rank.',
        context='Standardize theestablished Adernkatz alreadyused by14current consumers;five oldSC2 bodies andone ARM9 field are theonly inconsistent consumers.',
        localization_note=name['reason'],pointer_fields_ownership_unowned_bytes_native_getters_andglyphs_still_require_checks=False,
        original20byte_allocation_NOT_wholly_owned=True,current12byte_terminated_span_only=True,protected_Blades_neighbor=ownership['protected_neighbor'],
        progressive_current_andfull_getters_andactual_nameplane_evidence='8199/8200/8203/8210c/8219/8226/8229',
        full_catalogue_UI_custom_names_andall207_global_alias_review_not_claimed=True)
    previous_status=updated.pop('native_logical_layout_glyph_name_slot_alias_pointer_inverse_actual_atomic_registered_release_pending')
    updated.update(prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),historical_v1_combined_pending_flag=previous_status,
        status='source-context-prose-native-stored-reference-scoped-actual-approved-pending-frozen-policy-atomic-registered-release',
        native_logical_layout_glyph_name_slot_alias_pointer_inverse_andscoped_actual_checks_passed=True,
        actual_approval=str(ROOT/'scoped_actual_format_approval.json'),registered_release_pending=True,frozen_policy_andindependent_atomic_pending=True,
        full_goal_completed_record_credit=0,unique_revision_andretention_totals_unchanged=True,actual_scope_assessment=ASSESSMENT,
        full_B27_unvisited_intro_not_mislabelled_as_whole_scene_actual_coverage=True,
        Hodram28_body_prose_native_display_andregistered_gates_remain_separate=True,
        evidence={**updated['evidence'],**{str(p):sha(p.read_bytes()) for p in [OLD,PLAN,OWNERSHIP,NATIVE,STORED,RELOC,CONTROL,REFERENCE,CALLERS,MODELS,ACTUAL,COMPARE,FOCUS,Path(__file__)]}})
    assert all(all(r['review'].values()) for r in updated['records']) and all(name['review'].values())
    ROOT.mkdir(parents=True);save(OUT,updated)
    save(ROOT/'scoped_actual_format_approval.json',dict(manuscript=str(OUT),manuscript_sha256=sha(OUT.read_bytes()),prior_manuscript=str(OLD),prior_manuscript_sha256=sha(OLD.read_bytes()),
        individual_five_gate_body_records=5,individual_five_gate_owned_name_records=1,all_prior_prose_andper_record_retention_reasons_preserved=True,
        directly_viewed_sheets=viewed,complete_actual_body_holds=30,relevant_actual_name_holds=262,all5_changed_single_pages_complete=True,
        actual_approval_scope=ASSESSMENT,fullcatalogue_UI_customnames_Hodram28_andall207_names_not_approved_bythis_receipt=True,
        pending_frozen_policy_independent_atomic_andregistered_cumulative_cleanpatch=True,
        registered_current_V8172_andmainV4701_unchanged=True,new_credit=0,new_emulator_runs=8,total_Gerhard_scene_frames=176008,
        full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,PLAN,OWNERSHIP,NATIVE,STORED,RELOC,CONTROL,REFERENCE,CALLERS,MODELS,ACTUAL,COMPARE,FOCUS,Path(__file__)]}))
    print('Scoped formattingapproved:5prior-completed speeches/oneowned12-byte name,30actualbodyholds/262nameholds/11viewedsheets.Allprose retained exceptsurname;policy/atomic/registered pending;zero duplicate credit.')
