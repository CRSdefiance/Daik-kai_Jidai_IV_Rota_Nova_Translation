"""Keep prepared verifier immutable; correct only its current-build sheet caption before execution."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B215_startup_label_tools_v6779b')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/verify_lil_B215_startup_v6779.py';b='scripts/verify_lil_B215_startup_v6779b.py';c={'Current6733':'Current6775'};assert not Path(b).exists() and not Path('work/analysis/lil_B215_startup_v6779').exists();checked_text(Path(a).read_text('utf8'),c);proof=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_current_caption.json',dict(derivation=proof,comparison_still_exact_prior_V6733=True,no_native_guard_or_capture_change=True,full_goal_complete=False))
