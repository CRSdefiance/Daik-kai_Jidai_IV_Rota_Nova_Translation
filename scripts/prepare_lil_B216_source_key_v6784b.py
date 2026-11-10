"""Preserve rejected preflight and keep its source-code backslashes literal."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B216_source_key_v6784b')
if __name__=='__main__':
    assert not ROOT.exists();a='scripts/prepare_lil_B216_source_v6784.py';b='scripts/prepare_lil_B216_source_v6784b.py';key=chr(34)+'source[922:]==target[922:]==b';c={key:'r'+key,'source_tools_v6784':'source_tools_v6784b'};assert not Path(b).exists();checked_text(Path(a).read_text('utf8'),c);proof=derive(a,b,c);ROOT.mkdir(parents=True);save(ROOT/'source_locked_literal_key_fix.json',dict(derivation=proof,no_partial_binding_or_map_outputs_created_by_failed_preflight=True,full_goal_complete=False))
