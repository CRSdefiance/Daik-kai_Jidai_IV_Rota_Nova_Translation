"""Cold-boot the exact balanced sea-event ROM using the verified startup replay."""

from types import FunctionType

from scripts import run_diplomatic_outcome_startup_v2 as previous
from scripts.stage_sea_event_balanced_wrap_v2 import EVIDENCE, ROM, ROOT


STARTUP = ROOT / 'own_startup'


if __name__ == '__main__':
    replay = FunctionType(previous.main.__code__, {
        **previous.main.__globals__, 'EVIDENCE': EVIDENCE, 'ROM': ROM,
        'STARTUP': STARTUP, 'PRIOR': previous.STARTUP,
    })
    replay()
