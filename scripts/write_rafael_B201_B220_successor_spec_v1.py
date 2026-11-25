"""Describe the source-bound B201–B220 append over the verified Rafael2549 parent."""
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finalize_rafael_B201_B220_research_v1 import (
    CATALOGUE, FINAL_NAMES, LOADERS, REBUILT, ROOT, STORED, checksum,
)


RELEASE=Path('work/analysis/Rafael2549_extended_release_verified_v1_20261106/registered_release_verification.json')
SPEC=Path('translations/rafael_B201_B220_registered_successor_spec_v1.json')
REGISTRY=Path('translations/release_stack.json')
KEY='Rafael2952'
STAGES=('ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso',
    'abkhaz_elysion','shared_tutorial_pedro_hayreddin','Fernan_name_field')


def main():
    assert not SPEC.exists()
    completion=ROOT/'research_completion.json'
    release,ready,rebuilt,actual=map(load,(RELEASE,completion,REBUILT,ROOT/'actual_review.json'))
    assert release['registry_sha256']==checksum(REGISTRY) and release['complete_stack_entries']==688
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    assert (ready['records'],ready['revisions'],ready['retentions'])==(403,299,104)
    assert all(checksum(path)==digest for path,digest in ready['evidence'].items())
    assert rebuilt['parent_sha256']==release['candidate_sha256']
    evidence=dict(manuscript=ready['manuscript'],plan=ready['plan'],reconstruction=str(REBUILT),
        compiled_native=rebuilt['native'],stored_native=str(STORED),stored_lookup=str(CATALOGUE),loaders=str(LOADERS),
        visual_review=str(ROOT/'complete_visual_approval.json'),actual=str(ROOT/'actual_review.json'),
        scoped_names=str(FINAL_NAMES),typed_menu=rebuilt['menu'],native_styles=rebuilt['styles'],research_completion=str(completion))
    dependencies=set(evidence.values()) | {str(Path(__file__)),str(RELEASE),
        'scripts/prepare_rafael557_registered_successor_v1.py','scripts/prepare_plain_SC0_registered_successor_v1.py',
        'scripts/source_locked_derivation_v5118.py','dk4tool/patch/rafael_story_b141_b160_release_v1.py',
        'dk4tool/patch/reviewed_rafael_plain_scene_release_v1.py','dk4tool/patch/rafael_B51_B60_release_v1.py',
        'dk4tool/patch/reviewed_scene_batch_v5.py','scripts/rebuild_rafael_B201_B220_reviewed_v1.py',
        'scripts/check_rafael_B201_B220_stored_v1.py','scripts/finalize_rafael_B201_B220_research_v1.py',
        'dk4tool/dialogue/reviewed_choice_object_v2.py','dk4tool/dialogue/reviewed_two_choice_object_v1.py',
        'dk4tool/script/reviewed_scene_rebuild_with_fu_andcompounds_v1.py','dk4tool/script/reviewed_scene_rebuild_v3.py',
        'dk4tool/script/reviewed_scene_rebuild_v2.py','dk4tool/script/reviewed_scene_rebuild.py'}
    save(SPEC,dict(parent_release=str(RELEASE),previous_profile=release['profile'],expected_registry_sha256=release['registry_sha256'],
        profile='all-routes-rafael2952-prepared-20261106',extension_id='rafael-b201-b220',
        module='dk4tool.patch.rafael_story_b201_b220_release_v1',config='translations/rafael_B201_B220_editorial_release_v1.json',
        stage_configs=[f'translations/{stage}_{KEY}_release_v1.json' for stage in STAGES],
        counts=dict(record_count=403,speech_count=382,typed_choice_count=21,menu_count=10,scoped_name_count=41,native_pages=383,
            relative_cases=520,FE_count=34,actual_frames=58083,actual_runs=3,actual_speeches=173,actual_body_pages=174,
            actual_choice_labels=13,offline_speeches=209),
        evidence=evidence,dependencies=sorted(dependencies),
        note='Experimental cumulative Rafael and town dialogue successor with 299 revisions and 104 justified retentions. All accepted layers and eight final stages retained.'))
    print('Wrote the exact B201–B220 successor specification.')


if __name__=='__main__':
    main()

