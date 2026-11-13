"""Fix a Python conditional-expression spacing error before any test output."""
from pathlib import Path
OLD=Path('scripts/verify_aftermath_fled_fonts_v2542.py')
if __name__=='__main__':
 source=OLD.read_text();assert source.count('else255')==2
 source=source.replace('else255','else 255').replace('aftermath_fled_fonts_v2542','aftermath_fled_fonts_v2542b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
