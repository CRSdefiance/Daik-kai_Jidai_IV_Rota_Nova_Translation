"""Bind the six directly viewed startup captures to their exact composite."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(Path('scripts/bind_lil269_startup_visual_v1.py').read_text(encoding='utf-8'), {
    'work/lil269_B243_B282_release_v1': 'work/lil361_B283_B298_release_v1',
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-exact-six-capture-visual-binding', 'exec'), globals())
