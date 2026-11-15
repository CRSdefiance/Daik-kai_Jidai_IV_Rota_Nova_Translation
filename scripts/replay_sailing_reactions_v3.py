"""Supply a near-expiry white-whale condition and let the original game advance it."""

from struct import pack, unpack
from inspect import getsource
import sys

from scripts import replay_sailing_reactions_v1 as precedent
from scripts.source_locked_derivation_v5118 import checked_text


stage = precedent.stage
ROOT = precedent.ROOT.with_name('focused_reactions_v3')
END = 12600
COMMANDS = precedent.COMMANDS[:2] + (
    dict(until=11200, condition_fixture={'event': 'whale'}, buttons=['UP'], duration=220),
    dict(until=11400, buttons=['A'], duration=8),
    dict(until=11600, buttons=['A'], duration=8),
    dict(until=11800, buttons=['A'], duration=8),
    dict(until=END, buttons=[], duration=8),
    dict(stop=True),
)
DISMISS_ROOT = precedent.ROOT.with_name('focused_reactions_v4')
DISMISS_END = 12400
DISMISS_COMMANDS = COMMANDS[:-2] + (
    dict(until=12000, buttons=['A'], duration=8),
    dict(until=DISMISS_END, buttons=[], duration=8),
    dict(stop=True),
)


def set_condition(arm, raw, request):
    result, proof = precedent.set_condition(arm, raw, request)
    if request['event'] == 'wind':
        return result, proof
    timestamp = proof['fleet'] - stage.BASE + 0x30
    initial_age = 120
    assert unpack('<I', result[timestamp:timestamp + 4])[0] == proof['original_timestamp']
    result = result[:timestamp] + pack('<I', proof['original_timestamp'] - initial_age) + result[timestamp + 4:]
    proof['fixture_initial_age_ticks'] = initial_age
    allowed = {timestamp - 4, *range(timestamp, timestamp + 4)}
    proof['changes'] = [
        dict(address=stage.BASE + offset, before=raw[offset], after=result[offset])
        for offset in sorted(allowed) if raw[offset] != result[offset]
    ]
    return result, proof


if __name__ == '__main__':
    assert sys.argv[1:] in ([], ['--dismiss'])
    if sys.argv[1:]:
        ROOT, END, COMMANDS = DISMISS_ROOT, DISMISS_END, DISMISS_COMMANDS
    # The replay harness imports the selected condition setter by module name.
    code = checked_text(getsource(precedent.gameplay), {
        'from scripts.replay_sailing_reactions_v1 import set_condition':
            'from scripts.replay_sailing_reactions_v3 import set_condition',
    })
    env = vars(precedent) | globals()
    exec(compile(code, __file__ + '::focused-replay', 'exec'), env)
    env['gameplay']()
