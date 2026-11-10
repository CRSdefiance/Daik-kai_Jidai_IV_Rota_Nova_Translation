"""Measure exported later state without assuming equal captains or forcing simulation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_later_tools_v7158')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/measure_lil_B222_later_v7061b.py';b='scripts/measure_lil_B224_later_v7158.py'
    c={'B222':'B224','later_v7061b':'later_v7158','English_actual_v7060b/all16_English_speeches_complete_native_masks27_commands_source_comparison':'English_actual_v7157/all15_English_speeches_complete_native_masks27_commands_C200_source_comparison',
      'root=get(0xCB184);assert get(0x7F244)==2;':'root=get(0xCB184);captain=get(0x7F244);assert captain in range(4);',
      'captain_ID=2,seed=':'captain_ID=captain,seed=',
      "if r['block']==120 and r['word']==0":"if r['route']==2 and r['block']==120 and r['word']==0",
      "whole_actor_and_captain_equal=values[0]['whole_actor_sha256']==values[1]['whole_actor_sha256']":"captain_IDs=[v['captain_ID'] for v in values],whole_actor_and_captain_equal=values[0]['whole_actor_sha256']==values[1]['whole_actor_sha256'] and values[0]['captain_ID']==values[1]['captain_ID']",
    }
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_later_measurement.json',dict(tool=row,actual_captain_getters_captured_without_assuming_value2=True,only_actual_SC2_B120_ends_classified_as_that_followup=True,no_getter_native_address_RNG_RAM_roster_state_or_input_change=True,new_credit=0,full_goal_complete=False))
