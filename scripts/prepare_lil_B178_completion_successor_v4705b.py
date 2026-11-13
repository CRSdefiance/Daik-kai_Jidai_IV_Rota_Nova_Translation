"""Remove one unused whitespace alias before any completion tools were generated."""
from scripts.prepare_lil_B156_layout_v3705 import derive

derive('scripts/prepare_lil_B178_completion_v4705.py','scripts/prepare_lil_B178_completion_v4705b.py',{
    "    'revised=5,retained=5':'revised=2,retained=11',\n":'',
})
print('Prepared corrected completion-tool producer;all other substitution keys checked against actual source files.')
