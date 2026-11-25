"""Describe the verified 270-record B221–B240 append over registered Rafael2952."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B221_B240_contextual_v1 import REGISTRY, RELEASE
from scripts.finalize_rafael_B221_B240_research_v1 import FINAL_NAMES, LOADERS, LOOKUP, REBUILT, RESEARCH, STORED, digest

SPEC = Path('translations/rafael_B221_B240_registered_successor_spec_v1.json')
STAGES = ('ascii_bounds', 'emilio_name', 'fernando_samwell', 'follower_diogo',
          'geronimo_vasquez_alonso', 'abkhaz_elysion', 'shared_tutorial_pedro_hayreddin', 'Fernan_name_field')


def main():
    assert not SPEC.exists()
    completion = RESEARCH/'research_completion.json'
    release, ready, rebuilt = map(load, (RELEASE, completion, REBUILT))
    assert release['registry_sha256'] == digest(REGISTRY) and release['complete_stack_entries'] == 689
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert release['all_eight_registered_final_stages_preserved']
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'], ready['revisions'], ready['retentions']) == (270,221,49)
    assert all(digest(Path(path)) == checksum for path, checksum in ready['evidence'].items())
    assert rebuilt['parent_sha256'] == release['candidate_sha256']
    evidence = dict(manuscript=ready['manuscript'], plan=ready['plan'], reconstruction=str(REBUILT),
        compiled_native=rebuilt['native'], stored_native=str(STORED), stored_lookup=str(LOOKUP), loaders=str(LOADERS),
        visual_review=str(RESEARCH/'complete_visual_approval.json'), actual=str(RESEARCH/'actual_review.json'),
        scoped_names=str(FINAL_NAMES), typed_menu=rebuilt['menu'], native_styles=rebuilt['styles'],
        research_completion=str(completion))
    dependencies = set(evidence.values()) | {str(Path(__file__)), str(RELEASE),
        'scripts/prepare_rafael557_registered_successor_v1.py', 'scripts/prepare_plain_SC0_registered_successor_v1.py',
        'scripts/source_locked_derivation_v5118.py', 'scripts/finalize_rafael_B221_B240_research_v1.py',
        'scripts/rebuild_rafael_B221_B240_reviewed_v1.py', 'scripts/check_rafael_B221_B240_stored_v1.py',
        'dk4tool/patch/rafael_story_b141_b160_release_v1.py', 'dk4tool/patch/reviewed_rafael_plain_scene_release_v1.py',
        'dk4tool/patch/rafael_B51_B60_release_v1.py', 'dk4tool/patch/reviewed_scene_batch_v5.py',
        'dk4tool/dialogue/reviewed_choice_object_v2.py', 'dk4tool/dialogue/reviewed_two_choice_object_v1.py',
        'dk4tool/dialogue/reviewed_actor_style_object_v1.py', 'dk4tool/script/reviewed_scene_rebuild_with_fu_andcompounds_v1.py',
        'dk4tool/script/reviewed_scene_rebuild_v3.py', 'dk4tool/script/reviewed_scene_rebuild_v2.py',
        'dk4tool/script/reviewed_scene_rebuild.py'}
    save(SPEC, dict(parent_release=str(RELEASE), previous_profile=release['profile'],
        expected_registry_sha256=release['registry_sha256'], profile='all-routes-rafael3222-prepared-20261106',
        extension_id='rafael-b221-b240', module='dk4tool.patch.rafael_story_b221_b240_release_v1',
        config='translations/rafael_B221_B240_editorial_release_v1.json',
        stage_configs=[f'translations/{stage}_Rafael3222_release_v1.json' for stage in STAGES],
        counts=dict(record_count=270, speech_count=263, typed_choice_count=7, menu_count=3, style_count=29,
            scoped_name_count=26, native_pages=279, relative_cases=170, FE_count=3, actual_frames=33202, actual_runs=2,
            actual_speeches=86, actual_body_pages=94, actual_choice_labels=7, offline_speeches=177),
        evidence=evidence, dependencies=sorted(dependencies),
        note='Experimental cumulative Rafael and town dialogue successor with 221 revisions and 49 justified retentions. '
             'All accepted layers and eight registered final stages are preserved.'))
    print('Wrote the exact mixed Rafael B221–B240 registered successor specification.')


if __name__ == '__main__':
    main()

