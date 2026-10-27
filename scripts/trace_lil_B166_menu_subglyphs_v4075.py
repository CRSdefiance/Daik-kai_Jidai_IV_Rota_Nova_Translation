"""Trace actual single-ASCII coordinates and bitplane writes inside the original paired callback."""
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_SP,UC_ARM_REG_R0
if __name__=='__main__':
    draft=Path('scripts/trace_lil_B166_menu_first_glyph_v4074.py');t=draft.read_text(encoding='utf-8')
    replacements={
        "lil_B166_menu_trace_v4074":"lil_B166_menu_trace_v4075",
        "    h=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D5778,end=0x020D5778)":"""    def subglyph(u,pc,z,data):
        sp=u.reg_read(UC_ARM_REG_SP)
        traces.append(dict(single_char=u.mem_read(sp,1)[0],x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3),bitmap=u.reg_read(UC_ARM_REG_R1),pixel_writes=[]))
    h=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D5778,end=0x020D5778)
    sh=cpu.hook_add(UC_HOOK_CODE,subglyph,begin=0x020D16B4,end=0x020D16B4)""",
        "cpu.hook_del(h);cpu.hook_del(w)":"cpu.hook_del(h);cpu.hook_del(sh);cpu.hook_del(w)",
        "'UC_ARM_REG_PC':UC_ARM_REG_PC}":"'UC_ARM_REG_PC':UC_ARM_REG_PC,'UC_ARM_REG_SP':UC_ARM_REG_SP}",
        "    print([dict(width=r['logical_width']":"    print([dict(width=r['logical_width']"
    }
    for a,b in replacements.items():assert a in t,a;t=t.replace(a,b)
    start=t.index('    print([dict(width=');t=t[:start]+"    print([dict(width=r['logical_width'],subglyphs=[dict(char=chr(c['single_char']),x=c['x'],y=c['y'],bitmap=hex(c['bitmap']),writes=len(c['pixel_writes'])) for c in r['glyph_call_and_pixel_writes'] if 'single_char' in c]) for r in cases])\n"
    t=t.replace("save(ROOT/'first_glyph_call_and_owned_pixel_writes.json',dict(","save(ROOT/'first_glyph_call_and_owned_pixel_writes.json',dict(frozen_predecessor=str(DRAFT),frozen_predecessor_sha256=sha(DRAFT.read_bytes()),")
    exec(compile(t,__file__,'exec'),dict(__name__='__main__',__file__=__file__,DRAFT=draft,UC_ARM_REG_SP=UC_ARM_REG_SP,UC_ARM_REG_R0=UC_ARM_REG_R0))
