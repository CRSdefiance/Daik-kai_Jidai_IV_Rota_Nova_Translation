"""Reuse the complete clean-header role schema before native-page checking."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/project_maria363_native_roles_v1.py').read_text(encoding='utf-8'),{
    'Maria_B216_B252_clean_20261110':'Maria_B253_B274_clean_20261110',
    'formatting_v1/formatting_input.json':'formatting_v1/formatting_input_v2.json',
    "{'ordinary-speech':6,'4100-style-alternative':85}":"{'ordinary-speech':3,'4100-style-alternative':131}",
    'native_preflight_schema_failure_preserved=True':'previous_batch_schema_requirement_reused=True,no_new_preflight_failure_claim=True',
    'Bound6 ordinary and85 virtual-style controls':'Bound3 ordinary and131 virtual-style controls',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-complete-source-preamble-style-alias-andunchanged-role-guards','exec'),globals())
