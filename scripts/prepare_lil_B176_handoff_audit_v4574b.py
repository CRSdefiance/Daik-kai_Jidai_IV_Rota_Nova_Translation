"""Keep numeric quantity substitutions out of module names and DK4 paths."""
from pathlib import Path
source=Path(__file__).with_name('prepare_lil_B176_handoff_audit_v4574.py')
text=source.read_text(encoding='utf-8')
replacements={
    "ROOT=Path('work/analysis/lil_B176_audit_preparation_v4574')":"ROOT=Path('work/analysis/lil_B176_audit_preparation_v4574b')",
    "target=Path('scripts/verify_editorial_handoff_v4574.py')":"target=Path('scripts/verify_editorial_handoff_v4574b.py')",
    "r'(?<!\\d)'+k+r'(?!\\d)'":"r'(?<![A-Za-z0-9_])'+k+r'(?![A-Za-z0-9_])'",
}
for old,new in replacements.items():
    assert text.count(old)==1,old
    text=text.replace(old,new)
exec(compile(text,str(source),'exec'),{'__file__':str(source),'__name__':'__main__'})
