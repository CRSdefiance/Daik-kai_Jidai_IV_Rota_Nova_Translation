"""Twelve source-first contextual decisions; no formatting or integration approval."""
from copy import deepcopy
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_prose_v7873')
CURRENT=Path('work/analysis/Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B45_effective_v7872/all12_effective_English_templates24_original_dispatches_distinct_FE.json')
NATIVE_NAMES=Path('work/analysis/Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json')
CONTROLS=Path('work/analysis/Rafael_B45_source_controls_v7870b/source_EV0_five_relative_sites_predicate_resources_structural_andnormal_end.json')
CITY_HELP=Path('translations/city_help_manuscript_v1.json')
TOWN=Path('translations/town_trade_port_contextual_editorial_manuscript_v3.json')
MANUSCRIPT=Path('translations/rafael_B45_editorial_manuscript_v1.json')
NAMES=Path('translations/rafael_B45_speaker_name_review_v1.json')
DECISIONS={
    5:('retention',"Where did Julio go?",
       "Rafael's curious question already sounds natural before Julio calls back. The polite Japanese suffix does not require an English title or family term; the approved source-bound given name is sufficient."),
    9:('retention',"Over here!",
       "This lively, idiomatic call answers Rafael's question and draws his attention. The repeated Japanese here creates emphasis rather than additional facts, and the short English call preserves that effect without forced repetition."),
    13:('revision',"Oh, he's at the Market...",
        "Restore Rafael's realization after the call. The existing The Market fragment loses that response. Use Market consistently with the reviewed facility terminology, rather than confusing the trade facility with a retail shop."),
    18:('revision',"Start by selling some trade goods here. If you have anything you bought in Lisbon, try selling that. But remember...",
        "Keep Julio's practical first step and the conditional Lisbon cargo. The older anything we bought assumes shared purchases and drops the source if. The trailing warning leads directly into the required-contract explanation; no compulsory sale of all cargo is added."),
    21:('retention',"You need a contract to sell goods.",
        "This is a clear, natural teaching statement after But remember. Contract is the established command term, and the following question and explanation define it as local trading rights rather than a separate contract with each buyer."),
    24:('retention',"A contract?",
        "The short questioning echo naturally expresses Rafael's polite novice curiosity after Julio introduces the term. Context supplies the full question; adding fear, disrespect or a formal title would distort it."),
    29:('revision',"Go to the Palace or Governor's Office and pay the local ruler a contract fee. That gives you the right to trade in that town.",
        "Restore the full instructional sequence and the recipient of the fee. The older Pay at ... to earn local trade rights abbreviates away the local ruler and contract fee. Preserve both offices and town-specific permission without inventing an amount, bribery, tax or sale-specific agreement."),
    33:('revision',"It's a good idea to arrange contracts in different towns. When you're just starting out, the minimum fee should be enough.",
        "Replace the clipped commands with Julio's friendly recommendation. Retain various towns, the early-stage qualification and the tentative sufficiency of the minimum; do not promise that the minimum is always optimal or guarantees a particular share."),
    37:('revision',"I've already taken care of Ceuta's contract. You'll handle the next ones yourself.",
        "Restore Julio's explicit first-person responsibility for Ceuta and his expectation that Rafael handle future agreements. The older passive settled and clipped Next city's obscure both. No kinship, rank or universal exception is inferred."),
    52:('revision',"FO's market share in Ceuta is 20 percent. Your share determines how much of the local stock you can buy.",
        "Preserve Ceuta, the original FO substitution and the exact 20 percent without implying company ownership. Clean Help150 explains that share limits the purchasable fraction of specialty arrivals, while even 1 percent permits unlimited selling. Specify buying to convey the intended mechanic naturally and avoid the older Trade within that share suggesting a sales-volume cap. This does not add a stock formula, guaranteed supply, profit or new sales rule to the panel. Use percent, not an unsafe ASCII printf conversion."),
    58:('revision',"If there's anything you want to sell, go ahead.",
        "Restore the conditional personal choice in Julio's invitation. The older Have goods to sell? Sell them now changes want to sell into possession and adds urgency. Do not imply liquidation of all cargo or a deadline."),
    61:('retention',"All right.",
        "Rafael's brief, cooperative assent works naturally after the optional invitation. It accepts the advice without claiming a completed sale, profit or subsequent transaction."),
}
if __name__=='__main__':
    assert not ROOT.exists() and not MANUSCRIPT.exists() and not NAMES.exists()
    current,effective,names,controls,city,town=map(read,[CURRENT,EFFECTIVE,NATIVE_NAMES,CONTROLS,CITY_HELP,TOWN])
    assert effective['source_packet_sha256']==sha(CURRENT.read_bytes()) and effective['native_names_packet_sha256']==sha(NATIVE_NAMES.read_bytes())
    assert len(effective['source_current_dispatches'])==24 and effective['one_FE_original_null_actor_macro_call_expands_source_FO']
    clean=NdsImage.open('work/clean.nds');help_bytes=clean.read_file('/COMMON/HELP.DK4');blocks=IlnkContainer.parse(help_bytes).blocks
    share=next(r for r in city['records'] if r['topic_id']==150)
    assert sha(help_bytes)==city['source_clean_HELP_sha256'] and blocks[150].hex()==share['clean_source_hex']
    assert '売却は１％のシェアで、無制限に行えます。' in share['source_Japanese_with_link_IDs']
    terminology=next(r for r in town['records'] if r['id']=='COMMON_MESSAGE_654')
    assert 'Market matches the existing facility label' in terminology['localization_note']
    rows=[]
    for original in current['records']:
        row=deepcopy(original);decision,english,note=DECISIONS[row['source_record_index']]
        predecessor=next(r for r in effective['effective_current_records'] if r['id']==row['id'])
        if decision=='retention':assert english==predecessor['effective_predecessor_paragraph']
        else:assert english!=predecessor['effective_predecessor_paragraph']
        source_body=bytes.fromhex(row['source_hex'])[1:]
        assert english==english.strip() and '  ' not in english and not any(c in english for c in ['\n','\r','{','}','%'])
        assert {m:source_body.count(m.encode()) for m in ['FI','FA','FO']}=={m:english.count(m) for m in ['FI','FA','FO']}
        row.update(route=0,route_identity='Rafael',speaker={0:'Rafael',6:'Julio',254:'System information panel'}[row['source_selector']],
            english=english,source_meaning=row['fresh_clean_source_gloss'],context=row['full_source_exchange_context'],
            context_scope='Complete clean/source exchange, original own-captain0 names and dispatch; conditional source FE branch; natural activation/location unproved',
            localization_note=note,editorial_finding=note,decision=decision,editorial_decision='retain-wording' if decision=='retention' else 'revise-wording',
            retention_reason=note if decision=='retention' else None,current_effective_paragraph=predecessor['effective_predecessor_paragraph'],
            current_effective_runtime_template_hex=predecessor['effective_predecessor_template_hex'],
            current_expanded_runtime_hex=predecessor['current_actual_default_expanded_hex'],
            current_registered_catalogue_match=predecessor['registered_catalogue_match'],
            current_effective_body_dispatch_andcatalogue_pending=False,
            source_voice_class=None if row['source_selector']==254 else {0:2,6:5}[row['source_selector']],
            whole_exchange_situation_voice_andprogression_reviewed=True,exact_source_macros_preserved=True,
            review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False),
            native_font_wrapping_reference_actual_policy_andregistered_release_pending=True,new_credit=0)
        rows.append(row)
    assert len(rows)==12 and Counter(r['decision'] for r in rows)=={'revision':7,'retention':5}
    scoped_names=[]
    for r in names['naming_retentions']:
        scoped_names.append(dict(**r,decision='retention-in-this-exchange',
            clean_current_fields=next(n for n in names['complete_clean_andcurrent_name_fields'] if n['actor_ID']==r['actor_ID']),
            original_getters=[n for n in names['native_four_progressive_andfull_getters']['rows'] if n['actor_ID']==r['actor_ID']],
            source_speech_keys=[dict(file_path=r['file_path'],id=r['id']) for r in rows if r['source_selector']==r['actor_ID']],
            name_asset_changed=False,actual_B45_headers_andother_consumer_UI_pending=True,new_credit=0))
    save(NAMES,dict(format='dk4-contextual-speaker-name-review-v1',records=scoped_names,
        native_proof=str(NATIVE_NAMES),native_proof_sha256=sha(NATIVE_NAMES.read_bytes()),
        FE_is_separate_display_selector_not_actor254=True,two_scoped_retentions_not_full207_name_approval=True,
        full207_name_role_alias_review_active=True,new_credit=0,full_goal_complete=False))
    save(MANUSCRIPT,dict(format='dk4-whole-exchange-editorial-manuscript-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=['source','context','localization','naturalness','formatting'],
        file_path=current['file_path'],route=0,route_identity='Rafael',block=45,current_ROM=current['current_ROM'],
        current_ROM_sha256=current['current_ROM_sha256'],current_ARM9_sha256=current['current_ARM9_sha256'],current_COMMON_sha256=current['current_COMMON_sha256'],
        records=rows,source_current_packet=str(CURRENT),effective_packet=str(EFFECTIVE),names_packet=str(NAMES),source_controls_packet=str(CONTROLS),
        complete_clean_glosses_precede_current_comparison=True,all12_current_effective_templates_reviewed=True,
        source_macro_counts=dict(FI=0,FA=0,FO=1),all12_formatting_gates_false=True,formatting_review_pending=True,
        one_FE_market_share_panel_needs_distinct_native_consumer_percent_macro_bounds_andactual_checks=True,
        clean_Help150_mechanics_binding=dict(file_path='/COMMON/HELP.DK4',block=150,source_HELP_sha256=sha(help_bytes),
            source_hex=blocks[150].hex(),source_Japanese=share['source_Japanese_with_link_IDs'],reviewed_English=share['english'],
            relevance='Share limits purchases of local stock; no implication of a proportional selling cap',
            not_new_review_credit_oractual_mechanic_activation=True),
        facility_term_binding=dict(reviewed_record='COMMON_MESSAGE_654',packet=str(TOWN),sha256=sha(TOWN.read_bytes()),
            Japanese=terminology['japanese'],English=terminology['english'],note=terminology['localization_note'],
            existing_B45_effective_facility_word='Market',no_new_UI_capture_claim=True),
        no_explicit_EV0_dependencies_not_proof_ofnatural_activation_orimmediate_B44_chronology=True,
        no_invented_family_rank_fee_amount_deadline_profit_ownership_orcompleted_sale=True,
        no_manual_break_padding_alignment_orprose_abbreviation_authored=True,
        ordinary_captain0_context_no_unlock_orstate_fixture=True,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,EFFECTIVE,NATIVE_NAMES,CONTROLS,CITY_HELP,TOWN,NAMES,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    ROOT.mkdir(parents=True);save(ROOT/'twelve_contextual_decisions7_revisions5_retentions.json',dict(
        manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),names=str(NAMES),names_sha256=sha(NAMES.read_bytes()),
        revisions=7,retentions=5,two_scoped_name_retentions=True,source_macro_counts=dict(FI=0,FA=0,FO=1),
        all12_formatting_false=True,conditional_FE_separate=True,
        native_layout_fonts_stored_controls_actual_production_andregistered_release_pending=True,new_credit=0,full_goal_complete=False))
    print('Rafael B45:7 revisions/5 justified retentions;2 scoped name retentions;clean Help150 prevents an invented sales-volume cap. All formatting/release gates pending;zero credit.')
