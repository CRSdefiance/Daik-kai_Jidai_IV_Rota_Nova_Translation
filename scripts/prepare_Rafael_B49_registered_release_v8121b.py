"""Preserve failed release-tool preparation; the builder anchor is lowercase only."""
import runpy
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/prepare_Rafael_B49_registered_release_v8121.py','scripts/prepare_Rafael_B49_registered_release_v8121b_generated.py',{
        "'Rafael_B47_editorial':'Rafael_B48_editorial',":'',
    }))
    runpy.run_module('scripts.prepare_Rafael_B49_registered_release_v8121b_generated',run_name='__main__')
