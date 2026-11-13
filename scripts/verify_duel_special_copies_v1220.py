"""All7336 native copies and180 cache sequences under the special dispatch.

The opaque component's dedicated parser preserves its executable prefix.
The public single-slot function retains its exact original return0/BX entry.
"""
import inspect
from pathlib import Path
from dk4tool.patch.duel_editorial import owned_entries
from scripts import verify_duel_cache_copies_v1163 as previous


def main():
    source = inspect.getsource(previous.main)
    old = 'work/analysis/duel_native_release_v1162/final_payload_plan.json'
    assert source.count(old) == 1
    source = source.replace(old, 'work/analysis/duel_special_native_v1218/native_payload_plan.json')
    env = {**previous.__dict__, '__file__': __file__, 'entries': owned_entries,
           'ROOT': Path('work/analysis/duel_special_copies_v1220')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
