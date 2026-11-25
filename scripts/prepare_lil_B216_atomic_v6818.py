"""Prepare the positive successor without changing the executed predecessor."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/validate_lil_B215_atomic_v6772.py','scripts/validate_lil_B216_atomic_v6818.py',{
        'B215':'B216','v6772':'v6818','v6771':'v6816',
        "==15":"==11",'positive_records=15':'positive_records=11',
        'source924_bytes_inverse_recovered':'source580_bytes_inverse_recovered',
        'positive:15 records':'positive:11 records','complete924-byte':'complete580-byte'}))
