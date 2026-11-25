"""Prepare a complete letter-scene fixture without forcing its original branch or voice choices."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_source_tools_v6453')
if __name__=='__main__':
    assert not ROOT.exists();rows=[]
    rows.append(derive('scripts/research_lil_B208_source_fixture_v6397.py','scripts/research_lil_B209_source_fixture_v6453.py',{
        'B208':'B209','source_fixture_v6397':'source_fixture_v6453','source_v6390/all24_clean_current_complete_context.json':'source_v6450d/all20_clean_current_letter_and_voice_alternative_context.json','_source_v6397_':'_source_v6453_',
        'blocks[208]':'blocks[209]','source_block=208':'source_block=209','source_event208':'source_event209',
        'len(jp)==1188 and end==1186 and jp[end:]==bytes(2)':'len(jp)==1148 and end==1148 and jp[end:]==bytes(0)',
        'len(commands)==38 and len(speeches)==24 and sum(c[\'word\']==0x8000 for c in commands)==0':'len(commands)==27 and len(speeches)==5 and sum(c[\'word\']==0x8000 for c in commands)==1',
        "sum(c['word']==0xA000 for c in commands)==6":"sum(c['word']==0xA000 for c in commands)==5",
        'all38_stored_fixture_commands':'all27_stored_fixture_commands','all29_source_commands_plus9':'all18_source_commands_plus9',
        'pirate-sword-conversation-private-thought-and-named-attribute-notice':'formal-Muramasa-letter-two-automatic-voice-objects-and-original-conditional-reaction',
        '29 original+9 initializer commands,24 panels(23 progressive/one FE),private thought,no choices/relatives/predicates/macros':'18 original+9 initializer commands,5 speech objects,2 automatic4100 voice objects,original predicate/relative sites,zero FE/player choices',
        'explicitly_excluded_original_commands=[],all38_stored_fixture_commands=commands':'explicitly_excluded_original_commands=[],source_typed_actor_style_records=packet[\'typed_actor_style_records\'],all27_stored_fixture_commands=commands',
    }))
    rows.append(derive('scripts/run_lil_B208_source_v6398.py','scripts/run_lil_B209_source_v6454.py',{
        'B208':'B209','source_fixture_v6397':'source_fixture_v6453','source_run_v6398':'source_run_v6454','_source_v6398':'_source_v6454',
        "selected['source_block']==208":"selected['source_block']==209",'source_event208':'source_event209',"'displayed_original_source_block':208":"'displayed_original_source_block':209",'all29_source_commands_retained':'all18_source_commands_retained',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tools.json',dict(tools=rows,all18_original_commands_plus9_initializers_preserved=True,five_speech_objects15_stored_automatic_alternatives_not_all_conditionally_observed_claim=True,no_forced_actor_role_roster_RNG_results_RAM_battery_or_savestate=True,actual_source_capture_pending=True,full_goal_complete=False))
