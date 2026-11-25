"""Prepare the complete B208 content fixture and its explicitly limited cold boot."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_source_tools_v6397')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/research_lil_B207_source_fixture_v6345.py','scripts/research_lil_B208_source_fixture_v6397.py',{
        'B207':'B208','source_fixture_v6345':'source_fixture_v6397','source_v6338':'source_v6390','all13_clean_current_complete_context.json':'all24_clean_current_complete_context.json','_source_v6345_':'_source_v6397_',
        'blocks[207]':'blocks[208]','source_block=207':'source_block=208','source_event207':'source_event208',
        'len(jp)==656 and end==654':'len(jp)==1188 and end==1186',
        'len(commands)==24 and len(speeches)==13':'len(commands)==38 and len(speeches)==24',
        "sum(c['word']==0xA000 for c in commands)==5":"sum(c['word']==0xA000 for c in commands)==6",
        'all24_stored_fixture_commands':'all38_stored_fixture_commands','all15_source_commands_plus9':'all29_source_commands_plus9',
        'Minotaur-axe-request-conditional-search-and-gift':'pirate-sword-conversation-private-thought-and-named-attribute-notice',
        '15 original+9 initializer commands,13 speeches,no choices/relatives/predicates/FE/macros':'29 original+9 initializer commands,24 panels(23 progressive/one FE),private thought,no choices/relatives/predicates/macros'}))
    rows.append(derive('scripts/run_lil_B207_source_v6346.py','scripts/run_lil_B208_source_v6398.py',{
        'B207':'B208','source_fixture_v6345':'source_fixture_v6397','source_run_v6346':'source_run_v6398','_source_v6346':'_source_v6398',
        "selected['source_block']==207":"selected['source_block']==208",'source_event207':'source_event208',"'displayed_original_source_block':207":"'displayed_original_source_block':208",'all15_source_commands_retained':'all29_source_commands_retained',
        '11001':'16001','10501':'15501'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,no_source_omissions_or_forced_conditions_roster_funds_RNG_results_RAM_battery_or_savestate=True,full_goal_complete=False));print('Complete B208 source fixture and16001-frame ordinary-input runner prepared;no natural event claim.')
