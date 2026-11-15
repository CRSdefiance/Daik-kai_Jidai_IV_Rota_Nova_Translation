"""Bind Lil361's completed actual runs to the qualified native host transitions."""
from scripts.render_lil382_transitions_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {'display_run{choice}_v1': 'actual_run{choice}_v1'})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-transition-proof-with-current-run-paths', 'exec'), globals())
