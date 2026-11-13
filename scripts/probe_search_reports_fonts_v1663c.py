"""Successor:distinguish raw template from original printf-expanded input."""
from pathlib import Path

if __name__ == '__main__':
    source = Path('scripts/probe_search_reports_fonts_v1663.py').read_text(encoding='utf-8')
    source = source.replace('work/analysis/search_reports_fonts_v1663', 'work/analysis/search_reports_fonts_v1663c')
    source = source.replace('from scripts.search_reports_native_consumers_v1662 import', 'from scripts.search_reports_native_consumers_v1662b import')
    old = "            actual = [e for e in events if e['y'] == row_index*16]"
    new = """            origin = 0 if n == 312 else 6
            margin = [e for e in events if e['y'] == row_index*16 and e['x'] < origin]
            assert all(e['code'] == 32 and e['x'] == 0 for e in margin)
            guards.extend(margin)
            actual = [e for e in events if e['y'] == row_index*16 and e['x'] >= origin]"""
    assert source.count(old) == 1
    source = source.replace(old, new)
    old = "        assert native.get('input_hex', native.get('loaded_template_hex')) == value.hex()"
    assert source.count(old) == 1
    source = source.replace(old, "        assert native['loaded_template_hex'] == value.hex()")
    old = "        formatted = bytes.fromhex(native['formatted_hex'])"
    assert source.count(old) == 1
    source = source.replace(old, "        if n != 312: assert native['input_hex'] == expected.hex()\n" + old)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
