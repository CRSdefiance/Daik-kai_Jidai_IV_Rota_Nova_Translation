"""Keep Julio thoughtful invitation complete;preserve all earlier drafts."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/lil_christina_mivor_editorial_manuscript_v4.json')
DOC=Path('translations/lil_christina_mivor_editorial_manuscript_v5.json')
ROOT=Path('work/analysis/lil_Christina_Mivor_refine_v3053')
if __name__=='__main__':
 assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));r=next(r for r in doc['records'] if r['id']=='DK4_MES_B72_R0119');before=deepcopy(r)
 r['english']="{SPEAKER:06}Oh, yes, yes. I thought you might like to join me."
 r['localization_note']='Preserve Julio recollection andhis thought ofinviting his granddaughter. The complete sentence is a natural,kindly invitation incontext;joining him means the voyage just proposed,with no order orcompleted recruitment.'
 r.pop('qa_waivers',None);r.pop('qa_waiver_reason',None)
 doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()));ROOT.mkdir(parents=True);save(DOC,doc)
 save(ROOT/'complete_Julio_invitation_refinement.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),previous=before,successor=r,failed_plan_preserved='work/analysis/lil_Christina_Mivor_layout_v3052/all145_layout_and_QA.json',no_credit=True,full_goal_complete=False))
