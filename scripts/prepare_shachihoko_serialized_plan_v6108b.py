"""Compare regenerated cache-address maps in their exact persisted JSON representation."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('dk4tool/patch/shachihoko_item116_editorial_v1.py','dk4tool/patch/shachihoko_item116_editorial_v2.py',{
        "require(plan==doc['native_data_plan']==seal['data_plan']":"require(json.loads(json.dumps(plan))==doc['native_data_plan']==seal['data_plan']",
    }))
    print(derive('scripts/validate_shachihoko_item116_v6108.py','scripts/validate_shachihoko_item116_v6108b.py',{
        'shachihoko_item116_editorial_v1 as owned':'shachihoko_item116_editorial_v2 as owned',
        "ROOT=Path('work/analysis/shachihoko_atomic_v6108')":"ROOT=Path('work/analysis/shachihoko_atomic_v6108b')",
    }))
