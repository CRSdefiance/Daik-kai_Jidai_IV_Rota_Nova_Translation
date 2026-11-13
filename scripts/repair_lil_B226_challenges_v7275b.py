"""Preserve the dictionary-pop harness failure; repair only the test operation."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_challenge_repair_v7275b')
if __name__=='__main__':
    assert not ROOT.exists()
    rows=[derive('scripts/challenge_lil_B226_atomic_v7275.py','scripts/challenge_lil_B226_atomic_v7275b.py',{'lil_B226_atomic_v7275':'lil_B226_atomic_v7275b',"v['row_count_reasons'].pop()":"v['row_count_reasons'].pop(next(iter(v['row_count_reasons'])))"}),derive('scripts/register_lil_B226_v7276.py','scripts/register_lil_B226_v7276b.py',{'lil_B226_atomic_v7275':'lil_B226_atomic_v7275b'})]
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_harness_repair.json',dict(derivations=rows,original_failure='row_count_reasons is a dict; zero-argument pop is invalid',production_module_unchanged=True,failed_partial_producer_and_all_before_mutation_results_preserved=True))
