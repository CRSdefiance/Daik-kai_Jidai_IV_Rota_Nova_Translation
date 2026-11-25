"""Preserve failed preparation; distinguish a measured composition count from native addresses."""
from scripts.source_locked_derivation_v5118 import derive
import runpy

if __name__ == '__main__':
    print(derive('scripts/prepare_Rafael_B49_checkpoint_v8100.py',
                 'scripts/prepare_Rafael_B49_checkpoint_v8100b_generated.py',
                 {'==156250': "==int('156250')"}))
    runpy.run_module('scripts.prepare_Rafael_B49_checkpoint_v8100b_generated', run_name='__main__')
