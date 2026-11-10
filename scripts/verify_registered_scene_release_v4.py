"""Verify the preserved prior name stages plus the next exclusive-field successor."""
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from scripts import verify_registered_scene_release_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "sha(config_path.read_bytes())==preparation['config_sha256']":
        "sha(config_path.read_bytes())==profile['late_editorial_extensions'][-1]['config_sha256']",
    "manifest['batches'][:-4]==parent_manifest['batches'][:-2]":
        "manifest['batches'][:-5]==parent_manifest['batches'][:-3]",
    "manifest['batches'][-4:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds'])),str(Path(profile['owned_name_glyph'])),str(Path(profile['owned_name_fields']))]":
        "manifest['batches'][-5:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds'])),str(Path(profile['owned_name_glyph'])),str(Path(profile['owned_name_fields'])),str(Path(profile['owned_name_fields_next']))]",
    "    name_config=load(profile['owned_name_fields'])":"    name_config=load(profile['owned_name_fields_next'])",
    "    assert manifest['checks']['registered_owned_name_fields_and_complete_parent_target_inverse']":
        "    assert manifest['checks']['registered_owned_name_fields_and_complete_parent_target_inverse']\n    assert manifest['checks']['registered_next_owned_name_fields_and_complete_parent_target_inverse']",
    "['/__arm9__.bin']['owned_name_fields']['proof']":"['/__arm9__.bin']['owned_name_fields_next']['proof']",
})
exec(compile(source,__file__+'::all-prior-stages-and-next-owned-field-verification','exec'),globals())
