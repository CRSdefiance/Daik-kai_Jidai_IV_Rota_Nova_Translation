"""Bind Lil/Reika's four original name consumers with their owned/read-only paths."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_name_tools_v4416')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/prove_lil_B172_names_v4369.py','scripts/prove_lil_B173_names_v4416.py',{
        'six original Lil/Julian/Mihwa':'four original Lil/Reika','lil_B172_names_v4369':'lil_B173_names_v4416',
        'lil_B172_source_v4364/all27_clean_current_complete_context':'lil_B173_source_v4411/all11_clean_current_complete_context',
        'lil_B172_voices_v4365':'lil_B173_voices_v4412','current3_static_names':'current2_static_names',
        'for ident in [2,26,201]:':'for ident in [2,202]:','all_six_original_consumers':'all_four_original_consumers',
        '::three-source-names':'::two-source-names','fresh3_actor_names':'fresh2_actor_names',
        'len(values)==6':'len(values)==4',"{2:'Lil Argot',26:'Julian Lopes',201:'Mihwa'}":"{2:'Lil Argot',202:'Reika'}",
        'six_original_name_consumers':'four_original_name_consumers','native_six_consumer_cases':'native_four_consumer_cases',
        "{'2':'Lil','26':'Julian','201':'Mihwa'}":"{'2':'Lil','202':'Reika'}",
        'source_1A_and_C9_selectors_are_Julian26_Mihwa201_not_text_to_strip=True,source_printed_Yurian_and_Mihwa_use_bound_approved_spellings=True':'source_CA_selector_is_Reika202_not_text_to_strip=True,source_unnamed_feminine_voice_binds_native_Reika_without_invented_role=True',
        'source_familiar_flirtation_does_not_establish_romantic_partnership_or_actual_date_agreement=True':'source_uncertain_smooth_talking_man_report_does_not_confirm_Julian_identity_or_current_location=True',
        'not_actual_B172_nameplate_observation':'not_actual_B173_nameplate_observation','six_original_consumers_pass':'four_original_consumers_pass',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,source_selectors=[2,202],approved_spoken_names=['Lil','Reika'],
        every_owned_ring_or_original_readonly_path_restores_all4MiB=True,no_new_credit_or_ROM_change=True,full_goal_complete=False))
    print('Prepared four original Lil/Reika name consumers;source given-name/prose-role scope preserved.')
