"""Refine phrase continuity on the figurehead and regional gift pages."""

from types import FunctionType, SimpleNamespace

from scripts import stage_figurehead_navigation_gift_advice_v1 as first


ROOT = first.ROOT.with_name('figurehead_navigation_gift_advice_staged_20261111_v2')
ROM = ROOT / first.ROM.name
PROOF = ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('figurehead_navigation_gift_advice_context_v2.json')
AMENDMENTS = {
    3147: ('Fit it to any ship and the whole fleet should go faster.',
           'Keep the choice of any ship and the expected effect on the whole fleet. The recommendation reads naturally in two clauses.'),
    3149: ('It seems to clear dangerous clouds. You could fit it to any ship.',
           'Keep both the tentative claim and the choice of ship. Let each complete thought fit on its own row.'),
    3174: ('All the way from Persia to Japan... Perhaps it has deep ties to Asia.',
           'Keep the geographic route together and preserve the adviser’s tentative reflection about the piece.'),
}
PHRASES = first.PHRASES | {
    3147: ('Fit it to any ship and', 'the whole fleet should go faster.'),
    3149: ('It seems to clear dangerous clouds.', 'You could fit it to any ship.'),
    3150: ("I'd fit this to a ship", 'that matters to you.'),
    3151: ('Fit this to the ship', 'with the strongest guns.'),
    3153: ('It should work on any ship.', 'It seems to refresh the spirit', 'and ease fatigue...'),
    3155: ("I'd fit it to a ship", 'with plenty of sailors.', "It looks like it'll help", 'in boarding fights.'),
    3156: ("It should bring heaven's protection", 'to any ship. It might keep the crew', 'from getting sick.'),
    3168: ('Everyone around the Mediterranean', 'knows this statue.',
           "I'll wager plenty would want it.", 'Magnificent...'),
    3174: ('All the way from Persia to Japan...', 'Perhaps it has deep ties to Asia.'),
    3177: ('Fine silk, I see.', 'I imagine people in the East', 'would appreciate it, too.'),
    3179: ('It seems hard to get', "Europe's latest tools", 'in the New World.'),
}


def main():
    base = first.base
    assert not ROOT.exists()
    if not OUTPUT.exists():
        manuscript = base.load(first.OUTPUT)
        for row in manuscript['records']:
            if row['message_ID'] in AMENDMENTS:
                assert row['decision'] == 'revision'
                text, note = AMENDMENTS[row['message_ID']]
                row.update(english=text, localization_note=note)
        manuscript['visual_amendments'] = dict(previous_native_proof=str(first.PROOF),
            previous_native_proof_sha256=base.digest(first.PROOF), changed_prose=sorted(AMENDMENTS),
            changed_wrap_only=[3150, 3151, 3153, 3155, 3156, 3168, 3177, 3179])
        base.save(OUTPUT, manuscript)
    editorial = SimpleNamespace(**(vars(first.editorial) | {'OUTPUT': OUTPUT}))
    env = vars(first) | globals() | {'editorial': editorial}
    FunctionType(first.main.__code__, env)()


if __name__ == '__main__':
    main()
