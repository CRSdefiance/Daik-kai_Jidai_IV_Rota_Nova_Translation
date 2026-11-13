"""Present all six complete candidate-owned startup captures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/render_maria303_startup_v1.py').read_text(encoding='utf-8'),{
    'work/maria303_release_v1':'work/maria390_B152_B175_release_v1','Own Maria303':'Own Maria390 B152-B175',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-six-complete-candidate-owned-captures','exec'),globals())
