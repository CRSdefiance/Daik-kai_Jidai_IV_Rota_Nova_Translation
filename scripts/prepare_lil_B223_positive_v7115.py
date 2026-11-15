"""Bind the sealed B223 closure to a one-write reconstruction check."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B223_positive_tools_v7115')
if __name__=='__main__':
    assert not ROOT.exists()
    a='scripts/validate_lil_B214_atomic_v6730.py';b='scripts/validate_lil_B223_atomic_v7115.py'
    c={'B214':'B223','references_v6728':'references_v7111','atomic_v6730':'atomic_v7115','atomic_tools_v6729':'atomic_tools_v7114','prepare_lil_B214_atomic_v6729':'prepare_lil_B223_atomic_v7114'}
    assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);row=derive(a,b,c)
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_positive.json',dict(tool=row,immutable_dependencies_exclude_mutable_registry_builder_ledger_and_docs=True,exact_parent_and_reference_hashes_bound=True,new_credit=0,full_goal_complete=False))
