"""Apply the complete native host-return guards to the single longer-tail sample."""
from scripts.render_lil382_transitions_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'display_run{choice}_v1': 'extended_run{choice}_v1',
    'display_pixels{choice}_v1': 'extended_pixels{choice}_v1',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-exact-host-return-guards-focused-longer-input-tail', 'exec'), globals())
