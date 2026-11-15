"""Compare the localized Hint footer with its exact parent through the town return."""

import argparse
from inspect import getsource
from types import SimpleNamespace

from scripts import probe_ancient_map_documents_v1 as original
from scripts import replay_ancient_map_hint_label_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, stage, navigation = prior.base, prior.stage, prior.navigation
ROOT = stage.ROOT / 'exact_parent_comparison'
END = 12700
COMMANDS = (*navigation.COMMANDS[:-1], dict(until=12300, buttons=[], duration=8),
            dict(until=END, buttons=['B'], duration=8), dict(stop=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('side', choices=('parent', 'hint'))
    side = parser.parse_args().side
    registered = base.load(stage.parent.RELEASE)
    staged = base.load(stage.PROOF)
    assert registered['candidate_sha256'] == staged['parent_sha256']
    rom, expected = (stage.parent.ROM, registered) if side == 'parent' else (stage.ROM, staged)
    prior.map_replay.stage = SimpleNamespace(ROM=rom)
    source = checked_text(getsource(original.main), {
        'release = base.load(parent.RELEASE)': 'release = expected',
        'from scripts.probe_ancient_map_documents_v1 import set_condition':
            'from scripts.replay_ancient_map_hint_label_v1 import set_condition',
    })
    environment = vars(original) | dict(ROOT=ROOT / side, ROM=rom, expected=expected,
                                        END=END, COMMANDS=COMMANDS, __file__=__file__)
    ROOT.mkdir(exist_ok=True)
    exec(compile(source, __file__ + '::exact-parent-hint-footer', 'exec'), environment)
    environment['main']()


if __name__ == '__main__':
    main()
