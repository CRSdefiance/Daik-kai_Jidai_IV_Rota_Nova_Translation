"""Apply the qualified complete reconstruction with B294's one credited context speech."""
from scripts import rebuild_lil382_credited_context_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    "g['block']==115": "g['block']==294",
    'if block==115:': 'if block==294:',
    'assert not compound and len(records)==32': 'assert not compound and len(records)==15',
    'expected_context_objects=9,expected_context_speeches=4': 'expected_context_objects=1,expected_context_speeches=1',
})

env = {**previous.env, '__file__': __file__}
exec(compile(source, __file__ + '::same-complete-guards-exact-B294-credited-context', 'exec'), env)

if __name__ == '__main__':
    env['main']()
