"""Bind original actor fields and chisel item only; no current wording approval."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B233_clean_name_tools_v7525')
if __name__=='__main__':
    assert not ROOT.exists();row=derive('scripts/bind_lil_B231_clean_names_item_v7476.py','scripts/bind_lil_B233_clean_names_item_v7525.py',{'B231':'B233','v7476':'v7525','work/analysis/lil_B231_clean_context_v7475/all16_clean_ancient_medical_book_fatigue_report_glosses_before_old_English.json':'work/analysis/lil_B233_clean_context_v7524/all11_clean_legendary_chisel_paper_library_tools_joke_glosses_before_old_English.json','item99':'item97','POINTER_099':'POINTER_097','00a0ffff63000110':'00a0ffff61000110','original_A000_item_operand99':'original_A000_item_operand97','historical_person_spelling_andgender_require_source_identity_context_not_generic_physician_assumption':'historical_sculptor_spelling_requires_source_identity_item_andreported_legend_context'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_clean_name_item_binding.json',dict(tool=row,original_actor_fields_anditem97_only=True,no_current_getter_voice_display_orEnglish_approval=True,new_credit=0,full_goal_complete=False))
