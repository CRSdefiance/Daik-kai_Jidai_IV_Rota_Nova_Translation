"""Three whole-source revisions: restore agency and remove unsupported bounty."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_prose_v8723')
CURRENT=Path('work/analysis/Hodram_B31_B53_current_v8722/current_effective.json')
GLOSS=Path('work/analysis/Hodram_B31_B53_clean_context_v8714/three_clean_glosses_explicit52_31_53_dependency_andunnamed_man_before_current_English.json')
VIEW=Path('work/analysis/Hodram_B31_B53_source_view_v8721/direct_source_view_andscoped_name_findings.json')
TERM=Path('translations/lil_goods_mediterranean_editorial_manuscript_v6.json')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v1.json')
NAMES=Path('translations/hodram_B31_B53_speaker_name_review_v1.json')

REVIEWS={
 'DK4_MES_B31_R0013':dict(
    english="You just won't quit, will you? Fine. I'll take you on myself.",
    finding='Persistent fool. adds an intelligence judgment absent from しつこい野郎. Then face me yourself. shifts the emphatic action onto the addressee, while この俺が相手になろう says that the speaker himself will take the opponent on.',
    reason='Render the exasperated rough complaint as the pointed conversational You just won\'t quit, will you? rather than an unsupported label of stupidity. The rhetorical tag conveys irritation without adding a new factual question, admiration or a motive for persistence. Fine. supplies the natural transition in ならば. I\'ll take you on myself preserves the speaker\'s explicit first-person agency and emphatic この俺 in a direct challenge to the interlocutor. It does not order the player to act, promise victory or death, name a battlefield or invent a relationship. Read this complete short variant independently; it is not followed by the longer repeated opening.'),
 'DK4_MES_B31_R0018':dict(
    english="You just won't quit, will you? Fine. I'll take you on myself before you cross a man you really ought to fear.",
    finding='The longer current variant repeats the unsupported fool and the reversed face me yourself agency. Its existing before-clause recognizes the frightening man, whose identity the source leaves unnamed.',
    reason='Use the same irritated challenge and corrected I\'ll take you on myself agency as the distinct short variant. Attach the original before-clause to that decision. Cross a man you really ought to fear is idiomatic American English for incurring the anger of a truly frightening man; it preserves anger, masculine reference, warning and degree without wooden wrath phrasing. Keep a man unnamed: the Japanese does not establish that this is a sultan, commander, relative, the speaker himself or another named person. Do not add fear as an already observed player emotion, a specific punishment, rescue motive, national affiliation or guaranteed outcome. The wording warns about the prospective consequence and does not explain the original query as a plot fact.'),
 'DK4_MES_B53_R0007':dict(
    english="Looks like you've finally ended up wanted by the Ottoman Empire. You'd better watch yourself.",
    finding='Put a price on your head. invents a monetary bounty for 手配. The current statement also loses the apparent/reported status expressed by ようだ and the culmination/unwanted-development nuance of とうとう/されちまった.',
    reason='Looks like preserves apparent or reported status instead of claiming omniscient certainty. Finally ended up wanted carries the culmination and undesirable development, with wanted describing being sought by the Ottoman Empire rather than adding a price, crime, warrant, court process, named pursuer or location. You\'d better watch yourself gives the gruff practical caution of せいぜい気をつけなよ in the established informal port-worker voice. The contractions and complete conversational warning read naturally as one exchange. Preserve the approved Ottoman Empire term; do not import Hayreddin\'s identity or the preceding branch\'s unnamed man into this separate utterance.'),
}

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists() and not NAMES.exists()
    current,gloss,view,term=map(read,[CURRENT,GLOSS,VIEW,TERM]);ledger=read('translations/editorial_review_current_v1.json')
    assert current['source_first_glosses_andcomplete_native_page_view_precede_current_English'] and current['all3_source_units_uncredited_in_current_ledger']
    assert ledger['records_editorially_completed']==7234 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    completed={historical_key(r) for f in ledger['completed_editorial_families'] for r in f['records']}
    assert not completed&{historical_key(r) for r in current['records']}
    terms=[r for r in term['records'] if r['id']=='DK4_MES_B45_R0026'];assert len(terms)==1
    assert 'オスマン帝国' in terms[0]['source_Japanese'] and 'Ottoman Empire' in terms[0]['english']
    contexts={31:'Hayreddin\'s actor34 delivers a gruff irritated challenge. The original query and relative branches select either the short challenge or its longer warning variant, never both consecutive speeches. This complete exchange has no separate reply object. The before-clause leaves the frightening man unnamed. Original event31 requires52, and event53 requires31 while excluding74; the graph does not establish continuous conversation, original location, a particular B52 choice effect or earned activation. The actual query returns1 in own opening native context; value0 is separately mapped structurally without forcing the predicate.',
        53:'Actor113 gives one complete gruff practical warning that the addressee apparently has finally ended up wanted by the Ottoman Empire, then urges caution. The source gives no amount of money, named pursuer, crime, warrant, judicial process, location or outcome. Read the full statement as one warning, preserving its uncertainty and culmination. Original prerequisites link52->31->53 but do not make these one continuous conversation or identify the frightening man in B31. Actual natural event activation remains unobserved.'}
    rows=[]
    for original in current['records']:
        row=deepcopy(original);review=REVIEWS[row['id']];text=review['english']
        assert text!=row['effective_predecessor_paragraph'] and text==text.strip() and not any(v in text for v in ['\n','\r','{LB','{ALIGN','{PAD','  ','%'])
        assert not any(m in bytes.fromhex(row['source_hex'])[1:] or m in text.encode('cp932') for m in [b'FI',b'FA',b'FO'])
        row.update(english=text,logical_English=text,speaker='Barbarossa Hayreddin' if row['source_selector']==34 else 'Port Worker',
            source_meaning=row['first_clean_source_gloss'],context=contexts[row['block']],localization_note=review['reason'],finding=review['finding'],decision='revision',retention_reason=None,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            whole_clean_utterance_andalternate_branches_read=True,read_aloud_cadence_andemotional_progression_reviewed=True,
            prior_raw_storage_preserved=row['current_raw_storage_English'],prior_effective_paragraph_preserved=row['effective_predecessor_paragraph'],
            planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+text,
            no_authored_linebreak_alignment_padding_orallocation_driven_shortening=True,
            source_controls_andruntime_substitutions_must_remain_exact=True,formatting_native_stored_actual_policy_atomic_andregistered_integration_pending=True,
            source_prose_orcompletion_credit_added=False)
        rows.append(row)
    source_names=read(view['names']);progressive=source_names['fresh_actor34_two_getters']['rows'][0]
    assert progressive['consumer']=='progressive-nameplate' and progressive['text']=='Barbarossa Hayreddin'
    save(NAMES,dict(format='dk4-scoped-speaker-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        records=[dict(actor_ID=34,speaker='Barbarossa Hayreddin',decision='provisional-retention',
            source_components=['バルバロッサ','ハイレディン'],exact_source_current_andnative_bindings=source_names,
            reason='Both existing progressive name components are sourced, and the native consumer renders the established complete label in bounds. Preserve those components and current order while checking all relevant consumers. Do not promote the earlier surname-only approval into full-name approval or introduce historical titles or a biography.',
            review=dict(source=True,context=True,localization=False,naturalness=False,formatting=False),
            actual_scene_header_andfull_editorial_name_decision_pending=True),
            dict(actor_ID=113,speaker='Port Worker',decision='scoped-retention',source='出港所の兄貴',
                reason=view['scoped_progressive_name_findings'][1]['reason'],exact_source_current_andnative_binding=source_names['scoped_reused_actor113'],
                review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),actual_B53_header_observation_pending=True)],
        full_name_open_finding=view['full_name_open_finding'],new_name_asset_changes=0,all207_names_orfullcatalogue_UI_not_approved=True,new_credit=0,full_goal_complete=False))
    save(DOC,dict(format='dk4-whole-exchange-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],current_archive_sha256=current['current_archive_sha256'],
        file_path='/data/SC1.DK4',blocks=[31,53],records=rows,typed_choice_records=[],total_editorial_objects=3,physical_speech_objects=3,typed_choice_objects=0,revised=3,retained=0,
        names_packet=str(NAMES),names_packet_sha256=sha(NAMES.read_bytes()),source_context=str(GLOSS),source_context_sha256=sha(GLOSS.read_bytes()),current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),
        source_native_view=str(VIEW),source_native_view_sha256=sha(VIEW.read_bytes()),
        approved_Ottoman_Empire_term=dict(path=str(TERM),sha256=sha(TERM.read_bytes()),record=terms[0]),
        source_macro_counts=dict(FI=0,FA=0,FO=0),source_FE_panels=0,source_relative_sites=4,source_query_sites=1,source_opaque_commands=8,
        all_three_clean_first_glossed_andnative_viewed_before_current_English=True,whole_exchange_andalternate_branch_context_reviewed=True,
        all_four_prose_gates_true_all_formatting_gates_false=True,names_actor34_fullreview_still_pending=True,ordinary_wrapping_owned_by_formatter=True,
        no_new_ROM_registered_integration_orcompletion_credit=True,new_credit=0,full_goal_complete=False))
    ROOT.mkdir(parents=True)
    save(ROOT/'contextual_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        records=[dict(id=r['id'],source_reference=r['source_reference'],source_hex=r['source_hex'],current_reference=r['current_reference'],current_hex=r['current_hex'],
            prior=r['prior_effective_paragraph_preserved'],english=r['english'],decision=r['decision'],finding=r['finding'],reason=r['localization_note']) for r in rows],
        revisions=3,retentions=0,all_four_prose_gates_true_all_formatting_gates_false=True,actor34_fullname_review_andall_native_stored_actual_policy_atomic_release_gates_pending=True,
        no_ROM_registry_orcompletion_credit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,GLOSS,VIEW,TERM,DOC,NAMES,Path(__file__)]}))
    for r in rows:print(r['id'],repr(r['english']))
    print('Three contextual revisions recorded; agent andbounty defects corrected. Prose gates pass;formatting/name completion/actual/release remain pending;zero credit.')
