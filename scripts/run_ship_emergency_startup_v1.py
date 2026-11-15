"""Cold-boot the exact emergency research ROM against its registered parent."""

from types import FunctionType

from scripts import run_diplomatic_outcome_startup_v2 as replay
from scripts.run_mutiny_startup_v1 import STARTUP as PARENT
from scripts.stage_ship_emergency_balanced_v2 import PROOF, ROM, ROOT


STARTUP = ROOT / 'own_startup'


if __name__ == '__main__':
    run = FunctionType(replay.main.__code__, {
        **replay.main.__globals__, 'EVIDENCE': PROOF, 'ROM': ROM,
        'STARTUP': STARTUP, 'PRIOR': PARENT,
    })
    run()
