"""Use the actual loaded font resource with a guarded software bitmap."""
from pathlib import Path
if __name__=='__main__':
 source=Path('scripts/probe_primary_town_pixel_anchor_v2101.py').read_text(encoding='utf-8-sig').replace('v2101','v2101c')
 source=source.replace("source=inspect.getsource(original).replace", "raw_font_state=Path(row['snapshots']['WRAM']['path']).read_bytes()\n source=inspect.getsource(original).replace('    u = machine(arm)','    u = machine(arm)\\n    u.mem_write(BASE,raw_font_state)').replace")
 source=source.replace("env={**original.__globals__,'NdsImage':Font}","env={**original.__globals__,'NdsImage':Font,'raw_font_state':raw_font_state}")
 exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
