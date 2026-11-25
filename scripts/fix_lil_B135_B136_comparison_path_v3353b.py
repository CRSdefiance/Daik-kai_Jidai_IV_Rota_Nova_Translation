"""Preserve failed comparison producer andrepair its duplicated path prefix."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/compare_lil_B135_B136_effective_v3353.py');new=Path('scripts/compare_lil_B135_B136_effective_v3353c.py');assert not new.exists();t=old.read_text(encoding='utf-8');assert t.count('work/analysis/work/analysis/')==1;t=t.replace('work/analysis/work/analysis/','work/analysis/');compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B135_B136_comparison_path_v3353b');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),no_ROM_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes())))
