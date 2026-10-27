"""Include the review literal's closing quote in its replacement boundary."""
from pathlib import Path
source=Path(__file__).with_name('prepare_lil_B177_native_approval_v4622.py')
text=source.read_text(encoding='utf-8')
old='end=text.index("\'})",start)'
assert text.count(old)==1
text=text.replace(old,old+'+1')
exec(compile(text,str(source)+'::literal-boundary-successor','exec'),{'__file__':__file__,'__name__':'__main__'})
