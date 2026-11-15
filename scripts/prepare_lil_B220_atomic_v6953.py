"""Preflight a single archive write and21 actual-changing corruption cases including C200."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B220_atomic_tools_v6953');assert not root.exists()
    oldcase="        ('omitted-short-question-opening-reason','doc',lambda d:next(r for r in d['records'] if r['source_record_index']==8).update(reviewed_short_complete_sentence_openings=[]))]"
    newcase="        ('omitted-fuller-R35-boundary-reason','doc',lambda d:next(r for r in d['records'] if r['source_record_index']==35).update(reviewed_ordinary_boundaries=[])),\n        ('missing-C200-map','map',lambda m:m['blocks'][0]['original_C200_map'].clear()),\n        ('changed-C200-source','map',lambda m:m['blocks'][0]['original_C200_map'][0].update(source_hex='00c3')),\n        ('wrong-C200-target','map',lambda m:m['blocks'][0]['original_C200_map'][0].update(target_offset=1272))]"
    jobs=[('scripts/validate_lil_B218_atomic_v6907.py','scripts/validate_lil_B220_atomic_v6953.py',{'B218':'B220','v6907':'v6953','v6905':'v6951',"len(proof['changed_records'])==13":"len(proof['changed_records'])==17",'positive_records=13':'positive_records=17','source1088_bytes_inverse_recovered':'source1280_bytes_inverse_recovered','positive:13 records':'positive:17 records','complete1088-byte':'complete1280-byte'}),
    ('scripts/challenge_lil_B218_atomic_v6908.py','scripts/challenge_lil_B220_atomic_v6954.py',{'B218':'B220','v6908':'v6954','v6907':'v6953',"source_hex='00a0ffff2f000110'":"source_hex='00a0ffff44000110'",oldcase:newcase,'len(cases)==18':'len(cases)==21','negative_count=18':'negative_count=21','18 distinct B218 corruptions':'21 distinct B220 corruptions'})]
    for a,b,c in jobs:assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c)
    root.mkdir(parents=True);save(root/'source_locked_derivations.json',[derive(a,b,c) for a,b,c in jobs])
