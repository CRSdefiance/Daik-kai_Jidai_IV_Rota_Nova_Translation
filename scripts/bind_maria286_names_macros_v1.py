"""Bind scoped native names and default substitutions on the registered Maria runtime."""
import inspect
import struct
from pathlib import Path
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B169_contextual_v1 import fields, getter
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.execute_map_entity_tooltip_copy import STACK, STOP

ROOT = Path('work/Maria_B37_B50_clean_20261109')

def main():
    out = ROOT/'scoped_names_macros_reference_v1.json'
    assert not out.exists()
    drafts_path = ROOT/'all286_clean_meanings_andindependent_drafts_v2.json'
    current_path = ROOT/'current_v1/current_effective.json'
    drafts,current = map(load,[drafts_path,current_path])
    ctx = RegisteredRuntime(current['runtime']['release_proof'],current['runtime']['startup_proof'],captain=3)
    assert ctx.receipt()==current['runtime']
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    actors={r['source_selector'] for r in drafts['records'] if r.get('source_selector',254)<207}
    spoken=[]
    base=struct.unpack_from('<I',clean,0xCDAC0)[0]-BASE
    expected={'ハイレディン','バルデス','パシャ','クーン','エスカンテ'}
    for actor in range(207):
        values=[string(clean,p)['text'] if p else '' for p in struct.unpack_from('<3I',clean,base+32*actor)]
        if expected.intersection(values):
            actors.add(actor);spoken.append(dict(actor_ID=actor,source_components=values))
    assert len(spoken)==5 and expected=={v for r in spoken for v in r['source_components'] if v in expected}
    actors=sorted(actors)
    code=checked_text(inspect.getsource(getter),{'for ident in [2,4,13,23,109]:':'for ident in ACTORS:'})
    env={**getter.__globals__,'ACTORS':actors}
    exec(compile(code,__file__+'::same-original-name-getters-scoped-Maria286','exec'),env)
    names=ctx.execute(env['names'])
    assert len(names['rows'])==2*len(actors)
    bindings=[]
    for actor in actors:
        consumers=[r for r in names['rows'] if r['actor_ID']==actor]
        assert {r['consumer'] for r in consumers}=={'progressive-nameplate','full-catalogue'}
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=fields(actor,clean,ctx),
            current_consumers=consumers,context_record_ids=[r['id'] for r in drafts['records'] if r.get('source_selector')==actor],
            spoken_reference_only=not any(r.get('source_selector')==actor for r in drafts['records']),
            name_localization_andfresh_display_approval_pending=True))
    cpu,get,_=ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
    assert get(0x7F244)==3
    macros=[];ip,op=0x02430020,0x02431020
    for token in ['FI','FA','FO','FU']:
        cpu.mem_write(ip-32,b'\xa5'*640);cpu.mem_write(ip,token.encode()+b'\0')
        before=bytes(cpu.mem_read(ip-32,640));cpu.mem_write(op-32,b'\xa5'*1088)
        for reg,value in [(UC_ARM_REG_R0,op),(UC_ARM_REG_R1,ip),(UC_ARM_REG_R2,0),(UC_ARM_REG_SP,STACK),(UC_ARM_REG_LR,STOP)]:cpu.reg_write(reg,value)
        cpu.emu_start(0x02053914,STOP,count=1000000)
        assert cpu.reg_read(UC_ARM_REG_PC)==STOP and cpu.reg_read(UC_ARM_REG_SP)==STACK and cpu.reg_read(UC_ARM_REG_R0)==0
        raw=bytes(cpu.mem_read(op,1024)).split(b'\0')[0];assert raw and len(raw)<1024
        assert bytes(cpu.mem_read(ip-32,640))==before
        assert bytes(cpu.mem_read(op-32,1088))==b'\xa5'*32+raw+b'\0'+b'\xa5'*(1055-len(raw))
        macros.append(dict(token=token,text=raw.decode('cp932'),hex=raw.hex(),bytes=len(raw),
            original_expander_no_getter_bridges=True,complete_output_NUL_input_andstack_guards_pass=True,
            scope='one aligned default-name call on captain3; not arbitrary custom names or complete formatting approval'))
    assert bytes(cpu.mem_read(ctx.actor_root,0x1A04))==ctx.actor_bytes
    ctx.calls.clear()
    save(out,dict(runtime=ctx.receipt(),scoped_actors=len(actors),original_native_name_getters=2*len(actors),
        records=bindings,spoken_reference_components=spoken,default_macro_cases=macros,
        names_andterms_reference_only_not_editorial_orfont_approval=True,no_global207_name_approval=True,
        FE_unseen_voice_andhidden_monologue_not_assigned_static_actor=True,new_credit=0,
        evidence={str(p):digest(p) for p in [drafts_path,current_path,Path(__file__)]}))
    for r in bindings:
        print(r['actor_ID'],[(x['consumer'],x['text']) for x in r['current_consumers']])
    print('MACROS',[(r['token'],r['text']) for r in macros])
    print('Bound',len(actors),'scoped actors/',2*len(actors),'native getters;zero credit.')

if __name__=='__main__':main()
