"""Open the revised sailing Help and exercise its original links and history."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import register_tavern_help_20261120 as parent
from scripts import replay_tavern_help_20261120 as earlier
from scripts import stage_sailing_help_20261120 as stage
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = stage.ROOT
NAV = ROOT / 'navigation/navigation_plan.json'
CAPTURE = ROOT / 'gameplay'
LIVE = ROOT / 'gameplay_verification/ordinary_gameplay_verification.json'
ACTIONS = [
    dict(open=11), dict(open=73), dict(open=74), dict(open=76), dict(remember='Auto Move'),
    dict(open=104), dict(key='L'), dict(return_to='Auto Move'),
    dict(key='L'), dict(key='L'), dict(key='L'), dict(key='L'),
    dict(open=82), dict(open=85), dict(remember='Info'),
    dict(open=86), dict(open=85), dict(return_to='Info'), dict(key='L'), dict(key='L'),
    dict(open=87), dict(open=85), dict(return_to='Info'),
]

source = checked_text(earlier.source, {"required_topics=sorted(stage.ARTICLES.keys() | stage.CHILDREN.values())":
    "required_topics=sorted(stage.ARTICLES)"})
env = earlier.env | globals()
exec(compile(source, __file__ + '::sailing-help-gameplay', 'exec'), env)
startup = FunctionType(earlier.startup.__code__, env)


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('gameplay', 'startup'))
    if parser.parse_args().action == 'gameplay':
        env['gameplay']()
    else:
        startup()
