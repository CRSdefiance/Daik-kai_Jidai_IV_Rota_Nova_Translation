"""Propose source-bound phrase/page preferences after viewing every initial native page."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B0_B32_clean_20261109')
PAIRS={
    (0,39):(['really is'],'Keep the tentative predicate really is together.'),
    (0,48):(['truly is'],'Keep the parallel tentative predicate truly is together.'),
    (1,5):(['cursed blade'],'Keep the source weapon descriptor together; an ellipsis already supplies the hesitant introduction.'),
    (3,26):(['stiff and proper'],'Keep the mocked personality description together.'),
    (4,45):(['all ships'],'Keep the complete naval address All ships together.'),
    (5,49):(['prepare for battle'],'Keep the battle-preparation command together.'),
    (6,51):(['back again'],'Keep the recurring-rival idiom together.'),
    (9,16):(['come on'],'Avoid stranding the particle of the direct challenge.'),
    (10,12):(['sink you'],'Keep each repeated sinking threat intact.'),
    (12,5):(['after me'],'Avoid beginning the final row with the isolated question tail me.'),
    (12,16):(['truly saved'],'Keep the sincere gratitude predicate together.'),
    (13,35):(['other people'],'Keep the human noun phrase together if the existing one-page limit remains good.'),
    (14,5):(['admiral {macro:fa}'],'Keep the supported title and short default surname together.'),
    (19,5):(['next time'],'Keep the next-time challenge together.'),
    (19,40):(['going to'],'Keep the impending responsibility threat’s auxiliary phrase together.'),
    (19,85):(['stay out of it'],'Keep the outsider-interference idiom together.'),
    (19,169):(['how low','why did'],'Keep the two personal questions from starting at the end of a row.'),
    (19,202):(['like my father'],'Keep the central comparison with her father together.'),
    (19,213):(['like him'],'Keep the personal comparison’s referent with its preposition.'),
    (19,217):(['more than'],'Keep the comparative realization together.'),
    (20,17):(['next time'],'Keep the next-time threat together.'),
    (21,14):(['look down on'],'Keep the personal contempt idiom together.'),
    (21,26):(['next time'],'Keep the future rematch phrase together.'),
    (21,39):(['just because'],'Keep the causal qualifier together.'),
    (21,42):(['next time'],'Keep the death threat’s next-meeting phrase together.'),
    (28,5):(['soaring scarlet orca'],'Keep the complete source-qualified epithet together where it fits.'),
    (29,111):(['just because'],'Keep the refusal’s causal qualifier together.'),
    (29,134):(['supposed to'],'Keep the question’s predicate together instead of a tiny to-mean ending.'),
    (31,38):(['what are you'],'Keep Lil’s short surprised question from starting with a stranded What.'),
    (31,42):(['lil is in danger'],'Keep the short quoted warning together.'),
}
PAGES={
    (4,9):("To think I'd be facing a woman like you instead of Valdes.",'Keep the full incredulous contrast on one page rather than an isolated of-Valdes continuation.'),
    (8,5):("Get too full of yourself, and you'll regret it.",'Keep the complete warning on a page rather than stranding regret it.'),
    (18,36):("as though recalling the beat of a mother's heart, now far away.",'Keep the poem’s remembered-heartbeat image together rather than stranding far away.'),
    (24,11):('Feel free to keep talking back all the way to Havana.','Keep the complete taunting permission together rather than a to-Havana continuation.'),
    (30,20):("And you performed even better than I'd expected.",'Keep Clifford’s complete closing assessment together rather than a detached than-I-expected tail.'),
}


def main():
    out=ROOT/'formatting_v1/preferences_v3_candidates.json'
    findings_path=ROOT/'initial_visual_findings_v1.json'
    assert not out.exists() and not findings_path.exists()
    native_path=ROOT/'initial_native_v1/compiled_native_pages.json'
    native=load(native_path)
    assert len(native['records'])==299 and native['pages']==304 and native['fresh_compiled_alignments']==1196
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact']
    doc_path=ROOT/'formatting_v1/formatting_input.json';doc=load(doc_path)
    rows={(r['block'],r['source_record_index']):r for r in doc['records']}
    plans_path=ROOT/'initial_plans_v2/automatic_plans.json';plans=load(plans_path)
    old={r['id']:r for r in plans['records']}
    preferences=deepcopy(load(ROOT/'formatting_v1/preferences_v2.json'))
    findings=[]
    for key in sorted(PAIRS.keys()|PAGES.keys()|{(19,126)}):
        row=rows[key];rule={}
        if key in PAIRS:
            phrases,reason=PAIRS[key]
            rule.update(required_pairs=[list(pair) for phrase in phrases for pair in zip(phrase.split(),phrase.split()[1:])])
        elif key in PAGES:
            phrase,reason=PAGES[key];assert row['english'].count(phrase)==1
            rule['page_clause']=phrase
        else:
            reason='Her is the object of lay a hand on, not a possessive determiner; a comma before and permits a complete-clause boundary and may remove an unnecessary row.'
            rule['ordinary_boundaries']=[['her','and']]
        if old[row['id']]['expected_native_pages']==1:rule['one_page']=True
        rule.update(bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']},reason=reason)
        preferences['records'][row['id']]=rule
        findings.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            finding=reason,current_native_lines=old[row['id']]['lines'],candidate_preference=rule,
            proposal_not_approved_until_fresh_native_visual_comparison=True))
    save(out,preferences)
    save(findings_path,dict(records=findings,candidates=len(findings),
        prior_orphan_contrast_fix='DK4_MES_B5_R0035',
        all304_initial_native_pages_directly_viewed=True,
        directly_viewed_initial_sheets=native['review_sheets'],
        all44_distinct_name_strings_directly_viewed=True,menu_current_andreviewed_previews_directly_viewed=True,
        initial_font_andmenu_receipts=[str(ROOT/'name_planes_v1/native_name_planes.json'),str(ROOT/'menu_planes_v1/menu_provider_and_planes.json')],
        no_prose_orstored_bytes_changed=True,all_final_formatting_gates_still_pending=True,
        new_credit=0,evidence={str(p):digest(p) for p in [native_path,doc_path,plans_path,Path(__file__)]}))
    print('Saved',len(findings),'visual layout candidates plus the earlier orphan contrast fix;all304 initial pages viewed;no prose changes.')


if __name__=='__main__':main()
