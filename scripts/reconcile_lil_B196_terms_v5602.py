"""Bind source names,Charm,gold,FI and six prices without naming the offered item."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B196_terms_v5602')
SOURCE=Path('work/analysis/lil_B196_source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json')
NAMES=Path('work/analysis/lil_B196_source_names_v5598/six_source_name_fields_twelve_current_consumers_and_literal_scope.json')
FUNDS=Path('work/analysis/lil_B196_funds_v5601b/six_exact_source_prices_six_unforced_and_thirty_offline_payment_boundaries.json')
ROLES={'2':'Lil Argot','6':'Julio Erneco','19':'Carlo Sinat','20':'Fernando Dias','25':'Yifa Sol','173':'Suspicious Person'}
if __name__=='__main__':
    assert not ROOT.exists();packet,names,funds=map(read,[SOURCE,NAMES,FUNDS])
    assert names['source_context_sha256']==funds['source_context_sha256']==sha(SOURCE.read_bytes())
    assert funds['six_source_prices_match_six_exact_native_payment_amounts'] and len(funds['cases'])==36
    assert funds['native_payment_saturates_at_zero_not_a_proof_of_purchase_affordability_or_outer_eligibility']
    assert names['source_person173_first_field_is_gender_neutral_ayashii_hito']
    current,clean=[NdsImage.open(p) for p in [packet['current_ROM'],'work/clean.nds']]
    arm,jp=current.read_file('/__arm9__.bin'),clean.read_file('/__arm9__.bin')
    stat=next(r for r in read('translations/deck_view_arm9_v2.json')['records'] if r['id']=='DK4_STAT_CHARM_V2')
    at=stat['offset'];raw=bytes.fromhex(stat['source_hex']);assert jp[at:at+len(raw)]==raw
    assert raw.split(b'\0')[0].decode('cp932')=='魅力' and stat['english']=='Charm'
    value=arm[at:at+len(raw)];assert value.split(b'\0')[0]==b'Charm'
    prior=read('translations/lil_B142_B145_contextual_final_review_v1.json')
    money=next(r for r in prior['records'] if r['id']=='DK4_MES_B142_R0054')
    assert '金９０００００' in money['source_Japanese'] and money['english']=='{SPEAKER:02}Then take the 900,000 gold you need.'
    fe=next(r for r in packet['records'] if r['source_selector']==254)
    source_body=bytes.fromhex(fe['source_hex'])[1:];assert source_body.decode('cp932')=='FIの魅力が１上がりました！'
    assert packet['source_macro_counts']==dict(FI=1,FA=0,FO=0)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B196_voices_v5591/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    pipelines=[]
    for label,body in [('source-Japanese-notice',source_body),('isolated-original-FI-token',b'FI')]:
        pipelines.append(dict(kind=label,**ctx.execute(expand,body)));ctx.machines.pop()
    assert len(pipelines)==2 and sum(len(r['cases']) for r in pipelines)==8 and not ctx.machines
    assert all(bytes.fromhex(c['output_hex'])==b'Lil' for c in pipelines[1]['cases'])
    by={r['source_record_index']:r for r in packet['records']}
    fragments={5:['金','持ってそう','イッヒ'],8:['…'],12:['いいもん','２０００００'],24:['ふっかけ'],42:['太っ腹','きっと役に立つ'],
        45:['FI','魅力','１上が'],62:['１０００００'],74:['提督','１回','半額','あと２回','値切'],92:['さすが','きっと役に立つ'],
        107:['７００００'],118:['俺なら','もう１回'],136:['これだよ','きっと役に立つ'],152:['意外とがめつい','５００００'],
        170:['わしなら','もう１回','ねば'],178:['もっとまけ'],197:['なかなかのやり手','品物'],212:['４００００','………','イヒ'],
        223:['ここら','買い時','かね'],242:['買わないのかと思った','こいつ'],257:['頼むから','３００００'],268:['これ以上','下がらん','じゃろう'],
        287:['安く売っちまった','大事'],302:['見る目がなかったみたい'],306:['別の人に売る','もういい']}
    assert set(fragments)==set(by)
    for index,parts in fragments.items():assert all(p in by[index]['source_Japanese'] for p in parts),index
    choices=packet['typed_choice_records'];assert len(choices)==12
    assert all(r['source_Japanese']==['買う','買わない'][r['option_index']] for r in choices)
    save(ROOT/'six_roles_gold_Charm_FI_and_six_prices_without_invented_item_identity.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        approved_prose_names=ROLES,current_native_name_values=names['current_progressive_and_full_catalogue_values'],
        source_name_fields=names['source_name_fields'],original_voice_classes=names['current_native_voice_classes'],
        stat_term=dict(source='魅力',English='Charm',registered_record_ID=stat['id'],fixed_owned_offset=at,
            clean_complete_slot_hex=raw.hex(),current_complete_slot_hex=value.hex(),not_a_new_stat_widget_execution_or_fidelity_credit=True),
        money_term='gold',gold_approved_prior_record=dict(id=money['id'],source_Japanese=money['source_Japanese'],english=money['english']),
        source_FI_record=fe['id'],current_default_captain_ID=2,current_source_FI_expansion='Lil',native_FE_macro_pipelines=pipelines,
        source_owned_FI_adapter=inspect.getsource(expand),source_FI_macro_retained_not_replaced_by_literal_Lil=True,
        four_alignments_each_source_notice_and_isolated_token_preserve_all4MiB_ABI_and_canaries=True,
        custom_player_names_actual_B196_FE_rendering_and_new_UI_glyph_credit_not_claimed=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_price_ladder=list(funds['source_packed_payment_amounts'].values()),source_financial_context=str(FUNDS),source_financial_context_sha256=sha(FUNDS.read_bytes()),
        source_six_choice_labels_literal_buy_or_not_buy_not_an_invented_haggle_command=True,
        source_unnamed_item_and_picture_descriptor_not_used_to_invent_a_spoken_item_name=True,
        source_one_early_FI_Charm_plus1_notice_not_applied_to_all_six_purchases=True,
        source_cackling_pitch_skepticism_halving_at_least_two_more_advice_one_more_opinions_pleading_regret_and_dismissal_preserved=True,
        source_seller_usefulness_certainty_and_buying_floor_advice_remain_character_claims=True,
        source_R302_elliptical_judgment_requires_explicit_whole_exchange_editorial_interpretation=True,
        source_R306_future_sale_to_another_person_not_a_completed_other_sale=True,
        source_gender_neutral_person173_and_original_actor_voices_without_invented_kinship_rank_or_employment=True,
        source_Carlo_Admiral_address_explicit_no_new_title_elsewhere=True,
        current_Fernando_fullwidth_leading_F_and_unconsumed_person173_secondary_field_not_silently_renamed_or_promoted_to_fact=True,
        all24_clean_first_glosses_and12_choice_glosses_precede_predecessor_prose_comparison=True,
        raw_current_structural_hex_and_native_name_or_label_getters_are_evidence_not_translation_source=True,
        source_item_acquisition_Charm_effect_body_outer_eligibility_and_actual_transactions_not_claimed=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,FUNDS,Path('translations/deck_view_arm9_v2.json'),
            Path('translations/lil_B142_B145_contextual_final_review_v1.json'),Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B196 six roles,gold,Charm,source FI->current Lil across8 native alignment cases,and all six payment amounts bound. Keep FI,unnamed item,personal claims,price branches and literal choices;zero credit.')
