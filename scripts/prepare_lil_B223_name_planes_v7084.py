"""Prepare eleven complete current name/component planes without an AA5 runtime assumption."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_name_plane_tools_v7084')
if __name__=='__main__':
    assert not ROOT.exists();tool=derive('scripts/prove_lil_B214_name_planes_v6710.py','scripts/prove_lil_B223_name_planes_v7084.py',{'B214':'B223','name_planes_v6710':'name_planes_v7084','current_V6686_native_v6696':'current_V7067_native_v7077','names_v6699/four_names_eight_getters_signature_mismatch_and_other_raw_occurrence_leads':'names_v7083/four_names_eight_getters_full_Ian_signature_and_direct_given_name_binding','Al_Ferid_exact_native_context_v6520':'square_shopkeeper_exact_native_context_v7020','Al_Ferid_name_style_v6520':'square_shopkeeper_name_style_v7020','Al_Ferid_font_oracles_v6520':'square_shopkeeper_font_oracles_v7020',"{'Janus Pasar','Manuel Almeida','Sailor','Retainer'}":"{'Cesare Tony','Ian Dukov','Sailor','Retainer'}",'actual_source_headers_separate_proof_and_Manuel_header_unvisited':'actual_source_headers_separate_proof_and_Cesare_conditional_header_unvisited'})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_exact_current_name_planes.json',dict(tool=tool,all_original_native_addresses_literal_macro_guards_style11_and_bounds_preserved=True,new_credit=0,full_goal_complete=False))
