"""Preserve the stopped pre-write derivation and fix its longer inventory key."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive

derive('scripts/prepare_lil_B179_checkpoint_v4727.py','scripts/prepare_lil_B179_checkpoint_v4727b.py',{
    'change("remaining_B179_B180_physical_speeches=25","remaining_B180_physical_speeches=11")':
    'change("remaining_B179_B180_physical_speeches=11","remaining_B180_physical_speeches=11")'})
print('Prepared successor for the inventory key after its earlier count substitution; no current metadata writes.')
