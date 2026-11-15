"""Use complete table pointers and active noncaptain source voice objects.

V1256 stopped before the first font case: it compared a full table pointer
with low-word metadata, then correctly rejected the inactive base copy of
the captain. This successor selects existing noncaptain alternatives and
verifies both original role queries, without changing any actor identity.
"""
import inspect
from pathlib import Path

from scripts import probe_battle_aftermath_fonts_v1256 as previous


if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    replacements = {
        '    representatives = {}':
        "    source_cpu,source_get = get_machine(original_arm,raw)\n    captain_id = source_get(0x7F244)\n    representatives = {}",
        "        for choice in t['all208_original_selections']:\n            representatives.setdefault":
        "        for choice in t['all208_original_selections']:\n            if choice['actor_ID'] == captain_id:\n                continue\n            representatives.setdefault",
        'direct_keys = set(next(v for p,o,h,v in contract_rows() if p == 0x02053F40))':
        'direct_keys = {0x02110000|v for p,o,h,values in contract_rows() if p == 0x02053F40 for v in values}',
    }
    for old,new in replacements.items():
        assert source.count(old) == 1,old
        source = source.replace(old,new)
    helper = inspect.getsource(previous.assigned_role_raw)
    old = 'assert get(0x82428,duty,1) == actor_object'
    assert helper.count(old) == 1
    helper = helper.replace(old,old+'\n    assert get(0x82478,duty,1) == actor_id')
    env = {**previous.__dict__,'__file__':__file__,
        'ROOT':Path('work/analysis/battle_aftermath_fonts_v1256b')}
    exec(compile(helper,__file__,'exec'),env)
    exec(compile(source,__file__,'exec'),env)
    env['main']()
