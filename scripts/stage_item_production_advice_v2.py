"""Refine item advice after visual review of the first native sheets."""

from types import FunctionType, SimpleNamespace

from scripts import stage_item_production_advice_v1 as previous


ROOT = previous.ROOT.with_name('item_production_advice_staged_20261111_v2')
ROM = ROOT / previous.ROM.name
PROOF = ROOT / previous.PROOF.name
OUTPUT = previous.review.OUTPUT.with_name('item_production_advice_context_v2.json')
PHRASES = previous.PHRASES | {
    3037: ('I hear they eat shark fins in China', 'around the Black Sea,', 'beyond the Mediterranean.'),
    3038: ("Southeast Asia's climate", 'for growing pepper.'),
    3039: ('Southeast Asia is ideal for cloves.', 'The Mediterranean, though?', 'We might have trouble there.'),
    3052: ('unusual fruit.', 'from the peel of this one.'),
    3055: ('No sailor can defy the weather.', 'This is sure to come in handy.'),
}
AMENDMENTS = {
    3038: ("Southeast Asia's climate is perfect for growing pepper.",
           'Keep Southeast Asia and the ideal climate in one natural spoken observation.'),
    3039: ('Southeast Asia is ideal for cloves. The Mediterranean, though? We might have trouble there.',
           'State the favorable climate plainly. The short Mediterranean question keeps the change of thought and the tentative conclusion.'),
}


def main():
    assert not ROOT.exists()
    if not OUTPUT.exists():
        manuscript = previous.load(previous.review.OUTPUT)
        for row in manuscript['records']:
            if row['message_ID'] in AMENDMENTS:
                text, note = AMENDMENTS[row['message_ID']]
                row.update(english=text, localization_note=note, decision='revision')
        manuscript['counts']['revisions'] += 1
        manuscript['counts']['justified_retentions'] -= 1
        manuscript['visual_amendments'] = dict(previous_native_proof=str(previous.PROOF),
            previous_native_proof_sha256=previous.digest(previous.PROOF),
            findings=['Keep Southeast Asia together.', 'Let the shark remark use the available first row.',
                      'Avoid leaving the demonstrative of a new sentence at the end of the previous row.',
                      'Give the fruit opening room before the distinction about its peel.'])
        previous.save(OUTPUT, manuscript)
    review = SimpleNamespace(**(vars(previous.review) | {'OUTPUT': OUTPUT}))
    env = vars(previous) | globals() | {'review': review}
    env['stage'] = FunctionType(previous.stage.__code__, env)
    FunctionType(previous.main.__code__, env)()


if __name__ == '__main__':
    main()
