"""Explicit successor: native full-font/name tests for refined retreat prose."""
from pathlib import Path
from scripts import probe_retreat_transfer_fonts_v1512 as previous

if __name__ == '__main__':
    source = Path(previous.__file__).read_text(encoding='utf-8')
    for old, new in [
        ('from scripts.retreat_transfer_native_plan_v1511b import compiled',
         'from scripts.retreat_transfer_native_plan_v1514 import compiled'),
        ('work/analysis/retreat_transfer_fonts_v1512', 'work/analysis/retreat_transfer_fonts_v1515'),
        ('work/analysis/retreat_transfer_payload_v1511b/native_payload_plan.json',
         'work/analysis/retreat_transfer_payload_v1514/native_payload_plan.json'),
        ('translations/retreat_transfer_editorial_manuscript_v1.json',
         'translations/retreat_transfer_editorial_manuscript_v2.json'),
        ("'and','or'}", "'and','or','get','fall',\"we're\",\"let's\"}"),
    ]:
        assert source.count(old) == 1, old
        source = source.replace(old, new)
    exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
