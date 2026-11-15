"""Describe the 67 reviewed speeches over the verified 683-entry predecessor."""
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

A = Path('work/analysis')
ROOT = A / 'Rafael_B161_B165_research_final_v1_20261105'
RELEASE = A / 'Rafael1607_extended_release_verified_v1_20261105/registered_release_verification.json'
RECONSTRUCTION = A / 'Rafael_B161_B165_reconstruction_v1_20261105/reconstruction.json'
SPEC = Path('translations/rafael_B161_B165_registered_successor_spec_v2.json')
REGISTRY = Path('translations/release_stack.json')

if __name__ == '__main__':
    assert not SPEC.exists()
    completion = ROOT / 'research_completion.json'
    release, ready, rebuilt = map(load, (RELEASE, completion, RECONSTRUCTION))
    assert release['registry_sha256'] == sha(REGISTRY.read_bytes()) and release['complete_stack_entries'] == 683
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'], ready['revisions'], ready['retentions']) == (67, 51, 16)
    for path, digest in ready['evidence'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert rebuilt['parent_sha256'] == release['candidate_sha256']
    evidence = dict(manuscript=ready['manuscript'], plan=ready['plan'], reconstruction=str(RECONSTRUCTION),
        compiled_native=rebuilt['native'], stored_native=str(A/'Rafael_B161_B165_stored_v1_20261105/stored_native_verification.json'),
        stored_lookup=str(A/'Rafael_B161_B165_stored_catalogue_v1_20261105/all67_stored_effective_body_bindings.json'),
        loaders=str(A/'Rafael_B161_B165_loaders_v1_20261105/verification.json'), visual_review=str(ROOT/'complete_visual_approval.json'),
        actual=str(ROOT/'actual_review.json'), scoped_names='translations/rafael_B161_B165_scoped_names_final_v1.json',
        typed_menu=rebuilt['menu'], native_styles=rebuilt['styles'], research_completion=str(completion))
    dependencies = set(evidence.values()) | {str(Path(__file__)), str(RELEASE),
        'scripts/prepare_rafael557_registered_successor_v1.py', 'scripts/prepare_plain_SC0_registered_successor_v1.py',
        'scripts/source_locked_derivation_v5118.py', 'dk4tool/patch/rafael_story_b141_b160_release_v1.py',
        'dk4tool/patch/reviewed_rafael_plain_scene_release_v1.py', 'dk4tool/patch/rafael_B51_B60_release_v1.py',
        'dk4tool/patch/reviewed_scene_batch_v5.py', 'scripts/rebuild_rafael_B161_B165_reviewed_v1.py',
        'dk4tool/script/reviewed_scene_rebuild_with_fu_andcompounds_v1.py', 'dk4tool/script/reviewed_scene_rebuild_v3.py',
        'dk4tool/script/reviewed_scene_rebuild_v2.py', 'dk4tool/script/reviewed_scene_rebuild.py'}
    stages = ['ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso',
        'abkhaz_elysion','shared_tutorial_pedro_hayreddin','Fernan_name_field']
    save(SPEC, dict(parent_release=str(RELEASE), previous_profile=release['profile'],
        expected_registry_sha256=release['registry_sha256'], profile='all-routes-rafael1674-prepared-20261105',
        extension_id='rafael-b161-b165', module='dk4tool.patch.rafael_story_b161_b165_release_v2',
        config='translations/rafael_B161_B165_editorial_release_v2.json',
        stage_configs=['translations/'+stage+'_Rafael1674_release_v2.json' for stage in stages],
        counts=dict(record_count=67, speech_count=67, typed_choice_count=0, menu_count=0, scoped_name_count=8, native_pages=68,
            relative_cases=100, FE_count=1, actual_frames=18401, actual_runs=1, actual_speeches=55, actual_body_pages=56, offline_speeches=12),
        evidence=evidence, dependencies=sorted(dependencies),
        note='Experimental cumulative Rafael successor with 51 revisions and 16 justified retentions. All accepted layers and eight final stages retained.'))
    print('Wrote the exact five-block successor specification.')
