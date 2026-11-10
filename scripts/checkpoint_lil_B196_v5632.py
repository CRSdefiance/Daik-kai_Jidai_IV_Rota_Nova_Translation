"""Save36 uncredited B196 source objects with a complete historical inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B196_checkpoint_text_v5632 import NEXT,SUMMARY
from scripts.checkpoint_lil_B196_v5613 import gates as original_native_gates
ROOT=Path('work/analysis/lil_B196_checkpoint_v5632')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5633')
LEDGER=Path('translations/editorial_review_current_v1.json')
SOURCE=Path('work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json')
GLOSS=Path('work/analysis/lil_B196_clean_context_v5589/all24_clean_exchange_six_choices_and_fresh_glosses.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5614/verified_handoff.json')
KEY='Lil_B196_reference_review_v5632'
PREVIOUS='previous_latest_checkpoint_before_Lil_B196_v5632'
SCOPE='unfinished_editorial_scope_v5632'
COUNTERS=dict(records_editorially_completed=6155,records_with_source_and_prose_pass=6158,
    records_with_source_prose_drafts=6158,records_revised_and_integrated=3874,retained_wordings_editorially_completed=2281)
PROOFS={
 'voices':'work/analysis/lil_B196_voices_v5591/current207_catalog_eight_voices_and_six_source_selectors.json',
 'dispatch':'work/analysis/lil_B196_dispatches_v5592/all24_source_current_dispatches_FI1_and37_control_leaves.json',
 'entry':'work/analysis/lil_B196_entry_v5593/source_EV2_B196_action_dependency_and_native_getter_binding.json',
 'names':'work/analysis/lil_B196_names_v5594/twelve_original_progressive_and_catalogue_name_consumers.json',
 'branches':'work/analysis/lil_B196_branches_v5595/original_relative_skip_operand_proof.json',
 'controls':'work/analysis/lil_B196_controls_v5596/seven_unforced_predicates_six_picture_pairs_twenty_resource_cases_fourteen_opaque_effect_pairs.json',
 'special':'work/analysis/lil_B196_6003_ends_v5597/source6003_ten_boundary_cases_and_seventy_guarded_end_cases.json',
 'source_names':'work/analysis/lil_B196_source_names_v5598/six_source_name_fields_twelve_current_consumers_and_literal_scope.json'}

def inverse(value):
    result=deepcopy(value);result['latest_checkpoint']=result.pop(PREVIOUS);result.pop(KEY);result.pop(SCOPE);return result

def gates():
    packet,evidence=original_native_gates()
    from scripts.seal_lil_B196_references_v5631 import OUTPUT,CHOICE_OUTPUT,MAP,VISUAL,ACTUAL,STORED,STORED_MENUS,CENSUS,CONTROL,ENDS,PLAN,ROM
    receipt_path=Path('work/analysis/lil_B196_reference_approval_v5631/approval_receipt.json')
    receipt=read(receipt_path);doc,choice=map(read,[OUTPUT,CHOICE_OUTPUT])
    assert receipt['manuscripts']=={str(p):sha(p.read_bytes()) for p in [OUTPUT,CHOICE_OUTPUT]}
    assert receipt['all36_source_native_reference_and_representative_rules_approved'] and receipt['source_prose_English_unchanged']
    assert receipt['reference_map_sha256']==sha(MAP.read_bytes()) and receipt['new_editorial_credit']==0
    assert len(doc['records'])==24 and len(choice['records'])==12
    rows=doc['records']+choice['records']
    assert sum(r['editorial_decision']=='revise' for r in rows)==15 and sum(r['editorial_decision']=='retain-wording' for r in rows)==21
    assert all(all(r['review'].values()) for r in rows)
    assert all(r['fresh_retained_wording_justification'] for r in rows if r['editorial_decision']=='retain-wording')
    visual,actual,mapping=map(read,[VISUAL,ACTUAL,MAP])
    assert visual['representative_actual_coverage_sufficient_for_this_distinct_display_scope'] and not visual['visual_review_pending']
    assert visual['no_open_translation_specific_display_menu_control_or_return_finding'] and not actual['failures']
    assert len(actual['actual_panels'])==13 and len(actual['all_actual_speech_observations'])==24 and len(actual['actual_menu_cases'])==13
    assert len(actual['offline_only_display_IDs'])==11 and receipt['actual_buy_menu_offsets']==[218,1588]
    assert receipt['actual_pass_menu_offsets']==[218,582,832,1156,1370,1588]
    assert visual['actual_new_cold_boot_runs']==6 and visual['total_frames']==78006
    assert not actual['command_timing_differences'] and not actual['later_whole_RGB_differences']
    assert len(visual['reaped_tool_sessions'])==6
    assert len(mapping['blocks'][0]['mapped_native_commands'])==119 and len(mapping['blocks'][0]['relative_skip_fixups'])==52
    assert mapping['blocks'][0]['inverse_plus_original_two_tailzeros_recovers_every_stored_source_byte']
    for data in [receipt,visual,mapping,read(STORED),read(STORED_MENUS),read(CENSUS),read(CONTROL),read(ENDS)]:
        for p,h in data.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;evidence[p]=h
    for s in visual['all_actual_consumer_menu_sheets_viewed']+visual['paired_full_screen_views']+[visual['first_buy_postscene_view']]:
        assert s['viewed'] and s['viewed_after_image_return'] and sha(Path(s['path']).read_bytes())==s['sha256'];evidence[s['path']]=s['sha256']
    extra=[OUTPUT,CHOICE_OUTPUT,MAP,VISUAL,ACTUAL,STORED,STORED_MENUS,CENSUS,CONTROL,ENDS,PLAN,receipt_path,PRIOR,Path(__file__),Path('scripts/lil_B196_checkpoint_text_v5632.py')]
    evidence.update({str(p):sha(p.read_bytes()) for p in extra})
    assert sha(ROM.read_bytes())==mapping['blocks'][0].get('unowned_appended_copy',{}).get('ROM_sha256',sha(ROM.read_bytes()))
    prior=read(PRIOR);assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']
    packet['records']=doc['records'];packet['typed_choice_records']=choice['records']
    return packet,evidence

def audit(plan,applied=False):
    for item in plan['files']:
        assert sha(Path(item['target']).read_bytes())==item['planned_sha256' if applied else 'before_sha256']
        assert sha(Path(item['planned']).read_bytes())==item['planned_sha256']
    for p,h in plan['evidence'].items():assert sha(Path(p).read_bytes())==h
    old=json.loads(gzip.decompress((ROOT/'ledger.before.json.gz').read_bytes()));new=read(plan['files'][0]['planned'])
    assert inverse(new)==old and new['current_integrated_candidate']==old['current_integrated_candidate']
    assert all(new[k]==old[k]==v for k,v in COUNTERS.items())
    assert new['goal_status']=='active' and not new['full_goal_complete'];gates();return new

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('phase',choices=['stage','audit','apply','verify']);phase=parser.parse_args().phase
    if phase=='stage':
        assert not ROOT.exists();before=LEDGER.read_bytes();old=json.loads(before)
        assert sha(before)==read(PRIOR)['ledger_sha256'] and all(k not in old for k in [KEY,PREVIOUS,SCOPE])
        packet,evidence=gates();rows=packet['records']+packet['typed_choice_records']
        known={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']};fresh={historical_key(r) for r in rows}
        assert len(known)==6155 and len(fresh)==36 and not known&fresh
        fields=['id','file_path','block','kind','source_record_index','source_reference','source_hex','source_Japanese','source_complete_preamble_hex',
            'current_record_index','current_reference','current_hex','fresh_source_gloss','whole_exchange_note','command_offset','option_index','source_selector','english','compiled_hex','editorial_decision','localization_note','fresh_retained_wording_justification','review','reviewed_ordinary_boundaries','native_layout_retention_reason','actual_B22_display_fixture_observed','offline_only_native_display_checked','actual_label_visible','actual_choice_all_outcomes_observed']
        records=[{k:r[k] for k in fields if k in r} for r in rows]
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        scopepath=Path(old['unfinished_editorial_scope_v5613']['path']);assert sha(scopepath.read_bytes())==old['unfinished_editorial_scope_v5613']['sha256']
        scope=deepcopy(read(scopepath));scope['next_focus']=NEXT
        scope['historical_Lil_B196_native_approved_before_v5632']=scope.pop('next_Lil_B196_native_approved_uncredited_v5613')
        scope['next_Lil_B196_reference_approved_uncredited_v5632']=dict(
            speech_manuscript='translations/lil_B196_editorial_manuscript_v4.json',
            speech_manuscript_sha256=sha(Path('translations/lil_B196_editorial_manuscript_v4.json').read_bytes()),
            choice_manuscript='translations/lil_B196_choice_manuscript_v3.json',
            choice_manuscript_sha256=sha(Path('translations/lil_B196_choice_manuscript_v3.json').read_bytes()),
            reference_map='translations/lil_B196_editorial_relocation_map_v1.json',
            reference_map_sha256=sha(Path('translations/lil_B196_editorial_relocation_map_v1.json').read_bytes()),
            objects=36,speeches=24,choice_labels=12,typed_choice_objects=6,revisions=15,retentions=21,
            uncredited=True,source_prose_native_relocation_stored_reference_representative_approved=True,
            actual_speech_panels=13,offline_only_speeches=11,actual_menu_cases=13,actual_cold_boots=6,actual_frames=78006,
            actual_Buy_menu_offsets=[218,1588],actual_Pass_menu_offsets=[218,582,832,1156,1370,1588],
            atomic_compiler_registered_cumulative_clean_patch_and_startup_pending=True,
            exact_R74_three_ordinary_wraps_with_all_words_native_guards_retained=True)
        inventory=ROOT/'unfinished_editorial_scope_inventory.json';save(inventory,scope);evidence[str(inventory)]=sha(inventory.read_bytes())
        new=deepcopy(old)
        new[KEY]=dict(summary=SUMMARY,next=NEXT,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=records,
            reference_approved_uncredited_objects=36,speech_objects=24,typed_choice_labels=12,typed_choice_objects=6,
            proposed_revisions=15,individually_justified_retentions=21,source_prose_or_completion_credit_added=0,
            all36_source_context_localization_naturalness_native_reference_and_representative_approved=True,
            source_stored_logical=[1816,1814],target_stored_logical=[1668,1668],source_tailzeros=2,target_tailzeros=0,
            commands=119,relative_sites=52,target_skip_cases=260,exact_opaque_leaves=37,ends=7,
            final_stored_speech_alignments=96,fresh_stored_alignments=40,exact_reused_alignments=56,
            final_stored_menu_count_calls=12,final_stored_menu_pointer_calls=24,
            actual_speech_panels=13,actual_speech_observations=24,offline_only_speeches=11,actual_menu_cases=13,
            actual_Buy_menu_offsets=[218,1588],actual_Pass_menu_offsets=[218,582,832,1156,1370,1588],
            actual_end_offsets=[364,1708,1810],actual_exit_frames=[4299,5258,5255],
            new_ROMs=3,new_emulator_runs=6,total_frames=78006,all_six_sessions_terminal_and_reaped=True,
            zero_measured_command_timing_or_sampled_postscene_RGB_differences=True,
            paired_five_native_groups_actor_captain_and_PRNG_equal_within_scope=True,
            earlier_failed_audit_and_state_serialization_producers_preserved=True,
            remaining_gates=['atomic-speech-and-six-menu-compiler-and-meaningful-negatives',
                'registered-cumulative-build-with-both-companions','clean-input-patch-release-checks-and-current-startup','credit36-once-after-integration'],
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B196_reference_approved_uncredited_objects=36,
            broader_storylines_earlier_translations_town_shop_random_help_prose_and_retrospective_early_wrapping_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5613: B196 relocation and representative gameplay approved;36 uncredited objects\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5613\n\n'+section+NEXT+'\n\n'+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for index,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{index:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{index:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six reference/gameplay checkpoint targets staged;36 approvals remain uncredited.')
    elif phase=='audit':
        assert not (ROOT/'independent_preapplication_audit.json').exists();plan=read(ROOT/'staged_checkpoint.json');audit(plan)
        save(ROOT/'independent_preapplication_audit.json',dict(all_six_before_planned_and_evidence_hashes_exact=True,
            full_nested_inverse_recovers_every_historical_value=True,staged_plan_sha256=sha((ROOT/'staged_checkpoint.json').read_bytes()),full_goal_complete=False))
        print('Six targets and complete historical inverse pass.')
    elif phase=='apply':
        assert not (ROOT/'application_receipt.json').exists();plan=read(ROOT/'staged_checkpoint.json')
        assert read(ROOT/'independent_preapplication_audit.json')['staged_plan_sha256']==sha((ROOT/'staged_checkpoint.json').read_bytes());audit(plan)
        workspace=Path.cwd().resolve()
        for item in plan['files']:assert Path(item['target']).is_relative_to(workspace) and Path(item['planned']).is_relative_to(ROOT.resolve())
        for item in plan['files']:
            with Path(item['target']).open('r+b') as stream:
                stream.write(Path(item['planned']).read_bytes());stream.truncate();stream.flush();os.fsync(stream.fileno())
            assert sha(Path(item['target']).read_bytes())==item['planned_sha256']
        save(ROOT/'application_receipt.json',dict(all6_targets_exact=True,all_before_hashes_checked_before_first_write=True,full_goal_complete=False))
        print('Six audited reference/gameplay checkpoint files applied exactly.')
    else:
        assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all6_targets_exact']
        plan=read(ROOT/'staged_checkpoint.json');new=audit(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6155,source_prose=6158,revised=3874,retained=2281,SC2=4270,SC3=96,reviewed_routes=4556,completed_routes=4556,
            reference_approved_uncredited_Lil_B196_objects=36,B196_speeches=24,B196_choice_labels=12,B196_menus=6,
            proposed_revisions=15,individually_justified_retentions=21,all36_source_native_reference_representative_gates_true=True,
            actual_unique_speech_panels=13,offline_only_speeches=11,actual_speech_observations=24,actual_menu_cases=13,
            actual_Buy_menu_offsets=[218,1588],actual_Pass_menu_offsets=[218,582,832,1156,1370,1588],
            atomic_compiler_registered_release_clean_patch_and_current_startup_pending=True,
            new_editorial_credit=0,new_ROMs=3,new_emulator_runs=6,actual_frames=78006,main_V4701_preserved=True,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5632 verified;V5580 remains current.36 B196 reference/representative approvals uncredited;atomic integration next.Full editorial objective active.')
