"""Show all six complete candidate-owned startup checkpoints."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/render_maria303_startup_v1.py').read_text(encoding='utf-8'),{
    'work/maria303_release_v1':'work/maria305_B176_B195_release_v1','Own Maria303':'Own Maria305 B176-B195',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-six-complete-candidate-owned-captures','exec'),globals())
