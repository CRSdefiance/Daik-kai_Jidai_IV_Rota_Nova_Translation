"""Preserve2646 syntax-only refusal;separate conditional keywords and numbers."""
from pathlib import Path
import re
if __name__=='__main__':
 source=Path('scripts/verify_support_fonts_v2646.py').read_text();source=re.sub(r'\belse(?=\d)','else ',source).replace('support_fonts_v2646','support_fonts_v2646b');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
