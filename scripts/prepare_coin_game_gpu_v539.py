"""Research-only coin-game opcode fixture; no playable release or prose edits."""

import argparse
import json
import struct
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

PARENT = Path('out/all_routes_combined_v534_candidate.nds')
OUT = Path('work/analysis/fullscreen_caller_v539')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parent', type=Path, default=PARENT)
    parser.add_argument('--out', type=Path, default=OUT)
    args = parser.parse_args()
    output, parent_path = args.out, args.parent
    output.mkdir(parents=True, exist_ok=True)
    parent, clean = NdsImage.open(parent_path), NdsImage.open('work/clean.nds')
    digest = sha(parent_path.read_bytes())
    assert digest in ['cac800924a1dfb3e2bc6352ef3f47f8f82986229377de20bc5e194046b5a6f45',
                      '9f2e4c47c059b0606141d93c0f17a34f16a75fd66ceefe63c04e8a2a54577859']
    manifest = json.loads(parent_path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert manifest['candidate_sha256'] == digest and len(manifest['batches']) == 470
    packet = IlnkContainer.parse(clean.read_file('/data/SC0.DK4')).blocks[178][388:390]
    assert packet == bytes.fromhex('01c1')
    original, arm = clean.read_file('/__arm9__.bin'), parent.read_file('/__arm9__.bin')
    ranges = [(0x2A510, 0x2A5B4), (0x293B8, 0x29434), (0x63898, 0x6428C)]
    restored = bytearray(arm)
    for literal in (0x639F0, 0x639F4):
        restored[literal:literal + 4] = original[literal:literal + 4]
    assert all(original[lo:hi] == restored[lo:hi] for lo, hi in ranges)
    u = machine(arm)
    owner, stream, length, result = 0x02470000, 0x02470100, 0x02470200, 0x02470220
    u.mem_write(owner, struct.pack('<2I', 0, stream))
    u.mem_write(stream, packet)
    u.reg_write(UC_ARM_REG_R0, result)
    u.reg_write(UC_ARM_REG_R1, owner)
    u.reg_write(UC_ARM_REG_R2, length)
    u.reg_write(UC_ARM_REG_SP, STACK)
    u.emu_start(0x0202A510, 0x02029410, count=128)
    assert u.reg_read(UC_ARM_REG_PC) == 0x02029410
    assert struct.unpack('<I', u.mem_read(length, 4))[0] == 2
    assert bytes(u.mem_read(stream, 2)) == packet
    before = {p: data for _, p, data in parent.iter_files()} | dict(parent.iter_components())
    path = '/data/SC0.DK4'
    data = bytearray(before[path])
    offsets = struct.unpack_from('<344I', data, 8)
    offset = offsets[44] + 26
    assert data[offset:offset + 2] == bytes.fromhex('0049')
    data[offset:offset + 2] = packet
    fixture = NdsImage.open(parent_path)
    fixture.replace_file(path, bytes(data))
    destination = output / 'coin_game_RESEARCH_ONLY.nds'
    assert not destination.exists()
    fixture.save(destination)
    saved = NdsImage.open(destination)
    after = {p: raw for _, p, raw in saved.iter_files()} | dict(saved.iter_components())
    assert before.keys() == after.keys() and [p for p in before if before[p] != after[p]] == [path]
    assert saved.read_file(path) == data
    block_before, block_after = [IlnkContainer.parse(d[path]).blocks for d in (before, after)]
    assert all(a == b for n, (a, b) in enumerate(zip(block_before, block_after)) if n != 44)
    assert len(block_before[44]) == len(block_after[44])
    assert block_before[44][:26] == block_after[44][:26] and block_before[44][28:] == block_after[44][28:]
    inputs = json.loads(Path('work/analysis/movie_gpu_fixture_v336/opening_inputs.json').read_text(encoding='utf-8'))
    (output / 'opening_inputs.json').write_text(json.dumps(inputs, indent=2) + '\n', encoding='utf-8')
    proof = {'research_only': True, 'not_playable_distribution_or_registered_candidate': True,
             'parent': str(parent_path), 'parent_sha256': digest, 'parent_profile': manifest['profile'],
             'inherited_batches': 470, 'research_ROM': str(destination),
             'research_ROM_sha256': sha(destination.read_bytes()),
             'only_changed_file': path, 'block': 44, 'block_offset': 26,
             'original_movie_packet': '0049', 'replacement_original_coin_packet': packet.hex(),
             'clean_source': '/data/SC0.DK4 block178 offset388',
             'coin_major_opcode': 6, 'coin_subopcode': 1,
             'native_dispatch_endpoint': 0x02029410, 'native_entry': 0x02063898,
             'instruction_length': 2, 'source_exact_code_ranges': ranges,
             'all_prose_other_controls_blocks_art_and_components_exact_parent': True,
             'coin_game_post_return_story_branch_not_compatible_or_credited': True,
             'normal_gambler_recruitment_or_event_unlock_verified': False,
             'production_ROM_unchanged': True}
    destination.with_suffix('.fixture.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    assert sha(parent_path.read_bytes()) == digest
    print('Original two-byte coin-game instruction verified; research-only display fixture prepared.')


if __name__ == '__main__':
    main()
