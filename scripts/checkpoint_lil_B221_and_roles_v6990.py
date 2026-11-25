"""Publish zero-credit source/native/name progress with a deep inverse of all prior history."""
import argparse,gzip,json,os
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.complete_B210_Ferid_v6547 import parent_at
from scripts.lil_B221_checkpoint_text_v6990 import DETAILS,NEXT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_role_checkpoint_v6990')
VERIFY=Path('work/analysis/editorial_handoff_verification_v6991')
LEDGER=Path('translations/editorial_review_current_v1.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6962/verified_handoff.json')
KEY='lil_B221_and_ten_role_source_native_checkpoint_v6990'
SCOPE='unfinished_editorial_scope_v6990'
COUNTERS=['records_editorially_completed','records_with_source_and_prose_pass','records_with_source_prose_drafts','records_revised_and_integrated','retained_wordings_editorially_completed']
COUNTS=(6603,6606,6606,4126,2477)
DOC=Path('translations/lil_B221_editorial_manuscript_v1.json')
CHOICES=Path('translations/lil_B221_choice_manuscript_v1.json')
NAME=Path('translations/lil_B221_speaker_name_review_v1.json')
PLAN=Path('work/analysis/lil_B221_layout_v6976c/fourteen_whole_paragraph_plans_no_macros_no_prose_changes.json')
FONT=Path('work/analysis/lil_B221_native_pages_v6980c/all14_paragraphs16_complete_native_pages112_alignments.json')
NAMES=Path('work/analysis/lil_B221_name_planes_v6981/three_actors_six_getters_nine_name_component_planes36_alignments.json')
MENU=Path('work/analysis/lil_B221_choices_v6977/three_original_choice_decoders_nine_modal_cases_twelve_complete_label_planes.json')
QA=Path('work/analysis/lil_B221_base_QA_v6982b/all14_base_QA_diagnostics_before_any_scoped_classification.json')
CONTROL=Path('work/analysis/lil_B221_controls_v6971/two_A000_structural_cases50_normal_seeded_ends_choice_and_relatives_separate.json')
ENTRY=Path('work/analysis/lil_B221_entry_v6969/source_EV2_B221_action_dependency_and_native_getter_binding.json')
BRANCH=Path('work/analysis/lil_B221_branches_v6970/original_relative_skip_operand_proof.json')
ACTUAL=Path('work/analysis/lil_B221_source_actual_v6988/two_source_choices_all14_speeches_all30_commands_complete_bodies_names_and_returns.json')
VIEW=Path('work/analysis/lil_B221_native_source_view_v6989/all_native_pages_names_menu_both_source_choices_and_exact_wrap_reasons_viewed.json')
FIXTURE=Path('work/analysis/lil_B221_source_fixture_v6978/complete_B221_source_B22_fixture.json')
PIN=Path('work/analysis/lil_B221_source_fixture_v6978/pin_receipt.json')
ROLES=Path('translations/square_shopkeeper_label_manuscript_v2.json')
ROLE_CONTEXT=Path('work/analysis/square_shopkeeper_contexts_v6974/all42_complete_clean_contexts_ten_individual_role_decisions.json')
ROLE_BASELINE=Path('work/analysis/square_shopkeeper_baseline_v6973/all414_current_getters207_voices_and_all36_owner_pointer_values.json')
ROLE_SCOPE=Path('work/analysis/square_shopkeeper_scope_v6972/ten_source_identical_roles_current_owners_alias_fields_and_whole_clean_story_contexts.json')
INPUT=Path('work/analysis/current_V6956_native_v6966/current_native_input.json')
SOURCE=Path('work/analysis/lil_B221_source_v6967/sixteen_clean_current_Crusades_Saladin_context_four_relative_sites_one_choice.json')
CONSUMER=Path('work/analysis/lil_B221_consumers_v6968/fourteen_effective_bodies28_dispatches_three_actors_six_name_consumers.json')
PATHS=[DOC,CHOICES,NAME,PLAN,FONT,NAMES,MENU,QA,CONTROL,ENTRY,BRANCH,ACTUAL,VIEW,FIXTURE,PIN,
       ROLES,ROLE_CONTEXT,ROLE_BASELINE,ROLE_SCOPE,INPUT,SOURCE,CONSUMER,PRIOR,
       Path('scripts/lil_B221_checkpoint_text_v6990.py'),Path(__file__)]

