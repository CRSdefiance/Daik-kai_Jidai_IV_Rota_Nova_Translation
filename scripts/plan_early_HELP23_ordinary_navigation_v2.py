"""Use the proven Help selection protocol: A for the default first link, select+confirm for others."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/plan_early_HELP23_ordinary_navigation.py').read_text(encoding='utf-8'),{
    "ordinary_navigation_plan_v1":"ordinary_navigation_plan_v2",
    "        inputs.append(dict(start=now+1,duration=8,buttons=[],touch=[x,y]));now+=160":
        "        if page['links'][0]['id']!=target:\n            inputs.append(dict(start=now+1,duration=8,buttons=[],touch=[x,y]));now+=160",
    'no_fixtures_orstate_injection=True,':
        "no_fixtures_orstate_injection=True,\n        default_selected_first_link_uses_A_only=True,\n        native_selection_protocol_source='scripts/plan_interface_help_live_v457.py',\n        previous_double_activation_failure_preserved='work/analysis/Shared_HELP_early23_formatting_20261104/ordinary_navigation_v1',",
})
exec(compile(source,__file__+'::original-schedule-with-validated-native-selection-protocol','exec'),globals())
