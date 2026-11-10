"""Retain the caught old pool-size guard and bind the approved current size exactly."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_dispatch_tools_v6119b')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=derive('scripts/prove_lil_B204_dispatches_v6119.py','scripts/prove_lil_B204_dispatches_v6119b.py',{
        'import inspect\n':'import inspect\nfrom scripts.source_locked_derivation_v5118 import checked_text\n',
        "text=inspect.getsource(getattr(prior,name));adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)":"text=inspect.getsource(getattr(prior,name))\n        if name=='bind_current_catalog':text=checked_text(text,{'assert len(payload)==123040':\"assert len(payload)==123264 and sha(arm)=='03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd'\"})\n        adapters[name]=text;exec(compile(text,str(Path(__file__))+'::'+name,'exec'),namespace)",
        'lil_B204_dispatches_v6119':'lil_B204_dispatches_v6119b',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',dict(tool=tools,previous_caught_old123040_catalog_binding_guard_preserved=True,current_exact123264_and_whole_ARM9_hash_required=True,all_native_addresses_and_dispatch_code_unchanged=True,full_goal_complete=False));print('Successor binds exact current ARM9 and123264-byte pool;old failed producer preserved.')
