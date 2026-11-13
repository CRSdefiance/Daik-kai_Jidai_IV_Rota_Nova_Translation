"""Classify all16 village-card byte candidates through the actual terrain reader."""

import hashlib
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn import UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/worldmap_card_candidates_v656')
ROM = Path('out/all_routes_combined_v653_candidate.nds')
DESCRIPTOR, POINT, OUT, DATA = 0x02460000, 0x02460100, 0x02460200, 0x02480000


def resident(arm, address, size):
    for section in MainCodeFile(arm, BASE).sections:
        at = address - section.ramAddress
        if 0 <= at and at + size <= len(section.data):
            return bytes(section.data[at:at + size])
    raise ValueError('Requested decoder is not wholly resident')


def load_fragment(arm, block):
    u = machine(arm)
    u.mem_write(DESCRIPTOR - 16, b'\xA5' * 40)
    u.mem_write(DESCRIPTOR, struct.pack('<2I', 0xFFFFFFFF, DATA))
    u.reg_write(UC_ARM_REG_R0, DESCRIPTOR)
    u.reg_write(UC_ARM_REG_R1, block)
    u.reg_write(UC_ARM_REG_SP, STACK)
    # The real archive constructor executes. Stop before the original Open call;
    # no filesystem result or bytes are supplied inside this source fragment.
    u.emu_start(0x0206E578, 0x0206E59C, count=10000)
    assert u.reg_read(UC_ARM_REG_PC) == 0x0206E59C
    filename = u.reg_read(UC_ARM_REG_R1)
    assert bytes(u.mem_read(filename, 32)).split(b'\0')[0] == b'\\DATA\\WORLDMAP.DK4'
    assert bytes(u.mem_read(DESCRIPTOR, 8)) == struct.pack('<2I', block, DATA)
    assert bytes(u.mem_read(DESCRIPTOR - 16, 16)) == bytes(u.mem_read(DESCRIPTOR + 8, 16)) == b'\xA5' * 16
    return {'block': block, 'original_filename_pointer': filename,
            'original_filename': '\\DATA\\WORLDMAP.DK4',
            'native_descriptor_block_index_store': True,
            'stop_before_original_Open_not_a_complete_file_load': True}


