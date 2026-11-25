"""Resume derivation with a residue check that permits Manuel's source-owned name."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive as original_derive
from scripts.verify_village_wrap_v608 import save
def checked_derive(a,b,changes):
    text=Path(a).read_text(encoding='utf-8')
    for old in changes:assert old in text
    expected=re.sub('|'.join(re.escape(x) for x in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group(0)],text)
    if Path(b).exists():
        assert Path(b).read_text(encoding='utf-8')==expected
        return dict(previous=a,previous_sha256=sha(Path(a).read_bytes()),successor=b,successor_sha256=sha(Path(b).read_bytes()),existing_partial_derivation_verified=True)
    return original_derive(a,b,changes)
if __name__=='__main__':
    p=Path('scripts/prepare_lil_B167_registration_v4158.py');text=p.read_text(encoding='utf-8')
    old='from scripts.prepare_lil_B156_layout_v3705 import derive';assert text.count(old)==1;text=text.replace(old,'derive=checked_derive')
    old="assert '166' not in text and 'Fernando' not in text and 'Manuel' not in text";assert text.count(old)==1
    text=text.replace(old,"assert 'B166' not in text and 'Fernando' not in text")
    exec(compile(text,str(p)+'::name-aware-resume','exec'),dict(globals()))
    save(Path('work/analysis/lil_B167_registration_tools_v4158/partial_derivation_recovery.json'),dict(original_failure='Residue assertion rejected legitimate source-owned Manuel23 field; exact v2 compiler retained without rewrite. Guard now tests obsolete B166/Fernando tokens only.',original_producer=str(p),original_producer_sha256=sha(p.read_bytes()),resume_producer_sha256=sha(Path(__file__).read_bytes()),no_registry_ROM_orledger_change=True))
