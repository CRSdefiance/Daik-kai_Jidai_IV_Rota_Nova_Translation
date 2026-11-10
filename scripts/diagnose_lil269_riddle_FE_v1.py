"""Reuse the qualified read-only FE return observer for Lil's concrete riddle failure."""
from pathlib import Path
from scripts import diagnose_maria363_riddle_FE_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path(previous.__file__).read_text(encoding='utf-8'), {
    "work/Maria_B216_B252_clean_20261110": "work/Lil269_B243_B282_clean_20261110",
    'B221_R8_FE_failure_diagnostic_v1.json': 'B251_R9_FE_failure_diagnostic_v1.json',
    'native_inputs_v1/plans.json': 'plan_v4/automatic_plans.json',
    'DK4_MES_B221_R0008': 'DK4_MES_B251_R0009',
    'work/maria321_B196_B215_release_v1/registered_release_verification.json':
        'work/lil382_residual_A_release_v1/registered_release_verification.json',
    'work/maria321_B196_B215_release_v1/own_registered_startup_verification.json':
        'work/Lil269_B243_B282_clean_20261110/current_context_v1/own_Lil_startup_verification.json',
    'captain=3': 'captain=2',
})

if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-qualified-return-observer', 'exec'),
         {'__file__': __file__, '__name__': '__main__'})
