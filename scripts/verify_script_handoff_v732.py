"""Original cached SC parent handoff through the first native instruction read.

Loaded cache objects, an active-event field and scratch parent stack are explicit
research inputs. V727 supplies the full file-loader proof; it is not repeated.
Stop before the first opcode handler. No ordinary trigger/GPU/global-use claim.
"""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R8,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_R12,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.trace_control_aliases_v688 import sections
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/script_handoff_v732')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
PRIOR = Path('work/analysis/event_script_sources_v727/proof.json')
END = 0x0202A530
SOURCE_VTABLE, STREAM_VTABLE, CACHE_VTABLE = 0x021343E4, 0x021345B0, 0x02134578
ACTIVE = 0x02279668 + 0x54
SDK = (0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08, 0x020E5650)


def run(rom, label, prior):
    arm = rom.read_file('/__arm9__.bin')
    assert struct.unpack_from('<2I', arm, 0x23FF0) == (SOURCE_VTABLE, STREAM_VTABLE)
    assert struct.unpack_from('<3I', arm, 0x24118) == (SOURCE_VTABLE, ACTIVE - 0x54, STREAM_VTABLE)
    u = machine(arm)
    parts = sections(rom)
    source_words, reads, cache_events = {}, [], []
    begin, end = 0, 0

    def code(cpu, address, size, unused):
        assert address not in SDK, f'Unexpected loader/SDK/assert entry {address:#x}'
        actual = bytes(cpu.mem_read(address, size))
        assert any(data[address - base:address - base + size] == actual
            for _, base, data in parts if base <= address and address + size <= base + len(data)), hex(address)
        assert source_words.setdefault(address, actual) == actual
        if address == 0x02024134:
            cache_events.append([address, cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1)])
        if address == 0x02023F50:
            assert cpu.reg_read(UC_ARM_REG_R0) == 1 and cpu.reg_read(UC_ARM_REG_SP) == STACK

    def observe(cpu, access, address, size, value, unused):
        if address < end and begin < address + size:
            reads.append({'PC': cpu.reg_read(UC_ARM_REG_PC), 'address': address, 'bytes': size,
                'read_hex': bytes(cpu.mem_read(address, size)).hex()})

    h1, h2 = u.hook_add(UC_HOOK_CODE, code), u.hook_add(UC_HOOK_MEM_READ, observe)
    cases, route_provenance = [], []
    try:
        for route in range(4):
            path = f'/data/SC{route}.DK4'
            data = rom.read_file(path)
            blocks = IlnkContainer.parse(data).blocks
            old_route = next(r for r in prior['routes'] if r['route'] == route)
            assert old_route['SC_sha256'] == sha(data)
            old_blocks = {a['native_selected_block']: a for a in old_route['actions'] if a['kind'] == 2}
            assert len(old_blocks) == len(blocks)
            route_provenance.append({'route': route, 'SC_path': path, 'SC_sha256': sha(data),
                'all_blocks_bound_to_V727_complete_native_loader_payloads': len(blocks)})
            padding_counts = {0: 0, 2: 0}
            for index, block in enumerate(blocks):
                assert old_blocks[index]['payload_sha256'] == sha(block)
                assert len(block) >= 12
                declared = struct.unpack_from('<I', block, 4)[0]
                padding = len(block) - 8 - declared
                assert declared >= 2 and declared % 2 == 0 and padding in (0, 2)
                assert len(block) == ((8 + declared + 3) & ~3)
                assert block[8 + declared:] == bytes(padding)
                padding_counts[padding] += 1
                assert len(block) <= 0x2400
                for mode in (0, 1):
                    cache = STACK + 0x10
                    begin, end = cache + 8, cache + 8 + len(block)
                    u.mem_write(STACK - 0x100, b'\xA5' * 0x2700)
                    u.mem_write(cache, struct.pack('<2I', CACHE_VTABLE, index))
                    u.mem_write(begin, block)
                    u.mem_write(ACTIVE, struct.pack('<I', 1))
                    for register, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP),
                        (UC_ARM_REG_R0, cache), (UC_ARM_REG_R1, index), (UC_ARM_REG_R4, cache),
                        (UC_ARM_REG_R5, SOURCE_VTABLE), (UC_ARM_REG_R11, STREAM_VTABLE),
                        (UC_ARM_REG_R10, 0x02410010), (UC_ARM_REG_R8, mode)):
                        u.reg_write(register, value)
                    reads.clear()
                    cache_events.clear()
                    u.emu_start(0x02023F4C, END, count=2000)
                    assert u.reg_read(UC_ARM_REG_PC) == END
                    assert cache_events == [[0x02024134, cache, index]]
                    assert reads == [{'PC': 0x0202A524, 'address': begin + 8,
                        'bytes': 2, 'read_hex': block[8:10].hex()}]
                    player = u.reg_read(UC_ARM_REG_R1)
                    assert player == STACK - 0x48
                    assert struct.unpack('<2I', u.mem_read(player, 8)) == (STREAM_VTABLE, begin + 8)
                    assert struct.unpack('<2I', u.mem_read(STACK + 8, 8)) == (STREAM_VTABLE, begin + 8)
                    assert u.reg_read(UC_ARM_REG_R2) == player + 8
                    assert struct.unpack('<I', u.mem_read(player + 8, 4))[0] == 2
                    first = struct.unpack_from('<H', block, 8)[0]
                    assert u.reg_read(UC_ARM_REG_R12) == (first >> 13) & 7
                    assert u.reg_read(UC_ARM_REG_R3) == mode
                    assert bytes(u.mem_read(begin, len(block))) == block
                    assert struct.unpack('<2I', u.mem_read(cache, 8)) == (CACHE_VTABLE, index)
                    assert bytes(u.mem_read(end, 16)) == b'\xA5' * 16
                    assert bytes(u.mem_read(STACK + 0x2448, 4)) == b'\xA5' * 4
                    cases.append({'route': route, 'block': index, 'mode': mode,
                        'complete_source_block_bytes': len(block), 'source_block_sha256': sha(block),
                        'declared_SC_body_bytes': declared, 'stored_zero_alignment_padding_bytes': padding,
                        'source_header_bytes_skipped': 8, 'native_first_word': first,
                        'native_first_major_category': (first >> 13) & 7,
                        'original_cache_hit': list(cache_events[0]), 'original_source_reads': list(reads),
                        'whole_source_header_payload_cache_metadata_and_tail_guard_exact': True,
                        'first_instruction_pointer_and_mode_derived_by_original_parent': True})
            route_provenance[-1]['stored_zero_alignment_padding_histogram'] = padding_counts
            print(f'{label} route{route}: {len(blocks) * 2} original handoffs and first instruction reads pass.', flush=True)
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
    assert len(cases) == 2614
    return {'ROM': label, 'ROM_sha256': sha(rom.source.read_bytes()), 'routes': route_provenance,
        'native_handoff_and_first_read_cases': cases,
        'executed_source_words': [{'PC': p, 'hex': source_words[p].hex()} for p in sorted(source_words)]}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    assert not (ROOT / 'proof.json').exists()
    release = {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
        ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
        Path('out/raphael_natural_v2_accepted_base.nds'))}
    assert release[str(ROM)] == '6534e5619673ea6bdffa3a2342622b99ef393bef52ef58cac131ee94ae0f4030'
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, original = (r.read_file('/__arm9__.bin') for r in (current, clean))
    ranges = [(0x23F4C, 0x24134), (0x24134, 0x24230), (0x2A510, 0x2A530)]
    assert all(arm[lo:hi] == original[lo:hi] for lo, hi in ranges)
    previous = read(PRIOR)
    assert previous['candidate_sha256'] == release[str(ROM)]
    result = [run(r, label, next(p for p in previous['two_ROM_cases'] if p['ROM'] == label))
        for r, label in ((clean, 'clean'), (current, 'current'))]
    compared = []
    for rows in result:
        compared.append([(c['route'], c['block'], c['mode'], c['native_first_word'], c['native_first_major_category'])
            for c in rows['native_handoff_and_first_read_cases']])
    assert compared[0] == compared[1] and len(compared[0]) == 2614
    save(ROOT / 'native_cases.json', {'versions': result})
    proof = {'candidate': str(ROM), 'candidate_sha256': release[str(ROM)],
        'previous_goal_turn': 'progress: V731 original decimal sprite writer classified and recorded',
        'prior_full_file_loader_proof': str(PRIOR), 'prior_full_file_loader_proof_sha256': sha(PRIOR.read_bytes()),
        'source_exact_ranges': ranges, 'complete_source_block_count_per_ROM': 1307,
        'two_modes_two_ROM_original_handoff_and_first_read_cases': 5228,
        'no_generation_or_mutation_in_tested_original_cache_to_first_read_path': True,
        'source_instruction_pointer_is_loaded_SC_payload_plus8': True,
        'all_source_headers_payloads_metadata_and_tail_guards_exact': True,
        'all2614_clean_current_first_native_word_category_and_mode_pairs_exact': True,
        'ordered_first_word_pair_digest': sha(b''.join(struct.pack('<5I', *r) for r in compared[0])),
        'cached_objects_active_event_field_and_scratch_parent_stack_supplied_contracts': True,
        'first_opcode_handler_later_mutation_other_builders_ordinary_triggers_or_GPU_verified': False,
        'no_new_file_load_or_cache_success_stub': True,
        'pilot_exact_declared_length_assumption_corrected_for_original_zero_alignment_padding': True,
        'cases_file_sha256': sha((ROOT / 'native_cases.json').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'release_hashes_unchanged': release, 'full_goal_complete': False}
    for path, digest in release.items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'proof.json', proof)
    print('V732:5228 original cached SC handoffs/first native reads pass; no command generation in this path. Ordinary village triggers remain open.')


if __name__ == '__main__':
    main()
