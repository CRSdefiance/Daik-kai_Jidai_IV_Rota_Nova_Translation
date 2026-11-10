"""Bind the sealed 557 review and exact registered Rafael867 predecessor."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

A=Path('work/analysis')
ROOT=A/'Rafael557_research_final_v1_20261105'
RELEASE=A/'Rafael867_extended_release_verified_v3_20261105/registered_release_verification.json'
SPEC=Path('translations/rafael557_registered_successor_spec_v1.json')
REGISTRY=Path('translations/release_stack.json')
MODULE='dk4tool.patch.rafael_story_b141_b160_release_v1'

if __name__=='__main__':
    assert not SPEC.exists()
    release,ready=map(load,[RELEASE,ROOT/'research_completion.json'])
    assert release['registry_sha256']==sha(REGISTRY.read_bytes()) and release['complete_stack_entries']==681
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    for path,digest in ready['evidence'].items():assert sha(Path(path).read_bytes())==digest
    rec=A/'Rafael557_reconstruction_v2_20261105/reconstruction.json';rebuilt=load(rec)
    assert rebuilt['parent_sha256']==release['candidate_sha256']
    evidence=dict(manuscript=ready['manuscript'],plan=ready['plan'],reconstruction=str(rec),
        compiled_native=rebuilt['native'],stored_native=str(A/'Rafael557_stored_native_v3_20261105/stored_native_verification.json'),
        stored_lookup=str(A/'Rafael557_stored_catalogue_v2_20261105/all_stored_effective_body_bindings.json'),
        loaders=str(A/'Rafael557_loaders_v2_20261105/verification.json'),visual_review=str(ROOT/'complete_visual_approval.json'),
        actual=str(ROOT/'actual_review.json'),scoped_names='translations/rafael_B141_B160_scoped_names_final_v1.json',
        typed_menu=rebuilt['menu'],native_styles=rebuilt['styles'],research_completion=str(ROOT/'research_completion.json'))
    stages=['ascii_bounds','emilio_name','fernando_samwell','follower_diogo','geronimo_vasquez_alonso','abkhaz_elysion','shared_tutorial_pedro_hayreddin','Fernan_name_field']
    deps=set(evidence.values())|{str(Path(__file__)),str(RELEASE),
        'scripts/prepare_rafael557_registered_successor_v1.py','scripts/prepare_plain_SC0_registered_successor_v1.py',
        'scripts/source_locked_derivation_v5118.py','dk4tool/patch/reviewed_rafael_plain_scene_release_v1.py',
        'dk4tool/patch/rafael_B51_B60_release_v1.py','dk4tool/patch/reviewed_scene_batch_v5.py',
        'dk4tool/dialogue/reviewed_choice_object_v2.py','dk4tool/script/reviewed_scene_rebuild_with_fu_andcompounds_v1.py',
        'dk4tool/script/reviewed_scene_rebuild_v3.py','dk4tool/script/reviewed_scene_rebuild_v2.py','dk4tool/script/reviewed_scene_rebuild.py'}
    save(SPEC,dict(parent_release=str(RELEASE),previous_profile=release['profile'],expected_registry_sha256=release['registry_sha256'],
        profile='all-routes-rafael1424-prepared-20261105',extension_id='rafael-b141-b160',module=MODULE,
        config='translations/rafael_B141_B160_editorial_release_v1.json',
        stage_configs=['translations/'+s+'_Rafael1424_release_v1.json' for s in stages],
        counts=dict(record_count=557,speech_count=549,typed_choice_count=8,menu_count=4,scoped_name_count=20,native_pages=558,
            relative_cases=1190,FE_count=6,actual_frames=65763,actual_runs=3,actual_speeches=188,actual_body_pages=193,offline_speeches=361),
        evidence=evidence,dependencies=sorted(deps),note='Experimental cumulative Rafael editorial successor: 557 new reviews, 235 revisions and 322 justified retentions. Preserve all 114 accepted layers and eight final stages. No main promotion.'))
    print('Prepared exact successor specification for all 557 reviewed records.')
