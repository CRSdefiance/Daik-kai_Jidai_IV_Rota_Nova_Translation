"""Resolve all11 generic-wrapper argument setups without declaring legacy art unused."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R9

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v474_candidate.nds')
ROOT = Path('work/analysis/generic_file_arguments_v478')
SNAPSHOT = Path('work/emulation_v193/weapon_reload_v477/final_arm9_ram.bin')


def cstring(u, pointer):
    return bytes(u.mem_read(pointer, 128)).split(b'\0')[0].decode('cp932')


def direct_calls(arm, target):
    main = bytes(MainCodeFile(arm, 0x02000000).sections[0].data)
    calls = []
    for offset in range(0, len(main) - 3, 4):
        word = struct.unpack_from('<I', main, offset)[0]
        if word & 0x0F000000 != 0x0B000000:
            continue
        delta = word & 0xFFFFFF
        if delta & 0x800000:
            delta -= 0x1000000
        if 0x02000000 + offset + 8 + delta * 4 == target:
            calls.append(0x02000000 + offset)
    return calls


def slack_selector_domain(arm):
    u = machine(arm)
    u.emu_start(0x0209ED3C, 0x0209ED40, count=1)
    assert u.reg_read(UC_ARM_REG_R9) == 0
    selections = []
    # Execute the original selector arithmetic and loop-control instructions.
    # Loader, actor calls and complete UI construction are not simulated here.
    def stop(uc, address, size, data):
        if address == 0x0209EDA8:
            uc.emu_stop()

    hook = u.hook_add(UC_HOOK_CODE, stop)
    try:
        for expected in range(14, 18):
            u.emu_start(0x0209EDDC, 0x0209EDE0, count=1)
            assert u.reg_read(UC_ARM_REG_R0) == expected
            u.emu_start(0x0209EE80, 0x0209EE94, count=8)
            pc = u.reg_read(UC_ARM_REG_PC)
            assert pc == (0x0209EDA8 if expected < 17 else 0x0209EE94)
            selections.append({'block': expected, 'native_loop_tail_destination': pc})
    finally:
        u.hook_del(hook)
    return {'original_seed_and_four_selector_tail_cases': selections,
            'scope': 'Original scalar selector/loop control only;no complete controller,loader or gameplay display credit.'}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    ranges = [(0x23AC0, 0x23AD0), (0xD0398, 0xD051C)]
    assert all(arm[a:b] == original[a:b] for a, b in ranges)
    u = machine(arm)
    raw = SNAPSHOT.read_bytes()
    u.mem_write(0x02000000, raw)
    routes = []
    for index in range(4):
        call(u, 0x23AC0, (index,))
        path = cstring(u, u.reg_read(UC_ARM_REG_R0))
        assert path == f'/data/EV{index}.DK4'
        assert rom.read_file(path) == clean.read_file(path)
        routes.append({'selector': index, 'path': path, 'file_sha256': sha(rom.read_file(path))})
    fixed = []
    for caller, literal, path in [(0x02047A3C, 0x47AD4, '/GRP/CMMNIMG.000'),
                                  (0x02047B3C, 0x47C44, '/GRP/CMMNIMG.000'),
                                  (0x0204BB00, 0x4BC70, '/GRP/TITLEMAP.DK4'),
                                  (0x020D1A6C, 0xD1A9C, '/GRP/KANJI.FNT')]:
        pointer = struct.unpack_from('<I', arm, literal)[0]
        actual = cstring(u, pointer).replace('\\', '/')
        assert actual == path
        fixed.append({'call': caller, 'filename_literal_word': literal,
                      'filename_pointer': pointer, 'actual_filename': actual,
                      'file_sha256': sha(rom.read_file(actual))})
    dynamic = []
    for caller, literal in [(0x02047888, 0x478C8), (0x02047BA0, 0x47C50)]:
        owner = struct.unpack_from('<I', arm, literal)[0]
        pointer = struct.unpack('<I', u.mem_read(owner + 12, 4))[0]
        actual = cstring(u, pointer)
        assert actual == '_pxl/item.pxl'
        dynamic.append({'call': caller, 'owner_pointer_literal': literal, 'captured_owner': owner,
                        'filename_field_offset': 12, 'captured_filename': actual,
                        'current_file_sha256': sha(rom.read_file('/' + actual)),
                        'other_owner_filenames_in_other_states_not_excluded': True})
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    modes = []
    native = machine(arm)
    owner = 0x02460020
    for mode in (1, 2, 3):
        native.mem_write(owner - 16, b'\xA5' * 80)
        call(native, 0xD05D0, (owner,))
        trace = call(native, 0xD0398, (owner, 0x0213BA94, mode))
        result = native.reg_read(UC_ARM_REG_R0)
        assert result == (0 if mode == 3 else 1)
        assert 0x020DED50 not in trace
        assert bytes(native.mem_read(owner - 16, 16)) == b'\xA5' * 16
        assert bytes(native.mem_read(owner + 0x28, 24)) == b'\xA5' * 24
        modes.append({'mode': mode, 'return': result, 'SDK_file_open_not_executed': True,
                      'full_native_return_stack_saved_registers_and_owner_canaries_pass': True,
                      'executed_native_addresses': sorted(trace)})
    callers = [0x02023458, 0x02023A80, 0x02046494, 0x020466B8, 0x02047888,
               0x02047A3C, 0x02047B3C, 0x02047BA0, 0x0204BB00, 0x020D1A6C, 0x020D2024]
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    contexts = []
    for caller in callers:
        off = caller - 0x02000000
        assert arm[off - 44:off + 12] == original[off - 44:off + 12]
        contexts.append({'call': caller, 'source_exact_argument_instructions': [
            {'address': i.address, 'assembly': i.mnemonic + ' ' + i.op_str}
            for i in cs.disasm(arm[off - 44:off + 12], caller - 44)]})
    archive_calls = direct_calls(arm, 0x020D2018)
    assert archive_calls == [0x0200972C, 0x020097A8, 0x02024170, 0x02047074,
                             0x02053544, 0x0206E59C, 0x0207CE3C]
    archives = []
    for caller, literal, expected in [(0x0200972C, 0x9770, '/GRP/CHARA.DK4'),
                                      (0x020097A8, 0x9800, '/GRP/CHARA.DK4'),
                                      (0x02047074, 0x470B0, '/GRP/SLACKIMG.DK4'),
                                      (0x02053544, 0x535D0, '/COMMON/MESFILE.DK4'),
                                      (0x0206E59C, 0x6E5D8, '/DATA/WORLDMAP.DK4'),
                                      (0x0207CE3C, 0x7D068, '/COMMON/HELP.DK4')]:
        pointer = struct.unpack_from('<I', arm, literal)[0]
        path = cstring(u, pointer).replace('\\', '/')
        assert path == expected and arm[literal:literal + 4] == original[literal:literal + 4]
        archives.append({'call': caller, 'filename_pointer_word': literal, 'original_filename': path})
    route_paths = []
    for index in range(4):
        pointer = struct.unpack_from('<I', arm, 0x134580 + index * 4)[0]
        path = cstring(u, pointer).replace('\\', '/')
        assert path == f'/DATA/SC{index}.DK4'
        route_paths.append(path)
    assert direct_calls(arm, 0x0204704C) == [0x0209EDE8]
    assert arm[0x9ED3C:0x9EE94] == original[0x9ED3C:0x9EE94]
    domain = slack_selector_domain(arm)
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()), 'ROM_changed': False,
             'source_exact_ranges': ranges, 'all11_original_direct_caller_argument_contexts': contexts,
             'two_EV_callers_filename_selector': {'calls': callers[:2], 'four_complete_native_selectors': routes},
             'four_fixed_disk_filename_calls': fixed, 'two_owner_supplied_filename_calls': dynamic,
             'two_non_disk_calls': {'calls': [0x02046494, 0x020466B8], 'modes': [1, 2], 'full_native_mode_tests': modes},
             'forwarding_archive_open_call': {'call': 0x020D2024, 'entry': 0x020D2018,
                                              'filename_argument_remains_caller_supplied': True},
             'all7_aligned_main_ARM_archive_open_calls': archive_calls,
             'six_fixed_archive_name_bindings': archives,
             'route_archive_table_binding': {'call': 0x02024170, 'four_original_paths': route_paths},
             'only_aligned_main_direct_SLACK_helper_call': 0x0209EDE8,
             'original_direct_SLACK_selector_domain': domain,
             'raw_comic_block19_not_selected_by_this_four_portrait_loop': True,
             'actual_runtime_snapshot': str(SNAPSHOT), 'snapshot_sha256': sha(raw), 'captured_RAM_unchanged': True,
             'CMMNIMG_000_not_confused_with_legacy_CMMNIMG_DK4': True,
             'no_actual_raw_comic_or_legacy_display_credit': True, 'no_global_unused_file_claim': True,
             'next_remaining_consumer_work': 'Trace caller-supplied archive owners and later/indirect paths;these11 generic calls alone do not identify the legacy comic display.',
             'all22_historical_requirements_retained': True, 'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'argument_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('All11 generic filename setups classified;4 EV getters and3 original non-disk mode returns pass;legacy display remains open.')


if __name__ == '__main__':
    main()
