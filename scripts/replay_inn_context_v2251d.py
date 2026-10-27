"""Use the direct facility field; supersede the invalid2251b/c speaker context."""
from pathlib import Path
source=Path('scripts/replay_inn_context_v2251c.py').read_text().replace('inn_context_v2251c','inn_context_v2251d')
old="facility=struct.unpack('<I',u.mem_read(global_pointer,4))[0]+0x10";assert source.count(old)==1
source=source.replace(old,'facility=global_pointer+0x10')
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
