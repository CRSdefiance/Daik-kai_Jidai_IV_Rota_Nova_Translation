"""Bind the separate giant-tortoise shield designation while keeping catalog review open."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B229_item_tools_v7385')
if __name__=='__main__':
    assert not ROOT.exists()
    changes={'B228':'B229','name_item_v7338':'name_item_v7385','source_v7334/thirteen_clean_current_armadillo_shield_rumor_source_references':'source_v7381/seventeen_clean_current_giant_tortoise_callback_source_references','consumers_v7335/thirteen_effective_bodies26_dispatches_two_actors_four_name_consumers':'consumers_v7382/seventeen_effective_bodies34_dispatches_two_actors_four_name_consumers','アルマジロの鉄皮':'巨大ゾウガメの盾','Armadillo Hide':'Giant Tortoise Shield','exact_armadillo_item':'exact_giant_tortoise_item','current_Armadillo_Hide_asset_andharder_than_iron_source_meaning_bound':'current_Giant_Tortoise_Shield_asset_andreported_iron_hard_shell_source_meaning_bound','older_dialogue_Steel_Hide_conflicts_with_clean_iron_andcurrent_name_requires_revision':'older_dialogue_Giant_Tortoise_Shield_name_matches_exact_registered_item'}
    r=derive('scripts/bind_lil_B228_names_item_v7338.py','scripts/bind_lil_B229_names_item_v7385.py',changes);ROOT.mkdir(parents=True);save(ROOT/'source_locked_item_andnames.json',dict(tool=r,distinct_item53_binding_required_not_B228_item50=True,Samwell_full_catalogue_middle_still_unapproved=True,new_credit=0,full_goal_complete=False))
