"""Run the established release/dialogue regression selection after adding the item adapter."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/run_lil_B203_regressions_v6050.py','scripts/run_shachihoko_regressions_v6110.py',{'lil_B203_regressions_v6050':'shachihoko_regressions_v6110'}))
