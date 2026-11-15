"""Execute original post-report cleanup to the outcome boundary in copied RAM."""
import struct
from pathlib import Path
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R8, UC_ARM_REG_PC, UC_ARM_REG_SP
from scripts.current_common_native_context_v2620b import CurrentContext
from scripts.verify_village_wrap_v608 import read, save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/admiral_shot_return_v2662')
DOC = Path('translations/admiral_shot_contextual_editorial_manuscript_v2.json')
BASE, STACK, OPAQUE = 0x02000000,0x027F0000,0x02666000

if __name__ == '__main__':
    assert not ROOT.exists()
    ctx = CurrentContext(DOC,'out/all_routes_combined_v1807_candidate.nds',ROOT)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x73BAC,0x73C10),(0x55E6C,0x55E9C),(0xA3DCC,0xA3DD8),(0x6609C,0x66134),
             (0x72368,0x72474),(0x71D54,0x71EFC)]
    assert all(ctx.arm[a:b] == clean[a:b] == ctx.raw[a:b] for a,b in spans)
    cpu,get,_ = ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
    root = get(0xCB1A8); fleet = root+4+8*132; mobile = get(0x36C70,fleet+12)
    assert mobile and get(0x35320,fleet) == 8
    shipstate = get(0x55E6C,mobile)
    assert BASE <= shipstate < BASE+0x400000-20
    before = bytes(cpu.mem_read(BASE,0x400000))
    cpu.reg_write(UC_ARM_REG_SP,STACK); cpu.reg_write(UC_ARM_REG_R8,OPAQUE)
    cpu.mem_write(STACK+0x88,struct.pack('<2I',fleet,mobile))
    calls = []
    def observe(u,pc,size,_):
        if pc in [BASE+n for n in [0x55E6C,0xA3DCC,0x6609C,0x72368,0x71D54]]:
            calls.append(dict(PC=pc,args=[u.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2]]))
        if pc in [BASE+0x72368,BASE+0x71D54]: u.emu_stop()
    cpu.hook_add(UC_HOOK_CODE,observe)
    cpu.emu_start(BASE+0x73BAC,BASE+0x73C10,count=1000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE+0x72368
    assert [c['PC'] for c in calls] == [BASE+n for n in [0x55E6C,0xA3DCC,0x6609C,0x72368]]
    assert calls[0]['args'][0] == mobile and calls[1]['args'][0] == shipstate
    assert calls[2]['args'] == [2,250,0] and calls[3]['args'][:2] == [OPAQUE,0]
    after = bytes(cpu.mem_read(BASE,0x400000))
    assert after[mobile-BASE+13] == 0 and after[shipstate-BASE+4:shipstate-BASE+8] == b'\xff'*4
    changes = [dict(address=BASE+i,before=a,after=b) for i,(a,b) in enumerate(zip(before,after,strict=True)) if a != b]
    # The second branch is an isolated discriminator test; no world fleet,
    # captain,ship or battle result is changed. Stop before either callee.
    branches = []
    for captain_byte,target in [(32,0x72368),(181,0x71D54)]:
        u,g,_ = ctx.machine(ctx.arm,ctx.common,ctx.raw,ctx.plan)
        scratch = 0x02666100
        u.mem_write(scratch,bytes(132));u.mem_write(scratch+8,bytes([captain_byte]))
        u.mem_write(STACK+0x88,struct.pack('<I',scratch));u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_R8,OPAQUE)
        captured = []
        def stop(v,pc,size,_):
            if pc in [BASE+0x72368,BASE+0x71D54]:
                captured.append(dict(PC=pc,args=[v.reg_read(r) for r in [UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2]]));v.emu_stop()
        u.hook_add(UC_HOOK_CODE,stop);u.emu_start(BASE+0x73BD4,BASE+0x73C10,count=1000)
        assert len(captured) == 1 and captured[0]['PC'] == BASE+target and captured[0]['args'][:2] == [OPAQUE,0]
        if captain_byte == 181: assert captured[0]['args'][2] == 0
        assert bytes(u.mem_read(BASE,0x400000)) == ctx.raw
        branches.append(dict(synthetic_header_byte=captain_byte,original_target=captured[0],
            header_outside_main4MiB=True,all_main4MiB_unchanged=True,
            no_outcome_callee_executed=True,no_actual_merchant_or_shot_event=True))
    save(ROOT/'original_post_report_cleanup_and_dispatch.json',dict(candidate=str(ctx.rompath),candidate_sha256=sha(ctx.rompath.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        current_pipeline_plan=str(ctx.proof_path),current_pipeline_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_exact_spans=spans,source_snapshot='historical covering-fire6010;copied RAM only',
        CPU_only_interior_entry=BASE+0x73BAC,original_enemy_fleet=fleet,original_enemy_mobile=mobile,
        original_battle_ship_state=shipstate,original_cleanup_calls=calls,main4MiB_changes=changes,
        native_mobile_flag_cleared_and_battle_ship_state_marked_minus1=True,
        native_experience_dispatch_2_250_0_executed_without_substitution=True,
        original_post_message_calls_capture_mode0_for_regular_commander=True,
        opaque_caller_parameter_passed_through_unchanged_not_dereferenced=True,
        isolated_original_regular_and_B5_dispatch_tests=branches,
        current_instructions_exact=True,no_native_RNG_speech_effect_or_outcome_replaced=True,
        not_actual_UI_dismissal_shot_effect_chance_eligibility_or_gameplay_outcome=True,
        no_new_emulator_run_or_completion_credit=True,
        next='Reconcile the common portrait return and both outcome callees with preserved representative gameplay;do not assert that this copied-state interior entry is an activated shot.',
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Original post-report cleanup,experience dispatch andboth outcome targets pass copied-state focused tests;no actual shot or substituted outcome.')
