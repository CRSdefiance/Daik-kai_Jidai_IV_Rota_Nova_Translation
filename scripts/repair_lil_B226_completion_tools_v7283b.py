"""Keep the absent-version preflight failure; filter only unused version keys."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B226_completion_repair_v7283b')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/prepare_lil_B226_completion_v7283.py','scripts/prepare_lil_B226_completion_v7283b.py',{'lil_B226_completion_tools_v7283':'lil_B226_completion_tools_v7283b',"    rows=[derive('scripts/complete_lil_B225_v7236.py'":"    extra={k:v for k,v in extra.items() if not(k.startswith('v') and k[1:].isdigit() and k not in src)}\n    rows=[derive('scripts/complete_lil_B225_v7236.py'"})
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_unused_version_key_filter.json',r)
