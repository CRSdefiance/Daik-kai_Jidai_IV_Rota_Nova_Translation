"""Preserve failed2824 plan; refine one sentence without a manual break."""
from pathlib import Path
from copy import deepcopy
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
OLD=Path('translations/lil_goods_mediterranean_editorial_manuscript_v1.json')
DOC=Path('translations/lil_goods_mediterranean_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/lil_Goods_Mediterranean_refinement_v2825')
if __name__=='__main__':
    assert not DOC.exists() and not ROOT.exists();doc=deepcopy(read(OLD));rows={r['id']:r for r in doc['records']};r=rows['DK4_MES_B41_R0005'];before=r['english']
    assert before=="{SPEAKER:02}Oh! It looks like the governor's office is finished!"
    r['english']="{SPEAKER:02}Oh! Looks like the governor's office is finished!"
    note='The2824 automatic plan splits governor-office because the longer clause cannot fit between acceptable boundaries. Conversational subject omission preserves surprise, apparent completion and full building identity, permitting automatic wrapping without manual layout or any boundary waiver.'
    r['localization_note']+=' '+note
    changes=[dict(id=r['id'],before=before,after=r['english'],reason=note)]
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),phrase_flow_refinements=changes)
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'prose_refinement_receipt.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,credit_added=0,full_goal_complete=False));print('One source-faithful conversational refinement; original draft and failed plan preserved.')
