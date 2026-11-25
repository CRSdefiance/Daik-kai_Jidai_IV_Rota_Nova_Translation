"""Refine the phrase breaks flagged in the first native contact sheets."""

from types import FunctionType, SimpleNamespace

from scripts import stage_proof_and_relic_advice_v1 as first


ROOT = first.ROOT.with_name('proof_and_relic_advice_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('proof_and_relic_advice_context_v3.json')
AMENDMENTS = {
    3197: ('A map of the area around Turkey.',
           'Use the concise recognition appropriate to the item view and preserve the area around Turkey.'),
    3214: ("There may be a link to the map for the North Sea's Proof of Conquest.",
           'Keep the uncertain connection to the map and keep the regional Proof name together.'),
    3215: ("This seems tied to the map for the Mediterranean's Proof of Conquest.",
           'Preserve the adviser’s inference and distinguish the map from the Proof itself.'),
    3220: ("There may be a link to the map for the New World's Proof of Conquest.",
           'Match the equally tentative Red Dye clue and keep the regional Proof name together.'),
    3229: ("This holds a power beyond words. I'd give it to a trusted warrior.",
           'Keep the wonder of the first thought and the emphasis on trust in the recommendation.'),
    3230: ("You rarely see a piece this fine. I'd give it to a trusted warrior.",
           'Keep the appraisal of this exceptional piece and match the shield’s recommendation.'),
}
PHRASES = first.PHRASES | {
    3213: ('No doubt about it.', 'This is a key to finding', "the New World's Proof of Conquest."),
    3214: ('There may be a link to the map for', "the North Sea's Proof of Conquest."),
    3215: ('This seems tied to the map for the', "Mediterranean's Proof of Conquest."),
    3220: ('There may be a link to the map for', "the New World's Proof of Conquest."),
    3222: ("I'd give it to a deckhand", 'or the Boarding Leader.'),
    3229: ('This holds a power beyond words.', "I'd give it to a trusted warrior."),
    3230: ('You rarely see a piece this fine.', "I'd give it to a trusted warrior."),
}


def stage_environment():
    env = first.stage_environment() | globals()
    env['review'] = SimpleNamespace(**(vars(env['review']) | {'OUTPUT': OUTPUT}))
    env['stage'] = FunctionType(env['stage'].__code__, env)
    env['check_selector'] = FunctionType(env['check_selector'].__code__, env)
    return env


def main():
    base = first.base
    if not OUTPUT.exists():
        manuscript = base.load(first.OUTPUT)
        for row in manuscript['records']:
            if row['message_ID'] in AMENDMENTS:
                assert row['decision'] == 'revision'
                text, note = AMENDMENTS[row['message_ID']]
                row.update(english=text, localization_note=note)
        manuscript['visual_amendments'] = dict(previous_native_proof=str(first.PROOF),
            previous_native_proof_sha256=base.digest(first.PROOF), changed_prose=sorted(AMENDMENTS),
            changed_wrap_only=[3213, 3222])
        base.save(OUTPUT, manuscript)
    FunctionType(base.main.__code__, stage_environment())()


if __name__ == '__main__':
    main()
