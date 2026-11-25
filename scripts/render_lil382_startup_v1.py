"""Display all six exact cumulative-candidate startup checkpoints."""
from scripts.render_maria315_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous, {
    'work/maria315_B286_B302_release_v1':'work/lil382_residual_A_release_v1',
    'Own Maria315 B286-B302':'Own Lil382 cumulative',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-six-complete-startup-captures','exec'),globals())
