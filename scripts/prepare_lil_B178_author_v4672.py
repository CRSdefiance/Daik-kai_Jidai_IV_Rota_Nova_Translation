"""Prepare thirteen contextual decisions with formatting and integration gates open."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_author_tools_v4672')
assert not ROOT.exists()
tool=derive('scripts/author_lil_B177_v4612.py','scripts/author_lil_B178_v4672.py',{
    'lil_B177_prose_v4611':'lil_B178_prose_v4671','lil_B177_author_v4612':'lil_B178_author_v4672',
    'lil_B177_comparison_v4610/all10':'lil_B178_comparison_v4670/all13',
    'lil_B177_clean_context_v4601/all10_complete_B177':'lil_B178_clean_context_v4661/all13_complete_B178',
    'lil_B177_editorial_manuscript_v1':'lil_B178_editorial_manuscript_v1',
    'lil_B177_voices_v4603/current2':'lil_B178_voices_v4663/current3',
    'lil_B177_branches_v4605':'lil_B178_branches_v4665',
    'lil_B177_entry_v4606/source_EV2_B177':'lil_B178_entry_v4666/source_EV2_B178',
    'lil_B177_controls_v4608':'lil_B178_controls_v4668',
    'lil_B177_names_v4607/four_original_Owner_Cook':'lil_B178_names_v4667b/six_original_Lady166_167_168',
    'len(prose.REVISIONS)==5 and len(prose.RETAIN_NOTES)==5':'len(prose.REVISIONS)==2 and len(prose.RETAIN_NOTES)==11',
    "{174:'Owner',175:'Cook',254:'Impersonal fashion notice'}":"{166:'Lady',167:'Lady',168:'Lady',254:'Impersonal fashion notice'}",
    "counts=={'revise':5,'retain-wording':5}":"counts=={'revise':2,'retain-wording':11}",
    'len(rows)==10':'len(rows)==13','records=rows,revised=5,retained=5':'records=rows,revised=2,retained=11',
    'all10':'all13','all5_retentions':'all11_retentions','Record all10 B177':'Record all13 B178',
    'Owner_Cook_native_names_bound_and_FE_notice_impersonal':'three_Lady_native_names_bound_and_FE_notice_impersonal',
    'Genoa_two_inline_city_spans_and_unchanged_source_pointers_bound':'Amsterdam_two_inline_city_spans_and_Wheat_source_current_pointers_bound',
    'enthusiasm_color_skepticism_passion_reminiscence_detached_reply_cook_sell_order_offhand_reply_grand_laugh_and_forecast_preserved':
        'home_baking_enthusiasm_husband_example_curiosity_bakery_boast_offer_pleased_reply_ingredient_question_first_wheat_and_forecast_preserved',
    'no_added_lover_present_relationship_madam_rank_quantity_price_completed_sale_or_earned_boom':
        'no_added_rank_kinship_recipe_quantities_prices_completed_purchase_or_earned_boom_exact_speaker_assignments_preserved',
    'objects=10,progressive=9':'objects=13,progressive=12',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,expected_revisions=2,expected_retentions=11,
    no_ROM_registry_ledger_orreview_credit=True,formatting_native_actual_reference_and_release_still_pending=True,full_goal_complete=False))
