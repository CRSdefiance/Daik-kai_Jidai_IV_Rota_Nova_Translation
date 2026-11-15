"""Verify a scene-only successor retaining all six already registered final stages."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text


def record_ID(record):
    return record['id'] if isinstance(record, dict) else record


source = checked_text(Path('scripts/verify_registered_scene_release.py').read_text(encoding='utf-8'), {
    "sha(config_path.read_bytes())==preparation['config_sha256']":
        "sha(config_path.read_bytes())==profile['late_editorial_extensions'][-1]['config_sha256']",
    "manifest['batches'][:-2]==parent_manifest['batches'][:-1]":
        "manifest['batches'][:-7]==parent_manifest['batches'][:-6]",
    "manifest['batches'][-2:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds']))]":
        "manifest['batches'][-7:]==[str(Path(config['manuscript'])),*[str(Path(profile[k])) for k in ['ascii_glyph_right_bounds','owned_name_glyph','owned_name_fields','owned_name_fields_next','owned_name_fields_grouped','owned_static_text']]]",
    "    assert changed==[path] and all(candidate.read_file(p)==data for p,data in parent.iter_components())":
    """    assert changed==[path] and all(candidate.read_file(p)==data for p,data in parent.iter_components())
    for check in ['registered_owned_name_metadata_and_complete_parent_target_inverse','registered_owned_name_fields_and_complete_parent_target_inverse','registered_next_owned_name_fields_and_complete_parent_target_inverse','registered_grouped_owned_name_fields_and_complete_parent_target_inverse','registered_owned_static_text_and_complete_parent_target_inverse']:
        assert manifest['checks'][check]
    assert candidate.read_file('/__arm9__.bin')==parent.read_file('/__arm9__.bin')
    assert load(profile['owned_static_text'])['target_ROM_sha256']==manifest['candidate_sha256']""",
    "Counter(manifest['changed_records'].get(internal,[]))": "Counter(record_ID(r) for r in manifest['changed_records'].get(internal,[]))",
    "Counter(parent_manifest['changed_records'].get(internal,[]))": "Counter(record_ID(r) for r in parent_manifest['changed_records'].get(internal,[]))",
    '        all_other_files_components_graphics_names_andruntime_exact_to_parent=True,':
        '        all_other_files_components_graphics_names_andruntime_exact_to_parent=True,all_six_registered_final_stages_preserved=True,',
})
exec(compile(source, __file__ + '::complete-preserved-six-stage-stack-and-scene-only-clean-patch', 'exec'), globals())
