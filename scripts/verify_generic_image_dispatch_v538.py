"""Connected original image instruction, widget setup, cache and source view.

Operand streams are diagnostic inputs. Only SDK file I/O is bridged. Stop after
the real widget setup and before its frame wait; no GPU/route reachability claim.
"""

import json
import struct
from collections import Counter
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.research_online_loader_v190 import resource_call

ROM = Path('out/all_routes_combined_v534_candidate.nds')
SNAPSHOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ending_caller_v537_maria/frame_003000_arm9_ram.bin')
OUT = Path('work/analysis/generic_image_dispatch_v538')
BASE = 0x02000000
OWNER, STREAM, RESULT, LENGTH = 0x02470000, 0x02470100, 0x02470200, 0x02470220
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    digest = sha(ROM.read_bytes())
    assert digest == 'cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45'
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    ranges = [(0x2A510, 0x2A5C0), (0x29AA0, 0x29AF8), (0x29FFC, 0x2A0F8),
              (0x28A64, 0x28A8C), (0x28E14, 0x29094), (0x470B4, 0x47184)]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ranges)
    raw = SNAPSHOT.read_bytes()
    assert len(raw) == 0x400000
    u = machine(arm)
    handles, events, raw_reads, selections = {}, [], [], []

    def bridge(cpu, address, size, unused):
        if address == BASE + 0xE5650:
            raise ValueError('Original loader assertion')
        if address == BASE + 0x470B4:
            selections.append([cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1)])
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = cpu.reg_read(UC_ARM_REG_R0)
        arg1, arg2 = cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2)
        if address == OPEN:
            name = bytes(cpu.mem_read(arg1, 128)).split(b'\0')[0].decode('ascii')
            path = '/' + name.replace('\\', '/').lstrip('/')
            assert path.startswith('/_pxl/slackimg') and obj not in handles
            data = rom.read_file(path)
            handles[obj] = [path, data, 0]
            cpu.mem_write(obj + 0x20, struct.pack('<2I', 0, len(data)))
            events.append({'operation': 'open', 'path': path, 'sha256': sha(data)})
            result = 1
        elif address == READ:
            state = handles[obj]
            assert state[2] + arg2 <= len(state[1])
            cpu.mem_write(arg1, state[1][state[2]:state[2] + arg2])
            state[2] += arg2
            result = arg2
        elif address == SEEK:
            assert arg2 == 0 and 0 <= arg1 <= len(handles[obj][1])
            handles[obj][2] = arg1
            result = 1
        else:
            events.append({'operation': 'close', 'path': handles.pop(obj)[0]})
            result = 1
        cpu.reg_write(UC_ARM_REG_R0, result)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    def watch(cpu, access, address, size, value, unused):
        raw_reads.append([cpu.reg_read(UC_ARM_REG_PC), address, size])

    h1 = u.hook_add(UC_HOOK_CODE, bridge)
    h2 = u.hook_add(UC_HOOK_MEM_READ, watch, begin=0x02233040, end=0x0225303F)
    cases = []
    try:
        for short in (True, False):
            for index in range(256):
                u.mem_write(BASE, raw)
                events.clear()
                raw_reads.clear()
                selections.clear()
                source = struct.pack('<2H', 0x4800, (0x8300 if short else 0x0300) | index)
                if not short:
                    source += struct.pack('<2H', 0x0012, 0x0034)
                u.mem_write(OWNER - 16, b'\xA5' * 64)
                u.mem_write(OWNER, bytes(16))
                u.mem_write(OWNER + 4, struct.pack('<I', STREAM))
                u.mem_write(STREAM - 16, b'\xA5' * 48)
                u.mem_write(STREAM, source)
                u.mem_write(RESULT - 16, b'\xA5' * 80)
                u.mem_write(LENGTH, bytes(4))
                u.reg_write(UC_ARM_REG_R0, RESULT)
                u.reg_write(UC_ARM_REG_R1, OWNER)
                u.reg_write(UC_ARM_REG_R2, LENGTH)
                u.reg_write(UC_ARM_REG_SP, STACK)
                u.reg_write(UC_ARM_REG_LR, STOP)
                # Entire dispatch, descriptor decoding, real widget cleanup,
                # construction and image load execute in this one invocation.
                u.emu_start(BASE + 0x2A510, BASE + 0x28A74, count=200000)
                assert u.reg_read(UC_ARM_REG_PC) == BASE + 0x28A74
                assert struct.unpack('<I', u.mem_read(LENGTH, 4))[0] == len(source)
                assert selections == [[index, 0x02279458]]
                assert bytes(u.mem_read(STREAM, len(source))) == source
                assert bytes(u.mem_read(STREAM - 16, 16)) == b'\xA5' * 16
                assert bytes(u.mem_read(STREAM + len(source), 16)) == b'\xA5' * 16
                assert bytes(u.mem_read(OWNER + 4, 4)) == struct.pack('<I', STREAM)
                assert bytes(u.mem_read(OWNER - 16, 16)) == b'\xA5' * 16
                assert bytes(u.mem_read(RESULT - 16, 48)) == b'\xA5' * 48
                assert bytes(u.mem_read(LENGTH + 4, 28)) == b'\xA5' * 28
                assert not handles and not raw_reads
                selected = index if index <= 12 or index == 20 else (12 if index < 20 else 20)
                path = f'/_pxl/slackimg{selected:02d}.pxl'
                data = rom.read_file(path)
                pxl = PxlImage.from_bytes(data)
                view = struct.unpack('<12I', u.mem_read(0x02279458, 48))
                owner = struct.unpack('<I', u.mem_read(BASE + 0x115EA8 + min(index, 20) * 4, 4))[0]
                assert view[3] == owner and view[10:12] == (pxl.width, pxl.height)
                resource_call(u, 0xD4170, (0x02279458,))
                pointer = u.reg_read(UC_ARM_REG_R0)
                assert bytes(u.mem_read(pointer, len(data))) == data
                assert not handles and not raw_reads
                cases.append({'instruction_hex': source.hex(), 'short_form': short,
                              'instruction_length': len(source), 'index': index,
                              'path': path, 'file_sha256': sha(data),
                              'original_widget': 0x02279448, 'original_view': 0x02279458,
                              'native_view_fields': list(view), 'native_extent': [pxl.width, pxl.height],
                              'complete_header_palette_and_pixels_exact': True,
                              'whole_input_operands_and_neighbor_guards_exact': True,
                              'raw_SLACK_shared_buffer_reads': 0, 'SDK_open_close': list(events)})
            print(f'Connected {"four" if short else "eight"}-byte form: all256 index values pass.', flush=True)
    finally:
        u.hook_del(h1)
        u.hook_del(h2)

    (OUT / 'native_cases.json').write_text(json.dumps({
        'candidate_sha256': digest, 'snapshot_sha256': sha(raw), 'cases': cases,
        'source_script_sha256': sha(Path(__file__).read_bytes()),
    }, indent=2) + '\n', encoding='utf-8')

    scans = []
    for label, source_rom in [('clean', clean), ('current', rom)]:
        for prefix in ('SC', 'EV'):
            for route in range(4):
                path = f'/data/{prefix}{route}.DK4'
                data = source_rom.read_file(path)
                if prefix == 'SC':
                    blocks = IlnkContainer.parse(data).blocks
                    storage = 'ILNK blocks'
                else:
                    assert data[:2] == b'VE' and struct.unpack_from('<I', data, 4)[0] == len(data) - 96
                    blocks = [data]
                    storage = 'complete VE file; not decoded as an instruction stream'
                hits, positions = Counter(), 0
                for block in blocks:
                    for offset in range(len(block) - 3):
                        word, operand = struct.unpack_from('<2H', block, offset)
                        positions += 1
                        if word & 0xFF00 == 0x4800 and (operand >> 8) & 3 == 3:
                            hits[operand & 0xFF] += 1
                scans.append({'ROM': label, 'path': path, 'sha256': sha(data),
                              'storage': storage,
                              'blocks': len(blocks), 'byte_positions_checked': positions,
                              'image_patterns_not_decoded_instructions': dict(sorted(hits.items()))})
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'source_script_sha256': sha(Path(__file__).read_bytes()),
             'snapshot': str(SNAPSHOT), 'snapshot_sha256': sha(raw),
             'source_exact_code_ranges': ranges, 'connected_cases': cases, 'route_and_EV_scans': scans,
             'all512_original_instruction_widget_cache_view_cases_pass': True,
             'index13_through19_select_loose_name_labels_not_raw_archive_blocks': True,
             'index21_through255_select_original_press_button_fallback': True,
             'actual_RAM_parent_vtables_and_registered_owners_not_substituted': True,
             'SDK_filesystem_only_bridged': True, 'layout_flag_bits_tested': 0,
             'frame_wait_animation_GPU_or_live_instruction_reachability_proven': False,
             'positive_byte_patterns_are_candidates_not_real_instructions': True,
             'global_unused_raw_art_claim': False, 'ROM_modified': False,
             'all22_requirements_and18_incomplete_plaques_retained': True, 'full_goal_complete': False}
    assert sha(ROM.read_bytes()) == digest and SNAPSHOT.read_bytes() == raw
    (OUT / 'connected_dispatch_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Original subopcode8 connects to loose images across both complete index domains; no raw comic display credit.')


if __name__ == '__main__':
    main()
