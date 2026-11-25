"""Preserve2638 refusal;terminal snapshot's frame is the audited terminal frame."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/rebind_sighting_history_v2638.py').read_text();old="shots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']";new="shots={r.get('frame',returned):r for r in report['read_only_capture_RAM_snapshots']";assert source.count(old)==1;source=source.replace(old,new).replace('sighting_history_v2638','sighting_history_v2638b')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
