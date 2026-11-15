"""Correct the progressive receipt key; preserve the two failed audit producers."""
from pathlib import Path
SOURCE=Path('scripts/audit_hodram_opening_actual_v2027b.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    old="assert sha(pixels)==proof['native_plane_sha256'];width=216"
    new="assert sha(pixels)==proof['native_font_plane_sha256'];width=216"
    assert text.count(old)==2;text=text.replace(old,new).replace(".replace('hodram_opening_actual_v2027','hodram_opening_actual_v2027b')",".replace('hodram_opening_actual_v2027','hodram_opening_actual_v2027c')")
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
