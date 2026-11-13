"""Preserve failed derivation; seal path belongs to its separately prepared paths module."""
import runpy
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/prepare_Rafael_B49_seal_v8114.py','scripts/prepare_Rafael_B49_seal_v8114b_generated.py',{
        "        'all91_five_gates_exact_references_approved.json':'all61_five_gates_exact_references_approved.json',\n":'',
    }))
    runpy.run_module('scripts.prepare_Rafael_B49_seal_v8114b_generated',run_name='__main__')
