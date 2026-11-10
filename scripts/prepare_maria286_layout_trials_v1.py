"""Byte-bind scoped phrase trials and test ten two-page plans without changing prose."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B37_B50_clean_20261109')
PAIRS={
 (37,18):(['north sea'],'Keep the established two-word region name together.'),
 (38,29):(['trouble you'],'Keep the conditional trouble-you phrase together where it fits.'),
 (39,48):(['give me money'],'Keep Nagarpur’s repeated short plea intact.'),
 (40,22):(['serves as'],'Keep the trading-port predicate’s phrasal connection together.'),
 (42,11):(['just as'],'Keep the short comparison qualifier together.'),
 (42,30):(['all well and good'],'Keep Richard’s familiar idiom together instead of isolating all.'),
 (43,18):(['taken the first step'],'Keep Maria’s first-step image together and test a more compact arrangement of the same words.'),
 (45,4):(['zheng he'],'Keep the source-bound personal name together.'),
 (45,21):(['what brutal treatment'],'Avoid stranding What from the short appalled exclamation.'),
 (45,36):(['however i please'],'Keep Grau’s arbitrary-use claim together as a phrase.'),
 (45,63):(['get rid of'],'Keep the pest-removal idiom together.'),
 (45,67):(['want to die'],'Keep the short threatening question together.'),
 (46,42):(["i'll withdraw"],'Keep Clifford’s personal withdrawal predicate together.'),
 (46,45):(['pull out'],'Keep the withdrawal phrasal verb together.'),
 (47,147):(['live up to'],'Keep Maria’s hopes-and-effort idiom together.'),
 (47,179):(['fight for them'],'Keep the purpose of fighting together in Xien’s reassurance.'),
 (47,185):(['wave back'],'Keep Ian’s short gesture request together.'),
 (47,211):(['all of a sudden'],'Keep Maria’s familiar suddenness idiom together.'),
}

def main():
    out=ROOT/'formatting_v1/preferences_v2_trials.json';findings=ROOT/'layout_trial_findings_v1.json'
    assert not out.exists() and not findings.exists()
    doc_path=ROOT/'formatting_v1/formatting_input.json';plan_path=ROOT/'format_plan_v1/automatic_plans.json'
    doc,plan=map(load,[doc_path,plan_path]);rows={(r['block'],r.get('source_record_index')):r for r in doc['records']}
    byid={r['id']:r for r in plan['records']};prefs=deepcopy(load(ROOT/'formatting_v1/initial_preferences.json'))
    notes=[]
    for key,(phrases,reason) in PAIRS.items():
        row=rows[key];old=byid[row['id']]
        assert old['expected_native_pages']==1
        rule=dict(required_pairs=[list(pair) for phrase in phrases for pair in zip(phrase.split(),phrase.split()[1:])],one_page=True,
            reason=reason,bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        prefs['records'][row['id']]=rule
        notes.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            finding=reason,initial_lines=old['lines'],trial_preference=rule,
            derived_from_directly_viewed_initial_B37_B47_pages=True))
    trials=[]
    for old in plan['records']:
        if old['expected_native_pages']==1:continue
        row=next(r for r in doc['records'] if r['id']==old['id'])
        assert row['id'] not in prefs['records']
        prefs['records'][row['id']]=dict(one_page=True,
            reason='Test whether the identical complete paragraph fits four validated physical rows before choosing a better two-page boundary.',
            bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        trials.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            initial_lines=old['lines'],candidate_not_approved_until_native_anddirect_visual_review=True))
    assert len(trials)==10 and len(notes)==18
    save(out,prefs)
    save(findings,dict(phrase_findings=notes,one_page_trials=trials,
        all_words_meanings_native_controls_andsubstitutions_unchanged=True,
        no_width_reduction_orviewport_font_changes=True,all_initial_B48_B50_pages_not_yet_directly_reviewed=True,
        one_page_trials_are_layout_proposals_not_font_orpagination_approval=True,
        new_credit=0,evidence={str(p):digest(p) for p in [doc_path,plan_path,Path(__file__)]}))
    print('Saved18 viewed phrase candidates andten same-prose one-page trials;no prose changes orapproval.')

if __name__=='__main__':main()
