"""Measure current FE pair preflight and compiler-owned break guards; no scene/format approval."""
import struct
from pathlib import Path
from types import FunctionType
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import make_painter
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_FE_boundary_v7880')
if __name__=='__main__':
    assert not ROOT.exists();names=read('work/analysis/Rafael_B45_names_v7869/two_static_speakers_four_getters_clean_fields_eight_macro_alignments.json')
    image=NdsImage.open(names['candidate']);paint,calibration=make_painter(image);original=paint.__globals__['call'];calls=[]
    def measured_call(cpu,entry,args,**kw):
        events=[]
        def observe(u,pc,size,unused):
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
            events.append(dict(code=code,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
        hook=cpu.hook_add(UC_HOOK_CODE,observe,begin=0x020D16B4,end=0x020D16B4)
        try:result=original(cpu,entry,args,**kw)
        finally:cpu.hook_del(hook)
        calls.append(dict(returned_bytes=cpu.reg_read(UC_ARM_REG_R0)-args[1],events=events))
        return result
    measured=FunctionType(paint.__code__,{**paint.__globals__,'call':measured_call},argdefs=paint.__defaults__,closure=paint.__closure__)
    rows=[]
    for count in range(32,40):
        for kind,suffix in [('final',b''),('bare-LF',b'\nNext.'),('guarded-LF',b'\n Next.'),('phase-space-guarded-LF',b' \n Next.')]:
            text=b'A'*count+suffix;failure=None
            try:measured(text)
            except AssertionError as error:failure=type(error).__name__
            call=calls[-1];events=call['events'];ys=sorted({e['y'] for e in events})
            rows.append(dict(ascii_count=count,kind=kind,text_hex=text.hex(),full_original_painter_guards_pass=failure is None,
                guard_failure=failure,**call,rendered_rows=[dict(y=y,text=''.join(chr(e['code']) for e in events if e['y']==y)) for y in ys]))
    assert len(rows)==32
    ROOT.mkdir(parents=True);save(ROOT/'32_FE_terminal_andbreak_pair_boundary_measurements.json',dict(
        candidate=names['candidate'],candidate_sha256=names['candidate_sha256'],ARM9_sha256=sha(image.read_file('/__arm9__.bin')),
        cases=rows,physical_bitmap_width228_not_same_as_safe_formatted_text_width=True,
        all_original_painter_failures_preserved_not_relabelled_approved=True,
        synthetic_boundary_strings_not_added_to_ROM_orprose=True,no_actual_B45_ornew_review_credit=True,
        historical_geometry_calibration=calibration,new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    for r in rows:print(r['ascii_count'],r['kind'],r['full_original_painter_guards_pass'],r['returned_bytes'],[(v['y'],v['text']) for v in r['rendered_rows']])
