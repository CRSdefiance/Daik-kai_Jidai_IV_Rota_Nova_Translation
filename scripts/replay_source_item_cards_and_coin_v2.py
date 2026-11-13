"""Run the preserved item and coin fixtures against the fixed-allocation build."""

import argparse
from types import FunctionType, SimpleNamespace

from scripts import replay_source_item_cards_and_coin_v1 as prior
from scripts import run_diplomatic_outcome_startup_v2 as startup
from scripts import stage_faction_aftermath_portraits_v2 as predecessor
from scripts import stage_source_item_cards_and_coin_v2 as final


stage = SimpleNamespace(**(vars(final.initial) | vars(final)))
COIN_DIR = stage.ROOT / 'coin_fixture'
COIN_ROM = COIN_DIR / 'coin_RESEARCH_ONLY.nds'
SHARK_DIR = stage.ROOT / 'baby_shark'


def cold_boot():
    env = vars(startup) | dict(EVIDENCE=stage.PREP, ROM=stage.ROM, STARTUP=stage.ROOT / 'own_startup',
                               PRIOR=predecessor.ROOT / 'own_startup')
    FunctionType(startup.main.__code__, env)()


def offline():
    final.NdsImage = stage.NdsImage
    final.offline()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('shark', 'coin-fixture', 'startup', 'offline'))
    action = parser.parse_args().action
    if action == 'startup':
        cold_boot()
    elif action == 'offline':
        offline()
    else:
        original = prior.baby_shark if action == 'shark' else prior.coin_fixture
        FunctionType(original.__code__, vars(prior) | globals())()

