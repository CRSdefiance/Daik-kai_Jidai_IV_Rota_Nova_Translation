"""Reuse a verified canonical prefix, append registered transactions, rerun final contracts."""
import contextlib
import json
import runpy
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.registered_canonical_checkpoint_resume_v1 import STAGES, stage_source as original_stage_source
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_rafael_B51_B60_registered_release import KEYS


def stage_source(name):
    source = original_stage_source(name)
    if name == 'runtime_bounds':
        return checked_text(source, {'scripts.registered_canonical_checkpoint_resume_v1 import resume_checkpoint':
            'scripts.registered_canonical_extension_resume_v2 import resume_checkpoint'})
    prior = STAGES[STAGES.index(name)-1]
    return checked_text(source, {'scripts/resume_integrated_release_with_'+prior+'_v1.py':
        'scripts/resume_extended_release_with_'+prior+'_v2.py'})


def qualify(config, stack):
    previous_bytes = Path(config['previous_registry']).read_bytes()
    assert sha(previous_bytes) == config['previous_registry_sha256']
    previous = json.loads(previous_bytes)
    assert config['profile'] not in previous['profiles']
    assert set(stack['profiles']) == set(previous['profiles']) | {config['profile']}
    assert all(stack[k] == v for k,v in previous.items() if k != 'profiles')
    assert all(stack['profiles'][k] == v for k,v in previous['profiles'].items())
    profile = deepcopy(stack['profiles'][config['profile']])
    assert profile.pop('canonical_checkpoint_resume') == config['configuration']
    assert profile == previous['profiles'][config['prepared_profile']]
    prep, qualification, release = [load(config[k]) for k in ['preparation','qualification','parent_release']]
    assert qualification['preparation_sha256'] == sha(Path(config['preparation']).read_bytes())
    assert len(qualification['changed_scope_andordering_rejections']) == 10
    assert qualification['direct_prepublication_andshared_targets_equal'] and qualification['unchanged_eight_final_stage_contracts_compared_exactly']
    assert prep['profile'] == config['prepared_profile'] and prep['previous_profile'] == config['source_profile'] == release['profile']
    assert prep['registry_sha256'] == config['previous_registry_sha256']
    source_registry = Path(config['source_registry']).read_bytes()
    assert sha(source_registry) == release['registry_sha256']
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    assert sha(Path(release['candidate']).read_bytes()) == release['candidate_sha256']
    assert sha(Path(release['manifest']).read_bytes()) == release['manifest_sha256']
    assert sha(Path(release['own_registered_startup']).read_bytes()) == release['own_registered_startup_sha256']
    old = deepcopy(previous['profiles'][config['source_profile']])
    old.pop('canonical_checkpoint_resume',None)
    compared = deepcopy(profile)
    assert compared['late_editorial_extensions'] == old['late_editorial_extensions'] + config['new_extension_specs']
    assert config['new_extension_specs'] == prep['new_extension_specs'] and len(config['new_extension_specs']) == 1
    for key in [*KEYS,'late_editorial_extensions','note']:
        old.pop(key); compared.pop(key)
    assert old == compared
    assert all(profile[k] == prep['preserved_stage_configs'][k] for k in KEYS)
    for path,digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    prefix = load(config['canonical_manifest'])
    assert prefix['candidate_sha256'] == sha(Path(config['canonical_ROM']).read_bytes()) == prep['canonical_parent_sha256']
    assert prefix['profile'] == config['source_profile'] and prefix['release_stack_sha256'] == release['registry_sha256']
    assert all(prefix['checks'].values()) and len(prefix['batches']) == 672
    assert Path(config['canonical_ROM']) == Path(prep['canonical_parent'])
    bounds = load(profile['ascii_glyph_right_bounds'])
    contract = load(bounds['parent_manifest'])
    manuscripts = [str(Path(load(s['config'])['manuscript'])) for s in config['new_extension_specs']]
    assert contract['batches'] == prefix['batches'] + manuscripts
    assert contract['required_batches'] == prefix['required_batches'] and contract['base_sha256'] == prefix['base_sha256']
    assert contract['expected_candidate_sha256'] == bounds['parent_ROM_sha256'] == config['new_extension_specs'][-1]['target_ROM_sha256']
    assert config['new_extension_specs'][0]['parent_ROM_sha256'] == prefix['candidate_sha256']
    return dict(all_previous_profiles_and114_accepted_layers_exact=True, full_verified672_entry_canonical_prefix_exact=True,
        one_registered_source_bound_extension_withten_rejections=True, unchanged_eight_stage_contracts=True,
        all_original_canonical_final_safety_contracts_execute_after_extension=True,
        all_eight_original_final_stage_bodies_andguards_execute=True, no_repeated_canonical_prefix_build=True)


