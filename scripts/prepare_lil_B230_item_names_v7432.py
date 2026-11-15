"""Bind the separate phoenix helmet and reuse only byte-identical name-font evidence."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B230_item_tools_v7432')
if __name__=='__main__':
    assert not ROOT.exists()
    item={'B229':'B230','name_item_v7385':'name_item_v7432','source_v7381/seventeen_clean_current_giant_tortoise_callback_source_references':'source_v7428/seventeen_clean_current_phoenix_bascinet_callback_source_references','consumers_v7382':'consumers_v7429','巨大ゾウガメの盾':'不死鳥のバシネット','Giant Tortoise Shield':'Phoenix Bascinet','exact_giant_tortoise_item':'exact_phoenix_bascinet_item','source_named_shield_not_runtime_FI_substitution':'source_named_helmet_not_runtime_FI_substitution','current_Giant_Tortoise_Shield_asset_andreported_iron_hard_shell_source_meaning_bound':'current_Phoenix_Bascinet_asset_andreported_iron_flame_forging_anduncertain_name_bound','older_dialogue_Giant_Tortoise_Shield_name_matches_exact_registered_item':'older_dialogue_Phoenix_Bascinet_name_matches_exact_registered_item'}
    reuse={'B229':'B230','name_planes_v7386':'name_planes_v7433','lil_B228_name_planes_v7339':'lil_B229_name_planes_v7386','consumers_v7382':'consumers_v7429','exact B228':'exact B229','exact B228 name-font':'exact B229 name-font'}
    # The broader phrase above covers the narrower phrase without a second edit; every listed key must exist.
    reuse.pop('exact B228 name-font')
    jobs=[('scripts/bind_lil_B229_names_item_v7385.py','scripts/bind_lil_B230_names_item_v7432.py',item),('scripts/reuse_lil_B229_name_planes_v7386b.py','scripts/reuse_lil_B230_name_planes_v7433.py',reuse)]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    rows=[derive(a,b,c) for a,b,c in jobs];ROOT.mkdir(parents=True);save(ROOT/'source_locked_item_andname_font_reuse.json',dict(tools=rows,distinct_source_phoenix_helmet_item_not_prior_shield=True,Samwell_catalogue_middle_still_unapproved=True,name_font_reuse_requires_same_runtime_fonts_source_fields_andfour_getters=True,new_credit=0,full_goal_complete=False))
