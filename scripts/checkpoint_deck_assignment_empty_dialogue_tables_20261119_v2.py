"""Resolve which empty crew dialogue tables are bypassed on the normal Deck assignment path."""

from collections import Counter
from pathlib import Path
from struct import unpack_from

from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R4,UC_ARM_REG_SP

from scripts import checkpoint_shared_reader_and_crew_bypasses_20261119 as prior
from scripts.probe_button_prompt_native import BASE,STACK,STOP,VIEW,call,machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

base,current=prior.base,prior.current
OUTPUT=prior.OUTPUT.with_name("deck_assignment_empty_dialogue_tables_20261119_v2.json")
CABIN_TYPE=0x020132C0
PROHIBITED=(9,10,11,21,22,24)


def guard_inputs(arm):
    cpu=machine(arm)
    allowed = {}
    for role in range(25):
        call(cpu,0x7AD4,(role,))
        allowed[role]=cpu.reg_read(UC_ARM_REG_R0)
        assert allowed[role] == int(role not in PROHIBITED)
    exits=[]
    for role in range(25):
        cpu.reg_write(UC_ARM_REG_R4,role)
        cpu.reg_write(UC_ARM_REG_SP,STACK)
        destinations=(0x020136A0,0x020134CC)
        seen=[]
        def stop(u,pc,size,_):
            if pc in destinations:
                seen.append(pc)
                u.emu_stop()
        hook=cpu.hook_add(UC_HOOK_CODE,stop)
        cpu.emu_start(0x020134BC,STOP,count=256)
        cpu.hook_del(hook)
        assert seen==[destinations[allowed[role]]]
        exits.append(dict(role=role,assignable=bool(allowed[role]),original_exit=seen[0]))
    return exits


def captain_gate(arm):
    cpu=machine(arm)
    results=[]
    for captain in range(4):
        def run(u,pc,size,_):
            if pc==0x0207F244:
                u.reg_write(UC_ARM_REG_R0,captain)
                u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            elif pc==0x020CB184:
                u.reg_write(UC_ARM_REG_R0,VIEW)
                u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            elif pc==0x02082A88:
                passed.append(True)
                u.emu_stop()
        hook=cpu.hook_add(UC_HOOK_CODE,run)
        for actor in range(207):
            passed=[]
            cpu.reg_write(UC_ARM_REG_R0,VIEW)
            cpu.reg_write(UC_ARM_REG_R1,14)
            cpu.reg_write(UC_ARM_REG_R2,actor)
            cpu.reg_write(UC_ARM_REG_LR,STOP)
            cpu.reg_write(UC_ARM_REG_SP,STACK)
            cpu.emu_start(0x02081FA4,STOP,count=256)
            assert bool(passed)==(actor==captain)
            if not passed:
                assert cpu.reg_read(UC_ARM_REG_PC)==STOP and cpu.reg_read(UC_ARM_REG_R0)==0
        cpu.hook_del(hook)
        call(cpu,0x7EF28,(captain,))
        assert cpu.reg_read(UC_ARM_REG_R0)==0
        results.append(dict(captain=captain,accepted_at_original_seat_14_guard=[captain],all_207_stock_actor_ids_checked=True,
            original_actor_group=0,crew_dialogue_group_switch_r6=1))
    return results


