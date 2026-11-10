"""Preserve rejected preflight; remove guessed keys and keep the previous-stage order check exact."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B215_release_key_fix_v6775b')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/prepare_lil_B215_release_runners_v6775.py';b='scripts/prepare_lil_B215_release_runners_v6775b.py';c={'release_tools_v6775':'release_tools_v6775b',",'607 manifest':'607 manifest','605+17':'606+15'":"", "'startup_v6737':'startup_v6779','V6686':'V6733','V6733':'V6775'":"'startup_v6737':'startup_v6779','V6686':'V6733'"};assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);proof=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_release_preflight_successor.json',dict(derivation=proof,failed_preparer_preserved_no_partial_outputs_created=True,full_goal_complete=False))
