"""Restore the literal opening-block field after numeric template replacement."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/verify_editorial_handoff_v3377b.py');new=Path('scripts/verify_editorial_handoff_v3377c.py');assert not new.exists();t=old.read_text(encoding='utf-8');a='current_Lil_captain2_and_B21_payload_verified';assert t.count(a)==1;t=t.replace(a,'current_Lil_captain2_and_B22_payload_verified');compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B135_B136_audit_B22_v3377d');root.mkdir(parents=True);save(root/'provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),finding='Numeric21-consumer replacement incorrectly renamed the literal B22 opening field. Restore the exact proven field;no evidence orcheck is waived.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
