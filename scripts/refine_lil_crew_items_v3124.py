"""Successor prose for three concrete weak-boundary findings; preserve first draft."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('translations/lil_crew_items_editorial_manuscript_v1.json')
DOC=Path('translations/lil_crew_items_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/lil_Crew_Items_refine_v3124')
FAILURE=Path('work/analysis/lil_Crew_Items_layout_v3123/all198_layout_and_QA.json')
REVISIONS={
'DK4_MES_B82_R0075':("Yes. This was my lucky charm. I want someone like you to have it... I'm no longer physically able to sail.",'Reorder the charm explanation and personal offer into natural short sentences while retaining the same giver,kind of recipient,attachment and explicit physical inability. Resolve the concrete weak you boundary without manual spacing or a new cause of his condition.'),
'DK4_MES_B92_R0044':("I appreciate your faith in Christina, Admiral. But she's still my granddaughter. Please understand how an old man feels.",'Retain gratitude,admiral trust,the explicit granddaughter andrequest forunderstanding. Use a natural direct appeal in place of Try to understand an old mans feelings to resolve the concrete weak to boundary without losing the emotional perspective.'),
'DK4_MES_B95_R0013':("They say the admiral's telescope let him see incredibly far, even the moon's ridges and craters in clear detail.",'Combine the two report clauses naturally; the single They say qualifies both extraordinary range and clear lunar detail. Preserve admiral,telescope,range andsurfacefeatures while resolving the concrete weak article boundary without claiming historical certainty.')}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));failure=read(FAILURE)
    assert {r['id'] for r in failure['failures']}==set(REVISIONS)
    changes=[]
    for row in doc['records']:
        if row['id'] not in REVISIONS:continue
        prose,note=REVISIONS[row['id']];previous=row['english'];row['english']=previous.split('}',1)[0]+'}'+prose
        row['localization_note']+=' '+note
        assert row['editorial_decision']=='revise' and not row['review']['formatting']
        changes.append(dict(id=row['id'],previous=previous,english=row['english'],source_Japanese=row['source_Japanese'],source_meaning=row['source_meaning'],reason=note))
    assert len(changes)==3
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),layout_failure=str(FAILURE),layout_failure_sha256=sha(FAILURE.read_bytes()))
    ROOT.mkdir(parents=True);save(DOC,doc);save(ROOT/'three_source_faithful_weak_boundary_refinements.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),changes=changes,previous_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),native_formatting_and_release_pending=True,source_prose_or_completion_credit_added=0,full_goal_complete=False))
    print('Three source-faithful successor paragraphs;first draft/failed plan preserved. Native layout still requires verification.')