def validate():
    prior=read(PRIOR)
    d,ch,f,n,m,q,c,e,b,a,v,r,rc,rb=map(read,[DOC,CHOICES,FONT,NAMES,MENU,QA,CONTROL,ENTRY,BRANCH,ACTUAL,VIEW,ROLES,ROLE_CONTEXT,ROLE_BASELINE])
    assert d['current_ROM_sha256']==read(INPUT)['current_ROM_sha256']==prior['candidate_sha256']
    assert len(d['records'])==14 and len(ch['records'])==2
    assert Counter(x['editorial_decision'] for x in d['records'])=={'revise':8,'retain-wording':6}
    assert [x['english'] for x in ch['records']]==['Yes','No']
    assert all(x['editorial_decision']=='retain-wording' for x in ch['records'])
    assert all(all(x['review'][k] for k in ['source','context','localization','naturalness']) and not x['review']['formatting'] for x in d['records']+ch['records'])
    assert d['source_prose_or_completion_credit_added']==ch['source_prose_or_completion_credit_added']==0
    assert f['manuscript_sha256']==q['manuscript_sha256']==sha(DOC.read_bytes())
    assert f['layout_plan_sha256']==q['layout_plan_sha256']==sha(PLAN.read_bytes())
    assert f['complete_native_pages']==16 and f['logical_compiled_input_alignment_cases']==112
    assert f['fresh_compiled_alignment_cases']==4 and f['exact_alignment_cases_reused']==108
    assert n['complete_name_component_plane_count']==9 and n['name_literal_alignment_count']==36
    assert m['native_selection_cancel_cases']==9 and m['complete_current_and_reviewed_style_label_planes']==12
    assert not [i for x in q['records'] for i in x['base_QA']['issues'] if i['severity'] in ['error','warning']]
    assert sum(i['code']=='line-break-count' for x in q['records'] for i in x['base_QA']['issues'])==7
    assert len(c['source_A000_structural_cases'])==2 and len(c['normal_terminal_seed_cases'])==50
    assert c['normal_state0_retains_seeded_value_word_in_all50_cases'] and c['original_end1204_full4bytes_and_no_tail_preserved']
    assert c['no_predicate_C200_style_letter_picture_or6329_commands'] and len(b['cases'])==40
    assert len(b['operands_requiring_adjustment_when_resizing'])==4
    assert [(x['event_ID'],x['script_block'],x['action_index'],x['must_be_completed'],x['must_not_be_completed']) for x in e['selected_B221_source_events']]==[(221,221,222,[],[])]
    assert a['actual_source_unique_speeches']==14 and a['actual_speech_observations']==26
    assert a['actual_complete_source_body_holds']==a['actual_complete_name_holds']==102
    assert a['incomplete_sampled_body_holds']==0 and a['all30_stored_commands_executed_in_union'] and a['all_jobs_terminal_and_reaped']
    assert [x['native_terminal_result'] for x in a['versions']]==[[0,0],[0,1]]
    assert [(x['exit_frame'],x['normal_port_sample_frame']) for x in a['versions']]==[(6215,6310),(6215,6310)]
    for run in ['work/analysis/lil_B221_source_run_v6979','work/analysis/lil_B221_source_run_v6979c']:
        assert read(Path(run)/'terminal.json')['terminal']
    assert v['actual_source_proof_sha256']==sha(ACTUAL.read_bytes()) and not v['visual_review_pending']
    assert len(v['all26_source_overview_panes_complete_and_pixel_equal'])==26 and v['all8_source_sheets_individually_returned_and_viewed']
    for im in v['viewed_images']:assert sha(Path(im['path']).read_bytes())==im['sha256']
    assert len(r['records'])==10 and all(x['english']=='Shopkeeper' and not x['review']['formatting'] for x in r['records'])
    assert [x['actor_ID'] for x in r['records']]==list(range(82,92))
    assert len(rc['contexts'])==42 and rc['exact_source_unique_blocks']==34
    assert len(rb['original_name_consumers']['rows'])==414 and len(rb['catalogue_and_original_voices']['rows'])==207
    assert len(rb['exact_pointer_hits'])==10 and rb['no_interior_pointers_found']
    assert read(PIN)['all_prior_pins_preserved']
    for key in ['candidate','patch']:assert sha(Path(prior[key]).read_bytes())==prior[key+'_sha256']
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(registry['accepted_layers'])==114 and prior['profile']=='all-routes-unified-v6956'
    return prior

