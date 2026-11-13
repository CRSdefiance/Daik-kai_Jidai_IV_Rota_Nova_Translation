"""Independent source-bound two-menu successor;no haggling/effect/price assumptions inherited."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B206_choice_tools_v6281')
if __name__=='__main__':
    assert not ROOT.exists()
    proof=derive('scripts/prove_lil_B201_choices_v5924.py','scripts/prove_lil_B206_choices_v6281.py',{
      'B201':'B206','lil_B201_choices_v5924':'lil_B206_choices_v6281','scripts.lil_current_font_oracles_v5918':'scripts.shady_man_font_oracles_v6263',
      'work/analysis/lil_B201_source_v5902/all26_clean_current_complete_context_with_two_choice_labels.json':'work/analysis/lil_B206_current_v6280/all28_clean_current_context_rebound_to_V6270.json',
      'translations/lil_B201_choice_manuscript_v1.json':'translations/lil_B206_choice_manuscript_v1.json','[(201,880)]':'[(206,852),(206,1020)]',
      'assert len(cases)==1':'assert len(cases)==2','all1_typed_menu_native_proof':'all2_typed_menus_native_proof',
      'native_selection_cancel_cases=6,complete_current_and_reviewed_style_label_planes=8,clean_current_reviewed_native_decoder_cases=3,all2_labels_source_order':'native_selection_cancel_cases=12,complete_current_and_reviewed_style_label_planes=16,clean_current_reviewed_native_decoder_cases=6,all4_labels_source_order',
    })
    ROOT.mkdir(parents=True);save(ROOT/'two_original2100_menu_decoder_VM_geometry_and_font_tools.json',dict(derivation=proof,two_source_menu_offsets=[852,1020],four_labels=4,no_source_payment_effect_or_old_haggling_assumption=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Two source-bound typed-menu proofs prepared:852/1020,four labels,12 VM selection/cancel cases and16 complete style planes.')
