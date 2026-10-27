"""Derive the atomic typed-menu compiler with B166's distinct predicate/effect/end contract."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B166_compiler_tools_v4107')
SOURCE = Path('dk4tool/patch/lil_B164_editorial_v2.py')
TARGET = Path('dk4tool/patch/lil_B166_editorial_v1.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text = SOURCE.read_text(encoding='utf-8')
    original = text
    text = text.replace('B164','B166')
    text = re.sub(r'\b164\b','166',text)
    changes = {
        'lil_B166_layout_v2':'lil_B166_layout_v4',
        'SELECTORS={2,9,13}':'SELECTORS={2,9,20,23}',
        'all49':'all44','all47':'all42','==47':'==42','==49':'==44',
        '==376':'==336','==188':'==168',
        "len(native['source_consumer_negative_controls'])==15":"len(native['source_consumer_negative_controls'])==17",
        'all9_source_current_target_nonrelative_nonspeech_nonchoice_leaves':'all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves',
        "len(controls['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==9":"len(controls['all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves'])==11",
        'all42_progressive_consumers_three_static_actors_no_macros_exact':'all42_progressive_consumers_four_static_actors_FI3_exact',
        "controls['source0D_preserved_not_stripped_older_record_audit_still_open']":"controls['older_record_technical_reaudit_still_open'] and controls['unforced_Fernando_result_matches_source_without_roster_fixture'] and len(controls['relocated_predicate_pairs'])==1 and all(r['current_source_case']['native_result']==r['relocated_case']['native_result'] for r in controls['relocated_predicate_pairs'])",
        'all4_declared_end_decodes_return_type0_extent4_without_post_payload_read':'all2_declared_end_decodes_return_type0_extent4_without_post_payload_read',
        "len(ends['cases'])==4":"len(ends['cases'])==2 and ends['B166_single_end_is_declared_logical_tail']",
        "len(sample['viewed_actual_sheets'])==8":"len(sample['viewed_actual_sheets'])==7",
        "set(sample['actual_sampled_display_IDs'])=={r['id'] for r in rows}":"set(sample['actual_sampled_display_IDs'])=={r['id'] for r in rows}-{'DK4_MES_B166_R0087'}",
        "raw.count(m.encode())==row['english'].count('{MACRO:'+m+'}')==0":"raw.count(m.encode())==row['english'].count('{MACRO:'+m+'}')",
        "'unexpected macro:'+ident":"'source macro differs:'+ident",
        'at==1654':'at==2152',"['聞く','聞かない']":"['お願いする','遠慮する']",
        "[b'Yes',b'No']":"[b'Please do',b'Decline']",
        "len(edges)==4 and len(spec['target_native_skip_cases'])==20":"len(edges)==8 and len(spec['target_native_skip_cases'])==40",
        'len(commands)==61':'len(commands)==62',
        "[1854,3454] and stops[0]['new_offset']+4<stops[1]['new_offset']":"[2948] and len(stops)==1",
        "'two separated ends differ'":"'single declared tail end differs'",
        "next(c['old_offset'] for c in commands if c['word']==0xA000)<at and sum(c['word']==0x632B for c in commands)==1":"next(c['old_offset'] for c in commands if c['word']==0xA000)==2940>at and sum(c['word']==0x632B for c in commands)==sum(c['word']==0x632C for c in commands)==1 and sum(c['word']==0x8000 for c in commands)==1",
        "'recruitment-before-advice/resource scope differs'":"'late recruitment,one predicate,two resources scope differs'",
        'relative_operands=4,source_commands=61':'relative_operands=8,source_commands=62',
        'all44_reviewed_objects_one_menu_four_spans_two_separated_ends_and9_leaves_preserved':'all44_reviewed_objects_one_menu_eight_spans_one_tail_end_and11_leaves_preserved',
    }
    applied = []
    for old,new in changes.items():
        assert old in text, old
        text = text.replace(old,new)
        applied.append(dict(old=old,new=new))
    flags = ['all62_commands8_relative_sites40_target_skips_verified','all42_active_speech_targets_preserved',
        'one2100_object_two_labels_and_source_indices_0_1_cancel_verified',
        'all11_opaque_leaves_one_predicate_one_effect_two_resources_six_presentations_and_end_exact',
        'single_declared_tail_end_after_advice_rejoin_preserved','no_source_FE_2000_C200_or_dynamic_objects','representative_shared_rules_approved']
    lines = text.splitlines()
    for index,line in enumerate(lines):
        if line.startswith('FLAGS='):
            lines[index] = 'FLAGS='+repr(flags)
        elif line.strip().startswith("require(names['source_current_progressive_nameplate']"):
            lines[index] = '''    require(names['source_selector17_is_static_actor23_and14_is_static_actor20'] and names['original_Fernando_width_forms_preserved_without_name_asset_change'] and names['later_older_record0D_reaudit_stays_open'] and names['approved_prose_names']=={'23':'Manuel Almeida','20':'Fernando Dias','9':'Camille'},'source-owned Manuel,Fernando,Camille names required');require({(r['actor_ID'],r['consumer']):r['text'] for r in names['native_six_consumer_cases']['rows']}=={(9,'progressive-nameplate'):'Camille Overijssel',(9,'full-catalogue'):'Camille Marinus Overijssel',(20,'progressive-nameplate'):'Ｆernando Dias',(20,'full-catalogue'):'Ｆernando Dias',(23,'progressive-nameplate'):'Manuel Almeida',(23,'full-catalogue'):'Manuel Almeida'} and all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_recovers_all4MiB'] for r in names['native_six_consumer_cases']['rows']),'complete six-name scratch/consumer proof required')'''
        elif line.strip().startswith("require(sample['actual_four_disclosed_cold_boots_pass']"):
            lines[index] = '''    require(sample['actual_four_disclosed_cold_boots_pass'] and sample['new_emulator_runs']==4 and sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_Manuel17_original_nameplate_portrait_and_full_figure_observed'] and sample['actual41_unique_panels73_observations_both_advice_results_and_normal_returns_pass'] and sample['source_Fernando_query8_relative_containers_choice_and_single_end_retained_not_flattened'] and sample['source_recruitment_effect_excluded'] and sample['original_B22_four_A000_initialization_commands_retained'] and sample['actual_selected_B166_source_events']==[],'complete representative actual approval required');require(sample['offline_only_display_IDs']==['DK4_MES_B166_R0087'] and sample['Fernando_remark_not_actual_or_byte_identical_reuse'],'actual/offline display distinction required');offline=sample['offline_only_display_cases'];require(len(offline)==1 and offline[0]['id']=='DK4_MES_B166_R0087' and offline[0]['source_selector']==20 and offline[0]['actual_display_or_byte_identical_reuse_claim'] is False and offline[0]['reason'],'complete offline Fernando explanation required')'''
    text = '\n'.join(lines)+'\n'
    text = text.replace(text.splitlines()[0],'"""Atomic B166 layer:42 speeches,two labels,eight spans,FI3,Fernando predicate and one late effect/end."""',1)
    assert 'Cesare' not in text and '1854' not in text and '3454' not in text
    assert 'all49' not in text and 'all47' not in text and 'no_macros_exact' not in text
    compile(text,str(TARGET),'exec')
    TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(SOURCE),previous_sha256=sha(SOURCE.read_bytes()),
        successor=str(TARGET),successor_sha256=sha(TARGET.read_bytes()),replacements=applied,
        added_exact_six_name_and_single_offline_Fernando_guards=True,source_FI3_predicate_two_resources_single_end_guarded=True,
        no_ROM_registry_ledger_completion_change=True))
    print('B166 atomic typed-menu compiler created;source-specific names,predicate,FI3 and single late effect/end guarded.')
