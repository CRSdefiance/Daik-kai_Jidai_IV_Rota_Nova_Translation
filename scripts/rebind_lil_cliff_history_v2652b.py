"""Use terminal report/RAM/photos for execution;the journal records requests only."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/rebind_lil_cliff_history_v2652.py').read_text();old="and journal['completion_confirmed']";assert source.count(old)==1;source=source.replace(old,"and journal['commands_are_not_execution_receipts']").replace('lil_cliff_history_v2652','lil_cliff_history_v2652b');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
