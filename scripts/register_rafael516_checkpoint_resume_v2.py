"""Register only a manifest-spelling repair and an exact canonical-checkpoint resume."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_canonical_checkpoint_resume_v1 import STAGES, qualify, stage_source


def main():
    root = Path('work/analysis/Rafael516_registered_resume_v2_20261105')
    config_path = Path('translations/rafael516_canonical_checkpoint_resume_v2.json')
    bounds_path = Path('translations/ascii_bounds_Rafael516_release_v2.json')
    registry_path = Path('translations/release_stack.json')
    before = registry_path.read_bytes()
    assert sha(before) == '9bc4dd5e408f4e474844d25b1602d2cc4560db371d7c5ee4a92af8b3753cc6c9'
    assert not any(p.exists() for p in [root, config_path, bounds_path])
    correction_path = Path('work/analysis/Rafael516_canonical_contract_v2_20261105/qualification.json')
    correction = load(correction_path)
    prior_prep_path = Path('work/analysis/Rafael516_registered_preparation_v1_20261105/registered_preparation.json')
    prior_qual_path = Path('work/analysis/Rafael516_release_qualification_v1_20261105/qualification.json')
    prep, qualification = map(load, [prior_prep_path, prior_qual_path])
    assert qualification['preparation_sha256'] == sha(prior_prep_path.read_bytes())
    assert len(qualification['changed_scope_andordering_rejections']) == 10
    assert qualification['direct_prepublication_andshared_targets_equal']
    stack = load(registry_path)
    profile_name = 'all-routes-rafael516-checkpoint-v2-20261105'
    old_profile = stack['profiles'][prep['profile']]
    assert profile_name not in stack['profiles']
    bounds = load(old_profile['ascii_glyph_right_bounds'])
    bounds['parent_manifest'] = correction['corrected_contract']
    profile = deepcopy(old_profile)
    profile.update(ascii_glyph_right_bounds=str(bounds_path), canonical_checkpoint_resume=str(config_path))
    stack['profiles'][profile_name] = profile
    root.mkdir(parents=True)
    (root / 'release_stack_before.json').write_bytes(before)
    save(bounds_path, bounds)
    dependencies = [Path(__file__), Path('scripts/registered_canonical_checkpoint_resume_v1.py'),
        correction_path, Path(correction['corrected_contract']), Path(correction['canonical_manifest']),
        prior_prep_path, prior_qual_path, Path(correction['original_terminal']),
        *[Path('scripts/resume_integrated_release_with_' + s + '_v1.py') for s in STAGES]]
    config = dict(configuration=str(config_path), profile=profile_name, source_profile=prep['profile'],
        previous_registry=str(root / 'release_stack_before.json'), previous_registry_sha256=sha(before),
        canonical_ROM=correction['canonical_stage'], canonical_ROM_sha256=correction['canonical_stage_sha256'],
        canonical_manifest=correction['canonical_manifest'], qualified_expected_contract=correction['corrected_contract'],
        original_build_terminal=correction['original_terminal'], separator_qualification=str(correction_path),
        new_bounds_configuration=str(bounds_path),
        dependencies={str(p): sha(p.read_bytes()) for p in dependencies},
        expected_final_ROM_sha256=prep['target_ROM_sha256'], expected_final_manifest_entries=680,
        no_new_source_wording_orROM_layer=True, all_eight_final_stages_required=True, new_credit=0)
    save(config_path, config)
    positive = qualify(config, stack)
    negatives = []
    for kind in ['wrong-canonical-ROM-hash', 'wrong-source-profile', 'missing-resume-registration',
                 'changed-accepted-layer', 'changed-existing-profile', 'changed-final-stage-configuration',
                 'changed-extension-order', 'wrong-canonical-manifest', 'wrong-qualified-contract',
                 'wrong-dependency-digest']:
        bad, badstack = deepcopy(config), deepcopy(stack)
        if kind == 'wrong-canonical-ROM-hash': bad['canonical_ROM_sha256'] = '0' * 64
        elif kind == 'wrong-source-profile': bad['source_profile'] = prep['previous_profile']
        elif kind == 'missing-resume-registration': del badstack['profiles'][profile_name]['canonical_checkpoint_resume']
        elif kind == 'changed-accepted-layer': badstack['accepted_layers'] = []
        elif kind == 'changed-existing-profile': badstack['profiles'][prep['profile']]['note'] += ' altered'
        elif kind == 'changed-final-stage-configuration': badstack['profiles'][profile_name]['owned_Fernan_name_field'] = 'wrong.json'
        elif kind == 'changed-extension-order': badstack['profiles'][profile_name]['late_editorial_extensions'].reverse()
        elif kind == 'wrong-canonical-manifest': bad['canonical_manifest'] = correction['corrected_contract']
        elif kind == 'wrong-qualified-contract': bad['qualified_expected_contract'] = correction['original_expected_contract']
        elif kind == 'wrong-dependency-digest': bad['dependencies'][str(dependencies[0])] = '0' * 64
        try:
            qualify(bad, badstack)
        except (AssertionError, KeyError, ValueError) as error:
            negatives.append(dict(case=kind, exception=type(error).__name__, rejected_before_publication=True))
        else:
            raise AssertionError('Unexpectedly accepted ' + kind)
    sources = {s: sha(stage_source(s).encode('utf-8')) for s in STAGES}
    save(root / 'checkpoint_qualification.json', dict(positive=positive, negative_cases=negatives,
        stage_source_derivations=sources, all_eight_original_stage_bodies_preserved=True,
        only_child_driver_paths_andcanonical_invocation_replaced=True, new_credit=0))
    assert registry_path.read_bytes() == before
    pending = registry_path.with_name('release_stack.Rafael516_resume_v2.pending.json')
    assert not pending.exists()
    save(pending, stack)
    os.replace(pending, registry_path)
    prep = deepcopy(prep)
    prep.update(profile=profile_name, registry_sha256=sha(registry_path.read_bytes()),
        original_preparation=str(prior_prep_path), original_preparation_sha256=sha(prior_prep_path.read_bytes()),
        canonical_checkpoint_resume=str(config_path), canonical_checkpoint_resume_sha256=sha(config_path.read_bytes()),
        previous_registry_profiles_andall114_accepted_layers_unchanged=True,
        explicit_versioned_resume_not_new_canonical_execution=True)
    prep['preserved_stage_configs']['ascii_glyph_right_bounds'] = str(bounds_path)
    save(root / 'registered_preparation.json', prep)
    qualification = deepcopy(qualification)
    qualification.update(profile=profile_name, registry_sha256=sha(registry_path.read_bytes()),
        preparation=str(root / 'registered_preparation.json'),
        preparation_sha256=sha((root / 'registered_preparation.json').read_bytes()),
        original_qualification=str(prior_qual_path), original_qualification_sha256=sha(prior_qual_path.read_bytes()),
        original_scene_transactions_all_inputs_andfinal_targets_exact=True,
        checkpoint_qualification=str(root / 'checkpoint_qualification.json'),
        checkpoint_qualification_sha256=sha((root / 'checkpoint_qualification.json').read_bytes()))
    save(root / 'qualification.json', qualification)
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    print('Registered explicit516 checkpoint continuation:ten negatives rejected; all114 accepted layers, original profiles, scene transactions andeight final-stage guards preserved. Build pending;no credit orpromotion.')


if __name__ == '__main__':
    main()
