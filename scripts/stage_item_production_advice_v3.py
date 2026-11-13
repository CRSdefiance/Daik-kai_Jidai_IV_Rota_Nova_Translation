"""Keep the shark remark to three complete lines and balance four short starts."""

from types import FunctionType, SimpleNamespace

from scripts import stage_item_production_advice_v2 as previous


ROOT = previous.ROOT.with_name('item_production_advice_staged_20261111_v3')
ROM = ROOT / previous.ROM.name
PROOF = ROOT / previous.PROOF.name
OUTPUT = previous.OUTPUT.with_name('item_production_advice_context_v3.json')
PHRASES = previous.PHRASES | {
    3037: ('I hear they eat shark fins in China', 'and shark eggs around the Black Sea',
           'beyond the Mediterranean.'),
    3041: ('If only we could sell', 'this spice in Africa...'),
    3043: ('I think we could grow tea', 'in Africa, too.'),
    3044: ('This apparently needs', 'tropical conditions to grow.', 'Why not try taking it to Africa?'),
    3050: ('Perhaps we could find pearls', 'in East Asia too.'),
}


def main():
    base = previous.previous
    assert not ROOT.exists()
    if not OUTPUT.exists():
        manuscript = base.load(previous.OUTPUT)
        row = next(record for record in manuscript['records'] if record['message_ID'] == 3037)
        assert row['decision'] == 'retention' and row['english'].count('Black Sea, beyond') == 1
        row.update(english=row['english'].replace('Black Sea, beyond', 'Black Sea beyond'), decision='revision',
                   localization_note='Keep the reported food customs, the fins and eggs, and both regions. '
                   'Use ordinary ASCII I and run the geographic qualifier directly after Black Sea.')
        manuscript['counts']['revisions'] += 1
        manuscript['counts']['justified_retentions'] -= 1
        manuscript['visual_amendments_v3'] = dict(previous_native_proof=str(previous.PROOF),
            previous_native_proof_sha256=base.digest(previous.PROOF),
            findings=['Keep the two reported customs and the geographic qualifier on three complete rows.',
                      'Fill the opening rows of the pimento, tea, cacao and pearl remarks without changing their words.'])
        base.save(OUTPUT, manuscript)
    review = SimpleNamespace(**(vars(base.review) | {'OUTPUT': OUTPUT}))
    env = vars(base) | globals() | {'review': review}
    env['stage'] = FunctionType(base.stage.__code__, env)
    FunctionType(base.main.__code__, env)()


if __name__ == '__main__':
    main()
