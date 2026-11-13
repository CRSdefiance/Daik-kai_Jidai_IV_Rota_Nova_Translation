"""Broader SDK file-open census and real generated-FLS filename construction.

Only the SDK open result is bridged. Valid movie cases stop before decoding or
playback; no raw-comic viewer, GPU crop or globally unused archive is inferred.
"""

import json
import re
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.research_archive_callers_v264 import OPEN, census

ROOT = Path('work/analysis/graphics_file_open_v301')
ROM = Path('out/all_routes_combined_v299_candidate.nds')
DIGEST = '9f551e849f7cb8fbabee2bb4e9586fb527789c4b8a0ed97c084a21adaa49768f'
MOVIE, AFTER_OPEN = BASE + 0xD2B1C, BASE + 0xD2BA0


def scan(rom, arm, targets):
    # Scope the existing scanner's target set to this single fresh invocation.
    import scripts.research_archive_callers_v264 as previous

    old = previous.TARGETS
    try:
        previous.TARGETS = set(targets)
        return census(rom, arm)
    finally:
        previous.TARGETS = old


def resolve(rom, requested):
    name = '/' + requested.replace('\\', '/').lstrip('/')
    matches = [p for p in rom.path_map() if p.casefold() == name.casefold()]
    if len(matches) > 1:
        raise ValueError('Ambiguous filesystem spelling')
    return matches[0] if matches else None


