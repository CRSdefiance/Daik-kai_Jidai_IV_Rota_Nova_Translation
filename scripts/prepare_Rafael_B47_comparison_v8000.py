"""Prepare evidence-led11-scene comparison;measure every timing/RNG/UI/later difference."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B47_comparison_tools_v8000')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/measure_Rafael_B45_pairs_v7896b.py','scripts/measure_Rafael_B47_pairs_v8000.py',{
        'Rafael_B45_actual_comparison_v7896b':'Rafael_B47_actual_comparison_v8000',
        'Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json':
            'Rafael_B47_actual_v7999/paired_source_English_observed_path_complete_pages_names_andR53_transition.json',
        "actual=read(ACTUAL);groups=[]":"actual=read(ACTUAL);assert not actual['unresolved'];groups=[]",
        "assert a['native_result']==b['native_result'] and a['UI_after']==b['UI_after']":
            "assert a['native_result']==b['native_result']",
        "['start','returned','decoded_length','before_RNG','after_RNG']":
            "['start','returned','decoded_length','before_RNG','after_RNG','UI_before','UI_after']",
        "assert frames[0]==6730 and frames[-1]==16001":"assert frames and frames[0]>threshold and frames[-1]==16001",
        'all12_whole_upper_scene_portrait_andheader_RGB_equal':'all11_whole_upper_scene_portrait_andheader_RGB_equal',
        'all_original_initializer_andexchange_results_andUI_words_equal=True':
            "all_original_initializer_andexchange_results_equal=True,all_UI_request_words_equal=all(a['UI_before']==b['UI_before'] and a['UI_after']==b['UI_after'] for a,b in zip(source['command_pairs'],english['command_pairs'],strict=True))",
        'scene_pairs=12':'scene_pairs=len(pairs)',
        '12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json':
            '11_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json',
        'all12_source_English_upper_scene_portrait_complete_header_pairs_equal':
            'all11_source_English_upper_scene_portrait_complete_header_pairs_equal',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared11-scene actual comparison withall timing,RNG,UI,component andlateRGB measurements retained.')
