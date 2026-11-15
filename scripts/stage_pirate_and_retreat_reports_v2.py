"""Refine the long-bearing identification breaks and the temporary port order."""

from pathlib import Path
from types import FunctionType

from scripts import stage_pirate_and_retreat_reports_v1 as first


ROOT = Path('out/pirate_and_retreat_reports_staged_20261111_v2')
ROM, PROOF = ROOT / first.ROM.name, ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('pirate_and_retreat_reports_context_v2.json')
PHRASES = first.PHRASES | {2660: ("We'll dock at a nearby port for now.",)}
AMENDMENTS = {
    2617: ("Look, a pirate %s! It's %s!", 'Use a brisk call to the other crew and keep the identification together.'),
    2627: ("Look! A pirate %s! It's %s. They're attacking!", 'Restore the startled opening and keep the recognition before the alarm.'),
    2628: ("Hm! There's a pirate %s! It's %s! They're attacking!", 'Retain the older voice’s interjection and keep the recognition together.'),
    2630: ("There's a pirate %s! It's %s. We're under attack!", 'Preserve the sighting and follow it with the identification and immediate warning.'),
    2660: ("We'll dock at a nearby port for now.", 'Keep the rough voice’s plain plan, the port and the temporary qualifier together.'),
}


def draft():
    base = first.review.prior
    earlier = base.load(first.OUTPUT)
    assert base.digest(first.OUTPUT) == base.load(first.PROOF)['manuscript_sha256']
    for row in earlier['records']:
        number = row['message_ID']
        if number in AMENDMENTS:
            english, note = AMENDMENTS[number]
            assert row['decision'] == 'revision' and english.count('%s') == row['original_substitution_count']
            row.update(english=english, localization_note=note)
    earlier['prior_manuscript_sha256'] = base.digest(first.OUTPUT)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == earlier
    else:
        base.save(OUTPUT, earlier)


def main():
    draft()
    environment = vars(first) | dict(ROOT=ROOT, ROM=ROM, PROOF=PROOF, OUTPUT=OUTPUT, PHRASES=PHRASES)
    environment['stage'] = FunctionType(first.stage.__code__, environment, argdefs=first.stage.__defaults__)
    FunctionType(first.main.__code__, environment)()


if __name__ == '__main__':
    main()
