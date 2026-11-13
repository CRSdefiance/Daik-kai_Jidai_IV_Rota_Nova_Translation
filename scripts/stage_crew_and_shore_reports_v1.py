"""Compile the crew and shore dialogue using its original portrait consumers."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path

from scripts import review_crew_and_shore_reports_v1 as review
from scripts import stage_fleet_reports_v1 as first
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/crew_and_shore_reports_staged_20261111_v1')
ROM, PROOF = ROOT / 'crew_and_shore_reports_RESEARCH_ONLY.nds', ROOT / 'stored_verification.json'
OUTPUT = review.OUTPUT
PHRASES = {
    2198: ("Shouldn't you be working?", "There's no time to fool around."),
    2200: ('My, you have time to spare.', 'Must be nice.'),
    2234: ("Let's go, Admiral!",),
    2237: ('Shall we go now, Admiral?',),
    2248: ('At least nobody got eaten!',),
    2252: ('Sailors are missing!', 'They deserted!'),
    2264: ('when the animals attacked!',),
    2265: ('when those animals attacked!',),
    2266: ('when those beasts attacked!',),
}


def stage(runtime, release, rows, groups, verified=None):
    def selector_checks(arm, execute):
        if verified is None:
            return execute(arm)
        assert sha256(arm).hexdigest() == verified['research_ARM9_sha256']
        return verified['ownership']['selector_checks']

    source = checked_text(getsource(first.prior.stage), {
        "group['runtime_item_name_inputs']": "group['argument_kind']",
        "allocation['touched_blocks'] == [26, 27]": "allocation['touched_blocks'] == [23, 24]",
        "checks = env['verify_scope'](arm)": "checks = check_exact_selector(arm, env['verify_scope'])",
    })
    env = vars(first.prior) | {'review': review, 'PHRASES': PHRASES, 'check_exact_selector': selector_checks}
    exec(compile(source, __file__ + '::crew-and-shore-storage', 'exec'), env)
    return env['stage'](runtime, release, rows, groups)


def samples(kind, groups, number):
    assert kind is None
    return [None]


def main():
    source = checked_text(getsource(first.main), {
        'assert len(records) == 47 and len(pages) == 89': 'assert len(records) == len(pages) == 56',
    })
    env = vars(first) | globals()
    exec(compile(source, __file__ + '::crew-and-shore-portraits', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
