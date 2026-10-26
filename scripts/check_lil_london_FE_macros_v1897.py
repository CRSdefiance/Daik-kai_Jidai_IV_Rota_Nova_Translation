"""Exercise the exact FE macro caller with its original null actor context."""
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_FE_macros_v1897')
DOC=Path('translations/lil_london_editorial_manuscript_v3.json')
FONT=Path('work/analysis/lil_London_FE_v1896/all3_FE_native_planes_and_actual_mode_reconciliation.json')
INPUT,OUTPUT=0x02660000,0x02662000

if __name__=='__main__':
    assert not ROOT.exists()
    doc,font=map(read,(DOC,FONT))
    assert font['manuscript_sha256']==sha(DOC.read_bytes())
    arm=NdsImage.open(doc['current_ROM']).read_file('/__arm9__.bin')
    snapshot=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_London_context_run_v1884_RESEARCH_ONLY/frame_052110_arm9_ram.bin')
    raw=snapshot.read_bytes()
    cpu,get=get_machine(arm,raw)
    hook=cpu.hook_add(UC_HOOK_CODE,lambda u,a,z,d:u.reg_write(UC_ARM_REG_PC,0x027E0000),begin=0x02024314,end=0x02024314)
    cases=[]
    try:
        for row in doc['records']:
            if row['source_presentation_prefix_hex']!='fe':continue
            r=next(r for r in font['cases'] if r['id']==row['id'])
            logical=row['english'].split('}',1)[1].removesuffix('{PAD}').encode('ascii')
            wrapped=bytes.fromhex(r['encoded_hex'])[1:]
            checks=[]
            for kind,body in (('logical',logical),('wrapped',wrapped)):
                for phase in range(4):
                    cpu.mem_write(INPUT-16,b'\xa5'*2080)
                    cpu.mem_write(INPUT+phase,body+b'\0')
                    before=bytes(cpu.mem_read(INPUT-16,2080))
                    cpu.mem_write(OUTPUT-16,b'\xa5'*4128)
                    call(cpu,0x24310,(OUTPUT,INPUT+phase,0),instruction_limit=400000)
                    value=bytes(cpu.mem_read(OUTPUT,4096)).split(b'\0')[0]
                    assert value==body
                    assert bytes(cpu.mem_read(0x02000000,0x400000))==raw
                    assert bytes(cpu.mem_read(INPUT-16,2080))==before
                    assert bytes(cpu.mem_read(OUTPUT-16,16))==b'\xa5'*16
                    assert bytes(cpu.mem_read(OUTPUT+len(value)+1,4095-len(value)))==b'\xa5'*(4095-len(value))
                    checks.append(dict(kind=kind,alignment=phase,output_hex=value.hex(),null_actor_FE_call=True,
                        all4MiB_ABI_input_output_guards_exact=True))
            cases.append(dict(id=row['id'],macro_cases=checks))
    finally:cpu.hook_del(hook)
    assert len(cases)==3 and sum(len(r['macro_cases']) for r in cases)==24
    ROOT.mkdir(parents=True)
    save(ROOT/'all3_FE24_native_macro_alignment_cases.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        source_snapshot=str(snapshot),source_snapshot_sha256=sha(raw),cases=cases,
        exact_original_FE_null_actor_caller24310_proven=True,all24_full_macro_input_output_and4MiB_guards_pass=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(FE_macro_records=3,native_alignment_calls=24,null_actor_native_FE_context=True))
