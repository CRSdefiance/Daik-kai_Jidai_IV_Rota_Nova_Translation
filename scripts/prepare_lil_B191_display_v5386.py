"""Prepare complete paired content fixtures with mixed thresholds and no-effect paths."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B191_display_tools_v5386')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/research_lil_B190_display_fixture_v5337.py','scripts/research_lil_B191_display_fixture_v5386.py',{
        'B190':'B191','display_fixture_v5337':'display_fixture_v5386','display_v5337':'display_v5386','combined_v5304':'combined_v5346',
        'relocation_v5328':'relocation_v5377b','editorial_manuscript_v3':'editorial_manuscript_v4','bank[190]':'bank[191]','source_block=190':'source_block=191',
        'len(commands)==29':'len(commands)==38','len(walk)==38 and len(speeches)==17':'len(walk)==47 and len(speeches)==13',
        "sum(c['word']==0xA000 for c in walk)==7":"sum(c['word']==0xA000 for c in walk)==8",
        "sum(c['word']==0x8000 for c in walk)==1":"sum(c['word']==0x8000 for c in walk)==3",
        "sum(c['word'] in [0x100,0x200,0x300,0x400] for c in walk)==6":"sum(c['word'] in [0x100,0x200,0x300,0x400] for c in walk)==16",
        'all38_stored_fixture_commands':'all47_stored_fixture_commands','all17_speeches16_progressive1_FE_one_predicate_six_branches_three_alternative_A000':'all13_speeches12_progressive1_FE_three_predicates16_branches_four_alternative_A000_or_no_effect',
        'closing_notice_names_Havana':'closing_notice_names_Calicut','source_event190':'source_event191','source_all29_commands':'source_all38_commands',
        'one_original_predicate_six_relative_sites':'three_original_mixed_predicates16_relative_sites','stored_speech_objects=17':'stored_speech_objects=13',
        'all29 commands+9 original init commands,sixteen progressive/one impersonal FE,one predicate,six relative sites,three alternative A000s':'all38 commands+9 original init commands,twelve progressive/one impersonal FE,three mixed predicates,16relative sites,four alternative A000s and no-effect paths',
    })]
    rows.append(derive('scripts/pin_lil_B190_display_v5338.py','scripts/pin_lil_B191_display_v5387.py',{
        'B190':'B191','display_tools_v5338':'display_tools_v5387','display_fixture_v5337':'display_fixture_v5386',
        'source_speeches=17,progressive=16':'source_speeches=13,progressive=12','source_commands=29,stored_fixture_commands=38':'source_commands=38,stored_fixture_commands=47','All17 panels':'All13 panels',
    }))
    rows.append(derive('scripts/run_lil_B190_display_fixture_v5339.py','scripts/run_lil_B191_display_fixture_v5388.py',{
        'B190':'B191','display_fixture_v5337':'display_fixture_v5386','display_run_v5339':'display_run_v5388','display_v5339':'display_v5388',
        'source_event190':'source_event191',"'displayed_original_source_block':190":"'displayed_original_source_block':191",
        'all_source29_commands_16_progressive1_FE_one_predicate_six_branches_three_A000':'all_source38_commands_12_progressive1_FE_three_predicates16_branches_four_A000_or_no_effect',
    }))
    rows.append(derive('scripts/audit_lil_B190_actual_v5340b.py','scripts/audit_lil_B191_actual_v5389.py',{
        'B190':'B191','actual_v5340b':'actual_v5389','display_fixture_v5337':'display_fixture_v5386',
        'fonts_v5326/all17_progressive_FE_native_planes_and136_alignment_cases':'fonts_v5374b/all13_progressive_FE_native_planes_and104_alignment_cases',
        'display_run_v5339':'display_run_v5388','display_v5339':'display_v5388','source_event190':'source_event191',
        'all_source29_commands_16_progressive1_FE_one_predicate_six_branches_three_A000':'all_source38_commands_12_progressive1_FE_three_predicates16_branches_four_A000_or_no_effect',
        "source['block']!=190":"source['block']!=191",'original_source_block=190':'original_source_block=191',
        "pair.get('original_source_block')==190":"pair.get('original_source_block')==191","r.get('original_source_block')==190":"r.get('original_source_block')==191",
        'all38_stored':'all47_stored','==38':'==47',
        'result=0 if roll<500 else 1 if roll==500 else 2':"threshold=int.from_bytes(block[cursor+4:cursor+8],'little');assert threshold in [500,700]\n                result=0 if roll<threshold else 1 if roll==threshold else 2",
        'actual_unforced_original_LCG_transition=True':'actual_unforced_original_LCG_transition=True,threshold=threshold',
        "selected[-1]['original_source_offset']==602":"selected[-1]['original_source_offset']==730",
        "len(intervals)==len({r['id'] for r in intervals})==17":"len(intervals)==len({r['id'] for r in intervals})==13",
        "len(predicates)==1 and predicates[0]['source_offset']==8":"len(predicates)==2 and predicates[0]['source_offset']==8 and predicates[1]['source_offset'] in [28,76]",
        'len(effect_offsets)==1 and effect_offsets[0] in [28,40,52]':'len(effect_offsets) in [0,1] and all(at in [48,60,96,108] for at in effect_offsets)',
        "ui[0]['original_source_offset']==600":"ui[0]['original_source_offset']==728",'single_source_end602':'single_source_end730','len(actual)==17':'len(actual)==13',
        'actual_all17_progressive_FE_RNG_effect':'actual_all13_progressive_FE_RNG_effect_or_no_effect','fresh_actual_unique_speech_panels=17':'fresh_actual_unique_speech_panels=13',
        'all29_source_commands':'all38_source_commands','all17_speeches16_progressive1':'all13_speeches12_progressive1','actual_source_event190':'actual_source_event191','actual_panels=17':'actual_panels=13',
        'original_selected_effect_C200':'original_selected_effect_or_no_effect_C200',
    }))
    rows.append(derive('scripts/review_lil_B190_actual_v5341b.py','scripts/review_lil_B191_actual_v5390.py',{
        'B190':'B191','actual_review_v5341b':'actual_review_v5390','actual_v5340b':'actual_v5389','actual_all17_progressive_FE_RNG_effect':'actual_all13_progressive_FE_RNG_effect_or_no_effect',
        'display_fixture_v5337':'display_fixture_v5386','display_v5339':'display_v5388','display_run_v5339':'display_run_v5388',
        "actual['complete_matching_observations']==17":"actual['complete_matching_observations']==13","len(v['selected_intervals'])==17":"len(v['selected_intervals'])==13",'single_source_end602':'single_source_end730',
        "len(v['source_A000'])==len(v['source_C200'])==1":"len(v['source_A000']) in [0,1] and len(v['source_C200'])==1",
        "['DK4_MES_B190_R0032','DK4_MES_B190_R0056','DK4_MES_B190_R0067','DK4_MES_B190_R0085']":"['DK4_MES_B191_R0056','DK4_MES_B191_R0064','DK4_MES_B191_R0088','DK4_MES_B191_R0100']",
        'all17_complete_held_planes':'all13_complete_held_planes','all17_speeches16_progressive1':'all13_speeches12_progressive1',
        'source_selected_effect_C200_single_end602':'source_selected_effect_or_no_effect_C200_single_end730','source_event190':'source_event191',
        'conditional_commands17_planes':'conditional_commands13_planes','complete_panels=17':'complete_panels=13',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_complete_fixture_and_actual_checks.json',dict(tools=rows,source_commands=38,init_commands=9,stored_commands=47,speeches=13,
        three_mixed_predicates16_relative_sites_four_alternative_effects_and_no_effect_paths_stored=True,
        actual_two_used_predicates_and_zero_or_one_effect_to_be_measured_without_forcing=True,
        two9001_frame_content_boots_planned=True,no_natural_activation_or_earned_state_claim=True,no_credit=True,full_goal_complete=False))
