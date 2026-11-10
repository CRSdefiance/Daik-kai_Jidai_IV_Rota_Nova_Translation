"""Record261 individual complete-exchange decisions;hold concrete name/term andall display gates."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha
from translations.rafael_B85_B100_contextual_decision_data_v1 import RETAIN,OVERRIDES,FINDINGS,CHOICE_RETAIN

ROOT=Path('work/analysis/Rafael_B85_B100_current_20261105')
SEALED=Path('work/analysis/Rafael_B85_B100_clean_drafts_20261105/261_source_meanings_andindependent_drafts_v1.json')
OUTPUT=Path('translations/rafael_B85_B100_contextual_prose_review_v1.json')
SPEAKERS={0:'Rafael',4:'Janus',5:'Claudio',6:'Julio',7:'Cristina',12:'Yukihisa',13:'Cesare',14:'Emilio',
    15:'Angelo',16:'Gerhard',18:'Charles',20:'Fernando',26:'Julian',41:'Kurushima',108:'Trader',109:'Shipwright',
    114:'Port Worker',151:'Sailor',152:'Former sailor (visible label pending)',158:"Kurushima's henchman (visible label pending)",254:'System/sound panel'}
CONTEXT={
85:'Complete conditional return to Gerhard. A sailor proposes another visit; Rafael goes alone and shows he has learned. Gerhard admits that Rafael’s words have troubled him and agrees to come aboard. The alternative refusal choice defers the visit, rather than occurring afterward.',
86:'Complete Caribbean explosion and Charles recruitment. Julio proposes rum, Cesare panics and calculates benefits, and Claudio’s bluntness needs Janus’s restraint. The shipwright wants Charles taken elsewhere and hurries through the introduction. Charles’s scientific monologue derails the recruitment question until Rafael repeats it. Familiar older-man addresses establish no kinship.',
87:'Complete Zipang encounter, from Claudio’s rude hairstyle criticism and Julio’s cultural tolerance through Kurushima’s staged collision and attack. Yukihisa intervenes with the back of his blade, apologizes and asks to sail away. His personal aspiration and formal voice remain distinct. The gang’s hostile foreigner address is character speech, not narration; Sun imagery and the full source name order matter.',
88:'Complete Silla crown discovery and Julian encounter, including both alternative choices. The party overheard Julian and Meihua in Hangzhou and found the crown first. One branch gives it to him under Rafael’s hastily claimed helping motive. The other states Rafael’s own gift intention; Julian infers a romantic rivalry and rushes off. His inference does not establish Rafael’s feelings or a new relationship.',
90:'Complete Janus daydream about Mediterranean trade and Rafael’s promise. Ports, countries and ship variety explain Janus’s wish. The regional-fleet assignment is conditional and future, with no specified timing. Preserve their warm encouragement and polite enthusiasm.',
91:'Complete miracle-belief encounter and both alternative reward branches. The man questions a captain’s dependability, Fernando objects, and the man offers a believing captain his talisman. He has asked one hundred people and cannot physically sail anymore; no cause of disability is supplied. Luck and Spirit notices are distinct outcomes, and the source explicitly names Fernando.',
92:'Complete tomato conversation. Emilio keeps chewing and praising the food; Rafael reacts and privately notes his appetite. A trader gives a seedling because of the praise. He sells or handles tomatoes, with no claim that he grows them. Preserve the comic repetition and final deadpan thought.',
93:'Complete banana theft and chase, ending with Rafael distracting Emilio with local food at Rafael’s expense. Three FE animal-like cries remain separate source commands. Unfamiliar seeds are only a possible discovery from Rafael’s perspective; Emilio remains focused on the banana. The payer question and answer must agree.',
95:'Complete Gerhard lost-sword reminiscence. He personally lost a cherished, excellent-handling Katzbalger fighting pirates. The fisherman and cheap-sale account is conjecture. Rafael’s hopeful reassurance and Gerhard’s conditional comfort do not establish recovery, a new owner or an actual sale.',
97:'Complete rogue-ninja clothing discussion, explanation and quarrel. Angelo’s lack of knowledge produces the ninja joke. Yukihisa’s code describes death after exposure of a ninja’s identity and dangerous defection. Teasing clashes with his formality; Rafael intervenes, both apologize, and they return to the armor rumor. Avoid inventing a specific male ninja owner or making a conditional objection an actual insult.',
100:'Complete amber exchange. Charles’s educated enthusiasm and scientific explanation contrast with the port worker’s bewilderment, leading to an offshore-island rumor. Preserve tree sap, the bee and the source thousands-of-years timescale. The place is hearsay, and the worker’s own ignorance is not a statement about everyone’s knowledge. Familiar address establishes no brotherhood.',
}

def old_paragraph(row):
    text=' '.join(row.get('current_effective_text',row.get('current_English','')).split())
    latin=[]
    for i,c in enumerate(text):
        if '\uff21'<=c<='\uff3a' or '\uff41'<=c<='\uff5a':latin.append(dict(index=i,old=c,new=chr(ord(c)-0xfee0)))
    for item in latin:text=text.replace(item['old'],item['new'])
    for macro in ['FI','FA','FO','FU']:text=text.replace(macro,'{MACRO:'+macro+'}')
    return text,latin

if __name__=='__main__':
    assert not OUTPUT.exists();current=load(ROOT/'current_effective.json');findings=load(ROOT/'current_choice_andglyph_findings_v1.json')
    sealed=load(SEALED);assert sealed['source_meanings_anddrafts_sealed_before_current_story_extraction']
    source_ids={r['id'] for r in sealed['records']};rows=[];held=[];glyphs=[]
    untranslated={r['id'] for r in findings['untranslated_current_source_speeches']}
    for group in current['groups']:
        for original in group['records']:
            row=deepcopy(original);key=row['block'],row['source_reference']['record_index']
            old,latin=old_paragraph(row);retention=key[1] in RETAIN.get(key[0],{})
            reason=RETAIN[key[0]][key[1]] if retention else None
            english=old if retention else OVERRIDES.get(key,row['independent_English_draft'])
            if row['id'] in untranslated:
                finding='Translate the remaining Japanese source speech as part of its complete exchange: '+row['source_meaning']
            elif retention:finding=reason
            else:finding=FINDINGS.get(key,'Use natural complete-exchange wording that preserves: '+row['source_meaning'])
            if key==(97,28):
                row['independent_source_meaning']=row['source_meaning']
                row['source_meaning']='Yukihisa has never met one; under the ninja code, a ninja whose true identity is exposed must die.'
            pending=[]
            for term in ['Zipang','Meihua','Silla Gold Crown','bullet pendant','tomato seedling','Katzbalger','rogue']:
                if term.lower() in english.lower():pending.append('Bind approved native term: '+term)
            if row['source_selector'] in [152,158]:pending.append('Review the contextual generic role against both actual name getters andother uses.')
            if row['source_selector']==13:pending.append('Review Cesare’s full header surname トーニ/Tony before name approval;body uses no invented surname.')
            row.update(english=english,decision='retention' if retention else 'revision',finding=finding,
                retention_reason=reason,localization_note=finding,context=CONTEXT[row['block']],speaker=SPEAKERS[row['source_selector']],
                current_normalized_logical_English=old,current_English=row['current_effective_text'],
                retained_wording_exact_after_documented_glyph_normalization=retention and bool(latin),
                current_name_andterm_bindings_pending=pending,native_name_controls_andfresh_formatting_pending=True,
                review=dict(source=True,context=True,localization=not pending,naturalness=True,formatting=False),
                all_fresh_display_andregistered_integration_pending=True,new_credit=0)
            if latin:
                glyphs.append(dict(id=row['id'],current_reference=row['current_reference'],current_hex=row['current_hex'],
                    normalized_Latin=latin,prose_retained=retention))
            if pending:held.append(dict(id=row['id'],reasons=pending))
            assert english.isascii() and not any(t in english for t in ['\n','{LB','{ALIGN','{PAD}'])
            for m,count in row['source_macros'].items():assert english.count('{MACRO:'+m+'}')==count,(row['id'],m)
            rows.append(row)
    assert len(rows)==255 and sum(r['decision']=='retention' for r in rows)==149
    for original in findings['choices']:
        row=deepcopy(original);key=row['block'],row['source_command_offset'],row['source_index']
        old=' '.join(row['current_English'].split());retention=key in CHOICE_RETAIN
        row.update(english=old if retention else row['independent_English_draft'],decision='retention' if retention else 'revision',
            finding=CHOICE_RETAIN[key] if retention else 'Answer the explicit miracle-belief question naturally;Trust/Doubt canmisframe itastrusting theperson.',
            retention_reason=CHOICE_RETAIN.get(key),context=CONTEXT[row['block']],
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            current_normalized_logical_English=old,current_name_andterm_bindings_pending=[],new_credit=0)
        row['localization_note']=row['finding'];rows.append(row)
    assert len(rows)==261 and {r['id'] for r in rows}==source_ids
    assert (sum(r['decision']=='revision' for r in rows),sum(r['decision']=='retention' for r in rows))==(108,153)
    assert len(glyphs)==3 and sum(len(g['normalized_Latin']) for g in glyphs)==4
    assert len(untranslated)==10 and all(next(r for r in rows if r['id']==k)['decision']=='revision' for k in untranslated)
    dependencies=[SEALED,ROOT/'current_effective.json',ROOT/'current_choice_andglyph_findings_v1.json',
        Path('translations/rafael_B85_B100_contextual_decision_data_v1.py'),Path(__file__)]
    save(OUTPUT,dict(format='dk4-editorial-contextual-prose-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',file_path=current['file_path'],blocks=list(range(85,101)),
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_archive_sha256=current['current_archive_sha256'],
        review_gates=['source','context','localization','naturalness','formatting'],records=rows,
        source_speeches=255,source_choice_labels=6,contextual_comparisons=261,proposed_revisions=108,justified_retentions=153,
        four_gate_passes=sum(all(r['review'][k] for k in ['source','context','localization','naturalness']) for r in rows),
        pending_name_term_IDs=held,fullwidth_Latin_findings=glyphs,current_untranslated_speeches=10,
        six_fullwidth_English_questionmarks_inthree_records_pending_fresh_display=True,
        whole_exchange_reviewed_before_choosing_retention_orrevision=True,
        no_prior_English_story_consulted_before_sealed_independent_drafts_in_this_intake=True,
        no_blanket_historical_exposure_claim=True,all_fifth_formatting_gates_pending=True,
        all_native_visual_stored_gameplay_andregistered_integration_pending=True,
        no_native_name_approval_from_raw_field_metadata=True,new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in dependencies}))
    print('261 complete-exchange comparisons:108 revisions/153 justified retentions;',len(held),'name/term holds;',
        sum(all(r['review'][k] for k in ['source','context','localization','naturalness']) for r in rows),'four-gate passes;all display gates pending.')
