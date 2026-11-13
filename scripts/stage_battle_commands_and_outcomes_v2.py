"""Refine the long town question, defeat phrase and spoken creature names."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import stage_battle_commands_and_outcomes_v1 as first


ROOT = Path('out/battle_commands_and_outcomes_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('battle_commands_and_outcomes_context_v2.json')
AMENDMENTS = {
    2125: ('May we attack %s?', 'Keep the polite request for consent and preserve the full town name in a single question.'),
    2186: ("%s's flagship is disabled. We've lost!", 'Use a measured report of the disabled flagship and the resulting loss.'),
    2187: ("We've defeated the %s!", 'Retain the victory announcement and supply the natural article for a creature or ghost ship.'),
    2191: ('We defeated the %s!', 'Keep the direct, enthusiastic victory call and give the target its natural article.'),
}


def main():
    base = first.review.prior
    earlier = base.load(first.OUTPUT)
    assert base.digest(first.OUTPUT) == base.load(first.PROOF)['manuscript_sha256']
    for row in earlier['records']:
        if row['message_ID'] in AMENDMENTS:
            english, note = AMENDMENTS[row['message_ID']]
            assert english.count('%s') == row['original_substitution_count']
            row.update(english=english, localization_note=note, decision='revision')
    earlier['counts'] = dict(Counter(row['decision'] for row in earlier['records']))
    earlier['prior_manuscript_sha256'] = base.digest(first.OUTPUT)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == earlier
    else:
        base.save(OUTPUT, earlier)
    environment = vars(first) | dict(ROOT=ROOT, ROM=ROM, PROOF=PROOF, OUTPUT=OUTPUT)
    FunctionType(first.main.__code__, environment)()


if __name__ == '__main__':
    main()
