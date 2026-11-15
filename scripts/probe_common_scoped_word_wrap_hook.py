"""Serialize a scoped ID83 macro-pass/word-wrap hook as research ARM9."""

import json
import struct
from pathlib import Path

import ndspy.code
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_map_entity_tooltip_copy import BASE, STACK, STOP, machine_for
from scripts.probe_common_display_name_autoload import execute as autoload
from scripts.probe_common_display_name_hook import ARENA_LO_LITERAL, OVERLAY, branch_link
from scripts.probe_common_display_name_hook import prepare as name_hook
from scripts.probe_common_native_word_wrap import helper_bytes
from scripts.probe_common_tribute_guarded_wrap import wrap_expanded
from scripts.probe_common_tribute_loaded_copy import execute as loaded_copy
from scripts.probe_common_tribute_loaded_copy import research_dataset
from scripts.probe_common_tribute_modal_pixels import verify as pixels

MACRO_CALL = 0x54798
TEXT = 0x0242D000


def check_scope(source, parent_return, message_id, text):
    resident = ndspy.code.MainCodeFile(source, BASE).sections[1]
    destination = struct.unpack_from('<I', source, 0x54894)[0]

    def run(hooked):
        machine = machine_for(source)
        machine.mem_map(0x01FF8000, 0x8000)
        machine.mem_write(resident.ramAddress, bytes(resident.data))
        raw = text.encode('cp932') + b'\0'
        machine.mem_write(TEXT, raw)
        machine.mem_write(destination, b'\xa5' * 256)
        machine.mem_write(STACK + 0xC4, struct.pack('<I', parent_return))
        machine.mem_write(STACK + 0xD0, struct.pack('<I', message_id))
        for register, value in ((UC_ARM_REG_R0, destination), (UC_ARM_REG_R1, TEXT), (UC_ARM_REG_R2, 0)):
            machine.reg_write(register, value)
        executed = set()

        def code(uc, address, size, _):
            executed.add(address)

        machine.hook_add(UC_HOOK_CODE, code)
        end = BASE + MACRO_CALL + 4 if hooked else STOP
        machine.emu_start(BASE + MACRO_CALL if hooked else BASE + 0x53914, end, count=20000)
        if machine.reg_read(UC_ARM_REG_PC) != end or machine.reg_read(UC_ARM_REG_SP) != STACK:
            raise ValueError('Scope probe changes caller return or stack')
        result = bytes(machine.mem_read(destination, 256)).split(b'\0', 1)[0]
        if bytes(machine.mem_read(TEXT, len(raw))) != raw or BASE + 0x53914 not in executed:
            raise ValueError('Scope probe changes input or bypasses original macro expansion')
        return result, 0x01FF9BC8 in executed

    original, _ = run(False)
    candidate, invoked = run(True)
    active = parent_return == BASE + 0x546E8 and message_id == 83
    expected = wrap_expanded(original.decode('cp932')).encode('cp932') if active else original
    if candidate != expected or invoked != active:
        raise ValueError('Scoped wrapper changes an unrelated modal path or misses ID83')
    return {'parent_return': parent_return, 'message_id': message_id, 'input': text,
            'original_expansion': original.decode('cp932'), 'candidate': candidate.decode('cp932'),
            'word_wrapper_invoked': invoked, 'original_macro_expander_executed': True}


def wrapper_bytes(address, helper_address, *, monthly=False):
    words, branches, literal_loads = [], [], []

    def emit(word):
        words.append(word)

    def literal(rd, value):
        literal_loads.append((len(words), rd, value))
        emit(0)

    def done_branch():
        branches.append(len(words))
        emit(0)

    emit(0xE92D4070)  # push r4-r6,lr
    emit(0xE24DD0F0)  # 240-byte bounded scratch output
    emit(0xE1A04000)  # preserve expanded output pointer
    emit(branch_link(address + len(words) * 4, BASE + 0x53914))
    # Original modal frame begins 256 bytes above this wrapper's scratch.
    # Its saved LR is +C4; general native-ID wrapper's original r0 is +D0.
    emit(0xE59D0364 if monthly else 0xE59D01C4)
    literal(5, BASE + (0x53F40 if monthly else 0x546E8))
    emit(0xE1500005)
    done_branch()
    emit(0xE59D0374 if monthly else 0xE59D01D0)
    if monthly:
        literal(5, BASE + 0x1189C0)
        emit(0xE1500005)
    else:
        emit(0xE3500053)
    done_branch()
    emit(0xE1A00004)
    emit(0xE1A0100D)
    emit(branch_link(address + len(words) * 4, helper_address))
    emit(0xE3500000)
    emit(0)  # beq done on rejected input; no partial buffer is committed
    rejected_at = len(words) - 1
    emit(0xE2802001)  # length includes NUL for the native memcpy
    emit(0xE1A00004)
    emit(0xE1A0100D)
    emit(branch_link(address + len(words) * 4, BASE + 0xCEC74))
    done = len(words)
    emit(0xE3A00000)
    emit(0xE28DD0F0)
    emit(0xE8BD8070)
    for at in branches:
        words[at] = 0x1A000000 | ((done - at - 2) & 0xFFFFFF)
    words[rejected_at] = 0x0A000000 | ((done - rejected_at - 2) & 0xFFFFFF)
    for at, rd, value in literal_loads:
        pool_at = len(words)
        words.append(value)
        words[at] = 0xE59F0000 | rd << 12 | (pool_at - at - 2) * 4
    return struct.pack(f'<{len(words)}I', *words)


