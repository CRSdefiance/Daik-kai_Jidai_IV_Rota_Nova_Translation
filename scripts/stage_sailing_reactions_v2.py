"""Refine voice and phrase breaks identified in the first native contact sheets."""

from types import FunctionType

from scripts import stage_sailing_reactions_v1 as first


ROOT = first.ROOT.with_name('sailing_reactions_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('sailing_reactions_context_v2.json')
AMENDMENTS = {
    2359: ('Could it be trying to befriend us? Maybe it is gentle after all.',
           'Keep the tentative question and the change of perspective, with each thought on its own row.'),
    2459: ("Ah! It seems the wind's back.", 'Keep the exclamation, the uncertainty and the returning wind in one thought.'),
    2463: ('Maybe people drove it to fight by treating it like a monster. I feel sorry for it.',
           'Preserve the tentative human cause and keep the speaker’s sympathy as a complete thought.'),
    2465: ('Maybe it only fights because people treat it like a monster. Poor thing may not have a choice...',
           'Keep the uncertainty, people’s treatment of the whale, and the speaker’s sympathy.'),
    2467: ("People treated it like a monster. It may have had to fight back. I can't help but pity it...",
           'Keep the tentative inference and give the reflective ending a complete row.'),
    2476: ('Admiral, no damage from the reef! The extra armor did its job.',
           'Preserve the reef, the result and the reason in two complete thoughts.'),
    2489: ("The ram broke up the drift ice. The ship's safe now!",
           'Keep the cause and the reassurance in complete, spoken clauses.'),
    2492: ('The map was right, Admiral!', 'Keep the realization in a complete, excited exclamation.'),
    2493: ('Admiral, the map told the truth!', 'Keep the delighted confirmation of what the map said, without an isolated final word.'),
}
PHRASES = first.PHRASES | {
    2359: ('Could it be trying to befriend us?', 'Maybe it is gentle after all.'),
    2459: (),
    2463: ('Maybe people drove it to fight', 'by treating it like a monster.', 'I feel sorry for it.'),
    2465: ('Maybe it only fights because', 'people treat it like a monster.', 'Poor thing may not have a choice...'),
    2467: ('People treated it like a monster.', 'It may have had to fight back.', "I can't help but pity it..."),
    2476: ('Admiral, no damage from the reef!', 'The extra armor did its job.'),
    2489: ('The ram broke up the drift ice.', "The ship's safe now!"),
}


def stage_environment():
    env = vars(first) | globals()
    env['stage'] = FunctionType(first.stage.__code__, env)
    return env


def main():
    base = first.base
    if not OUTPUT.exists():
        draft = base.load(first.OUTPUT)
        for row in draft['records']:
            if row['message_ID'] in AMENDMENTS:
                text, note = AMENDMENTS[row['message_ID']]
                row.update(english=text, localization_note=note, decision='revision')
        draft['counts'] = {decision: sum(row['decision'] == decision for row in draft['records'])
                           for decision in ('revision', 'retention')}
        draft['visual_amendments'] = sorted(AMENDMENTS)
        draft['previous_proof_sha256'] = base.digest(first.PROOF)
        base.save(OUTPUT, draft)
    FunctionType(first.main.__code__, stage_environment())()


if __name__ == '__main__':
    main()
