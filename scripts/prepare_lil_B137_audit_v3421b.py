"""Correct the exact carried inventory key before running the final audit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('scripts/verify_editorial_handoff_v3421.py');b=Path('scripts/verify_editorial_handoff_v3421b.py');assert not b.exists()
    t=a.read_text(encoding='utf-8');old="'next_clean_only_uncredited_exchange_inventory_v3258','lil_B137_registered_hook_repair_v3415'";new="'next_clean_only_uncredited_exchange_inventory_v3258','B137_registered_hook_repair_v3415'"
    assert old in t;t=t.replace(old,new);compile(t,str(b),'exec');b.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B137_audit_tools_v3421b');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ledger_or_ROM_mutation=True,full_goal_complete=False))
