"""Successor:acknowledge already-viewed report families;stop on sailor loss312."""
from pathlib import Path
if __name__=='__main__':
    source=Path('scripts/navigate_search_reports_v1681.py').read_text(encoding='utf-8')
    old="'KNOWN':{308,309,2234,2239,2244,2245,339},'TARGETS':set(IDS)|{310,*range(2275,2288)}"
    assert source.count(old)==1
    source=source.replace(old,"'KNOWN':{308,309,2234,2239,2244,2245,339,310,*range(2275,2288),*range(2217,2222),*range(2229,2234)},'TARGETS':{312}")
    source=source.replace('bounded_navigator_v1681.jsonl','bounded_navigator_v1681b.jsonl')
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
