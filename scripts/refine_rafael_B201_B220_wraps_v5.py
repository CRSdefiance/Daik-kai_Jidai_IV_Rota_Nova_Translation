"""Give two spoken questions natural single openings after visual review."""
import sys

from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B201_B220_v1 import ROOT, digest
from scripts.refine_rafael_B201_B220_wraps_v4 import MANUSCRIPT as PRIOR_DOC, PREFS as PRIOR_PREFS, PLAN as PRIOR_PLAN
from dk4tool.patch.grand_race_menu_release import sha


MANUSCRIPT=ROOT/'ordinary_formatting_manuscript_v3.json'
PREFS=ROOT/'ordinary_visual_preferences_v6.json'
PLAN=ROOT/'ordinary_plans_v6/automatic_plans.json'
DELTA_DOC=ROOT/'ordinary_delta_manuscript_v4.json'
DELTA_PLAN=ROOT/'ordinary_delta_plan_v4.json'
EDITS={
    'DK4_MES_B201_R0049': ("Well, well. Good customers, huh? I'm a little short on cash. Why don't we go talk to them?",
        "Why don't we go talk to them?", 'Keep the man’s opportunism and the invitation to approach the buyers.'),
    'DK4_MES_B220_R0036': ("Oh, you want to get stronger? How about looking for that pirate's treasured sword?",
        'Oh, you want to get stronger?', 'Keep the old man’s interest in her answer and the suggestion to seek the pirate’s sword.'),
}


def prepare():
    assert not MANUSCRIPT.exists() and not PREFS.exists()
    doc,prefs=map(load,(PRIOR_DOC,PRIOR_PREFS))
    rows={r['id']:r for r in doc['records']}
    for ident,(text,phrase,note) in EDITS.items():
        row=rows[ident]
        assert row['decision']=='revision' and not row['native_literal_tokens']
        row.update(visual_revision_previous_English=row['english'],english=text,editorial_logical_English=text,
            planned_English_markup=f"{{SPEAKER:{row['source_selector']:02X}}}"+text,finding=note,localization_note=note)
        prefs['records'][ident]=dict(line_phrases=[phrase],reason=note,
            bindings={k:sha(row[k].encode('utf-8')) for k in ('source_hex','current_hex','english')})
    doc.update(previous_manuscript=str(PRIOR_DOC),previous_manuscript_sha256=digest(PRIOR_DOC),
        source_bound_read_aloud_refinements=sorted([*doc['source_bound_read_aloud_refinements'],*EDITS]))
    prefs['prior_plan_diagnostics_sha256']=digest(PRIOR_PLAN.with_name('diagnostics.json'))
    save(MANUSCRIPT,doc)
    save(PREFS,prefs)


def isolate():
    assert not DELTA_DOC.exists() and not DELTA_PLAN.exists()
    doc,before,after=map(load,(MANUSCRIPT,PRIOR_PLAN,PLAN))
    assert not after['failures'] and after['manuscript_sha256']==digest(MANUSCRIPT)
    assert all(issue['severity']=='info' for row in after['records'] for issue in row['base_QA']['issues'])
    changes=[]
    for old,row in zip(before['records'],after['records'],strict=True):
        assert old['id']==row['id']
        if old['encoded_hex']!=row['encoded_hex']:
            assert row['id'] in EDITS and old['expected_native_pages']==row['expected_native_pages']==1
            changes.append(row)
            print(row['id'],row['lines'])
        else:
            assert old['logical_English']==row['logical_English'] and old['lines']==row['lines']
    assert {row['id'] for row in changes}==set(EDITS)
    save(DELTA_DOC,{**doc,'records':[r for r in doc['records'] if r['id'] in EDITS],
        'physical_speech_objects':2,'ordinary_speech_objects':2,'typed_choice_objects':0,'typed_choice_commands':0})
    save(DELTA_PLAN,{**after,'records':changes,'manuscript':str(DELTA_DOC),
        'manuscript_sha256':digest(DELTA_DOC),'complete_plan_sha256':digest(PLAN)})


if __name__=='__main__':
    (prepare if sys.argv[1:]==['--prepare'] else isolate)()

