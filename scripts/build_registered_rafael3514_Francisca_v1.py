"""Register the final name-field stage and build its verified cumulative output."""
import argparse
from copy import deepcopy
import os
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.registered_Francisca_name_field_v1 import plan_release
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.prepare_rafael3514_Francisca_field_v1 import CLEAN, CONFIG, OUT as FIELD_PROOF, digest
from scripts.verify_rafael_B51_B60_registered_release import KEYS


REGISTRY = Path('translations/release_stack.json')
PARENT = 'all-routes-rafael3514-dialogue-extended-v1-20261106'
PROFILE = 'all-routes-rafael3514-Francisca-extended-v1-20261106'
FIELD_KEY = 'owned_Francisca_name_field'
CHECK_KEY = 'registered_Francisca_name_field_and_complete_parent_target_inverse'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    assert not args.out.exists()
    before, stack = REGISTRY.read_bytes(), load(REGISTRY)
    assert len(stack['accepted_layers']) == 114 and PROFILE not in stack['profiles']
    parent = args.parent
    manifest_path = parent.with_suffix('.manifest.json')
    original = load(manifest_path)
    config, field = map(load, (CONFIG, FIELD_PROOF/'qualification.json'))
    assert original['profile'] == PARENT and digest(REGISTRY) == original['release_stack_sha256']
    assert original['candidate_sha256'] == digest(parent) == config['parent_ROM_sha256']
    assert len(original['batches']) == 691 and len(original['checks']) == 26 and all(original['checks'].values())
    assert field['config_sha256'] == digest(CONFIG) and field['wrong_predecessor_rejected']
    assert digest(field['target_reference']) == field['target_reference_sha256'] == config['target_ROM_sha256']
    prior_profile = stack['profiles'][PARENT]
    applied = {Path(path) for path in original['batches']}
    assert all(Path(prior_profile[key]) in applied for key in KEYS)
    assert all(layer.get('baked_into_baseline') or Path(layer['batch']) in applied for layer in stack['accepted_layers'])
    assert original['checks']['registered_runtime_bounds_and_complete_parent_target_inverse']
    assert original['checks']['registered_Fernan_name_field_and_complete_parent_target_inverse']
    assert Path(prior_profile['canonical_checkpoint_resume']) == Path(original['canonical_checkpoint_resume']['configuration'])

    image = NdsImage.open(parent)
    arm, proof = plan_release(image, CONFIG)
    assert proof == field['owned_name_field_proof']
    source_blocks = IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks
    expected = NdsImage.open(field['target_reference'])
    assert all(expected.read_file(path) == value for _, path, value in image.iter_files())
    assert expected.read_file('/__arm9__.bin') == arm
    assert IlnkContainer.parse(expected.read_file('/data/SC0.DK4')).blocks == source_blocks

    args.out.mkdir(parents=True)
    snapshot = args.out/'release_stack_before_Francisca.json'
    snapshot.write_bytes(before)
    profile = deepcopy(prior_profile)
    del profile['canonical_checkpoint_resume']
    checkpoint = dict(profile=PARENT, candidate=str(parent), candidate_sha256=digest(parent),
        manifest=str(manifest_path), manifest_sha256=digest(manifest_path), registry=str(snapshot),
        registry_sha256=digest(snapshot), verified_prefix_and_eight_stage_output_reused=True)
    profile.update({FIELD_KEY:str(CONFIG), 'verified_Francisca_stage_predecessor':checkpoint,
                    'note':'Experimental four-route dialogue successor with the exclusive Francisca width correction.'})
    stack['profiles'][PROFILE] = profile

    candidate = args.out/'all_routes_rafael3514_Francisca_extended_v1_20261106_candidate.nds'
    image.replace_file('/__arm9__.bin', arm)
    image.save(candidate)
    assert digest(candidate) == config['target_ROM_sha256']
    patch = candidate.with_suffix('.xdelta')
    rebuilt = args.out/'clean_input_reconstruction_RESEARCH_ONLY.nds'
    assert digest(CLEAN) == config['clean_ROM_sha256']
    make_xdelta(CLEAN, candidate, patch)
    apply_xdelta(CLEAN, patch, rebuilt)
    assert rebuilt.read_bytes() == candidate.read_bytes()

    assert REGISTRY.read_bytes() == before
    pending = REGISTRY.with_name('release_stack.Rafael3514_Francisca_v1.pending.json')
    assert not pending.exists()
    save(pending, stack)
    os.replace(pending, REGISTRY)
    actual_stack = load(REGISTRY)
    previous = load(snapshot)
    assert set(actual_stack['profiles']) == set(previous['profiles']) | {PROFILE}
    assert all(actual_stack['profiles'][name] == value for name, value in previous['profiles'].items())
    assert all(actual_stack[key] == value for key, value in previous.items() if key != 'profiles')

    result = deepcopy(original)
    result.update(profile=PROFILE, candidate_rom=str(candidate), candidate_sha256=digest(candidate),
                  release_stack_sha256=digest(REGISTRY))
    result['batches'].append(str(CONFIG))
    result['changed_records'].setdefault('/__arm9__.bin', []).extend(proof['changed_records'])
    result['relocations'].setdefault('/__arm9__.bin', {})[FIELD_KEY] = dict(
        release_config=str(CONFIG), release_config_sha256=digest(CONFIG), proof=proof)
    result['checks'][CHECK_KEY] = True
    result['Francisca_field_production_pipeline'] = dict(
        driver=__file__, driver_sha256=digest(__file__), predecessor=checkpoint,
        qualification=str(FIELD_PROOF/'qualification.json'), all_prior_stage_contracts_preserved=True)
    assert len(result['batches']) == 692 and len(result['checks']) == 27 and all(result['checks'].values())
    final_manifest = candidate.with_suffix('.manifest.json')
    save(final_manifest, result)
    save(args.out/'registered_name_stage_verification.json', dict(profile=PROFILE, candidate=str(candidate),
        candidate_sha256=digest(candidate), manifest=str(final_manifest), manifest_sha256=digest(final_manifest),
        predecessor=checkpoint, registry_sha256=digest(REGISTRY), patch=str(patch), patch_sha256=digest(patch),
        clean_input_sha256=digest(CLEAN), reconstructed_sha256=digest(rebuilt), clean_input_patch_byte_exact=True,
        accepted_layers=114, registered_manifest_entries=692, passing_release_checks=27,
        all_preceding_eight_stages_and_exclusive_field_preserved=True,
        registered_own_startup_pending=True, new_credit=0, experimental_not_promoted=True))
    print(f'Registered cumulative Rafael3514 with the Francisca field, {digest(candidate)}. Exact patch passes.')


if __name__ == '__main__':
    main()
