"""Resolve two native layout findings without losing source meaning or tone."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/lil_christina_mivor_editorial_manuscript_v1.json')
DOC=Path('translations/lil_christina_mivor_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/lil_Christina_Mivor_refine_v3044')
CHANGES={
 'DK4_MES_B72_R0018':("Ugh, enough! Listen, our parents arranged this engagement without asking me! I don\'t want to get married at all!",'Keep her exasperation,unwanted parental engagement andunqualified refusal in a natural paragraph. Enough conveys the preceding exhausted complaint without redundant exposition;no source fact or refusal is removed.'),
 'DK4_MES_B72_R0204':("You couldn\'t even beat a child with a stance like that.",'Keep her exact swordsmanship criticism and child comparison. Natural clause order avoids isolating a child as anorphan row;no new opponent or outcome is added.')}
if __name__=='__main__':
 assert not DOC.exists() and not ROOT.exists();doc=deepcopy(read(OLD));changes=[]
 for r in doc['records']:
  if r['id'] not in CHANGES:continue
  before=deepcopy(r);english,note=CHANGES[r['id']];r['english']='{SPEAKER:'+r['source_presentation_prefix_hex'].upper()+'}'+english;r['localization_note']=note;assert r['editorial_decision']=='revise'
  changes.append(dict(id=r['id'],previous=before,successor=deepcopy(r)))
 assert len(changes)==2;ROOT.mkdir(parents=True);doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()));save(DOC,doc)
 save(ROOT/'two_source_faithful_paragraph_refinements.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,failed_plan_preserved='work/analysis/lil_Christina_Mivor_layout_v3043/all145_layout_and_QA.json',no_credit=True,full_goal_complete=False))
 print('Two complete source-faithful refinements;previous draft andfailed plan preserved;zero credit.')
