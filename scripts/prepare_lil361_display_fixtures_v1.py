"""Reuse the complete qualified Lil B22 host and this exact parent's ordinary input schedule."""
from scripts.prepare_lil269_display_fixtures_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/Lil269_B243_B282_clean_20261110/current_context_v1/ordinary_Lil_inputs.json':
        'work/Lil361_B283_B298_clean_20261110/current_context_v1/ordinary_Lil_inputs.json',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-complete-host-andordinary-input-guards', 'exec'),
         {'__file__': __file__, '__name__': '__main__'})
