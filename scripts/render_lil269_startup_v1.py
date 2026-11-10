"""Show all six exact cumulative-candidate startup checkpoints."""
from scripts.render_lil382_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'work/lil382_residual_A_release_v1': 'work/lil269_B243_B282_release_v1',
    'Own Lil382 cumulative': 'Own Lil269 cumulative',
})
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-six-complete-startup-captures', 'exec'), globals())
