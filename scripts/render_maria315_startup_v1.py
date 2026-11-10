"""Show all six complete candidate-owned startup checkpoints."""
from scripts.render_maria349_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous, {
    'work/maria349_B275_B285_release_v1': 'work/maria315_B286_B302_release_v1',
    'Own Maria349 B275-B285': 'Own Maria315 B286-B302',
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-six-complete-startup-captures', 'exec'), globals())
