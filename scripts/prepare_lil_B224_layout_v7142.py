"""Plan unchanged English prose and preserve the source/current silence glyph exactly."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B224_layout_tools_v7142')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/plan_lil_B222_layout_v7046b.py';b='scripts/plan_lil_B224_layout_v7142.py';s=Path(a).read_text('utf8')
    old=next(line for line in s.splitlines() if line.startswith('PAIRS='))
    new="PAIRS={('as','ever'),('get','lost'),('your','eyes'),('turning','to'),('to','stone'),('medusa','shield'),('tasman','sea'),('on','my'),('my','mind'),('beautiful','eyes'),('eyes','alone'),('take','care'),('care','of'),('live','near'),('near','you'),('bathed','in'),('in','moonlight'),('how','romantic'),('heart','flutter'),('a','little'),('time','to'),('to','go'),('see','you')}"
    c={'B222':'B224','editorial_manuscript_v2.json':'editorial_manuscript_v1.json','layout_v7046b':'layout_v7142','[2,16]':'[26,197]',
      'all(32<=ord(c)<127 for c in body)':"all(32<=ord(c)<127 or c=='…' and row['id']=='DK4_MES_B224_R0011' for c in body)",
      "def display(text):return text.replace('{MACRO:FA}','Argot')":"def display(text):return text.replace('{MACRO:FA}','Argot').replace('…','XX')",
      old:new,'sixteen_whole_paragraph_plans_no_macros_no_prose_changes':'fifteen_whole_paragraph_plans_no_macros_no_prose_changes','all16_formatting_gates_remain_false':'all15_formatting_gates_remain_false'}
    assert not Path(b).exists();checked_text(s,c);row=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_paragraph_planner.json',dict(tool=row,only_source_current_R11_ellipsis_CP932_punctuation_eligible=True,ellipsis_uses_original_two_ASCII_cell_width_not_a_new_font_metric=True,all_other_prose_ASCII_and_original_guard_pair_phase_geometry_unchanged=True,no_manual_breaks_or_prose_cut=True,new_credit=0,full_goal_complete=False))
