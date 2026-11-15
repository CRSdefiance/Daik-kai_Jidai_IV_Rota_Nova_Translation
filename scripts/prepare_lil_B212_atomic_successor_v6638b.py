"""Correct only a proof-schema field; preserve the rejected v1 compiler and producer."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B212_atomic_successor_v6638b')
if __name__=='__main__':
    assert not ROOT.exists();proofs=[derive('dk4tool/patch/lil_B212_editorial_v1.py','dk4tool/patch/lil_B212_editorial_v2.py',{'unchanged_words_glyphs_page_count_and_zero_ink_tail':'all_words_glyphs_native_page_count_and_guards_preserved'}),derive('scripts/validate_lil_B212_atomic_v6638.py','scripts/validate_lil_B212_atomic_v6638b.py',{'lil_B212_editorial_v1':'lil_B212_editorial_v2','atomic_v6638':'atomic_v6638b'})];ROOT.mkdir(parents=True);save(ROOT/'source_locked_correction.json',dict(proofs=proofs,proof_schema_only_no_prose_source_target_native_or_ROM_change=True,rejected_attempt_preserved=True,full_goal_complete=False))
