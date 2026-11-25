"""Keep complete questions and reactions together in the native portrait width."""

from pathlib import Path
from types import FunctionType

from scripts import stage_sailing_hazards_and_dolphins_v1 as previous


ROOT = Path('out/sailing_hazards_and_dolphins_staged_20261111_v2')
ROM = ROOT / 'sailing_hazards_and_dolphins_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PHRASES = previous.PHRASES | {
    2372: ('So many dolphins!', "I'd love to put this", "in the ship's log.", 'Can I, Admiral?'),
    2378: ('What a peaceful sight.',),
    2381: ('That sure was peaceful.',),
    2382: ('That put me at ease.',),
    2383: ('That was so relaxing.',),
    2384: ('That was a welcome little break...',),
    2385: ("I feel like I'm losing my mind!",),
    2387: ("I feel like I'm going mad!",),
    2388: ("I feel like I'm going mad!",),
    2393: ('going to swallow our ship!',),
    2406: ("The ship's caught in the tornado!",),
    2420: ("We can't turn in time!",),
}


def stage_environment():
    environment = vars(previous) | dict(ROOT=ROOT, ROM=ROM, PROOF=PROOF, PHRASES=PHRASES, __file__=__file__)
    environment['stage'] = FunctionType(previous.stage.__code__, environment, argdefs=previous.stage.__defaults__)
    return environment


def main():
    environment = stage_environment()
    FunctionType(previous.main.__code__, environment)()


if __name__ == '__main__':
    main()
