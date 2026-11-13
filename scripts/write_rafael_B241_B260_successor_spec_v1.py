"""Prepare the reviewed dialogue transaction without changing the release registry."""
from pathlib import Path

from dk4tool.patch.rafael_story_b241_b260_release_v1 import qualify_evidence
from scripts.assemble_rafael_B241_B260_offline_v2 import OUT, ROOT, digest
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B241_B260_research_v1 import READY
from scripts.save_rafael3222_weekend_checkpoint_v1 import RELEASE
from scripts.write_rafael_B221_B240_successor_spec_v1 import STAGES


SPEC = Path('translations/rafael_B241_B260_registered_successor_spec_v1.json')
REGISTRY = Path('translations/release_stack.json')
REBUILT = ROOT / 'reconstruction_v1/reconstruction.json'
FIELD = ROOT / 'Francisca_name_field_v1/owned_fields_proposal.json'


def main():
    assert not SPEC.exists()
    release, ready, rebuilt = map(load, (RELEASE, READY, REBUILT))
    assert release['registry_sha256'] == digest(REGISTRY) and release['complete_stack_entries'] == 690
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert release['all_eight_registered_final_stages_preserved']
    assert release['candidate_sha256'] == digest(release['candidate']) == rebuilt['parent_sha256']
    assert digest(release['manifest']) == release['manifest_sha256']
    assert ready['all_individual_five_gates_pass'] and ready['registered_integration_pending']
    for path, checksum in ready['evidence'].items():
        assert digest(path) == checksum
    evidence = dict(manuscript=ready['manuscript'], plan=ready['plan'], reconstruction=str(REBUILT),
        compiled_native=rebuilt['native'], stored_native=str(ROOT/'stored_v1/stored_native_verification.json'),
        stored_lookup=str(ROOT/'stored_catalogue_all_v1/all286_stored_effective_body_bindings.json'),
        loaders=str(ROOT/'loaders_v1/verification.json'), visual_review=str(READY.with_name('complete_visual_approval.json')),
        actual=str(READY.with_name('actual_review.json')),
        scoped_names=str(Path('translations/rafael_B241_B260_scoped_names_final_v1.json')),
        typed_menu=str(OUT/'menu.json'), native_styles=str(OUT/'styles.json'), research_completion=str(READY))
    counts = dict(record_count=292, speech_count=286, typed_choice_count=6, menu_count=3, style_count=14,
        scoped_name_count=20, native_pages=294, relative_cases=120, FE_count=7, actual_frames=48003, actual_runs=3,
        actual_speeches=132, actual_body_pages=135, actual_choice_labels=6, offline_speeches=154)
    qualify_evidence({**evidence, **counts, 'final_dependency_ROM': release['candidate'],
        'final_dependency_ROM_sha256': release['candidate_sha256'],
        'final_runtime_ARM9_sha256': load(evidence['compiled_native'])['runtime']['ARM9_sha256']},
        load(evidence['manuscript']), load(evidence['stored_native']))
    # This transaction owns SC0 only. The exclusive Francisca field has its
    # own native proof and must pass separately before combined delivery.
    field = load(FIELD)
    assert field['runtime']['candidate_sha256'] == release['candidate_sha256']
    assert [row['actor'] for row in field['fields']] == [186]
    previous = load('translations/rafael_B221_B240_registered_successor_spec_v1.json')
    dependencies = {p for p in previous['dependencies'] if 'B221_B240' not in p and 'Rafael2952_' not in p}
    dependencies.update(evidence.values())
    dependencies.update(map(str, (RELEASE, Path(__file__))))
    dependencies.update({'scripts/finalize_rafael_B241_B260_research_v1.py',
        'scripts/rebuild_rafael_B241_B260_reviewed_v1.py', 'scripts/check_rafael_B241_B260_stored_v1.py',
        'dk4tool/patch/rafael_story_b221_b240_release_v1.py', 'dk4tool/patch/rafael_story_b241_b260_release_v1.py'})
    save(SPEC, dict(parent_release=str(RELEASE), previous_profile=release['profile'],
        expected_registry_sha256=release['registry_sha256'], profile='all-routes-rafael3514-dialogue-prepared-20261106',
        extension_id='rafael-b241-b260', module='dk4tool.patch.rafael_story_b241_b260_release_v1',
        config='translations/rafael_B241_B260_editorial_release_v1.json',
        stage_configs=[f'translations/{stage}_Rafael3514_dialogue_v1.json' for stage in STAGES],
        counts=counts, evidence=evidence, dependencies=sorted(dependencies),
        note='Verified SC0 transaction for 244 revisions and 48 retentions. The existing eight final stages are preserved.',
        paired_exclusive_name_field=str(FIELD), paired_exclusive_name_field_sha256=digest(FIELD),
        paired_name_field_requires_separate_registration=True))
    assert digest(REGISTRY) == release['registry_sha256']
    print('Qualified the 292-record dialogue transaction specification. Registry unchanged.')


if __name__ == '__main__':
    main()
