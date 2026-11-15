"""Keep the final price instruction and the seller's rebuke from splitting awkwardly."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest
from scripts.refine_rafael_B201_B220_wraps_v2 import OUT as MANUSCRIPT, PREFS as PRIOR


PREFS = ROOT/'ordinary_visual_preferences_v4.json'
BEFORE = ROOT/'ordinary_plans_v3/automatic_plans.json'
AFTER = ROOT/'ordinary_plans_v4/automatic_plans.json'
DELTA_DOC = ROOT/'ordinary_delta_manuscript_v2.json'
DELTA_PLAN = ROOT/'ordinary_delta_plan_v2.json'
RULES = {
    'DK4_MES_B208_R0077': dict(one_page=True,line_phrases=['get him to lower it twice more.)'],
        reason='Keep the complete bargain advice on one page and both further reductions in the same phrase.'),
    'DK4_MES_B218_R0119': dict(line_phrases=["If you still don't get it",'after all that,'],
        reason='Keep the condition of the seller’s rebuke intact before he turns the buyer away.'),
}


def prepare():
    assert not PREFS.exists()
    prefs=load(PRIOR)
    for ident,change in RULES.items():
        prefs['records'][ident].update(change)
    prefs['prior_plan_diagnostics_sha256']=digest(BEFORE.with_name('diagnostics.json'))
    save(PREFS,prefs)


def isolate():
    assert not DELTA_DOC.exists() and not DELTA_PLAN.exists()
    doc,before,after=map(load,(MANUSCRIPT,BEFORE,AFTER))
    assert not after['failures'] and after['manuscript_sha256']==digest(MANUSCRIPT)
    assert all(issue['severity']=='info' for row in after['records'] for issue in row['base_QA']['issues'])
    changes=[]
    for old,row in zip(before['records'],after['records'],strict=True):
        assert old['id']==row['id'] and old['logical_English']==row['logical_English']
        if old['encoded_hex']!=row['encoded_hex']:
            assert row['id'] in RULES
            changes.append(row)
            print(row['id'],row['lines'])
    ids={r['id'] for r in changes}
    assert ids==set(RULES)
    save(DELTA_DOC,{**doc,'records':[r for r in doc['records'] if r['id'] in ids],
        'physical_speech_objects':len(ids),'ordinary_speech_objects':len(ids),
        'typed_choice_objects':0,'typed_choice_commands':0})
    save(DELTA_PLAN,{**after,'records':changes,'manuscript':str(DELTA_DOC),
        'manuscript_sha256':digest(DELTA_DOC),'complete_plan_sha256':digest(AFTER)})


if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--prepare']:
        prepare()
    else:
        isolate()

