"""Replay original unforced powder fire in registered V1316;two untouched holds."""
import inspect
from pathlib import Path
from scripts import run_town_hold_v1297 as previous
from scripts.native_powder_fire_fixture_v1319 import ROM,apply_fixture

if __name__ == '__main__':
    source = inspect.getsource(previous.main)
    changes = [
        ('work/analysis/aftermath_town_v1291/navigation.jsonl','work/analysis/town_gunnery_v1300/navigation.jsonl'),
        ("<= 5910", "<= 7210"),
        ("commands[-1]['until'] == 5910", "commands[-1]['until'] == 7210"),
        ('SaoTomeFirstMate','SaoTomeGunnery'),
        ("commands += [{'until':6010,'touch':[128,96],'duration':8}]", "commands += [{'until':7250,'duration':1}]"),
        ('scripts/native_aftermath_town_fixture_v1290.py','scripts/native_powder_fire_fixture_v1319.py')]
    for old,new in changes:
        assert source.count(old) >= 1,old
        source = source.replace(old,new)
    env = {**previous.__dict__,'__file__':__file__,'ROM':ROM,'apply_fixture':apply_fixture,
        'ROOT':Path('work/analysis/powder_fire_scene_v1320'),
        'CAP':Path('E:/Rota Nova translations/Generated/work/emulation_v193/powder_fire_v1320_1316')}
    exec(compile(source,__file__,'exec'),env)
    env['main']()
