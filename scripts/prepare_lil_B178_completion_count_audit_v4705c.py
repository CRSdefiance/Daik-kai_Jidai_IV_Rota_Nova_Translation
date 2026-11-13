"""Correct inherited ten-completion reporting labels without changing numeric checks."""
from scripts.prepare_lil_B156_layout_v3705 import derive

derive('scripts/verify_lil_B178_completion_plan_v4705.py','scripts/verify_lil_B178_completion_plan_v4705b.py',{
    "ROOT/'independent_preapplication_audit.json'":"ROOT/'independent_preapplication_audit_v2.json'",
    'source_prose_credit_unchanged_completion_adds_ten_once':'source_prose_credit_unchanged_completion_adds_thirteen_once',
    'ten completions only':'thirteen completions only',
})
print('Prepared accurate thirteen-completion audit labels;original audit and numeric checks preserved.')
