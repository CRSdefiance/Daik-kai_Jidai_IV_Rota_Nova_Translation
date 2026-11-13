"""Cold-boot the exact mutiny research ROM against the registered startup schedule."""

from types import FunctionType

from scripts import run_diplomatic_outcome_startup_v2 as replay
from scripts.run_sailing_alert_startup_v2 import STARTUP as PARENT
from scripts.stage_mutiny_review_v1 import PROOF, ROM, ROOT


STARTUP = ROOT / 'own_startup'


if __name__ == '__main__':
    run = FunctionType(replay.main.__code__, {
        **replay.main.__globals__, 'EVIDENCE': PROOF, 'ROM': ROM,
        'STARTUP': STARTUP, 'PRIOR': PARENT,
    })
    run()
