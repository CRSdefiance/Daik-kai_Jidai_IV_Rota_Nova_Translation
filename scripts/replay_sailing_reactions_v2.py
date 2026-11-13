"""Replay the whale exchange through the original 144-tick expiry."""

from types import FunctionType

from scripts import replay_sailing_reactions_v1 as precedent


ROOT = precedent.ROOT.with_name('focused_reactions_v2')
END = 13200
COMMANDS = precedent.COMMANDS[:5] + (
    dict(until=12000, buttons=['A'], duration=8),
    dict(until=12200, buttons=['A'], duration=8),
    dict(until=12600, buttons=[], duration=8),
    dict(until=12800, buttons=['A'], duration=8),
    dict(until=13000, buttons=['A'], duration=8),
    dict(until=END, buttons=['A'], duration=8),
    dict(stop=True),
)


if __name__ == '__main__':
    FunctionType(precedent.gameplay.__code__, vars(precedent) | globals())()
