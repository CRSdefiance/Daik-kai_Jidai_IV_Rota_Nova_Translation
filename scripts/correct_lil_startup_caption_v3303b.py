"""Keep generated3303; correct only displayed current-version captions."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/verify_lil_B122_B127_startup_v3303.py');new=Path('scripts/verify_lil_B122_B127_startup_v3303b.py');assert not new.exists()
    text=old.read_text(encoding='utf-8');assert text.count('Current3251')==2;text=text.replace('Current3251','Current3300')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf-8')
    root=Path('work/analysis/lil_B122_B127_release_tools_v3300');save(root/'startup_caption_successor.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),change='Only current-version caption/print labels corrected to3300. Comparison ROM and prior actual capture controls remain3251.',producer_sha256=sha(Path(__file__).read_bytes())))
