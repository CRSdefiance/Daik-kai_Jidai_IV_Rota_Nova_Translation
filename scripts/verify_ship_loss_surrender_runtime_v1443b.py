"""Prove the disjoint780-bias successor through every original selector/ABI case."""
from pathlib import Path

if __name__=='__main__':
    source = Path('scripts/verify_ship_loss_surrender_runtime_v1443.py').read_text(encoding='utf-8')
    for old,new in [
        ('ship_loss_surrender_runtime_v1442 as runtime','ship_loss_surrender_runtime_v1442b as runtime'),
        ("'work/analysis/ship_loss_surrender_runtime_v1443'","'work/analysis/ship_loss_surrender_runtime_v1443b'")]:
        assert source.count(old)==1
        source = source.replace(old,new)
    exec(compile(source,__file__,'exec'),{**globals(),'__name__':'__main__'})
