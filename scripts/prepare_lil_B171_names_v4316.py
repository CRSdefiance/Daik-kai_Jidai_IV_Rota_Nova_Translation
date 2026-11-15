"""Prepare six original Lil/Yifa/Sanghyeon name consumers and scratch ownership."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B171_name_tools_v4316')

if __name__ == '__main__':
    assert not ROOT.exists()
    tool = derive('scripts/prove_lil_B170_names_v4266.py', 'scripts/prove_lil_B171_names_v4316.py', {
        'four original Lil/Yifa': 'six original Lil/Yifa/Sanghyeon',
        'lil_B170_names_v4266': 'lil_B171_names_v4316',
        'lil_B170_source_v4260/all33_clean_current_complete_context': 'lil_B171_source_v4311/all37_clean_current_complete_context',
        'lil_B170_voices_v4262': 'lil_B171_voices_v4312',
        'current2_static_names_voices': 'current3_static_names_voices',
        'for ident in [2,25]:': 'for ident in [2,25,81]:',
        'all_four_original_consumers': 'all_six_original_consumers',
        '::two-source-names': '::three-source-names',
        'fresh2_actor_names': 'fresh3_actor_names', 'len(values)==4': 'len(values)==6',
        "{2:'Lil Argot',25:'Yifa Sol'}": "{2:'Lil Argot',25:'Yifa Sol',81:'Sanghyeon Kan'}",
        'four_original_name_consumers_and_owned_scratch_paths': 'six_original_name_consumers_and_owned_scratch_paths',
        'native_four_consumer_cases': 'native_six_consumer_cases',
        "{'2':'Lil','25':'Yifa'}": "{'2':'Lil','25':'Yifa','81':'Sanghyeon'}",
        'source_onesan_address_does_not_establish_kinship': 'source_anideshi_and_sibling_simile_do_not_establish_biological_kinship',
        'not_actual_B170_nameplate_observation': 'not_actual_B171_nameplate_observation',
        'four_original_consumers_pass': 'six_original_consumers_pass',
    })
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tool=tool, source_selectors=[2,25,81],
        approved_spoken_names=['Lil','Yifa','Sanghyeon'], source51_is_static_actor81_not_Q=True,
        source_Sanghyeon_introduction_does_not_include_Kan=True, no_new_credit_or_ROM_change=True, full_goal_complete=False))
