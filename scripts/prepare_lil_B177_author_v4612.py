"""Prepare ten B177 contextual decisions with exact source and individual retention notes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B177_author_tools_v4612')
assert not ROOT.exists()
tool=derive('scripts/author_lil_B176_v4558.py','scripts/author_lil_B177_v4612.py',{
    'B176':'B177','lil_B176':'lil_B177',
    'prose_v4557':'prose_v4611','author_v4558':'author_v4612',
    'comparison_v4556':'comparison_v4610','clean_context_v4547':'clean_context_v4601',
    'voices_v4549':'voices_v4603','branches_v4551':'branches_v4605','entry_v4552':'entry_v4606',
    'controls_v4554':'controls_v4608','names_v4553':'names_v4607',
    'Seville_pointer_bound_in_clean_and_current_staged_pool':
        'Genoa_two_inline_city_spans_and_unchanged_source_pointers_bound',
    'enthusiasm_taste_reason_doubt_imperious_insistence_compliance_order_offhand_reply_grand_laugh_and_forecast_preserved':
        'enthusiasm_color_skepticism_passion_reminiscence_detached_reply_cook_sell_order_offhand_reply_grand_laugh_and_forecast_preserved',
    'no_royal_rank_formal_relationship_quantity_price_completed_purchase_or_earned_boom_added':
        'no_added_lover_present_relationship_madam_rank_quantity_price_completed_sale_or_earned_boom',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,revisions=5,retentions=5,
    no_formatting_approval_orledger_credit=True,full_goal_complete=False))
