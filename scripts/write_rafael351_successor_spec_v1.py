"""Bind the reviewed351 batch to the now verified516 cumulative predecessor."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha


if __name__ == '__main__':
    path = Path('translations/rafael351_registered_successor_spec_v1.json')
    assert not path.exists()
    parent = 'work/analysis/Rafael516_resume_release_verified_v2_20261105/registered_release_verification.json'
    release = load(parent)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    evidence = dict(
        manuscript='translations/rafael_B121_B140_cumulative867_refs_v2.json',
        plan='work/analysis/Rafael351_final_metadata_v2_20261105/cumulative_release_plans.json',
        reconstruction='work/analysis/Rafael351_final_metadata_v2_20261105/cumulative_reconstruction.json',
        compiled_native='work/analysis/Rafael351_storage_inputs_v1_20261105/native.json',
        stored_native='work/analysis/Rafael351_stored_native_v1_20261105/stored_native_verification.json',
        stored_lookup='work/analysis/Rafael351_stored_catalogue_v1_20261105/all_stored_effective_body_bindings.json',
        loaders='work/analysis/Rafael351_loaders_v1_20261105/verification.json',
        visual_review='work/analysis/Rafael351_checked_v1_20261105/complete_visual_approval.json',
        actual='work/analysis/Rafael351_checked_v1_20261105/actual_review.json',
        scoped_names='translations/rafael_B121_B140_scoped_names_final_v2.json',
        typed_menu='work/analysis/Rafael351_storage_inputs_v1_20261105/menu.json',
        native_styles='work/analysis/Rafael351_storage_inputs_v1_20261105/styles.json',
        focused_pixels='work/analysis/Rafael351_tutorial_actual_pixels_v1_20261105/focused_actual_pixels.json',
        menu_body_pixels='work/analysis/Rafael351_story_actual_pixels_v1_20261105/focused_actual_pixels.json',
        tutorial_menu_pixels='work/analysis/Rafael351_tutorial_menu_pixels_v1_20261105/menu_actual_pixels.json',
        story_menu_pixels='work/analysis/Rafael351_story_menu_pixels_v1_20261105/menu_actual_pixels.json',
        dependency_qualification='work/analysis/Rafael867_combined_research_v1_20261105/dependency_reuse.json',
        metadata_qualification='work/analysis/Rafael351_final_metadata_v2_20261105/qualification.json',
        research_reconstruction='work/analysis/Rafael351_rebuilt678_v2_20261105/reconstruction.json')
    stages = ['ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso',
              'abkhaz_elysion','shared_tutorial_pedro_hayreddin','Fernan_name_field']
    dependencies = set(evidence.values()) | {str(Path(__file__)), parent,
        'dk4tool/patch/rafael_story_b121_b140_release_v1.py', 'scripts/prepare_rafael351_registered_successor_v1.py',
        'scripts/prepare_plain_SC0_registered_successor_v1.py', 'scripts/source_locked_derivation_v5118.py',
        'dk4tool/patch/rafael_story_b101_b120_release_v1.py', 'dk4tool/patch/reviewed_rafael_plain_scene_release_v1.py',
        'dk4tool/patch/rafael_B51_B60_release_v1.py', 'dk4tool/dialogue/reviewed_actor_style_object_v1.py',
        'dk4tool/dialogue/reviewed_two_choice_object_v1.py', 'dk4tool/script/reviewed_scene_rebuild_v3.py',
        'work/analysis/Rafael351_final_metadata_v2_20261105/research_completion.json'}
    save(path, dict(parent_release=parent, previous_profile=release['profile'],
        expected_registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        profile='all-routes-rafael867-v1-20261105', extension_id='rafael-b121-b140',
        module='dk4tool.patch.rafael_story_b121_b140_release_v1', config='translations/rafael_B121_B140_editorial_release_v1.json',
        stage_configs=['translations/'+s+'_Rafael867_release_v1.json' for s in stages],
        counts=dict(record_count=351,speech_count=341,typed_choice_count=10,menu_count=5,scoped_name_count=22,
            native_pages=344,relative_cases=405,FE_count=15,actual_frames=43282,actual_runs=2,actual_speeches=132,
            actual_body_pages=134,offline_speeches=209), evidence=evidence, dependencies=sorted(dependencies),
        note='Experimental cumulative867 reviews afterverified516;351 new source reviews,201 revisions/150 retentions. Preserveall114 accepted layers/eight final stages andfull scope. No promotion ornew credit beforefinal verification.'))
    print('Wrote351 registered successor specification againstverified516;all prior research bindings retained.')
