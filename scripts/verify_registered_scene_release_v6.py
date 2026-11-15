"""Verify scene integration plus the final owned static-data stage and clean patch."""
from pathlib import Path
from dk4tool.patch.hodram_static_labels_v1 import plan_static_labels
from scripts.source_locked_derivation_v5118 import checked_text


def record_ID(record):
    return record['id'] if isinstance(record, dict) else record


source = checked_text(Path('scripts/verify_registered_scene_release.py').read_text(encoding='utf-8'), {
    "preparation['target_ROM_sha256']==rebuilt['research_ROM_sha256']": "preparation['target_ROM_sha256']==sha(Path(preparation['final_ROM']).read_bytes())",
    "sha(config_path.read_bytes())==preparation['config_sha256']": "sha(config_path.read_bytes())==profile['late_editorial_extensions'][-1]['config_sha256']",
    "manifest['batches'][:-2]==parent_manifest['batches'][:-1]": "manifest['batches'][:-7]==parent_manifest['batches'][:-5]",
    "manifest['batches'][-2:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds']))]":
        "manifest['batches'][-7:]==[str(Path(config['manuscript'])),*[str(Path(profile[k])) for k in ['ascii_glyph_right_bounds','owned_name_glyph','owned_name_fields','owned_name_fields_next','owned_name_fields_grouped','owned_static_text']]]",
    "len(manifest['batches'])==len(parent_manifest['batches'])+1": "len(manifest['batches'])==len(parent_manifest['batches'])+2",
    "    assert changed==[path] and all(candidate.read_file(p)==data for p,data in parent.iter_components())":
    """    assert changed==[path]
    static_config=load(profile['owned_static_text'])
    expected_arm,static_proof=plan_static_labels(parent.read_file('/__arm9__.bin'),load(static_config['proposal']),NdsImage.open(config['clean_ROM']).read_file('/__arm9__.bin'))
    assert candidate.read_file('/__arm9__.bin')==expected_arm
    changed_components=[p for p,data in parent.iter_components() if candidate.read_file(p)!=data]
    assert changed_components==['/__arm9__.bin']
    for check in ['registered_owned_name_metadata_and_complete_parent_target_inverse','registered_owned_name_fields_and_complete_parent_target_inverse','registered_next_owned_name_fields_and_complete_parent_target_inverse','registered_grouped_owned_name_fields_and_complete_parent_target_inverse','registered_owned_static_text_and_complete_parent_target_inverse']:
        assert manifest['checks'][check]
    assert static_config['target_ROM_sha256']==manifest['candidate_sha256']
    recorded=manifest['relocations']['/__arm9__.bin']['owned_static_text']['proof']
    assert recorded['complete_owned_data_plan']==static_proof
    expected_static_IDs=[r['id'] for r in static_proof['fields']]
    assert [r['id'] for r in recorded['changed_records']]==expected_static_IDs""",
    "Counter(manifest['changed_records'].get(internal,[]))": "Counter(record_ID(r) for r in manifest['changed_records'].get(internal,[]))",
    "Counter(parent_manifest['changed_records'].get(internal,[]))": "Counter(record_ID(r) for r in parent_manifest['changed_records'].get(internal,[]))",
    "        assert added==(Counter(row['id'] for row in approved['records']) if internal==path else Counter())":
        "        expected=Counter(row['id'] for row in approved['records']) if internal==path else Counter(expected_static_IDs) if internal=='/__arm9__.bin' else Counter()\n        assert added==expected",
    "args.candidate.read_bytes()==Path(rebuilt['research_ROM']).read_bytes()": "args.candidate.read_bytes()==Path(preparation['final_ROM']).read_bytes()",
    '        changed_internal_files=changed,changed_blocks={path:changed_blocks},': '        changed_internal_files=changed+changed_components,changed_blocks={path:changed_blocks},',
    '        all_other_files_components_graphics_names_andruntime_exact_to_parent=True,':
        '        all_unowned_files_components_graphics_names_fonts_andruntime_code_exact_to_parent=True,static_data_only_change_verified=True,static_data_proof=static_proof,',
})
exec(compile(source, __file__ + '::preserved-stack-and-static-data-verified-from-clean-input', 'exec'), globals())
