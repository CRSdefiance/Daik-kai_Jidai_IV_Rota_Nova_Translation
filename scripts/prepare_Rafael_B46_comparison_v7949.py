"""Measure both actual source/English path pairs without forcing timing,RNG,UI orstate equality."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_comparison_tools_v7949');assert not root.exists()
    row=derive('scripts/measure_Rafael_B45_pairs_v7896b.py','scripts/measure_Rafael_B46_pairs_v7949.py',{
        'Rafael_B45_actual_comparison_v7896b':'Rafael_B46_actual_comparison_v7949',
        'Rafael_B45_actual_v7895b/paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json':'Rafael_B46_actual_v7948/four_runs24_unique_speeches58_occurrences_two_choices_actual_body_name_FE_return_audit.json',
        "sheet=Image.new('RGB',(1536,410)":"sheet=Image.new('RGB',(1536,820)",
        '    for route in [0]:':"    assert not actual['unresolved']\n    for choice_index,choice in enumerate(['accept','decline']):\n        route=0",
        "g['route']==route and g['version']==v":"g['route']==route and g['choice']==choice and g['version']==v",
        "assert a['native_result']==b['native_result'] and a['UI_after']==b['UI_after']":"assert a['native_result']==b['native_result']",
        "['start','returned','decoded_length','before_RNG','after_RNG']":"['start','returned','decoded_length','before_RNG','after_RNG','UI_before','UI_after']",
        'assert frames[0]==6730 and frames[-1]==16001':'assert frames and frames[0]>threshold and frames[-1]==16001',
        'route*410':'choice_index*410',
        "f'route{route} '":"f'route{route} {choice} '",
        "route_identity=source['route_identity'],source_English_exits":"route_identity=source['route_identity'],choice=choice,source_English_exits",
        'all12_whole_upper_scene_portrait_andheader_RGB_equal':'all_measured_whole_upper_scene_portrait_andheader_RGB_equal',
        'all_original_initializer_andexchange_results_andUI_words_equal=True':'all_original_initializer_andexchange_results_equal=True,all_UI_request_words_equal=all(a[\'UI_before\']==b[\'UI_before\'] and a[\'UI_after\']==b[\'UI_after\'] for a,b in zip(source[\'command_pairs\'],english[\'command_pairs\'],strict=True))',
        'scene_pairs=12':'choice=choice,scene_pairs=len(pairs)',
        'Rafael_unmasked_return_midpoint_final_source_English_pairs.png':'Rafael_B46_both_choices_unmasked_return_midpoint_final_source_English_pairs.png',
        '12_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json':'both_choices29_scene_pairs_full_measured_timing_RNG_components_RGB_limits.json',
        'all12_source_English_upper_scene_portrait_complete_header_pairs_equal':'all29_source_English_upper_scene_portrait_complete_header_pairs_equal',
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
