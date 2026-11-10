"""Bind the actual current opening without a new boot or weakened native guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B221_current_tools_v6966');assert not root.exists();root.mkdir(parents=True)
    p=derive('scripts/bind_current_V6910_native_v6920.py','scripts/bind_current_V6956_native_v6966.py',{'V6910':'V6956','v6920':'v6966','verification_v6916':'verification_v6962','lil_B218_release_v6911':'lil_B220_release_v6957','lil_B218_runs_v6913':'lil_B220_runs_v6959','current_V6865_native_v6874':'current_V6910_native_v6920','B220':'B221'})
    save(root/'source_locked_derivation.json',p)
