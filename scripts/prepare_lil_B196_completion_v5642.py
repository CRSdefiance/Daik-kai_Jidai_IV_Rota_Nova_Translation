"""Prepare lossless once-only credit for both integrated B196 companions."""
from pathlib import Path
from collections import Counter
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B196_completion_tools_v5642')
GATES='''def gates():
    release,start,view,reg,actual,transitions=map(read,[RELEASE,START,VIEW,REG,ACTUAL,TRANSITIONS])
    assert release['all581_manifest_batches_and114_accepted_layers_present'] and release['whole_ROM_reconstruction_byte_exact']
    assert start['all_current_requested_and_final_framebuffers_equal_V5580'] and start['paired_frame_count']==31
    assert start['all_five_postload_actor_model_and_captain_checks_equal'] and start['source_and_disposable_town_donor_unchanged']
    assert view['viewed'] and view['six_selected_character_selection_Lil_opening_town_and_Refit_frames_viewed'] and view['sha256']==start['review_sheet_sha256']==sha(Path(view['sheet']).read_bytes())
    assert reg['negative_count']==90 and reg['all_negatives_reject_before_mutation']
    assert actual['fresh_actual_unique_speech_panels']==13 and len(actual['all_actual_speech_observations'])==24 and len(actual['actual_menu_cases'])==13
    assert actual['complete_native_holds']==67 and not actual['failures'] and not actual['paired_nontext_region_differences']
    assert len(actual['offline_only_display_IDs'])==11 and not actual['command_timing_differences'] and not actual['later_whole_RGB_differences']
    assert transitions['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and transitions['no_open_translation_specific_display_menu_control_or_return_finding']
    assert transitions['actual_new_cold_boot_runs']==6 and transitions['total_frames']==78006 and len(transitions['reaped_tool_sessions'])==6
    assert all(all(p['five_native_component_equality'].values()) and p['whole1A04_actor_and_captain2_equal'] and p['PRNG_equal'] for p in transitions['paired_final_state_measurements'])
    tests=read('work/analysis/lil_B196_regressions_v5637/terminal.json');assert tests['returncode']==0 and sha(Path(tests['log']).read_bytes())==tests['log_sha256'] and '110 passed' in Path(tests['log']).read_text(encoding='utf-8')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']==start['candidate_sha256'] and sha(Path(release['patch']).read_bytes())==release['patch_sha256']
    registry=read('translations/release_stack.json');manifest=read(release['manifest'])
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(manifest['batches'])==581 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert read('work/analysis/lil_B196_retention_v5641/pin_receipt.json')['all_prior_pins_preserved']
    return release

'''
RECORDS='''        refs={r['id']:r for r in mapping['blocks'][0]['text_records']};stage={r['id']:r for r in release['stage']['changed_records']}
        for command in mapping['blocks'][0]['choice_commands']:
            refs.update({r['id']:{**r,'target_hex':block[r['new_offset']:r['new_offset']+r['new_length']].hex(),'target_command_offset':command['new_offset']} for r in command['label_references']})
        for row in rows:
            ref=refs[row['id']];at=ref['new_offset'];value=bytes.fromhex(ref['target_hex']);speech='source_selector' in row
            assert block[at:at+len(value)+1]==value+b'\\0' and stage[row['id']]['new_offset']==at
            if speech:assert block[at-5:at+1].hex()==row['source_complete_preamble_hex']
            fields=['current_reference','current_hex','current_text_hex','current_English','current_record_index','record_index','source_prose_or_completion_credit_added','command_offset']
            row['historical_source_prose_predecessor_fields']={k:deepcopy(row[k]) for k in fields if k in row}
            body=value[1:] if speech else value;template=body.decode('ascii');runtime=template.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.')
            logical=' '.join(template.split())
            for macro in ['FI','FA','FO']:logical=logical.replace(macro,'{MACRO:'+macro+'}')
            newref=dict(block=196,offset=at,bytes=len(value),record_index=block[:at].count(b'\\0'))
            if speech:newref['header_offset']=at-5
            else:newref['command_offset']=ref['target_command_offset'];row['current_command_offset']=ref['target_command_offset']
            row.update(current_reference=newref,integrated_reference=newref,current_hex=value.hex(),current_text_hex=value.hex(),integrated_hex=value.hex(),
                record_index=newref['record_index'],current_record_index=newref['record_index'],current_English=template,current_stored_English=template,
                current_raw_storage_English=template,current_effective_runtime_English=runtime,current_effective_macro_template_hex=body.hex(),
                current_effective_macro_template_English=template,current_effective_paragraph=logical,registered_runtime_catalog_entry=None,
                completed_candidate_reference=release['candidate'],completed_candidate_sha256=release['candidate_sha256'],current_native_voice_macro_entry_controls_and_context_pending=False,
                current_complete_native_display_pending=False,registered_integration_pending=False,source_prose_or_completion_credit_added=1,
                decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-reviewed',status='complete-contextual-current-native-references-representative-and-registered-release')
            assert row['current_effective_paragraph']==(row['english'].split('}',1)[1] if speech else row['english']) and all(row['review'].values())
'''
INVENTORY='''        inventory=deepcopy(read(old['unfinished_editorial_scope_v5632']['path']));inventory['next_focus']=NEXT
        inventory['Lil_B196_completed_v5642']=dict(final_review=str(FINAL),completed_objects=36,registered_candidate=release['candidate'],natural_event196_not_selected=True,
            actual_speeches=13,offline_only_speeches=11,actual_menu_cases=13,actual_Buy_menu_offsets=[218,1588],actual_Pass_menu_offsets=[218,582,832,1156,1370,1588])
        inventory['historical_Lil_B196_reference_approved_before_v5642']=inventory.pop('next_Lil_B196_reference_approved_uncredited_v5632')
        inventory['next_Lil_B197_clean_review_pending']=dict(file_path='/data/SC2.DK4',block=197,clean_inventory_and_full_exchange_gloss_before_prior_English=True,
            reviewed_objects=0,new_completion_credit=0,no_B197_command_actor_or_control_assumptions_inherited=True)
'''
VERIFY='''            VERIFY.mkdir(parents=True);save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
                patch=release['patch'],patch_sha256=release['patch_sha256'],all_original_root_and_nested_history_preserved=True,exactly36_new_disjoint_source_prose_and_completed_records=True,
                completed=6191,source_prose=6194,revised=3889,retained=2302,SC2=4306,SC3=96,reviewed_routes=4592,completed_routes=4592,
                all581_manifest_batches114_accepted18_checks_verified=True,actual_unique_B196_speeches=13,offline_only_B196_speeches=11,actual_menu_cases=13,actual_matching_holds=67,
                startup31_frames_and_five_actor_controls_match_V5580=True,source196_natural_eligibility_and_earned_affordability_not_claimed=True,
                measured_paired_content_timings_sampled_postscene_RGB_five_native_groups_actor_and_PRNG_equal_within_scope=True,
                next_Lil_B197_clean_review_pending=True,main_V4701_preserved=True,all_sessions_terminal_and_reaped=True,
                full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
            print('V5637 integration verified;6191 completed/6194 source-prose. Next B197 clean-source review pending;full goal active.')
'''
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/complete_lil_B195_v5585.py');text=source.read_text(encoding='utf-8')
    a=text.index('def gates():');b=text.index('def restore(',a)
    c=text.index("        refs={r['id']");e=text.index('        oldkeys=',c)
    f=text.index("        inventory=deepcopy(read(old['unfinished_editorial_scope_v5576'");g=text.index("        for unit in inventory['broader_coverage_units']:",f)
    v=text.index("            VERIFY.mkdir(parents=True)")
    active_restore="""    active=inverse['active_source_prose_drafts'];assert active['manuscripts'].pop()==str(DOC)
    assert active['route_record_subsets_pending'].pop(str(DOC))==[];active['note']=back['active_note']
"""
    active_new="""    active=inverse['active_source_prose_drafts']
    for p in reversed([DOC,MENU]):
        assert active['manuscripts'].pop()==str(p) and active['route_record_subsets_pending'].pop(str(p))==[]
    active['note']=back['active_note']
"""
    active_stage="""        active=new['active_source_prose_drafts'];assert str(DOC) not in active['manuscripts'] and str(DOC) not in active['route_record_subsets_pending']
        active['manuscripts'].append(str(DOC));active['route_record_subsets_pending'][str(DOC)]=[];active['note']=note
"""
    active_stage_new="""        active=new['active_source_prose_drafts']
        for p in [DOC,MENU]:
            assert str(p) not in active['manuscripts'] and str(p) not in active['route_record_subsets_pending']
            active['manuscripts'].append(str(p));active['route_record_subsets_pending'][str(p)]=[]
        active['note']=note
"""
    row=derive(source,'scripts/complete_lil_B196_v5642.py',{
        text[a:b]:GATES,text[c:e]:RECORDS,text[f:g]:INVENTORY,text[v:]:VERIFY,
        active_restore:active_new,active_stage:active_stage_new,
        "DOC=Path('translations/lil_B195_editorial_manuscript_v4.json')":"DOC=Path('translations/lil_B196_editorial_manuscript_v4.json')\nMENU=Path('translations/lil_B196_choice_manuscript_v3.json')",
        "rows=deepcopy(doc['records'])":"rows=deepcopy(doc['records']+read(MENU)['records'])",
        "[DOC,RELEASE,START":"[DOC,MENU,RELEASE,START",
        'B195':'B196','completion_v5585':'completion_v5642','verification_v5586':'verification_v5643','verification_v5577':'verification_v5633',
        'release_v5581':'release_v5638','startup_v5583':'startup_v5640','registration_v5579':'registration_v5636',
        'actual_v5572/actual_all20_progressive_FE_A000_C200_and_single_end.json':'actual_v5628b/three_paired_paths_native_panels_menus_and_separate_endings.json',
        'actual_review_v5573/all20_panels20_fullscreens_three_roles_return_and_measured_differences.json':'actual_review_v5630/viewed13_panels13_menus_three_paths_and_measured_state_scope.json',
        'completion_text_v5585':'completion_text_v5642',
        'Lil-B195-three-roles-cheese-specialty-coaxing-shared-order-taste-intention-and-prospective-Veracruz20':'Lil-B196-six-price-bargaining-six-menus-conditional-advice-Charm-and-seven-endings36',
        'editorial_scope_v5585':'editorial_scope_v5642','B195_v5585':'B196_v5642','retention_v5584':'retention_v5641','regressions_v5580':'regressions_v5637',
        "{'revise':3,'retain-wording':17}":"{'revise':15,'retain-wording':21}",
        '6135':'6155','6155':'6191','6158':'6194','3874':'3889','2281':'2302','4250':'4270','4270':'4306','4556':'4592',
        '[-20:]':'[-36:]','all20':'all36','exactly20':'exactly36','==20':'==36','=20':'=36',
        'revised=3':'revised=15','revised_count=3':'revised_count=15','fresh_revisions=3':'fresh_revisions=15','new_revisions=3':'new_revisions=15',
        'retained=17':'retained=21','retained_count=17':'retained_count=21','fresh_retentions=17':'fresh_retentions=21','justified_retentions=17':'justified_retentions=21',
        'actual_unique_speeches=20,actual_matching_holds=79':'actual_unique_speeches=13,offline_only_speeches=11,actual_menu_cases=13,actual_matching_holds=67',
        'actual_B22_content_speeches=20':'actual_B22_content_speeches=13,offline_only_speeches=11,actual_menu_cases=13',
        'blocks[195]':'blocks[196]','blocks=[195]':'blocks=[196]','event195':'event196','source195':'source196',
        'Lil_B196_clean_review_pending=True':'Lil_B197_clean_review_pending=True',
        'explicit_content_fixture_runs=2':'explicit_content_fixture_runs=6','batch_new_emulator_runs=4':'batch_new_emulator_runs=8','batch_new_frames=39404':'batch_new_frames=99408',
        'no_record_specific_ordinary_boundary_exception_required=True':'only_exact_R74_three_ordinary_boundaries_approved=True',
        'Twenty Lil B195 reviews integrated once in cumulative V5580':'Thirty-six Lil B196 reviews integrated once in cumulative V5637',
        'V5585':'V5642','twenty':'thirty-six'})
    old,new=native_numbers(text),native_numbers(Path(row['successor']).read_text())
    assert old-new==Counter({3942509462:1,3085513495:1}) and not new-old
    ROOT.mkdir(parents=True);save(ROOT/'prepared_completion.json',dict(derivation=row,both_speech_and_choice_companions_counted_once=True,
        native_high_constants_preserved_except_removed_old_B195_PRNG_assertion_data=True,
        full_root_and_nested_inverse_required=True,source_prose_credit=36,completion_credit=36,full_goal_complete=False))
