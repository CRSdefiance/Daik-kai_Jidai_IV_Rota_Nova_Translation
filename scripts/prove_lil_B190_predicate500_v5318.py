"""Original500 predicate: strict threshold result and exactly one owned RNG write."""
from pathlib import Path
import struct
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_PC
from scripts.native_call_abi_v764 import call
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer

BASE=0x02000000
ROOT=Path('work/analysis/lil_B190_predicate500_v5318')
SOURCE=Path('work/analysis/lil_B190_source_v5314/all17_clean_current_complete_context.json')


def probe500(arm,common,raw,plan,block,command,seed_fixture=None):
    original=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans=[(0x25664,0x2570C),(0x519D4,0x51A28),(0xD9834,0xD9868),(0x29874,0x29968)]
    assert all(arm[a:b]==original[a:b] for a,b in spans)
    assert command['word']==0x8000 and command['whole_command_hex']=='0080fffff4010000' and command['native_extent']==8
    cpu,get,provider=machine(arm,common,raw,plan)
    seed_address,multiplier,increment,mask=struct.unpack_from('<4I',arm,0xD9858)
    assert (seed_address,multiplier,increment,mask)==(0x02168EB8,0x41C64E6D,0x3039,0x7FFF)
    init_flag=struct.unpack_from('<I',arm,0x51A20)[0]
    assert struct.unpack('<I',cpu.mem_read(init_flag,4))[0]==0
    snapshot_seed=struct.unpack('<I',cpu.mem_read(seed_address,4))[0]
    if seed_fixture is not None:
        assert 0<=seed_fixture<=0xFFFFFFFF
        cpu.mem_write(seed_address,struct.pack('<I',seed_fixture))
    stream,owner,result,length=0x02660000,0x02650000,0x02668000,0x02668100
    cpu.mem_write(stream-16,b'\xA5'*(len(block)+32));cpu.mem_write(stream,block)
    cpu.mem_write(owner-16,b'\xA5'*64);cpu.mem_write(owner,struct.pack('<4I',0,stream+command['offset'],0,0))
    owner_before=bytes(cpu.mem_read(owner-16,64))
    cpu.mem_write(result-16,b'\xA5'*80);cpu.mem_write(result,bytes(24))
    cpu.mem_write(length-16,b'\xA5'*36);cpu.mem_write(length,bytes(4))
    before=bytes(cpu.mem_read(BASE,0x400000));seed=struct.unpack('<I',cpu.mem_read(seed_address,4))[0]
    next_seed=(seed*multiplier+increment)&0xFFFFFFFF
    roll=((next_seed>>16)&mask)%1000
    expected_result=0 if roll<500 else 1 if roll==500 else 2
    writes=[];calls=[];returns=[]
    def trace(u,pc,size,_):
        if pc==BASE+0x519D4:calls.append(dict(PC=pc,bound=u.reg_read(UC_ARM_REG_R0)))
        else:returns.append(dict(PC=pc,roll=u.reg_read(UC_ARM_REG_R0)))
    hooks=[cpu.hook_add(UC_HOOK_CODE,trace,begin=BASE+0x519D4,end=BASE+0x519D4),
           cpu.hook_add(UC_HOOK_CODE,trace,begin=BASE+0x25680,end=BASE+0x25680),
           cpu.hook_add(UC_HOOK_MEM_WRITE,lambda u,a,address,size,value,d:writes.append(dict(PC=u.reg_read(UC_ARM_REG_PC),address=address,size=size,value=value)),begin=BASE,end=BASE+0x3FFFFF)]
    try:call(cpu,0x2A510,(result,owner,length,0),instruction_limit=500000)
    finally:
        for h in hooks:cpu.hook_del(h)
    values=list(struct.unpack('<6I',cpu.mem_read(result,24)))
    assert values==[2,expected_result,0,0,0,0] and struct.unpack('<I',cpu.mem_read(length,4))[0]==8
    assert calls==[dict(PC=BASE+0x519D4,bound=1000)] and returns==[dict(PC=BASE+0x25680,roll=roll)]
    expected_writes=[dict(PC=BASE+0xD984C,address=seed_address,size=4,value=next_seed)]
    assert writes==expected_writes
    expected=bytearray(before);struct.pack_into('<I',expected,seed_address-BASE,next_seed)
    assert bytes(cpu.mem_read(BASE,0x400000))==expected
    assert bytes(cpu.mem_read(stream,len(block)))==block and bytes(cpu.mem_read(owner-16,64))==owner_before
    for at in [stream-16,stream+len(block),result-16,result+24,length-16,length+4]:assert bytes(cpu.mem_read(at,16))==b'\xA5'*16
    # Cleanup restores only the exact owned RNG field, after validating its
    # genuine native update. No outcome is forced in the unmodified case.
    cpu.mem_write(seed_address,struct.pack('<I',seed))
    assert bytes(cpu.mem_read(BASE,0x400000))==before
    if seed_fixture is not None:cpu.mem_write(seed_address,struct.pack('<I',snapshot_seed))
    return dict(offset=command['offset'],word=command['word'],source_command_hex=command['whole_command_hex'],
        native_result=values,native_extent=8,seed_address=seed_address,snapshot_seed=snapshot_seed,
        supplied_CPU_only_seed_fixture=seed_fixture,unforced_current_snapshot=seed_fixture is None,
        before_seed=seed,after_seed=next_seed,bound=1000,threshold=500,roll=roll,
        result_classes='0 when roll<500;1 when equal500;2 when roll>500',
        original_native_seed_writes=writes,original_bounded_random_calls=calls,original_roll_returns=returns,
        full4MiB_difference_exactly_one_original_owned_RNG_word=True,
        cleanup_restores_owned_seed_and_recovers_all4MiB=True,all_input_owner_output_canaries_and_ABI_exact=True,
        current_executed_instruction_addresses=len(provider.executed_current),source_plot_effect_semantics_not_inferred=True)


