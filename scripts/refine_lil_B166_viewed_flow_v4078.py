"""Resolve nine viewed phrase boundaries through scoped automatic wrapping only."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B166_viewed_flow_v4078')
FINDINGS=Path('work/analysis/lil_B166_checkpoint_v4072/viewed_native_sheets_phrase_flow_and_unapproved_menu.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(FINDINGS);assert len(d['all_six_native_sheets_viewed'])==6 and len(d['nine_phrase_flow_findings'])==9
    for s in d['all_six_native_sheets_viewed']:assert s['viewed'] and sha(Path(s['path']).read_bytes())==s['sha256']
    tools=[];tools.append(derive('dk4tool/dialogue/lil_B166_layout_v1.py','dk4tool/dialogue/lil_B166_layout_v2.py',{'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('make','her'),('her','stronger'),('used','to'),('man','like'),('like','that'),('since','i'),('take','good'),('care','of'),('of','her'),('seem','to'),('ease','the'),('food','and'),('and','water'),('recover','faster'),('rests','on'),('give','refitting')})\n\ndef _word(value):"}))
    tools.append(derive('scripts/plan_lil_B166_layout_v4067.py','scripts/plan_lil_B166_layout_v4078.py',{'lil_B166_layout_v1':'lil_B166_layout_v2','lil_B166_layout_v4067':'lil_B166_layout_v4078','lil_B166_editorial_manuscript_v1':'lil_B166_editorial_manuscript_v2','lil_B166_editorial_manuscript_v2':'lil_B166_editorial_manuscript_v3'}))
    ROOT.mkdir(parents=True);save(ROOT/'nine_viewed_phrase_flow_refinements.json',dict(previous_viewed_findings=str(FINDINGS),previous_viewed_findings_sha256=sha(FINDINGS.read_bytes()),findings=d['nine_phrase_flow_findings'],viewed_sheets=d['all_six_native_sheets_viewed'],tools=tools,all42_reviewed_words_meanings_macros_selectors_and_decisions_unchanged=True,no_authored_layout_global_guard_change_or_wording_waiver=True,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Nine viewed phrase-flow refinements recorded;only scoped automatic phrase protection changes.')
