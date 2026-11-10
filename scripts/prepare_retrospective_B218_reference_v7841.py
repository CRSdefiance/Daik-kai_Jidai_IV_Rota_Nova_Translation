"""Prepare a pinned one-block research image from the verified registered checkpoint."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/retrospective_B218_reference_tools_v7841');assert not root.exists()
    result=derive('scripts/create_lil_B218_reference_v6896.py','scripts/create_retrospective_B218_reference_v7841.py',{
        'work/analysis/lil_B218_reference_v6896':'work/analysis/retrospective_B218_reference_v7841',
        'work/analysis/lil_B218_relocation_v6894/all13_objects15_commands_full1088_inverse_RESEARCH.json':
        'work/analysis/retrospective_B218_relocation_v7839b/all13_bound_one_changed_wrap15_commands_complete_clean_predecessor_inverse.json',
        'work/analysis/lil_B218_stored_v6895/all13_final_stored_targets52_alignments13_complete_pages.json':
        'work/analysis/retrospective_B218_stored_controls_v7840/one_changed_stored_plane13_dispatches_A00025_ends_andtwo_sheets_viewed.json',
        'out/all_routes_combined_v6865_candidate.nds':'out/all_routes_combined_v7821_candidate.nds',
        'out/lil_B218_reference_v6896_RESEARCH_ONLY.nds':'out/lil_B218_wrap_reference_v7841_RESEARCH_ONLY.nds',
        "stored['relocation_plan_sha256']":"stored['relocation_map_sha256']",
        "stored['all_final_stored_targets_equal_reviewed_complete_native_ink']":"stored['changed_parity_tail_zero_ink_complete_characters_bounds_andconsumption']",
        "plan['target_SC2']":"plan['target_archive']",
        "plan['target_SC2_sha256']":"plan['target_archive_sha256']",
        "plan['source_SC2_sha256']":"plan['source_archive_sha256']",
        'B218 thirteen whole-exchange speeches,thirteen native pages,zero macros,no relative/predicate/typed controls,oneA000 and normal end;all1088 predecessor bytes reversible,name assets unchanged.':
        'B218 retrospective R27 automatic-wrap research;13 source-bound speeches/15 original commands,one fresh changed native page/12 unchanged stored bodies,no relatives;complete1016-byte predecessor block inverse,name assets unchanged.',
        'V6865/mainV4701':'V7821/mainV4701',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        registered_parent_V7821_only_one_changed_block=True,all_previous_ROMs_andpins_preserved=True,
        not_registered_release_ornew_current_parent=True,new_credit=0,full_goal_complete=False))
