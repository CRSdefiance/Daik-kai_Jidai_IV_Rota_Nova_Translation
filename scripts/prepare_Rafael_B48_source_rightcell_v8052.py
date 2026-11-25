"""Reuse the guarded source-only nineteenth-cell calibration for one B48 source paragraph."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/bind_Maria_B35_source_rightcell_v7753.py','scripts/bind_Rafael_B48_source_rightcell_v8052.py',{
        'maria_B35_source_rightcell_v7753':'Rafael_B48_source_rightcell_v8052',
        'maria_story_source_name_planes_v7751/67_clean_source_native_pages8_complete_name_planes32_literal_alignments.json':'Rafael_B48_source_name_planes_v8037/91_complete_source_pages9_names36_literal_alignments4_FE.json',
        'maria_story_actual_v7752b/six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json':'Rafael_B48_actual_v8051b/paired_source_English_observed_path_complete_pages_names_andR347_transition.json',
        'maria_story_scene_runs_v7750/route3_B35_clean_Japanese':'Rafael_B48_scene_runs_v8050/route0_clean_Japanese',
        'DK4_MES_B35_R0065':'DK4_MES_B48_R0129',
        "p['frame']==8600":"p['frame']==7330", 'frame8600':'frame7330',
        'B35_R65':'B48_R129', 'R65':'R129',
        '67_source_native_pages8_name_planes_R65_actual_rightcell_bound.json':'91_source_native_pages9_name_planes_R129_actual_rightcell_bound.json',
        'English216px_safe_geometry_all67_compiled_stored_bytes_andall33_parity_tails_unchanged':'English216px_safe_geometry_all91_compiled_stored_bytes_andall48_parity_tails_unchanged',
        'Allother glyphs andEnglish216geometry unchanged.':'Allother glyphs andEnglish216geometry unchanged.',
    }))
