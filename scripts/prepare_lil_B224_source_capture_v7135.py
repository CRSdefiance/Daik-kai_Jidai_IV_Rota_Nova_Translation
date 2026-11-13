"""Keep every original source command in an initialized whole-scene capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_source_capture_tools_v7135')
if __name__=='__main__':
    assert not ROOT.exists()
    fixture={'B220':'B224','source_fixture_v6930':'source_fixture_v7135','source_v6930':'source_v7135','source_v6921/seventeen_clean_current_empress_gown_exchange_source_references':'source_v7130/fifteen_clean_current_Medusa_flirtation_exchange_source_references','blocks[220]':'blocks[224]','source_block=220':'source_block=224','source_event220':'source_event224','len(jp)==1280 and end==1280 and jp[end:]==bytes(0)':'len(jp)==960 and end==958 and jp[end:]==bytes(2)','len(commands)==29 and len(speeches)==17':'len(commands)==27 and len(speeches)==15','all29_stored_fixture_commands':'all27_stored_fixture_commands','all20_source_commands_plus9_original_initializers':'all18_source_commands_plus9_original_initializers','clean-source17-speech empress-gown flirtation with all20 commands':'clean-source15-speech Medusa-shield flirtation with all18 commands','20 original+9 initializer commands;17 speeches':'18 original+9 initializer commands;15 speeches'}
    runner={'B220':'B224','source_fixture_v6930':'source_fixture_v7135','source_run_v6931':'source_run_v7136','source_v6931':'source_v7136',"selected['source_block']==220":"selected['source_block']==224",'source_event220':'source_event224',"'displayed_original_source_block':220":"'displayed_original_source_block':224",'all20_source_commands_retained':'all18_source_commands_retained'}
    jobs=[('scripts/research_lil_B220_source_fixture_v6930.py','scripts/research_lil_B224_source_fixture_v7135.py',fixture),('scripts/run_lil_B220_source_v6931.py','scripts/run_lil_B224_source_v7136.py',runner)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_whole_scene_tools.json',dict(tools=rows,all18_source_commands15_speeches_and_two_byte_tail_retained=True,nine_original_B22_initializers_without_new_roles_or_assignments=True,ordinary16001_frame_schedule_and_observer_unchanged=True,no_native_address_change=True,new_credit=0,full_goal_complete=False))
