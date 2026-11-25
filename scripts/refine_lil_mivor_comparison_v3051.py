"""Retain all executed drafts/plans;resolve the invitation and fear-comparison flow."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/lil_christina_mivor_editorial_manuscript_v3.json')
DOC=Path('translations/lil_christina_mivor_editorial_manuscript_v4.json')
ROOT=Path('work/analysis/lil_Christina_Mivor_refine_v3051')
CHANGES={
'DK4_MES_B72_R0119':("Oh, yes, yes. Would you like to come along with me?",'Keep Julio kindly invitation andrecollective yes repetition as a natural direct question. His intent to invite her remains explicit;no new demand orcompleted recruitment.'),
'DK4_MES_B73_R0139':("I love Christina, but... The sea scares me! Scares me! Scares me even more!",'Preserve the three fearful beats andthe first greater-than comparison:fear still outweighs love. Natural comic clause order avoids a stranded name while keeping the later opposite comparison distinct;no early bravery orpermanent fear cure.')}
if __name__=='__main__':
 assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));changes=[]
 for r in doc['records']:
  if r['id'] not in CHANGES:continue
  before=deepcopy(r);text,note=CHANGES[r['id']];r['english']='{SPEAKER:'+r['source_presentation_prefix_hex'].upper()+'}'+text;r['localization_note']=note
  r.pop('qa_waivers',None);r.pop('qa_waiver_reason',None);assert r['editorial_decision']=='revise';changes.append(dict(id=r['id'],previous=before,successor=deepcopy(r)))
 assert len(changes)==2;ROOT.mkdir(parents=True);doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()));save(DOC,doc)
 save(ROOT/'invitation_and_fear_comparison_flow_refinements.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,failed_plan_preserved='work/analysis/lil_Christina_Mivor_layout_v3049/all145_layout_and_QA.json',no_credit=True,full_goal_complete=False))
 print('Two source-faithful successor paragraphs;all previous drafts/plans preserved;zero credit.')
