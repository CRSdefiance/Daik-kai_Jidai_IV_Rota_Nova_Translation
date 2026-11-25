"""Canonical reconstruction followed by one registered, source-locked runtime layer.

The original builder is immutable because historical native contracts bind its
complete bytes. Execute it unchanged, retain its full manifest, then apply the
registered code-only layer with complete parent/target identities and inverses.
Never hand off the intermediate canonical reconstruction.
"""
import argparse
import contextlib
import json
import runpy
import sys
from copy import deepcopy
from pathlib import Path

from dk4tool.patch.ascii_glyph_right_bounds import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile', required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists() and not args.out.with_suffix('.manifest.json').exists()
    registry = Path('translations/release_stack.json')
    registry_bytes = registry.read_bytes()
    stack = json.loads(registry_bytes)
    profile = stack['profiles'][args.profile]
    config_path = Path(profile['ascii_glyph_right_bounds'])
    config = json.loads(config_path.read_bytes())
    from dk4tool.patch.ascii_right_bounds_builder_guard import validate_current
    validate_current(config)
    args.work.mkdir(parents=True, exist_ok=True)
    stage = args.work / 'canonical_reconstruction_stage.nds'
    assert not stage.exists()
    print('Canonical builder reconstruction started; all original guards enabled.', flush=True)
    sys.argv = ['scripts/build_integrated_release.py', '--profile', args.profile, '--out', str(stage)]
    with (args.work / 'canonical_builder.log').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
        namespace = runpy.run_path('scripts/build_integrated_release.py', run_name='canonical_builder')
        namespace['main']()
    assert registry.read_bytes() == registry_bytes
    source = NdsImage.open(stage)
    manifest = json.loads(stage.with_suffix('.manifest.json').read_bytes())
    assert sha(stage.read_bytes()) == config['parent_ROM_sha256'] == manifest['candidate_sha256']
    assert manifest['profile'] == args.profile and manifest['release_stack_sha256'] == sha(registry_bytes)
    assert all(manifest['checks'].values())
    expected_manifest = json.loads(Path(config['parent_manifest']).read_bytes())
    assert manifest['batches'] == expected_manifest['batches']
    assert manifest['required_batches'] == expected_manifest['required_batches']
    assert manifest['base_sha256'] == expected_manifest['base_sha256']
    target = deepcopy(source)
    arm, proof = apply_release(source.read_file('/__arm9__.bin'), config_path)
    target.replace_file('/__arm9__.bin', arm)
    assert all(target.read_file(p) == value for _, p, value in source.iter_files())
    assert target.read_file('/__arm7__.bin') == source.read_file('/__arm7__.bin')
    for label in [b'Continue', b'New Game', b'Options', b'Grand Race', b'Extras', b'Gallery']:
        assert label in arm
    serialized = bytes(target.rom.save())
    assert sha(serialized) == config['target_ROM_sha256']
    # Serialize and re-open before publishing the final candidate and manifest.
    reviewed = args.work / 'complete_reviewed_target_RESEARCH_ONLY.nds'
    assert not reviewed.exists()
    reviewed.write_bytes(serialized)
    check = NdsImage.open(reviewed)
    assert check.read_file('/__arm9__.bin') == arm
    assert all(check.read_file(p) == value for _, p, value in target.iter_files())
    assert check.read_file('/__arm7__.bin') == target.read_file('/__arm7__.bin')
    result = deepcopy(manifest)
    result['candidate_rom'] = str(args.out)
    result['candidate_sha256'] = sha(serialized)
    result['batches'].append(str(config_path))
    result['changed_records'].setdefault('/__arm9__.bin', []).extend(proof['changed_records'])
    result['relocations'].setdefault('/__arm9__.bin', {})['ascii_glyph_right_bounds'] = {
        'release_config': str(config_path), 'release_config_sha256': sha(config_path.read_bytes()), 'proof': proof}
    result['checks']['registered_runtime_bounds_and_complete_parent_target_inverse'] = True
    result['production_pipeline'] = dict(
        driver=__file__, driver_sha256=sha(Path(__file__).read_bytes()),
        canonical_builder='scripts/build_integrated_release.py',
        canonical_builder_sha256=sha(Path('scripts/build_integrated_release.py').read_bytes()),
        canonical_stage=str(stage), canonical_stage_sha256=sha(stage.read_bytes()),
        canonical_manifest=str(stage.with_suffix('.manifest.json')),
        canonical_manifest_sha256=sha(stage.with_suffix('.manifest.json').read_bytes()),
        only_final_internal_component_changed='/__arm9__.bin',
        all_prior_batches_files_graphics_dialogue_fonts_and_accepted_layers_preserved=True)
    assert registry.read_bytes() == registry_bytes
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(serialized)
    args.out.with_suffix('.manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Registered integrated runtime-bound candidate:', args.out, sha(serialized), flush=True)


if __name__ == '__main__':
    main()
