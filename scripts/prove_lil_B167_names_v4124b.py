"""Distinguish native read-only player/NPC strings from owned crew-name scratch rings."""
import inspect,struct
from pathlib import Path
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B167_names_v4124b')
SOURCE = Path('work/analysis/lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice.json')
VOICE = Path('work/analysis/lil_B167_voices_v4120/current5_static_names_voices_and207_catalog_rebind.json')

def names(arm,common,raw,plan):
    cpu,get,provider = machine(arm,common,raw,plan)
    root = get(0xCB184)
    rows = []
    initial = bytes(cpu.mem_read(0x02000000,0x400000))
    for ident in [2,4,13,23,109]:
        actor = root+4+32*ident
        for kind,offset in [('progressive-nameplate',0x7ED88),('full-catalogue',0x7EDD4)]:
            before = bytes(cpu.mem_read(0x02000000,0x400000))
            rings,writes = [],[]
            def ring(u,pc,size,unused):
                owner = u.reg_read(UC_ARM_REG_R0)
                index = struct.unpack('<I',u.mem_read(owner+8,4))[0]
                assert index<32
                rings.append(dict(owner=owner,counter_address=owner+8,source_index=index,output_slot=owner+12+index*128))
            hook = cpu.hook_add(UC_HOOK_CODE,ring,begin=0x020AC000,end=0x020AC000)
            wh = cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(
                PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=0x02000000,end=0x023fffff)
            try:
                pointer = get(offset,actor)
            finally:
                cpu.hook_del(hook)
                cpu.hook_del(wh)
            data = bytes(cpu.mem_read(pointer,80)).split(b'\0')[0]
            value = data.decode('cp932')
            print(dict(actor=ident,consumer=kind,text=value,rings=len(rings),writes=len(writes)),flush=True)
            assert len(rings) in [0,1]
            if rings:
                owned = rings[0]
                assert pointer==owned['output_slot']
                counter,end = owned['counter_address'],pointer+len(data)+1
                restored = bytearray(cpu.mem_read(0x02000000,0x400000))
                for write in writes:
                    if write['address']==counter:
                        assert write['PC'] in [0x020AC00C,0x020AC020] and write['size']==4
                    else:
                        assert pointer<=write['address'] and write['address']+write['size']<=end
                        assert write['size']==1 and write['PC'] in [0x020CED7C,0x020CED90,0x020CEDAC,0x020CEDC0]
                assert struct.unpack('<I',cpu.mem_read(counter,4))[0]==(owned['source_index']+1)%32
                for a,b in [(counter,counter+4),(pointer,end)]:
                    restored[a-0x02000000:b-0x02000000]=before[a-0x02000000:b-0x02000000]
                    cpu.mem_write(a,before[a-0x02000000:b-0x02000000])
                assert bytes(restored)==before
                mode = 'original-owned-name-scratch-ring'
            else:
                assert not writes
                assert 0x02000000<=pointer and pointer+len(data)+1<=0x02400000
                assert before[pointer-0x02000000:pointer-0x02000000+len(data)+1]==data+b'\0'
                mode = 'original-read-only-name-pointer-without-scratch-ring'
            assert bytes(cpu.mem_read(0x02000000,0x400000))==before
            rows.append(dict(actor_ID=ident,actor_object=actor,consumer=kind,getter=0x02000000+offset,pointer=pointer,
                text=value,text_hex=data.hex(),ownership_mode=mode,original_scratch_rings=rings,original_getter_writes=writes,
                all_actor_models_and_unowned4MiB_exact=True,source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB=True))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==initial
    return dict(rows=rows,current_executed_instruction_addresses=len(provider.executed_current),
        all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact=True)

if __name__ == '__main__':
    assert not ROOT.exists()
    source,voice=read(SOURCE),read(VOICE)
    image=NdsImage.open(source['current_ROM'])
    arm=image.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8]==clean[0x541C0:0x541C8]
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B167_voices_v4120/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    native=ctx.execute(names)
    ctx.machines.pop()
    assert not ctx.machines
    values={(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']}
    expected={2:'Lil Argot',4:'Janus Pasar',13:'Cesare Tony',23:'Manuel Almeida',109:'Shipwright'}
    full={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh5_actor_names']['rows']}
    assert len(values)==10 and {i:values[i,'progressive-nameplate'] for i in expected}==expected
    assert {i:values[i,'full-catalogue'] for i in expected}==full
    save(ROOT/'ten_original_names_owned_scratch_and_readonly_paths.json',dict(candidate=source['current_ROM'],
        candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        ARM9_sha256=sha(arm),native_ten_consumer_cases=native,progressive_nameplate_values=expected,full_catalogue_values=full,
        approved_prose_names={'2':'Lil','4':'Janus','13':'Cesare','23':'Manuel','109':'Shipwright'},
        source_selector6D_is_static_actor109_not_literal_m=True,source_selector0D_is_static_actor13_not_CR=True,
        generic_source_Shipwright_role_bound_without_inventing_personal_name=True,later_older_record0D_reaudit_stays_open=True,
        not_actual_B167_nameplate_observation=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_owned_adapter=inspect.getsource(names),preserved_failed_one_ring_assumption='scripts/prove_lil_B167_names_v4124.py',
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,Path('scripts/prove_lil_B167_names_v4124.py'),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Ten original name consumers pass with exact owned-scratch/read-only paths;no assets changed.')
