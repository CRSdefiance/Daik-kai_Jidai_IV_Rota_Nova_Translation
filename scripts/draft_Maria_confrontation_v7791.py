"""Localize the complete confrontation against fresh clean glosses andactual current templates."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_prose_v7791')
CURRENT=Path('work/analysis/maria_confrontation_current_v7789/all16_complete_source_current_refs_before_new_English_manuscript.json')
CONSUMERS=Path('work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json')
NATIVE_NAMES=Path('work/analysis/maria_confrontation_names_v7788/three_static_speakers_six_getters_clean_fields_source_macros.json')
GLOSS=Path('work/analysis/maria_confrontation_gloss_v7787/sixteen_clean_whole_exchange_glosses_before_current_English.json')
MANUSCRIPT=Path('translations/maria_B36_editorial_manuscript_v1.json')
NAMES=Path('translations/maria_B36_speaker_name_review_v1.json')
DECISIONS={
    5:('retention',"Everyone ready to sail?",
        "This is already a natural question to the group about departure readiness. It preserves the source intent without claiming that sailing has begun or naming an unproved current port."),
    9:('retention',"Oh, that must be Lil Argot, head of Argot Company.",
        "Retain this spoken recognition: that must be naturally conveys identifying the person in sight, and the source-supported leader and company names are intact. Argot Company functions as the company name here. Actor0A is Xien Yan, not Camille; no new rank or Camille attendance is inferred."),
    12:('retention',"Seems so.",
        "The brief conversational confirmation sounds natural after Xien's identification and preserves Maria's measured assent. It is a complete response in this exchange, rather than a missing fragment of an explanation."),
    16:('retention',"Excuse me. Admiral Lil Argot?",
        "The polite interruption followed by the questioning name and source-supported title is idiomatic American dialogue. The identity question remains clear without expanding an already effective line."),
    19:('revision',"W-what's this about? Yes, I'm Lil. Who are you?",
        "Preserve Lil's stammer and defensive surprise, her acknowledgement and demand for an identity. Restore the natural first-person clause; avoid the old clipped Yes, Lil Argot or an invented question about the stranger's physical origin."),
    23:('revision',"I'm FI of FO. Surely you've heard of me.",
        "Maria confidently identifies herself and expects recognition. Preserve both runtime tokens exactly. The source line gives her name and company, so do not add an admiral rank to this particular introduction merely to smooth it."),
    27:('retention',"FI?! You came here in person?",
        "This already sounds like Lil's shocked recognition and preserves the direct personal arrival. The exclamation and question convey the source repetition without mechanically repeating interjections or inventing an invasion or battle."),
    31:('retention',"Ah! You came to kill me?!",
        "Retain the sudden fearful question in Lil's voice. In this exchange it is an alarmed suspicion that Maria immediately denies, not a narrator's claim or an established assassination attempt."),
    34:('revision',"No. It seems Kuhn's really misled you... I came to tell you the truth. He's using you.",
        "Use the established Kuhn spelling. Preserve Maria's denial, inferred assessment of misleading influence, explicit purpose in coming and accusation of manipulation. The source poison metaphor concerns misinformation; do not imply literal poisoning or omit why Maria came."),
    37:('revision',"What do you mean? Kuhn's trying to save the people of Southeast Asia. He's a great merchant!",
        "Restore the people and named Southeast Asia rather than the vague this land. Keep the attempted rescue and praise as Lil's confident belief, not confirmed truth, and retain merchant. Use contractions appropriate to her direct voice and the established Kuhn spelling."),
    41:('revision',"I'm only helping him! You're the one running China's underworld, you pirate!",
        "Restore the complete first-person defense and the contemptuous counteraccusation. The accusation is explicitly Lil's speech; running the underworld does not mean ruling China itself, and the localization does not endorse the charge as narrator fact."),
    45:('revision',"You don't know what Kuhn's really like... He plans to use you for all you're worth, then get rid of you.",
        "本性 concerns Kuhn's true character, not only his plans. Use a natural contraction and the idiom use you for all you're worth. Preserve his intended future sequence. Get rid of you retains the source euphemism; the surrounding kill question and life warning make its lethal implication clear without inventing a method."),
    49:('revision',"That's a lie! Stop making things up! Do you have any proof that Kuhn's the bad guy? You don't, do you?!",
        "Preserve all parts of Lil's rejection: denial, accusation of fabrication, demand for proof and insistent rhetorical challenge. Her contracted, colloquial argument should not sound like the older formal No, you do not. No document or proof is invented."),
    52:('revision',"Don't you understand yet? Your life is at stake. It's not too late.",
        "Preserve Maria's frustrated question, explicit life danger and present opportunity to act. Avoid the older Still blind and archaic There is time yet, while adding no deadline, escape plan or guaranteed mechanic."),
    56:('revision',"You can't just spring that on me and expect me to believe it! Hmph!",
        "Localize the abrupt unsupported claim as springing something on someone. Lil refuses to believe Maria merely because she says it; the issue is the sudden allegation, not a literal person appearing from nowhere. Retain the dismissive snort and unresolved disagreement."),
    60:('retention',"Stubborn girl...",
        "This works as Maria's exasperated aside after Lil refuses to listen. Girl is the source's dismissive reference to Lil; it creates no mother-daughter relationship, romance, childish age claim or reconciliation. Keep the existing trailing pause without authored layout breaks."),
}
if __name__=='__main__':
    assert not ROOT.exists() and not MANUSCRIPT.exists() and not NAMES.exists()
    current,effective,native,gloss=map(read,[CURRENT,CONSUMERS,NATIVE_NAMES,GLOSS])
    assert current['gloss_packet_sha256']==sha(GLOSS.read_bytes()) and effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    assert effective['native_names_packet_sha256']==sha(NATIVE_NAMES.read_bytes()) and len(effective['source_current_dispatches'])==32
    assert native['exact_static_source_selectors']==[2,3,10] and native['measured_current_macro_ascii_lengths']==dict(FI=5,FA=2,FO=7)
    getters=native['native_six_progressive_and_full_name_consumers']['rows'];rows=[]
    for original in current['records']:
        row=deepcopy(original);index=row['source_record_index'];decision,english,reason=DECISIONS[index]
        before=next(r for r in effective['effective_current_records'] if r['id']==row['id'])
        assert (english==before['effective_predecessor_paragraph'])==(decision=='retention')
        assert all(english.count(token)==bytes.fromhex(row['source_hex'])[1:].count(token.encode()) for token in ['FI','FA','FO'])
        assert not any(token in english for token in ['{LB','{ALIGN','{PAD','\n','\r'])
        speaker=next(g['text'] for g in getters if g['actor_ID']==row['source_selector'] and g['consumer']=='progressive-nameplate')
        row.update(english=english,speaker=speaker,source_meaning=row['source_gloss'],context=row['full_clean_exchange_context'],
            localization_note=reason,decision=decision,decision_reason=reason,editorial_decision='revise' if decision=='revision' else 'retain-wording',
            retention_reason=reason if decision=='retention' else None,predecessor_effective_reference=before,
            effective_predecessor_paragraph=before['effective_predecessor_paragraph'],
            whole_English_exchange_cadence_andemotional_progression_reviewed=True,
            exact_source_macros_preserved=True,native_control_font_reference_actual_andrelease_gates_pending=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),new_credit=0)
        rows.append(row)
    assert len(rows)==16 and Counter(r['decision'] for r in rows)=={'revision':9,'retention':7}
    name_notes={
        2:"Retain Lil Argot: the clean リル/アーゴット fields and both original getters support it, and the body identifies her by that name and company. The source explicitly uses admiral/head of the company; no additional rank, relationship or biography is added.",
        3:"Retain approved Maria and surname Li in the nameplate, with existing full getter Maria Huamei Li. Keep runtime FI/FO in the dialogue; no fixed substitution or new rank is authored into her source name/company introduction.",
        10:"Retain Xien Yan from the clean シエン/ヤン fields and both original getters. The source selector0A is Xien, not Camille09; the recognition line therefore gives no reason to invent Camille changing his earlier reluctance to meet Lil.",
    }
    name_rows=[]
    for actor in [2,3,10]:
        name_rows.append(dict(actor_ID=actor,decision='retention-in-this-exchange',reason=name_notes[actor],
            clean_current_static_fields=next(v for v in native['complete_clean_andcurrent_static_name_fields'] if v['actor_ID']==actor),
            original_getters=[g for g in getters if g['actor_ID']==actor],
            source_speech_keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows if r['source_selector']==actor],
            name_asset_changed=False,actual_scene_headers_andfull_catalogue_UI_pending=True,new_credit=0))
    save(NAMES,dict(format='dk4-contextual-speaker-name-review-v1',records=name_rows,
        native_name_macro_proof=str(NATIVE_NAMES),native_name_macro_proof_sha256=sha(NATIVE_NAMES.read_bytes()),
        three_scoped_retentions_not_full207_name_orother_consumer_approval=True,
        all207_name_role_alias_review_active=True,all_shared151_159_andother_prior_name_leads_preserved=True,new_credit=0,full_goal_complete=False))
    save(MANUSCRIPT,dict(format='dk4-whole-exchange-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path=current['file_path'],route=3,route_identity='Maria',block=36,current_ROM=current['current_ROM'],
        current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],
        records=rows,source_current_packet=str(CURRENT),effective_packet=str(CONSUMERS),names_packet=str(NAMES),
        complete_clean_glosses_precede_current_comparison=True,all_current_effective_templates_reviewed=True,
        actual_source_macro_counts=dict(FI=2,FA=0,FO=1),all16_formatting_gates_false=True,formatting_review_pending=True,
        source_dependency35_to36_not_natural_activation_immediate_chronology_orlocation=True,
        all_claims_in_argument_attributed_to_original_speakers=True,no_invented_Camille_presence_rank_kinship_motive_orcompleted_mechanic=True,
        existing_system_only_unlock_earned_false=True,evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,CONSUMERS,NATIVE_NAMES,GLOSS,NAMES,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);save(ROOT/'sixteen_complete_exchange_decisions9_revisions7_retentions.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        revisions=9,retentions=7,source_macro_counts=dict(FI=2,FA=0,FO=1),all16_formatting_false=True,
        current_native_controls_fonts_stored_reference_actual_policy_production_andrelease_pending=True,new_credit=0,full_goal_complete=False))
    print('Maria B36:9 contextual revisions/7 individually justified retentions;3 scoped name retentions;FI2/FO1 intact.All formatting/release gates pending;zero credit.')
