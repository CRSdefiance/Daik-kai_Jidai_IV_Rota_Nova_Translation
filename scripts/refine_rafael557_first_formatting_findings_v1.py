"""Resolve one macro-order rejection and one source-bound weak wrap without cutting prose."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

PROSE=Path('translations/rafael_B141_B160_contextual_review_v2.json')
DOC=Path('translations/rafael_B141_B160_formatting_manuscript_v2.json')
PLAN=Path('work/analysis/Rafael557_automatic_plans_v1_20261105/automatic_plans.json')
PREF=Path('translations/rafael_B141_B160_visual_preferences_v1.json')

if __name__=='__main__':
    p,d,plan,pref=map(load,[PROSE,DOC,PLAN,PREF])
    assert plan['manuscript_sha256']==sha(DOC.read_bytes())
    assert plan['failures']==[dict(id='DK4_MES_B143_R0005',error_type='DialogueEncodingError',error='control-order: runtime macros or controls changed order')]
    pnew,dnew,prefnew=deepcopy(p),deepcopy(d),deepcopy(pref)
    ident='DK4_MES_B143_R0005'
    english="You're with FO, Admiral FA, I take it. Admiral Albuquerque is expecting you. Please go inside."
    note='Keep the guard\'s respectful identity check and source-supported admiral title. Natural company-first address also preserves the source FO-before-FA runtime-token order; the previous proposed wording was rejected before ROM writing.'
    for doc in [pnew,dnew]:
        row=next(r for r in doc['records'] if r['id']==ident)
        assert row['decision']=='revision' and row['review']['formatting'] is False
        row['previous_rejected_macro_order_English']=row['english']
        row['english']=english if doc is pnew else english.replace('FO','{MACRO:FO}').replace('FA','{MACRO:FA}')
        row['finding']=row['localization_note']=note
        if doc is dnew:
            row['editorial_logical_English']=english
            row['planned_English_markup']='{SPEAKER:78}'+row['english']
            assert row['source_selector']==120
    target=next(r for r in dnew['records'] if r['id']=='DK4_MES_B151_R0293')
    oldplan=next(r for r in plan['records'] if r['id']==target['id'])
    assert oldplan['lines'][1].endswith('the')
    prefnew['records'][target['id']]=dict(bindings={k:sha(target[k].encode('utf-8')) for k in ['source_hex','current_hex','english']},
        line_phrases=["isn't the governor"],reason='Keep the determiner with its noun and the short negated governor phrase intact; preserve every word and the available native width.')
    paths=[Path('translations/rafael_B141_B160_contextual_review_v3.json'),
        Path('translations/rafael_B141_B160_formatting_manuscript_v3.json'),
        Path('translations/rafael_B141_B160_visual_preferences_v2.json')]
    assert all(not f.exists() for f in paths)
    for out,doc,parent in zip(paths,[pnew,dnew,prefnew],[PROSE,DOC,PREF],strict=True):
        doc.update(previous_manuscript=str(parent),previous_manuscript_sha256=sha(parent.read_bytes()),
            first_formatting_findings=str(PLAN),first_formatting_findings_sha256=sha(PLAN.read_bytes()),
            no_formatting_gate_credit_orROM_changes=True)
        save(out,doc)
    print('Preserved rejected plan;correctedFO-before-FA intro andboundone negated-phrase wrap preference.No shortened prose orROM/gate changes.')
