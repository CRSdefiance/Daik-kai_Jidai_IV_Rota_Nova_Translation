"""Polish the crew-equipment remarks flagged during native visual review."""

from types import FunctionType, SimpleNamespace

from scripts import stage_crew_equipment_advice_v1 as first


ROOT = first.ROOT.with_name('crew_equipment_advice_staged_20261111_v2')
ROM = ROOT / first.ROM.name
PROOF = ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('crew_equipment_advice_context_v2.json')
AMENDMENTS = {
    3116: ("Learn the tricks experience brings, and you'll steer a lot better.",
           'Keep practical experience as the source of the techniques and the strong benefit to steering. Let the two clauses run naturally.'),
    3120: ('A First Mate must win over disgruntled sailors and negotiate with other factions.',
           'Keep both duties and use the game’s First Mate title. Win over is natural spoken English for persuading the dissatisfied crew.'),
    3140: ('Anyone can understand this Bible.',
           'Retain the claim that it is accessible to anyone and give the short appraisal one complete row.'),
    3143: ('The power to see the future... Did the great strategists of old have that gift, I wonder?',
           'Keep the pause and the adviser’s speculative question about the strategists of old.'),
}
PHRASES = first.PHRASES | {
    3116: ('Learn the tricks experience brings,', "and you'll steer a lot better."),
    3120: ('A First Mate must win over', 'disgruntled sailors and negotiate', 'with other factions.'),
    3121: ('A voyage is easier on the nerves', 'with a First Mate who knows', "the world's geography."),
    3124: ('A Boarding Leader you can count on', 'knows how to fight', 'and is skilled with a sword.'),
    3125: ('A Boarding Leader you can count on', 'knows how to fight', 'and is skilled with a sword.'),
    3138: ('Those are stylish boots.', 'They ought to make tending animals', 'more comfortable.'),
    3143: ('The power to see the future...', 'Did the great strategists of old', 'have that gift, I wonder?'),
    3146: ('With this, I doubt anyone could', 'overcharge you', 'for a pittance.'),
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
            changed_wrap_only=[3121, 3124, 3125, 3138, 3146])
        base.save(OUTPUT, manuscript)
    editorial = SimpleNamespace(**(vars(first.editorial) | {'OUTPUT': OUTPUT}))
    env = vars(first) | globals() | {'editorial': editorial}
    FunctionType(first.main.__code__, env)()


if __name__ == '__main__':
    main()
