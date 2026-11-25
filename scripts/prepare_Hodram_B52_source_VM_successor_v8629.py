"""Preserve the stopped B52 VM producer and use the measured caller-span field."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_source_VM_successor_v8629');assert not root.exists()
    result=derive('scripts/prove_Hodram_B52_source_choice_VM_v8628.py','scripts/prove_Hodram_B52_source_choice_VM_v8628b.py',{
        'Hodram_B52_source_choice_VM_v8628':'Hodram_B52_source_choice_VM_v8628b',
        "forward['original_caller_instruction_span']":"forward['original_caller_span']"})
    root.mkdir(parents=True);save(root/'derivation.json',dict(derivation=result,prior_failure='KeyError original_caller_instruction_span; authoritative field original_caller_span',prior_source_preserved_andno_prior_output_orcredit=True,all_native_constants_andguards_preserved=True,new_credit=0,full_goal_complete=False))
