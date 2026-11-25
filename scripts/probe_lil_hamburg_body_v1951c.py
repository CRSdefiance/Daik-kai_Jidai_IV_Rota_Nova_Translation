"""Recheck successor79 bodies; separate FE native display approval still pending."""
from pathlib import Path

SOURCE=Path('scripts/probe_lil_hamburg_body_v1951.py')

if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8')
    for old,new in(('lil_hamburg_recruitment_editorial_manuscript_v1.json','lil_hamburg_recruitment_editorial_manuscript_v2.json'),
        ('lil_Hamburg_body_probe_v1951','lil_Hamburg_body_probe_v1951c')):
        assert text.count(old)==1
        text=text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
