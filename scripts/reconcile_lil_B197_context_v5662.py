"""Reconcile clean-first glosses with observed original menu paths before English comparison."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_context_v5662')
SOURCE=Path('work/analysis/lil_B197_source_v5647/all24_clean_current_complete_context_with_three_choice_labels.json')
ACTUAL=Path('work/analysis/lil_B197_source_paths_v5661/three_actual_source_menu_paths_and_original_response_intervals.json')
NAMES=Path('work/analysis/lil_B197_source_names_v5653/two_source_name_fields_four_current_consumers_and_literal_scope.json')
FUNDS=Path('work/analysis/lil_B197_funds_v5660/one_exact8500_source_price_one_unforced_and_five_offline_payment_boundaries.json')
PROGRESSION=("The Alluring Woman calls Ian handsome and offers him a book for 8,500 gold. Ian asks what kind; she describes an Indian classic about the love of a celestial maiden and a sage, then asks whether he wants it. Ian asks the Admiral to decide. Buying leads to Ian's acceptance, her teasing hope that he too will find love with a celestial maiden, his lack of interest in romance, and her playful disappointment. Refusing leads to Ian's polite decline and her intention to sell elsewhere. Delegating leads to Ian's personal inability to afford the book and considerate apology; she gives it to him, surprises him and wishes for a future romance with a man like him. Ian reports her disappearance, wonders whether she was a celestial maiden, then dismisses his own thought. The original common tail displays Ian's Charm plus one after all three choices. Her supernatural identity remains unconfirmed.")

if __name__=='__main__':
    assert not ROOT.exists()
    packet,actual,names,funds=map(read,[SOURCE,ACTUAL,NAMES,FUNDS])
    gp=Path(packet['whole_exchange_context_notes']);gloss=read(gp)
    assert gloss['read_no_predecessor_English'] and len(gloss['records'])==21 and len(gloss['choices'])==1
    assert names['source_context_sha256']==funds['source_context_sha256']==sha(SOURCE.read_bytes())
    assert funds['source8500_price_matches_exact_native_payment_amount'] and len(funds['cases'])==6
    expected={'buy':[5,9,14,17,21,24,45,49,53,57,109],
              'no_buy':[5,9,14,17,21,24,64,68,109],
              'delegate':[5,9,14,17,21,24,74,77,81,85,89,93,97,101,109]}
    for option,v in enumerate(actual['versions']):
        assert v['actual_choice_result']==[2,option]
        assert v['selected_source_speech_indices']==expected[v['path']]
        assert v['source_FE_Ian_Charm_notice_selected']
    assert actual['total_frames']==39003 and len(actual['source_unique_speech_indices'])==21
    assert len(actual['review_sheets'])==6
    for sheet in actual['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    rows=deepcopy(gloss['records'])
    for r in rows:
        n=r['source_record_index'];r['actual_source_paths']=[p for p,indices in expected.items() if n in indices]
        if n==53:
            r['prior_gloss_reference']=dict(path=str(gp),record_index=53,previous_note=r['whole_exchange_note'])
            r['whole_exchange_note']="Ian has accepted the book at R45. This reply answers the woman's romantic wish at R49, not the sale. Preserve his courteous, dry disinterest in romance. The older note's book-refusal interpretation is superseded by the complete actual purchase exchange."
        if n==64:r['whole_exchange_note']="This is the book refusal, selected by option 1. Keep the polite decline distinct from R53's romantic disinterest and R74's personal lack of money."
        if n==74:r['whole_exchange_note']="Option 2 delegates the decision to Ian. He says he personally lacks that much money. The unchanged opening company funds are not an inferred affordability gate; do not add debt,poverty,a failed company purchase or a request for charity."
        if n==109:r['whole_exchange_note']="All three original menu paths reach this common FE notice. It explicitly names Ian and Charm plus one without FI. This is observed notice ownership,not execution proof of the Charm effect body's complete mechanics."
    current,clean=[NdsImage.open(p) for p in [packet['current_ROM'],'work/clean.nds']]
    arm,jp=[im.read_file('/__arm9__.bin') for im in [current,clean]]
    stat=next(r for r in read('translations/deck_view_arm9_v2.json')['records'] if r['id']=='DK4_STAT_CHARM_V2')
    at=stat['offset'];raw=bytes.fromhex(stat['source_hex']);value=arm[at:at+len(raw)]
    assert jp[at:at+len(raw)]==raw and raw.split(b'\0')[0].decode('cp932')=='魅力'
    assert stat['english']=='Charm' and value.split(b'\0')[0]==b'Charm'
    money=next(r for r in read('translations/lil_B142_B145_contextual_final_review_v1.json')['records'] if r['id']=='DK4_MES_B142_R0054')
    assert '金９０００００' in money['source_Japanese'] and money['english']=='{SPEAKER:02}Then take the 900,000 gold you need.'
    ROOT.mkdir(parents=True)
    save(ROOT/'clean_first_context_original_three_paths_gold_and_Charm.json',dict(
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        historical_clean_gloss=str(gp),historical_clean_gloss_sha256=sha(gp.read_bytes()),
        corrected_contextual_gloss_records=rows,complete_exchange_progression=PROGRESSION,
        approved_prose_names={'21':'Ian Dukov','169':'Alluring Woman'},
        source_name_fields=names['source_name_fields'],original_voice_classes=names['current_native_voice_classes'],
        current_native_name_values=names['current_progressive_and_full_catalogue_values'],
        money_term='gold',gold_approved_prior_record=dict(id=money['id'],source_Japanese=money['source_Japanese'],english=money['english']),
        stat_term=dict(source='魅力',English='Charm',registered_record_ID=stat['id'],fixed_owned_offset=at,clean_complete_slot_hex=raw.hex(),current_complete_slot_hex=value.hex()),
        source_financial_context=str(FUNDS),source_financial_context_sha256=sha(FUNDS.read_bytes()),
        exact_native_payment_amount=8500,payment_body_test_is_offline_not_earned_affordability=True,
        source_actual_paths=str(ACTUAL),source_actual_paths_sha256=sha(ACTUAL.read_bytes()),actual_source_speech_paths=expected,
        actual_original_source_cold_boots=3,actual_source_frames=39003,source_speech_observations=35,distinct_source_speeches_observed=21,
        viewed_six_source_contact_sheets_original_detail=actual['review_sheets'],
        source_purchase_R53_answers_R49_romance_after_R45_acceptance_not_book_refusal=True,
        source_delegated_gift_not_inferred_from_company_funds=True,
        source_FE_R109_common_tail_observed_after_all_three_choices=True,
        source_item_card_observed_text=['Shakuntala','Gift','—'],
        item_card_is_existing_UI_not_permission_to_add_title_to_unnamed_seller_prose_or_new_widget_fidelity_credit=True,
        cultural_translation='Indian classic about the love of a celestial maiden and a sage; no new title,author,religion or Western angel/wizard identity in spoken prose',
        selected_source_still_portrait_name_absences={'no_buy':[9,14,17,21],'delegate':[21]},
        selected_source_still_portraits_restore_at_R24_and_absence_cause_not_established=True,
        source_no_buy_FE_keeps_book_card_buy_and_delegate_FE_clear_it=True,
        disappearance_reported_in_dialogue_no_distinct_animation_or_supernatural_identity_certified=True,
        all39_source_commands_plus9_original_initializers_retained=True,
        source_B22_fixture_not_natural_event197_activation_or_original_scene_location=True,
        ordinary_input_only_no_funds_roster_RNG_predicate_or_effect_forcing=True,
        source_screens_not_a_complete_target_English_native_glyph_or_pagination_or_portrait_acceptance=True,
        source_opaque_item_Charm_6003_resource_bodies_and_outer_eligibility_not_fully_executed_offline=True,
        all_clean_first_glosses_and_original_actual_context_precede_predecessor_speech_comparison=True,
        historical_gloss_files_and_5656_handoff_preserved_contextual_interpretations_superseded_here=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,gp,ACTUAL,NAMES,FUNDS,Path('translations/deck_view_arm9_v2.json'),Path('translations/lil_B142_B145_contextual_final_review_v1.json'),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B197 contextual reconciliation:purchase romance reply,delegated gift,common Ian Charm notice;21 corrected-context glosses,8500 gold,6 viewed source sheets. No old-English comparison yet;zero credit.')
