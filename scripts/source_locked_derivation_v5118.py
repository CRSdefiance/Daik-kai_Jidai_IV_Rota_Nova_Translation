"""Reject accidental native-number changes while preparing frozen successors."""
import ast,re
from collections import Counter
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive

def native_numbers(text):
    return Counter(n.value for n in ast.walk(ast.parse(text)) if isinstance(n,ast.Constant)
        and type(n.value) is int and n.value>=0x20000)

def checked_text(source,changes):
    for key in changes:
        if key not in source:raise ValueError('Derivation key absent:'+key)
    target=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],source)
    compile(target,'<source-locked-successor>','exec')
    a,b=native_numbers(source),native_numbers(target)
    if a!=b:
        raise ValueError('Native numeric constants changed:removed='+repr(dict(a-b))+';added='+repr(dict(b-a)))
    return target

def derive(a,b,changes):
    source=Path(a).read_text(encoding='utf-8');planned=checked_text(source,changes)
    result=original_derive(a,b,changes)
    assert Path(b).read_text(encoding='utf-8')==planned
    return {**result,'native_high_integer_constants_and_multiplicity_preserved':True}
