"""Original interpreter query-value forwarding; structural B51 paths, not gameplay.

The original caller resumes after its parser call with a six-word result. Run
that exact instruction fragment until the next parser call, without executing
UI or substituting any actual game predicate. Synthetic result arguments are
explicit tests of the caller contract, never forced conversation coverage.
"""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R10, UC_ARM_REG_SP
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B50_registered_route_context_v8546 import RouteCurrentContext
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B51_result_flow_v8558b')
INPUT = Path('work/analysis/current_V8543_Hodram_native_v8546/current_native_input.json')
CONTROL = Path('work/analysis/Hodram_B51_source_controls_v8555/source_controls.json')
BASE = 0x02000000

def forward(arm, common, raw, plan, result_kind, result_value, prior_value):
    cpu, get, provider = machine(arm, common, raw, plan)
    stack, runtime, stream = 0x02670020, 0x02671020, 0x02672020
    result = (result_kind, result_value, 0x1357, 0x2468, 0x3579, 0x4680)
    cpu.mem_write(stack - 16, b'\xA5' * 144)
    cpu.mem_write(stack, struct.pack('<3I', 0, stream, 8))
    cpu.mem_write(stack + 12, struct.pack('<6I', *result))
    cpu.mem_write(runtime - 16, b'\xA5' * 128)
    cpu.mem_write(runtime + 0x54, struct.pack('<I', 1))
    cpu.mem_write(stream - 16, b'\xA5' * 64)
    initial_stack = bytes(cpu.mem_read(stack - 16, 144))
    initial_runtime = bytes(cpu.mem_read(runtime - 16, 128))
    initial_stream = bytes(cpu.mem_read(stream - 16, 64))
    before = bytes(cpu.mem_read(BASE, 0x400000))
    for reg, value in [(UC_ARM_REG_SP, stack), (UC_ARM_REG_R6, 1), (UC_ARM_REG_R7, 0), (UC_ARM_REG_R8, prior_value), (UC_ARM_REG_R10, runtime)]:
        cpu.reg_write(reg, value)
    stop = BASE + 0x24070
    visited = []
    def trace(u, pc, size, unused):
        visited.append(pc)
        if pc == stop:
            u.emu_stop()
    hook = cpu.hook_add(UC_HOOK_CODE, trace)
    try:
        cpu.emu_start(BASE + 0x24074, 0, count=100)
    finally:
        cpu.hook_del(hook)
    assert visited[-1] == stop and len(visited) < 100
    expected = result_value if result_kind == 2 else prior_value
    assert cpu.reg_read(UC_ARM_REG_R3) == cpu.reg_read(UC_ARM_REG_R8) == expected
    assert cpu.reg_read(UC_ARM_REG_R0) == stack + 12 and cpu.reg_read(UC_ARM_REG_R1) == stack and cpu.reg_read(UC_ARM_REG_R2) == stack + 8
    assert cpu.reg_read(UC_ARM_REG_SP) == stack
    after_stack = bytes(cpu.mem_read(stack - 16, 144))
    expected_stack = bytearray(initial_stack)
    expected_stack[20:24] = struct.pack('<I', stream + 8)
    expected_stack[24:28] = bytes(4)  # Original caller zeroes the next extent before calling the parser.
    assert after_stack == expected_stack and struct.unpack('<6I', cpu.mem_read(stack + 12, 24)) == result
    assert bytes(cpu.mem_read(runtime - 16, 128)) == initial_runtime and bytes(cpu.mem_read(stream - 16, 64)) == initial_stream
    assert bytes(cpu.mem_read(BASE, 0x400000)) == before
    return dict(result=list(result), previous_structural_value=prior_value, next_parser_r3=expected,
        original_value_update_orcarry_andcursor_advance_exact=True, all_six_return_words_preserved=True,
        full_unowned4MiB_actors_stream_runtime_stack_canaries_andSP_exact=True,
        executed_current_instruction_addresses=visited, synthetic_caller_arguments_not_gameplay_predicates=True)

