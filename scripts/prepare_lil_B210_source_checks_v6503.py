"""Prepare B210's complete source scene, own control/end checks and source event binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B210_source_tools_v6503')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/research_lil_B208_source_fixture_v6397.py','scripts/research_lil_B210_source_fixture_v6503.py',{
        'B208':'B210','source_fixture_v6397':'source_fixture_v6503','source_v6390/all24_clean_current_complete_context.json':'source_v6498/ten_clean_current_complete_exchange_source_references.json','_source_v6397_':'_source_v6503_',
        'blocks[208]':'blocks[210]','source_block=208':'source_block=210','source_event208':'source_event210',
        'len(jp)==1188 and end==1186':'len(jp)==688 and end==686',
        "len(commands)==38 and len(speeches)==24":"len(commands)==21 and len(speeches)==10",
        "sum(c['word']==0xA000 for c in commands)==6":"sum(c['word']==0xA000 for c in commands)==5",'all38_stored_fixture_commands':'all21_stored_fixture_commands','all29_source_commands_plus9':'all12_source_commands_plus9',
        'pirate-sword-conversation-private-thought-and-named-attribute-notice':'local-lord-reddish-sword-rumor-ten-original-speeches-and-one-original-A000',
        '29 original+9 initializer commands,24 panels(23 progressive/one FE),private thought,no choices/relatives/predicates/macros':'12 original+9 initializer commands,10 progressive speeches,one original A000,no FE/typed objects/choices/relatives/predicates/macros',
    }))
    rows.append(derive('scripts/run_lil_B209_source_v6454.py','scripts/run_lil_B210_source_v6504.py',{'B209':'B210','source_fixture_v6453':'source_fixture_v6503','source_run_v6454':'source_run_v6504','_source_v6454':'_source_v6504',"selected['source_block']==209":"selected['source_block']==210",'source_event209':'source_event210',"'displayed_original_source_block':209":"'displayed_original_source_block':210",'all18_source_commands_retained':'all12_source_commands_retained'}))
    rows.append(derive('scripts/prove_lil_B208_controls_v6396.py','scripts/prove_lil_B210_controls_v6505.py',{
        'all five B208 leaves':'both B210 leaves','B208':'B210','controls_v6396':'controls_v6505','source_v6390/all24_clean_current_complete_context.json':'source_v6498/ten_clean_current_complete_exchange_source_references.json','blocks[208]':'blocks[210]','==29':'==12',
        "[(1118,'0560'),(1120,'2e63'),(1166,'00a0ffff01020760'),(1174,'00a0ffff28000110'),(1182,'00000000')]":"[(674,'00a0ffff24000110'),(682,'00000000')]",
        '(1188,1186)':'(688,686)','b[1182:1186]':'b[682:686]','stored_bytes=1188,logical_end=1186':'stored_bytes=688,logical_end=686',',b,1182,previous)':',b,682,previous)',
        'len(structural)==4':'len(structural)==1','four_source_current_structural_pairs':'one_source_current_structural_pair','all5_source_current_nontext_leaves':'all2_source_current_nontext_leaves','source6005_632E_two_A000_structural_pairs':'source_A000_structural_pair','source_stored1188_logical1186_tail2_complete_end1182':'source_stored688_logical686_tail2_complete_end682','no_inherited_B207_A000_operand_or_zero_FE_assumption':'no_inherited_B209_typed_relative_predicate_or_A000_operand_assumption','source_23_progressive_one_FE_private_thought_and_literal_character_notice_preserved':'source10_static_progressive_speeches_no_FE_or_macro_preserved','four source/current structural pairs(6005,632E,two A000)':'one source/current A000 structural pair',
    }))
    rows.append(derive('scripts/prove_lil_B209_entry_v6471.py','scripts/prove_lil_B210_entry_v6506.py',{'B209':'B210','entry_v6471':'entry_v6506','source_v6450d/all20_clean_current_letter_and_voice_alternative_context.json':'source_v6498/ten_clean_current_complete_exchange_source_references.json','current_V6439_native_v6449':'current_V6488_native_v6497','[209]':'[210]'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,source_commands=12,complete_source_objects=10,source_stored688_logical686_tail2=True,no_forced_actor_role_roster_condition_RNG_result_RAM_or_progress=True,all_native_instruction_constants_preserved=True,actual_source_capture_pending=True,full_goal_complete=False));print('B210 full12-command source fixture,ordinary source runner,own A000/end checks and source event getter tools prepared;no new ROM or run yet.')
