"""Honor the two original FFFFFFFF voice fallbacks in the powder-fire table."""
import inspect
from pathlib import Path
from scripts import research_powder_fire_context_v1303 as previous

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    changes = [
        ('values == [2052,2053,2054,2054,2054,2055,2056,2057]',
         'values == [2052,2053,0xFFFFFFFF,0xFFFFFFFF,2054,2055,2056,2057]'),
        ('number == values[voice]', 'number == (values[0] if values[voice] == 0xFFFFFFFF else values[voice])'),
        ("'all8_voice_selections':values", "'raw8_voice_table':values,'all8_effective_voice_selections':[values[0] if n == 0xFFFFFFFF else n for n in values]")]
    for old,new in changes:
        assert source.count(old) == 1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/powder_fire_context_v1303b')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