def prepare(source):
    named, _ = name_hook(source)
    code = ndspy.code.MainCodeFile(named, BASE)
    resident = code.sections[1]
    previous = [bytes(section.data) for section in code.sections]
    helper_address = resident.ramAddress + len(resident.data)
    helper = helper_bytes()
    wrapper_address = helper_address + len(helper)
    extra = helper + wrapper_bytes(wrapper_address, helper_address)
    if wrapper_address + len(extra) - len(helper) > OVERLAY:
        raise ValueError('Scoped word-wrap payload overlaps the native overlay')
    if struct.unpack_from('<I', code.sections[0].data, MACRO_CALL)[0] != branch_link(BASE + MACRO_CALL, BASE + 0x53914):
        raise ValueError('Original modal macro call differs')
    resident.data.extend(extra)
    arena_low = (resident.ramAddress + len(resident.data) + 31) & ~31
    struct.pack_into('<I', code.sections[0].data, ARENA_LO_LITERAL, arena_low)
    struct.pack_into('<I', code.sections[0].data, MACRO_CALL,
                     branch_link(BASE + MACRO_CALL, wrapper_address))
    saved = bytes(code.save())
    loaded = ndspy.code.MainCodeFile(saved, BASE)
    expected = bytearray(previous[0])
    struct.pack_into('<I', expected, ARENA_LO_LITERAL, arena_low)
    struct.pack_into('<I', expected, MACRO_CALL, branch_link(BASE + MACRO_CALL, wrapper_address))
    for at in (code.codeSettingsOffs, code.codeSettingsOffs + 4):
        struct.pack_into('<I', expected, at, struct.unpack_from('<I', previous[0], at)[0] + len(extra))
    if (bytes(loaded.sections[0].data) != expected
            or bytes(loaded.sections[1].data) != previous[1] + extra
            or bytes(loaded.sections[2].data) != previous[2]):
        raise ValueError('Scoped hook serialization changes unrelated code/data')
    return saved, {'helper_address': helper_address, 'wrapper_address': wrapper_address,
                   'new_payload_bytes': len(extra), 'total_payload_bytes': len(resident.data) - 6944,
                   'reserved_arena_low': arena_low}


def main():
    source = NdsImage.open('out/all_routes_combined_v142_candidate.nds').read_file('/__arm9__.bin')
    saved, placement = prepare(source)
    dataset = research_dataset(saved)
    names = (b'Fleet', b'Indigo', b'F' * 18, b'I' * 18, 'あ'.encode('cp932') * 9, b'Fleet  Group')
    cases = [loaded_copy(dataset.arm9, dataset.common, name, index, word_wrapped=True)
             for name in names for index in (0, 1, 30, 31)]
    cold = [loaded_copy(dataset.arm9, dataset.common, name, index, word_wrapped=True, cold_cache=True)
            for name in names for index in (0, 31)]
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    font = rom.read_file('/GRP/KANJI.FNT')
    unique = list(dict.fromkeys(case['complete_prepared_text'] for case in cases))
    rendered = [{'text': text, 'mode': mode,
                 'pixels_sha256': sha(pixels(source, font, text, mode, guarded=True)['pixels'])}
                for text in unique for mode in (4, 16)]
    scope = [check_scope(saved, parent, message, text)
             for parent, message in ((BASE + 0x546E8, 83), (BASE + 0x546E8, 82),
                                     (BASE + 0x5469C, 83), (BASE + 0x54720, 83))
             for text in ('This notice contains several complete words and ８８４６２９ gold coins.',
                          'I? says hello.')]
    proof = {'status': 'pass-scoped-word-wrap-hook-native-caller-loader-preparation-and-pixels',
             'source_arm9_sha256': sha(source), 'research_arm9_sha256': sha(saved),
             'placement': placement, 'native_autoload': autoload(saved),
             'cases': cases, 'native_modal_pixels': rendered,
             'cold_cache_cases_with_host_file_contract': cold,
             'scope_checks': scope,
             'scope': 'Saved parent LR 020546E8 and native ID83 in original modal frame. All paths run original 53914 macro expansion first.',
             'limitations': 'Research ARM9 only; actual cache preparation and unchanged renderer connect across separate invocations. Cold-cache native ILNK logic executes with host D0398 open/D0170 read contracts; physical SDK filesystem I/O, hardware cache/physical composition/input and monthly actor windows remain pending.'}
    Path('work/analysis/common_scoped_word_wrap_arm9.bin').write_bytes(saved)
    Path('work/analysis/common_scoped_word_wrap_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'{len(cases)} scoped native caller/loader/word-wrap cases and {len(rendered)} pixel cases pass; ITCM extension {placement["total_payload_bytes"]} bytes.')


if __name__ == '__main__':
    main()
