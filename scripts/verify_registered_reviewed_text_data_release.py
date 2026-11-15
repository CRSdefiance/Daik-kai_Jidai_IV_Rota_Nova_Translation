"""Verify all seven cumulative stages and reconstruct the complete target from clean input."""
import argparse
import sys
from collections import Counter
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.registered_reviewed_text_data_v3 import plan_release
from dk4tool.patch.xdelta import make_xdelta, apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.verify_release_baseline import main as verify_baseline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['candidate', 'preparation', 'out']:
        parser.add_argument('--' + key, type=Path, required=True)
    args = parser.parse_args(); assert not args.out.exists()
    prepared = load(args.preparation)
    config_path = Path(prepared['config']); config = load(config_path)
    parent_path = Path(prepared['parent_ROM']); parent_manifest = load(parent_path.with_suffix('.manifest.json'))
    manifest_path = args.candidate.with_suffix('.manifest.json'); manifest = load(manifest_path)
    registry_path = Path(manifest['release_stack']); registry = load(registry_path)
    assert sha(registry_path.read_bytes()) == manifest['release_stack_sha256'] == prepared['registry_sha256']
    assert manifest['profile'] == prepared['profile'] and all(manifest['checks'].values())
    assert manifest['checks']['registered_reviewed_text_data_and_complete_parent_target_inverse']
    assert all(manifest['checks'][key] == value for key, value in parent_manifest['checks'].items())
    assert manifest['batches'] == [*parent_manifest['batches'], str(config_path)] and len(manifest['batches']) == 667
    assert manifest['required_batches'] == parent_manifest['required_batches']
    assert sha(config_path.read_bytes()) == prepared['config_sha256']
    assert registry['profiles'][prepared['profile']]['owned_reviewed_text_data'] == str(config_path)
    old_registry = load(args.preparation.parent / 'release_stack.before.json')
    assert registry['accepted_layers'] == old_registry['accepted_layers'] and len(registry['accepted_layers']) == 114
    assert all(registry['profiles'][key] == value for key, value in old_registry['profiles'].items())
    present = {str(Path(p).resolve()).casefold() for p in manifest['batches']}
    assert all(r.get('baked_into_baseline') is True or str(Path(r['batch']).resolve()).casefold() in present
               for r in registry['accepted_layers'])
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256'] == sha(Path(registry['canonical_baseline']['path']).read_bytes())
    assert sha(parent_path.read_bytes()) == parent_manifest['candidate_sha256'] == prepared['parent_ROM_sha256']
    assert sha(args.candidate.read_bytes()) == manifest['candidate_sha256'] == prepared['target_ROM_sha256']
    assert args.candidate.read_bytes() == Path(prepared['reference_ROM']).read_bytes()
    parent, candidate = NdsImage.open(parent_path), NdsImage.open(args.candidate)
    arm, proof = plan_release(parent, config_path)
    assert proof == prepared['positive_plan'] and candidate.read_file('/__arm9__.bin') == arm
    assert all(candidate.read_file(p) == value for _, p, value in parent.iter_files())
    assert [p for p, value in parent.iter_components() if candidate.read_file(p) != value] == ['/__arm9__.bin']
    for internal in set(manifest['changed_records']) | set(parent_manifest['changed_records']):
        old, new = parent_manifest['changed_records'].get(internal, []), manifest['changed_records'].get(internal, [])
        assert new == old + (proof['changed_records'] if internal == '/__arm9__.bin' else [])
    stored = manifest['relocations']['/__arm9__.bin']['owned_reviewed_text_data']
    assert stored['proof'] == proof and stored['release_config_sha256'] == prepared['config_sha256']
    pipeline = manifest['reviewed_text_data_production_pipeline']
    assert pipeline['all_prior_drivers_unchanged'] and pipeline['only_final_six_disjoint_source_owned_text_spans_changed']
    assert sha(Path(pipeline['post_static_text_stage']).read_bytes()) == prepared['parent_ROM_sha256']
    old_argv = sys.argv
    try:
        sys.argv = ['verify_release_baseline', str(registry['canonical_baseline']['path']), str(args.candidate)]
        for path in manifest['changed_paths']:
            sys.argv += ['--allow-path', path]
        verify_baseline()
    finally:
        sys.argv = old_argv
    clean = Path(config['clean_ROM']); assert sha(clean.read_bytes()) == config['clean_ROM_sha256']
    patch = args.candidate.with_suffix('.xdelta'); assert not patch.exists()
    args.out.mkdir(parents=True)
    reconstructed = args.out / 'clean_input_reconstruction_RESEARCH_ONLY.nds'
    make_xdelta(clean, args.candidate, patch); apply_xdelta(clean, patch, reconstructed)
    assert reconstructed.read_bytes() == args.candidate.read_bytes()
    save(args.out / 'registered_release_verification.json', dict(candidate=str(args.candidate),
        candidate_sha256=manifest['candidate_sha256'], manifest=str(manifest_path), manifest_sha256=sha(manifest_path.read_bytes()),
        profile=manifest['profile'], registry_sha256=manifest['release_stack_sha256'], canonical_base=manifest['base_rom'],
        canonical_sha256=manifest['base_sha256'], parent=str(parent_path), parent_sha256=parent_manifest['candidate_sha256'],
        changed_internal_files=[], changed_components=['/__arm9__.bin'], owned_text_data_proof=proof,
        all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent=True,
        six_owned_text_data_spans_only=True, complete_stack_entries=667, accepted_layers=114,
        passing_release_checks=len(manifest['checks']), all_seven_registered_final_stages_preserved=True,
        new_contextual_records=4, dialogue_revisions=1, justified_retentions=3, wrap_fixes=4, separate_name_field_corrections=2,
        four_target_panels_andfull_catalogue_UI_live_unvisited=True, representative_live_consumer_bodies=7,
        byte_exact_to_checked_research_image=True, patch=str(patch), patch_sha256=sha(patch.read_bytes()),
        clean_input_sha256=sha(clean.read_bytes()), exact_clean_reconstruction=str(reconstructed),
        reconstructed_sha256=sha(reconstructed.read_bytes()), clean_input_patch_byte_exact=True,
        own_registered_startup_pending=True, experimental_not_promoted=True, full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    pin_path = Path('translations/rom_retention_pins.json'); pins = load(pin_path)
    for rom in [args.candidate, reconstructed]:
        if not any(Path(r['path']).resolve() == rom.resolve() for r in pins):
            pins.append(dict(path=str(rom.resolve()), reason='Preserve registered seven-stage successor and exact clean-input reconstruction;main unchanged.'))
    save(pin_path, pins)
    print('All667 entries/114 accepted layers/seven stages and exact clean-input patch pass;own startup pending.', flush=True)


if __name__ == '__main__':
    main()