def decode(arm, overlay, blocks, block, slot, candidate_offsets):
    u = machine(arm)
    u.mem_write(overlay.ramAddress, bytes(overlay.data))
    source = blocks[block]
    offset, length = struct.unpack_from('<2H', source, slot * 4)
    point = [block * 5 + slot % 5, slot // 5]
    u.mem_write(DESCRIPTOR, struct.pack('<2I', block, DATA))
    u.mem_write(DATA - 16, b'\xA5' * 16 + source + b'\xA5' * 16)
    u.mem_write(POINT - 16, b'\xA5' * 16 + struct.pack('<2i', *point) + b'\xA5' * 16)
    u.mem_write(OUT - 16, b'\xA5' * (2500 + 32))
    call(u, 0x6E530, (DESCRIPTOR, POINT))
    assert u.reg_read(UC_ARM_REG_R0) == DATA + slot * 4
    touched, pcs = set(), {}

    def observe(cpu, kind, address, size, value, unused):
        pc = cpu.reg_read(UC_ARM_REG_PC)
        for at in range(address - DATA, address - DATA + size):
            touched.add(at)
            if at in candidate_offsets:
                pcs.setdefault(at, set()).add(pc)

    hook = u.hook_add(UC_HOOK_MEM_READ, observe, begin=DATA, end=DATA + len(source) - 1)
    try:
        executed = call(u, 0x01FFA10C - BASE, (DESCRIPTOR, POINT, OUT), instruction_limit=500000)
    finally:
        u.hook_del(hook)
    output = bytes(u.mem_read(OUT, 2500))
    assert bytes(u.mem_read(OUT - 16, 16)) == bytes(u.mem_read(OUT + 2500, 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(DATA, len(source))) == source
    assert bytes(u.mem_read(DATA - 16, 16)) == bytes(u.mem_read(DATA + len(source), 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(POINT, 8)) == struct.pack('<2i', *point)
    assert bytes(u.mem_read(POINT - 16, 16)) == bytes(u.mem_read(POINT + 8, 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(DESCRIPTOR, 8)) == struct.pack('<2I', block, DATA)
    assert not executed & {0x0202A510, 0x02029FB4, 0x02028AA8, 0x02028B74}
    assert {0x0206E530, 0x01FFA10C} <= executed
    if length == 0xFFFF:
        words = struct.unpack('<1250H', output)
        assert list(words) == [offset + (x & 1) + (((y + point[1] % 2) & 1) << 4)
                               for y in range(25) for x in range(50)]
        assert 0x01FF8000 not in executed
    else:
        assert 0x01FF8000 in executed
    return output, {'block': block, 'slot': slot, 'source_page_coordinates': point,
        'header_words': [offset, length], 'native_header_pointer_matches_declared250_entry_table': True,
        'native_decoder': 0x01FFA10C, 'compressed_stream_decoder': 0x01FF8000 if length != 65535 else None,
        'all2500_output_bytes_sha256': sha(output), 'complete50x25_word_page_and_ABI_guards_pass': True,
        'source_block_and_descriptor_and_coordinates_unchanged': True,
        'candidate_byte_reads': {str(at): sorted(pcs[at]) for at in sorted(pcs)},
        'source_read_count_unique_bytes': len(touched),
        'executed_instruction_addresses': sorted(executed),
        'no_script_dispatch_or_event_still_loader_executed': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    archive = current.read_file('/data/WORLDMAP.DK4')
    assert archive == clean.read_file('/data/WORLDMAP.DK4')
    blocks = IlnkContainer.parse(archive).blocks
    assert len(blocks) == 10
    old = read('work/analysis/village_dispatch_v589/dispatch_proof.json')
    records = next(r for r in old['container_scans']['clean'] if r['path'] == '/data/WORLDMAP.DK4')
    assert records['sha256'] == sha(archive)
    hits = records['village_card_byte_candidates_not_reachability']
    assert len(hits) == 16
    layouts, owners, pages = [], [], set()
    for block, data in enumerate(blocks):
        entries = [struct.unpack_from('<2H', data, slot * 4) for slot in range(250)]
        streams, last = [], 1000
        for slot, (offset, length) in enumerate(entries):
            if length == 0xFFFF:
                continue
            lo, hi = 1000 + offset, 1000 + offset + length
            assert lo == last and 1000 <= lo < hi <= len(data)
            streams.append({'slot': slot, 'begin': lo, 'end': hi})
            last = hi
        assert 0 <= len(data) - last <= 3
        uniform = next(slot for slot, (_, length) in enumerate(entries) if length == 65535)
        pages.add((block, uniform))
        layouts.append({'block': block, 'whole_block_sha256': sha(data),
                        'all250_four_byte_native_page_headers': [list(e) for e in entries],
                        'compressed_payload_spans': streams,
                        'all_compressed_payload_bytes_partitioned_exactly': True,
                        'final_alignment_padding': len(data) - last})
        for hit in (h for h in hits if h['block'] == block):
            at = hit['offset']
            assert struct.unpack_from('<2H', data, at) == (hit['word'], hit['operand'])
            own = [s for s in streams if s['begin'] <= at and at + 4 <= s['end']]
            assert len(own) == 1
            span = own[0]
            pages.add((block, span['slot']))
            owners.append({**hit, 'candidate_four_bytes_hex': data[at:at + 4].hex(),
                           'owning_native_compressed_page': span,
                           'offset_in_compressed_stream': at - span['begin']})
    assert len(owners) == 16 and len(pages) == 26
    arms = [r.read_file('/__arm9__.bin') for r in (clean, current)]
    overlays = [loadOverlayTable(r.rom.arm9OverlayTable, lambda _, fid, r=r: r.rom.files[fid])[0]
                for r in (clean, current)]
    assert arms[0][0x6E530:0x6E5DC] == arms[1][0x6E530:0x6E5DC]
    assert resident(arms[0], 0x01FF8000, 0x3AC) == resident(arms[1], 0x01FF8000, 0x3AC)
    assert bytes(overlays[0].data[0x10C:0x230]) == bytes(overlays[1].data[0x10C:0x230])
    archive_cases = [load_fragment(arm, block) for arm in arms for block in range(10)]
    native = []
    for block, slot in sorted(pages):
        at = {p for h in owners if h['block'] == block and h['owning_native_compressed_page']['slot'] == slot
              for p in range(h['offset'], h['offset'] + 4)}
        a, old_row = decode(arms[0], overlays[0], blocks, block, slot, at)
        b, row = decode(arms[1], overlays[1], blocks, block, slot, at)
        assert a == b and old_row == row
        assert at <= {int(k) for k in row['candidate_byte_reads']}
        if at:
            assert all(0x01FF8000 <= pc < 0x01FF83AC for pcs in row['candidate_byte_reads'].values() for pc in pcs)
        row['all_clean_current_native_output_and_reader_events_exact'] = True
        native.append(row)
    digest = hashlib.sha256()
    for row in native:
        digest.update(bytes.fromhex(row['all2500_output_bytes_sha256']))
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'WORLDMAP_sha256': sha(archive), 'all10_blocks_and2500_declared_pages_typed': layouts,
        'all16_original_byte_candidates_have_exact_compressed_page_owners': owners,
        'twenty_original_pathname_open_prefixes': archive_cases,
        'fiftytwo_original_native_page_decodes_clean_current': native,
        'all64_candidate_bytes_read_as_compressed_input_by_original_ITCM_decoder': True,
        'all26_clean_current_2500_byte_outputs_and_full_ABI_guards_exact': True,
        'ten_uniform_pages_match_independent_complete1250_word_model': True,
        'ordered_native_output_digest': digest.hexdigest(),
        'loaded_archive_blocks_and_page_coordinates_are_supplied_native_contracts': True,
        'no_filesystem_open_result_or_actual_gameplay_or_GPU_credit': True,
        'these16_patterns_do_not_establish_village_card_event_reachability': True,
        'computed_other_filename_paths_and_global_card_nonuse_not_excluded': True,
        'ROM_patch_registry_and_release_pointers_unchanged': True,
        'all18_original_plaques_incomplete22_historical_scopes_retained': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V656: all16 candidates belong to compressed terrain pages;64 candidate bytes read by native decompressor;52 clean/current decodes and20 pathname prefixes pass.')


if __name__ == '__main__':
    main()
