"""Bind older pause-only RAM exports;do not require an absent legacy final export."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/rebind_lil_cliff_history_v2652.py').read_text().replace("and journal['completion_confirmed']","and journal['commands_are_not_execution_receipts']").replace("report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]","report['read_only_pause_RAM_snapshots']+([report['read_only_RAM_snapshot']]if report.get('read_only_RAM_snapshot')else[])").replace('lil_cliff_history_v2652','lil_cliff_history_v2652c');exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
