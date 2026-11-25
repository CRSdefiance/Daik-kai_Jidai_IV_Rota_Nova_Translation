"""Refine phrase breaks and keep both remedy names intact on screen."""

from collections import Counter
from types import FunctionType, SimpleNamespace

from scripts import stage_crew_item_actions_v1 as first


ROOT = first.ROOT.with_name('crew_item_actions_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.review.OUTPUT.with_name('crew_item_actions_context_v2.json')
AMENDMENTS = {
    2502: ("Admiral, take that away and I can't do my job.",
           'Keep the blunt address and the consequence while avoiding an isolated opening address.'),
    2504: ("Admiral, if you take that, I won't be able to do my job!",
           'Keep the objection and fit the address with the conditional phrase.'),
    2508: ("Looks like we don't need it right now, though...",
           'Keep the tentative crew perspective and group the trailing time phrase.'),
    2509: ("We've given %s to the sailors.",
           'Keep the completed action and exact substitution. This order keeps the longer remedy name together.'),
    2511: ('We handed out %s to the sailors!',
           'Keep the livelier report and the complete remedy name.'),
    2518: ('I beg you, O God, let your anger pass!',
           'Keep the solemn plea and group the invocation with the appeal.'),
    2527: ("Hold on. Dismiss all the sailors and the ship won't go anywhere!",
           'Keep the interruption and both complete clauses without breaking the object phrase.'),
    2528: ("Fire 'em all and who's gonna sail? I can't do it alone!",
           'Keep the familiar voice, the dismissal question and the speaker’s inability to sail alone.'),
}
PHRASES = first.PHRASES | {
    2502: ('Admiral, take that away', "and I can't do my job."),
    2504: ('Admiral, if you take that,', "I won't be able to do my job!"),
    2508: ("Looks like we don't need it", 'right now, though...'),
    2518: ('I beg you, O God,', 'let your anger pass!'),
    2527: ('Dismiss all the sailors', "and the ship won't go anywhere!"),
    2528: ("Fire 'em all and who's gonna sail?", "I can't do it alone!"),
}


def stage_environment():
    env = vars(first) | {'ROOT': ROOT, 'ROM': ROM, 'PROOF': PROOF, 'PHRASES': PHRASES,
                         'review': SimpleNamespace(**(vars(first.review) | {'OUTPUT': OUTPUT}))}
    env['stage'] = FunctionType(first.stage.__code__, env)
    return env


def main():
    base = first.review.prior
    assert not OUTPUT.exists()
    draft = base.load(first.review.OUTPUT)
    for row in draft['records']:
        number = row['message_ID']
        if number in AMENDMENTS:
            english, note = AMENDMENTS[number]
            assert english.count('%s') == row['original_substitution_count']
            row.update(english=english, localization_note=note, decision='revision')
    draft['counts'] = dict(Counter(row['decision'] for row in draft['records']))
    draft['visual_amendments'] = sorted(AMENDMENTS)
    draft['previous_proof_sha256'] = base.digest(first.PROOF)
    base.save(OUTPUT, draft)
    env = stage_environment()
    FunctionType(first.main.__code__, env)()


if __name__ == '__main__':
    main()
