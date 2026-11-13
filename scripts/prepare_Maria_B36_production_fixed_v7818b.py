"""Freeze the validated atomic production path against the single sealed B36 exchange."""
import ast
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B36_production_tools_v7818b')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('dk4tool/patch/maria_story_editorial_v3.py').read_text('utf8')
    node=next(n for n in ast.parse(source).body if isinstance(n,ast.FunctionDef) and n.name=='late_summary')
    previous=ast.get_source_segment(source,node)
    replacement="""def late_summary(group):
    return dict(source_English_exits=group['source_English_exits'],command_difference_rows=len(group['command_comparison_differences']),
        duration_difference_rows=len(group['duration_differences']),later_RGB_differences=len(group['later_RGB_differences']),
        later_samples=group['later_sample_count'],five_component_equality=group['five_native_component_equality'],
        whole_actor_equality=group['whole_actors_equal'],final_PRNG_seeds=group['final_PRNG_seeds'])"""
    a=derive('dk4tool/patch/maria_story_editorial_v3.py','dk4tool/patch/maria_B36_editorial_v1.py',{
        previous:replacement,
        'maria_story_profile_v1':'maria_B36_profile_v1',
        'maria_story_layout_v1':'maria_B36_layout_v2',
        'Maria_story_final_paths_v7771':'Maria_B36_final_paths_v7816b',
        'seal_Maria_story_references_v7772':'seal_Maria_B36_references_v7817b',
        'translations/maria_story_editorial_release_v1.json':'translations/maria_B36_editorial_release_v1.json',
        'dk4-Maria67-editorial-release-v1':'dk4-Maria16-B36-editorial-release-v1',
        'dk4-Maria67-source-relocation-map-v1':'dk4-Maria16-B36-source-relocation-map-v1',
        '[34,108,35]':'[36]',
        'all67_five_gates_andexact_references_approved':'all16_five_gates_andexact_references_approved',
        'all67_single_native_four_row_pages_complete_glyph_bounds_andconsumption':'all16_single_native_pages_complete_glyph_bounds_canaries_andconsumption',
        "font['final_complete_pages']==67":"font['final_complete_pages']==16",
        "font['exact_own_current_compiled_alignment_cases_reused']==268":"font['exact_own_current_compiled_alignment_cases_reused']==64",
        "stored['stored_alignment_coverage']==268 and stored['zero_ink_parity_tails']==33 and stored['final_complete_native_pages']==67 and stored['all67_final_stored_targets_equal_reviewed_complete_native_ink']":
        "stored['stored_alignment_cases']==64 and stored['zero_ink_parity_tail_count']==11 and stored['complete_stored_native_pages']==16 and stored['all16_stored_targets_equal_reviewed_complete_native_ink']",
        "policy['positive_count']==len(policy['positive_cases'])==67 and policy['negative_count']==len(policy['negative_cases'])==200":
        "policy['positive_count']==len(policy['positive_cases'])==16 and policy['negative_count']==len(policy['negative_cases'])==81",
        "view['all130_final_actual_panes_viewed_with_exact_reuse'] and view['complete_body_andheader_holds']==528 and view['shared155_Sailor_Retainer_review_open_no_global_name_asset_change']":
        "view['all9_actual_transition_late_sheets_individually_viewed'] and view['complete_body_andheader_holds']==132 and view['all207_name_role_alias_and151_159_review_remain_open']",
        "actual['total_actual_speech_occurrences']==actual['complete_actual_page_panels']==130":
        "actual['total_actual_speech_occurrences']==actual['complete_actual_page_panels']==32",
        "len(actual['groups'])==6 and sum(g['complete_body_andheader_holds'] for g in actual['groups'])==528":
        "len(actual['groups'])==2 and sum(g['complete_body_andheader_holds'] for g in actual['groups'])==132",
        '{34:8,108:29,35:28}':'{36:16}','{34:30,108:49,35:47}':'{36:29}',
        "len(later['groups'])==3":"len(later['groups'])==1",
        "require([late_summary(g) for g in later['groups']]==view['final_late_limits']==mapping['observed_comparison_contract'],'full measured comparison contract')":
        "observed=late_summary(later['groups'][0]);require(observed=={key:view[key] for key in observed}==mapping['observed_comparison_contract'],'full measured comparison contract')",
        'expected=[(34,[6295,6295],7,0,0,163),(108,[11336,11335],37,13,60,79),(35,[11335,11334],35,8,60,79)]':
        'expected=[(36,[8213,8216],18,6,108,131)]',
        "names['seven_actual_distinct_speaker_headers_seen_Julian26_offline_only'] and names['all207_name_role_alias_review_active'] and names['shared155_label_semantic_review_still_unresolved_no_asset_edit']":
        "names['all_three_selected_progressive_headers_actually_observed'] and names['all207_name_role_alias_review_active'] and names['no_name_asset_edit_orfull207_shared_role_semantic_approval']",
        "len(branches['operands_requiring_adjustment_when_resizing'])==20":"len(branches['operands_requiring_adjustment_when_resizing'])==0",
        "branches['native_cases']==200 and branches['complete_nested0100_and0200_0300_branch_targets_are_mapped_native_boundaries']":
        "branches['original_source_andcurrent_complete_native_command_lists_bound'] and branches['source_current_relative_andinblock_predicate_commands']==0",
        "entry['source_completion_dependency_chain']==[34,108,35] and len(entry['native_predicate_cases'])==10":
        "entry['source_completion_dependency_chain']==[35,36] and len(entry['native_predicate_cases'])==0",
        '[(34,35,34,[],[]),(35,36,35,[108],[]),(108,109,108,[34],[])]':'[(36,37,36,[35],[])]',
        "len(rows)==len({r['id'] for r in rows})==67 and Counter(r['editorial_decision'] for r in rows)=={'revise':48,'retain-wording':19}":
        "len(rows)==len({r['id'] for r in rows})==16 and Counter(r['editorial_decision'] for r in rows)=={'revise':9,'retain-wording':7}",
        "set(bindings)-set(panels)=={'DK4_MES_B108_R0020','DK4_MES_B108_R0125'}":"set(bindings)==set(panels)",
        '==[34,35,108]':'==[36]',
        'three original Maria entries':'one original Maria entry','six actual groups/holds':'two actual groups/holds',
        'three measured comparison groups':'one measured comparison group','67 unique decisions':'16 unique decisions',
        'all native sets andtwo unplayed conditionals':'all16 native andactual record sets',
        'only three owned blocks':'only the owned B36 block',
        'three_clean_predecessor_blocks_andarchive_inverse_exact':'complete_clean_predecessor_block_andarchive_inverse_exact',
        'all67_original_preambles_macros_controls_andsingle_native_pages_preserved':'all16_original_preambles_macros_controls_andsingle_native_pages_preserved',
        'actual65_eachlanguage_two_offline_Julian_conditions_andshared_name_scope_preserved':'actual16_eachlanguage_all_speeches_andshared_name_scope_preserved',
    })
    b=derive('scripts/validate_Maria_story_atomic_v7775c.py','scripts/validate_Maria_B36_atomic_v7818b.py',{
        'maria_story_editorial_v3':'maria_B36_editorial_v1','Maria_story_final_paths_v7771':'Maria_B36_final_paths_v7816b',
        'maria_story_atomic_v7775c':'maria_B36_atomic_v7818b',
        'maria_story_profile_v1':'maria_B36_profile_v1','maria_story_layout_v1':'maria_B36_layout_v2',
        'maria_story_plan_v1':'maria_B36_plan_v2','seal_Maria_story_references_v7772':'seal_Maria_B36_references_v7817b',
        'dk4-Maria67-editorial-release-v1':'dk4-Maria16-B36-editorial-release-v1',
        "len(proof['changed_records'])==67":"len(proof['changed_records'])==16",
        'positive_records=67':'positive_records=16',
        'three_clean_predecessor_blocks_andwhole_archive_inverse_exact':'complete_clean_predecessor_block_andwhole_archive_inverse_exact',
        '67-record atomic positive':'16-record atomic positive',
    })
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivations=[a,b],
        all_original_native_high_constants_source_identity_atomic_commit_andfull_inverse_guards_preserved=True,
        new_scope_from_exact_B36_source_native_actual_andsealed_proofs_not_prior67_orbranch_counts=True,
        original_pure_reconstruction_helper_reused_unchanged=True,new_credit=0,full_goal_complete=False))
