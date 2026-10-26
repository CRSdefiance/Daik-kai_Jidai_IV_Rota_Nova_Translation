"""Trace original glyph calls and owned pixel writes;do not approve the failing synthetic plane."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B166_menu_trace_v4074')
DIAG=Path('work/analysis/lil_B166_menu_pixels_v4071/width_cases_no_mismatch_approval.json')
if __name__=='__main__':
    assert not ROOT.exists();d=read(DIAG);arm=NdsImage.open(d['source_ROM']).read_file('/__arm9__.bin');text=d['source_owned_painter_diagnostic_adapter']
    old='    call(cpu, 0xD5340, (context, string))'
    new='''    traces=[]
    def glyph(u,pc,z,data):
        point=u.reg_read(UC_ARM_REG_R1);value=u.reg_read(UC_ARM_REG_R2)
        traces.append(dict(char=bytes(u.mem_read(value,2)).hex(),point=list(struct.unpack('<2I',u.mem_read(point,8))),function=u.reg_read(UC_ARM_REG_R3),pixel_writes=[]))
    def write(u,access,address,n,value,data):
        if traces:traces[-1]['pixel_writes'].append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=n,value=value))
    h=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D5778,end=0x020D5778)
    w=cpu.hook_add(UC_HOOK_MEM_WRITE,write,begin=header+20,end=header+20+size-1)
    try:call(cpu,0xD5340,(context,string))
    finally:cpu.hook_del(h);cpu.hook_del(w)'''
    assert text.count(old)==1;text=text.replace(old,new);old="'expected_hex':expected.hex()}";assert text.count(old)==1;text=text.replace(old,"'expected_hex':expected.hex(),'glyph_call_and_pixel_writes':traces}")
    cases=[]
    for width in [54,60]:
        env={**prior.__dict__,'LABEL_WIDTH':width,'struct':struct,'UC_HOOK_CODE':UC_HOOK_CODE,'UC_HOOK_MEM_WRITE':UC_HOOK_MEM_WRITE,'UC_ARM_REG_R1':UC_ARM_REG_R1,'UC_ARM_REG_R2':UC_ARM_REG_R2,'UC_ARM_REG_R3':UC_ARM_REG_R3,'UC_ARM_REG_PC':UC_ARM_REG_PC};exec(compile(text,__file__+'::first-glyph-native-write-trace','exec'),env);pixels,proof=env['paint'](arm,b'Please do',1);proof.pop('expected_hex');cases.append(proof)
    ROOT.mkdir(parents=True);save(ROOT/'first_glyph_call_and_owned_pixel_writes.json',dict(diagnostic=str(DIAG),diagnostic_sha256=sha(DIAG.read_bytes()),cases=cases,source_owned_painter_trace_adapter=text,no_menu_approval_or_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([dict(width=r['logical_width'],match=r['independent_complete_native_pixels_match'],glyphs=[dict(char=t['char'],point=t['point'],function=hex(t['function']),pixel_writes=len(t['pixel_writes']),write_PCs=sorted({hex(w['PC']) for w in t['pixel_writes']})) for t in r['glyph_call_and_pixel_writes']]) for r in cases])