if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B190_voices_v5315/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])]
    blocks=[IlnkContainer.parse(i.read_file('/data/SC2.DK4')).blocks[190] for i in images]
    predicates=[c for c in packet['blocks'][0]['all_current_native_commands'] if c['word']==0x8000]
    inverse=pow(0x41C64E6D,-1,1<<32)
    fixtures={roll:(((roll<<16)-0x3039)*inverse)&0xFFFFFFFF for roll in [499,500,501]}
    cases=[]
    for label,block in zip(['clean','current'],blocks,strict=True):
        for c in predicates:
            for target,seed in [(None,None),*fixtures.items()]:
                row=ctx.execute(probe500,block,c,seed);ctx.machines.pop()
                if target is not None:assert row['roll']==target
                cases.append(dict(version=label,**row))
    assert not ctx.machines and len(cases)==8 and sum(r['unforced_current_snapshot'] for r in cases)==2
    for at in [8]:
        for fixture in [None,*fixtures.values()]:
            pair=[r for r in cases if r['offset']==at and r['supplied_CPU_only_seed_fixture']==fixture]
            assert len(pair)==2 and pair[0]['native_result']==pair[1]['native_result'] and pair[0]['after_seed']==pair[1]['after_seed']
    save(ROOT/'all8_original500_predicate_RNG_ownership_cases.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),cases=cases,
        unforced_cases=2,CPU_only_boundary_fixture_cases=6,actual_emulator_seed_writes=0,
        no_global_RNG_or_state_preservation_waiver=True,B180_predecessor_diagnostics_preserved_without_claiming_a_new_failure=True,
        all8_seed_transitions_native_results_and_unowned4MiB_checks_pass=True,
        no_B190_gameplay_outcome_or_earned_fashion_claim=True,new_reviews=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(cases=8,unforced=2,CPU_boundary_fixtures=6,all_three_native_result_classes_proved=True,
        seed_address=hex(0x2168EB8),actual_emulator_writes=0,review_credit=0),flush=True)
