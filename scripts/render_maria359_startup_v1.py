"""Reuse exact startup comparison and readable candidate-owned checkpoint views."""
from scripts.render_maria363_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/maria363_B216_B252_release_v1':'work/maria359_B253_B274_release_v1',
    'Own Maria363 B216-B252':'Own Maria359 B253-B274',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-complete-startup-pixel-comparisons','exec'),globals())
