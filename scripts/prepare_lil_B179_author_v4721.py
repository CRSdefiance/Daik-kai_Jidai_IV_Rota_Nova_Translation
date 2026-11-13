"""Prepare fourteen source-contextual decisions with separate city-alias scope retained."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_author_tools_v4721');assert not ROOT.exists()
tool=derive('scripts/author_lil_B178_v4672.py','scripts/author_lil_B179_v4721.py',{
    'lil_B178_prose_v4671':'lil_B179_prose_v4720','lil_B178_author_v4672':'lil_B179_author_v4721',
    'lil_B178_comparison_v4670/all13':'lil_B179_comparison_v4719/all14',
    'lil_B178_clean_context_v4661/all13_complete_B178':'lil_B179_clean_context_v4707/all14_complete_B179',
    'lil_B178_editorial_manuscript_v1':'lil_B179_editorial_manuscript_v1',
    'lil_B178_voices_v4663':'lil_B179_voices_v4709','lil_B178_branches_v4665':'lil_B179_branches_v4711',
    'lil_B178_entry_v4666/source_EV2_B178':'lil_B179_entry_v4712/source_EV2_B179',
    'lil_B178_controls_v4668/one_A000_C200_single_end_and3_source_leaves':
        'lil_B179_controls_v4714/one_A000_no_C200_single_end_and2_source_leaves',
    'lil_B178_names_v4667b/six_original_Lady166_167_168_name_consumers_readonly_paths':
        'lil_B179_names_v4713b/six_original_Barkeep_Patron_Retainer_name_consumers',
    'len(prose.REVISIONS)==2 and len(prose.RETAIN_NOTES)==11':'len(prose.REVISIONS)==8 and len(prose.RETAIN_NOTES)==6',
    "{166:'Lady',167:'Lady',168:'Lady',254:'Impersonal fashion notice'}":"{92:'Barkeep',96:'Patron',152:'Sailor',254:'Impersonal fashion notice'}",
    "counts=={'revise':2,'retain-wording':11}":"counts=={'revise':8,'retain-wording':6}",
    'len(rows)==13':'len(rows)==14','records=rows,revised=2,retained=11':'records=rows,revised=8,retained=6',
    'all13':'all14','all11_retentions':'all6_retentions','Record all13 B178':'Record all14 B179',
    'three_Lady_native_names_bound_and_FE_notice_impersonal':'Barkeep_Patron_Sailor_dialogue_names_bound_distinct_catalogue_Retainer_and_FE_impersonal',
    'Amsterdam_two_inline_city_spans_and_Wheat_source_current_pointers_bound':'Sao_Jorge20_byte_owned_city_span_and_Wine_pointer_bound_separate_Japanese_alias_lead_open',
    'home_baking_enthusiasm_husband_example_curiosity_bakery_boast_offer_pleased_reply_ingredient_question_first_wheat_and_forecast_preserved':
        'challenge_concession_repeated_taste_questions_hyperbole_trial_order_service_three_gulps_verdict_repeat_joining_order_and_forecast_preserved',
    'no_added_rank_kinship_recipe_quantities_prices_completed_purchase_or_earned_boom_exact_speaker_assignments_preserved':
        'no_invented_prior_drink_brand_drunkenness_rank_master_relationship_price_completed_sale_or_earned_boom',
    'objects=13,progressive=12':'objects=14,progressive=13',
    "    doc.update(manuscript_kind='speech'":
        "    terms=read(comparison['terms_binding'])\n    doc.update(separate_untranslated_city_alias_lead=terms['separate_untranslated_city_alias_lead'],separate_untranslated_city_alias_lead_sha256=terms['separate_untranslated_city_alias_lead_sha256'])\n    doc.update(manuscript_kind='speech'",
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,revisions=8,justified_retentions=6,
    six_current_Sailor_records_still_Japanese_to_be_translated=True,no_cause_for_historical_omission_inferred=True,
    separate_untranslated_city_alias_lead_must_be_preserved=True,formatting_native_actual_reference_and_release_pending=True,
    no_ROM_registry_ledger_orreview_credit=True,full_goal_complete=False))
