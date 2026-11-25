"""Show all six complete candidate-owned startup checkpoints."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/render_maria303_startup_v1.py').read_text(encoding='utf-8'), {
    'work/maria303_release_v1': 'work/maria363_B216_B252_release_v1',
    'Own Maria303': 'Own Maria363 B216-B252',
})

if __name__ == '__main__':
    exec(compile(source,__file__+'::same-six-complete-candidate-owned-captures','exec'),globals())
