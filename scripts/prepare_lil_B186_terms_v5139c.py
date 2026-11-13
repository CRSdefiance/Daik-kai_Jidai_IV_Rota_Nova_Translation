"""Allow three explicit output-address additions while preserving existing constants."""
from collections import Counter
from pathlib import Path
import re
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive

def derive(a,b,changes):
    source=Path(a).read_text(encoding='utf-8')
    for key in changes:assert key in source,key
    target=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],source)
    compile(target,str(b),'exec')
    before,after=native_numbers(source),native_numbers(target)
    assert not before-after
    assert after-before==Counter({0x1223E4:1,0x15E4D0:1,0x1230B4:1})
    row=original_derive(a,b,changes)
    return {**row,'existing_native_constants_and_multiplicities_preserved':True,'only_new_integer_literals_are_three_explicit_output_address_fields':True}

if __name__=='__main__':
    source=Path('scripts/prepare_lil_B186_terms_v5139b.py').read_text(encoding='utf-8')
    old='from scripts.source_locked_derivation_v5118 import derive\n'
    assert source.count(old)==1
    source=source.replace(old,'').replace('lil_B186_terms_preparation_v5139b','lil_B186_terms_preparation_v5139c')
    exec(compile(source,__file__+'::explicit-output-address-additions','exec'),globals())
