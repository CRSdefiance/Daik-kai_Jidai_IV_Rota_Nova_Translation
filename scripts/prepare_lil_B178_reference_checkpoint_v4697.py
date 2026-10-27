"""Prepare the full-history-guarded B178 sealed-reference metadata checkpoint."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_reference_checkpoint_tools_v4697');assert not ROOT.exists()
tool=derive('scripts/checkpoint_lil_B177_references_v4641.py','scripts/checkpoint_lil_B178_references_v4697.py',{
    'lil_B177_reference_checkpoint_text_v4641':'lil_B178_reference_checkpoint_text_v4697',
    'lil_B177_reference_checkpoint_v4641':'lil_B178_reference_checkpoint_v4697',
    'lil_B177_editorial_manuscript_v5':'lil_B178_editorial_manuscript_v3',
    'lil_B177_editorial_manuscript_v6':'lil_B178_editorial_manuscript_v4',
    'lil_B177_reference_approval_v4640':'lil_B178_reference_approval_v4696',
    'Lil-B177-tomato-red-passion-youthful-love-dry-Cook-cook-sell-and-prospective-Genoa-fashion10':
        'Lil-B178-home-baking-three-Ladies-husband-corner-bakery-teaching-ingredients-and-prospective-Amsterdam-wheat13',
    'editorial_handoff_verification_v4628':'editorial_handoff_verification_v4684',
    "len(approval['actual_sampled_display_IDs'])==10":"len(approval['actual_sampled_display_IDs'])==13",
    '(5885,5875,10)':'(5898,5885,13)',
    '5885 rereads/5875 integrated/10 pending;B177':'5898 rereads/5885 integrated/13 pending;B178',
    '3-reviewed-COMMON-incomplete;10-Lil-B177':'3-reviewed-COMMON-incomplete;13-Lil-B178',
    'unfinished_editorial_scope_v4623':'unfinished_editorial_scope_v4679',
    'B177_reference_and_actual_coverage_v4641':'B178_reference_and_actual_coverage_v4697',
    'unfinished_editorial_scope_v4641':'unfinished_editorial_scope_v4697',
    'lil_B177_reference_reconciliation_v4641':'lil_B178_reference_reconciliation_v4697',
    '(5875,5888,3733,2142)':'(5885,5901,3738,2147)',
    'lil_B177_display_fixture_v4635':'lil_B178_display_fixture_v4691','complete_B177_B22_fixtures':'complete_B178_B22_fixtures',
    'lil_B177_research_v4630':'lil_B178_research_v4686',
    '## V4641:10 B177':'## V4697:13 B178','# Current editorial handoff - V4641':'# Current editorial handoff - V4697',
    "checkpoint='V4641'":"checkpoint='V4697'",'fresh_reread=5885':'fresh_reread=5898',
    'integrated=5875,pending=10,source_prose=5888':'integrated=5885,pending=13,source_prose=5901',
    'actual_complete_native_panels=10':'actual_complete_native_panels=13','reviewed_sheets=2':'reviewed_sheets=3',
    'Record sealed10-actual B177':'Record sealed13-actual B178',
    'V4641:10 B177 records reference/actual-approved;counts and main V4541 unchanged.':
        'V4697:13 B178 records reference/actual-approved;counts and main V4595 unchanged.',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,no_new_credit=True,full_root_and_nested_history_validation_before_writes=True,
    all13_actual_panels_and_three_retained_ROMs_bound=True,full_goal_complete=False))
