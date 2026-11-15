"""Run the unchanged grouped-fields pipeline, then registered fixed-slot static text."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/build_integrated_release_with_owned_fields.py').read_text(encoding='utf-8'), {
    'from dk4tool.patch.registered_owned_name_fields_v2 import plan_release': 'from dk4tool.patch.registered_owned_static_text_v1 import plan_release',
    "['owned_name_fields']": "['owned_static_text']",
    "stage=args.work/'post_Emilio_RESEARCH_ONLY.nds'": "stage=args.work/'post_grouped_fields_RESEARCH_ONLY.nds'",
    'scripts/build_integrated_release_with_owned_names.py': 'scripts/build_integrated_release_with_grouped_fields.py',
    "args.work/'owned_names'": "args.work/'grouped_fields'",
    "'immutable_registered_owned_names'": "'immutable_registered_grouped_fields'",
    "['registered_owned_name_fields_and_complete_parent_target_inverse']": "['registered_owned_static_text_and_complete_parent_target_inverse']",
    "['owned_fields_production_pipeline']": "['static_text_production_pipeline']",
    "['owned_name_fields']=dict": "['owned_static_text']=dict",
    'post_Emilio_stage': 'post_grouped_fields_stage',
    'post_Emilio_manifest': 'post_grouped_fields_manifest',
    'only_final_exclusive_fixed_slot_name_fields_changed=True': 'only_final_source_qualified_fixed_slot_static_text_changed=True',
})
exec(compile(source, __file__ + '::unchanged-grouped-fields-then-static-owned-data', 'exec'), globals())
