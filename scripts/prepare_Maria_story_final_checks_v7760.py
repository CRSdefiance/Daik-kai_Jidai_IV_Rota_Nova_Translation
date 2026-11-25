"""Source-lock final-v3 reference, original loaders, callers and two affected fixtures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/maria_story_final_check_tools_v7760');assert not root.exists()
    results=[]
    results.append(derive('scripts/create_Maria_story_reference_v7746.py','scripts/create_Maria_story_reference_v7760.py',{
        'maria_story_reference_v7746':'maria_story_reference_v7760',
        'work/analysis/maria_story_relocation_v7742/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json':'work/analysis/maria_story_final_relocation_v7758/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json',
        'work/analysis/maria_story_stored_v7743/67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json':'work/analysis/maria_story_final_stored_v7759/67_final_v3_stored_pages33_tails_two_new_dispatches65_exact_reuse.json',
        'work/analysis/maria_story_native_view_v7739/67_complete_paragraphs68_native_pages12_sheets_viewed.json':'work/analysis/maria_story_final_native_v7757b/67_final_v3_native_pages_andfully_bound_logical_lineage.json',
        "stored['all67_stored_targets_equal_reviewed_complete_native_ink']":"stored['all67_final_stored_targets_equal_reviewed_complete_native_ink']",
        "view['all12_sheets_individually_viewed']":"view['all67_single_native_four_row_pages_complete_glyph_bounds_andconsumption']",
        '68 reviewed complete native pages':'67 complete final-v3 native pages',
    }))
    results.append(derive('scripts/verify_Maria_story_loaders_v7747.py','scripts/verify_Maria_story_loaders_v7761.py',{
        'create_Maria_story_reference_v7746':'create_Maria_story_reference_v7760',
        'maria_story_loaders_v7747':'maria_story_loaders_v7761',
        'maria_story_reference_v7746/research_image_receipt':'maria_story_reference_v7760/research_image_receipt',
    }))
    results.append(derive('scripts/verify_Maria_story_references_v7748.py','scripts/verify_Maria_story_references_v7762.py',{
        'create_Maria_story_reference_v7746':'create_Maria_story_reference_v7760',
        'maria_story_reference_census_v7748':'maria_story_reference_census_v7762',
        'maria_story_loaders_v7747':'maria_story_loaders_v7761',
    }))
    results.append(derive('scripts/create_Maria_story_scene_fixtures_v7749.py','scripts/create_Maria_story_scene_fixtures_v7763.py',{
        'create_Maria_story_reference_v7746':'create_Maria_story_reference_v7760',
        'maria_story_scene_fixtures_v7749':'maria_story_scene_fixtures_v7763',
        'maria_story_reference_census_v7748':'maria_story_reference_census_v7762',
        "g in mapping['groups'] for v in ['clean_Japanese','English']":"g in mapping['groups'] if g['block'] in [34,108] for v in ['English']",
        "for version in ['clean_Japanese','English']:":"if g['block']==35:continue\n        for version in ['English']:",
        "_v7749_RESEARCH_ONLY.nds":"_v7763_RESEARCH_ONLY.nds",
        'values[:-6]':'values[:-2]',
        'six_complete_source_English_original_prelude_fixtures.json':'two_final_English_original_prelude_fixtures.json',
        'all_three_full_exchanges67_positions_preserved_in_both_languages=True':'two_affected_final_English_exchanges39_positions_preserved=True',
        "'Six pinned full source/English original-prelude fixtures ready. No new actual gameplay claim until captures complete.'":"'Two pinned final-v3 English fixtures ready;all prior source andEnglishB35 artifacts preserved.No actual claim until capture.'",
    }))
    results.append(derive('scripts/run_Maria_story_scenes_v7750.py','scripts/run_Maria_story_scenes_v7764.py',{
        'maria_story_scene_runs_v7750':'maria_story_scene_runs_v7764',
        'maria_story_scene_fixtures_v7749/six_complete_source_English_original_prelude_fixtures':'maria_story_scene_fixtures_v7763/two_final_English_original_prelude_fixtures',
        "choices=['clean_Japanese','English']":"choices=['English']",
        'choices=[34,108,35]':'choices=[34,108]',
        'Maria_story_B{block}_route{route}_{version}_v7750':'Maria_story_B{block}_route{route}_{version}_v7764',
    }))
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivations=results,
        all_native_high_constants_and_original_ABI_guards_preserved=True,
        two_changed_English_scenes_only_no_repeat_of_three_source_orunchanged_EnglishB35_runs=True,
        original_inputs_unlock_andall_prior_artifacts_preserved=True,
        no_registered_build_ledger_credit_orpromotion_change=True,full_goal_complete=False))
    print('Final-v3 reference/loaders/callers andtwo affected English fixture adapters frozen;all native numeric guards exact.')