def model_slots(release):
    runtime=RegisteredRuntime(current.RELEASE,release["own_registered_startup"],captain=3)
    cpu,get,_=runtime.machine(runtime.arm,runtime.common,runtime.raw,runtime.plan)
    root=get(0xCB148)
    cases,role_counts=[],Counter()
    for model in range(154):
        obj=root+4+140*model
        vt=unpack_from("<I",cpu.mem_read(obj,4))[0]
        assert unpack_from("<I",cpu.mem_read(vt+0x18,4))[0]==CABIN_TYPE
        roles=[get(CABIN_TYPE-BASE,obj,i) for i in range(31)]
        assert roles==list(cpu.mem_read(obj+0x1E,31))
        seats=[i for i,role in enumerate(roles) if role==5]
        assert seats in ([],[14])
        cases.append(dict(model_index=model,role_5_seats=seats,other_empty_table_roles=sorted(set(roles)&{9,10,11,12,16})))
        role_counts.update(roles)
    next_object=root+4+140*154
    next_word=unpack_from("<I",cpu.mem_read(next_object,4))[0]
    assert not (BASE <= next_word < BASE+0x400000)
    return dict(snapshot=runtime.receipt(),role_cases=31*len(cases),initialized_designs=cases,
        native_role_counts=dict(sorted(role_counts.items())),next_unverified_design=dict(index=154,first_word=next_word))


def only_voice_calls(clean,arm):
    wanted={0x02012600,0x0201278C}
    expected=[(0x02012230,0x02012600,"arm_bl"),(0x02012250,0x0201278C,"arm_bl")]
    for image in (clean,arm):
        assert prior.inventory.branch_hits(image,BASE,wanted)==expected
    dis=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    dis.detail=True
    address=BASE+0x12130
    prepared=list(dis.disasm(clean[0x12130:0x12254],address))
    writes=[i.address for i in prepared if "r6" in [i.reg_name(r) for r in i.regs_access()[1]] and i.mnemonic!="pop"]
    assert writes==[0x0201213C,0x02012140]
    for off, words in ((0x12218,("000056e3","0200000a")),(0x12238,("000056e3","0200000a"))):
        assert clean[off:off+8].hex()=="".join(words)
    return expected


def main():
    assert not OUTPUT.exists()
    release=base.load(current.RELEASE)
    assert base.digest(current.ROM)==release["candidate_sha256"]
    assert base.digest(base.REGISTRY)==release["registry_sha256"]
    earlier=base.load(prior.OUTPUT)
    assert earlier["candidate_sha256"]==release["candidate_sha256"]
    clean,arm=(base.NdsImage.open(path).read_file(current.stage.ARM) for path in (current.stage.CLEAN,current.ROM))
    locks=[(0x7AD4,0x7B3C),(0x134BC,0x134D0),(0x81FA4,0x81FEC),(0x132C0,0x132CC),
        (0x12130,0x12254),(0x7EF28,0x7EF68)]
    assert all(clean[lo:hi]==arm[lo:hi] for lo,hi in locks)
    ja,en=map(guard_inputs,(clean,arm))
    assert ja==en
    clean_gates,stock=map(captain_gate,(clean,arm))
    assert clean_gates==stock
    branches=only_voice_calls(clean,arm)
    inventory=model_slots(release)
    grouped=[]
    for scope in earlier["remainder"]:
        values=set(scope["remaining_null_inputs"])
        assert values in ({5,9,10,11},{9,10,11})
        grouped.append(scope | dict(normal_deck_assignment_rejects=sorted(values&set(PROHIBITED)),
            captain_voice_table_condition_verified=5 in values,
            null_inputs_with_unverified_display_owner_outside_normal_assignment=sorted(values)))
    base.save(OUTPUT,dict(candidate_sha256=release["candidate_sha256"],clean_sha256=release["clean_input_sha256"],
        role_assignment_gate=ja,seat_14_guard=stock,only_direct_voice_table_callers=branches,
        stock_model_evidence=inventory,results=grouped,display_owners_newly_proven=0,new_gameplay_runs=0,
        excerpt_no_actual_assignment_or_playthrough=True,custom_saved_assignments_out_of_scope=True,
        raw_pending_shared_keys=276,full_goal_complete=False,
        evidence={str(p):base.digest(p) for p in (prior.OUTPUT,current.RELEASE,Path(__file__))}))
    print("Verified original Deck role rejection and Captain-seat restrictions for the scoped initialized models.")


if __name__=="__main__":
    main()

