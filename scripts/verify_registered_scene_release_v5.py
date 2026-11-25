"""Verify the cumulative scene plus complete-owner-group fields and exact clean patch."""
from dk4tool.patch.owned_name_fields_v3 import plan_arm9_name_fields
from scripts import verify_registered_scene_release_v4 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "manifest['batches'][:-5]==parent_manifest['batches'][:-3]":
    "manifest['batches'][:-6]==parent_manifest['batches'][:-4]",
    "manifest['batches'][-5:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds'])),str(Path(profile['owned_name_glyph'])),str(Path(profile['owned_name_fields'])),str(Path(profile['owned_name_fields_next']))]":
    "manifest['batches'][-6:]==[str(Path(config['manuscript'])),str(Path(profile['ascii_glyph_right_bounds'])),str(Path(profile['owned_name_glyph'])),str(Path(profile['owned_name_fields'])),str(Path(profile['owned_name_fields_next'])),str(Path(profile['owned_name_fields_grouped']))]",
    "    name_config=load(profile['owned_name_fields_next'])": "    name_config=load(profile['owned_name_fields_grouped'])",
    "    assert manifest['checks']['registered_next_owned_name_fields_and_complete_parent_target_inverse']":
    "    assert manifest['checks']['registered_next_owned_name_fields_and_complete_parent_target_inverse']\n    assert manifest['checks']['registered_grouped_owned_name_fields_and_complete_parent_target_inverse']",
    "['/__arm9__.bin']['owned_name_fields_next']['proof']": "['/__arm9__.bin']['owned_name_fields_grouped']['proof']",
    "expected_name_IDs=[f'ACTOR{f[\"actor\"]}_NAME_COLUMN{f[\"column\"]}_LOCALIZED' for f in load(name_config['proposal'])['fields']]":
    "expected_name_IDs=[f'ACTOR{o[\"actor\"]}_NAME_COLUMN{o[\"column\"]}_LOCALIZED' for f in load(name_config['proposal'])['fields'] for o in f['owners']]",
})
exec(compile(source, __file__ + '::all-preserved-stages-complete-reviewed-owner-groups', 'exec'), globals())
