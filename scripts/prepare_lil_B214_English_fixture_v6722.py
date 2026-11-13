"""Prepare the whole reviewed English exchange with exactly the source fixture's ordinary inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_English_fixture_tools_v6722')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('scripts/research_lil_B209_English_fixture_v6469.py','scripts/research_lil_B214_English_fixture_v6722.py',{
        'B209':'B214','reference_v6468':'reference_v6718','create_lil_B209_reference_v6468':'create_lil_B214_reference_v6718','English_fixture_v6469':'English_fixture_v6722','English_v6469':'English_v6722','source_fixture_v6453':'source_fixture_v6702','source_event209':'source_event214','source_block=209':'source_block=214','bank[209]':'bank[214]',
        'end==1334 and len(bank[209])==1336':'end==1302 and len(bank[214])==1304',
        'len(native)==18 and len(commands)==27 and len(speeches)==5':'len(native)==27 and len(commands)==36 and len(speeches)==10',
        "sum(c['word']==0x4100 for c in commands)==2 and sum(c['word']==0x8000 for c in commands)==1":"sum(c['word']==0x4100 for c in commands)==1 and sum(c['word']==0x8000 for c in commands)==2",
        'all27_stored_fixture_commands':'all36_stored_fixture_commands','all18_source_commands_plus9':'all27_source_commands_plus9',
        'both_long_letter_paragraphs_original_native_four_row_continuation_under_test':'all_ten_speeches_original_native_four_row_single_pages_under_test',
        'V6439':'V6686','source_v6454':'source_v6703','source_run_v6454':'source_run_v6703','English_run_v6470':'English_run_v6723','English_v6470':'English_v6723','run_lil_B209_source_v6454':'run_lil_B214_source_v6703','run_lil_B209_English_v6470':'run_lil_B214_English_v6723',
        '18source+9initializers,2automatic voice objects,original predicate/relative paths,two long letter continuations':'27source+9initializers,one automatic voice object,two predicates/eight relative paths,ten single-page speeches andcomplete Janus Pasar signature'
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_complete_English_fixture.json',dict(derivation=proof,all27_source_commands_plus9_initializers_preserved=True,all_ten_speeches_seven_bodies_eight_aliased_slots=True,same_source_ordinary_inputs_no_role_result_RNG_or_state_forcing=True,new_credit=0,full_goal_complete=False))
