"""Complete current barmaid native font pages and independent physical glyph planes."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read

matrix=read('work/analysis/barmaid_context_layouts_v2217/all31_current_native_layouts.json')
count=len(matrix['representative_full_font_indices'])
source=Path('scripts/verify_tavern_fonts_v2189.py').read_text()
for old,new in (
    ('tavern_fonts_v2189','barmaid_context_fonts_v2218'),
    ('tavern_layouts_v2188/all63_current_native_layouts.json','barmaid_context_layouts_v2217/all31_current_native_layouts.json'),
    ("matrix['case_count']==67454","matrix['case_count']==273"),
    ('len(fonts)==310',f'len(fonts)=={count}'),
    ('set(range(820,883))','set(range(989,1020))'),
    ('all63','all31'),('all67454','all273'),('all310',f'all{count}'),
):
    assert old in source,old
    source=source.replace(old,new)
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
