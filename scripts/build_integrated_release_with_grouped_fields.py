"""Keep all prior registered pipelines unchanged, then apply reviewed complete owner groups."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/build_integrated_release_with_owned_fields.py').read_text(encoding='utf-8'), {
    'from dk4tool.patch.registered_owned_name_fields_v2 import plan_release': 'from dk4tool.patch.registered_owned_name_fields_v4 import plan_release',
    "['owned_name_fields']": "['owned_name_fields_grouped']",
    "stage=args.work/'post_Emilio_RESEARCH_ONLY.nds'": "stage=args.work/'post_next_fields_RESEARCH_ONLY.nds'",
    'scripts/build_integrated_release_with_owned_names.py': 'scripts/build_integrated_release_with_next_owned_fields.py',
    "args.work/'owned_names'": "args.work/'next_fields'",
    "'immutable_registered_owned_names'": "'immutable_registered_next_fields'",
    "['registered_owned_name_fields_and_complete_parent_target_inverse']": "['registered_grouped_owned_name_fields_and_complete_parent_target_inverse']",
    "['owned_fields_production_pipeline']": "['grouped_owned_fields_production_pipeline']",
    'post_Emilio_stage': 'post_next_fields_stage',
    'post_Emilio_manifest': 'post_next_fields_manifest',
    'only_final_exclusive_fixed_slot_name_fields_changed=True': 'only_final_complete_reviewed_owner_group_fixed_slots_changed=True',
})
exec(compile(source, __file__ + '::unchanged-next-fields-then-complete-owner-groups', 'exec'), globals())
