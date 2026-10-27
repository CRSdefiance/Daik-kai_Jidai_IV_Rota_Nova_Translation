"""Respect FE's12px logical rows and64px physical plane in the existing typed painter."""
from pathlib import Path
if __name__=='__main__':
    a=Path('scripts/verify_lil_B142_B145_fonts_v3586.py');t=a.read_text(encoding='utf-8');changes=[('lil_B142_B145_fonts_v3586','lil_B142_B145_fonts_v3586b'),("0<=e['y']<=48 and e['y']%16==0","0<=e['y']<=(36 if fe else 48) and e['y']%(12 if fe else 16)==0"),('all_visible_origins_zero_and16px_rows_within4rows=True','all_visible_origins_zero_and_native_rows_within4rows=True,logical_row_pitch=12 if fe else 16,physical_row_pitch=16')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    exec(compile(t,str(Path(__file__))+'::FE_logical_row_correction','exec'),dict(__name__='__main__',__file__=__file__))
