"""Successor probes valid low attributes6 rather than the minimum1."""
import inspect
from pathlib import Path
from scripts import research_duel_health_limits_v1238 as previous


if __name__=='__main__':
    source=inspect.getsource(previous.main)
    for old,new in [('get(0x7E750,actor,index,1-before)','get(0x7E750,actor,index,6-before)'),
                    ('get(0x7E944,actor,index)==1','get(0x7E944,actor,index)==6')]:
        assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/duel_health_limits_v1238b')}
    exec(compile(source,__file__,'exec'),env);env['main']()
