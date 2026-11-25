"""Two no-save cold boots ofthe disclosed B155 display fixtures;read-only observer."""
from pathlib import Path
if __name__=='__main__':
    p=Path('scripts/run_lil_B152_B154_display_fixture_v3645.py');t=p.read_text(encoding='utf-8');changes=[('lil_B152_B154_display_fixture_v3644','lil_B155_display_fixture_v3687'),('lil_B152_B154_display_run_v3645_','lil_B155_display_run_v3688_'),('lil_B152_B154_display_v3645_','lil_B155_display_v3688_'),('source_events152_to154_not_selected','source_event155_not_selected'),("'--frames','24401'","'--frames','20401'"),('range(2600,23501,240)','range(2600,19501,240)'),('range(2350,24001,60)','range(2350,20001,60)'),('explicit_B22_three_exchange_fixture','explicit_B22_B155_flattened_display_fixture')]
    for a,b in changes:assert a in t,a;t=t.replace(a,b)
    exec(compile(t,str(p)+'::B155-disclosed-display-scope','exec'),dict(__name__='__main__',__file__=__file__))
