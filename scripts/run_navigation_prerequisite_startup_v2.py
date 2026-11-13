"""Cold-boot the final two-row version of the navigation warnings."""

from types import FunctionType

from scripts import run_navigation_prerequisite_startup_v1 as first
from scripts.stage_navigation_prerequisite_balanced_v2 import PROOF, ROM, ROOT


STARTUP = ROOT / 'own_startup'


if __name__ == '__main__':
    run = FunctionType(first.replay.main.__code__, {
        **first.replay.main.__globals__, 'EVIDENCE': PROOF, 'ROM': ROM,
        'STARTUP': STARTUP, 'PRIOR': first.PARENT,
    })
    run()
