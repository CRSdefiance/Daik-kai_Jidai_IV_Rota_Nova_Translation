"""Bind two current inventory graphics to actual source-command widget fixtures.

The substituted event instruction proves the original widget, not ordinary
event reachability. Byte-pattern census results are never treated as scripts.
"""

import struct
from collections import Counter
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE
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
from scripts.inspect_committed_gpu_v646 import CORE_SHA
from scripts.prepare_generic_inventory_v724 import OUT, PARENT
from scripts.probe_button_prompt_native import BASE, STACK, STOP, machine
from scripts.research_online_loader_v190 import resource_call
from scripts.trace_control_aliases_v688 import sections
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = OUT.parent
CAP = Path('work/emulation_v193')
FRAMES = (3600, 3900, 4200, 4500, 4800)
VIEW = 0x02279458


def scan(rom):
    rows = []
    for _, path, data in rom.iter_files():
        if not path.startswith(('/COMMON/', '/data/', '/testdata/')):
            continue
        if data.startswith(b'ILNK'):
            blocks, storage = IlnkContainer.parse(data).blocks, 'ILNK blocks'
        elif data.startswith(b'VE'):
            blocks, storage = [data], 'whole VE including header'
        else:
            continue
        counts, targets, positions = Counter(), [], 0
        for block, raw in enumerate(blocks):
            for offset in range(len(raw) - 3):
                word, operand = struct.unpack_from('<2H', raw, offset)
                positions += 1
                if word & 0xFF00 == 0x4800 and (operand >> 8) & 3 == 3:
                    index = operand & 255
                    counts[index] += 1
                    if index >= 12:
                        targets.append({'block': block, 'offset': offset, 'word': word,
                            'operand': operand, 'index': index,
                            'exact_4800_word': word == 0x4800,
                            'standard03_or83_high_operand': operand >> 8 in (3, 131)})
        rows.append({'path': path, 'sha256': sha(data), 'storage': storage,
            'blocks': len(blocks), 'byte_positions_checked': positions,
            'kind3_byte_pattern_counts_not_decoded_instructions': dict(sorted(counts.items())),
            'index12_up_byte_candidates_not_reachability': targets})
    assert len(rows) == 20
    return rows


