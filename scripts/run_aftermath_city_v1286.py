"""Original Madeira target controls; location-only fixture before any conflict."""
import inspect
from pathlib import Path
from scripts import run_aftermath_city_v1283 as previous
from scripts.native_aftermath_city_fixture_v1285 import ROM, apply_fixture

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    source = source.replace('Amsterdam', 'MadeiraNeutral').replace(
        'scripts/native_aftermath_city_fixture_v1282.py', 'scripts/native_aftermath_city_fixture_v1285.py')
    source = source.replace("{'until':5110,'duration':1}", "{'until':5110,'buttons':['Y'],'duration':16}")
    env = {**previous.__dict__, '__file__': __file__, 'ROM': ROM, 'apply_fixture': apply_fixture,
           'ROOT': Path('work/analysis/aftermath_city_v1286'),
           'CAP': Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_city_v1286_1266')}
    exec(compile(source, __file__, 'exec'), env)
    env['main']()
