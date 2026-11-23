"""Replay the catalogue's longest revised design and the registered startup."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_embedded_story_roles_20261115 as boot
from scripts import replay_specialized_ship_labels_20261115 as previous
from scripts import stage_trade_and_armed_ship_labels_20261115 as stage
from scripts.source_locked_derivation_v5118 import checked_text


MODEL = 136


def shipyard(version):
    source = checked_text(getsource(previous.replay), {
        "stage.ROOT / 'istanbul_special_parent/capture_report.json'":
            "REFERENCE_ROOT / 'istanbul_special_parent/capture_report.json'",
        "stage.ROOT / 'istanbul_special_continue_inputs.json'":
            "REFERENCE_ROOT / 'istanbul_special_continue_inputs.json'",
    })
    settings = vars(previous) | dict(stage=stage, MODELS={MODEL: 22}, REFERENCE_ROOT=previous.stage.ROOT)
    settings['select_model'] = FunctionType(previous.select_model.__code__, settings)
    exec(compile(source, __file__ + '::existing-stock-model-replay', 'exec'), settings)
    settings['replay'](MODEL, version, 1)


def startup():
    settings = SimpleNamespace(ROOT=stage.ROOT, base=stage.base, ROM=stage.ROM, STORED=stage.OUTPUT,
                               parent=stage.parent)
    FunctionType(boot.startup.__code__, vars(boot) | {'stage': settings})()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('case', choices=('parent', 'staged', 'startup'))
    case = parser.parse_args().case
    startup() if case == 'startup' else shipyard(case)
