"""Distinguish the predecessor's measured PRNG data from native instruction constants."""
import ast
import re
from pathlib import Path
from collections import Counter
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive
from scripts.verify_village_wrap_v608 import read

def derive_with_reviewed_data(a,b,changes):
    assert a=='dk4tool/patch/lil_B195_editorial_v1.py' and b=='dk4tool/patch/lil_B199_editorial_v1.py'
    source=Path(a).read_text(encoding='utf-8')
    doc=read('translations/lil_B195_editorial_manuscript_v3.json')
    observed=read(doc['postscene_native_state_proof'])
    data=observed['postscene9001_PRNG_seeds']
    sites=[]
    for n in ast.walk(ast.parse(source)):
        if (isinstance(n,ast.Compare) and isinstance(n.left,ast.Subscript) and isinstance(n.left.slice,ast.Constant)
            and n.left.slice.value=='postscene9001_PRNG_seeds'):
            assert len(n.comparators)==1 and isinstance(n.comparators[0],ast.List)
            values=[v.value for v in n.comparators[0].elts];assert values==data
            sites.append(values)
    assert sites==[data]
    for key in changes:assert key in source,key
    planned=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],source)
    compile(planned,b,'exec')
    before,after=native_numbers(source),native_numbers(planned)
    # The only high literals in this predecessor compiler are this independently
    # bound measured-data comparison. No native address or instruction is waived.
    assert before==Counter(data) and after==Counter()
    result=original_derive(a,b,changes)
    assert Path(b).read_text(encoding='utf-8')==planned
    return {**result,'native_instruction_and_address_integer_constants_unchanged':True,
        'retired_predecessor_measured_data_literals':data,'retired_data_owner':doc['postscene_native_state_proof'],
        'data_roles_verified_by_AST_comparison_not_string_obfuscation':True,
        'new_scene_measured_PRNG_values_bound_through_original_proofs_not_inherited':True}
