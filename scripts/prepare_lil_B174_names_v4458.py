"""Prepare eight original Lil/Emilio/Julian/Mihwa name consumers."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_name_tools_v4458')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/prove_lil_B172_names_v4369.py','scripts/prove_lil_B174_names_v4458.py',{
        'six original Lil/Julian/Mihwa':'eight original Lil/Emilio/Julian/Mihwa',
        'lil_B172_names_v4369':'lil_B174_names_v4458',
        'lil_B172_source_v4364/all27_clean_current_complete_context':'lil_B174_source_v4453/all33_clean_current_complete_context',
        'lil_B172_voices_v4365':'lil_B174_voices_v4454','current3_static_names':'current4_static_names',
        'for ident in [2,26,201]:':'for ident in [2,14,26,201]:',
        'all_six_original_consumers':'all_eight_original_consumers','::three-source-names':'::four-source-names',
        'fresh3_actor_names':'fresh4_actor_names','len(values)==6':'len(values)==8',
        "{2:'Lil Argot',26:'Julian Lopes',201:'Mihwa'}":"{2:'Lil Argot',14:'Emilio Ｆerog',26:'Julian Lopes',201:'Mihwa'}",
        'six_original_name_consumers':'eight_original_name_consumers','native_six_consumer_cases':'native_eight_consumer_cases',
        "{'2':'Lil','26':'Julian','201':'Mihwa'}":"{'2':'Lil','14':'Emilio','26':'Julian','201':'Mihwa'}",
        'source_1A_and_C9_selectors_are_Julian26_Mihwa201_not_text_to_strip=True':
            'source_0E_1A_C9_selectors_are_Emilio14_Julian26_Mihwa201_not_literal_prose=True',
        'source_familiar_flirtation_does_not_establish_romantic_partnership_or_actual_date_agreement=True':
            'source_new_employer_and_actual_grandfather_preserved_without_romance_status_or_unconditional_date=True',
        'not_actual_B172_nameplate_observation':'not_actual_B174_nameplate_observation',
        'six_original_consumers_pass':'eight_original_consumers_pass',
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,selectors=[2,14,26,201],
        native_full_names_unchanged=True,Emilio_fullwidth_F_native_spelling_not_reauthored=True,
        no_new_credit_or_ROM_change=True,full_goal_complete=False))
    print('Prepared eight original four-actor name consumers, preserving owned and read-only paths.')
