"""Prepare full revised B208 against retained16001-frame source inputs without replay."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_English_fixture_tools_v6429')
if __name__=='__main__':
    assert not ROOT.exists();p=Path('scripts/research_lil_B207_English_fixture_v6372.py');source=p.read_text('utf-8');a=source.index('    runner=derive(');b=source.index("    save(ROOT/'pin_and_runner_receipt.json'",a)
    runner='''    runner=derive('scripts/run_lil_B208_source_v6398.py','scripts/run_lil_B208_English_v6430.py',{
        'source_fixture_v6397':'English_fixture_v6429','complete_B208_source_B22_fixture':'complete_B208_English_B22_fixture',"selected['case']=='clean_Japanese'":"selected['case']=='reviewed_English'",'source_run_v6398':'English_run_v6430','source_v6398':'English_v6430','B208 Japanese content':'B208 reviewed English content',
    })
'''
    r=derive(str(p),'scripts/research_lil_B208_English_fixture_v6429.py',{
        source[a:b]:runner,'B207':'B208','create_lil_B207_reference_v6367':'create_lil_B208_reference_v6424','English_fixture_v6372':'English_fixture_v6429','English_v6372':'English_v6429','source_fixture_v6345':'source_fixture_v6397',
        'loader_v6368':'loader_v6425','reference_census_v6369':'reference_census_v6426','all15_commands':'all29_commands','all15_clean':'all29_clean','relocated_controls_v6371':'relocated_controls_v6428','all13_dispatches_one_A000_and10_guarded_ends':'all24_dispatches_four_structural_effects_and10_guarded_ends',
        "len(controls['relocated_dispatch_cases'])==13":"len(controls['relocated_dispatch_cases'])==24",'bank[207]':'bank[208]','len(native)==15 and len(commands)==24 and len(speeches)==13':'len(native)==29 and len(commands)==38 and len(speeches)==24',"sum(c['word']==0xA000 for c in commands)==5":"sum(c['word']==0xA000 for c in commands)==6",'source_block=207':'source_block=208','all24_stored_fixture_commands':'all38_stored_fixture_commands','all15_source_commands_plus9_initializers':'all29_source_commands_plus9_initializers','not_natural_event207_activation':'not_natural_event208_activation',
        'Minotaur-axe-request/conditional-search/undecided-gift/return':'pirate-sword/resemblance/hearsay/private-thought/named-FE-attribute-notice/return',
        '15 source+9 initializer commands,13 progressive objects,no FE/macros/choices/branches':'29 source+9 initializer commands,23 progressive/one FE objects,private thought,no macros/choices/branches',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_English_fixture.json',dict(tool=r,source_commands=29,source_panels=24,progressive=23,FE=1,complete_fixture_commands=38,source_inputs_and16001_frame_scope_preserved=True,no_forced_state_result_eligibility_or_full_effect_claim=True,new_review_credit=0,full_goal_complete=False));print('B208 complete revised-English fixture/runner prepared against retained source;all38 commands and original16001-frame ordinary inputs.')
