"""Keep the focal phrases together in the faction aftermath portraits."""

import inspect
from types import FunctionType

from scripts import stage_faction_aftermath_portraits_v1 as initial
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = initial.ROOT.with_name('faction_aftermath_portraits_staged_20261111_v2')
ROM = ROOT / initial.ROM.name
PROOF = ROOT / initial.PROOF.name
OUTPUT = initial.OUTPUT
transform, relocate, reference = initial.transform, initial.relocate, initial.reference
AMENDMENTS = {
    2690: dict(english="I can't let this be the end of me... I'll avenge this defeat!",
               localization_note='Keep the personal resolve and place the vow together after the pause.'),
    2695: dict(english="Blast it! It can't end like this! I'll settle this score yet!",
               localization_note='Give the seasoned speaker a distinct curse and keep the whole final vow together.'),
    2698: dict(english="Our commander's last wishes... I'll carry them out myself!",
               localization_note='Keep the speaker’s personal promise and place “last wishes” together.'),
    2704: dict(english="Well, I'm in a difficult position. What am I to do now?",
               localization_note='Give the measured admission and uncertain question their own turns in the paragraph.'),
    2705: dict(english="Am I just going to waste away...? No. There must be a place for me.",
               localization_note='Preserve the shift from doubt to resolve and keep the second thought complete.'),
    2707: dict(english="Well, that puts me in a tough spot. What am I supposed to do now...?",
               localization_note='Keep the question together and preserve the hesitation at the end.'),
}


def active_rows(manuscript):
    return FunctionType(initial.active_rows.__code__, vars(initial) | {'AMENDMENTS': AMENDMENTS})(manuscript)


def main():
    source = checked_text(inspect.getsource(initial.main), {
        '(OUTPUT, RELEASE, Path(wrapper.__file__), Path(__file__))':
            '(OUTPUT, RELEASE, Path(wrapper.__file__), Path(initial.__file__), initial.PROOF, Path(__file__))',
    })
    env = vars(initial) | globals()
    exec(compile(source, __file__ + '::phrase-safe-original-portraits', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

