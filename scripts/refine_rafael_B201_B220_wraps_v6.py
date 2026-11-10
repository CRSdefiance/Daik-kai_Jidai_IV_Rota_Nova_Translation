"""Keep the two phrases in the old man's final suggestion intact."""
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest
from scripts.refine_rafael_B201_B220_wraps_v5 import MANUSCRIPT, PREFS as PRIOR, PLAN as BEFORE


PREFS=ROOT/'ordinary_visual_preferences_v7.json'
PLAN=ROOT/'ordinary_plans_v7/automatic_plans.json'
DELTA_DOC=ROOT/'ordinary_delta_manuscript_v5.json'
DELTA_PLAN=ROOT/'ordinary_delta_plan_v5.json'
ID='DK4_MES_B220_R0036'


def prepare():
    assert not PREFS.exists()
    preferences=load(PRIOR)
    rule=preferences['records'][ID]
    rule['line_phrases'].extend(['How about looking',"pirate's treasured sword?"])
    rule['reason']='Keep the opening question, proposal, and name of the object together.'
    save(PREFS,preferences)


def isolate():
    assert not DELTA_DOC.exists() and not DELTA_PLAN.exists()
    doc,before,after=map(load,(MANUSCRIPT,BEFORE,PLAN))
    assert not after['failures'] and after['manuscript_sha256']==digest(MANUSCRIPT)
    assert all(issue['severity']=='info' for row in after['records'] for issue in row['base_QA']['issues'])
    changes=[]
    for old,row in zip(before['records'],after['records'],strict=True):
        assert old['id']==row['id'] and old['logical_English']==row['logical_English']
        if old['encoded_hex']!=row['encoded_hex']:
            assert row['id']==ID and old['expected_native_pages']==row['expected_native_pages']==1
            changes.append(row)
            print(row['lines'])
    assert len(changes)==1
    save(DELTA_DOC,{**doc,'records':[r for r in doc['records'] if r['id']==ID],
        'physical_speech_objects':1,'ordinary_speech_objects':1,'typed_choice_objects':0,'typed_choice_commands':0})
    save(DELTA_PLAN,{**after,'records':changes,'manuscript':str(DELTA_DOC),
        'manuscript_sha256':digest(DELTA_DOC),'complete_plan_sha256':digest(PLAN)})


if __name__=='__main__':
    (prepare if sys.argv[1:]==['--prepare'] else isolate)()

