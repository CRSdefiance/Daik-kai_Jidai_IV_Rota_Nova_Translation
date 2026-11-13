"""Trial16 byte-bound readability findings after all318 initial pages were viewed."""
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

CLAUSES={
(51,31):('We Europeans linked them through our great voyages.','Keep the complete voyage boast on one page instead of stranding our great voyages.'),
(53,117):('bringing an end to war and holding the nation together...','Keep the whole stabilizing-purpose clause on a page instead of a detached the nation together.'),
(54,122):('bringing an end to war and holding the nation together...','Apply the same complete purpose-clause preference to the independently bound ending variant.'),
(53,127):("and peace would come to the world's seas.",'Keep the entire peace clause together instead of splitting its subject and predicate at A.'),
(54,132):("and peace would come to the world's seas.",'Keep the same peace clause intact in the second ending variant.'),
(57,17):('I have no intention of getting married!','Keep Cristina\'s complete refusal together instead of stranding of getting married on the second page.'),
(57,136):('What about traveling the world to train with your sword?','Keep the full travel-and-sword-training suggestion on a page instead of a lone with your sword question tail.'),
}
RULES={
(51,82):dict(one_page=True,ordinary_boundaries=[['blindly','in']],reason='Trial the unchanged131-character realization on one page,allowing the ordinary adverb/preposition boundary instead of a detached his life on it page.'),
(53,123):dict(ordinary_boundaries=[['have','the']],reason='Trial a normal complete-word verb/article boundary to avoid a separate to match row;retain all ability-and-character wording.'),
(54,128):dict(ordinary_boundaries=[['have','the']],reason='Trial the same normal complete-word boundary in the independently bound ending variant.'),
(54,515):dict(ordinary_boundaries=[['she','and']],reason='Trial a normal coordinated-subject boundary to reduce the four-row thought with a detached of history tail,without changing the narrator sentence.'),
(55,120):dict(required_pairs=[['come','with'],['with','me']],reason='Keep Angelo\'s short come with me invitation together without shortening the flowers promise.'),
(55,127):dict(required_pairs=[['worried','about']],reason='Keep the worried about predicate together in his reassurance about illness.'),
(56,26):dict(required_pairs=[['come','on']],reason='Keep Jam\'s short Come on invitation intact rather than splitting Come/on,Admiral.'),
(56,185):dict(required_pairs=[["what's",'your'],['your','name']],reason='Keep the short name question together while preserving the corrected ASCII I and both live name macros.'),
(57,129):dict(required_pairs=[['admiral','{macro:fi}'],['{macro:fi}','{macro:fa}']],reason='Keep Admiral plus the short default full name together in Julio\'s corrected normal-font introduction.'),
}

def main():
    out=ROOT/'formatting_v1/preferences_v5_visual_trials.json';findings=ROOT/'initial_visual_findings_v1.json'
    assert not out.exists() and not findings.exists()
    native_path=ROOT/'initial_complete_native_v1.json';native=load(native_path)
    assert len(native['records'])==310 and native['pages']==318 and not native['direct_visual_review_pending']
    path=ROOT/'formatting_v1/preferences_v4_FE_guards.json';pref=deepcopy(load(path))
    doc=load(ROOT/'formatting_v1/formatting_input.json');bykey={(r['block'],r['source_record_index']):r for r in doc['records']}
    plan_path=ROOT/'plan_v4_FE_guards/automatic_plans.json';plans={r['id']:r for r in load(plan_path)['records']}
    notes=[]
    for key in sorted(CLAUSES.keys()|RULES.keys()):
        row=bykey[key]
        if key in CLAUSES:
            clause,reason=CLAUSES[key];assert row['english'].count(clause)==1;rule=dict(page_clause=clause,reason=reason)
        else:rule=deepcopy(RULES[key])
        if plans[row['id']]['expected_native_pages']==1:rule['one_page']=True
        rule['bindings']={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']}
        pref['records'].setdefault(row['id'],{}).update(rule)
        notes.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            initial_lines=plans[row['id']]['lines'],finding=rule['reason'],candidate=rule))
    assert len(notes)==16
    pref.update(previous_preferences=str(path),previous_preferences_sha256=digest(path),all_initial318_pages_viewed_or_exact_visual_reuse=True)
    save(out,pref)
    save(findings,dict(records=notes,candidates=16,initial_native=str(native_path),initial_native_sha256=digest(native_path),
        all318_initial_pages_directly_viewed_or36_exact_duplicate_visual_reuses=True,
        five_FE_guard_corrections_already_native_verified=True,
        no_new_prose_orfont_viewport_engine_changes=True,all_final_formatting_gates_still_pending=True,new_credit=0))
    print('Prepared16 scoped wrap/page trials after318 viewed pages;all prose andnative controls unchanged.')
if __name__=='__main__':main()
