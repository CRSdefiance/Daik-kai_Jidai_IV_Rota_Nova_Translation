"""Refine the four longer or unevenly wrapped weapon and armor remarks."""

from types import FunctionType, SimpleNamespace

from scripts import stage_weapon_armor_advice_v1 as first


ROOT = first.ROOT.with_name('weapon_armor_advice_staged_20261111_v2')
ROM = ROOT / first.ROM.name
PROOF = ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('weapon_armor_advice_context_v2.json')
AMENDMENTS = {
    3059: ('They say Lohengrin was a swan in human form, with uncanny powers. And this saber looks awfully sharp.',
           'Keep the legend attributed and give the separate observation about the saber a complete final line.'),
    3065: ('An officer could carry it, Admiral. Or you could wield it yourself.',
           'Keep both recipients and let the direct address stay with the first suggestion.'),
    3078: ('One of your crew could use this, or you could wield it, Admiral.',
           'Keep the broader crew wording here and the choice to use the weapon personally.'),
    3105: ("It has a great conqueror's dignity and bearing... What a sight! It's moments like this that make being a naturalist worthwhile.",
           'Let the appraisal turn into personal delight. Keep both the conqueror’s dignity and bearing and the explicit reference to being a naturalist.'),
}
PHRASES = first.PHRASES | {
    3059: ('They say Lohengrin was a swan', 'in human form, with uncanny powers.', 'And this saber looks awfully sharp.'),
    3065: ('An officer could carry it, Admiral.', 'Or you could wield it yourself.'),
    3075: ("I'd give this to a deckhand", 'for protection.'),
    3078: ('One of your crew could use this,', 'or you could wield it, Admiral.'),
    3105: ("It has a great conqueror's dignity", 'and bearing... What a sight!',
           "It's moments like this that make", 'being a naturalist worthwhile.'),
}


def main():
    base, editorial = first.previous, first.editorial
    assert not ROOT.exists()
    if not OUTPUT.exists():
        manuscript = base.load(first.OUTPUT)
        for row in manuscript['records']:
            if row['message_ID'] in AMENDMENTS:
                assert row['decision'] == 'revision'
                text, note = AMENDMENTS[row['message_ID']]
                row.update(english=text, localization_note=note)
        manuscript['wrap_amendments'] = dict(previous_native_proof=str(first.PROOF),
            previous_native_proof_sha256=base.digest(first.PROOF),
            changed_prose=sorted(AMENDMENTS), changed_wrap_only=[3075])
        base.save(OUTPUT, manuscript)
    review = SimpleNamespace(**(vars(editorial.previous) | vars(editorial) | {
        'RELEASE': first.parent.RELEASE, 'FIRST': first.FIRST, 'OUTPUT': OUTPUT,
    }))
    env = vars(base) | vars(first) | globals() | {'review': review}
    env['stage'] = FunctionType(first.stage_build.__code__, env)
    env['check_selector'] = FunctionType(base.check_selector.__code__, env)
    FunctionType(base.main.__code__, env)()


if __name__ == '__main__':
    main()
