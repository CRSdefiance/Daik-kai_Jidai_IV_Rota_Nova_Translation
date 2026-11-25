"""Bind the corrected source-owned header-only fixture;original observer unchanged."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/run_lil_B152_B154_display_fixture_v3645.py');t=p.read_text(encoding='utf-8');t=t.replace('lil_B152_B154_display_fixture_v3644','lil_B152_B154_display_fixture_v3644b').replace('lil_B152_B154_display_run_v3645_','lil_B152_B154_display_run_v3645b_').replace('lil_B152_B154_display_v3645_','lil_B152_B154_display_v3645b_');exec(compile(t,str(p)+'::headers-once-fixture','exec'),dict(__name__='__main__',__file__=__file__))
