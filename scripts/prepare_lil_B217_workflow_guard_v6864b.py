"""Correct preflight-detected substring changes before either generated release producer runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
if __name__=='__main__':
    jobs=[('scripts/register_lil_B217_v6864.py','scripts/register_lil_B217_v6864b.py',{'scripts.verify_village_wrap_v609':'scripts.verify_village_wrap_v608',"len(registry['accepted_layers'])==44":"len(registry['accepted_layers'])==114"}),('scripts/verify_lil_B217_release_v6866.py','scripts/verify_lil_B217_release_v6866b.py',{'scripts.verify_village_wrap_v609':'scripts.verify_village_wrap_v608'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    for a,b,c in jobs:print(derive(a,b,c))
