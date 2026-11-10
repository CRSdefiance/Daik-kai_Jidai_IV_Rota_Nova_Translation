"""Keep the compiled method's imported underlying machine distinct from the method itself."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/Gerhard_target_name_tools_v8210b')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/prove_Gerhard_target_name_v8210.py','scripts/prove_Gerhard_target_name_v8210b.py',{
        'Gerhard_target_name_v8210':'Gerhard_target_name_v8210b',
        "OwnedNameInputContext.machine=machine_env['machine']":
        "OwnedNameInputContext.machine=machine_env['machine']\nmachine_env['machine']=RouteCurrentContext.machine.__globals__['machine']",
        'actual_name_scene_fullreference_frozen_policy_atomic_andregistered_release_pending=True,':
        "actual_name_scene_fullreference_frozen_policy_atomic_andregistered_release_pending=True,\n        preserved_failure='scripts/prove_Gerhard_target_name_v8210.py compiled method shadowed its underlying imported machine;TypeError before research overlay/getters/no ROM changes',",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivation.json',result)
    print('Preserved all native guards;compiled method retains original underlying machine binding.')
