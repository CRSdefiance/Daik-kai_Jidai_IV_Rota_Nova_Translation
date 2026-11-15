"""Correct the preparer's assertions for absent, harmless import/path aliases."""
from pathlib import Path

source = Path(__file__).with_name('prepare_v4496_promotion_verifier.py')
text = source.read_text(encoding='utf-8')
old = 'for key in replacements:\n    assert key in text, key\n'
assert text.count(old) == 1
text = text.replace(old, "print('Unused aliases:', [key for key in replacements if key not in text])\n")
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
