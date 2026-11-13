"""Bound the inventory count replacement so1371 fresh COMMON rows stay intact."""
from pathlib import Path
OLD=Path('scripts/verify_editorial_handoff_v2561.py')
if __name__=='__main__':
 source=OLD.read_text()
 a='"\'/COMMON/MESFILE.DK4\':137":"\'/COMMON/MESFILE.DK4\':115"'
 b='"\'/COMMON/MESFILE.DK4\':137,":"\'/COMMON/MESFILE.DK4\':115,"'
 assert source.count(a)==1
 source=source.replace(a,b).replace('editorial_handoff_verification_v2561','editorial_handoff_verification_v2561b').replace('V2561-audit-of-V2560','V2561b-audit-of-V2560')
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
