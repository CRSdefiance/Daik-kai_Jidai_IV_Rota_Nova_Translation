"""Prepare single-write validation and18 actual-changing corruption cases including the short opening."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
if __name__=='__main__':
    jobs=[('scripts/validate_lil_B217_atomic_v6862.py','scripts/validate_lil_B218_atomic_v6907.py',{'B217':'B218','v6862':'v6907','v6860':'v6905',"len(proof['changed_records'])==4":"len(proof['changed_records'])==13",'positive_records=4':'positive_records=13','source304_bytes_inverse_recovered':'source1088_bytes_inverse_recovered','positive:4 records':'positive:13 records','complete304-byte':'complete1088-byte'}),
    ('scripts/challenge_lil_B217_atomic_v6863b.py','scripts/challenge_lil_B218_atomic_v6908.py',{'B217':'B218','v6863b':'v6908','v6862':'v6907',"source_hex='00a0ffff2e000110'":"source_hex='00a0ffff2f000110'","source_hex='00a0ffff2e000110'))]":"source_hex='00a0ffff2f000110')),\n        ('omitted-short-question-opening-reason','doc',lambda d:next(r for r in d['records'] if r['source_record_index']==8).update(reviewed_short_complete_sentence_openings=[]))]",'len(cases)==17':'len(cases)==18','negative_count=17':'negative_count=18','17 distinct B217 corruptions':'18 distinct B218 corruptions'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    for a,b,c in jobs:print(derive(a,b,c))
