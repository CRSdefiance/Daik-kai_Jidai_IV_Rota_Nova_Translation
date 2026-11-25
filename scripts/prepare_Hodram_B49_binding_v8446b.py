"""Preserve stopped binder;bind exact negative_cases field of the existing builder proof."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    derive('scripts/bind_Hodram_B49_predecessor_v8446.py','scripts/bind_Hodram_B49_predecessor_v8446b.py',{
        "guard['negatives']":"guard['negative_cases']",
        'Hodram_B49_predecessor_binding_v8446':'Hodram_B49_predecessor_binding_v8446b',
    })
