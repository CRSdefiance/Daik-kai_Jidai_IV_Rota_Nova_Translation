"""Emit relative command headers once;preserve failed whole-container fixture derivation."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/research_lil_B152_B154_display_fixture_v3644.py');t=p.read_text(encoding='utf-8');t=t.replace('lil_B152_B154_display_fixture_v3644','lil_B152_B154_display_fixture_v3644b').replace('lil_B152_B154_display_v3644_','lil_B152_B154_display_v3644b_');a="value=bank[n][at:at+extent];row=";b="extent=4 if c['word'] in [0x100,0x200,0x300,0x400] else extent;value=bank[n][at:at+extent];row=";assert a in t;t=t.replace(a,b);exec(compile(t,str(p)+'::headers-once','exec'),dict(__name__='__main__',__file__=__file__))
