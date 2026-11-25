"""Compare the active Rafael confirmation and cumulative startup on the two ROMs."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_kurushima_encounter_20261115 as startup_workflow
from scripts import replay_rafael_setup_labels_20261115 as setup_workflow
from scripts import stage_setup_confirmation_prose_20261115 as stage


def replay(side):
    scope = vars(setup_workflow) | {'stage': stage, 'ROOT': stage.ROOT}
    FunctionType(setup_workflow.replay.__code__, scope)(side)


def startup():
    scope = vars(startup_workflow) | {'stage': stage}
    FunctionType(startup_workflow.startup.__code__, scope)()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('before', 'after', 'startup'))
    mode = parser.parse_args().mode
    if mode == 'startup':
        startup()
    else:
        replay(mode)
