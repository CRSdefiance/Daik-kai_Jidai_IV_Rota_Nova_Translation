"""Keep the complete original two-choice/eight-relative-site scene and ordinary initialized entry."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B206_source_fixture_tools_v6242')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/research_lil_B201_source_fixture_v5910.py','scripts/research_lil_B206_source_fixture_v6242.py',{
        'B201':'B206','source_fixture_v5910':'source_fixture_v6242','source_v5910':'source_v6242','work/analysis/lil_B201_source_v5902/all26_clean_current_complete_context_with_two_choice_labels.json':'work/analysis/lil_B206_source_v6232/all28_clean_current_complete_context_with_four_choice_labels.json','.blocks[201]':'.blocks[206]','source_block=201':'source_block=206',
        'len(jp)==1452 and end==1452 and jp[end:]==bytes(0)':'len(jp)==1524 and end==1522 and jp[end:]==bytes(2)','len(commands)==53':'len(commands)==51',"sum(c['word']==0xA000 for c in commands)==10":"sum(c['word']==0xA000 for c in commands)==7",'all53_stored_fixture_commands':'all51_stored_fixture_commands','all44_source_commands_plus9_original_initializers_stored':'all42_source_commands_plus9_original_initializers_stored','source_event201_not_naturally_activated':'source_event206_not_naturally_activated',
        'rigging-haggling-buy-refuse-and-three-stat-notices':'ceramic-earring-pitch-two-choices-purchase-and-two-refusals',
        '44 original+9 initializer commands,24 speeches,one2100/fourrelativesites/no predicates':'42 original+9 initializer commands,24 speeches,two2100/eightrelativesites/no predicates',
    })]
    tools.append(derive('scripts/run_lil_B201_source_buy_v5911.py','scripts/run_lil_B206_source_buy_v6243.py',{
        'B201':'B206','source_fixture_v5910':'source_fixture_v6242','source_run_v5911_buy':'source_run_v6243_buy','source_v5911_buy':'source_v6243_buy',"selected['source_block']==201":"selected['source_block']==206",'source_event201_not_naturally_selected':'source_event206_not_naturally_selected',"'displayed_original_source_block':201":"'displayed_original_source_block':206",'all44_source_commands_retained':'all42_source_commands_retained',
        'range(2600,12501,240)':'range(2600,15501,240)',"'--frames','13001'":"'--frames','16001'",'range(2350,13001,60)':'range(2350,16001,60)',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_fixture_and_first_unforced_path.json',dict(tools=tools,source_speeches=24,source_typed_choice_objects=2,source_typed_labels=4,source_commands=42,complete_fixture_commands=51,relative_sites=8,three_A000_plus_four_original_initializer_A000=True,source_stored1524_logical1522_tail2_preserved=True,no_assumed_menu_selection_cancel_affordability_or_effect_outcome=True,no_ROM_registry_ledger_or_review_credit_change_yet=True,full_goal_complete=False));print('B206 complete Japanese fixture/first ordinary-input run prepared:51 commands,24 speeches,two choices,eight relative sites;no forced state.')
