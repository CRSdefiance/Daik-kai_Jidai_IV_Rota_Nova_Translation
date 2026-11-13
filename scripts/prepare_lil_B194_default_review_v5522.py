"""Measure default-case timing,all sampled regions and final state without equivalence assumptions."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/review_lil_B193_actual_v5473.py', 'scripts/review_lil_B194_default_actual_v5522.py', {
        'B193': 'B194', 'actual_review_v5473': 'default_actual_review_v5522',
        'actual_v5472/actual_all15_progressive_FE_A000_C200_and_single_end':
        'actual_v5517/actual_selected9_progressive_FE_availability0_A000_C200_and_single_end',
        'display_fixture_v5469': 'display_fixture_v5514', 'display_v5471': 'display_v5515',
        'display_run_v5471': 'display_run_v5515',
        "actual['complete_matching_observations']==15": "actual['complete_matching_observations']==9",
        "len(actual['review_sheets'])==3": "len(actual['review_sheets'])==2",
        "len(v['selected_B22_command_pairs'])==27 and len(v['selected_intervals'])==15":
        "len(v['selected_B22_command_pairs'])==24 and len(v['selected_intervals'])==9",
        'single_source_end662': 'single_source_end536',
        "v['source_C200']['original_source_offset']==660": "v['source_C200'][0]['original_source_offset']==534",
        "['DK4_MES_B193_R0006','DK4_MES_B193_R0025','DK4_MES_B193_R0044','DK4_MES_B193_R0059']":
        "['DK4_MES_B194_R0006','DK4_MES_B194_R0026','DK4_MES_B194_R0034','DK4_MES_B194_R0056']",
        'all15_complete_held_planes': 'all9_selected_complete_held_planes',
        'all15_speeches14_progressive1': 'all9_selected_speeches8_progressive1',
        'source_A0008_C200660_single_end662': 'source_A0008_common_C200534_single_end536',
        'actual27_of27_stored_fixture_commands_selected': 'actual24_of30_stored_fixture_commands_selected_with_source_availability_false',
        'source_event193_natural_eligibility': 'source_event194_natural_eligibility',
        'paired_all115_samples27_commands15_planes': 'paired_all115_samples24_selected_commands9_planes',
        'complete_panels=15': 'complete_panels=9',
    }))
