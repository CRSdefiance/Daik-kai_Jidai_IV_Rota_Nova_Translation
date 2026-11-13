"""Original raw reads/scaling with explicit research descriptors, not a comic scene."""

import struct
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_comic_final_letters_v251 import backing_and_payload
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/comic_scaling_v680')
ROM = Path('out/all_routes_combined_v678_candidate.nds')
HEADER, POINT, SIZE, DEST = 0x02420020, 0x02470000, 0x02470020, 0x02470040
FB = 0x022E1794
OPEN, READ, SEEK, CLOSE = 0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08
BATCH = Path('translations/gallery_chase_fringe_raw_art_v8.json')


def sample_axis(source, destination):
    # Pixel-center nearest sample, with exact ties selecting the preceding cell.
    # Derived from the original midpoint accumulator, not fitted to output pixels.
    return [((2 * x + 1) * source + 2 * destination - 1) // (2 * destination) - 1
            for x in range(destination)]


def rgb(data, width, height):
    return Image.frombytes('RGB', (width, height), bytes(c for w, in struct.iter_unpack('<H', data)
                                                    for c in bgr555(w)[:3]))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    prepath = ROOT / 'preflight.json'
    if not prepath.exists():
        names = ('graphics_completion_campaign_v1.json', 'graphics_visual_audit_v150.json', 'graphics_completion_requirements_v313.json')
        save(prepath, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
            'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
                ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
                Path('out/raphael_natural_v2_accepted_base.nds'))},
            'all_original_audits_before': {n: read(Path('translations') / n) for n in names},
            'previous_goal_turn_classification': 'progress: V679 actual cached view headers,paired cold boots and123-file final archive verified',
            'plaque_material_review_presented_to_user_not_assumed_accepted': True,
            'full_goal_complete': False})
    pre = read(prepath)
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    u, original = machine(arm), machine(clean.read_file('/__arm9__.bin'))
    ranges = ((0x0204704C, 0x020470B4), (0x020D1EF0, 0x020D2138), (0x01FF8E4C, 0x01FF92D8))
    code = []
    for lo, hi in ranges:
        data = bytes(u.mem_read(lo, hi - lo))
        assert data == bytes(original.mem_read(lo, hi - lo))
        code.append({'range': [lo, hi], 'sha256': sha(data)})
    archive = rom.read_file('/GRP/SLACKIMG.DK4')
    block = IlnkContainer.parse(archive).blocks[19]
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    source_archive = canonical.read_file('/GRP/SLACKIMG.DK4')
    source_block = IlnkContainer.parse(source_archive).blocks[19]
    assert len(block) == len(source_block) == 21 * 153600
    assert not any(v & 0x8000 for v, in struct.iter_unpack('<H', block))
    previous = read('work/analysis/comic_current_v506/proof.json')
    batch = read(BATCH)
    assert sha(BATCH.read_bytes()) == previous['batch_sha256']
    captions = []
    for row, case in zip(batch['records'], previous['cases'], strict=True):
        assert row['id'] == case['id'] and row['english'] == case['english']
        index, box = row['image_index'], row['box']
        x0, y0, x1, y1 = box
        original_region = b''.join(source_block[index * 153600 + (y * 320 + x0) * 2:
            index * 153600 + (y * 320 + x1) * 2] for y in range(y0, y1))
        payload, backing, _, _ = backing_and_payload(row, original_region, batch, source_block)
        actual_region = b''.join(block[index * 153600 + (y * 320 + x0) * 2:
            index * 153600 + (y * 320 + x1) * 2] for y in range(y0, y1))
        assert actual_region == payload and sha(payload) == case['word_payload_sha256']
        assert sha(backing) == case['reconstructed_backing_sha256']
        captions.append((row, case, struct.unpack(f'<{len(backing) // 2}H', backing)))
    handles, events = {}, []

    def bridge(cpu, address, size, unused):
        if address not in (OPEN, READ, SEEK, CLOSE):
            return
        obj = cpu.reg_read(UC_ARM_REG_R0)
        if address == OPEN:
            name = bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R1), 96)).split(b'\0')[0].decode('ascii')
            assert name.replace('\\', '/').casefold() == '/grp/slackimg.dk4' and obj not in handles
            handles[obj] = 0
            cpu.mem_write(obj + 0x20, struct.pack('<2I', 0, len(archive)))
            events.append({'operation': 'open', 'path': name})
            result = 1
        elif address == SEEK:
            offset = cpu.reg_read(UC_ARM_REG_R1)
            assert cpu.reg_read(UC_ARM_REG_R2) == 0 and 0 <= offset <= len(archive)
            handles[obj] = offset
            events.append({'operation': 'seek', 'offset': offset})
            result = 1
        elif address == READ:
            target, count = cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2)
            at = handles[obj]
            assert 0 <= at <= at + count <= len(archive)
            if target == HEADER + 20:
                assert count == 153600
            cpu.mem_write(target, archive[at:at + count])
            handles[obj] += count
            events.append({'operation': 'read', 'offset': at, 'bytes': count, 'destination': target})
            result = count
        else:
            del handles[obj]
            events.append({'operation': 'close'})
            result = 1
        cpu.reg_write(UC_ARM_REG_R0, result)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    fill = struct.pack('<H', 0x89AB) * 98304
    views = [('full_fit', 0, (0, 0), (0, 0, 256, 192)), ('clipped_origin', 1, (7, 11), (0, 0, 256, 192))]
    cases, outputs = [], {}

    def scale(pixels, screen, origin, destination):
        left, top, right, bottom = destination
        left, right = max(0, left - origin[0]), min(256, right - origin[0])
        top, bottom = max(0, top - origin[1]), min(192, bottom - origin[1])
        xs, ys = sample_axis(320, right - left), sample_axis(240, bottom - top)
        u.mem_write(FB - 16, b'\xA5' * 16 + fill + b'\xA5' * 16)
        u.mem_write(0x022E1770, struct.pack('<i', origin[0]))
        u.mem_write(0x022E176C, struct.pack('<i', origin[1]))
        u.mem_write(POINT, bytes(8))
        u.mem_write(SIZE, struct.pack('<2I', 320, 240))
        u.mem_write(DEST, struct.pack('<4i', *destination))
        u.mem_write(STACK, struct.pack('<2I', SIZE, DEST))
        executed = call(u, 0x01FF8E4C - BASE, (screen, HEADER, 0, POINT), instruction_limit=5000000)
        assert 0x01FF9250 in executed and 0x01FF925C in executed
        expected = bytearray(fill)
        for y, sy in enumerate(ys, top):
            for x, sx in enumerate(xs, left):
                offset = (screen * 49152 + y * 256 + x) * 2
                expected[offset:offset + 2] = pixels[(sy * 320 + sx) * 2:(sy * 320 + sx) * 2 + 2]
        actual = bytes(u.mem_read(FB, len(fill)))
        assert actual == bytes(expected)
        assert bytes(u.mem_read(FB - 16, 16)) == bytes(u.mem_read(FB + len(fill), 16)) == b'\xA5' * 16
        assert bytes(u.mem_read(HEADER + 20, 153600)) == pixels
        return actual, xs, ys, (left, top, right, bottom), executed

    hook = u.hook_add(UC_HOOK_CODE, bridge)
    try:
        for index in range(21):
            pixels = block[index * 153600:(index + 1) * 153600]
            header = struct.pack('<5I', 16, 320, 240, 20, 20)
            u.mem_write(HEADER - 16, b'\xA5' * (153620 + 32))
            u.mem_write(HEADER, header)
            start = len(events)
            call(u, 0x4704C, (19, HEADER + 20, index * 153600, 153600), instruction_limit=500000)
            assert not handles and bytes(u.mem_read(HEADER, 153620)) == header + pixels
            io = events[start:]
            assert len([e for e in io if e['operation'] == 'read' and e['destination'] == HEADER + 20 and e['bytes'] == 153600]) == 1
            for label, screen, origin, destination in views:
                actual, xs, ys, bounds, executed = scale(pixels, screen, origin, destination)
                assert bytes(u.mem_read(HEADER, 153620)) == header + pixels
                assert bytes(u.mem_read(HEADER - 16, 16)) == bytes(u.mem_read(HEADER + 153620, 16)) == b'\xA5' * 16
                plane = actual[screen * 98304:(screen + 1) * 98304]
                target = ROOT / f'frame_{index:02d}_{label}_SOFTWARE_RGB_NOT_GPU.png'
                rgb(plane, 256, 192).save(target)
                glyph_checks = []
                words = struct.unpack('<49152H', plane)
                for row, case, backing in captions:
                    if row['image_index'] != index:
                        continue
                    x0, y0, x1, y1 = row['box']
                    for position in (0, len(case['characters']) - 1):
                        g = case['characters'][position]
                        a, b, c, d = g['complete_record_relative_bounds']
                        points = [(dx + bounds[0], dy + bounds[1]) for dy, sy in enumerate(ys) for dx, sx in enumerate(xs)
                            if x0 + a <= sx < x0 + c and y0 + b <= sy < y0 + d
                            and (words[(dy + bounds[1]) * 256 + dx + bounds[0]] & 32767)
                            != (backing[(sy - y0) * (x1 - x0) + sx - x0] & 32767)]
                        glyph_checks.append({'id': row['id'], 'character_position': position,
                            'character': g['character'], 'projected_contrast_points': len(points),
                            'letter_has_visible_stored_word_contrast_after_this_scale': bool(points)})
                outputs[(index, label)] = target
                cases.append({'frame': index, 'source_sha256': sha(pixels), 'view': label, 'screen': screen,
                    'viewport_origin': list(origin), 'destination_LTRB': list(destination),
                    'actual_clipped_destination': list(bounds), 'source_sample_x': xs, 'source_sample_y': ys,
                    'complete_two_screen_framebuffer_sha256': sha(actual), 'original_IO': io,
                    'complete196608_framebuffer_bytes_source_header_descriptors_guards_and_ABI_pass': True,
                    'source_high_bits_copied_exact_no_opacity_conversion': True,
                    'caption_edge_letter_checks': glyph_checks,
                    'executed_original_instruction_count': len(executed),
                    'software_plane': str(target), 'software_plane_sha256': sha(target.read_bytes())})
    finally:
        u.hook_del(hook)
    coordinate_controls = []
    for dimension in (0, 1):
        pixels = struct.pack('<76800H', *[x if dimension == 0 else y for y in range(240) for x in range(320)])
        u.mem_write(HEADER, struct.pack('<5I', 16, 320, 240, 20, 20) + pixels)
        for label, screen, origin, destination in views:
            actual, _, _, _, _ = scale(pixels, screen, origin, destination)
            coordinate_controls.append({'axis': dimension, 'view': label,
                'all_destination_words_identify_exact_source_coordinate': True, 'sha256': sha(actual)})
    sheets = []
    for first in range(0, 21, 4):
        count = min(4, 21 - first)
        sheet = Image.new('RGB', (896, count * 266), '#263238')
        draw = ImageDraw.Draw(sheet)
        for row, index in enumerate(range(first, first + count)):
            for x, block_data, title in ((0, source_block, 'Original source320x240'), (320, block, 'V678 stored English320x240')):
                im = rgb(block_data[index * 153600:(index + 1) * 153600], 320, 240)
                sheet.paste(im, (x, row * 266 + 24))
                draw.text((x + 3, row * 266 + 4), f'{index}: {title}', fill='white')
            sheet.paste(Image.open(outputs[(index, 'full_fit')]), (640, row * 266 + 24))
            draw.text((643, row * 266 + 4), 'Native scale RGB; NOT GPU', fill='white')
        target = ROOT / f'source_current_native_scale_{first:02d}.png'
        sheet.save(target)
        sheets.append({'path': str(target), 'sha256': sha(target.read_bytes())})
    missing = [g for case in cases for g in case['caption_edge_letter_checks']
               if not g['letter_has_visible_stored_word_contrast_after_this_scale']]
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'archive_sha256': sha(archive), 'block19_sha256': sha(block), 'original_code_ranges': code,
        'original_partial_archive_reads': 21, 'complete_native_scale_cases': cases,
        'independent_xy_coordinate_controls': coordinate_controls,
        'complete_two_screen_framebuffer_bytes_compared': len(cases) * 196608,
        'full_caption18_source_planes_and331_stored_character_bounds_preserved': True,
        'caption_edge_checks': sum(len(c['caption_edge_letter_checks']) for c in cases),
        'projected_missing_edge_letter_contrasts': missing, 'review_sheets': sheets,
        'original_scale_uses_clipped_destination_size_to_resample_whole_source_not_post_scale_crop': True,
        'descriptor_buffer_and_destination_are_explicit_isolated_research_inputs': True,
        'only_SDK_filesystem_calls_bridged': True,
        'no_original_comic_parent_GPU_alpha_readability_or_gameplay_clearance': True,
        'all_brown_marks_and_original_high_bits_production_ROM_unchanged': True,
        'source_restoration_approximation_and_other_graphics_gates_remain_open': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'current_goal_turn_classification': 'progress',
        'full_goal_complete': False})
    print(f'V680:21 original reads,42 full raw16 native scales,4 coordinate controls,{len(missing)} lost edge contrasts;original parent/GPU still open.', flush=True)


if __name__ == '__main__':
    main()
