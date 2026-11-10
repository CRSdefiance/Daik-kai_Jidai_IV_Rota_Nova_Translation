"""Run all seven earlier drivers unchanged, then the registered exclusive Fernan field."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/build_integrated_release_with_owned_fields.py').read_text(encoding='utf-8'), {
    'from dk4tool.patch.registered_owned_name_fields_v2 import plan_release':
        'from dk4tool.patch.registered_Fernan_name_field_v1 import plan_release',
    "['owned_name_fields']": "['owned_Fernan_name_field']",
    "stage=args.work/'post_Emilio_RESEARCH_ONLY.nds'": "stage=args.work/'post_reviewed_text_RESEARCH_ONLY.nds'",
    'scripts/build_integrated_release_with_owned_names.py': 'scripts/build_integrated_release_with_reviewed_text_data_v3.py',
    "args.work/'owned_names'": "args.work/'prior'",
    "'immutable_registered_owned_names'": "'immutable_registered_seven_stages'",
    "['registered_owned_name_fields_and_complete_parent_target_inverse']":
        "['registered_Fernan_name_field_and_complete_parent_target_inverse']",
    "['owned_fields_production_pipeline']": "['Fernan_field_production_pipeline']",
    "['owned_name_fields']=dict": "['owned_Fernan_name_field']=dict",
    'post_Emilio_stage': 'post_reviewed_text_stage',
    'post_Emilio_manifest': 'post_reviewed_text_manifest',
    'only_final_exclusive_fixed_slot_name_fields_changed=True': 'only_final_exclusive_Fernan_name_field_changed=True',
})
exec(compile(source,__file__+'::unchanged-seven-drivers-then-exclusive-Fernan-field','exec'),globals())
