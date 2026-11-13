"""Original direct-town input with disclosed Gunnery/staffing prerequisites."""
import inspect
from pathlib import Path
from scripts import run_aftermath_city_v1283 as previous
from scripts.native_town_gunnery_fixture_v1299 import ROM,apply_fixture

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    source = source.replace('Amsterdam','SaoTomeGunnery').replace("'city_context'","'town_context'")
    source = source.replace('scripts/native_aftermath_city_fixture_v1282.py','scripts/native_town_gunnery_fixture_v1299.py')
    source = source.replace("{'until':5110,'duration':1}","{'until':5110,'buttons':['Y'],'duration':16}")
    env = {**previous.__dict__,'__file__':__file__,'ROM':ROM,'apply_fixture':apply_fixture,
        'ROOT':Path('work/analysis/town_gunnery_v1300'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_gunnery_v1300_1266')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
