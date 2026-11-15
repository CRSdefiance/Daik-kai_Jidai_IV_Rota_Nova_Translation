"""Bind successor constants as well as completion body; keep the first draft."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('scripts/complete_lil_B137_v3420.py');b=Path('scripts/complete_lil_B137_v3420b.py');assert not b.exists()
    t=a.read_text(encoding='utf-8');cut=t.index('SUMMARY=');prefix,body=t[:cut],t[cut:]
    for x,y in [('completion_v3413b','completion_v3420'),('release_v3410','release_v3417'),('startup_v3412','startup_v3419'),('editorial_handoff_verification_v3400','editorial_handoff_verification_v3415c')]:assert x in prefix;prefix=prefix.replace(x,y)
    t=prefix+body;compile(t,str(b),'exec');b.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B137_completion_tools_v3420b');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),no_completion_or_ledger_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
