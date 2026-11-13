"""Conservative negative route census with original full image-op dispatch."""

import json
import struct
from collections import Counter
from pathlib import Path

from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine
from scripts.verify_event_still_routing_v426 import CARDS

ROM = Path('out/all_routes_combined_v414_candidate.nds')
OUT = Path('work/analysis/village_card_references_v427')
OWNER, STREAM, RESULT, LENGTH = 0x02460000, 0x02461000, 0x02462000, 0x02462020


def main():
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == '699c19373b11dbbbc91c4ace9a29bde680da424fed92f92451e267b8570fdd0c'
    ranges = [(0x2A510, 0x2A5C0), (0x29AA0, 0x29AF8), (0x29F50, 0x29FBC)]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ranges)
    cases = []
    for label, payload in [('clean', original), ('current', arm)]:
        u = machine(payload)
        for image in CARDS:
            for flags in (0, 1, 7, 0x80, 0xFF):
                for high in (0x80, 0xFF):
                    instruction, operand = 0x4600 | flags, high << 8 | image
                    u.mem_write(OWNER, bytes(0x20))
                    u.mem_write(OWNER + 4, struct.pack('<I', STREAM))
                    source = struct.pack('<2H', instruction, operand)
                    u.mem_write(STREAM - 16, b'\xA5' * 36)
                    u.mem_write(STREAM, source)
                    u.mem_write(RESULT - 16, b'\xA5' * 64)
                    u.reg_write(UC_ARM_REG_R0, RESULT)
                    u.reg_write(UC_ARM_REG_R1, OWNER)
                    u.reg_write(UC_ARM_REG_R2, LENGTH)
                    u.reg_write(UC_ARM_REG_SP, STACK)
                    # Full original dispatch reaches the actual scene-parent
                    # call, including major/subopcode and instruction length.
                    u.emu_start(0x0202A510, 0x02029FB4, count=128)
                    assert u.reg_read(UC_ARM_REG_PC) == 0x02029FB4
                    assert u.reg_read(UC_ARM_REG_R1) == image
                    assert struct.unpack('<I', u.mem_read(LENGTH, 4))[0] == 4
                    assert struct.unpack('<I', u.mem_read(RESULT, 4))[0] == 0xA5A5A5A5
                    after = bytearray(u.mem_read(RESULT - 16, 64))
                    after[LENGTH - RESULT + 16:LENGTH - RESULT + 20] = b'\xA5' * 4
                    assert after == b'\xA5' * 64
                    assert bytes(u.mem_read(OWNER + 4, 4)) == struct.pack('<I', STREAM)
                    assert bytes(u.mem_read(STREAM, 4)) == source
                    assert bytes(u.mem_read(STREAM - 16, 16)) == b'\xA5' * 16
                    assert bytes(u.mem_read(STREAM + 4, 16)) == b'\xA5' * 16
                    cases.append({'ROM': label, 'instruction': instruction,
                                  'operand': operand, 'image': image, 'length': 4})
    scans = []
    for label, rom in [('clean', clean), ('current', current)]:
        for route in range(4):
            path = f'/data/SC{route}.DK4'
            raw = rom.read_file(path)
            blocks = IlnkContainer.parse(raw).blocks
            patterns, positions, card_hits = Counter(), 0, []
            for block_index, block in enumerate(blocks):
                # Every byte position, including header/padding and odd offsets.
                # This intentionally over-approximates instruction boundaries.
                for offset in range(len(block) - 3):
                    word, operand = struct.unpack_from('<2H', block, offset)
                    positions += 1
                    if word & 0xFF00 == 0x4600 and operand & 0x8000:
                        image = operand & 0xFF
                        patterns[image] += 1
                        if image in CARDS:
                            card_hits.append({'block': block_index, 'offset': offset,
                                              'instruction': word, 'operand': operand,
                                              'image': image})
            assert not card_hits
            scans.append({'ROM': label, 'path': path, 'sha256': sha(raw),
                          'ILNK_blocks': len(blocks), 'byte_positions_checked': positions,
                          'pattern_counts_not_decoded_instructions': dict(sorted(patterns.items())),
                          'village_card_pattern_matches': card_hits})
    proof = {'format': 'dk4-village-card-references-v427', 'candidate': str(ROM),
             'candidate_sha256': sha(ROM.read_bytes()), 'source_exact_code_ranges': ranges,
             'full_native_dispatch_cases': cases, 'route_scans': scans,
             'all_eight_cards_absent_from_direct_scene_encoding_in_all_four_routes': True,
             'prior_Gallery_exclusion_proof': 'work/analysis/event_still_routing_v426/routing_proof.json',
             'scope': 'Full original dispatch to the scene-parent call with supplied operand stream, then every-byte negative census of all four clean/current route archives. Positive byte patterns are not treated as decoded instructions. Runtime-generated operands, other containers and indirect consumers remain unproven.',
             'global_unused_claim': False, 'actual_scene_display_proven': False,
             'ROM_or_save_modified': False, 'all18_plaques_fully_completed': False,
             'full_goal_complete': False}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'reference_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'native_dispatch_cases': len(cases),
                      'route_blocks_scanned': sum(r['ILNK_blocks'] for r in scans),
                      'byte_positions_checked': sum(r['byte_positions_checked'] for r in scans),
                      'village_card_pattern_matches': 0}))


if __name__ == '__main__':
    main()
