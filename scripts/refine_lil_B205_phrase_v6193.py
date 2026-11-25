"""Keep got caught together without changing any English words or native limits."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_phrase_tools_v6193')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('dk4tool/dialogue/lil_B205_layout_v1.py','dk4tool/dialogue/lil_B205_layout_v2.py',{"('finally','got'),('got','it'),('save','face')":"('finally','got'),('got','it'),('got','caught'),('save','face')"})]
    tools.append(derive('scripts/plan_lil_B205_layout_v6191.py','scripts/plan_lil_B205_layout_v6194.py',{'layout_v6191':'layout_v6194','lil_B205_layout_v1':'lil_B205_layout_v2','manuscript_v2.json':'manuscript_v3.json','manuscript_v3.json':'manuscript_v4.json'}))
    tools.append(derive('scripts/verify_lil_B205_fonts_v6192.py','scripts/verify_lil_B205_fonts_v6195.py',{'fonts_v6192':'fonts_v6195','lil_B205_layout_v1':'lil_B205_layout_v2','manuscript_v3.json':'manuscript_v4.json'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_captured_bird_phrase_refinement.json',dict(tools=tools,reason='The viewed R67 native plane separated got/caught. Keep that verbal phrase intact while preserving every word,the sounds-like qualification and the complete defeat idiom. Native metrics,guard,pair phase,viewport and four-row limits stay exact. No manual break or weaker QA rule.',no_prose_or_ROM_or_ledger_credit_change=True,full_goal_complete=False))
