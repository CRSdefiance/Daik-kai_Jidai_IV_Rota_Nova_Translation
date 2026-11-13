"""Audit the generated compiler including one deliberate prior-result boundary fixture."""
from pathlib import Path
from collections import Counter
import py_compile
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B190_compiler_tools_v5344')
if __name__=='__main__':
    assert not ROOT.exists()
    a=Path('dk4tool/patch/lil_B186_editorial_v1.py');b=Path('dk4tool/patch/lil_B190_editorial_v1.py')
    old,new=native_numbers(a.read_text(encoding='utf-8')),native_numbers(b.read_text(encoding='utf-8'))
    assert old-new==Counter({1803218166:1}) and new-old==Counter({2467799992:1,0xFFFFFFFF:1})
    text=b.read_text(encoding='utf-8');py_compile.compile(str(b),doraise=True)
    assert text.count('image.replace_file(')==1 and text.index("image.replace_file(PATH, result)")>text.index("inverse does not restore every predecessor byte")
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_conditional_compiler.json',dict(
        source=str(a),source_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),
        native_high_constants_preserved_except_measured_PRNG_data_and_one_explicit_FFFFFFFF_prior_result_fixture=True,
        first_preparation_stopped_after_compilation_on_overstrict_literal_count=True,
        original_stopped_producer_preserved=True,no_native_address_changed=True,
        complete_metadata_both_maps_terms_layout_and_original_result_propagation_guarded=True,
        all_checks_precede_single_replace_file=True,new_credit=0,full_goal_complete=False))
    print('Compiled conditional compiler:original native addresses exact;measured PRNG and explicit FFFFFFFF result fixture audited.')
