"""Cold original direct-town controls with pre-battle location/crew assignment."""
import inspect
from pathlib import Path
from scripts import run_aftermath_city_v1283 as previous
from scripts.native_aftermath_town_fixture_v1290 import ROM, apply_fixture

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    source = source.replace('Amsterdam','SaoTomeFirstMate').replace("'city_context'", "'town_context'")
    source = source.replace('scripts/native_aftermath_city_fixture_v1282.py','scripts/native_aftermath_town_fixture_v1290.py')
    source = source.replace("{'until':5110,'duration':1}", "{'until':5110,'buttons':['Y'],'duration':16}")
    env = {**previous.__dict__, '__file__':__file__, 'ROM':ROM, 'apply_fixture':apply_fixture,
           'ROOT':Path('work/analysis/aftermath_town_v1291'),
           'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_town_v1291_1266')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
