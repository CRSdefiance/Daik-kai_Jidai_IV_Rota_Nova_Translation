"""Open the Palace Help articles and three owned continuations in the emulator."""

from argparse import ArgumentParser
from pathlib import Path
from subprocess import run
import sys
from types import FunctionType

from scripts import register_load_confirmation_20261120 as parent
from scripts import replay_damaged_save_digits_20261120 as boot
from scripts import stage_palace_help_20261120 as stage


base, ROOT = stage.base, stage.ROOT
ENTRY = Path('work/help_market_terms_20261119_v1/entry.json')
NAV = ROOT / 'navigation/navigation_plan.json'
CAPTURE = ROOT / 'gameplay'
LIVE = ROOT / 'gameplay_verification/ordinary_gameplay_verification.json'


def gameplay():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof['candidate_sha256']
    assert not NAV.parent.exists() and not CAPTURE.exists()
    qualification, itinerary = (ROOT / name for name in ('qualification.json', 'itinerary.json'))
    base.save(qualification, dict(research_ROM=str(stage.ROM), research_ROM_sha256=proof['candidate_sha256']))
    actions = [dict(open=11), dict(open=35), dict(remember='Palace menu'),
               dict(open=37), dict(remember='Military Investment start'), dict(open=204), dict(open=37),
               dict(return_to='Military Investment start'), dict(key='L'), dict(key='L'), dict(key='L'),
               dict(return_to='Palace menu')]
    for topic, child in stage.CHILDREN.items():
        if topic != 37:
            actions.extend([dict(open=topic), dict(open=child), dict(key='L'), dict(key='L')])
    actions += [dict(open=40), dict(key='L'), dict(open=41)]
    base.save(itinerary, dict(start_frame=21400, required_topics=sorted(stage.ARTICLES.keys() | stage.CHILDREN.values()),
                              actions=actions))
    run([sys.executable, '-B', '-m', 'scripts.plan_reviewed_help_navigation_v1', '--qualification', str(qualification),
         '--plan', str(stage.PLAN), '--itinerary', str(itinerary), '--entry', str(ENTRY), '--out', str(NAV.parent)], check=True)
    nav = base.load(NAV)
    frames = [nav['page_frames'][str(n)] for n in nav['observed_reviewed_topics']]
    frames.extend(frame for pair in nav['return_pairs'] for frame in pair['frames'])
    run([sys.executable, '-B', '-m', 'scripts.headless_desmume_v193', '--rom', str(stage.ROM), '--out', str(CAPTURE),
         '--frames', str(nav['terminal_frame']), '--inputs-json', str(NAV.parent / 'inputs.json'), '--press-start', '-1',
         '--touchscreen', '--capture-every', '999999', '--dump-capture-ram', '--capture-at', *map(str, sorted(set(frames)))],
        check=True)
    run([sys.executable, '-B', '-m', 'scripts.verify_reviewed_help_navigation_v1', '--capture', str(CAPTURE),
         '--navigation', str(NAV), '--plan', str(stage.PLAN), '--out', str(LIVE.parent)], check=True)


def startup():
    history = base.load(parent.STARTUP_CAPTURE)
    donor = history['battery_save_preloaded']
    assert base.digest(donor['source']) == donor['source_sha256']
    assert base.digest(stage.ROM) == base.load(stage.PROOF)['candidate_sha256']
    launch = FunctionType(boot.replay.__code__, vars(boot) | {'stage': stage})
    launch(stage.ROM, history, donor['source'], 'startup')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('gameplay', 'startup'))
    globals()[parser.parse_args().action]()