def restore(value):
    doc=deepcopy(value);entry=doc.pop(KEY)
    for op in reversed(entry['inverse_operations']):
        parent,key=parent_at(doc,op['path'])
        if op['existed']:parent[key]=deepcopy(op['before'])
        else:parent.pop(key)
    return doc

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);mode=parser.parse_args().phase
    if mode=='stage':
        assert not ROOT.exists() and not VERIFY.exists()
        before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'] and tuple(old[k] for k in COUNTERS)==COUNTS
        assert KEY not in old and SCOPE not in old
        release=validate();ROOT.mkdir(parents=True);new=deepcopy(old);ops=[]
        def put(path,value):
            parent,key=parent_at(new,path);existed=key in parent if isinstance(parent,dict) else key<len(parent)
            ops.append(dict(path=path,existed=existed,before=deepcopy(parent[key]) if existed else None))
            parent[key]=deepcopy(value)
        evidence={str(p):sha(p.read_bytes()) for p in PATHS}
        summary=DETAILS+'\n\nCandidate SHA256 '+release['candidate_sha256']+'. Patch SHA256 '+release['patch_sha256']+'.\n\n'+NEXT
        pending=dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),choice_manuscript=str(CHOICES),choice_manuscript_sha256=sha(CHOICES.read_bytes()),
            name_review=str(NAME),name_review_sha256=sha(NAME.read_bytes()),paragraph_plan=str(PLAN),paragraph_plan_sha256=sha(PLAN.read_bytes()),
            native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),native_name_proof=str(NAMES),native_name_proof_sha256=sha(NAMES.read_bytes()),
            native_choice_proof=str(MENU),native_choice_proof_sha256=sha(MENU.read_bytes()),source_actual_proof=str(ACTUAL),source_actual_proof_sha256=sha(ACTUAL.read_bytes()),
            source_native_view=str(VIEW),source_native_view_sha256=sha(VIEW.read_bytes()),sixteen_four_prose_gates_true_formatting_false=True,
            proposed_revisions=8,justified_retentions=8,fourteen_paragraphs16_native_pages112_alignments=True,
            nine_name_planes36_alignments_three_choice_decoders9_counterfactual_modal_cases12_label_planes=True,
            source14_unique26_observations102_body102_name30_command_union=True,
            Yes0_R27_No1_R33_normal0_0_and0_1_end6215_port6310=True,
            frozen_policy_final_stored_relocation_English_two_page_actual_and_registered_release_pending=True,
            new_completed_records=0,new_source_prose_credit=0,full_goal_complete=False)
        roles=dict(manuscript=str(ROLES),manuscript_sha256=sha(ROLES.read_bytes()),context_review=str(ROLE_CONTEXT),context_review_sha256=sha(ROLE_CONTEXT.read_bytes()),
            baseline_proof=str(ROLE_BASELINE),baseline_proof_sha256=sha(ROLE_BASELINE.read_bytes()),scope_inventory=str(ROLE_SCOPE),scope_inventory_sha256=sha(ROLE_SCOPE.read_bytes()),
            ten_source_identical_roles_proposed_Shopkeeper_not_integrated=True,whole_clean_contexts=42,unique_source_blocks=34,role_utterances=216,
            all414_current_getters207_voices621_fields36_pointer_values_and_two_literal_owners_bound=True,
            shared_dynamic_paired_target_native_representative_and_registered_name_layer_pending=True,
            all207_name_queue_and_actor151_distinction_remain_open=True,new_name_or_dialogue_credit=0,full_goal_complete=False)
        put(['lil_B221_native_source_pending_v6990'],pending)
        put(['ten_Square_Shopkeeper_roles_contextual_localization_pending_v6990'],roles)
        put(['latest_checkpoint'],summary)
        put(['formatting_watchlist','lil_B221_v6990'],dict(status='source-and-native-reviewed-English-policy-reference-actual-release-pending',
            manuscript=str(DOC),two_source_bound_two_page_paragraphs_R46_R60=True,all_sixteen_formatting_gates_false=True,
            exact_R67_had_gone_reason_all25_boundaries_seven_info_diagnostics_preserved=True,new_credit=0))
        previous=old['unfinished_editorial_scope_v6961'];assert sha(Path(previous['path']).read_bytes())==previous['sha256']
        inventory=deepcopy(read(previous['path']));inventory['next_focus']=NEXT
        inventory['Lil_B221_native_pending_v6990']=pending;inventory['ten_Shopkeeper_roles_pending_v6990']=roles
        inventory['historical_B221_clean_only_flags_superseded_by_source_native_v6990']=True
        for unit in inventory['broader_coverage_units']:
            if unit['id']=='all-route-scenes':
                assert unit['reviewed_route_records']==unit['completed_route_records']==5003;unit['next']=NEXT
        assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory
        assert 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory
        assert 'Square_Shopkeeper_actor82_localization_lead_v6789' in old
        inv=ROOT/'unfinished_editorial_scope_inventory.json';save(inv,inventory);evidence[str(inv)]=sha(inv.read_bytes())
        put([SCOPE],dict(path=str(inv),sha256=sha(inv.read_bytes()),sixteen_B221_objects_native_source_uncredited=True,
            ten_Shopkeeper_role_proposals_wider_source_baseline_done_target_shared_and_registered_layer_pending=True,
            initial_Man_Woman_Stranger_Shady_Man_completed_history_preserved=True,
            incomplete_COMMON=3,incomplete_credited_route_drafts=0,
            retrospective207_names_and_all_prior_unresolved_leads_open=True,
            broader_storylines_shared_town_shop_random_help_prose_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False))
        ri=next(i for i,u in enumerate(new['coverage_units']) if u['id']=='all-route-scenes');put(['coverage_units',ri,'next'],NEXT)
        new[KEY]=dict(summary=summary,next=NEXT,evidence=evidence,inverse_operations=ops,
            new_completed_records=0,new_source_prose_credit=0,new_name_credit=0,
            successful_source_cold_boots=2,successful_source_frames=32002,
            preserved_failed_partial_input_run='work/analysis/lil_B221_source_run_v6979b',
            failed_partial_run_excluded_from_complete_coverage=True,new_ROMs=1,
            goal_turn_classification='progress',all_jobs_terminal_and_reaped=True,full_goal_complete=False)
        assert restore(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate']
        assert new['completed_editorial_families']==old['completed_editorial_families']
        assert new['goal_status']=='active' and not new['full_goal_complete']
        (ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        targets={LEDGER:encode_ledger(new)}
        section='## V6990: B221 source/native review; ten Shopkeeper role proposals\n\n'+summary+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name
            prefix=('# Current editorial handoff - V6990\n\n' if name=='editorial_handoff_current.md' else '')+section
            targets[path]=prefix.replace('\n','\r\n').encode('utf-8')+path.read_bytes()
        files=[]
        for index,(path,data) in enumerate(targets.items()):
            planned=ROOT/f'{index:02d}.after';planned.write_bytes(data)
            if path!=LEDGER:(ROOT/f'{index:02d}.before.gz').write_bytes(gzip.compress(path.read_bytes(),mtime=0))
            files.append(dict(target=str(path.resolve()),before_sha256=sha(path.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,new_credit=0,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six targets staged; current V6956/counters untouched. Deep inverse audit required.')
    else:
        plan=read(ROOT/'staged_checkpoint.json');old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()))
        new=read(plan['files'][0]['planned'])
        assert restore(new)==old and tuple(new[k] for k in COUNTERS)==COUNTS
        assert new['current_integrated_candidate']==old['current_integrated_candidate'] and new['completed_editorial_families']==old['completed_editorial_families']
        release=validate()
        for item in plan['files']:
            assert sha(Path(item['planned']).read_bytes())==item['planned_sha256']
            assert sha(Path(item['target']).read_bytes())==item['planned_sha256' if mode=='verify' else 'before_sha256']
        for path,digest in plan['evidence'].items():assert sha(Path(path).read_bytes())==digest
        if mode=='audit':
            assert not (ROOT/'preapplication_audit.json').exists()
            save(ROOT/'preapplication_audit.json',dict(staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),
                deep_inverse_recovers_every_prior_root_and_nested_value=True,all_six_before_and_planned_hashes_verified=True,
                all_counters_completed_families_and_current_release_unchanged=True,full_goal_complete=False))
            print('All six targets audited; deep inverse recovers every prior value, no completion credit.')
        elif mode=='apply':
            assert not (ROOT/'application_receipt.json').exists()
            assert read(ROOT/'preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes())
            workspace=Path.cwd().resolve()
            for item in plan['files']:
                assert Path(item['target']).is_relative_to(workspace) and Path(item['planned']).is_relative_to(ROOT.resolve())
            for item in plan['files']:
                with Path(item['target']).open('r+b') as stream:
                    stream.write(Path(item['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
                assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
            save(ROOT/'application_receipt.json',dict(all_six_targets_hash_exact=True,all_original_hashes_checked_before_first_write=True,full_goal_complete=False))
            print('Six audited source/native/role-progress targets applied exactly.')
        else:
            assert read(ROOT/'application_receipt.json')['all_six_targets_hash_exact'] and not VERIFY.exists()
            VERIFY.mkdir(parents=True);out=deepcopy(read(PRIOR))
            out.update(ledger_sha256=sha(LEDGER.read_bytes()),prior_verified_handoff=str(PRIOR),prior_verified_handoff_sha256=sha(PRIOR.read_bytes()),
                zero_credit_B221_and_roles_source_native_checkpoint_v6990=True,
                verified_cumulative_release_reused_unchanged_from_v6962=True,
                B221_sixteen_uncredited_objects_eight_revisions_eight_retentions=True,
                B221_fourteen_paragraphs16_native_pages112_alignments9_name_planes36_alignments=True,
                B221_source14_unique26_observations102_body102_name30_commands_union=True,
                B221_Yes0_R27_No1_R33_normal0_0_and0_1_6215_ports6310=True,
                B221_English_policy_final_stored_reference_pagination_actual_and_release_pending=True,
                ten_Shopkeeper_roles42_clean_contexts216_utterances414_getters207_voices621_fields36_pointer_values=True,
                Shopkeeper_shared_dynamic_paired_target_native_actual_and_registered_name_layer_pending=True,
                all207_names_and_all_prior_scope_leads_preserved=True,
                successful_source_cold_boots=2,successful_source_frames=32002,
                failed_partial_Down_input_run_preserved_excluded=True,
                source_current_ROM_counters_and_completed_families_unchanged=True,
                all_prior_root_nested_history_inverse_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes()))
            save(VERIFY/'verified_handoff.json',out)
            print('V6990 verified: V6956 and6603 completed unchanged; B221 and ten role proposals pending. Full objective active.')