def dialogue_boundary(rom, path, block):
    raw = IlnkContainer.parse(rom.read_file(path)).blocks[block]
    assert raw[18:24] == bytes.fromhex('0040ffff0048')
    owner, stream, result, length = 0x02470000, 0x02471000, 0x02472000, 0x02472040
    cpu = machine(rom.read_file('/__arm9__.bin'))
    cpu.mem_write(owner - 16, b'\xA5' * 48)
    cpu.mem_write(owner, bytes(16))
    cpu.mem_write(owner + 4, struct.pack('<I', stream + 18))
    cpu.mem_write(stream - 16, b'\xA5' * 16 + raw + b'\xA5' * 16)
    cpu.mem_write(result, bytes(16))
    cpu.mem_write(length, bytes(4))
    calls, executed = [], set()

    def bridge(u, address, size, unused):
        executed.add(address)
        if address == 0x0202425C:
            calls.append({'PC': address, 'speaker': u.reg_read(UC_ARM_REG_R0),
                          'text_offset_in_block': u.reg_read(UC_ARM_REG_R1) - stream})
            u.reg_write(UC_ARM_REG_R0, 0)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
        elif address == 0x020470B4:
            raise AssertionError('Text boundary unexpectedly selects an image')

    cpu.hook_add(UC_HOOK_CODE, bridge)
    for reg, value in ((UC_ARM_REG_R0, result), (UC_ARM_REG_R1, owner),
                       (UC_ARM_REG_R2, length), (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
        cpu.reg_write(reg, value)
    cpu.emu_start(BASE + 0x2A510, STOP, count=10000)
    consumed = struct.unpack('<I', cpu.mem_read(length, 4))[0]
    end = raw.index(0, 24) + 1
    assert consumed == (end - 18 + 1) // 2 * 2
    assert cpu.reg_read(UC_ARM_REG_PC) == STOP
    assert calls == [{'PC': 0x0202425C, 'speaker': 72, 'text_offset_in_block': 24}]
    assert bytes(cpu.mem_read(stream, len(raw))) == raw
    assert bytes(cpu.mem_read(stream - 16, 16)) == bytes(cpu.mem_read(stream + len(raw), 16)) == b'\xA5' * 16
    assert bytes(cpu.mem_read(owner - 16, 16)) == bytes(cpu.mem_read(owner + 16, 16)) == b'\xA5' * 16
    return {'path': path, 'block': block, 'block_sha256': sha(raw), 'instruction_offset': 18,
        'apparent_4800_candidate_offset': 22, 'native_consumed_bytes': consumed,
        'text_display_calls_bridged_only': calls, 'native_image_helper_not_called': True,
        'executed_instruction_addresses': sorted(executed), 'normal_event_progression_proven': False}


def main():
    assert not (ROOT / 'proof.json').exists()
    release_paths = [PARENT, PARENT.with_suffix('.manifest.json'), PARENT.with_suffix('.xdelta'),
                     Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds')]
    hashes = {str(p): sha(p.read_bytes()) for p in release_paths}
    current, clean = NdsImage.open(PARENT), NdsImage.open('work/clean.nds')
    baseline = {p: data for _, p, data in current.iter_files()} | dict(current.iter_components())
    arm, source = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    ranges = [(0x2A510, 0x2A5BC), (0x29AA0, 0x29BD0), (0x29FFC, 0x2A0F8),
              (0x28A64, 0x28A8C), (0x28E14, 0x29094), (0x470B4, 0x47184)]
    assert all(arm[a:b] == source[a:b] for a, b in ranges)
    parts = sections(current)
    cases = []
    inputs = read(OUT / 'opening_inputs.json')
    for index in (12, 20):
        fixture = OUT / f'index{index}_RESEARCH_ONLY.nds'
        manifest = read(fixture.with_suffix('.fixture.json'))
        assert manifest['parent_sha256'] == hashes[str(PARENT)] and manifest['inherited_batches'] == 470
        altered = NdsImage.open(fixture)
        files = {p: data for _, p, data in altered.iter_files()} | dict(altered.iter_components())
        assert files.keys() == baseline.keys()
        assert [p for p in baseline if files[p] != baseline[p]] == ['/data/SC0.DK4']
        original, new = [IlnkContainer.parse(d['/data/SC0.DK4']).blocks for d in (baseline, files)]
        assert all(a == b for n, (a, b) in enumerate(zip(original, new)) if n != 44)
        assert len(original[44]) == len(new[44]) and original[44][:30] == new[44][:30]
        assert original[44][34:] == new[44][34:] and new[44][30:34] == bytes.fromhex(manifest['replacement_generic_image_packet'])
        folder = CAP / f'generic_inventory_v724_{index}'
        report_path = folder / 'capture_report.json'
        report = read(report_path)
        assert report['ROM_sha256'] == sha(fixture.read_bytes()) == manifest['research_ROM_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['frames'] == 5000 and report['core_DLL_sha256'] == CORE_SHA
        assert report['scripted_input_schedule'] == inputs
        path = f'/_pxl/slackimg{index}.pxl'
        data = current.read_file(path)
        pxl = PxlImage.from_bytes(data)
        origin = [(256 - pxl.width) // 2, 20]
        points = [(i % pxl.width, i // pxl.width, native5(pxl.palette[c]))
                  for i, c in enumerate(pxl.indices) if c]
        shots = {r['frame']: r for r in report['frames_captured']}
        snapshots = {r['frame']: r for r in report['read_only_capture_RAM_snapshots']}
        frames = []
        for frame in FRAMES:
            shot, snap = shots[frame], snapshots[frame]
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            raw = Path(snap['path']).read_bytes()
            assert sha(raw) == snap['sha256'] and len(raw) == 0x400000
            image = Image.open(shot['path']).convert('RGB')
            assert all(native5(image.getpixel((x + origin[0], y + origin[1]))) == rgb for x, y, rgb in points)
            view = struct.unpack_from('<12I', raw, VIEW - BASE)
            assert view[5] == 4 and view[6:10] == (0, 0, 0, 0) and view[10:] == (pxl.width, pxl.height)
            name_pointer = struct.unpack_from('<I', raw, view[3] - BASE + 12)[0]
            name = raw[name_pointer - BASE:name_pointer - BASE + 128].split(b'\0')[0].decode('ascii')
            assert '/' + name.replace('\\', '/').lstrip('/') == path
            cpu = machine(arm)
            cpu.mem_write(BASE, raw)
            executed = resource_call(cpu, 0xD4170, (VIEW,))
            pointer = cpu.reg_read(UC_ARM_REG_R0)
            assert bytes(cpu.mem_read(pointer, len(data))) == data
            for pc in executed:
                matches = [b[pc - base:pc - base + 4] for _, base, b in parts if base <= pc and pc + 4 <= base + len(b)]
                assert matches and all(b == raw[pc - BASE:pc - BASE + 4] for b in matches)
            frames.append({'frame': frame, 'screenshot': shot, 'RAM': snap,
                'actual_view_fields': list(view), 'actual_resource_filename': name,
                'native_cache_pointer': pointer, 'complete_cached_file_exact': True,
                'native_cache_getter_executed_code_source_exact': sorted(executed),
                'all_nonzero_source_pixels_exact': len(points)})
        cases.append({'index': index, 'source_path': path, 'current_file_sha256': sha(data),
            'extent': [pxl.width, pxl.height], 'native_origin': origin, 'frames': frames,
            'complete_letter_edges_shadow_and_native_bounds_reviewed': True,
            'source_command_fixture_not_ordinary_event_progression': True,
            'palette_zero_behavior_and_every_transition_not_claimed': True,
            'fixture_manifest': str(fixture.with_suffix('.fixture.json')),
            'capture_report': str(report_path), 'capture_report_sha256': sha(report_path.read_bytes())})
    scans = {'clean': scan(clean), 'current': scan(current)}
    text_cases = []
    for label, rom in (('clean', clean), ('current', current)):
        for prefix in ('data', 'testdata'):
            for route, block in ((1, 24), (3, 26)):
                text_cases.append({'ROM': label, **dialogue_boundary(rom, f'/{prefix}/SC{route}.DK4', block)})
    # This narrow canonical operand test excludes untested flag combinations.
    standard = [dict(row, hits=[h for h in row['index12_up_byte_candidates_not_reachability']
                               if h['standard03_or83_high_operand']])
                for row in scans['clean']]
    assert not any(r['hits'] for r in standard if r['path'] != '/data/WORLDMAP.DK4')
    proof = {'candidate': str(PARENT), 'candidate_sha256': hashes[str(PARENT)],
        'source_exact_decoder_ranges': ranges, 'two_current_native_widget_cases': cases,
        'two_terminal5000_frame_research_cold_boots': True,
        'ten_complete_current_source_images_and_resident_file_getters_pass': True,
        'script_container_byte_census': scans, 'eight_original_text_boundary_cases': text_cases,
        'no_standard03_or83_operand_index12_up_outside_WORLDMAP_in_clean20_containers': True,
        'positive_patterns_not_decoded_instruction_or_global_unused_claim': True,
        'ordinary_name_entry_and_prompt_parents_still_unidentified': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()),
        'preparer_sha256': sha(Path('scripts/prepare_generic_inventory_v724.py').read_bytes()),
        'release_hashes_unchanged': hashes, 'full_goal_complete': False}
    for p, digest in hashes.items():
        assert sha(Path(p).read_bytes()) == digest
    save(ROOT / 'proof.json', proof)
    print('V724: two current widget fixtures,ten complete source/caches,eight original text boundaries; ordinary contexts remain open.')


if __name__ == '__main__':
    main()
