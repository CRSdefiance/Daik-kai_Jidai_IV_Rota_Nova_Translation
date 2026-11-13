"""Compare existing English only after clean glosses,both complete source paths and six sheets."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_comparison_v5915')
SOURCE=Path('work/analysis/lil_B201_source_v5902/all26_clean_current_complete_context_with_two_choice_labels.json')
GLOSS=Path('work/analysis/lil_B201_clean_context_v5901/all24_clean_rigging_price_negotiation_purchase_refusal_and_three_stat_glosses.json')
ACTUAL=Path('work/analysis/lil_B201_source_paths_v5914/two_actual_source_choice_paths_all24_speeches_all53_commands_and_returns.json')
DISPATCH=Path('work/analysis/lil_B201_dispatches_v5904/all24_source_current_dispatches_two_FI_and15_control_leaves.json')
NAMES=Path('work/analysis/lil_B201_names_v5907/six_original_progressive_and_catalogue_name_consumers.json')
CONTROLS=Path('work/analysis/lil_B201_controls_v5908/fifteen_exact_leaves_three_resources_two6003_picture_eight_structural_pairs_and_complete_end.json')
FUNDS=Path('work/analysis/lil_B201_funds_v5912/one_exact100000_source_price_one_unforced_and_five_offline_payment_boundaries.json')
TERMS=Path('guide/research/player-terminology-reference.json')

if __name__=='__main__':
    assert not ROOT.exists();packet,gloss,actual,dispatch,names,controls,funds=map(read,[SOURCE,GLOSS,ACTUAL,DISPATCH,NAMES,CONTROLS,FUNDS])
    assert gloss['prior_English_speech_unread'] and len(gloss['records'])==24
    assert actual['source_distinct_speech_observations']==24 and actual['total_speech_observations']==37 and not actual['unvisited_source_indices']
    assert actual['all44_source_commands_and9_original_initializers_observed_over_two_paths']
    assert [(r['path'],r['actual_choice_result'],r['exit_frame']) for r in actual['versions']]==[('buy',[2,0],7895),('decline',[2,1],7416)]
    assert len(controls['all15_source_current_nonrelative_nonspeech_nonchoice_leaves'])==15
    assert funds['source100000_price_matches_exact_native_payment_amount'] and len(funds['cases'])==6
    assert names['progressive_nameplate_values']==names['full_catalogue_values']=={'2':'Lil Argot','19':'Carlo Sinat','105':'Trader'}
    sheets=actual['review_sheets']+actual['transition_sheets'];assert len(sheets)==6
    for row in sheets:assert sha(Path(row['path']).read_bytes())==row['sha256']
    arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');fields=[]
    for ident in [2,19,105]:
        parts=[]
        for delta in [0,4,8]:
            field=0x120B80+ident*32+delta;p=struct.unpack_from('<I',arm,field)[0]
            if p:
                at=p-0x02000000;raw=arm[at:arm.index(b'\0',at)+1]
                parts.append(dict(pointer_field=field,pointer=p,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
            else:parts.append(dict(pointer_field=field,null=True))
        fields.append(dict(actor_ID=ident,source_fields=parts))
    assert [[p.get('Japanese') for p in r['source_fields']] for r in fields]==[['リル','アーゴット',None],['カルロ','シナート',None],['交易所の親父','イスラム',None]]
    terms=read(TERMS);selected=[]
    for jp,en in [('魅力','Charm'),('知力','Wits'),('精神','Spirit')]:
        r=next(r for r in terms if r['japanese']==jp and r['english']==en);selected.append(dict(**r,exact_reference=f'{TERMS}#/item/{terms.index(r)}'))
    assert 'permanent Spirit' in next(r for r in terms if r['japanese']=='精神' and r['english']=='Mood')['explanation']
    bp=Path(dispatch['registered_catalog_binding']);binding=read(bp);assert sha(bp.read_bytes())==dispatch['registered_catalog_binding_sha256']
    rows=[];matches=[]
    for r in packet['records']:
        raw=bytes.fromhex(r['current_hex']);current=next(x for x in dispatch['speech_dispatch_cases'] if x['id']==r['id'] and x['version']=='current-English')
        match=current['registered_catalog_match'];body=raw[1:].decode('cp932');effective=body;entry=None
        if match is not None:
            entry=binding['records'][match['table_index']];assert entry['key_hex']==raw[1:].hex() and entry['route_mask']&4
            assert dict(owner=['/data/SC2.DK4',r['id']],form='body') in entry['requests']
            effective=bytes.fromhex(entry['target_hex']).decode('cp932');matches.append(r['id'])
        expanded=effective.replace('FI','Lil').replace('FA','Argot').replace('FO','Argot Co.')
        assert current['boundaries'][1]['text_hex']==expanded.encode('cp932').hex()
        observations=[dict(path=v['path'],**o) for v in actual['versions'] for o in v['speech_observations'] if o['id']==r['id']]
        assert observations and all(o['selected_capture'] for o in observations)
        row=deepcopy(r);row.update(previous_raw_storage_body=body,previous_effective_template_body=effective,previous_registered_catalog_match=match,
            previous_registered_catalog_entry=entry,previous_display_body=effective,previous_paragraph=' '.join(effective.split()),
            previous_macro_template_paragraph=' '.join(effective.split()),previous_effective_runtime_paragraph=' '.join(expanded.split()),
            actual_source_fixture_observed=True,actual_source_paths=[o['path'] for o in observations],source_actual_observations=observations,
            clean_first_whole_exchange_gloss_and_actual_source_scenes_precede_English_comparison=True,prior_English_comparison_only_not_translation_source=True)
        rows.append(row)
    choices=[]
    for r in packet['typed_choice_records']:
        row=deepcopy(r);row.update(previous_paragraph=bytes.fromhex(r['current_hex']).decode('cp932'),
            actual_source_menu_outcomes_observed=[0,1],clean_original_labels_and_gloss_precede_existing_English=True)
        choices.append(row)
    ROOT.mkdir(parents=True);context=ROOT/'complete_clean_context_source_paths_three_names_prices_stat_terms_and_item_scope.json'
    evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,ACTUAL,DISPATCH,NAMES,CONTROLS,FUNDS,TERMS,bp,Path(__file__)]}
    save(context,dict(source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),complete_exchange_progression=gloss['whole_exchange_progression'],
        approved_prose_names={'2':'Lil','19':'Carlo','105':'Trader'},source_name_fields=fields,
        native_source_voices={'2':3,'19':7,'105':0},source_FI_FA_FO_counts=packet['source_macro_counts'],
        source_Trader_role_retention=dict(actor_ID=105,current='Trader',decision='retain-wording',
            reason='Clean primary交易所の親父 identifies the familiar trade-house vendor;Trader is natural and identifies the occupation in this complete sale without pretending to be a personal name. 親父 here is familiar address,not fatherhood. Keep the unused secondaryイスラム as exact metadata without adding religion,nationality or biography to the displayed label.',
            existing_two_original_consumers_and_actual_source_nameplate_bound=True,no_name_bytes_changed_or_duplicate_review_credit=True,
            other105_contexts_and_all207_name_queue_not_globally_closed=True),
        approved_stat_terms=selected,source_FE_notices=[dict(index=77,recipient='runtime FI',stat='Charm',increment=1),dict(index=80,recipient='Carlo',stat='Wits',increment=1),dict(index=100,recipient='runtime FI',stat='Spirit',increment=1)],
        Spirit_is_permanent_fortitude_notice_not_current_Mood_condition=True,
        all_seven_price_turns=gloss['seller_asks_and_counteroffers'],final_native_payment=100000,
        source_native_payment_saturates_at_zero_not_affordability_or_outer_eligibility_proof=True,
        original_fixture_funds35000_and_buy_town_zero_decline_town35000_visually_observed=True,
        source_menu_Buy_decline_order_0_1_both_observed_no_delegation=True,
        seller_mysterious_power_and_uniqueness_remain_reported_claims_not_new_item_lore=True,
        item_card_observed=['Tireless Hawser','Equipment','Sail Handle'],spoken_item_stays_unnamed_no_new_item_title_widget_or_full_effect_fidelity_credit=True,
        original_item_card_clears_before_delivery_or_decline_and_all_three_FE_portrait_name_regions_clear=True,
        buy_after_scene_returns_to_town_then_B120_black_upper_dialogue_still_active_at12970=True,
        decline_after_scene_returns_to_town_then_B120_and_SeaView_by12970=True,
        following_B120_is_not_reviewed_or_counted_again=True,
        source_actual_speeches=24,source_speech_observations=37,offline_only_speeches=[],viewed_source_sheets=sheets,
        actual_new_source_cold_boots=2,total_source_frames=26002,
        initialized_Amsterdam_B22_not_natural_event201_activation_original_location_earned_purchase_full_route_or_hardware=True,
        original_conditions_roster_funds_RNG_effect_results_unforced=True,all_source_and_earlier_evidence_preserved=True,
        no_new_ROM_or_run_beyond_recorded_source_fixture=True,new_review_credit=0,evidence=evidence,full_goal_complete=False))
    save(ROOT/'all26_complete_clean_and_predecessor_exchange_including_two_choices.json',dict(
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),records=rows,typed_choice_records=choices,
        contextual_reconciliation=str(context),contextual_reconciliation_sha256=sha(context.read_bytes()),current_registered_catalog_matches=len(matches),
        current_registered_catalog_matched_IDs=matches,all24_clean_glosses_and_two_label_glosses_precede_previous_English=True,
        source_old_English_stored_native_runtime_and_logical_references_exact=True,no_new_editorial_or_name_completion_credit=True,
        evidence=evidence,full_goal_complete=False))
    for r in rows:print(r['source_record_index'],r['previous_paragraph'])
    print('MENU',[(r['option_index'],r['previous_paragraph']) for r in choices]);print('B20126 comparison objects after allsix source sheets viewed;no credit.')
