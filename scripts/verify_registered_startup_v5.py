"""Own candidate startup with exact RGB reuse and the complete-owner-group inverse."""
from dk4tool.patch.owned_name_fields_v3 import plan_arm9_name_fields
from scripts import verify_registered_startup_v4 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "profile['owned_name_fields_next']": "profile['owned_name_fields_grouped']",
    'ARM9_except_exclusive_name_fields_COMMON_HELP_font_equal_registered_runtime_parent=True':
    'ARM9_except_source_qualified_grouped_name_fields_COMMON_HELP_font_equal_registered_runtime_parent=True',
})
exec(compile(source, __file__ + '::own-startup-preserved-runtime-complete-owner-groups', 'exec'), globals())
