"""Prepare six source actors,48 speech dispatches,EV2 entry and12 name consumers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B196_contract_tools_v5591')
OLD='source_v5541/all20_clean_current_complete_context.json'
NEW='source_v5590/all36_clean_current_complete_context_with_twelve_choice_labels.json'
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/reconcile_lil_B195_voices_v5542.py','scripts/reconcile_lil_B196_voices_v5591.py',{
        'B195':'B196',OLD:NEW,'voices_v5542':'voices_v5591',
        '[92,103,119]':'[2,6,19,20,25,173]','fresh3_actor_names':'fresh6_actor_names','len(fresh)==3':'len(fresh)==6',
        'current207_catalog_eight_voices_and_three_source_selectors':'current207_catalog_eight_voices_and_six_source_selectors',
        'the three':'the six','V5531':'V5580',
        'no_kinship_rank_employment_or_named_dish_inferred_from_familiar_food_banter':'no_kinship_rank_employment_item_identity_or_guaranteed_bargaining_outcome_inferred_from_dialogue'})]
    rows.append(derive('scripts/prove_lil_B195_dispatches_v5543.py','scripts/prove_lil_B196_dispatches_v5592.py',{
        'B195':'B196',OLD:NEW,'voices_v5542':'voices_v5591','dispatches_v5543':'dispatches_v5592',
        'Bind40':'Bind48','and3 exact':'and37 exact','len(cases)==40 and len(leaves)==3':'len(cases)==48 and len(leaves)==37',
        'all20_source_current_dispatches_no_macros_and3_control_leaves':'all24_source_current_dispatches_FI1_and37_control_leaves',
        'all3_nonrelative':'all37_nonrelative','all3_static_actors':'all6_static_actors',
        '40 source/current dispatches pass:three static actors,one FE/null-actor object,no macros. All3 nonrelative leaves exact.':
        '48 source/current dispatches pass:six static actors,one FE/null-actor object,FI1. All37 nonrelative leaves exact.'}))
    rows.append(derive('scripts/prove_lil_B195_entry_v5544.py','scripts/prove_lil_B196_entry_v5593.py',{
        'B195':'B196',OLD:NEW,'voices_v5542':'voices_v5591','entry_v5544':'entry_v5593','in [195]':'in [196]'}))
    rows.append(derive('scripts/prove_lil_B195_names_v5546.py','scripts/prove_lil_B196_names_v5594.py',{
        'B195':'B196',OLD:NEW,'voices_v5542':'voices_v5591','names_v5546':'names_v5594',
        'current207_catalog_eight_voices_and_three_source_selectors':'current207_catalog_eight_voices_and_six_source_selectors',
        '[92,103,119]':'[2,6,19,20,25,173]','fresh3_actor_names':'fresh6_actor_names','len(native[\'rows\'])==6':"len(native['rows'])==12",
        'six_original_progressive_and_catalogue_name_consumers':'twelve_original_progressive_and_catalogue_name_consumers',
        'native_six_consumer_cases':'native_twelve_consumer_cases','source-three-name-consumers':'source-six-name-consumers','Six source-owned':'Twelve source-owned'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_native_contracts.json',dict(tools=rows,source_speech_objects=24,
        typed_choice_objects=6,typed_choice_labels=12,source_commands=119,six_source_static_actors=[2,6,19,20,25,173],
        source_FI1_not_removed_or_hardcoded=True,relative_control_predicate_resource_picture_effect_and_choice_UI_gates_pending=True,
        no_ROM_registry_ledger_or_credit_change=True,full_goal_complete=False))
