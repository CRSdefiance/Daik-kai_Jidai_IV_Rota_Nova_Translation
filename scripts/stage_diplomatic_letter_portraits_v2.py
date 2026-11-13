"""Refine the phrases split awkwardly in the first native portrait sheets."""

import inspect
from types import FunctionType

from scripts import stage_diplomatic_letter_portraits_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = previous.ROOT.with_name('diplomatic_letter_portraits_staged_20261111_v2')
ROM = ROOT / previous.ROM.name
PROOF = ROOT / previous.PROOF.name
OUTPUT = previous.OUTPUT
AMENDMENTS = {
    2734: dict(english='Taking on %s right now would be a mistake... See if you can turn them down.',
               localization_note='Keep the speaker’s softened instruction and place the faction name together on the opening line.'),
    2740: dict(english="What?! Ending the pact, are they? Damn %s. What's their game?",
               localization_note='Retain the rhetorical tag, curse and suspicion. Keep the final question intact with every captain surname.'),
    2755: dict(english="If that's how you want it, I've got plans of my own. Just you wait!",
               localization_note='Keep the controlled threat and the complete closing warning together.'),
    2767: dict(english="So that's what all this is about... I want no part of that farce!",
               localization_note='Keep the speaker’s dismissive realization and spoken refusal in two coherent beats.'),
    2769: dict(english="So that's what they meant to ask... I have no time for such nonsense!",
               localization_note='Keep the realization and brisk dismissal intact. The latter starts with a complete subject and verb.'),
}


def active_rows(manuscript):
    return FunctionType(previous.active_rows.__code__, vars(previous) | {'AMENDMENTS': AMENDMENTS})(manuscript)


def main():
    source = checked_text(inspect.getsource(previous.main), {
        "env = vars(previous) | globals() | {'transform': wrapper.transform}":
            "env = inherited | globals() | {'transform': wrapper.transform, 'active_rows': active}",
        "(OUTPUT, RELEASE, Path(wrapper.__file__), Path(__file__))":
            "(OUTPUT, RELEASE, Path(wrapper.__file__), Path(prior_stage_file), prior_stage_proof, Path(__file__))",
    })
    env = vars(previous) | globals() | {
        'previous': previous.previous, 'inherited': vars(previous.previous) | vars(previous),
        'active': active_rows, 'prior_stage_file': previous.__file__, 'prior_stage_proof': previous.PROOF,
    }
    exec(compile(source, __file__ + '::phrase-safe-native-portrait-rebuild', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()

