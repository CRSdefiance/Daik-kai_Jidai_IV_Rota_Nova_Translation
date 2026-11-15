"""Repair conditional spacing before the first historical-verifier execution."""
from pathlib import Path
OLD=Path('scripts/rebind_aftermath_defeat_history_v2551.py')
if __name__=='__main__':
 source=OLD.read_text();assert source.count('else0x02117F00')==1
 source=source.replace('else0x02117F00','else 0x02117F00').replace('aftermath_defeat_history_v2551','aftermath_defeat_history_v2551b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
