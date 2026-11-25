"""Forensic FE return/glyph capture only; retain the failing complete-page assertion."""
import dis,struct
from pathlib import Path
from types import FunctionType
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import make_painter
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_FE_diagnostic_v7879')
PLAN=Path('work/analysis/Rafael_B45_layout_v7877/12_automatic_plans_full_native_width_zero_preamble_separate_body.json')
if __name__=='__main__':
    assert not ROOT.exists();plan=read(PLAN);doc=read(plan['manuscript'])
    p=next(r for r in plan['records'] if r['source_selector']==254)
    expected=bytes.fromhex(p['encoded_hex'])[1:].replace(b'FO',b'Castor Co.')
    paint,calibration=make_painter(NdsImage.open(doc['current_ROM']));original_call=paint.__globals__['call'];observed=[]
    def capture_call(cpu,entry,args,**kw):
        events=[]
        def glyph(u,pc,size,unused):
            code,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
            events.append(dict(code=code,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
        hook=cpu.hook_add(UC_HOOK_CODE,glyph,begin=0x020D16B4,end=0x020D16B4)
        try:result=original_call(cpu,entry,args,**kw)
        finally:cpu.hook_del(hook)
        observed.append(dict(entry=entry,args=args,return_r0=cpu.reg_read(UC_ARM_REG_R0),events=events))
        return result
    probe=FunctionType(paint.__code__,{**paint.__globals__,'call':capture_call},argdefs=paint.__defaults__,closure=paint.__closure__)
    failure=None
    try:probe(expected)
    except (AssertionError,ValueError) as error:
        frames=[];tb=error.__traceback__
        while tb:
            frame=tb.tb_frame
            instructions=list(dis.get_instructions(frame.f_code))
            nearby=[dict(offset=i.offset,op=i.opname,arg=i.argrepr) for i in instructions if abs(i.offset-tb.tb_lasti)<48]
            frames.append(dict(file=frame.f_code.co_filename,line=tb.tb_lineno,last_instruction=tb.tb_lasti,nearby=nearby))
            tb=tb.tb_next
        failure=dict(type=type(error).__name__,message=str(error),frames=frames)
    ROOT.mkdir(parents=True);save(ROOT/'FE_native_return_andcomplete_glyph_forensic_failure.json',dict(
        candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),
        compiled_hex=p['encoded_hex'],expanded_hex=expected.hex(),lines=p['lines'],native_calls=observed,failure=failure,
        forensic_only_no_suppressed_assertion_orformatting_approval=True,new_credit=0,full_goal_complete=False))
    print('failure',None if failure is None else [(r['line'],r['nearby']) for r in failure['frames'][-1:]])
    for r in observed:print('return offset',r['return_r0']-r['args'][1],'expected',len(expected),'visible',len([e for e in r['events'] if e['code']!=32]),'rows',sorted({e['y'] for e in r['events']}),'last',r['events'][-5:])
