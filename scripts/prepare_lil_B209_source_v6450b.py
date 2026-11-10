"""Preserve the rejected overbroad unchanged-span assertion; bind exact registered pointers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_source_tools_v6450b')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/map_lil_B209_source_v6450.py','scripts/map_lil_B209_source_v6450b.py',{
        'source_v6450\')':'source_v6450b\')',
        'from scripts.verify_village_wrap_v608 import read,save':'from scripts.verify_village_wrap_v608 import read,save\nfrom scripts.lil_B209_source_span_binding_v6450b import source_span_matches_registered_pointer_literals',
        'assert arm[a:b]==original[a:b]':'assert source_span_matches_registered_pointer_literals(arm,original,a,b)',
        'evidence={str(p):sha(p.read_bytes()) for p in [PRIOR':'evidence={str(p):sha(p.read_bytes()) for p in [Path(\'scripts/lil_B209_source_span_binding_v6450b.py\'),PRIOR',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',dict(tool=r,prior_failure='Whole2425C-243A0 incorrectly assumed unchanged. Only the already registered three renderer pointer words differ;their exact clean/current values and current whole ARM9 equality to V6380 now bound. Other instructions and style getter ranges remain exact.',no_ROM_or_ledger_mutation_before_failure=True,strict_current_ARM9_COMMON_directory_payload_and_instruction_guards_unchanged=True,full_goal_complete=False))
