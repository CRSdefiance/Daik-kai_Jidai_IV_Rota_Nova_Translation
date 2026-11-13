"""Reuse the complete Lil B22 QA host with this batch's ordinary cold-boot inputs."""
from scripts.prepare_lil382_display_fixtures_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'work/Lil382_residual_A_clean_20261110/current_context_v1/ordinary_Lil_inputs.json':
        'work/Lil269_B243_B282_clean_20261110/current_context_v1/ordinary_Lil_inputs.json',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-complete-host-controls-native-objects-andinverse', 'exec'),
         {'__file__': __file__, '__name__': '__main__'})
