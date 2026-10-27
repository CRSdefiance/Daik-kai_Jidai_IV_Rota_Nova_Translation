"""Successor draft for two concrete native layout failures; preserve first draft."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('translations/lil_recruits_julian_editorial_manuscript_v1.json')
DOC=Path('translations/lil_recruits_julian_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/lil_Recruits_Julian_refine_v3086')
FAILURE=Path('work/analysis/lil_Recruits_Julian_layout_v3085/all197_layout_and_QA.json')
REVISIONS={
'DK4_MES_B76_R0218':("Hmm. It turned out so well, I displayed it for three years. A mistake, perhaps... Lesson learned! Use gunpowder promptly!",'Tighten the overlong explanation while preserving his excellent result, three years on display, uncertain diagnosis and explicit gunpowder lesson. No new damage or certainty is added.'),
'DK4_MES_B79_R0020':("On his travels, he met a black-haired girl with a delicate air. No one knew who she was at the time.",'Tighten the identity account while retaining the journey, black hair, delicate air and identity unknown at that time; no illness, amnesia or rescue is invented.')}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));failure=read(FAILURE)
    assert {r['id'] for r in failure['failures']}==set(REVISIONS)
    changes=[]
    for row in doc['records']:
        if row['id'] not in REVISIONS:continue
        prose,note=REVISIONS[row['id']];old=row['english'];row['english']=old.split('}',1)[0]+'}'+prose
        row['localization_note']+=' '+note
        assert row['editorial_decision']=='revise' and all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
        changes.append(dict(id=row['id'],previous=old,english=row['english'],source_Japanese=row['source_Japanese'],source_meaning=row['source_meaning'],reason=note))
    assert len(changes)==2
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),layout_failure=str(FAILURE),layout_failure_sha256=sha(FAILURE.read_bytes()))
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'two_source_faithful_layout_refinements.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,previous_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),native_formatting_and_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('Two source-faithful successor paragraphs; first draft and failed layout preserved.')
