"""Bind original predicate globals as well as its exact source-result constants."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_predicate_globals_repair_v3445b');assert not root.exists()
    a=Path('scripts/prove_lil_B138_relocated_controls_v3445.py');b=Path('scripts/prove_lil_B138_relocated_controls_v3445b.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    t=t.replace("ROOT=Path('work/analysis/lil_B138_relocated_controls_v3445')","ROOT=Path('work/analysis/lil_B138_relocated_controls_v3445b')")
    needle="namespace={**prior.__dict__,'SOURCE':";assert t.count(needle)==1;t=t.replace(needle,"namespace={**prior.predicate.__globals__,**prior.__dict__,'SOURCE':")
    marker="    assert 'predicate' in portable;";assert marker in t
    t=t.replace(marker,"    needed={name for name in prior.predicate.__code__.co_names if name in prior.predicate.__globals__};assert needed<=namespace.keys(),needed-namespace.keys()\n"+marker)
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');failed=Path('work/analysis/lil_B138_relocated_controls_v3445');assert failed.exists() and not (failed/'all44_relocated_dispatches10_predicates_and1_query_pairs.json').exists();root.mkdir(parents=True)
    save(root/'failure_and_successor_receipt.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),failed_assertion='Reconstructed source predicate lacked original UC_HOOK_MEM_WRITE import.',failed_partial_directory=str(failed),failed_artifacts_preserved={str(p):sha(p.read_bytes()) for p in failed.rglob('*') if p.is_file()},original_predicate_namespace_and_exact_SCOPED_RESULTS_now_bound=True,no_source_Runtime_ROM_or_review_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
