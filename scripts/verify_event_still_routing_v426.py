"""Original Gallery tables and scene operand decoding; no live unlocks."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R1,
    UC_ARM_REG_R5,
    UC_ARM_REG_R7,
    UC_ARM_REG_R9,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine

ROM = Path('out/all_routes_combined_v414_candidate.nds')
OUT = Path('work/analysis/event_still_routing_v426')
CARDS = (168, 169, 170, 171, 206, 207, 208, 209)
OWNER, STREAM = 0x02460000, 0x02461000


def main():
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == '699c19373b11dbbbc91c4ace9a29bde680da424fed92f92451e267b8570fdd0c'
    ranges = [(0x42C74, 0x42C94), (0x42E5C, 0x42ED4),
              (0x42F4C, 0x42F70), (0x29F94, 0x29FBC),
              (0x28AA8, 0x28BAC)]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ranges)
    galleries, decoded = [], []
    for label, payload in [('clean', original), ('current', arm)]:
        u = machine(payload)
        u.mem_write(OWNER, b'\xA5' * 0x80)
        u.reg_write(UC_ARM_REG_R11, OWNER)
        u.emu_start(0x02042C74, 0x02042C94, count=16)
        assert u.reg_read(UC_ARM_REG_PC) == 0x02042C94
        counts = struct.unpack('<4I', u.mem_read(OWNER + 0x2C, 16))
        assert counts == (46, 41, 39, 38)
        after = bytearray(u.mem_read(OWNER, 0x80))
        after[0x2C:0x3C] = b'\xA5' * 16
        assert after == b'\xA5' * 0x80
        routes = []
        for route, count in enumerate(counts):
            u.mem_write(OWNER + 0x1C, struct.pack('<I', route))
            u.reg_write(UC_ARM_REG_R5, 0)
            u.emu_start(0x02042E5C, 0x02042ED4, count=32)
            assert u.reg_read(UC_ARM_REG_PC) == 0x02042ED4
            pointer = struct.unpack('<I', u.mem_read(OWNER + 0x14, 4))[0]
            indices = list(struct.unpack(f'<{count}I', u.mem_read(pointer, count * 4)))
            assert len(set(indices)) == count
            assert not set(indices).intersection(CARDS)
            assert u.reg_read(UC_ARM_REG_R9) == count
            # Execute the exact image argument load for every valid Gallery
            # selection. Stop at the real reader call, before drawing/loading.
            for selection, expected in enumerate(indices):
                u.reg_write(UC_ARM_REG_R7, selection)
                u.emu_start(0x02042F58, 0x02042F6C, count=8)
                assert u.reg_read(UC_ARM_REG_PC) == 0x02042F6C
                assert u.reg_read(UC_ARM_REG_R1) == expected
            routes.append({'route': route, 'count': count, 'table_pointer': pointer,
                           'image_indices': indices,
                           'exact_reader_argument_cases': count})
        galleries.append({'ROM': label, 'routes': routes})
        # Supplied two-word scene operands, not fabricated route progression.
        # Both low and high auxiliary bits execute the actual bit15/low8 decode.
        u.mem_write(OWNER, bytes(0x80))
        u.mem_write(OWNER + 4, struct.pack('<I', STREAM))
        for high in (0x80, 0xFF):
            for index in range(256):
                operand = high << 8 | index
                u.mem_write(STREAM, struct.pack('<2H', 0, operand))
                u.reg_write(UC_ARM_REG_R5, OWNER)
                u.reg_write(UC_ARM_REG_SP, STACK)
                u.emu_start(0x02029F94, 0x02029FB4, count=16)
                assert u.reg_read(UC_ARM_REG_PC) == 0x02029FB4
                assert u.reg_read(UC_ARM_REG_R1) == index
                assert bytes(u.mem_read(STREAM, 4)) == struct.pack('<2H', 0, operand)
                decoded.append({'ROM': label, 'operand': operand, 'image_index': index})
    assert galleries[0]['routes'] == galleries[1]['routes']
    assets = []
    for index in CARDS:
        path = f'/evstill/evstill{index:03d}.pxl'
        pxl = PxlImage.from_bytes(current.read_file(path))
        assets.append({'index': index, 'path': path, 'bytes': len(current.read_file(path)),
                       'current_sha256': sha(current.read_file(path)),
                       'clean_sha256': sha(clean.read_file(path)),
                       'dimensions': [pxl.width, pxl.height],
                       'Gallery_table_membership': [], 'scene_operand': 0x8000 | index})
    proof = {'format': 'dk4-event-still-routing-v426', 'candidate': str(ROM),
             'candidate_sha256': sha(ROM.read_bytes()),
             'source_exact_code_ranges': ranges, 'Gallery_tables': galleries,
             'actual_Gallery_reader_argument_cases': 328,
             'scene_operand_decode_cases': len(decoded),
             'scene_decoder_samples': [r for r in decoded if r['image_index'] in CARDS],
             'village_cards': assets,
             'village_cards_absent_from_all_four_Gallery_route_lists': True,
             'story_opcode_or_actual_route_reachability_proven': False,
             'scope': 'Original Gallery count/table and argument fragments; original scene operand bit15/low8 decode with explicit supplied owner/stream. No live Gallery unlock, scene transition, script instruction boundary census or GPU display is credited.',
             'unused_art_claim': False, 'ROM_or_save_modified': False,
             'all18_plaques_fully_completed': False, 'full_goal_complete': False}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'routing_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'Gallery_reader_argument_cases': 328,
                      'scene_decode_cases': len(decoded),
                      'all_eight_cards_absent_from_Gallery': True}))


if __name__ == '__main__':
    main()
