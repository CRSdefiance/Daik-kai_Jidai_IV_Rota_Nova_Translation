"""Use the source's direct global object, not a second pointer dereference."""
from pathlib import Path
source=Path('scripts/replay_palace_context_v2250c.py').read_text().replace('palace_context_v2250c','palace_context_v2250d')
old="facility=struct.unpack('<I',cpu.mem_read(global_pointer,4))[0]+0x10";assert source.count(old)==1
source=source.replace(old,'facility=global_pointer+0x10')
exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
