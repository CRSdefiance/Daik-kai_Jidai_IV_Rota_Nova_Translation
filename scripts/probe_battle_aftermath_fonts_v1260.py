"""Rerun the complete783-case original pipeline/font matrix for refined prose."""
from pathlib import Path


if __name__ == '__main__':
    path = Path('scripts/probe_battle_aftermath_fonts_v1256b.py')
    source = path.read_text(encoding='utf-8')
    old = "'ROOT':Path('work/analysis/battle_aftermath_fonts_v1256b')}"
    new = """'ROOT':Path('work/analysis/battle_aftermath_fonts_v1260'),
        'PLAN':Path('work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json'),
        'MANUSCRIPT':Path('translations/battle_aftermath_editorial_manuscript_v2.json')}"""
    assert source.count(old) == 1
    source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
