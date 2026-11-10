"""Whole-exchange en-US decisions for24 speeches/two choices; native formatting still pending."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B46_prose_v7930')
CURRENT=Path('work/analysis/Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B46_effective_v7928/all24_effective_English_templates48_original_dispatches12_FE.json')
GLOSS=Path('work/analysis/Rafael_B46_branch_gloss_v7926/24_speeches2_choices_fresh_branch_context_before_current_English.json')
NATIVE_NAMES=Path('work/analysis/Rafael_B46_names_v7921/three_static_speakers_six_getters_clean_fields12_synthetic_macro_alignments.json')
FLOW=Path('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
MENU=Path('work/analysis/Rafael_B46_current_menu_v7929/two_current_choices_native_getters_geometry_exact_control_inverse_Hayreddin_component.json')
MANUSCRIPT=Path('translations/rafael_B46_editorial_manuscript_v1.json')
NAMES=Path('translations/rafael_B46_speaker_name_review_v1.json')
DECISIONS={
15:('retention',"Whew. Hayreddin saved our lives.",
    "Claudio's relieved exhalation and direct gratitude already sound natural after the Spanish-fleet danger. Saved our lives conveys 命拾い without inventing a formal alliance or rank. Hayreddin is bound to the clean ハイレディン name component; no full-name or biography correction is implied."),
18:('revision',"Yeah...",
    "Use a quiet, natural American acknowledgment after Claudio's relief. Yeah makes Rafael's assent clearer than Mm while the trailing pause preserves his preoccupation; do not make him cheerful or add a new motive."),
23:('retention',"At this rate, an enemy fleet may challenge us sooner than we expect.",
    "Julio's warning already reads naturally between Rafael's subdued reply and the offer to teach. It correctly makes an enemy fleet the possible initiator and preserves sooner-than-expected uncertainty, without ordering an immediate attack."),
27:('revision',"I'd better explain what else you can do at sea.",
    "Replace the interface-like your other sea options with Julio's spoken concern that he should teach Rafael more. This follows the warning and leads naturally to both Please do and No, thanks; it adds no family or military relationship."),
41:('revision',"Let me explain how to inspect your surroundings, start a battle, and search.",
    "On acceptance, turn the clipped list of action labels into a natural teacher's introduction. Keep all three activities and their source order, distinguish starting a battle from receiving an attack, and make no claim that these exhaust every action at sea."),
44:('retention',"To inspect a nearby city or fleet, or to attack one, you must first select it as your target.",
    "The explanation already clearly connects detailed inspection or a player-initiated attack with selecting a specific nearby town/city or fleet. Both target types and both purposes remain, without inventing a port, nationality or automatic battle."),
47:('revision',"Try searching along the coast. You might find all sorts of things.",
    "Preserve Julio's practical suggestion, coastline and possible variety of discoveries. Quite a lot shifts variety toward quantity; all sorts of things keeps 様々な物, and might avoids promising a find or a cash reward."),
51:('retention',"At sea, you can inspect nearby cities and fleets.",
    "The first system panel plainly introduces nearby town/fleet information. Inspect conveys the informational action and stays consistent with the following mode instructions, without turning the panel into character speech."),
54:('retention',"Press Y for the magnifying glass icon, which indicates Inspect mode.",
    "This concise system instruction preserves Y, the magnifying-glass icon and its information-mode meaning. Inspect is used consistently within the exchange; no new button or automatic target action is supplied."),
58:('retention',"To inspect a city or fleet, aim the magnifier at it and press A.",
    "The natural instruction retains both target types, placing the already introduced magnifying-glass cursor on the chosen target, and A confirmation. The shorter magnifier is unambiguous in this adjacent explanation."),
62:('retention',"Your ship can also attack cities and fleets.",
    "The source permits initiating battle against both towns and other fleets; this direct system sentence preserves both. It neither erases town attacks nor substitutes a defensive-only rule."),
65:('retention',"Press L in Inspect mode for the sword icon, which indicates Battle mode.",
    "The original information-to-battle transition, L button and sword mark are clear. The sentence keeps the starting mode, rather than implying that L always selects battle from any state."),
68:('retention',"To start a battle, aim the sword at a city or fleet and press A.",
    "The instruction naturally preserves both battle targets and the separate A confirmation. Switching to the sword alone is not described as starting an attack."),
72:('retention',"To search for items or supplies at sea, press R in Inspect mode.",
    "This is already clear American game instruction. It preserves R, the starting information mode, and both items and supplies; no extra search condition or guaranteed result is added."),
76:('retention',"A gray frame appears. This indicates Search mode.",
    "The two short sentences explain the visible gray frame and its search-mode role without the Japanese's redundant repeated identification. Color, shape and purpose remain."),
80:('revision',"Press A to search the land inside the gray frame.",
    "State the source's exact search area: land within the displayed frame. This is clearer than only aiming the frame at land, and preserves A confirmation without claiming that water or every visible object is searched."),
83:('retention',"Press L or R to cycle between Inspect, Battle, and Search modes.",
    "The overview already names all three modes and both cycling buttons naturally. The following two panels supply the opposite orders; do not invent another mode or a new confirmation step."),
87:('retention',"Press L to cycle modes: Inspect, Battle, then Search.",
    "The existing instruction preserves the exact source L order and is easy to follow after the overview. The list deliberately differs from the next R/Y instruction."),
91:('retention',"Press R or Y to cycle modes: Inspect, Search, then Battle.",
    "Retain the exact opposite direction and the source's alternative Y button. Both button names and the information/search/battle order already work; no global button swap is justified."),
95:('retention',"Well? Got it?",
    "On the acceptance path, Julio's brief, informal check sounds like spoken instruction and matches the two source questions. It checks understanding without claiming that Rafael has demonstrated mastery."),
98:('retention',"Yes. Thank you, Julio.",
    "On acceptance, Rafael's polite assent and appreciation naturally answer the check. Addressing the established speaker by name preserves respectful warmth without inventing kinship, a rank or a newly learned fact."),
105:('revision',"All right. Just don't let your guard down at sea.",
    "This belongs to the declined-explanation path. All right acknowledges No, thanks; Good would sound like approval of demonstrated understanding. Preserve Julio's emphatic caution and mentor's voice without adding a threat or scolding."),
109:('retention',"Yes.",
    "The brief acknowledgment responds naturally to Julio's decline-path warning. A sir, family title or expanded promise would add source-unsupported implications."),
117:('revision',"(Someday, for sure...)",
    "Use an idiomatic American private fragment in place of the stiff Someday, surely. For sure preserves きっと's determination and the unfinished thought remains unfinished on both paths; no revenge, victory, rank or specific ambition is invented."),
}
CHOICES={
0:("Please do.","This politely accepts Julio's offer and leads into the explanation. The wording already matches the request's function and respectful tone; raw storage padding is formatter-owned and is not retained as prose."),
1:("No, thanks.","This is a natural polite decline of the offered lesson, matching the option's I can manage now function. It leads to Julio's acknowledgment and caution, not the tutorial. It adds neither a health claim nor an assertion of proven mastery; raw storage padding is not prose."),
}
if __name__=='__main__':
    assert not ROOT.exists() and not MANUSCRIPT.exists() and not NAMES.exists()
    current,effective,gloss,names,flow,menu=map(read,[CURRENT,EFFECTIVE,GLOSS,NATIVE_NAMES,FLOW,MENU])
    assert effective['source_packet_sha256']==menu['current_packet_sha256']==sha(CURRENT.read_bytes())
    assert current['gloss_packet_sha256']==sha(GLOSS.read_bytes()) and len(effective['source_current_dispatches'])==48
    assert len(gloss['records'])==24 and len(gloss['menu_choices'])==2 and flow['decline_path7_speeches_skips_tutorial_enters_caution_inside_outer0100']
    rows=[]
    for original in current['records']:
        row=deepcopy(original);decision,english,note=DECISIONS[row['source_record_index']]
        before=next(r for r in effective['effective_current_records'] if r['id']==row['id'])
        assert (english==before['effective_predecessor_paragraph'])==(decision=='retention')
        row.update(english=english,logical_English=english,speaker={0:'Rafael',5:'Claudio',6:'Julio',254:'System information panel'}[row['source_selector']],
            source_meaning=row['source_gloss'],context=row['full_clean_exchange_context'],localization_note=note,
            decision=decision,editorial_decision='retain-wording' if decision=='retention' else 'revise-wording',
            retention_reason=note if decision=='retention' else None,editorial_finding=note,
            effective_predecessor=deepcopy(before),original_voice_class={0:2,5:4,6:5}.get(row['source_selector']),
            whole_exchange_situation_voice_andprogression_reviewed=True,
            exact_source_macros_preserved=True,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            native_font_wrapping_reference_actual_policy_andregistered_release_pending=True,new_credit=0)
        rows.append(row)
    choices=[]
    for original in current['typed_choice_records']:
        row=deepcopy(original);english,note=CHOICES[row['option_index']]
        assert english==row['raw_storage_comparison_paragraph']
        row.update(english=english,logical_English=english,speaker="Player choice (Rafael's response; menu has no speech selector)",
            source_meaning=row['source_gloss'],context=row['full_clean_exchange_context'],localization_note=note,
            decision='retention',editorial_decision='retain-wording',retention_reason=note,editorial_finding=note,
            whole_exchange_situation_voice_andprogression_reviewed=True,source_choice_order_preserved=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            menu_native_getters_geometry_backing_highlights_actual_selection_andregistered_release_pending=True,new_credit=0)
        choices.append(row)
    allrows=rows+choices
    assert len(rows)==24 and len(choices)==2 and Counter(r['decision'] for r in allrows)=={'revision':7,'retention':19}
    assert all(r['english']==r['english'].strip() and not any(v in r['english'] for v in ['\n','\r','\0','{LB','{ALIGN','%']) for r in allrows)
    scoped=[]
    for r in names['naming_retentions']:
        scoped.append(dict(**r,decision='retention-in-this-exchange',
            clean_current_fields=next(n for n in names['complete_clean_andcurrent_name_fields'] if n['actor_ID']==r['actor_ID']),
            original_getters=[n for n in names['native_six_progressive_andfull_getters']['rows'] if n['actor_ID']==r['actor_ID']],
            source_speech_keys=[dict(file_path=s['file_path'],id=s['id']) for s in rows if s['source_selector']==r['actor_ID']],
            name_asset_changed=False,actual_B46_headers_andother_consumer_UI_pending=True,new_credit=0))
    ROOT.mkdir(parents=True)
    save(NAMES,dict(format='dk4-contextual-speaker-name-review-v1',records=scoped,
        native_proof=str(NATIVE_NAMES),native_proof_sha256=sha(NATIVE_NAMES.read_bytes()),
        mentioned_Hayreddin_component=menu['Hayreddin_source_current_name_component'],
        mention_component_proof=str(MENU),mention_component_proof_sha256=sha(MENU.read_bytes()),
        mentioned_Hayreddin_full_name_middle_catalogue_andother_consumers_not_newly_approved=True,
        FE_is_separate_display_selector_not_actor254=True,three_scoped_retentions_not_full207_approval=True,
        full207_name_role_alias_review_active=True,new_credit=0,full_goal_complete=False))
    evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,GLOSS,NATIVE_NAMES,FLOW,MENU,NAMES,Path(__file__)]}
    save(MANUSCRIPT,dict(format='dk4-whole-exchange-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path=current['file_path'],route=0,route_identity='Rafael',block=46,
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],
        records=rows,typed_choice_records=choices,total_editorial_objects=26,revisions=7,retentions=19,
        source_current_packet=str(CURRENT),effective_packet=str(EFFECTIVE),names_packet=str(NAMES),
        source_controls_packet='work/analysis/Rafael_B46_source_controls_v7922/source_EV0_entry_four_relative_sites20_cases25_seeded_ends_menu_scope.json',
        source_branch_context_packet=str(GLOSS),native_menu_flow_packet=str(FLOW),current_menu_packet=str(MENU),
        complete_clean_glosses_andconditional_context_precede_current_comparison=True,
        all24_current_effective_templates_andtwo_native_choices_reviewed=True,
        source_macro_counts=dict(FI=0,FA=0,FO=0),all26_formatting_gates_false=True,formatting_review_pending=True,
        body_only_logical_draft_native_prefix_markup_stored_padding_andlayout_owned_by_formatter=True,
        source_selectors=[0,5,6,254],FE_panels=12,typed_menu_count=1,typed_choice_count=2,
        accept22_decline7_are_native_compositions_not_actual_gameplay=True,
        original_five_A000_four_relative_sites6300_61FF_andfull_normal_end_must_be_preserved=True,
        no_invented_family_rank_alliance_guaranteed_discovery_orcompleted_private_ambition=True,
        exact_Y_L_R_A_buttons_mode_orders_marks_andland_inside_search_frame_preserved=True,
        mode_terminology_scope=menu['mode_terminology_scope'],
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,
        ordinary_captain0_context_no_unlock_orstate_fixture=True,
        native_pages_full_characters_bounds_menu_backing_highlights_actual_paths_andatomic_release_pending=True,
        evidence=evidence,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    save(ROOT/'whole_exchange_26_contextual_decisions_formatting_pending.json',dict(manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        names_review=str(NAMES),names_review_sha256=sha(NAMES.read_bytes()),source_current_packet=str(CURRENT),
        revised=7,retained=19,all26_individual_first_four_gates_true_formatting_false=True,
        all_retained_wordings_exact_to_effective_predecessor_with_individual_reasons=True,
        no_completed_source_prose_credit_orROM_change=True,evidence=evidence,new_credit=0,full_goal_complete=False))
    print('B46:26 contextual decisions,seven revisions/nineteen justified retentions. All formatting/actual/atomic/release gates remain pending; no credit.')
