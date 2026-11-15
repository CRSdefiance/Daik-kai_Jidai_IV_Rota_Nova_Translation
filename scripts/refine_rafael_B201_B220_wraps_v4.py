"""Bind the final phrase-continuity adjustments to the directly viewed pages."""
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest
from scripts.refine_rafael_B201_B220_wraps_v2 import OUT as MANUSCRIPT
from dk4tool.patch.grand_race_menu_release import sha


PREFS = ROOT/'ordinary_visual_preferences_v5.json'
BASE = ROOT/'ordinary_plans_v4/automatic_plans.json'
PLAN = ROOT/'ordinary_plans_v5/automatic_plans.json'
DELTA_DOC = ROOT/'ordinary_delta_manuscript_v3.json'
DELTA_PLAN = ROOT/'ordinary_delta_plan_v3.json'
RULES = {
    'B201_R0049': (["Why don't we"], 'Keep the invitation intact after the cash remark.'),
    'B203_R0064': (['sold out,'], 'Keep the phrasal verb together.'),
    'B204_R0023': (['try it.'], 'Keep the invitation to try tobacco intact.'),
    'B206_R0034': (["Let's get going."], 'Keep the decision to leave together.'),
    'B207_R0032': (["I'll bring it right out."], 'Keep the barkeep’s promise as a unit.'),
    'B208_R0043': (['come in handy,'], 'Keep the merchant’s stock phrase together.'),
    'B209_R0021': (['immortal sage.'], 'Keep the sage’s description together in the book pitch.'),
    'B210_R0010': (['Any naughty children here?'], 'Keep the repeated namahage question as two distinct beats.'),
    'B210_R0014': (['Any naughty children here?'], 'Use the same two beats in the repeated source call.'),
    'B211_R0063': (["Let's take a look."], 'Keep the suggestion together after locating the sound.'),
    'B214_R0061': (['A Dictionary of Glassmaking...'], 'Keep the complete book title on one line.'),
    'B216_R0071': (['One figurehead per ship,'], 'Keep Jam’s whole per-ship rule together.'),
    'B218_R0040': (['How about you, Cristina?'], 'Keep the complete question to Cristina on one line.'),
    'B220_R0036': (['get stronger, do you?'], 'Keep the short question tag attached to what the man heard.'),
}


def prepare():
    assert not PREFS.exists()
    prior=load(ROOT/'ordinary_visual_preferences_v4.json')
    rows={r['id'].removeprefix('DK4_MES_'):r for r in load(MANUSCRIPT)['records']}
    for key,(phrases,note) in RULES.items():
        row=rows[key]
        assert row['id'] not in prior['records'] and all(p in row['english'] for p in phrases)
        pref=dict(line_phrases=phrases,reason=note,
            bindings={k:sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
        if key in ('B210_R0010','B210_R0014'):
            pref['coherent_pairs']=[('any','naughty'),('naughty','children')]
        prior['records'][row['id']]=pref
    prior['prior_plan_diagnostics_sha256']=digest(BASE.with_name('diagnostics.json'))
    prior['visual_review_sheet_index_sha256']=digest(ROOT/'body_visual_final_v1/sheet_index.json')
    save(PREFS,prior)


def isolate():
    assert not DELTA_DOC.exists() and not DELTA_PLAN.exists()
    doc,before,after=map(load,(MANUSCRIPT,BASE,PLAN))
    assert not after['failures'] and after['manuscript_sha256']==digest(MANUSCRIPT)
    assert all(issue['severity']=='info' for row in after['records'] for issue in row['base_QA']['issues'])
    changes=[]
    for old,row in zip(before['records'],after['records'],strict=True):
        assert old['id']==row['id'] and old['logical_English']==row['logical_English']
        if old['encoded_hex']!=row['encoded_hex']:
            assert row['id'].removeprefix('DK4_MES_') in RULES
            assert old['expected_native_pages']==row['expected_native_pages']==1
            changes.append(row)
            print(row['id'],row['lines'])
    ids={r['id'] for r in changes}
    assert len(ids)==len(RULES)
    save(DELTA_DOC,{**doc,'records':[r for r in doc['records'] if r['id'] in ids],
        'physical_speech_objects':len(ids),'ordinary_speech_objects':len(ids),
        'typed_choice_objects':0,'typed_choice_commands':0})
    save(DELTA_PLAN,{**after,'records':changes,'manuscript':str(DELTA_DOC),
        'manuscript_sha256':digest(DELTA_DOC),'complete_plan_sha256':digest(PLAN)})


if __name__=='__main__':
    import sys
    if sys.argv[1:]==['--prepare']:
        prepare()
    else:
        isolate()

