"""Preserve every prior registered driver, then apply the next source-owned fields."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/build_integrated_release_with_owned_fields.py').read_text(encoding='utf-8'),{
    'from dk4tool.patch.registered_owned_name_fields_v2 import plan_release':'from dk4tool.patch.registered_owned_name_fields_v3 import plan_release',
    "['owned_name_fields']":"['owned_name_fields_next']",
    "stage=args.work/'post_Emilio_RESEARCH_ONLY.nds'":"stage=args.work/'post_prior_fields_RESEARCH_ONLY.nds'",
    'scripts/build_integrated_release_with_owned_names.py':'scripts/build_integrated_release_with_owned_fields.py',
    "args.work/'owned_names'":"args.work/'prior_fields'",
    "'immutable_registered_owned_names'":"'immutable_registered_prior_fields'",
    "['owned_name_fields']":"['owned_name_fields_next']",
    "['registered_owned_name_fields_and_complete_parent_target_inverse']":"['registered_next_owned_name_fields_and_complete_parent_target_inverse']",
    "['owned_fields_production_pipeline']":"['next_owned_fields_production_pipeline']",
    'post_Emilio_stage':'post_prior_fields_stage',
    'post_Emilio_manifest':'post_prior_fields_manifest',
})
exec(compile(source,__file__+'::unchanged-prior-fields-then-next-owned-fields','exec'),globals())
