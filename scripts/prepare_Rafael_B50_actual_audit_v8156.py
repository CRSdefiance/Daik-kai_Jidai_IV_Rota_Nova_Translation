"""Derive B50 actual-page audit, requiring all37 linear commands rather than branch coverage."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Rafael_B50_actual_tools_v8156')
if __name__=='__main__':
    assert not ROOT.exists()
    receipt=derive('scripts/audit_Rafael_B49_actual_v8107.py','scripts/audit_Rafael_B50_actual_v8156.py',{
        'Audit observed complete B49 paths, source/English single pages, seven names and C281 transition.':'Audit all37 linear B50 commands,28 source/English single pages,three names and4821/4720/4681 return.',
        'Rafael_B49_actual_v8107':'Rafael_B50_actual_v8156',
        'Rafael_B49_scene_fixtures_v8105':'Rafael_B50_scene_fixtures_v8154',
        'Rafael_B49_scene_runs_v8106':'Rafael_B50_scene_runs_v8155',
        'Rafael_B49_source_name_planes_v8093/61_complete_source_pages7_names8_fresh20_reused_literal_alignments.json':'Rafael_B50_source_name_planes_v8142/28_complete_source_pages3_names0_fresh12_reused_literal_alignments.json',
        'Rafael_B49_pages_refined_v8092/61_final_native_pages20_fresh224_reused_alignments.json':'Rafael_B50_pages_refined_v8143/28_final_native_pages20_fresh92_reused_alignments.json',
        'Rafael_B49_stored_v8097/all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages.json':'Rafael_B50_stored_v8147/all28_stored_bodies_full_native_alignment_and28_exact_viewed_pages.json',
        'Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B49_source_paths_v8082/156250_compositions_distinct_complete_text_paths_and61_source_memberships.json':'Rafael_B50_reference_census_v8153/all37_commands_zero_relative_sites28_speeches_4821_EV0_entry_shipped_callers.json',
        'all61_native_ink_planes_exact_to_already_viewed':'all28_native_ink_planes_exact_to_already_viewed',
        "terminal['frames']==24001":"terminal['frames']==16001","report['frames']==24001":"report['frames']==16001",
        'len(expected)==164 and len(records)==61':'len(expected)==47 and len(records)==28',
        'after_B49_return':'after_B50_return','actor in [0,2,4,5,6,8,9]':'actor in [0,2,9]',
        "matchedpaths=[p for p in flow['representative_text_paths'] if p['visited_source_offsets']==visited]\n        assert matchedpaths and all(p['source_speech_IDs']==[s['id'] for s in speeches] for p in matchedpaths)":
        "assert len(flow['all_command_maps'])==37 and not flow['relative_operand_maps'] and not flow['relocated_relative_cases']\n        assert visited==[c['offset'] for c in current['groups'][0]['all_source_commands']]\n        assert [s['id'] for s in speeches]==[r['id'] for r in current['records']]\n        matchedpaths=[dict(visited_source_offsets=visited,source_speech_IDs=[s['id'] for s in speeches])]",
        'assert len(speeches)==len({s[\'id\'] for s in speeches})':'assert len(speeches)==len({s[\'id\'] for s in speeches})==28',
        'after,24000]':'after,16000]','_C281_return_final.png':'_4821_departure_return_final.png',
        'observed_native_composition_matches':'observed_exact_complete_linear_sequence_matches',
        "assert all(any(p['word']==0xC281 and p['decoded_length']==2 for p in g['command_pairs']) for g in groups)":
        "assert all(all(any(p['word']==word and p['decoded_length']==extent for p in g['command_pairs']) for word,extent in [(0x4821,4),(0x4720,2),(0x4681,4),(0xA000,8)]) for g in groups)\n    assert all(g['observed_original_exchange_commands']==37 and not g['original_structural_commands_not_selected'] and not g['native_only_unvisited_speech_IDs'] for g in groups)",
        'paired_source_English_observed_path_complete_pages_names_C281_andreturn.json':'paired_source_English_all28_pages_three_names_4821_departure_andreturn.json',
        'actual_source_English_single_page_speeches_C281_command_andfollowing_return_preserved':'actual_source_English_all28_single_page_speeches_4821_4720_4681_A000_andnormal_return_preserved',
        'actual_total_frames=48002':'actual_total_frames=32002',
        'all61_source_objects_retained_butonly_observed_path_is_actual_gameplay_coverage':'all28_source_speeches_and37_original_commands_actually_selected_in_initialized_fixture',
        'original_ten_command_B44_ROM_entry_fixture_not_natural_B49_activation_original_location_orfullroute':'original_ten_command_B44_ROM_entry_fixture_not_natural_B50_activation_original_location_orfullroute',
        'Observed source/English pages, names and C281 command/return audited;unresolved':'Observed all28 source/English pages,three names and4821/4720/4681/A000/return audited;unresolved',
        '.Actual scope explicitly lists every native-only conditional object;comparison/view/release pending.':'.Actual initialized fixture covers all37 commands;natural eligibility/comparison/view/release pending.',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',receipt)
    print('Prepared B50 actual audit requiring all28 speeches/all37 commands andcomplete glyph/name masks;no coverage assumed.')
