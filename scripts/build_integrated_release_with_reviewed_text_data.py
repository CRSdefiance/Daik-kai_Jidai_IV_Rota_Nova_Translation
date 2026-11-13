"""Run all six unchanged final stages, then six source-owned reviewed data spans."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/build_integrated_release_with_owned_fields.py').read_text(encoding='utf-8'), {
    'from dk4tool.patch.registered_owned_name_fields_v2 import plan_release': 'from dk4tool.patch.registered_reviewed_text_data_v1 import plan_release',
    "['owned_name_fields']": "['owned_reviewed_text_data']",
    "stage=args.work/'post_Emilio_RESEARCH_ONLY.nds'": "stage=args.work/'post_static_text_RESEARCH_ONLY.nds'",
    'scripts/build_integrated_release_with_owned_names.py': 'scripts/build_integrated_release_with_static_text.py',
    "args.work/'owned_names'": "args.work/'prior'",
    "'immutable_registered_owned_names'": "'immutable_registered_static_text'",
    "['registered_owned_name_fields_and_complete_parent_target_inverse']": "['registered_reviewed_text_data_and_complete_parent_target_inverse']",
    "['owned_fields_production_pipeline']": "['reviewed_text_data_production_pipeline']",
    "['owned_name_fields']=dict": "['owned_reviewed_text_data']=dict",
    'post_Emilio_stage': 'post_static_text_stage',
    'post_Emilio_manifest': 'post_static_text_manifest',
    'only_final_exclusive_fixed_slot_name_fields_changed=True': 'only_final_six_disjoint_source_owned_text_spans_changed=True',
})
exec(compile(source, __file__ + '::unchanged-six-stages-then-reviewed-data', 'exec'), globals())
