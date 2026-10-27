"""Omit unused historical count aliases while retaining every structural assertion."""
from pathlib import Path
source=Path(__file__).with_name('prepare_lil_B177_handoff_audit_v4624.py')
text=source.read_text(encoding='utf-8')
old='replacements.update({str(k):str(v) for k,v in numbers.items()})'
assert text.count(old)==1
text=text.replace(old,'replacements.update({str(k):str(v) for k,v in numbers.items() if str(k) in text})')
exec(compile(text,str(source)+'::used-quantity-aliases','exec'),{'__file__':__file__,'__name__':'__main__'})
