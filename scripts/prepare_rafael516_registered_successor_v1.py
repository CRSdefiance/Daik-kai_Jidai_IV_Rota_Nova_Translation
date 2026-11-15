"""Reuse the verified678 release and append the qualified261 and255 transactions in order."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_plain_SC0_registered_successor_v1.py').read_text(encoding='utf-8'), {
    "    spec = load(args.spec)": """    spec = load(args.spec)
    assert all(Path(p).is_file() for p in [*spec['dependencies'],*spec['evidence'].values()])
    prefix_preparation = load(spec['qualified_prefix_preparation'])
    prefix_spec = prefix_preparation['new_extension_specs'][0]
    assert len(prefix_preparation['new_extension_specs']) == 1
    prefix_config = load(prefix_spec['config'])
    assert sha(Path(prefix_spec['config']).read_bytes()) == prefix_spec['config_sha256']
    assert sha(Path(*prefix_spec['module'].split('.')).with_suffix('.py').read_bytes()) == prefix_spec['module_sha256']
    prefix_qualification = load(spec['qualified_prefix_qualification'])
    assert prefix_qualification['preparation_sha256'] == sha(Path(spec['qualified_prefix_preparation']).read_bytes())
    assert len(prefix_qualification['changed_scope_andordering_rejections']) == 8
    assert prefix_qualification['direct_prepublication_andshared_targets_equal']
    prefix_parent = Path(spec['new_extension_parent'])
    assert sha(prefix_parent.read_bytes()) == prefix_spec['target_ROM_sha256']
    assert prefix_preparation['previous_profile'] == spec['previous_profile']""",
    "    assert rebuilt['parent_sha256'] == release['candidate_sha256']":
        """    assert rebuilt['parent_is_qualified_unregistered261_research_not_a_registered_release']
    assert rebuilt['registered_predecessor_is_verified678']
    assert rebuilt['parent_sha256'] == prefix_preparation['target_ROM_sha256']
    assert release['candidate_sha256'] == spec['verified_parent_ROM_sha256']
    assert prefix_spec['parent_ROM_sha256'] == sha(oldstates[0].read_bytes())""",
    "assert sha(original.read_file(doc['file_path'])) == rebuilt['source_archive_sha256']":
        "assert sha(original.read_file(doc['file_path'])) == spec['verified_parent_archive_sha256']",
    "    contract['batches'].append(str(final))":
        "    contract['batches'].extend([prefix_config['manuscript'],str(final)])",
    "new_extension_configs=[str(configpath)]":
        "new_extension_configs=[prefix_spec['config'],str(configpath)]",
    "format='dk4-reviewed-rafael-plain-scene-release-v1'":
        "format='dk4-reviewed-rafael-mixed-scene-release-v1'",
    "parent_ROM_sha256=sha(oldstates[0].read_bytes()),":
        "parent_ROM_sha256=sha(prefix_parent.read_bytes()),",
    "planner(NdsImage.open(oldstates[0]),NdsImage.open(registry['canonical_baseline']['path']),configpath)":
        "planner(NdsImage.open(prefix_parent),NdsImage.open(registry['canonical_baseline']['path']),configpath)",
    "profile['late_editorial_extensions'].append(new_spec)":
        "profile['late_editorial_extensions'].extend([prefix_spec,new_spec])",
    "configs=[str(configpath)],new_extension_specs=[new_spec]":
        "configs=[prefix_spec['config'],str(configpath)],new_extension_specs=[prefix_spec,new_spec]",
    "ordered_canonical_targets=[identity(targets[0])]":
        "ordered_canonical_targets=[identity(prefix_parent),identity(targets[0])]",
    "len(manifest['batches'])+1": "len(manifest['batches'])+2",
    "new_source_editorial_objects=config['record_count']":
        "new_source_editorial_objects=prefix_config['record_count']+config['record_count']",
    "records=config['record_count']":
        "records=prefix_config['record_count']+config['record_count']",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::two-qualified-ordered-transactions-verified678-prefix-all-eight-stages', 'exec'), globals())
