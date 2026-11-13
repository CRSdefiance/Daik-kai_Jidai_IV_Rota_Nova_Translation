"""Account for the original ASCII pair renderer's exact odd trailing blank.

V1397 stopped at its glyph-event assumption after complete pixels already
matched. The original renderer emits one blank cell for an odd final pair;
require that precise event rather than dropping or ignoring glyph events.
"""
from pathlib import Path


if __name__=='__main__':
    path = Path('scripts/probe_battle_victory_fonts_v1397.py')
    source = path.read_text(encoding='utf-8')
    for old,new in [
        ('work/analysis/battle_victory_fonts_v1397','work/analysis/battle_victory_fonts_v1397b'),
        ("        assert [e['code'] for e in events]==list(formatted)",
         "        expected_codes = list(formatted)+([32] if len(formatted)%2 else [])\n        assert [e['code'] for e in events]==expected_codes"),
        ('[(6*i,0,1) for i in range(len(formatted))]','[(6*i,0,1) for i in range(len(expected_codes))]'),
        ("'original_leading_cell_count':1,","'original_leading_cell_count':1,'original_odd_pair_trailing_blank_cells':len(expected_codes)-len(formatted),")]:
        assert source.count(old)==1,(old,source.count(old))
        source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
