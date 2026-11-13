"""Exercise the translated Y-button label, clue view and original Back path."""

from inspect import getsource

from scripts import probe_ancient_map_documents_v1 as original
from scripts import probe_ancient_map_documents_v4 as navigation
from scripts import replay_ancient_map_text_v1 as map_replay
from scripts import stage_ancient_map_hint_label_v1 as stage
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = stage.ROOT / 'ancient_map'
base = stage.base


def set_condition(arm, raw, request):
    return map_replay.set_condition(arm, raw, request)


def main():
    expected = base.load(stage.PROOF)
    release = base.load(stage.parent.RELEASE)
    assert expected['parent_sha256'] == release['candidate_sha256']
    old = base.load(navigation.ROOT / 'terminal.json')
    assert base.digest(old['commands']) == old['commands_sha256']
    source = checked_text(getsource(original.main), {
        "release = base.load(parent.RELEASE)": "release = expected",
        'from scripts.probe_ancient_map_documents_v1 import set_condition':
            'from scripts.replay_ancient_map_hint_label_v1 import set_condition',
    })
    map_replay.stage = stage
    environment = vars(original) | dict(ROOT=ROOT, ROM=stage.ROM, COMMANDS=navigation.COMMANDS,
                                        expected=expected, __file__=__file__)
    exec(compile(source, __file__ + '::localized-Y-label', 'exec'), environment)
    environment['main']()
    assert base.digest(ROOT / 'commands.jsonl') == old['commands_sha256']


if __name__ == '__main__':
    main()
