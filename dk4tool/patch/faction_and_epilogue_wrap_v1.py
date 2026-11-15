"""Append only the qualified long-notice selector to the registered runtime."""

import inspect

from dk4tool.patch import discovery_reward_wrap_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text


SOURCE = 'b664fab3098dfadd3e28a344811cfeed5cc6a605bd15996f235f13ba0827887c'
PRIOR = 0x01FFDB54
SCOPE = (334, 342, 343, 344, 345)


def transform(source):
    selector_env = previous.selector.__globals__ | {'PRIOR': PRIOR, 'SCOPE': SCOPE}
    exec(compile(inspect.getsource(previous.selector), __file__ + '::exact-notice-scope', 'exec'), selector_env)
    code = checked_text(inspect.getsource(previous.transform), {
        'Exact registered Shipyard and Fleet Setup ARM9 required':
            'Exact registered Discovery and Rewards ARM9 required',
    })
    env = {**vars(previous), **globals(), 'previous': previous.previous, 'selector': selector_env['selector']}
    exec(compile(code, __file__ + '::unchanged-append-and-complete-inverse', 'exec'), env)
    return env['transform'](source)
