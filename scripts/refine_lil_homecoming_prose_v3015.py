"""Preserve the first draft and failed phrase plan; refine two spoken paragraphs."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/lil_homecoming_ian_editorial_manuscript_v2.json')
DOC=Path('translations/lil_homecoming_ian_editorial_manuscript_v3.json')
ROOT=Path('work/analysis/lil_Homecoming_Ian_refine_v3015')
CHANGES={
 'DK4_MES_B70_R0476':('From you, that rings hollow...','Keep Yifa skeptical rings-hollow idiom and its pointed second-person target. Fronting From you is a natural dismissive reply to Julian sincerity advice and resolves the artificial isolated Coming or hollow wrap without authored breaks.'),
 'DK4_MES_B70_R0677':('Nothing in this world is absolutely right. You can only follow your own convictions. Do you understand, Marinus?','Express walking the path one believes in as following one own convictions, a natural moral instruction. Preserve the universal claim about rightness, the limitation can only and the direct Marinus address; do not substitute objective truth or add a new historical lesson.')}
if __name__=='__main__':
 assert not DOC.exists() and not ROOT.exists(); doc=deepcopy(read(OLD)); changes=[]
 for r in doc['records']:
  if r['id'] not in CHANGES: continue
  before=deepcopy(r); english,note=CHANGES[r['id']]
  r['english']='{SPEAKER:'+r['source_presentation_prefix_hex'].upper()+'}'+english
  r['localization_note']=note;r.pop('fresh_retained_wording_justification',None);r.pop('qa_waivers',None);r.pop('qa_waiver_reason',None)
  r['editorial_decision']='revise';changes.append(dict(id=r['id'],previous=before,successor=deepcopy(r)))
 assert len(changes)==2
 counts=Counter(r['editorial_decision'] for r in doc['records']);doc.update(revised=counts['revise'],retained=counts['retain-wording'],previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),formatting_review_pending=True)
 ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'two_source_faithful_paragraph_refinements.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,failed_layout_preserved='work/analysis/lil_Homecoming_Ian_layout_v3014/all172_layout_and_QA.json',no_credit=True,full_goal_complete=False))
 print(dict(revised=doc['revised'],retained=doc['retained'],source_meaning_and_source_controls_unchanged=True))
