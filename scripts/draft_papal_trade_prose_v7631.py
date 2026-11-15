"""Review both complete route exchanges; keep display and integration gates pending."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/papal_trade_prose_v7631')
CURRENT=Path('work/analysis/papal_trade_SC0_SC1_current_v7620/two_complete_current_exchanges36_source_current_refs_before_new_prose.json')
CLEAN=Path('work/analysis/papal_trade_SC0_SC1_clean_v7619/two_complete_clean_exchanges36_refs_exact_Japanese_gloss_reuse_before_current_English.json')
FINDINGS=Path('work/analysis/papal_trade_route_identity_v7624/corrected_SC0_Rafael_SC1_Hodram36_raw_findings_no_body_changes.json')
CONSUMERS=Path('work/analysis/papal_trade_consumers_v7627b/two_routes36_effective_bodies72_dispatches_eight_getters.json')
ENTRY=Path('work/analysis/papal_trade_entries_v7628/original_EV0_EV1_events_actions_dependencies_andactual_route_getters.json')
FONTS=Path('work/analysis/papal_trade_name_inputs_v7629/two_routes40_fresh_literal_alignments_five_exact_reused_font_planes.json')
CONTROLS=Path('work/analysis/papal_trade_controls_v7630/two_current_blocks50_fresh_seeded_ends_exact_effect_andclean_end_reuse.json')
PRIOR_NAMES=Path('translations/lil_B234_speaker_name_review_v2.json')
NAMES=Path('translations/papal_trade_speaker_name_review_v1.json')
MANUSCRIPTS={0:Path('translations/rafael_B246_editorial_manuscript_v1.json'),1:Path('translations/hodram_B237_editorial_manuscript_v1.json')}
PROSE={
5:('………',"Retain all three original CP932 ellipses as meaningful absorbed silence. Carlo's following familiar question brings the merchant out of his thoughts. Do not add speech or a physical staging break. Exact prior source-glyph and palette observations remain scoped reuse; counterpart English display is pending."),
9:("What's wrong, Filippo? Daydreaming?","Use natural familiar concern and light teasing. Restore the explicit source address フィリポ: SC0 substitutes friend and SC1 uses a full-width initial F, both confirmed effective native output. ASCII Filippo follows the source-bound project spelling, not a new shared actor104 nameplate or invented relationship."),
12:("Huh? Carlo! When did you return?","Retain the warm startled recognition and clear return question. Return is slightly more formal than get back but fits the merchant's spoken voice without stiffness in this short line. Huh? and Carlo! carry the source's startled recognition; repeating Carlo again is unnecessary in natural English. No date, home city or promised visit is inferred."),
16:("I just stopped by on business. But Filippo, you'll never draw customers with that vacant look on your face!","Make the incidental stop a complete spoken sentence, restore Filippo, and preserve the familiar vacant-look/customer teasing. This is practical banter between acquaintances, not an assertion of stupidity or illness. Business is unspecified and adds no transaction, recovery cause, rank or kinship."),
19:("Mind your own business! Still, teasing me like that... You seem to be back to your old self.","Keep the idiomatic rebuff and friendly sharp-tongue turn. You seem restores the source's tentative inference; back to your old self leaves the cause of Carlo's recovery unspecified. The hesitation belongs to spoken progression, not an authored line break. No illness, bereavement, romance or treatment is supplied."),
23:("Yes. Back in action at last. I'm aboard their ship now.","Use natural first-person speech instead of the confirmed stored This man. Back in action preserves the return to active life; aboard their ship restores the explicit current ship relationship lost in sails with these people, which could imply only a convoy. No precise crew role, employment agreement or ownership by Carlo is added."),
26:("Oh! Customers? Sorry about that. I was lost in thought, remembering a story my great-grandfather told me.","Preserve recognition of the visitors, apology, distraction and the explicitly related great-grandfather in a flowing complete account. First-person my belongs to the merchant; the role 親父 does not make him Carlo's father. No purchase or new relationship is invented."),
29:("What story?","Retain the natural short invitation after a story my great-grandfather told me. The question asks for the account and lets the next speaker introduce its topic. It is conversationally complete in this exchange; adding kind of would be an optional variation, not a necessary correction."),
33:("It was about trade in the Papal States. The pope's direct rule once stretched almost to Venice.","Preserve the territorial trading subject and restore direct rule from 直轄. Papal States retains the established cultural and territorial expression. Almost to Venice preserves the approximation and does not assert rule over Venice itself, a present location, a date or a modern historical correction."),
37:("I've heard about that. They say trade flourished in those lands when papal power was at its height.","Restore natural first-person recollection and both hearing/reporting layers. Keep prosperity in those lands at peak papal influence as a historical report. This supplies no current market trend, price forecast, trading mechanic or guaranteed profit."),
40:("That's right. Back then, the lords competed over what to donate to the pope and how much to give...","Use conversational agreement and preserve the past competition over both kinds and quantities of donations. Lords naturally expresses the broad 諸侯 without assigning a princely rank to an NPC. The trailing hesitation introduces the explanation of ancestral profits; it is not a physical break, tax, quota or bribe."),
43:("My ancestors made fortunes just moving goods around. But these days...","Keep the commercial idiom and the trailing contrast. My places the ancestors with the merchant's great-grandfather account instead of implying shared ancestry with Carlo. Moving goods around conveys passing assorted goods along without inventing the old English's lord-to-lord route, a monopoly or present guaranteed profit."),
47:("Papal authority faded, and commerce with the Church fell away.","Retain Carlo's natural, slightly learned cooperative completion of But these days. Faded and fell away express decline in this historical trading context, not a declaration that every transaction ceased. Church identifies the institution already under discussion; no new date, accusation or current market rule is added."),
51:("Right. We're back to earning our living through hard work. How lucky my great-grandfather was!","Restore natural rueful agreement, making one's own way in business and the explicit great-grandfather comparison. How lucky expresses the source's envy of that earlier generation's easier conditions. Do not add poverty, laziness, inability to trade or shared ancestry."),
54:("Come to think of it, I've heard that objects linked to the pope sometimes turn up in lands he once ruled.","Restore personal hearsay and occasional finds while retaining the conversational recollection. Objects linked to the pope avoids treating general associated objects as authenticated holy relics. Former papal lands remain broad; no particular site, ownership, item title or guaranteed acquisition is given."),
57:("So they say. Something said to have been used by a pope might carry a blessing. Ah, I could use some divine aid myself!","Restore the hearsay agreement and reportedly used object, then make the rueful wish natural first-person speech. Might keeps the blessing speculative. Divine aid preserves God's favor in the explicit papal/religious context and sets up Carlo's retained reflective echo. No supernatural effect, stat, reward or authenticity is asserted."),
60:("Divine aid...","Retain the concise reflective echo, with R57 now ending in divine aid as well. The religious sense remains clear from the pope and prospective blessing, and the pause motivates Carlo's next thought. No prayer, conversion or narrator confirmation of supernatural truth is introduced."),
64:("Admiral, this may be no joke. If we found an object a pope treasured, it would be quite a discovery.","Retain the courteous source-supported Admiral address and tentative may be no joke while restoring the explicit if-found condition. Treasured conveys favored use. No particular pope, formal title, specific site, established possession, guaranteed acquisition, authenticity, wealth or stat is invented."),
}
RETAIN={5,12,29,47,60}

if __name__=='__main__':
    assert not ROOT.exists() and not NAMES.exists() and all(not p.exists() for p in MANUSCRIPTS.values())
    current,clean,findings,consumers,entry,fonts,controls,prior_names=map(read,[CURRENT,CLEAN,FINDINGS,CONSUMERS,ENTRY,FONTS,CONTROLS,PRIOR_NAMES])
    assert current['all36_clean_Japanese_gloss_bindings_precede_first_other_route_current_English_comparison']
    assert clean['source_glosses_reused_by_exact_whole_block_andrecord_bytes_not_freshly_authored_orEnglish_derived']
    assert consumers['fresh_original_route_specific_dispatches']==72 and consumers['fresh_original_name_getter_consumers']==8
    assert consumers['actual_original_captain_IDs']==[0,1] and consumers['actual_native_catalogue_route_masks']==[1,2]
    assert fonts['fresh_native_literal_alignment_cases']==40 and fonts['fresh_name_font_renderer_executions']==0
    assert controls['fresh_current_normal_end_cases']==50 and controls['distinct_exact_reused_clean_normal_end_cases']==25
    allpaths=[CURRENT,CLEAN,FINDINGS,CONSUMERS,ENTRY,FONTS,CONTROLS,PRIOR_NAMES,Path(__file__)]
    evidence={str(p):sha(p.read_bytes()) for p in allpaths}
    names=[];rows_all=[];outputs=[]
    for g,cg,eg in zip(current['groups'],consumers['groups'],entry['groups'],strict=True):
        route=g['route'];identity={0:'Rafael',1:'Hodram'}[route]
        assert route==cg['route']==eg['route'] and cg['route_identity']==identity
        assert eg['selected_source_events'][0]['script_block']==g['block']
        assert eg['selected_source_events'][0]['must_be_completed']==eg['selected_source_events'][0]['must_not_be_completed']==[]
        effective={r['id']:r for r in cg['effective_current_records']}
        voices={r['source_selector']:r['original_voice_class'] for r in cg['original_static_selectors']['rows']}
        assert voices=={19:7,104:0}
        for oldname in prior_names['records']:
            actor=oldname['actor_ID'];name=oldname['english']
            fields=next(r['fields'] for r in cg['source_name_fields'] if r['actor_ID']==actor)
            getters=[r for r in cg['native_four_distinct_name_consumers']['rows'] if r['actor_ID']==actor]
            assert fields==oldname['source_fields'] and len(getters)==2 and all(r['text']==name for r in getters)
            reason=("Retain Carlo Sinat from clean カルロ/シナート, both actual-route original getters, and Carlo's explicit body address and familiar banter. The null middle field contributes no additional name. The later courteous Admiral address does not establish a new rank or biography for Carlo." if actor==19 else "Retain Trader as a concise natural role for 交易所の親父 in this business exchange. Both original getters return Trader alone; 親父 does not prove Carlo's father. The separately stored European field is excluded from both returned names and supplies neither surname nor approved nationality. Filippo is the explicit body address, not permission to relabel every shared actor104 consumer.")
            names.append(dict(route=route,route_identity=identity,file_path=g['file_path'],block=g['block'],actor_ID=actor,english=name,editorial_decision='retain-wording',retention_reason=reason,source_fields=deepcopy(fields),source_voice_class=voices[actor],fresh_route_getter_references=[dict(consumer=r['consumer'],getter=r['getter'],text=r['text'],text_hex=r['text_hex'],ownership_mode=r['ownership_mode']) for r in getters],review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),approval_scope='This whole exchange and exact getter wording only; actual counterpart optional headers and full catalogue UI unvisited',prior_B234_display_is_exact_font_reuse_not_counterpart_gameplay=True,no_name_asset_or_duplicate_credit=True))
        rows=[]
        for r in g['records']:
            index=r['source_record_index'];text,reason=PROSE[index];e=effective[r['id']];retained=index in RETAIN
            assert (text==e['effective_predecessor_paragraph'])==retained
            assert not any(t in text for t in ['{LB','{PAD','{ALIGN','{MACRO:','\n','\r'])
            assert all(32<=ord(ch)<127 or index==5 and ch=='…' for ch in text)
            oldfinding=next(f for f in findings['records'] if f['file_path']==g['file_path'] and f['id']==r['id'])
            row=deepcopy(r)
            # Preserve historical pending-state fields with their original packet instead of
            # silently carrying stale pending descriptions as current approvals.
            for k in ['route_specific_current_context_name_entry_native_actual_andrelease_pending','current_effective_runtime_body_getter_voice_andcatalog_binding_pending','all_five_editorial_native_actual_andrelease_gates_pending']:
                row.pop(k,None)
            row.update(route=route,route_identity=identity,speaker={19:'Carlo Sinat',104:'Trader'}[r['source_selector']],english='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+text,source_meaning=r['source_gloss'],context=r['whole_clean_exchange_context'],context_scope='Exact complete clean exchange; native route/captain/getters verified; optional scene activation/location unvisited',localization_note=reason,editorial_finding=oldfinding['raw_source_current_editorial_finding'],editorial_decision='retain-wording' if retained else 'revise',retention_reason=reason if retained else None,current_effective_runtime_template_hex=e['current_effective_runtime_template_hex'],current_expanded_runtime_hex=e['current_expanded_runtime_hex'],current_effective_paragraph=e['effective_predecessor_paragraph'],current_registered_catalogue_match=e['registered_catalogue_match'],source_voice_class=voices[r['source_selector']],review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),full_exchange_read_aloud_review=True,no_manual_line_break_padding_or_alignment_authored=True,current_complete_native_display_pending=True,registered_integration_pending=True,formatting_reason='One logical paragraph; route-aware full-width formatting, complete glyphs, guards, pair phase, bounds, pagination, stored bytes and representative actual English display remain pending. Reused B234 source/font observations are not new SC0/SC1 optional gameplay.',source_prose_or_completion_credit_added=0)
            rows.append(row)
        assert len(rows)==18 and sum(r['editorial_decision']=='revise' for r in rows)==13
        out=MANUSCRIPTS[route]
        doc=dict(format='dk4-dialogue-batch-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',file_path=g['file_path'],route_identity=identity,source_ROM=clean['source_ROM'],source_ROM_sha256=clean['source_ROM_sha256'],current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],source_context=str(CURRENT),source_context_sha256=sha(CURRENT.read_bytes()),whole_clean_source_packet=str(CLEAN),whole_clean_source_packet_sha256=sha(CLEAN.read_bytes()),current_consumer_proof=str(CONSUMERS),current_consumer_proof_sha256=sha(CONSUMERS.read_bytes()),current_strict_native_input=cg['current_strict_native_input'],current_strict_native_input_sha256=cg['current_strict_native_input_sha256'],speaker_name_review=str(NAMES),source_entry_proof=str(ENTRY),name_font_proof=str(FONTS),controls_proof=str(CONTROLS),records=rows,revised=13,retained=5,retained_record_indices=sorted(RETAIN),all_clean_glosses_bound_before_current_English=True,source_glosses_exact_reuse_not_fresh_authoring=True,all18_source_context_localization_naturalness_gates_true=True,all18_formatting_gates_false=True,body_source_spoken_alias_Filippo_not_shared_nameplate_replacement=True,no_global_I_macro_font_orweak_word_rule_change=True,no_new_relationship_rank_nationality_recovery_cause_history_site_authenticity_orreward_invented=True,original_UI_controls_andzero_runtime_macros_preserved=True,new_emulator_runs=0,new_source_prose_reviews=0,new_completed_records=0,new_credit=0,registered_integration_pending=True,evidence=evidence,full_goal_complete=False)
        outputs.append((out,doc));rows_all.extend(rows)
    assert len(names)==4 and len(rows_all)==36
    ROOT.mkdir(parents=True)
    save(NAMES,dict(format='dk4-contextual-speaker-name-review-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',records=names,spoken_alias=dict(Japanese='フィリポ',English='Filippo',source_record_indices=[9,16],decision='restore-source-body-address',reason='Exact source personal address and established project spelling; no shared actor104 relabel.',legacy_metadata_leads=deepcopy(prior_names['spoken_alias']['legacy_metadata_leads'])),current_consumer_proof=str(CONSUMERS),name_font_proof=str(FONTS),four_contextual_name_retentions_no_assets_or_dialogue_credit=True,actual_optional_headers_andfull_catalogue_UI_unvisited=True,all_name_formatting_gates_false=True,full207_name_role_alias_andearlier_consumer_review_open=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    for out,doc in outputs:
        doc['speaker_name_review_sha256']=sha(NAMES.read_bytes());save(out,doc)
    save(ROOT/'two_complete_exchanges36_decisions26_revisions10_justified_retentions_display_pending.json',dict(manuscripts=[dict(path=str(p),sha256=sha(p.read_bytes()),route_identity=d['route_identity'],revised=d['revised'],retained=d['retained']) for p,d in outputs],speaker_name_review=str(NAMES),speaker_name_review_sha256=sha(NAMES.read_bytes()),records=rows_all,total_source_current_references=36,revised=26,retained=10,retained_source_indices_per_route=sorted(RETAIN),all36_formatting_gates_false=True,no_ROM_registry_orledger_mutation=True,no_duplicate_B234_ornew_source_prose_orcompletion_credit=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    for p,d in outputs:
        print(p, d['route_identity'], '13 revisions / 5 justified retentions; formatting/integration pending')
        for r in d['records']: print(r['source_record_index'],r['editorial_decision'],r['english'])
