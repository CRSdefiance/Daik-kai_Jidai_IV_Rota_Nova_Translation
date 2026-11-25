"""Preserve the premature verifier and require both terminal receipts first."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('scripts/verify_lil_B139_B140_startup_v3490.py');b=Path('scripts/verify_lil_B139_B140_startup_v3490b.py');assert not b.exists();t=a.read_text(encoding='utf-8');needle="if __name__=='__main__':\n";assert t.count(needle)==1;t=t.replace(needle,needle+"    assert all((RUN/(case+'_terminal.json')).exists() and read(RUN/(case+'_terminal.json'))['terminal'] for case in ['newgame','town']),'Both actual capture jobs must be terminal before comparison'\n");compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B139_B140_startup_tools_v3490b');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),failure='The first verifier started before town_terminal.json existed. It made no verification output,ROM or capture change. The successor requires both jobs terminal first.',producer_sha256=sha(Path(__file__).read_bytes()),all_actual_captures_and_prior_producers_preserved=True,full_goal_complete=False))
