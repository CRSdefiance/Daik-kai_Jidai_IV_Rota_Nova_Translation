"""Original printf/shared macro pipeline,all84 logical templates and typed samples.

This is not a layout,active-role,cache-repack or actual revised-panel approval.
"""
from pathlib import Path
import struct
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/town_services_literals_v2055')
DOC=Path('translations/primary_town_services_contextual_editorial_manuscript_v1.json')
OBS=Path('E:/Rota Nova translations/Generated/work/emulation_v193/town_services_actual_v2053_V2047/common_observer/requests.json')
TEMPLATE,OUTPUT,FORMATTED,ARGS,NAMES=0x02660000,0x02662000,0x02664000,0x02666000,0x02667000

if __name__=='__main__':
    assert not ROOT.exists()
    doc,obs=map(read,(DOC,OBS));assert not obs['errors']and not obs['mismatches']and obs['all_host_slots_restored_and_core_file_exact']
    seed=next(r for r in obs['rows']if r['message_ID']==55)['complete_readonly_snapshots']['WRAM'];raw=Path(seed['path']).read_bytes()
    assert sha(raw)==seed['sha256']and len(raw)==4194304
    arm=NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin');assert sha(arm)==doc['required_runtime_ARM9_sha256']
    cpu,get=get_machine(arm,raw);assert get(0x7F244)==3
    cases=[];failures=[]
    for row in doc['records']:
        n=row['message_id'];text=row['english'].removesuffix('{PAD}');template=text.encode('ascii');count=template.count(b'%s')
        assert b'\n'not in template and b'\r'not in template and count==row['source_Japanese'].count('%s')
        # Supplied values are typed stress inputs,not visits to those conditional lines.
        if n in(54,55):variants=[['Mihwa'],['Margherita']]
        elif n==58:variants=[['Maria'],['Rafael']]
        elif 65<=n<=70:variants=[['Hangzhou'],['Constantinople']]
        elif n==83:variants=[['Li Clan','１'],['Bergstrom Fleet','９９９９９９９９９９']]
        elif count:variants=[['１'],['６００'],['９９９９９９９９９９']]
        else:variants=[[]]
        for supplied in variants:
            assert len(supplied)==count
            args=[value.encode('cp932')for value in supplied];expected=template
            for value in args:expected=expected.replace(b'%s',value,1)
            for phase in range(4):
                try:
                    cpu.mem_write(TEMPLATE-16,b'\xa5'*2080);cpu.mem_write(TEMPLATE+phase,template+b'\0');before=bytes(cpu.mem_read(TEMPLATE-16,2080))
                    pointers=[];arg_snapshots=[]
                    for index,value in enumerate(args):
                        p=NAMES+index*256+phase;cpu.mem_write(p-16,b'\xa5'*(len(value)+33));cpu.mem_write(p,value+b'\0')
                        pointers.append(p);arg_snapshots.append((p-16,bytes(cpu.mem_read(p-16,len(value)+33))))
                    vector=b''.join(struct.pack('<I',p)for p in pointers);cpu.mem_write(ARGS-16,b'\xa5'*128);cpu.mem_write(ARGS,vector)
                    vector_before=bytes(cpu.mem_read(ARGS-16,128));cpu.mem_write(FORMATTED-16,b'\xa5'*4128)
                    call(cpu,0xCE898,(FORMATTED,TEMPLATE+phase,ARGS),instruction_limit=300000)
                    assert cpu.reg_read(UC_ARM_REG_R0)==len(expected)
                    formatted=bytes(cpu.mem_read(FORMATTED,4096)).split(b'\0')[0];assert formatted==expected
                    assert bytes(cpu.mem_read(FORMATTED-16,16))==b'\xa5'*16
                    assert bytes(cpu.mem_read(FORMATTED+len(expected)+1,4095-len(expected)))==b'\xa5'*(4095-len(expected))
                    cpu.mem_write(OUTPUT-16,b'\xa5'*4128);call(cpu,0x53914,(OUTPUT,FORMATTED,0),instruction_limit=400000)
                    expanded=bytes(cpu.mem_read(OUTPUT,4096)).split(b'\0')[0];assert expanded==expected
                    assert bytes(cpu.mem_read(OUTPUT-16,16))==b'\xa5'*16
                    assert bytes(cpu.mem_read(OUTPUT+len(expected)+1,4095-len(expected)))==b'\xa5'*(4095-len(expected))
                    assert bytes(cpu.mem_read(TEMPLATE-16,2080))==before and bytes(cpu.mem_read(ARGS-16,128))==vector_before
                    assert all(bytes(cpu.mem_read(at,len(value)))==value for at,value in arg_snapshots)
                    assert bytes(cpu.mem_read(FORMATTED,len(expected)+1))==expected+b'\0'
                    assert bytes(cpu.mem_read(0x02000000,4194304))==raw
                    cases.append(dict(message_ID=n,alignment=phase,supplied_arguments=supplied,formatted_hex=formatted.hex(),expanded_hex=expanded.hex(),
                        original_printf_return_exact=True,all4MiB_ABI_and_input_argument_output_guards_exact=True))
                except(ValueError,AssertionError)as exc:failures.append(dict(message_ID=n,alignment=phase,supplied=supplied,type=type(exc).__name__,error=str(exc)))
    ROOT.mkdir(parents=True)
    save(ROOT/'all84_original_printf_shared_expander_and_literal_guards.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        current_ROM=doc['current_ROM'],current_ROM_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),source_snapshot=seed,cases=cases,failures=failures,
        original_native_printf_calls=len(cases),original_shared_macro_calls=len(cases),
        all84_complete_logical_template_IDs=sorted({r['message_ID']for r in cases}),
        native_PRINTF_and_shared_expander_no_formatter_or_macro_stubs=True,
        supplied_typed_values_not_actual_conditional_line_visits=True,
        input_paragraphs_unwrapped_before_native_macro_expansion=True,
        active_argument_role_currency_direction_layout_repacking_and_revised_actual_gates_pending=True,
        no_ROM_profile_or_registry_mutation=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(templates=len({r['message_ID']for r in cases}),printf_calls=len(cases),shared_expander_calls=len(cases),failures=failures))
