"""Replay complete native logical/font checks for the fresh 106-entry review."""
from pathlib import Path

source = Path('scripts/verify_tavern_fonts_v2189.py').read_text()
for old, new in (
    ('tavern_fonts_v2189', 'recruitment_scheme_fonts_v2205'),
    ('tavern_layouts_v2188/all63_current_native_layouts.json', 'recruitment_scheme_layouts_v2203b/all106_current_native_layouts.json'),
    ("matrix['case_count']==67454", "matrix['case_count']==56852"),
    ('len(fonts)==310', 'len(fonts)==400'),
    ('set(range(820,883))', 'set(range(883,989))'),
    ('all63', 'all106'),
    ('all67454', 'all56852'),
    ('all310', 'all400'),
):
    assert old in source, old
    source = source.replace(old, new)
exec(compile(source, __file__, 'exec'), {'__name__': '__main__', '__file__': __file__})
