"""Save36 uncredited B196 source objects with a complete historical inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B196_checkpoint_text_v5599 import NEXT,SUMMARY
ROOT=Path('work/analysis/lil_B196_checkpoint_v5599')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5600')
LEDGER=Path('translations/editorial_review_current_v1.json')
SOURCE=Path('work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json')
GLOSS=Path('work/analysis/lil_B196_clean_context_v5589/all24_clean_exchange_six_choices_and_fresh_glosses.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5586/verified_handoff.json')
KEY='Lil_B196_source_contracts_v5599'
PREVIOUS='previous_latest_checkpoint_before_Lil_B196_v5599'
SCOPE='unfinished_editorial_scope_v5599'
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
    packet,gloss=read(SOURCE),read(GLOSS);proof={k:read(p) for k,p in PROOFS.items()}
    assert len(packet['records'])==24 and len(packet['typed_choice_records'])==12 and packet['total_editorial_objects']==36
    assert packet['source_native_commands']==119 and packet['source_relative_sites']==52
    assert packet['source_macro_counts']==dict(FI=1,FA=0,FO=0)
    assert packet['source_static_actor_selectors']==[2,6,19,20,25,173]
    assert packet['all48_original_label_getters_and24_count_getters_clean_current_even_alignments_pass']
    assert packet['source_end_words']==7 and packet['source_A000']==14 and packet['source_C200']==0
    assert gloss['read_no_predecessor_English'] and gloss['new_review_credit']==0
    assert len(gloss['records'])==24 and len(gloss['choices'])==6 and gloss['choice_labels']==12
    assert (gloss['source_stored_bytes'],gloss['source_logical_end'],gloss['source_alignment_tailzeros'])==(1816,1814,2)
    for d in proof.values():assert d['source_context_sha256']==sha(SOURCE.read_bytes())
    assert len(proof['voices']['catalog']['rows'])==207 and len(proof['voices']['fresh6_actor_names']['rows'])==6
    assert len(proof['dispatch']['speech_dispatch_cases'])==48 and len(proof['dispatch']['source_current_opaque_nonrelative_control_leaves'])==37
    assert len(proof['names']['native_twelve_consumer_cases']['rows'])==12
    assert [(r['event_ID'],r['action_index'],r['must_be_completed'],r['must_not_be_completed']) for r in proof['entry']['selected_B196_source_events']]==[(196,197,[],[])]
    assert len(proof['branches']['cases'])==520 and len(proof['branches']['operands_requiring_adjustment_when_resizing'])==52
    control=proof['controls']
    assert len(control['source_predicate_cases'])==7 and all(c['native_result']==[2,0,0,0,0,0] for c in control['source_predicate_cases'])
    assert len(control['source_picture_pairs'])==6 and len(control['source630x_boundary_cases'])==20 and len(control['source_A000_structural_pairs'])==14
    assert control['source_A000_packed_effect_semantics_funds_debits_inventory_and_FI_stat_effect_unbound']
    assert len(proof['special']['source6003_cases'])==10 and len(proof['special']['source_end_cases'])==70
    assert proof['special']['all_end_payload_reads_within_four_bytes']
    assert proof['source_names']['five_named_actors_have_ten_owned_scratch_name_paths_person173_has_two_readonly_paths']
    assert proof['source_names']['source_person173_first_field_is_gender_neutral_ayashii_hito']
    paths=[SOURCE,GLOSS,PRIOR,Path(__file__),Path('scripts/lil_B196_checkpoint_text_v5599.py'),
        Path('scripts/map_lil_B196_source_v5590.py'),Path('scripts/map_lil_B196_source_v5590b.py'),
        Path('work/analysis/lil_B196_source_tools_v5590b/nested_container_ownership_correction.json'),*[Path(p) for p in PROOFS.values()]]
    evidence={str(p):sha(p.read_bytes()) for p in paths}
    for data in [packet,gloss,*proof.values()]:
        for p,h in data.get('evidence',{}).items():assert sha(Path(p).read_bytes())==h;evidence[p]=h
        for k,v in data.items():
            if k.endswith('_sha256') and isinstance(data.get(k[:-7]),str):
                p=Path(data[k[:-7]])
                if p.is_file():assert sha(p.read_bytes())==v;evidence[str(p)]=v
    prior=read(PRIOR);assert sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==packet['current_ROM_sha256']
    assert sha(Path(prior['patch']).read_bytes())==prior['patch_sha256']
    manifest=read(Path(prior['candidate']).with_suffix('.manifest.json'));registry=read('translations/release_stack.json')
    assert manifest['profile']=='all-routes-unified-v5580' and len(manifest['batches'])==579 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
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
            'current_record_index','current_reference','current_hex','fresh_source_gloss','whole_exchange_note','command_offset','option_index','source_selector']
        records=[{k:r[k] for k in fields if k in r} for r in rows]
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        scopepath=Path(old['unfinished_editorial_scope_v5585']['path']);assert sha(scopepath.read_bytes())==old['unfinished_editorial_scope_v5585']['sha256']
        scope=deepcopy(read(scopepath));scope['next_focus']=NEXT
        scope['historical_Lil_B196_unread_lead_before_v5599']=scope.pop('next_Lil_B196_clean_review_pending')
        scope['next_Lil_B196_source_bound_uncredited_v5599']=dict(path=str(SOURCE),sha256=sha(SOURCE.read_bytes()),
            mapped_objects=36,speeches=24,choice_labels=12,typed_choice_objects=6,uncredited=True,new_approved_objects=0,
            whole_exchange_English_comparison_localization_and_native_fonts_pending=True,
            source_control_boundaries_distinct_from_unexecuted_effects_and_actual_gameplay=True)
        inventory=ROOT/'unfinished_editorial_scope_inventory.json';save(inventory,scope);evidence[str(inventory)]=sha(inventory.read_bytes())
        new=deepcopy(old)
        new[KEY]=dict(summary=SUMMARY,next=NEXT,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=records,
            source_mapped_uncredited_objects=36,speech_objects=24,typed_choice_labels=12,typed_choice_objects=6,
            new_approved_editorial_objects=0,source_prose_or_completion_credit_added=0,
            clean_first_gloss_and_source_native_boundaries_complete=True,old_English_prose_comparison_and_approved_localization_pending=True,
            offline_native_checks=dict(speech_dispatches=48,label_getters=48,count_getters=24,relative_cases=520,
                predicates=7,picture_pairs=6,resource_boundary_cases=20,opaque_A000_pairs=14,current6003_boundary_cases=10,end_cases=70,name_consumers=12),
            remaining_gates=['approved-terms-and-FI-expansion','source-purchase-context-for-concrete-fidelity-risks',
                'whole-exchange-predecessor-comparison-and-v2-localization','individual-revision-retention-reasons',
                'native-text-and-choice-font-glyph-bounds-pagination-selection-cancellation','reversible-relocation-and-native-references',
                'representative-actual-transitions','atomic-compiler-and-registered-cumulative-release','clean-input-patch-and-current-startup'],
            actual_B196_gameplay_observed=False,new_ROMs=0,new_emulator_runs=0,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B196_source_mapped_uncredited_objects=36,
            broader_storylines_earlier_translations_town_shop_random_help_prose_and_retrospective_early_wrapping_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5599: B196 clean exchange and native source contracts;36 uncredited objects\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5599\n\n'+section+NEXT+'\n\n'+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for index,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{index:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{index:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six source-contract checkpoint targets staged;36 objects remain unapproved/uncredited.')
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
        print('Six audited source-contract checkpoint files applied exactly.')
    else:
        assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all6_targets_exact']
        plan=read(ROOT/'staged_checkpoint.json');new=audit(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6155,source_prose=6158,revised=3874,retained=2281,SC2=4270,SC3=96,reviewed_routes=4556,completed_routes=4556,
            mapped_uncredited_Lil_B196_objects=36,B196_speeches=24,B196_typed_choice_labels=12,B196_typed_choice_objects=6,new_editorial_approvals=0,
            clean_source_gloss_and_current_native_boundaries_verified=True,English_comparison_localization_fonts_actual_and_release_pending=True,
            new_editorial_credit=0,new_ROMs=0,new_emulator_runs=0,main_V4701_preserved=True,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5599 verified;V5580 remains current.36 B196 source objects uncredited;full editorial objective active.')
