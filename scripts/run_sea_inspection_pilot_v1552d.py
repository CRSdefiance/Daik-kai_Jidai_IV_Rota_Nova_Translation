"""Dismiss the original departure notice before checking normal world activation."""
from pathlib import Path
from scripts import run_sea_inspection_pilot_v1552c as previous

if __name__ == '__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    old = "commands = [{'until': 4900, 'duration': 1, 'battle_fixture': {'sea_inspection_context': 'activate_existing_Monster_Fish'}}, {'stop': True}]"
    new = "commands = [{'until': 4900, 'duration': 1, 'battle_fixture': {'sea_inspection_context': 'activate_existing_Monster_Fish'}}, {'until': 5000, 'buttons': ['A'], 'duration': 4}, {'until': 5100, 'duration': 1}, {'stop': True}]"
    assert source.count(old) == 1
    source = source.replace(old, new)
    for old, new in [('work/analysis/sea_inspection_pilot_v1552c', 'work/analysis/sea_inspection_pilot_v1552d'),
                     ('sea_inspection_pilot_v1552c_1542', 'sea_inspection_pilot_v1552d_1542')]:
        assert source.count(old) == 1
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
