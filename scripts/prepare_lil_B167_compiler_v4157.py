"""Derive an atomic compiler for the complete B167 sail lesson and typed menu."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_compiler_tools_v4157')
SOURCE=Path('dk4tool/patch/lil_B166_editorial_v1.py')
TARGET=Path('dk4tool/patch/lil_B167_editorial_v1.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists();original=SOURCE.read_text(encoding='utf-8')
    text=re.sub(r'\b166\b','167',original.replace('B166','B167'))
    changes={
        'lil_B167_layout_v4':'lil_B167_layout_v6','SELECTORS={2,9,20,23}':'SELECTORS={2,4,13,23,109}',
        'all44':'all29','all42':'all27','==42':'==27','==44':'==29','==336':'==216','==168':'==108',
        "len(native['source_consumer_negative_controls'])==17":"len(native['source_consumer_negative_controls'])==19",
        'all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves':'all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves',
        "len(controls['all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==11":"len(controls['all6_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==6",
        'all27_progressive_consumers_four_static_actors_FI3_exact':'all27_progressive_consumers_five_static_actors_no_macros_exact',
        'unforced_Fernando_result_matches_source_without_roster_fixture':'both_unforced_Cesare_results_match_source_without_roster_fixture',
        "len(controls['relocated_predicate_pairs'])==1":"len(controls['relocated_predicate_pairs'])==2",
        'all2_declared_end_decodes':'all4_declared_end_decodes',
        "len(ends['cases'])==2 and ends['B167_single_end_is_declared_logical_tail']":"len(ends['cases'])==4 and ends['B167_first_end_precedes_second_end_and_declared_logical_end']",
        "len(sample['viewed_actual_sheets'])==7":"len(sample['viewed_actual_sheets'])==5",
        "{'DK4_MES_B167_R0087'}":"{'DK4_MES_B167_R0045','DK4_MES_B167_R0131'}",
        "raw.count(m.encode())==row['english'].count('{MACRO:'+m+'}')":"raw.count(m.encode())==row['english'].count('{MACRO:'+m+'}')==0",
        'at==2152':'at==152',"['お願いする','遠慮する']":"['いいわよ','やめとくわ']", "[b'Please do',b'Decline']":"[b'Okay',b'No thanks']",
        "len(edges)==8 and len(spec['target_native_skip_cases'])==40":"len(edges)==12 and len(spec['target_native_skip_cases'])==60",
        'len(commands)==62':'len(commands)==46',
        "[2948] and len(stops)==1":"[430,2172] and len(stops)==2 and stops[0]['new_offset']+4<stops[1]['new_offset']",
        "'single declared tail end differs'":"'two separated source ends differ'",
        "sum(c['word']==0xA000 for c in commands)==1 and next(c['old_offset'] for c in commands if c['word']==0xA000)==2940>at and sum(c['word']==0x632B for c in commands)==sum(c['word']==0x632C for c in commands)==1 and sum(c['word']==0x8000 for c in commands)==1":"sum(c['word']==0xA000 for c in commands)==0 and sum(c['word']==0x6327 for c in commands)==sum(c['word']==0x632B for c in commands)==1 and sum(c['word']==0x8000 for c in commands)==2",
        "'late recruitment,one predicate,two resources scope differs'":"'two predicates,two resources,no A000 scope differs'",
        'relative_operands=8,source_commands=62':'relative_operands=12,source_commands=46',
        'all29_reviewed_objects_one_menu_eight_spans_one_tail_end_and11_leaves_preserved':'all29_reviewed_objects_one_menu_twelve_spans_two_separate_ends_and6_leaves_preserved',
        "'49 exact records required'":"'29 exact records required'"
    }
    applied=[]
    for old,new in changes.items():assert old in text,old;text=text.replace(old,new);applied.append(dict(old=old,new=new))
    flags=['all46_commands12_relative_sites60_target_skips_verified','all27_active_speech_targets_preserved','one2100_object_two_labels_and_source_indices_0_1_cancel_verified','all6_opaque_leaves_two_predicates_two_resources_and_two_ends_exact','two_separate_refusal_and_lecture_endwords_preserved','no_source_FE_2000_C200_or_dynamic_objects','representative_shared_rules_approved']
    lines=text.splitlines()
    for i,line in enumerate(lines):
        if line.startswith('FLAGS='):lines[i]='FLAGS='+repr(flags)
        elif line.strip().startswith("require(names['source_selector17_is_static_actor23_and14_is_static_actor20']"):
            lines[i]="""    require(names['source_selector6D_is_static_actor109_not_literal_m'] and names['source_selector0D_is_static_actor13_not_CR'] and names['generic_source_Shipwright_role_bound_without_inventing_personal_name'] and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names']=={'2':'Lil','4':'Janus','13':'Cesare','23':'Manuel','109':'Shipwright'},'source-owned five actor identities required');namecases=names['native_ten_consumer_cases']['rows'];expectednames={2:'Lil Argot',4:'Janus Pasar',13:'Cesare Tony',23:'Manuel Almeida',109:'Shipwright'};require(len(namecases)==10 and {(r['actor_ID'],r['consumer']):r['text'] for r in namecases}=={(n,c):v for n,v in expectednames.items() for c in ['progressive-nameplate','full-catalogue']} and all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in namecases),'complete ten original name-consumer proof required');require(all(r['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring' and not r['original_scratch_rings'] and not r['original_getter_writes'] for r in namecases if r['actor_ID']==109),'Shipwright read-only name path required')"""
        elif line.strip().startswith("require(sample['actual_four_disclosed_cold_boots_pass']"):
            lines[i]="""    require(sample['actual_four_disclosed_cold_boots_pass'] and sample['new_emulator_runs']==4 and sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_Shipwright109_Lil2_Janus4_Manuel23_original_names_and_portraits_observed'] and sample['actual25_unique_panels28_observations_both_choices_and_distinct_returns_pass'] and sample['source_two_Cesare_queries12_relative_containers_choice_and_both_ends_retained_not_flattened'] and sample['no_B167_effect_or_source_command_omitted'] and sample['original_B22_four_A000_initialization_commands_retained'] and sample['actual_selected_B167_source_events']==[],'complete representative actual approval required');require(sample['offline_only_display_IDs']==['DK4_MES_B167_R0045','DK4_MES_B167_R0131'] and sample['both_Cesare_remarks_not_actual_or_byte_identical_reuse'],'actual/offline display distinction required');offline=sample['offline_only_display_cases'];require(len(offline)==2 and {r['id'] for r in offline}=={'DK4_MES_B167_R0045','DK4_MES_B167_R0131'} and all(r['source_selector']==13 and r['actual_display_or_byte_identical_reuse_claim'] is False and r['reason'] for r in offline),'complete offline Cesare explanations required')
    actualpaths=[p for p in sample['evidence'] if p.endswith('actual_both_choices_conditional_panels_and_distinct_returns.json')];require(len(actualpaths)==1,'one exact actual outcome proof required');actual=load(actualpaths[0]);require(sha(Path(actualpaths[0]).read_bytes())==sample['evidence'][actualpaths[0]] and not actual['failures'] and len(actual['versions'])==4 and {(r['option_index'],r['case']) for r in actual['versions']}=={(o,c) for o in [0,1] for c in ['clean_Japanese','reviewed_English']},'four distinct actual paths required');require(all(v['actual_choice_command_pair']['result_words']==[2,v['option_index']] and v['actual_unforced_Cesare_predicate']['result_words']==[2,0] and v['source_end_offset']==(2172 if v['option_index']==0 else 430) and v['selected_B22_command_pairs'][-1]['result_words']==[0,0] for v in actual['versions']),'actual menu and later query result must remain distinct')"""
    text='\n'.join(lines)+'\n';text=text.replace(text.splitlines()[0],'"""Atomic B167:27 speeches,two labels,twelve spans,two Cesare queries,two resources and distinct ends."""',1)
    assert 'Fernando' not in text and '2948' not in text and '2152' not in text and 'all44' not in text
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(previous=str(SOURCE),previous_sha256=sha(SOURCE.read_bytes()),successor=str(TARGET),successor_sha256=sha(TARGET.read_bytes()),replacements=applied,exact_five_names_ten_owned_or_readonly_consumers_guarded=True,source0D_and_printable6D_no_macros_two_queries_two_ends_and_distinct_actual_results_guarded=True,no_ROM_registry_ledger_completion_change=True))
    print('B167 atomic compiler created;full source controls,names,typed menu and separate end/result contracts guarded.')
