"""Original exclusion and post-RNG comparison tests;stop before every shot effect."""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_PC, UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/admiral_shot_gate_v2659')
CONTEXT = Path('work/analysis/admiral_shot_context_v2656c/source_context_packet.json')
BASE, STACK = 0x02000000, 0x027F0000

if __name__ == '__main__':
    assert not ROOT.exists()
    context = read(CONTEXT)
    rom = NdsImage.open(context['current_ROM'])
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    raw = Path(context['actual_snapshot']).read_bytes()
    assert sha(arm) == context['current_ARM9_sha256'] and sha(raw) == context['actual_snapshot_sha256']
    for lo,hi in [(0x73B18,0x73C10),(0x8235C,0x823D8),(0x7DD38,0x7DE1C)]:
        assert arm[lo:hi] == clean[lo:hi] == raw[lo:hi]
    def run(start, registers, locals_):
        cpu,get = get_machine(arm,raw)
        before = bytes(cpu.mem_read(BASE,0x400000))
        cpu.reg_write(UC_ARM_REG_SP,STACK)
        for offset,value in locals_.items(): cpu.mem_write(STACK+offset,struct.pack('<I',value))
        for reg,value in registers.items(): cpu.reg_write(reg,value)
        executed = []
        def watch(u,pc,size,_):
            assert BASE <= pc < BASE+len(arm)
            at = pc-BASE
            assert bytes(u.mem_read(pc,size)) == arm[at:at+size]
            executed.append(pc)
            if pc in [BASE+0x73D7C,BASE+0x73C10,BASE+0x73B8C]: u.emu_stop()
            assert pc not in [BASE+0x519D4,BASE+0x1096F8,BASE+0x53D44,BASE+0x72368,BASE+0x71D54]
        cpu.hook_add(UC_HOOK_CODE,watch)
        cpu.emu_start(BASE+start,BASE+0x73D80,count=100000)
        end = cpu.reg_read(UC_ARM_REG_PC)
        assert end in [BASE+0x73D7C,BASE+0x73C10,BASE+0x73B8C]
        assert bytes(cpu.mem_read(BASE,0x400000)) == before == raw
        return dict(end_PC=end,executed_addresses=executed,
            all_executed_instructions_current_exact=True,all_main4MiB_bytes_unchanged=True,
            no_RNG_effect_speech_or_outcome_called=True)
    exclusions = []
    for state,flag,target,metric_called in [(1,0,0x73D7C,False),(2,1,0x73D7C,False),(2,0,0x73C10,True)]:
        result = run(0x73B18,{}, {0x90:state,0x94:flag})
        assert result['end_PC'] == BASE+target
        assert (BASE+0x8235C in result['executed_addresses']) == metric_called
        if metric_called: assert BASE+0x823C8 in result['executed_addresses']
        exclusions.append(dict(CPU_only_battle_condition_locals=[state,flag],
            physical_Lookout_unassigned_unchanged=True,original_metric_called=metric_called,**result))
    comparisons = []
    # These are pure arithmetic unit inputs after the RNG call. They are never
    # written to an emulator save,actor,RNG state or battle object. Stop before
    # the effect even when the comparison would allow an event.
    for metric in [151,159,160,499,500]:
        threshold = metric//10
        for draw in sorted({0,threshold,threshold+1,1999}):
            result = run(0x73B70,{UC_ARM_REG_R0:draw,UC_ARM_REG_R4:metric},{})
            accepts = draw <= threshold
            assert result['end_PC'] == BASE+(0x73B8C if accepts else 0x73C10)
            comparisons.append(dict(synthetic_post_RNG_comparison_inputs_only=True,
                computed_role_metric=metric,draw_value=draw,integer_threshold=threshold,
                accepted_comparison=accepts,not_original_chance_draw_or_gameplay_eligibility=True,**result))
    thresholds = []
    for metric in [0,149,150]:
        result = run(0x73B60,{UC_ARM_REG_R4:metric},{})
        assert result['end_PC'] == BASE+0x73C10
        thresholds.append(dict(synthetic_threshold_input_only=metric,**result))
    md = Cs(CS_ARCH_ARM,CS_MODE_ARM)
    aftermath = [dict(address=i.address,mnemonic=i.mnemonic,operands=i.op_str)
        for i in md.disasm(arm[0x73BAC:0x73C10],BASE+0x73BAC)]
    ROOT.mkdir(parents=True)
    save(ROOT/'original_gate_focused_tests.json',dict(candidate=context['current_ROM'],
        candidate_sha256=context['current_ROM_sha256'],ARM9_sha256=sha(arm),
        source_context=str(CONTEXT),source_context_sha256=sha(CONTEXT.read_bytes()),
        exclusion_cases=exclusions,threshold_cases=thresholds,post_RNG_arithmetic_cases=comparisons,
        physical_empty_job_returns_zero_not_logical_speaker_skill=True,
        exact_original_post_report_instructions=aftermath,
        no_new_actual_event_or_current_emulator_run=True,
        unresolved_risk='Distinct shot-effect,held-message dismissal and post-shot outcome transition have not yet been reconciled with representative runtime evidence. Neither the original1022dispatch-only probe nor these comparison tests establish them. Existing generic role7/portrait and battle-result evidence should be reused where exact source/current control paths match;individual visits to every alternative are unnecessary.',
        scope='Three original exclusion paths with unchanged physical job and models;three threshold exclusions;20isolated arithmetic inputs after the RNG call. No actual RNG call,result,speech,effect or battle outcome is substituted or executed. All tests stop before the shot effect. Post-report code is exact-source disassembly only,not a dynamic transition proof.',
        completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Three source exclusion paths,three threshold exclusions and20post-RNG arithmetic unit cases pass;no shot effects or gameplay outcomes executed.')
