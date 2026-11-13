"""Connect the current owned108-row constructor, stored selector, copy and native painter."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R8,UC_ARM_REG_SP,UC_ARM_REG_PC,UC_ARM_REG_LR
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_layout_v2 import INIT_START,INIT_END
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.execute_map_entity_tooltip_copy import BASE,STACK,ACTOR
from scripts.prepare_refit_layout_v712 import PIXELS

ROOT=Path('work/analysis/Shared_Deck_connected_current_20261104')
NATIVE=Path('work/analysis/Shared_Deck_current_native_v5_20261104/native_andstorage_verification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    proof=load(NATIVE);ctx=RegisteredRuntime(proof['runtime']['release_proof'],proof['runtime']['startup_proof'],captain=0)
    assert ctx.receipt()==proof['runtime'];review=load(proof['review']);rows={r['id']:r for r in review['records']}
    target=Path(proof['proposed_ARM9']).read_bytes();assert sha(target)==proof['proposed_ARM9_sha256']
    cases=[]
    for plan in proof['plans']:
        row=rows[plan['id']];room=row['source_reference']['room'];raw=bytes.fromhex(plan['compiled_hex'])
        for state in (0,255):
            cpu,_,_=machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
            for p in proof['plans']:
                at=p['current_offset'];cpu.mem_write(BASE+at,target[at:at+p['allocation']])
            cpu.mem_write(ACTOR+0x10,ctx.arm[0xD3C00:0xD3C04])
            events=[];executed=set();allocations=[]
            def code(u,pc,size,_):
                owners=[s for s in ctx.sections if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
                assert len(owners)==1,hex(pc)
                s=owners[0];assert bytes(u.mem_read(pc,size))==bytes(s.data[pc-s.ramAddress:pc-s.ramAddress+size]),hex(pc)
                executed.add(pc)
                if pc==0x02005154:
                    assert u.reg_read(UC_ARM_REG_R0)==9072;allocations.append(9072)
                    u.reg_write(UC_ARM_REG_R0,PIXELS);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
                elif pc==BASE+0xD16B4:
                    glyph,style=struct.unpack('<2I',u.mem_read(u.reg_read(UC_ARM_REG_SP),8))
                    events.append(dict(kind='ascii',code=glyph,style=style,x=u.reg_read(UC_ARM_REG_R2),y=u.reg_read(UC_ARM_REG_R3)))
            cpu.hook_add(UC_HOOK_CODE,code)
            cpu.reg_write(UC_ARM_REG_SP,STACK);cpu.reg_write(UC_ARM_REG_R4,1);cpu.reg_write(UC_ARM_REG_R5,ACTOR)
            cpu.emu_start(BASE+INIT_START,BASE+INIT_END,count=100000)
            assert allocations==[9072] and cpu.reg_read(UC_ARM_REG_PC)==BASE+INIT_END and cpu.reg_read(UC_ARM_REG_SP)==STACK
            header=ACTOR+0x1C38
            assert struct.unpack('<3I',cpu.mem_read(header,12))==(4,42,108)
            assert struct.unpack('<2I',cpu.mem_read(ACTOR+0x38,8))==(168,108)
            assert (header+struct.unpack('<I',cpu.mem_read(header+16,4))[0])&0xffffffff==PIXELS
            cpu.mem_write(PIXELS-16,b'\xa5'*16+b'\x99'*9072+b'\xa5'*16);cpu.mem_write(STACK,b'\xa5'*0x500)
            cpu.reg_write(UC_ARM_REG_R6,room);cpu.reg_write(UC_ARM_REG_R5,state);cpu.reg_write(UC_ARM_REG_R8,ACTOR)
            before=bytes(cpu.mem_read(BASE,len(ctx.raw)))
            cpu.emu_start(BASE+0x19E70,BASE+0x19EB4,count=1000000)
            assert cpu.reg_read(UC_ARM_REG_PC)==BASE+0x19EB4 and cpu.reg_read(UC_ARM_REG_SP)==STACK
            assert bytes(cpu.mem_read(BASE,len(ctx.raw)))==before
            assert bytes(cpu.mem_read(STACK+0x10,1024))==raw+b'\xa5'*(1024-len(raw))
            assert bytes(cpu.mem_read(PIXELS-16,16))==bytes(cpu.mem_read(PIXELS+9072,16))==b'\xa5'*16
            actual=bytes(cpu.mem_read(PIXELS,9072));shifted=[{**e,'y':e['y']+1} for e in events]
            canvas=expected_pixels(ctx.arm,b'',shifted,4,background=9)
            expected=b''.join(canvas[y*128:y*128+84] for y in range(108));assert actual==expected
            content=[e for e in events if e['code']!=32]
            assert [e['code'] for e in content]==[ord(c) for c in plan['logical_English'] if c!=' ']
            assert all(0<=e['x'] and e['x']+6<=168 and 0<=e['y'] and e['y']+12<=60 for e in content)
            assert {BASE+n for n in [0x16868,0x53914,0xD5160,0xD5404,0xD16B4]}<=executed
            cases.append(dict(id=plan['id'],room=room,state=state,stored_text_hex=raw.hex(),complete_native_pixels_sha256=sha(actual),
                constructor_selector_macrocopy_context_andcurrent_glyphs_connected=True,complete_words_leading_internal_final_glyphs_bounds_andblank_plane_exact=True,
                all_main4MiB_ABI_andpixel_text_guards_exact=True,executed_current_source_addresses=sorted(executed)))
    ROOT.mkdir();save(ROOT/'connected_verification.json',dict(runtime=ctx.receipt(),native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),
        proposed_ARM9=proof['proposed_ARM9'],proposed_ARM9_sha256=sha(target),cases=cases,
        all8_complete_current_native_constructor_selector_copy_raster_andfont_cases_pass=True,
        supplied9072_byte_allocator_result_is_explicit_fixture_not_actual_heap_orGPU_proof=True,
        native_original_bitmap_vtable_andpalette_and168x108_dimensions_andall_current_instructions_verified=True,
        no_historical_RAM_overlay=True,actual_gameplay=False,representative_Refit_UI_andregistered_deployment_pending=True,
        no_ROM_created=True,new_credit=0,guide_photos=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Eight complete current108-row constructor->stored selector->copy->font cases pass;4MiB/ABI/canaries exact;actual UI pending.')
