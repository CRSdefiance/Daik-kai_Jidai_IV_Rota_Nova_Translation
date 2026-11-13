"""Allow removal of the two B191 RNG constants because B194 uses actor availability."""
from scripts.source_locked_derivation_v5118 import derive

if __name__ == '__main__':
    print(derive('scripts/prepare_lil_B194_actual_audit_v5517.py', 'scripts/prepare_lil_B194_actual_audit_v5517c.py', {
        'from scripts.source_locked_derivation_v5118 import derive': '''from pathlib import Path
import re
from collections import Counter
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive

def derive(a,b,changes):
    source=Path(a).read_text(encoding='utf-8')
    assert all(k in source for k in changes)
    target=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],source)
    compile(target,b,'exec')
    before,after=native_numbers(source),native_numbers(target)
    assert before-after==Counter({4294967295:1,1103515245:1}) and not after-before
    result=original_derive(a,b,changes)
    assert Path(b).read_text(encoding='utf-8')==target
    return {**result,'only_removed_constants_are_B191_LCG_multiplier_and_modulus_mask':True,
        'all_native_addresses_and_other_high_constants_exact':True}''',
    }))
