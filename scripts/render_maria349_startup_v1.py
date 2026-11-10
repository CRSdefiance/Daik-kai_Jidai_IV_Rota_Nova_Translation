"""Show all six complete candidate-owned startup checkpoints."""
from scripts.render_maria359_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'work/maria359_B253_B274_release_v1':'work/maria349_B275_B285_release_v1',
    'Own Maria359 B253-B274':'Own Maria349 B275-B285'})
if __name__=='__main__':exec(compile(source,__file__+'::same-six-complete-startup-captures','exec'),globals())
