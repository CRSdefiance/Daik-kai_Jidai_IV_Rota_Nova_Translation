"""Save36 uncredited B197 source objects with a complete historical inverse."""
import argparse,gzip,json,os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B197_checkpoint_text_v5656 import NEXT,SUMMARY
ROOT=Path('work/analysis/lil_B197_checkpoint_v5656')
VERIFY=Path('work/analysis/editorial_handoff_verification_v5657')
LEDGER=Path('translations/editorial_review_current_v1.json')
SOURCE=Path('work/analysis/lil_B197_source_v5647/all24_clean_current_complete_context_with_three_choice_labels.json')
GLOSS=Path('work/analysis/lil_B197_clean_context_v5646/all21_clean_exchange_three_labels_and_fresh_glosses.json')
PRIOR=Path('work/analysis/editorial_handoff_verification_v5643/verified_handoff.json')
KEY='Lil_B197_source_review_v5656'
PREVIOUS='previous_latest_checkpoint_before_Lil_B197_v5656'
SCOPE='unfinished_editorial_scope_v5656'
COUNTERS=dict(records_editorially_completed=6191,records_with_source_and_prose_pass=6194,
    records_with_source_prose_drafts=6194,records_revised_and_integrated=3889,retained_wordings_editorially_completed=2302)
def inverse(value):
    result=deepcopy(value);result['latest_checkpoint']=result.pop(PREVIOUS);result.pop(KEY);result.pop(SCOPE);return result

