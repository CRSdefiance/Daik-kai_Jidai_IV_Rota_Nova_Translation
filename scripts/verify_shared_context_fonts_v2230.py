"""Complete current50 native font pages, plus separate physical glyph-plane oracles."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read

matrix=read('work/analysis/shared_context_layouts_v2229/all50_current_native_layouts.json')
count=len(matrix['representative_full_font_indices'])
source=Path('scripts/verify_tavern_fonts_v2189.py').read_text()
for old,new in(('tavern_fonts_v2189','shared_context_fonts_v2230'),('tavern_layouts_v2188/all63_current_native_layouts.json','shared_context_layouts_v2229/all50_current_native_layouts.json'),("matrix['case_count']==67454","matrix['case_count']==857"),('len(fonts)==310',f'len(fonts)=={count}'),('set(range(820,883))','set(range(1020,1070))'),('all63','all50'),('all67454','all857'),('all310',f'all{count}')):
    assert old in source,old
    source=source.replace(old,new)
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
