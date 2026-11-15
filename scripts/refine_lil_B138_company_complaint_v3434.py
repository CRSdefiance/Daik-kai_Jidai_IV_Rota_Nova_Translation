"""Resolve a weak wrap without dropping the failure report or ongoing trouble."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_company_complaint_v3434');old=Path('translations/lil_B138_editorial_manuscript_v1.json');new=Path('translations/lil_B138_editorial_manuscript_v3.json');assert not root.exists() and not new.exists()
    proof=Path('work/analysis/lil_B138_layout_v3433b/all44_paragraph_layout_QA.json');failed=read(proof);assert len(failed['failures'])==1 and failed['failures'][0]['id']=='DK4_MES_B138_R0040'
    doc=deepcopy(read(old));r=next(r for r in doc['records'] if r['id']=='DK4_MES_B138_R0040');before=r['english'];r['english']="{SPEAKER:5C}Nagarpur Co. went under... Nothing but trouble ever since!"
    r['localization_note']+=' The first automatic layout ended a row on it\'s. This faithful spoken successor preserves the company failure and continuing troubles, with no manual break or warning exemption.'
    r['prose_refinement_producer']=str(Path(__file__));r['prose_refinement_producer_sha256']=sha(Path(__file__).read_bytes())
    doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()));save(new,doc);root.mkdir(parents=True)
    a=Path('scripts/plan_lil_B138_layout_v3433b.py');b=Path('scripts/plan_lil_B138_layout_v3434b.py');assert not b.exists();t=a.read_text(encoding='utf-8').replace('lil_B138_layout_v3433b','lil_B138_layout_v3434b').replace('lil_B138_editorial_manuscript_v1','lil_B138_editorial_manuscript_v3').replace('lil_B138_editorial_manuscript_v2','lil_B138_editorial_manuscript_v4');compile(t,str(b),'exec');b.write_text(t,encoding='utf-8')
    save(root/'finding_and_successors.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),failure_proof=str(proof),failure_proof_sha256=sha(proof.read_bytes()),id=r['id'],source_Japanese=r['source_Japanese'],before=before,after=r['english'],meaning_and_ongoing_trouble_preserved=True,no_manual_break_or_warning_waiver=True,successor_planner=str(b),successor_planner_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
