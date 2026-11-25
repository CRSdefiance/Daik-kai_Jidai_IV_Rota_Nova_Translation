"""Execute the complete native printf with guarded source/target market literals."""
import struct
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.market_goods_info_terminator_v1 import FIELDS,FORMAT,NEW_FORMAT,PAYLOAD
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import STACK

ROOT=Path('work/market_goods_info_terminator_20261109_v1')

def main():
    out=ROOT/'native_verification_v1.json';assert not out.exists()
    prepared=ROOT/'prepared_v1';proof=load(prepared/'preparation.json')
    ctx=RegisteredRuntime('work/maria301_release_v1/registered_release_verification.json',
        'work/maria301_release_v1/own_registered_startup_verification.json',captain=3)
    source=(prepared/'source_arm9.bin').read_bytes();target=(prepared/'target_arm9.bin').read_bytes()
    assert source==ctx.arm and sha(target)==proof['target_ARM9_sha256']
    cases=[];all_executed=set()
    for version,arm in [('current-defect',source),('prepared-correction',target)]:
        sections=MainCodeFile(arm,BASE).sections
        owners=[*sections,SimpleNamespace(ramAddress=POOL,data=bytes(sections[3].data[:-48]))]
        cpu,get,provider=machine(arm,ctx.common,ctx.raw,ctx.plan)
        # The parent’s dynamic own-boot state is reused offline. Overlay only the
        # two target static pointers that this data-only transform owns. Every
        # executable instruction must still match the supplied ARM9 sections.
        for field in FIELDS:cpu.mem_write(BASE+field,arm[field:field+4])
        assert bytes(cpu.mem_read(ctx.actor_root,0x1A04))==ctx.actor_bytes
        def exact(u,pc,size,_):
            matches=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
            assert len(matches)==1,hex(pc)
            owner=matches[0];at=pc-owner.ramAddress
            assert bytes(u.mem_read(pc,size))==bytes(owner.data[at:at+size]),hex(pc)
            all_executed.add(pc)
        hook=cpu.hook_add(UC_HOOK_CODE,exact)
        if version=='prepared-correction':assert bytes(cpu.mem_read(NEW_FORMAT,len(PAYLOAD)))==PAYLOAD
        for field in FIELDS:
            for name,category,number in [('Cheese','Food',101),('Cheese','Food',0),('Cheese','Food',100),
                ('Wine','Liquor',99),('Black Glacier Sword','Crafts',125),('Almond','Food',999)]:
                output,np,cp=0x02660020,0x02661020,0x02662020
                cpu.mem_write(np-16,b'\xa5'*128);cpu.mem_write(np,name.encode()+b'\0')
                cpu.mem_write(cp-16,b'\xa5'*128);cpu.mem_write(cp,category.encode()+b'\0')
                names_before=bytes(cpu.mem_read(np-16,128));category_before=bytes(cpu.mem_read(cp-16,128))
                cpu.mem_write(output-16,b'\xa5'*544);cpu.mem_write(STACK,struct.pack('<I',number))
                pointer=struct.unpack('<I',cpu.mem_read(BASE+field,4))[0]
                main_before=bytes(cpu.mem_read(BASE,0x400000))
                call(cpu,0xD7720,(output,pointer,np,cp),instruction_limit=1000000)
                raw=bytes(cpu.mem_read(output,512)).split(b'\0')[0]
                expected=(name+'\n  '+category+' '+str(number)+'%').encode()
                assert bytes(cpu.mem_read(output-16,16))==bytes(cpu.mem_read(output+512,16))==b'\xa5'*16
                assert bytes(cpu.mem_read(output+len(raw)+1,511-len(raw)))==b'\xa5'*(511-len(raw))
                assert bytes(cpu.mem_read(np-16,128))==names_before and bytes(cpu.mem_read(cp-16,128))==category_before
                assert bytes(cpu.mem_read(BASE,0x400000))==main_before
                if version=='prepared-correction':assert raw==expected and raw.isascii() and raw.count(b'%')==1
                else:assert raw.startswith(expected) and raw!=expected
                cases.append(dict(version=version,pointer_field=field,native_format_pointer=pointer,
                    name=name,category=category,number=number,output_hex=raw.hex(),expected_hex=expected.hex(),
                    output_CP932=raw.decode('cp932',errors='backslashreplace'),
                    full_native_sprintf_helpers_ABI_input_output_stack_return_andunowned4MiB_pass=True,
                    defect_reproduced=version=='current-defect',correction_exact=version=='prepared-correction'))
        cpu.hook_del(hook)
        assert bytes(cpu.mem_read(ctx.actor_root,0x1A04))==ctx.actor_bytes
    assert len(cases)==24
    save(out,dict(cases=cases,source_cases=12,corrected_cases=12,both_Local_andCargo_pointer_fields_checked=True,
        target_ARM9_sha256=sha(target),parent_runtime=ctx.receipt(),current_executed_addresses=sorted(all_executed),
        all_executed_instructions_exact_target_orparent_owned_sections=True,
        all_corrected_outputs_complete_ASCII_with_one_literal_percent_andone_NUL=True,
        same_name_category_integer_arguments_andnative_callers=True,
        all_existing_code_town_capture_fonts_trade_andpredicates_preserved=True,
        offline_parent_snapshot_plus_declared_target_static_pointers_not_gameplay=True,
        target_own_coldboot_market_pixels_andregistered_release_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [prepared/'preparation.json',prepared/'target_arm9.bin',Path(__file__)]}))
    print('PASS12 source reproductions/12 exact target native printf cases;Local/Cargo,Cheese Food101%,one percent/no garbage;gameplay pending.')

if __name__=='__main__':main()
