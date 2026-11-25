"""Permit only the documented meaning-pending transition; preserve all source bytes and gates."""
import inspect
from scripts import checkpoint_maria301_source_and67_drafts_20261109 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    "assert all(row[k] == v for k, v in original.items()), key":
        "assert all(row[k] == v for k, v in original.items() if k != 'source_meaning_pending'), key\n"
        "        assert original['source_meaning_pending'] and row['source_meaning_pending'] is False",
})
env = {**previous.main.__globals__, '__file__': __file__}
exec(compile(source, __file__ + '::same-checkpoint-allow-explicit-meaning-completion-flag-only', 'exec'), env)
main = env['main']

if __name__ == '__main__':
    main()
