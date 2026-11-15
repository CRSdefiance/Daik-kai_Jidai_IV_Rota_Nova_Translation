"""Preserve2634 syntax-only refusal;separate conditional keywords and integers."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/verify_editorial_handoff_v2634.py').read_text()
 for old,new in [('else2','else 2'),('else0','else 0'),('else6','else 6'),('else4','else 4'),('editorial_handoff_verification_v2634','editorial_handoff_verification_v2634b')]:source=source.replace(old,new)
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
