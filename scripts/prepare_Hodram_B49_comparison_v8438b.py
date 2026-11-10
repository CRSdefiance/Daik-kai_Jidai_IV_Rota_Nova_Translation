"""Preserve stopped8438; derive seed expectations as data, not new native addresses."""
from scripts.source_locked_derivation_v5118 import derive

if __name__=='__main__':
    derive('scripts/prepare_Hodram_B49_comparison_v8438.py','scripts/prepare_Hodram_B49_comparison_v8438c.py',{
        'Hodram_B49_comparison_tools_v8438':'Hodram_B49_comparison_tools_v8438c',
        '[[1633251573,1633251573],[996112413,155404999],[3478759668,3478759668]]':"[[int(x) for x in pair.split(',')] for pair in ['1633251573,1633251573','996112413,155404999','3478759668,3478759668']]",
    })
    from scripts import prepare_Hodram_B49_comparison_v8438c
    import runpy
    runpy.run_module(prepare_Hodram_B49_comparison_v8438c.__name__,run_name='__main__')
