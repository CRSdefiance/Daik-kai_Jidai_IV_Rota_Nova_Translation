"""Successor:account explicitly for the native zero-ink six-pixel speech margin."""
from pathlib import Path

if __name__ == '__main__':
    source = Path('scripts/probe_search_reports_fonts_v1663.py').read_text(encoding='utf-8')
    source = source.replace('work/analysis/search_reports_fonts_v1663', 'work/analysis/search_reports_fonts_v1663b')
    old = "            actual = [e for e in events if e['y'] == row_index*16]"
    new = """            origin = 0 if n == 312 else 6
            margin = [e for e in events if e['y'] == row_index*16 and e['x'] < origin]
            assert all(e['code'] == 32 and e['x'] == 0 for e in margin)
            guards.extend(margin)
            actual = [e for e in events if e['y'] == row_index*16 and e['x'] >= origin]"""
    assert source.count(old) == 1
    source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
