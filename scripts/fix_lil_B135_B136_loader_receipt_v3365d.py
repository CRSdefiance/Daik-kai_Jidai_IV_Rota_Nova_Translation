"""Bind the loader tothis batch's finalized research receipt."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/verify_lil_B135_B136_loader_v3365b.py');new=Path('scripts/verify_lil_B135_B136_loader_v3365c.py');assert not new.exists();t=old.read_text(encoding='utf-8');a='work/analysis/lil_B131_B133_research_v3330b/research_image_receipt.json';assert a in t;t=t.replace(a,'work/analysis/lil_B135_B136_research_v3364b/research_image_receipt.json');compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B135_B136_loader_receipt_v3365d');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),finding='Prior generator retained B131/B133 research receipt;bind exact current B135/B136 receipt. No loader/runtime check changed.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
