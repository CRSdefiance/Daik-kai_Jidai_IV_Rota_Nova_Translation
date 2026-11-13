"""Preserve the pre-manuscript failure;call each row's selected consumer compiler."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/review_sea_inspection_context_v2613.py').read_text();assert source.count('and compiled(r)==')==1
 source=source.replace('and compiled(r)==','and compiler(r)==').replace('sea_inspection_editorial_v2613','sea_inspection_editorial_v2613b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
