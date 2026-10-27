"""Preserve all words; prevent a stranded auxiliary in Lil's neighboring-ship question."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    ROOT=Path('work/analysis/lil_B160_wrap_refinement_v3878');assert not ROOT.exists();old=Path('work/analysis/lil_B160_layout_v3876/all22_paragraph_layout_QA.json');v=read(old);assert len(v['failures'])==1 and v['failures'][0]['id']=='DK4_MES_B160_R0008'
    pairs=[derive('dk4tool/dialogue/lil_B160_layout_v1.py','dk4tool/dialogue/lil_B160_layout_v2.py',{'def _word(value):':'''PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({("you're","not")})

def _word(value):'''})]
    pairs.append(derive('scripts/plan_lil_B160_layout_v3876.py','scripts/plan_lil_B160_layout_v3879.py',{'lil_B160_layout_v1':'lil_B160_layout_v2','lil_B160_layout_v3876':'lil_B160_layout_v3879'}))
    pairs.append(derive('scripts/verify_lil_B160_fonts_v3877.py','scripts/verify_lil_B160_fonts_v3880.py',{'lil_B160_layout_v1':'lil_B160_layout_v2','lil_B160_fonts_v3877':'lil_B160_fonts_v3880'}))
    ROOT.mkdir(parents=True);save(ROOT/'failed_plan_and_automatic_phrase_refinement.json',dict(failed_plan=str(old),failed_plan_sha256=sha(old.read_bytes()),finding='A possible line ended with the auxiliary you are. Keep the auxiliary and negation together through automatic phrase protection.',all_words_unchanged=True,source_and_manuscript_unchanged=True,no_waiver=True,derived_tools=pairs,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
