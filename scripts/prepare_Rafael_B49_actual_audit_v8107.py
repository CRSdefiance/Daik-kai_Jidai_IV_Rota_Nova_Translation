"""Derive complete B49 actual-mask audit without inheriting B48-specific pagination or geometry claims."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B49_actual_tools_v8107')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/audit_Rafael_B48_actual_v8053.py','scripts/audit_Rafael_B49_actual_v8107.py',{
        'Audit observed source/English paths,complete native pages/names andordinary R347 pagination.':'Audit observed complete B49 paths, source/English single pages, seven names and C281 transition.',
        'Rafael_B48_actual_v8053':'Rafael_B49_actual_v8107',
        'Rafael_B48_scene_fixtures_v8049':'Rafael_B49_scene_fixtures_v8105',
        'Rafael_B48_scene_runs_v8050':'Rafael_B49_scene_runs_v8106',
        'Rafael_B48_source_rightcell_v8052/91_source_native_pages9_name_planes_R129_actual_rightcell_bound.json':'Rafael_B49_source_name_planes_v8093/61_complete_source_pages7_names8_fresh20_reused_literal_alignments.json',
        'Rafael_B48_pages_refined_v8038/91_final_native_paragraphs92_pages4_fresh360_reused_alignments.json':'Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json',
        'Rafael_B48_stored_v8042/all91_stored_bodies192_fresh172_reused_alignments92_exact_viewed_pages.json':'Rafael_B49_stored_v8097/all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages.json',
        'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B48_source_paths_v8025/500_source_result_compositions32_text_paths_two_exclusive_pairs.json':'Rafael_B49_source_paths_v8082/156250_compositions_distinct_complete_text_paths_and61_source_memberships.json',
        'all91_native_ink_planes_exact_to_already_viewed':'all61_native_ink_planes_exact_to_already_viewed',
        "terminal['frames']==40001":"terminal['frames']==24001", "report['frames']==40001":"report['frames']==24001",
        'len(expected)==173 and len(records)==91':'len(expected)==164 and len(records)==61',
        'after_B48_return':'after_B49_return',
        'actor in [0,4,5,6,7,8,13,75,113,254]':'actor in [0,2,4,5,6,8,9]',
        "source_rightcell=version=='clean_Japanese' and record['id']=='DK4_MES_B48_R0129'":"source_rightcell=False",
        "flow['source_result_compositions']":"flow['representative_text_paths']",
        "r53=next(s for s in speeches if s['id']=='DK4_MES_B48_R0347')":"r53=speeches[-1]",
        "after,40000]":"after,24000]",
        "{version}_R347_return_final.png":"{version}_C281_return_final.png",
        "original53=next(s for s in source['speech_observations'] if s['id']=='DK4_MES_B48_R0347')\n    english53=next(s for s in en['speech_observations'] if s['id']=='DK4_MES_B48_R0347')\n    assert original53['native_page_count']==1 and english53['native_page_count']==2 and len(english53['ordinary_page_transitions'])==1":"assert all(s['native_page_count']==1 and not s['ordinary_page_transitions'] for g in groups for s in g['speech_observations'])\n    assert all(any(p['word']==0xC281 and p['decoded_length']==2 for p in g['command_pairs']) for g in groups)",
        'paired_source_English_observed_path_complete_pages_names_andR347_transition.json':'paired_source_English_observed_path_complete_pages_names_C281_andreturn.json',
        'actual_source_R347_one_page_English_two_pages_ordinary_A_turn_andfollowing_return_preserved':'actual_source_English_single_page_speeches_C281_command_andfollowing_return_preserved',
        'actual_total_frames=80002':'actual_total_frames=48002',
        'all91_source_objects_retained_butonly_observed_path_is_actual_gameplay_coverage':'all61_source_objects_retained_butonly_observed_path_is_actual_gameplay_coverage',
        'original_ten_command_B44_ROM_entry_fixture_not_natural_B48_activation_original_location_orfullroute':'original_ten_command_B44_ROM_entry_fixture_not_natural_B49_activation_original_location_orfullroute',
        'Observed source/English pages andR347 ordinary page turn audited;unresolved':'Observed source/English pages, names and C281 command/return audited;unresolved',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Prepared B49 actual audit; no assumed path count, FE consumers or invented page-turn coverage.')
