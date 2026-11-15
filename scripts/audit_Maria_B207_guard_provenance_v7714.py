"""Bind identical shared-memory helper AST andseparate measured PRNG constants from addresses."""
import ast
from collections import Counter
from pathlib import Path
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_B207_guard_provenance_v7714')
OLD=Path('dk4tool/patch/papal_trade_atomic_support_v1.py')
NEW=Path('dk4tool/patch/maria_B207_atomic_support_v1.py')
LATER=Path('work/analysis/maria_B207_actual_comparison_v7707/Maria18_scene_portrait_header_pairs_full_measured_timing_RNG_components_RGB_limits.json')
if __name__=='__main__':
    assert not ROOT.exists();a,b=[p.read_text('utf8') for p in [OLD,NEW]]
    def fields(text):
        return next(n for n in ast.walk(ast.parse(text)) if isinstance(n,ast.FunctionDef) and n.name=='fields')
    assert ast.dump(fields(a),include_attributes=False)==ast.dump(fields(b),include_attributes=False)
    old,new=map(native_numbers,[a,b]);seeds=read(LATER)['groups'][0]['final_PRNG_seeds'];assert seeds==[1942423083,327589790]
    added,removed=new-old,old-new
    assert added==Counter(seeds) and removed==Counter([2470616159,2470616159,3950740296,3249748893])
    ROOT.mkdir(parents=True);save(ROOT/'identical_shared_fields_AST_andmeasured_seed_rebinding.json',dict(original_shared_scope=str(OLD),original_shared_scope_sha256=sha(OLD.read_bytes()),Maria_shared_scope=str(NEW),Maria_shared_scope_sha256=sha(NEW.read_bytes()),complete_fields_helper_AST_exact_including_every_pointer_static_payload_andnull_guard=True,all_non_PRNG_high_native_constants_andmultiplicity_identical=True,added_measured_PRNG_constants=dict(added),removed_prior_route_PRNG_constants=dict(removed),measured_Maria_comparison=str(LATER),measured_Maria_comparison_sha256=sha(LATER.read_bytes()),no_generic_derivation_guard_weakened=True,new_credit=0,full_goal_complete=False))
    print('Shared-memory field helper AST exact;all non-PRNG high constants/multiplicity identical. Only two measured Maria seeds replace the separately bound prior route seeds.')
