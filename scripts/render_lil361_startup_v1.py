"""Show all six exact cumulative-candidate startup checkpoints."""
from scripts.render_lil269_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'work/lil269_B243_B282_release_v1': 'work/lil361_B283_B298_release_v1',
    'Own Lil269 cumulative': 'Own Lil361 cumulative',
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-six-complete-startup-captures', 'exec'), globals())