def gates():
    packet,gloss,prior=map(read,[SOURCE,GLOSS,PRIOR])
    assert packet['source_context'] if 'source_context' in packet else packet['format']=='dk4-editorial-source-context-packet-v1'
    assert packet['current_ROM_sha256']==prior['candidate_sha256']==sha(Path(prior['candidate']).read_bytes())
    assert len(packet['records'])==21 and len(packet['typed_choice_records'])==3 and packet['total_editorial_objects']==24
    assert gloss['read_no_predecessor_English'] and len(gloss['records'])==21 and gloss['choice_labels']==3
    assert gloss['choices'][0]['source_labels']==['買おう','買わない','任せる']
    assert packet['source_macro_counts']==dict(FI=0,FA=0,FO=0) and packet['source_native_commands']==39
    assert packet['source_relative_sites']==6 and packet['source_A000']==5 and packet['source_picture_commands']==packet['source_end_words']==1
    assert packet['all12_original_label_getters_and4_count_getters_clean_current_even_alignments_pass']
    names=read('work/analysis/lil_B197_source_names_v5653/two_source_name_fields_four_current_consumers_and_literal_scope.json')
    assert names['current_progressive_and_full_catalogue_values']=={'21':'Ian Dukov','169':'Alluring Woman'}
    assert names['current_native_voice_classes']=={'21':1,'169':0} and names['source169_primary_field_explicitly_says_woman_and_supports_female_pronoun']
    assert names['celestial_maiden_identity_remains_character_question_then_self_dismissal_not_narrator_confirmation']
    branch=read('work/analysis/lil_B197_branches_v5651/original_relative_skip_operand_proof.json')
    assert len(branch['operands_requiring_adjustment_when_resizing'])==6 and len(branch['cases'])==60
    controls=read('work/analysis/lil_B197_controls_v5654/eleven_exact_leaves_five_effect_two47xx_pairs_picture_resource_6003_and_end_cases.json')
    assert len(controls['all11_source_current_nonrelative_nonspeech_nonchoice_leaves'])==11 and len(controls['source_A000_and47xx_structural_pairs'])==7
    assert controls['source_picture_descriptor']==[0,140,1,5]
    assert len(controls['source632E_boundary_cases'])==len(controls['source6003_boundary_cases'])==len(controls['source_declared_end_cases'])==10
    choice=read('work/analysis/lil_B197_choice_source_v5655/all_three_indices_and_cancel_original_VM_geometry_without_live_input.json')
    assert choice['native_selection_cancel_cases']==8 and choice['modal_input_loop_bridged_not_actual_selected_gameplay']
    evidence={}
    proofs=[SOURCE,GLOSS,PRIOR,
        Path('work/analysis/lil_B197_voices_v5648/current207_catalog_eight_voices_and_two_source_selectors.json'),
        Path('work/analysis/lil_B197_dispatches_v5649/all21_source_current_dispatches_no_macros_and11_control_leaves.json'),
        Path('work/analysis/lil_B197_entry_v5650/source_EV2_B197_action_dependency_and_native_getter_binding.json'),
        Path('work/analysis/lil_B197_branches_v5651/original_relative_skip_operand_proof.json'),
        Path('work/analysis/lil_B197_names_v5652/four_original_progressive_and_catalogue_name_consumers.json'),
        Path('work/analysis/lil_B197_source_names_v5653/two_source_name_fields_four_current_consumers_and_literal_scope.json'),
        Path('work/analysis/lil_B197_controls_v5654/eleven_exact_leaves_five_effect_two47xx_pairs_picture_resource_6003_and_end_cases.json'),
        Path('work/analysis/lil_B197_choice_source_v5655/all_three_indices_and_cancel_original_VM_geometry_without_live_input.json'),
        Path('scripts/inventory_lil_B197_clean_v5645.py'),Path('scripts/inventory_lil_B197_clean_v5645b.py'),
        Path('scripts/read_lil_B197_clean_context_v5646.py'),Path('scripts/read_lil_B197_clean_context_v5646b.py'),Path('scripts/read_lil_B197_clean_context_v5646c.py'),
        Path('work/analysis/lil_B197_clean_inventory_v5645/three_option_classification_correction.json'),
        Path('work/analysis/lil_B197_clean_inventory_v5645b/exact_menu_decoding_before_gloss_output.json'),
        Path('scripts/lil_B197_checkpoint_text_v5656.py'),Path(__file__)]
    for p in proofs:
        evidence[str(p)]=sha(p.read_bytes())
        if p.suffix=='.json':
            data=read(p)
            for q,h in data.get('evidence',{}).items():assert sha(Path(q).read_bytes())==h;evidence[q]=h
            for key,h in data.items():
                if key.endswith('_sha256') and isinstance(data.get(key[:-7]),str) and Path(data[key[:-7]]).is_file():
                    q=Path(data[key[:-7]]);assert sha(q.read_bytes())==h;evidence[str(q)]=h
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
        assert len(known)==6191 and len(fresh)==24 and not known&fresh
        fields=['id','file_path','block','kind','source_record_index','source_reference','source_hex','source_Japanese','source_complete_preamble_hex',
            'current_record_index','current_reference','current_hex','fresh_source_gloss','whole_exchange_note','command_offset','option_index','source_selector','english','compiled_hex','editorial_decision','localization_note','fresh_retained_wording_justification','review','reviewed_ordinary_boundaries','native_layout_retention_reason','actual_B22_display_fixture_observed','offline_only_native_display_checked','actual_label_visible','actual_choice_all_outcomes_observed']
        records=[{k:r[k] for k in fields if k in r} for r in rows]
        ROOT.mkdir(parents=True);(ROOT/'ledger.before.json.gz').write_bytes(gzip.compress(before,mtime=0))
        scopepath=Path(old['unfinished_editorial_scope_v5642']['path']);assert sha(scopepath.read_bytes())==old['unfinished_editorial_scope_v5642']['sha256']
        scope=deepcopy(read(scopepath));scope['next_focus']=NEXT
        scope['historical_Lil_B197_clean_pending_before_v5656']=scope.pop('next_Lil_B197_clean_review_pending')
        scope['next_Lil_B197_source_bound_uncredited_v5656']=dict(
            source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),clean_context=str(GLOSS),clean_context_sha256=sha(GLOSS.read_bytes()),
            objects=24,speeches=21,choice_labels=3,typed_three_option_menus=1,uncredited=True,
            clean_Japanese_whole_exchange_and_exact_three_label_gloss_complete=True,
            original_names_voices_dispatch_entry_six_relative_sites_and_opaque_leaf_contracts_bound=True,
            actual_prose_comparison_localization_current_native_display_and_release_pending=True,
            money8500_delegation_gift_47xx_disappearance_and_Charm_effect_context_pending=True)
        inventory=ROOT/'unfinished_editorial_scope_inventory.json';save(inventory,scope);evidence[str(inventory)]=sha(inventory.read_bytes())
        new=deepcopy(old)
        new[KEY]=dict(summary=SUMMARY,next=NEXT,source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=records,
            source_bound_uncredited_objects=24,speech_objects=21,typed_choice_labels=3,typed_choice_objects=1,source_prose_or_completion_credit_added=0,
            clean_stored_bytes=880,clean_logical_bytes=878,source_tailzeros=2,commands=39,progressive=20,FE=1,FI=0,FA=0,FO=0,
            source_2200_labels=['買おう','買わない','任せる'],third_option_is_delegation_not_refusal=True,
            source_actors=[21,169],source_voices={'21':1,'169':0},source_names={'21':'Ian Dukov','169':'Alluring Woman'},
            native_speech_dispatch_cases=42,native_name_consumers=4,relative_sites=6,native_clean_current_relative_cases=60,
            native_choice_count_calls=4,native_choice_label_calls=12,native_modal_bridged_selection_cancel_cases=8,
            exact_nonrelative_leaves=11,picture_descriptor=[0,140,1,5],source_resource_cases=10,source6003_cases=10,guarded_end_cases=10,
            clean_glosses_precede_old_English_speech_comparison=True,old_current_hex_and_label_getters_are_structural_not_translation_source=True,
            two_stopped_gloss_drafts_and_typed_inventory_classification_correction_preserved=True,
            remaining_gates=['source-money8500-affordability-debit-delegation-gift-and-Charm-effect-paths',
                'source-short4720-4735-disappearance-and-original-response-path-behavior','approved-cultural-money-stat-terminology',
                'whole-exchange-prior-English-comparison-and-natural-prose','native-speech-three-option-display-layout-and-relocation',
                'focused-actual-and-registered-cumulative-clean-patch-current-startup'],
            actual_B197_gameplay_observed=False,new_ROMs=0,new_emulator_runs=0,
            previous_goal_turn_classification='progress',current_goal_turn_classification='progress',evidence=evidence,full_goal_complete=False)
        new[SCOPE]=dict(path=str(inventory),sha256=sha(inventory.read_bytes()),Lil_B197_source_bound_uncredited_objects=24,
            broader_storylines_earlier_translations_town_shop_random_help_prose_and_retrospective_early_wrapping_open=True,
            graphics_and_later_older_record_technical_reaudit_separate=True,full_goal_complete=False)
        new[PREVIOUS]=old['latest_checkpoint'];new['latest_checkpoint']=SUMMARY;assert inverse(new)==old
        targets={LEDGER:encode_ledger(new)};assert len(targets[LEDGER])<100*1024*1024
        section='## V5656: B197 clean exchange and native source contracts;24 uncredited objects\n\n'+SUMMARY+'\n\n'
        for name in ['editorial_handoff_current.md','translation_progress.md','editorial_review_goal.md','todo.md','known_issues.md']:
            path=Path('docs')/name;text=path.read_text(encoding='utf-8')
            if name=='editorial_handoff_current.md':after='# Current editorial handoff - V5656\n\n'+section+NEXT+'\n\n'+text
            else:first,rest=text.split('\n',1);after=first+'\n\n'+section+rest.lstrip('\n')
            targets[path]=after.replace('\n','\r\n').encode('utf-8')
        files=[]
        for index,(target,data) in enumerate(targets.items()):
            planned=ROOT/f'{index:02d}.after';planned.write_bytes(data)
            if target!=LEDGER:(ROOT/f'{index:02d}.before').write_bytes(target.read_bytes())
            files.append(dict(target=str(target.resolve()),before_sha256=sha(target.read_bytes()),planned=str(planned.resolve()),planned_sha256=sha(data)))
        save(ROOT/'staged_checkpoint.json',dict(files=files,evidence=evidence,no_shared_mutation_yet=True,full_goal_complete=False))
        print('Six clean-source checkpoint targets staged;24 source objects remain uncredited.')
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
        print('Six audited clean-source checkpoint files applied exactly.')
    else:
        assert not VERIFY.exists() and read(ROOT/'application_receipt.json')['all6_targets_exact']
        plan=read(ROOT/'staged_checkpoint.json');new=audit(plan,True);prior=read(PRIOR);VERIFY.mkdir(parents=True)
        save(VERIFY/'verified_handoff.json',dict(ledger_sha256=sha(LEDGER.read_bytes()),candidate=prior['candidate'],candidate_sha256=prior['candidate_sha256'],
            patch=prior['patch'],patch_sha256=prior['patch_sha256'],all_original_root_and_nested_history_preserved=True,all_coverage_counters_unchanged=True,
            completed=6191,source_prose=6194,revised=3889,retained=2302,SC2=4306,SC3=96,reviewed_routes=4592,completed_routes=4592,
            source_bound_uncredited_Lil_B197_objects=24,B197_speeches=21,B197_choice_labels=3,B197_three_option_menus=1,
            exact_native_indices0_1_2_and_cancel_preserved=True,original_six_relative_sites60_cases_and_four_name_consumers_bound=True,
            prior_English_speech_comparison_prose_native_display_actual_and_registered_release_pending=True,
            source_8500_delegation_gift_47xx_disappearance_and_Charm_context_pending=True,
            new_editorial_credit=0,new_ROMs=0,new_emulator_runs=0,main_V4701_preserved=True,
            full_goal_active=True,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
        print('V5656 verified;V5637 remains current.24 B197 clean/source-bound objects uncredited;effect/decision context and prose next.Full editorial objective active.')