if __name__ == '__main__':
    assert not ROOT.exists()
    inp, control = map(read, [INPUT, CONTROL])
    image = NdsImage.open(inp['current_ROM'])
    arm, clean = image.read_file('/__arm9__.bin'), NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    start, end = 0x24048, 0x24118
    assert arm[start:end] == clean[start:end]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    instructions = [dict(address=i.address, hex=i.bytes.hex(), mnemonic=i.mnemonic, operands=i.op_str) for i in decoder.disasm(arm[start:end], BASE + start)]
    assert arm[0x24068:0x24074].hex() == '0830a0e108708de5261900eb'
    assert arm[0x240D4:0x240D8].hex() == '10809de5'
    ROOT.mkdir(parents=True)
    ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', ROOT / 'current_context')
    cases = []
    for kind in [2, 3]:
        for previous in [0, 1, 2, 3, 0xFFFFFFFF]:
            for value in [0, 1, 2, 3, 0xFFFFFFFF]:
                cases.append(ctx.execute(forward, kind, value, previous))
                ctx.machines.pop()
    assert len(cases) == 50 and not ctx.machines
    by_offset = {r['offset']: r for r in control['source_relative_cases']}
    path_cases = []
    for event30 in [0, 1]:
        for raw_value in [0, 1, 2, 3, 0xFFFFFFFF]:
            offset, last, trace, speeches = 230, 0, [], [12, 106, 132]
            while offset != 334:
                trace.append(offset)
                if offset in [230, 242]:
                    last = event30 if offset == 230 else raw_value
                    offset += 4 if offset == 230 else 8
                elif offset in by_offset:
                    offset = next(c['next_offset'] for c in by_offset[offset]['cases'] if c['previous_result_structural_argument'] == last)
                elif offset in [262, 294]:
                    speeches.append(offset)
                    offset += 28 if offset == 262 else 24
                elif offset == 318:
                    offset += 8
                else:
                    raise AssertionError(offset)
                assert len(trace) < 25
            assert speeches == ([12, 106, 132] if event30 else [12, 106, 132] + ([262] if raw_value == 1 else []) + [294])
            path_cases.append(dict(event30_boolean_argument=event30, raw_predicate_argument=raw_value,
                source_command_offsets=trace + [334, 336], source_speech_headers=speeches,
                structural_composition_not_actual_complete_script_orouter_selection=True))
    queries = control['source_raw_query_cases']
    assert [q['native_result'] for q in queries] == [[2, 0, 0, 0, 0, 0], [2, 0, 0, 0, 0, 0]]
    save(ROOT / 'result_flow.json', dict(candidate=inp['current_ROM'], candidate_sha256=inp['current_ROM_sha256'],
        current_native_input=str(INPUT), current_native_input_sha256=sha(INPUT.read_bytes()), source_controls=str(CONTROL), source_controls_sha256=sha(CONTROL.read_bytes()),
        original_caller_span=dict(start=start, end=end, sha256=sha(arm[start:end])), original_caller_instructions=instructions,
        original_parser_r3_receives_carried_value_word=True, result_kind2_updates_from_second_word_result_kind3_preserves_previous=True,
        caller_fragment_cases=cases, source_structural_paths=path_cases,
        conditional_context='If event30 is complete, the initial three speeches skip the later reactions. Otherwise the raw predicate controls only Charles: the echo is included for value1. Gerhard follows on that event30-incomplete branch, including after Charles when that echo is selected. These are composed original structural rules, not naturally reached paths.',
        unforced_snapshot_query_results=queries,
        no_predicate_event_flag_actor_role_RNG_inventory_orinput_forced_in_gameplay=True,
        no_full_script_effect_UI_outer_eligibility_chronology_original_location_oractual_activation_claim=True,
        native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0, new_emulator_runs=0, full_goal_complete=False,
        evidence={str(p): sha(p.read_bytes()) for p in [INPUT, CONTROL, Path(__file__)]}))
    print('B51 original caller: fifty guarded result-channel cases; ten composed structural paths. Event30 and raw query stay distinct. No gameplay predicate forced or actual path claimed.')
