"""Keep twenty phrases together after direct complete-page review; no prose changes."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B176_B195_clean_20261110')
CHANGES={
(179,99):(['approached','us'],'Keep approached us together in Cristinas rebuttal.'),
(180,14):(["what's",'this','weapon','called'],'Keep the complete short weapon-name question together after the food joke.'),
(180,28):(["let's",'take','our','time'],'Keep take our time together in Marias patient-search response.'),
(181,85):(["i'd",'like','to','see','it'],'Keep Cristinas complete short closing wish together in the private sword thought.'),
(182,26):(['bane','of','tokugawa'],'Do not split bane from of Tokugawa across the letter page turn.'),
(183,22):(["must've",'been'],'Keep the auxiliary phrase intact in the speakers cowardice judgment.'),
(183,33):(['ended','up'],'Keep ended up together in Marias location question.'),
(184,20):(['each','other'],'Keep each other together in Cristinas affectionate observation.'),
(184,35):(['what','were','you','looking','at'],'Keep Marias short complete observation question together after the greeting.'),
(185,31):(["who's",'your','favorite','hero'],'Keep the favorite-hero question together after the enthusiasts greeting.'),
(186,37):(['two','hundred','years'],'Keep the exact prophecy quantity and time unit together.'),
(186,58):(['shandong','peninsula'],'Keep the complete Shandong Peninsula name together in the clue.'),
(187,86):(['leave','it','to','you'],'Keep Manuels leave it to you expression together without changing his qualification.'),
(188,53):(['demon',"king's"],'Keep demon king together in the weapon-name reflection.'),
(190,11):(['just','west'],'Keep just west together in the uncertain Avalon direction.'),
(191,39):(['move','me'],'Keep move me together in Ians personal response to the ancient tales.'),
(193,26):(['came','out','of','nowhere'],'Keep came out of nowhere together in Julians apology for his abrupt comparison.'),
(194,56):(['drove','back'],'Keep drove back together in the Saladin explanation.'),
(195,32):(['seven','boats'],'Keep seven boats together without changing the source quantity or claiming arrival.'),
(195,57):(['get','back','to','work'],'Keep get back to work together in the ordinary closing return.'),
}


def main():
    target=ROOT/'formatting_v1/page_preferences_v8_phrases.json';findings=ROOT/'viewed_phrase_findings_v1.json'
    assert not target.exists() and not findings.exists()
    source=ROOT/'formatting_v1/page_preferences_v7_FE.json';prefs=load(source)
    docpath=ROOT/'formatting_v1/formatting_input.json';rows={r['id']:r for r in load(docpath)['records']}
    planpath=ROOT/'plan_v6/automatic_plans.json';plans={r['id']:r for r in load(planpath)['records']}
    visualpath=ROOT/'initial_body_visual_review_v1.json';visual=load(visualpath)
    assert visual['body_records']==294 and visual['body_pages']==302 and visual['all_native_pages_bound_to_directly_viewed_exact_contact_sheet_tiles']
    viewed={r['id']:r for r in visual['records']};records=[]
    for (block,number),(words,reason) in CHANGES.items():
        key=f'DK4_MES_B{block}_R{number:04d}';row=rows[key];assert viewed[key]['compiled_hex']==plans[key]['encoded_hex']
        entry=prefs['records'].setdefault(key,dict(bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']}))
        pairs=entry.setdefault('required_pairs',[])
        for pair in zip(words,words[1:]):
            if list(pair) not in pairs:pairs.append(list(pair))
        entry['reason']=entry.get('reason','')+' '+reason
        records.append(dict(id=key,source_reference=row['source_reference'],current_reference=row['current_reference'],
            initial_lines=plans[key]['lines'],initial_compiled_hex=plans[key]['encoded_hex'],finding=reason,
            exact_viewed_native_pages=viewed[key]['pages'],native_refresh_anddirect_view_pending=True))
    prefs.update(previous_preferences=str(source),previous_preferences_sha256=digest(source),
        all_findings_from_directly_viewed_exact_native_tiles=True,no_prose_or_physical_width_changes=True,
        evidence={str(p):digest(p) for p in [docpath,planpath,visualpath,source,Path(__file__)]})
    save(target,prefs);save(findings,dict(records=records,findings=len(records),visual_review=str(visualpath),visual_review_sha256=digest(visualpath),
        no_new_prose_revision_orcompletion_credit=True,new_credit=0,evidence={str(p):digest(p) for p in [target,Path(__file__)]}))
    print('Prepared twenty source/current-bound phrase refinements fromdirectly viewed native pages; no prose changes.')


if __name__=='__main__':main()
