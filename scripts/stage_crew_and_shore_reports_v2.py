"""Keep question, supply and follow-up phrases together in the native wraps."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import stage_crew_and_shore_reports_v1 as first


ROOT = Path('out/crew_and_shore_reports_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('crew_and_shore_reports_context_v2.json')
PHRASES = first.PHRASES | {
    2238: ("Come on, Admiral, let's go!",),
    2239: ('food and water with us.',),
    2240: ('food and water with us!',),
    2241: ('food and water!',),
    2242: ('their food and water',),
    2243: ('attacked our expedition!',),
    2248: ('our party!', 'At least nobody got eaten!'),
    2249: ('attacked our expedition!',),
    2251: ('Prepare to leave...', 'some sailors have deserted!'),
    2253: ('Shall we go, then?', 'some of the sailors deserted!'),
    2255: ('some sailors have deserted!',),
    2256: ("Let's go...", "We're short some sailors!"),
    2264: ('It seems the expedition caught it', 'when the animals attacked!'),
    2265: ('Looks like the party caught it', 'when those animals attacked!'),
    2266: ('all through the ship!', 'Looks like the expedition', 'when those beasts attacked!'),
    2267: ('the party the animals attacked!',),
    2269: ('caught in quicksand!',),
    2270: ('caught in quicksand!',),
    2274: ('caught in quicksand!',),
}


def stage(runtime, release, rows, groups, verified=None):
    env = vars(first) | {'PHRASES': PHRASES}
    return FunctionType(first.stage.__code__, env, argdefs=first.stage.__defaults__)(runtime, release, rows, groups, verified)


def main():
    base = first.review.prior
    draft = base.load(first.OUTPUT)
    assert base.digest(first.OUTPUT) == base.load(first.PROOF)['manuscript_sha256']
    row = next(row for row in draft['records'] if row['message_ID'] == 2270)
    row.update(english='Looks like the expedition got caught in quicksand!', decision='revision',
               localization_note='Name the expedition as in the surrounding reports and keep the uncertainty and quicksand phrase together.')
    draft['counts'] = dict(Counter(row['decision'] for row in draft['records']))
    draft['prior_manuscript_sha256'] = base.digest(first.OUTPUT)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == draft
    else:
        base.save(OUTPUT, draft)
    environment = vars(first) | dict(ROOT=ROOT, ROM=ROM, PROOF=PROOF, OUTPUT=OUTPUT, PHRASES=PHRASES, stage=stage)
    FunctionType(first.main.__code__, environment)()


if __name__ == '__main__':
    main()
