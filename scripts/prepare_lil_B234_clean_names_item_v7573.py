"""Read original fields and item106; keep the merchant's personal alias unresolved."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_clean_name_tools_v7573')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/bind_lil_B233_clean_names_item_v7525.py','scripts/bind_lil_B234_clean_names_item_v7573.py',{'B233':'B234','v7525':'v7573','work/analysis/lil_B233_clean_context_v7524/all11_clean_legendary_chisel_paper_library_tools_joke_glosses_before_old_English.json':'work/analysis/lil_B234_clean_context_v7572/all18_clean_familiar_banter_greatgrandfather_papal_trade_andconditional_discovery_glosses_before_old_English.json','item97':'item106','POINTER_097':'POINTER_106','00a0ffff61000110':'00a0ffff6a000110','original_A000_item_operand97':'original_A000_item_operand106','historical_sculptor_spelling_requires_source_identity_item_andreported_legend_context':'merchant_role_personal_alias_andpapal_item_scope_require_complete_source_consumers'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_name_item_binding.json',dict(tool=row,original_actor19_104_fields_anditem106_only=True,no_current_name_getter_voice_display_alias_global_label_orEnglish_approval=True,no_predecessor_story_English_read=True,new_credit=0,full_goal_complete=False))
