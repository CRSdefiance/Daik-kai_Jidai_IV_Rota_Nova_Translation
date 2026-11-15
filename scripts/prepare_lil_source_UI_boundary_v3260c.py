"""Keep the original2000 UI boundary explicit while mapping stored dialogue."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    old=Path('scripts/map_lil_B122_B127_source_v3260.py');new=Path('scripts/map_lil_B122_B127_source_v3260c.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    t=t.replace('from unicorn.arm_const import UC_ARM_REG_R0','from unicorn import UC_HOOK_CODE\nfrom unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_PC,UC_ARM_REG_LR')
    a=t.index('def empty2000(');z=t.index("if __name__=='__main__':",a)
    t=t[:a]+'''def control2000(arm,command):
    assert command['whole_command_hex']=='0020' and command['native_extent']==2
    stream,owner,result,length=0x02660000,0x02662000,0x02664000,0x02664100
    value=bytes.fromhex(command['whole_command_hex']);cases=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for incidental_UI_return in [0,0xFFFFFFFF]:
            cpu=machine(arm);cpu.mem_write(stream-16,b'\\xa5'*34);cpu.mem_write(stream,value)
            cpu.mem_write(owner-16,b'\\xa5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream,0,0));owned=bytes(cpu.mem_read(owner-16,64));before=bytes(cpu.mem_read(BASE,0x400000));calls=[]
            def boundary(u,pc,size,unused):
                args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]]
                assert args==[0,0,length,stream]
                calls.append(dict(address=pc,args=args,original_caller_return=u.reg_read(UC_ARM_REG_LR),UI_body_unexecuted=True))
                u.reg_write(UC_ARM_REG_R0,incidental_UI_return);u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            h=cpu.hook_add(UC_HOOK_CODE,boundary,begin=BASE+0x54E44,end=BASE+0x54E44)
            cpu.mem_write(result-16,b'\\xa5'*80);cpu.mem_write(result,bytes(24));cpu.mem_write(length-16,b'\\xa5'*36);cpu.mem_write(length,bytes(4))
            try:call(cpu,0x2A510,(result,owner,length,previous))
            finally:cpu.hook_del(h)
            extent=struct.unpack('<I',cpu.mem_read(length,4))[0];decoded=struct.unpack('<6I',cpu.mem_read(result,24))
            assert len(calls)==1 and calls[0]['original_caller_return']==BASE+0x2A218
            assert extent==2 and decoded==(3,0,0,0,0,0) and bytes(cpu.mem_read(BASE,0x400000))==before
            assert bytes(cpu.mem_read(owner-16,64))==owned and bytes(cpu.mem_read(stream,2))==value
            for at in [stream-16,stream+2,result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\\xa5'*16
            cases.append(dict(previous_result=previous,incidental_unexecuted_UI_return=incidental_UI_return,native_extent=extent,native_result=list(decoded),original_UI_boundary_calls=calls,no_source_resident_text_payload=True,ABI_all4MiB_owner_stream_result_length_and_boundary_guards_exact=True,full_UI_body_effects_display_and_input_behavior_not_executed=True))
    return cases

'''+t[z:]
    for a,b in [('lil_B122_B127_source_v3260','lil_B122_B127_source_v3260c'),('empty2000(code,cmd)','control2000(code,cmd)'),('all20_original2000_decoder_cases_have_type3_extent2_without_stored_text=True','all40_original2000_decoder_cases_have_type3_extent2_without_stored_text=True,original2000_calls54E44_with_zero_arguments_and_UI_body_unexecuted=True,original2000_UI_display_input_and_side_effect_contract_still_require_binding=True'),('16source/current label getters/20native2000decoder cases pass. Two2000controls contain no stored text. No editorialcredit.','16source/current label getters/40native2000decoder cases pass withoriginal54E44UIboundary explicit andunexecuted. Two2000controls contain no stored text;UIbinding pending. No editorialcredit.')]:assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B122_2000_diagnostic_v3260b')
    save(root/'source_UI_boundary_successor.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),source_code_contract='Original2A20C-2A224 calls54E44 withr0/r1 zero,then overwritesr0 withresulttype3;the UIreturn isunused. Preserve thetwo-byte command andexplicitlyleave theUIbody unexecuted. Bothsource/current decoder paths receive scoped0/FFFFFFFFboundary returns toconfirm noresult dependency;this isnot aUIbehavior orside-effect proof.',full_current_UI_side_effect_and_display_input_binding_pending=True,failed_producer_and_diagnostic_preserved=True,no_ROM_or_editorial_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
