"""Preserve the stopped count assertion and derive the accurately counted receipt."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_layout_count_correction_v5667c')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('scripts/refine_lil_B197_layout_v5667b.py','scripts/refine_lil_B197_layout_v5667c.py',{
        '5667b':'5667c','53-character':'56-character','29 and23':'31 and24',
        "==53 and list(map(len,expected))==[29,23]":"==56 and list(map(len,expected))==[31,24]"})
    ROOT.mkdir(parents=True);save(ROOT/'stopped_receipt_count_assertion_preserved.json',dict(tool=tool,
        original_error='Hand-counted53/29/23 was incorrect;actual saved QA rows are31 and24 characters,56 including their separating space.',
        original_stopped_before_successor_or_receipt_creation=True,no_word_or_compiled_byte_or_native_rule_changed=True,new_credit=0))
