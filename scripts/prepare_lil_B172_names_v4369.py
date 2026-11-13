"""Prepare six original Lil/Julian/Mihwa name consumers with source-owned identity scope."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_name_tools_v4369')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/prove_lil_B171_names_v4316.py','scripts/prove_lil_B172_names_v4369.py',{
        'Lil/Yifa/Sanghyeon':'Lil/Julian/Mihwa','lil_B171_names_v4316':'lil_B172_names_v4369',
        'lil_B171_source_v4311/all37_clean_current_complete_context':'lil_B172_source_v4364/all27_clean_current_complete_context',
        'lil_B171_voices_v4312':'lil_B172_voices_v4365','for ident in [2,25,81]:':'for ident in [2,26,201]:',
        "{2:'Lil Argot',25:'Yifa Sol',81:'Sanghyeon Kan'}":"{2:'Lil Argot',26:'Julian Lopes',201:'Mihwa'}",
        "{'2':'Lil','25':'Yifa','81':'Sanghyeon'}":"{'2':'Lil','26':'Julian','201':'Mihwa'}",
        'source_19_selector_is_Yifa25_not_text_to_strip=True,source_printed_Ifa_maps_to_approved_Yifa_spelling=True':'source_1A_and_C9_selectors_are_Julian26_Mihwa201_not_text_to_strip=True,source_printed_Yurian_and_Mihwa_use_bound_approved_spellings=True',
        'surname_not_added_to_source_spoken_introduction=True,source_anideshi_and_sibling_simile_do_not_establish_biological_kinship=True':'surname_not_added_to_source_given_name_addresses=True,source_familiar_flirtation_does_not_establish_romantic_partnership_or_actual_date_agreement=True',
        'not_actual_B171_nameplate_observation':'not_actual_B172_nameplate_observation',
        "    assert all(r['original_scratch_rings'] and r['original_getter_writes'] for r in native['rows'])":"    assert all((r['original_scratch_rings'] and r['original_getter_writes']) or (r['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring' and not r['original_getter_writes']) for r in native['rows'])",
    })
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tool=tool,source_selectors=[2,26,201],approved_spoken_names=['Lil','Julian','Mihwa'],
        every_owned_ring_or_original_readonly_name_path_restores_all4MiB=True,no_source_surname_or_romance_invention=True,
        no_new_credit_or_ROM_change=True,full_goal_complete=False))
