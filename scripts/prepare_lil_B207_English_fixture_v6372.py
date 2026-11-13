"""Prepare complete English B207 with the exact retained source inputs and11001-frame scope."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B207_English_fixture_tools_v6372')
if __name__=='__main__':
    assert not ROOT.exists()
    old='''    runner=derive('scripts/run_lil_B205_source_fixture_v6181.py','scripts/run_lil_B205_English_fixture_v6210.py',{
        'source_fixture_v6180':'English_fixture_v6209','complete_B205_source_B22_fixture':'complete_B205_English_B22_fixture',"selected['case']=='clean_Japanese'":"selected['case']=='reviewed_English'",'source_run_v6181_clean_Japanese':'English_run_v6210_reviewed_English','source_v6181_clean_Japanese':'English_v6210_reviewed_English','B205 Japanese content':'B205 reviewed English content',
    })'''
    new='''    runner=derive('scripts/run_lil_B207_source_v6346.py','scripts/run_lil_B207_English_v6373.py',{
        'source_fixture_v6345':'English_fixture_v6372','complete_B207_source_B22_fixture':'complete_B207_English_B22_fixture',"selected['case']=='clean_Japanese'":"selected['case']=='reviewed_English'",'source_run_v6346':'English_run_v6373','source_v6346':'English_v6373','B207 Japanese content':'B207 reviewed English content',
    })'''
    row=derive('scripts/research_lil_B205_English_fixture_v6209.py','scripts/research_lil_B207_English_fixture_v6372.py',{
      old:new,'B205':'B207','from scripts.prepare_lil_B205_references_v6200 import PARENT,PLAN':'from scripts.create_lil_B207_reference_v6367 import PARENT,PLAN',
      'English_fixture_v6209':'English_fixture_v6372','English_v6209':'English_v6372',
      'source_fixture_v6180':'source_fixture_v6345','loader_v6205':'loader_v6368','reference_census_v6206':'reference_census_v6369','all25_commands':'all15_commands','all25_clean':'all15_clean',
      'relocated_controls_v6208':'relocated_controls_v6371','all17_dispatches_one_picture_one47xx_pair_and8_exact_leaves':'all13_dispatches_one_A000_and10_guarded_ends',
      "len(controls['relocated_dispatch_cases'])==17":"len(controls['relocated_dispatch_cases'])==13",'bank[205]':'bank[207]','len(native)==25 and len(commands)==34 and len(speeches)==17':'len(native)==15 and len(commands)==24 and len(speeches)==13',"sum(c['word']==0xA000 for c in commands)==7":"sum(c['word']==0xA000 for c in commands)==5",'source_block=205':'source_block=207','all34_stored_fixture_commands':'all24_stored_fixture_commands','all25_source_commands_plus9_initializers':'all15_source_commands_plus9_initializers','not_natural_event205_activation':'not_natural_event207_activation',
      'parrot/five-echo/two-sound/capture/transition':'Minotaur-axe-request/conditional-search/undecided-gift/return',
      '25 source+9 initializer commands,17 objects,five FE echoes/two sounds,unchanged current item data':'15 source+9 initializer commands,13 progressive objects,no FE/macros/choices/branches,unchanged current name/item data'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_English_fixture.json',dict(tool=row,source_commands=15,source_speeches=13,complete_fixture_commands=24,source_inputs_and11001_frame_scope_preserved=True,no_forced_state_result_eligibility_or_quest_effect_claim=True,new_review_credit=0,full_goal_complete=False));print('B207 complete revised-English fixture/runner prepared against the retained source schedule;no omitted commands or forced state.')
