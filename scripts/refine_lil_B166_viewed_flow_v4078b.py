"""Keep the full care object together without forcing a37-cell clause into36 cells."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B166_viewed_flow_v4078b')
if __name__=='__main__':
    assert not ROOT.exists();failed=Path('work/analysis/lil_B166_layout_v4078/all42_paragraph_layout_QA.json');d=read(failed);assert [r['id'] for r in d['failures']]==['DK4_MES_B166_R0123'];tools=[]
    tools.append(derive('dk4tool/dialogue/lil_B166_layout_v2.py','dk4tool/dialogue/lil_B166_layout_v3.py',{"('take','good'),":""}))
    tools.append(derive('scripts/plan_lil_B166_layout_v4078.py','scripts/plan_lil_B166_layout_v4078b.py',{'lil_B166_layout_v2':'lil_B166_layout_v3','lil_B166_layout_v4078':'lil_B166_layout_v4078b'}))
    ROOT.mkdir(parents=True);save(ROOT/'preserved_failed_plan_and_feasible_care_phrase_core.json',dict(failed_plan=str(failed),failed_plan_sha256=sha(failed.read_bytes()),tools=tools,source_words_meanings_controls_and_decisions_unchanged=True,care_phrase_core='good care of her',reason='The complete question Then would you take good care of her? is37 visible cells. Keeping every link forces every earlier legal cut onto aweak auxiliary/pronoun orone protected phrase. Keep good care of her intact andpermit the transitive verb take onthe preceding row;no weak-ending,orphan,glyph,bounds,pagination ormacro waiver.',no_authored_layout_or_global_guard_change=True,no_credit_or_ROM_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Preserved failed full-chain plan;scoped successor protects the complete care object without aQA waiver.')
