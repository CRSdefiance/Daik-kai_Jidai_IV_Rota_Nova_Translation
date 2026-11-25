"""Prepare the complete translated scene using the unchanged source input schedule."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_English_fixture_tools_v7106')
if __name__=='__main__':
    assert not ROOT.exists()
    a='scripts/research_lil_B214_English_fixture_v6722.py';b='scripts/research_lil_B223_English_fixture_v7106.py'
    c={
      'B214':'B223','reference_v6718':'reference_v7102',
      'English_fixture_v6722':'English_fixture_v7106','English_v6722':'English_v7106',
      'source_fixture_v6702':'source_fixture_v7085','source_run_v6703':'source_run_v7086','source_v6703':'source_v7086',
      'English_run_v6723':'English_run_v7107','English_v6723':'English_v7107',
      'V6686':'V7067','bank[214]':'bank[223]','source_block=214':'source_block=223',
      'end==1302 and len(bank[214])==1304':'end==1384 and len(bank[223])==1384',
      'len(native)==27 and len(commands)==36':'len(native)==22 and len(commands)==31',
      "sum(c['word']==0x8000 for c in commands)==2":"sum(c['word']==0x8000 for c in commands)==1",
      'all36_stored_fixture_commands':'all31_stored_fixture_commands',
      'all27_source_commands_plus9_initializers':'all22_source_commands_plus9_initializers',
      'all_ten_speeches_original_native_four_row_single_pages_under_test':'all_ten_speeches_original_four_row_pages_two_continuations_under_test',
      'not_natural_event214':'not_natural_event223',
      '27source+9initializers,one automatic voice object,two predicates/eight relative paths,ten single-page speeches andcomplete Janus Pasar signature':'22source+9initializers,one automatic voice object,one predicate/four relative paths,ten speeches with two native continuations and complete Ian Dukov signature',
    }
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_fixture_tool.json',dict(tool=row,no_native_address_or_input_schedule_change=True,new_credit=0,full_goal_complete=False))
