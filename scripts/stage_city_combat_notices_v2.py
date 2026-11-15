"""Keep long port and ship names together in the original battle portraits."""

from collections import Counter
from inspect import getsource

from scripts import stage_city_combat_notices_v1 as first
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = first.ROOT.with_name('city_combat_notices_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('city_combat_notices_context_v2.json')
AMENDMENTS = {
    2586: ('%s is firing on us!', 'Keep the urgent warning and the direction of fire in a complete short call.'),
    2591: ('We sank their %s!', 'Keep the excited first-person report and enemy ownership. The full ship name fits.'),
    2594: ('Captured their %s!', 'Keep the quick capture report and explicit enemy ownership. Keep the ship name together.'),
    2595: ('Captured their %s.', 'Keep the even result and explicit enemy ownership without a lone verb on a second row.'),
    2596: ('We took their %s!', 'Keep the familiar naval sense of taking an opposing ship and the whole name.'),
    2601: ('We grabbed loot worth %s gold!', 'Keep the informal voice and group the amount and currency as the valuation.'),
    2603: ('We seized loot worth %s gold!', 'Keep the forceful result and the amount together with the currency.'),
    2607: ('Attacking %s now!', 'Keep the clipped launch report and the full city name.'),
    2608: ('Attack on %s has begun.', 'Keep the measured announcement of the attack starting and the full city name.'),
    2614: ('Time to attack %s.', 'Keep the turn to the next action and the complete city name in a single thought.'),
}


def main():
    base = first.review.prior
    if not OUTPUT.exists():
        draft = base.load(first.OUTPUT)
        for row in draft['records']:
            number = row['message_ID']
            if number in AMENDMENTS:
                english, note = AMENDMENTS[number]
                assert english.count('%s') == row['original_substitution_count'] == 1
                row.update(english=english, localization_note=note, decision='revision')
        draft['counts'] = dict(Counter(row['decision'] for row in draft['records']))
        draft['visual_amendments'] = sorted(AMENDMENTS)
        draft['previous_proof_sha256'] = base.digest(first.PROOF)
        base.save(OUTPUT, draft)
    source = checked_text(getsource(first.first.main), {
        "            assert b' '.join(display.split()) == expected, (number, display, expected)":
            "            original_expanded = expected\n"
            "            if group['argument_kind'] == 'gold':\n"
            "                expected = template % (str(sample['value']).encode('ascii'),)\n"
            "            assert b' '.join(display.split()) == expected, (number, display, expected)",
        "            assert all(any(phrase in line for line in lines)":
            "            if group['argument_kind'] in ('town', 'ship'):\n"
            "                name = arguments[0].decode('cp932')\n"
            "                assert any(name in line for line in lines), (number, name, lines)\n"
            "            assert all(any(phrase in line for line in lines)",
        'expanded_hex=expected.hex(),': 'expanded_hex=original_expanded.hex(), normalized_visible_hex=expected.hex(),',
        'assert len(records) == 47 and len(pages) == 89': 'assert len(records) == 35 and len(pages) == 80',
    })
    env = vars(first.first) | vars(first) | globals()
    exec(compile(source, __file__ + '::combat-portrait-name-continuity', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