def generated(rom, arm, index):
    cpu = machine(arm)
    saved = {r: 0xA1000000 + r for r in (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6,
                                       UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9)}
    for reg, value in saved.items():
        cpu.reg_write(reg, value)
    cpu.reg_write(UC_ARM_REG_R0, index)
    cpu.reg_write(UC_ARM_REG_R1, 0)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.mem_write(STACK - 0x1000, b'\xA5' * 0x1020)
    events = []
    stack_writes = []

    def observe_write(uc, access, address, size, value, _):
        # Native sprintf and SDK construction have their own nested stack frames.
        if STACK - 0x1000 <= address < STACK + 32:
            assert address + size <= STACK
            stack_writes.append([address, size, uc.reg_read(UC_ARM_REG_PC)])

    def bridge(uc, address, size, _):
        if address != OPEN:
            return
        owner, pointer = uc.reg_read(UC_ARM_REG_R0), uc.reg_read(UC_ARM_REG_R1)
        assert pointer == STACK - 0xA0 and owner == pointer + 0x40
        requested = bytes(uc.mem_read(pointer, 64)).split(b'\0', 1)[0].decode('ascii')
        path = resolve(rom, requested)
        events.append({'requested': requested, 'actual_path': path,
                       'file_sha256': sha(rom.read_file(path)) if path else None,
                       'native_stack_filename_and_constructor_owner': [pointer, owner]})
        uc.reg_write(UC_ARM_REG_R0, int(path is not None))
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    cpu.hook_add(UC_HOOK_CODE, bridge)
    cpu.hook_add(UC_HOOK_MEM_WRITE, observe_write)
    valid = index == 0 or 20 <= index <= 32
    cpu.emu_start(MOVIE, AFTER_OPEN if valid else STOP, count=30000)
    assert cpu.reg_read(UC_ARM_REG_PC) == (AFTER_OPEN if valid else STOP)
    assert bytes(cpu.mem_read(STACK - 0x1000, 0x800)) == b'\xA5' * 0x800
    assert bytes(cpu.mem_read(STACK, 32)) == b'\xA5' * 32
    if valid:
        expected = 'FLS\\logo.fls' if index == 0 else f'FLS\\M{index:02d}.fls'
        assert len(events) == 1 and events[0]['requested'] == expected and events[0]['actual_path']
        assert cpu.reg_read(UC_ARM_REG_SP) == STACK - 0xA0
    else:
        assert cpu.reg_read(UC_ARM_REG_SP) == STACK
        assert all(cpu.reg_read(reg) == value for reg, value in saved.items())
        assert len(events) == (1 if index == 33 else 0)
        assert cpu.reg_read(UC_ARM_REG_R0) == (1 if index == 33 else 0)
    return {'index': index, 'SDK_open_events': events, 'valid_FLS_stopped_before_decoder': valid,
            'invalid_or_missing_case_native_return_ABI_pass': not valid,
            'native_stack_filename_and_outer_memory_guards_pass': True,
            'lowest_native_nested_stack_write': min(a for a, _, _ in stack_writes),
            'nested_stack_write_count': len(stack_writes)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert sha(ROM.read_bytes()) == DIGEST
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    manifest = json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert manifest['candidate_sha256'] == DIGEST
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    sdk = scan(rom, arm, (OPEN,))
    calls = sdk['aligned_ARM_BL_calls']
    assert len(calls) == 25 and not sdk['Thumb_calls'] and not sdk['literal_pointers']
    cs, constant, dynamic = Cs(CS_ARCH_ARM, CS_MODE_ARM), [], []
    for row in calls:
        assert row['unit'] == 'main-0'
        at = row['address'] - BASE
        context = list(cs.disasm(arm[at - 16:at + 4], row['address'] - 16))
        literal = next((i for i in reversed(context[:-1]) if i.mnemonic == 'ldr' and re.fullmatch(r'r1, \[pc, #[^\]]+\]', i.op_str)), None)
        record = {**row, 'context': [{'address': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str} for i in context],
                  'caller_context_bytes_exact_clean': arm[at - 16:at + 4] == original[at - 16:at + 4]}
        assert record['caller_context_bytes_exact_clean']
        if literal:
            delta = int(literal.op_str.split('#')[1][:-1], 0)
            pointer_field = literal.address + 8 + delta
            pointer = struct.unpack_from('<I', arm, pointer_field - BASE)[0]
            assert BASE <= pointer < BASE + len(arm)
            raw = arm[pointer - BASE:].split(b'\0', 1)[0]
            assert 0 < len(raw) < 64
            requested = raw.decode('ascii')
            path = resolve(rom, requested)
            assert path is not None
            record.update(requested=requested, actual_path=path, string_pointer=pointer,
                          pointer_field=pointer_field, file_sha256=sha(rom.read_file(path)))
            constant.append(record)
        else:
            dynamic.append(record)
    assert len(constant) == 20 and len(dynamic) == 5
    movie_calls = scan(rom, arm, (MOVIE,))
    assert len(movie_calls['aligned_ARM_BL_calls']) == 6 and not movie_calls['literal_pointers'] and not movie_calls['Thumb_calls']
    for row in movie_calls['aligned_ARM_BL_calls']:
        at = row['address'] - BASE
        row['argument_setup'] = [{'address': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str}
                                 for i in cs.disasm(arm[at - 20:at + 4], row['address'] - 20)]
        assert arm[at - 20:at + 4] == original[at - 20:at + 4]
    assert arm[0xD2B1C:0xD2BAC + 4] == original[0xD2B1C:0xD2BAC + 4]
    cases = [generated(rom, arm, index) for index in [0, *range(20, 33), *range(1, 20), 33, 0xFFFFFFFF]]
    available = {event['actual_path'] for row in cases for event in row['SDK_open_events'] if event['actual_path']}
    expected = {p for _, p, _ in rom.iter_files() if p.casefold().startswith('/fls/') and p.casefold().endswith('.fls')}
    assert available == expected and len(available) == 14
    whole_file = scan(rom, arm, (BASE + 0xB7158,))
    source_only = {'/GRP/CMMNIMG.DK4', '/GRP/SLACKIMG.DK4'}
    proof = {'format': 'dk4-native-sdk-graphics-file-open-census-v301', 'candidate': str(ROM), 'candidate_sha256': DIGEST,
             'current_manifest_and_registry_verified': True, 'SDK_scan': sdk,
             'constant_filename_cases': constant, 'caller_supplied_filename_cases': dynamic,
             'generated_FLS_parent_scan': movie_calls, 'generated_FLS_native_cases': cases,
             'all14_available_FLS_family_paths_constructed_by_original_native_code': sorted(available),
             'root_m02_03_FLS_not_part_of_generated_family': '/m02_03.fls',
             'generic_whole_file_reader_caller_scan': whole_file,
             'legacy_archive_literal_matches_in_20_constant_SDK_callers': [r for r in constant if r['actual_path'] in source_only],
             'no_claim_that_generic_callers_or_computed_paths_cannot_open_legacy_archives': True,
             'FLS_playback_decoder_GPU_and_raw_comic_native_viewer_unproved': True,
             'SDK_existence_result_is_only_instruction_bridge': True,
             'valid_FLS_parent_return_and_full_loader_not_claimed': True,
             'all11_legacy_native_layout_and_composition_gates_remain_open': True,
             'all18_plaque_hint_entries_remain_incomplete': True, 'ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('25 SDK-open callers:20 constant/5 supplied; six FLS parent callers;14 native FLS filenames;21 rejection/missing cases.')


if __name__ == '__main__':
    main()
