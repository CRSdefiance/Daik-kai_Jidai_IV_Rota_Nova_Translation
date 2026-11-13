"""Successor fixes a lexical typo before the first probe could execute."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/replay_work_context_v2307.py')
if __name__=='__main__':
 source=OLD.read_text().replace("work_context_v2307'","work_context_v2307b'");assert source.count('else1398')==1;source=source.replace('else1398','else 1398');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
 save('work/analysis/work_context_v2307b/successor_provenance.json',dict(failed_producer=str(OLD),failed_producer_sha256=sha(OLD.read_bytes()),failure='A missing space in else1398 caused a syntax rejection before execution or outputs.',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
