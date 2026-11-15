"""Cold-boot and replay the corrected Ancient Map wrap profile."""

import sys
from types import FunctionType

from scripts import replay_ancient_map_text_v1 as prior
from scripts import stage_ancient_map_text_v2 as stage


if __name__ == '__main__':
    environment = vars(prior) | dict(stage=stage, STARTUP=stage.ROOT / 'own_startup',
                                     DISPLAY=stage.ROOT / 'ancient_map', __file__=__file__)
    gameplay = FunctionType(prior.gameplay.__code__, environment)
    # The replay harness imports the original fixture by module name.
    prior.stage = stage
    assert sys.argv[1:] in (['startup'], ['gameplay'])
    action = FunctionType(prior.cold_boot.__code__, environment) if sys.argv[1] == 'startup' else gameplay
    action()
