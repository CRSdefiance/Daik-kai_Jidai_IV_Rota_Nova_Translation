"""Resume an exact completed canonical build; retain every original final-stage guard."""
import importlib
import json
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.source_locked_derivation_v5118 import checked_text

STAGES = [
    'runtime_bounds', 'owned_names', 'owned_fields', 'next_owned_fields',
    'grouped_fields', 'static_text', 'reviewed_text_data_v3', 'Fernan_field',
]


def stage_source(name):
    assert name in STAGES
    original = 'scripts/build_integrated_release_with_' + name + '.py'
    module = importlib.import_module(original[:-3].replace('/', '.'))
    source = getattr(module, 'source', Path(original).read_text(encoding='utf-8'))
    if name == 'runtime_bounds':
        old = """    print('Canonical builder reconstruction started; all original guards enabled.', flush=True)
    sys.argv = ['scripts/build_integrated_release.py', '--profile', args.profile, '--out', str(stage)]
    with (args.work / 'canonical_builder.log').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
        namespace = runpy.run_path('scripts/build_integrated_release.py', run_name='canonical_builder')
        namespace['main']()
"""
        new = """    from scripts.registered_canonical_checkpoint_resume_v1 import resume_checkpoint
    resume_checkpoint(args.profile, stage, registry_bytes)
"""
        source = checked_text(source, {old: new})
    else:
        prior = STAGES[STAGES.index(name) - 1]
        child = 'scripts/build_integrated_release_with_' + prior + '.py'
        # Every successor has the exact prior driver's path in argv and run_path.
        assert source.count(child) == 2
        source = checked_text(source, {child: 'scripts/resume_integrated_release_with_' + prior + '_v1.py'})
    return source


def qualify(config, stack):
    """Pure fail-closed qualification: no files written and no native guard omitted."""
    previous_bytes = Path(config['previous_registry']).read_bytes()
    assert sha(previous_bytes) == config['previous_registry_sha256']
    previous = json.loads(previous_bytes)
    assert config['profile'] not in previous['profiles']
    assert all(stack[k] == v for k, v in previous.items() if k != 'profiles')
    assert set(stack['profiles']) == set(previous['profiles']) | {config['profile']}
    assert all(stack['profiles'][k] == v for k, v in previous['profiles'].items())
    old = previous['profiles'][config['source_profile']]
    new = deepcopy(stack['profiles'][config['profile']])
    assert new.pop('canonical_checkpoint_resume') == config['configuration']
    assert new['ascii_glyph_right_bounds'] == config['new_bounds_configuration']
    new['ascii_glyph_right_bounds'] = old['ascii_glyph_right_bounds']
    assert new == old
    oldbounds, bounds = map(load, [old['ascii_glyph_right_bounds'], config['new_bounds_configuration']])
    assert bounds['parent_manifest'] == config['qualified_expected_contract']
    assert {k: v for k, v in bounds.items() if k != 'parent_manifest'} == {
        k: v for k, v in oldbounds.items() if k != 'parent_manifest'}
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    terminal = load(config['original_build_terminal'])
    assert terminal['terminal'] and not terminal['driver_completed_without_exception']
    assert terminal['all_original_driver_andregistry_bytes_unchanged']
    assert terminal['registry_sha256'] == config['previous_registry_sha256']
    for path, digest in terminal['driver_andcanonical_bytes'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    correction = load(config['separator_qualification'])
    assert correction['all672_entries_exact_after_one_host_Path_spelling_correction']
    assert correction['all_required_batches_base_canonical_checks_andROM_identity_exact']
    assert correction['corrected_contract'] == config['qualified_expected_contract']
    assert correction['canonical_stage'] == config['canonical_ROM']
    assert correction['canonical_manifest'] == config['canonical_manifest']
    stage, manifest, contract = Path(config['canonical_ROM']), load(config['canonical_manifest']), load(config['qualified_expected_contract'])
    assert sha(stage.read_bytes()) == config['canonical_ROM_sha256'] == manifest['candidate_sha256'] == bounds['parent_ROM_sha256']
    assert manifest['profile'] == config['source_profile'] and manifest['release_stack_sha256'] == config['previous_registry_sha256']
    assert manifest['batches'] == contract['batches'] and len(manifest['batches']) == 672
    assert manifest['required_batches'] == contract['required_batches'] and manifest['base_sha256'] == contract['base_sha256']
    assert all(manifest['checks'].values())
    for path in manifest['batches']:
        assert Path(path).is_file(), path
    return dict(original_manifest_checks_exact=True, exact_672_batch_required_base_andROM_contract=True,
        unchanged_all114_accepted_layers_andall_previous_profiles=True,
        only_new_profile_bounds_contract_path_andexplicit_resume_registration=True,
        all_original_drivers_dependencies_andstage_configuration_fields_exact=True,
        canonical_builder_not_rerun=True, original_manifest_not_relabelled=True,
        all_eight_final_stage_bodies_andguards_still_required=True)


def resume_checkpoint(profile, destination, registry_bytes):
    stack = json.loads(registry_bytes)
    path = Path(stack['profiles'][profile]['canonical_checkpoint_resume'])
    config = load(path)
    assert config['profile'] == profile and Path(config['configuration']) == path
    proof = qualify(config, stack)
    assert Path('translations/release_stack.json').read_bytes() == registry_bytes
    assert not destination.exists() and not destination.with_suffix('.manifest.json').exists()
    destination.write_bytes(Path(config['canonical_ROM']).read_bytes())
    manifest = deepcopy(load(config['canonical_manifest']))
    manifest.update(profile=profile, release_stack_sha256=sha(registry_bytes), candidate_rom=str(destination))
    manifest['canonical_checkpoint_resume'] = dict(configuration=str(path), configuration_sha256=sha(path.read_bytes()),
        original_profile=config['source_profile'], original_release_stack_sha256=config['previous_registry_sha256'],
        original_ROM=config['canonical_ROM'], original_ROM_sha256=config['canonical_ROM_sha256'],
        original_manifest=config['canonical_manifest'], original_manifest_sha256=sha(Path(config['canonical_manifest']).read_bytes()),
        original_terminal=config['original_build_terminal'], original_terminal_sha256=sha(Path(config['original_build_terminal']).read_bytes()),
        explicit_versioned_continuation_not_a_new_canonical_builder_run=True, qualification=proof,
        stage_source_derivations={name: sha(stage_source(name).encode('utf-8')) for name in STAGES})
    save(destination.with_suffix('.manifest.json'), manifest)
    print('Exact registered canonical checkpoint resumed; every original final-stage guard remains enabled.', flush=True)


def run_driver(name, filename):
    source = stage_source(name)
    env = {'__name__': 'registered_canonical_checkpoint_stage', '__file__': filename}
    exec(compile(source, filename + '::unchanged-final-stage-body-explicit-checkpoint-chain', 'exec'), env)
    env['main']()
