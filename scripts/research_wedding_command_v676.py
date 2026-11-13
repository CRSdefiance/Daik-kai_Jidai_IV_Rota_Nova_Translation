"""Trace original CS command extents and the separate chapter-movie selector.

The linear extent walk bridges opaque scene/gameplay effects and does not claim
runtime branch reachability. The selector cases bridge only movie playback and
scene reset, and run the complete original command with saved-register ABI.
"""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UcError
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/wedding_movie_v676')
OWNER, STREAM, RESULT, LENGTH = 0x02460000, 0x02470000, 0x02468000, 0x02468040
REGS = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)


def walk(arm, block):
    u = machine(arm)
    u.mem_write(OWNER, bytes(32))
    u.mem_write(STREAM - 16, b'\xA5' * (len(block) + 32))
    u.mem_write(STREAM, block)
    offset, rows, bridges, calls = 8, [], [], []
    limit = 8 + struct.unpack_from('<H', block, 4)[0]
    assert block[:4] == b'CS\0\1' and limit <= len(block) and not any(block[limit:])

    def effect(cpu, pc, size, unused):
        if 0x020293B8 <= pc < 0x0202A600 or 0x02028A28 <= pc < 0x02028A64:
            return
        lr = cpu.reg_read(UC_ARM_REG_LR)
        assert (0x020293B8 <= lr < 0x0202A600 or 0x02028A28 <= lr < 0x02028A64), (pc, lr)
        args = [cpu.reg_read(reg) for reg in REGS]
        bridges.append({'source_offset': offset, 'PC': pc, 'LR': lr, 'args': args, 'opaque_result': 0})
        if pc == 0x020D2B1C:
            calls.append({'source_offset': offset, 'args': args})
        cpu.reg_write(UC_ARM_REG_R0, 0)
        cpu.reg_write(UC_ARM_REG_PC, lr)

    h = u.hook_add(UC_HOOK_CODE, effect)
    error = None
    try:
        while offset < limit:
            assert len(rows) < 5000
            u.mem_write(OWNER + 4, struct.pack('<I', STREAM + offset))
            u.mem_write(RESULT, bytes(48))
            u.mem_write(LENGTH, bytes(4))
            call(u, 0x2A510, (RESULT, OWNER, LENGTH), instruction_limit=20000)
            length = struct.unpack('<I', u.mem_read(LENGTH, 4))[0]
            assert length >= 2 and length % 2 == 0 and offset + length <= limit, (offset, length, limit)
            rows.append({'offset': offset, 'word': struct.unpack_from('<H', block, offset)[0],
                         'native_extent': length, 'result': bytes(u.mem_read(RESULT, 24)).hex()})
            offset += length
        assert bytes(u.mem_read(STREAM, len(block))) == block
        assert bytes(u.mem_read(STREAM - 16, 16)) == bytes(u.mem_read(STREAM + len(block), 16)) == b'\xA5' * 16
    except (AssertionError, ValueError, UcError) as exc:
        error = repr(exc)
    finally:
        u.hook_del(h)
    return {'rows': rows, 'stopped_offset': offset, 'logical_end': limit, 'error': error,
            'opaque_effect_bridges': bridges, 'native_movie_requests': calls,
            'linear_native_extents_not_runtime_branch_reachability': True}


def selector(arm):
    u, cases, requests, effects = machine(arm), [], [], []
    # LDR at A0F8 uses PC+8+44, i.e. A144 (not adjacent A140).
    assert bytes(u.mem_read(0x0202A0F8, 4)) == bytes.fromhex('44009fe5')
    scene = struct.unpack('<I', u.mem_read(0x0202A144, 4))[0]
    assert scene == 0x02276F88

    def bridge(cpu, pc, size, unused):
        if pc not in (0x020D2B1C, 0x02021C14):
            return
        args = [cpu.reg_read(reg) for reg in REGS]
        (requests if pc == 0x020D2B1C else effects).append({'PC': pc, 'args': args})
        cpu.reg_write(UC_ARM_REG_R0, 0)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    h = u.hook_add(UC_HOOK_CODE, bridge)
    try:
        for low in range(256):
            requests.clear()
            effects.clear()
            u.mem_write(OWNER, bytes(32))
            u.mem_write(OWNER + 4, struct.pack('<I', STREAM))
            u.mem_write(STREAM - 16, b'\xA5' * 34)
            word = struct.pack('<H', 0x4900 | low)
            u.mem_write(STREAM, word)
            u.mem_write(LENGTH - 16, b'\xA5' * 36)
            u.mem_write(LENGTH, bytes(4))
            u.mem_write(RESULT - 16, b'\xA5' * 80)
            u.mem_write(scene + 0x24B8, bytes(8))
            executed = call(u, 0x2A510, (RESULT, OWNER, LENGTH))
            assert requests == [{'PC': 0x020D2B1C, 'args': [20 + low, 0, 1, 0]}]
            assert len(effects) == 1 and effects[0]['args'][:2] == [scene, 1]
            assert bytes(u.mem_read(scene + 0x24B8, 8)) == struct.pack('<2I', 1, 1)
            assert bytes(u.mem_read(RESULT, 4)) == struct.pack('<I', 3)
            assert bytes(u.mem_read(LENGTH, 4)) == struct.pack('<I', 2)
            assert bytes(u.mem_read(STREAM, 2)) == word
            for address in (STREAM - 16, STREAM + 2, RESULT - 16, RESULT + 4, LENGTH - 16, LENGTH + 4):
                assert bytes(u.mem_read(address, 16)) == b'\xA5' * 16
            assert {0x0202A510, 0x02029AA0, 0x0202A0F8, 0x02028A28} <= executed
            cases.append({'word': 0x4900 | low, 'movie_args': requests[0]['args'],
                          'whole_original_command_ABI_and_stream_result_length_guards_exact': True})
    finally:
        u.hook_del(h)
    return cases


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    results, selectors = {}, {}
    for label, path in (('current', pre['candidate']), ('clean', 'work/clean.nds')):
        rom = NdsImage.open(path)
        block = IlnkContainer.parse(rom.read_file('/data/SC2.DK4')).blocks[70]
        result = walk(rom.read_file('/__arm9__.bin'), block)
        results[label] = {'source_sha256': sha(block), **result}
        save(ROOT / 'native_extent_research.json', results)
        print(label, 'extent rows', len(result['rows']), 'stop', result['stopped_offset'],
              'error', result['error'], 'movies', result['native_movie_requests'], flush=True)
        selectors[label] = selector(rom.read_file('/__arm9__.bin'))
        save(ROOT / 'chapter_selector_cases.json', selectors)
    assert selectors['current'] == selectors['clean']
    print('V676512 complete original chapter-movie command cases match clean/current.', flush=True)


if __name__ == '__main__':
    main()
