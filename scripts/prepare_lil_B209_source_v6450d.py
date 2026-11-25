"""Compare a relative parent's header while binding its owned child speech independently."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_source_tools_v6450d')
if __name__=='__main__':
    assert not ROOT.exists();p=Path('scripts/map_lil_B209_source_v6450c.py');s=p.read_text('utf-8')
    old=next(x for x in s.splitlines() if "for c in nontext]==" in x)
    new="    structural=lambda c:(c['offset'],c['whole_command_hex'][:8] if c['word']==0x100 else c['whole_command_hex'])\n    assert [structural(c) for c in nontext]==[structural(c) for c in now if c['word'] not in [0x4000,0x4100]]"
    r=derive(str(p),'scripts/map_lil_B209_source_v6450d.py',{'source_v6450c\')':'source_v6450d\')',old:new})
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',dict(tool=r,prior_rejection='The0100 object at1036 contains a translated child4000 speech. Whole parent equality was overbroad;its complete4-byte header and skip operand remain exact,and the nested child has its own complete preamble/body/source/current references. All other opaque nontext objects remain whole-byte equal. Native relative semantics remain pending distinct tests.',no_ROM_registry_ledger_mutation_before_failure=True,full_goal_complete=False))
