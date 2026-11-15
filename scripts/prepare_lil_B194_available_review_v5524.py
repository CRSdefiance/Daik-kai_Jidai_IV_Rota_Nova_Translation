"""Measure conditional-case captures and final native state,including original actor6 join outcome."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/review_lil_B194_default_actual_v5522.py', 'scripts/review_lil_B194_available_actual_v5524.py', {
        'default_actual_review_v5522': 'available_actual_review_v5524',
        'actual_v5517/actual_selected9_progressive_FE_availability0_A000_C200_and_single_end':
        'available_actual_v5523b/actual_all11_progressive_FE_FI_availability1_resource42_two_C200_and_single_end',
        'display_fixture_v5514': 'available_fixture_v5519', 'display_v5515': 'available_v5520',
        'display_run_v5515': 'available_run_v5520',
        "actual['complete_matching_observations']==9": "actual['complete_matching_observations']==11",
        "len(v['selected_B22_command_pairs'])==24 and len(v['selected_intervals'])==9":
        "len(v['selected_B22_command_pairs'])==30 and len(v['selected_intervals'])==11",
        "v['source_C200'][0]['original_source_offset']==534":
        "[r['original_source_offset'] for r in v['source_C200']]==[494,534] and all(r['result_words']==[3,1] for r in v['source_C200'])",
        "v['selected_B22_command_pairs'][-1]['result_words']==[0,0]": "v['selected_B22_command_pairs'][-1]['result_words']==[0,1]",
        "['DK4_MES_B194_R0006','DK4_MES_B194_R0026','DK4_MES_B194_R0034','DK4_MES_B194_R0056']":
        "['DK4_MES_B194_R0026','DK4_MES_B194_R0046','DK4_MES_B194_R0049','DK4_MES_B194_R0056']",
        'all9_selected_complete_held_planes': 'all11_complete_held_planes',
        'all9_selected_speeches8_progressive1': 'all11_speeches10_progressive1',
        'source_A0008_common_C200534_single_end536': 'source_A0008_resource42_two_C200494_534_single_end536',
        'actual24_of30_stored_fixture_commands_selected_with_source_availability_false':
        'actual30_of31_stored_fixture_commands_selected_with_original_recruitment_setup_and_unforced_availability_true',
        'paired_all115_samples24_selected_commands9_planes': 'paired_all115_samples30_selected_commands11_planes',
        'complete_panels=9': 'complete_panels=11',
        "assert captain==2 and 0x02000000<=root<=0x02400000-0x1A04":
        "assert captain==2 and 0x02000000<=root<=0x02400000-0x1A04\n        before_getters=bytes(cpu.mem_read(0x02000000,0x400000));actor6=root+4+6*32\n        actor6_company=get(0x7E958,actor6);actor6_available=get(0x7DB14,actor6)\n        assert (actor6_company,actor6_available)==(1,1) and bytes(cpu.mem_read(0x02000000,0x400000))==before_getters",
        'captain_ID=captain,seed=': 'captain_ID=captain,actor6_company=actor6_company,actor6_availability=actor6_available,seed=',
        'future_world_equivalence_and_full_RAM_equality_not_claimed=True':
        "observed_original_join_actor6_company_and_availability=[dict(company=r['actor6_company'],availability=r['actor6_availability']) for r in native],disclosed_original_recruitment_setup_is_not_earned_story_progress=True,future_world_equivalence_and_full_RAM_equality_not_claimed=True",
    }))