def resume_checkpoint(profile, destination, registry_bytes):
    stack = json.loads(registry_bytes)
    config_path = Path(stack['profiles'][profile]['canonical_checkpoint_resume'])
    config = load(config_path)
    assert config['profile'] == profile and Path(config['configuration']) == config_path
    proof = qualify(config, stack)
    assert not destination.exists() and not destination.with_suffix('.manifest.json').exists()
    prefix = load(config['canonical_manifest'])
    builder = Path('scripts/build_integrated_release.py')
    raw = builder.read_text(encoding='utf-8')
    assert raw.count('    # Lexically valid "% o"') == 1
    tail = raw[raw.index('    # Lexically valid "% o"'):raw.index('\n\nif __name__ == "__main__":')]
    from dk4tool.patch.late_editorial_extensions_v1 import BUILDER_STAGE
    extension = checked_text(BUILDER_STAGE, {
        "profile_config.get('late_editorial_extensions', [])": "pending_registered_extensions",
    })
    namespace = runpy.run_path(str(builder),run_name='immutable_canonical_final_contract_functions')
    baseline = NdsImage.open(stack['canonical_baseline']['path'])
    clean = NdsImage.open('work/clean.nds')
    from dk4tool.dialogue.font_audit import GameAsciiFont
    font = GameAsciiFont.from_arm9(clean.read_file('/__arm9__.bin'))
    assert sha(font.glyphs) == prefix['final_plaque_contract']['baked_artwork_original_font_sha256']
    namespace.update(candidate=NdsImage.open(config['canonical_ROM']), baseline=baseline,
        pending_registered_extensions=config['new_extension_specs'], profile_config=stack['profiles'][profile],
        experimental_artwork_font=font, grouped={p:[] for p in prefix['changed_paths']},
        changed_records=deepcopy(prefix['changed_records']), relocation_checks=deepcopy(prefix['relocations']),
        release_batches=list(map(Path,prefix['batches'])), release_stack=stack, base_hash=prefix['base_sha256'],
        palace_label_contract=deepcopy(prefix['final_palace_menu_contract']),
        final_square_font_scratch_contract=deepcopy(prefix['final_square_font_scratch_contract']),
        args=SimpleNamespace(profile=profile,out=destination,manifest=None,base=Path(stack['canonical_baseline']['path'])))
    code='def complete_registered_checkpoint():\n'+extension+tail
    exec(compile(code,__file__+'::unchanged-canonical-extension-andall-final-safety-contracts','exec'),namespace)
    with (destination.parent/'extended_canonical_contracts.log').open('w',encoding='utf-8') as output, contextlib.redirect_stdout(output):
        namespace['complete_registered_checkpoint']()
    manifest = load(destination.with_suffix('.manifest.json'))
    bounds = load(stack['profiles'][profile]['ascii_glyph_right_bounds'])
    contract = load(bounds['parent_manifest'])
    assert manifest['batches'] == contract['batches'] and len(manifest['batches']) == 673
    assert manifest['candidate_sha256'] == sha(destination.read_bytes()) == contract['expected_candidate_sha256']
    assert all(manifest['checks'].values()) and len(manifest['checks']) == len(prefix['checks']) == 18
    assert Path('translations/release_stack.json').read_bytes() == registry_bytes
    manifest['canonical_checkpoint_resume'] = dict(configuration=str(config_path),configuration_sha256=sha(config_path.read_bytes()),
        original_profile=config['source_profile'],original_ROM=config['canonical_ROM'],original_ROM_sha256=prefix['candidate_sha256'],
        original_manifest=config['canonical_manifest'],original_manifest_sha256=sha(Path(config['canonical_manifest']).read_bytes()),
        original_release_stack_sha256=prefix['release_stack_sha256'], prefix_resume_provenance=prefix.get('canonical_checkpoint_resume'),
        appended_registered_extensions=config['new_extension_specs'], original_builder=str(builder),original_builder_sha256=sha(builder.read_bytes()),
        executed_original_final_contract_source_sha256=sha(tail.encode('utf-8')),
        explicit_versioned_prefix_reuse_not_a_new_full_canonical_builder_run=True,qualification=proof,
        stage_source_derivations={s:sha(stage_source(s).encode('utf-8')) for s in STAGES})
    save(destination.with_suffix('.manifest.json'),manifest)
    print('Exact canonical prefix plus351 registered transaction andall original final safety contracts pass; eight original final stages follow.',flush=True)


def run_driver(name, filename):
    env={'__name__':'registered_canonical_extension_stage','__file__':filename}
    exec(compile(stage_source(name),filename+'::unchanged-eight-stage-body-qualified-extended-prefix','exec'),env)
    env['main']()
