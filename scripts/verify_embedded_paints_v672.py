"""Explicit scratch descriptors test legacy palette words in original blit code.

No legacy loader, original descriptor creator, gameplay consumer or GPU display
is supplied by this experiment. Both original drawing modes are explicit inputs.
"""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.compact_font import layout
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.frame_buttons_v165 import atlas_indices
from scripts.inspect_graphic_paints_v669 import ROM, units
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_frame_style_tiles_v584 import CELLS
from scripts.verify_movie_transition_bitmaps_v648 import rgb
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/embedded_paints_v672')
HEADER, POINT, SIZE, POSITION = 0x02420000, 0x02440000, 0x02440010, 0x02440020
DEST, DEST_BYTES = 0x022E1794, 98304
RECT, ORIGIN = (440, 32, 72, 24), (16, 40)
BACKGROUNDS = (0x1234, 0x2EEE)


def preflight():
    ROOT.mkdir(parents=True, exist_ok=True)
    path = ROOT / 'preflight.json'
    if not path.exists():
        frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
        save(path, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
            'release_hashes': {str(p): sha(p.read_bytes()) for p in (ROM, ROM.with_suffix('.manifest.json'),
                ROM.with_suffix('.xdelta'), Path('translations/release_stack.json'),
                Path('out/raphael_natural_v2_accepted_base.nds'))},
            'previous_goal_turn_classification': 'progress: V671 fresh current all18 plaque run, exact native crops, archived sheets and guide candidates',
            'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
            'supplied_descriptor_flags_are_experimental_inputs_not_original_legacy_parent': [4, 260],
            'production_ROM_modified': False, 'full_goal_complete': False})
    pre = read(path)
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    return pre


def sources(image, clean):
    archive = IlnkContainer.parse(image.read_file('/GRP/CMMNIMG.DK4'))
    original = IlnkContainer.parse(clean.read_file('/GRP/CMMNIMG.DK4'))
    palette, pixels = archive.blocks[4:6]
    assert palette == original.blocks[4]
    assert struct.unpack_from('<IIIIHH', palette) == (19, 2, 2668, 32505856, 16, 83)
    assert struct.unpack_from('<IIIIHH', pixels) == (18, 0, 65548, 16777792, 128, 256)
    assert len(palette) == 2676 and len(pixels) == 65556
    indices = atlas_indices(image.read_file('/GRP/CMMNIMG.DK4'))
    for path, dx in (('/_pxl/__marker.pxl', 0), ('/_pxl/__frame.pxl', 256)):
        loose = PxlImage.from_bytes(image.read_file(path))
        half = b''.join(indices[y * 512 + dx:y * 512 + dx + 256] for y in range(256))
        assert half == bytes(loose.indices), path
    return palette[20:], pixels[20:], indices


def main():
    pre = preflight()
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    palette, packed, indices = sources(current, clean)
    old_palette, old_packed, old_indices = sources(clean, clean)
    assert palette == old_palette and len(palette) == 83 * 32
    captions, expected_ink = [], set()
    batch = read('translations/frame_action_buttons_graphics_v7.json')
    for text, box in CELLS:
        row = next(r for r in batch['records'] if r['text'] == text and r.get('font_face') == 'compact-en-7px-v1')
        draw_box = row.get('draw_box', row['box'])
        mask, _, _ = layout(text, tuple(draw_box), word_space_width=row.get('compact_word_space_width', 2),
                             font_face=row['font_face'])
        l, t, r, b = box
        ink = {(x + 256, y) for y in range(t, b) for x in range(l, r)
               if indices[y * 512 + x + 256] == 9}
        wanted = {(draw_box[0] + x + 256, draw_box[1] + y)
                  for y in range(mask.height) for x in range(mask.width) if mask.getpixel((x, y))}
        assert ink == wanted
        assert {indices[y * 512 + x + 256] for y in range(t, b) for x in range(l, r)} <= {0, 9}
        original_indices = sorted({old_indices[y * 512 + x + 256] for y in range(t, b) for x in range(l, r)})
        assert 9 in original_indices
        expected_ink |= ink
        captions.append({'English': text, 'Japanese': row['source_japanese'],
            'legacy_box': [l + 256, t, r + 256, b], 'complete_current_ink_pixels': len(ink),
            'current_monochrome_caption_cells_use_only_indices0_and9': True,
            'original_antialiased_caption_palette_indices': original_indices})
    assert len(expected_ink) == 307
    arm = current.read_file('/__arm9__.bin')
    uc, original_uc = machine(arm), machine(clean.read_file('/__arm9__.bin'))
    # Code is compared before replay and again for every executed instruction.
    for base, data in units(clean):
        if base <= 0x01FF92D8 < base + len(data):
            assert bytes(uc.mem_read(0x01FF92D8, 0x500)) == bytes(original_uc.mem_read(0x01FF92D8, 0x500))
    cases, previews, executed, active, writes, reads = [], [], set(), False, set(), set()

    def write(cpu, kind, address, size, value, user):
        if not active:
            return
        if DEST - 16 <= address < DEST + DEST_BYTES + 16:
            assert DEST <= address and address + size <= DEST + DEST_BYTES
            for p in range(address, address + size):
                y, x = divmod((p - DEST) // 2, 256)
                assert ORIGIN[0] <= x < ORIGIN[0] + RECT[2] and ORIGIN[1] <= y < ORIGIN[1] + RECT[3]
                writes.add(p)
        elif not STACK - 1024 <= address < STACK:
            raise AssertionError(f'Unexpected native nonstack write {address:#x} PC {cpu.reg_read(UC_ARM_REG_PC):#x}')

    def read_memory(cpu, kind, address, size, value, user):
        if not active:
            return
        assert address + size <= DEST or address >= DEST + DEST_BYTES, 'Output read by painter'
        if HEADER <= address < HEADER + 20 + len(palette) + len(packed):
            reads.update(range(address, address + size))

    wh = uc.hook_add(UC_HOOK_MEM_WRITE, write)
    rh = uc.hook_add(UC_HOOK_MEM_READ, read_memory)
    try:
        for version, pix, idx in (('original_Japanese', old_packed, old_indices), ('current_English', packed, indices)):
            for flags in (4, 260):
                descriptor = struct.pack('<5I', flags, 128, 256, 20, 20 + len(palette)) + palette + pix
                uc.mem_write(HEADER - 16, b'\xA5' * (len(descriptor) + 32))
                uc.mem_write(HEADER, descriptor)
                uc.mem_write(POINT, struct.pack('<2I', *RECT[:2]))
                uc.mem_write(SIZE, struct.pack('<2I', *RECT[2:]))
                uc.mem_write(POSITION, struct.pack('<2I', *ORIGIN))
                for bank in range(83):
                    colors = struct.unpack_from('<16H', palette, bank * 32)
                    opaque = 0
                    for background in BACKGROUNDS:
                        uc.mem_write(DEST - 16, b'\xA5' * (DEST_BYTES + 32))
                        uc.mem_write(DEST, struct.pack('<H', background) * 49152)
                        uc.mem_write(STACK, struct.pack('<2I', SIZE, POSITION))
                        writes, reads = set(), set()
                        active = True
                        executed |= call(uc, 0x01FF92D8 - BASE, (0, HEADER, bank, POINT), instruction_limit=1000000)
                        active = False
                        actual = bytes(uc.mem_read(DEST, DEST_BYTES))
                        wanted, expected_writes = [background] * 49152, set()
                        opaque = 0
                        for y in range(RECT[3]):
                            for x in range(RECT[2]):
                                value = colors[idx[(RECT[1] + y) * 512 + RECT[0] + x]]
                                if flags & 256 or value & 0x8000:
                                    offset = (ORIGIN[1] + y) * 256 + ORIGIN[0] + x
                                    wanted[offset] = value
                                    expected_writes.update((DEST + offset * 2, DEST + offset * 2 + 1))
                                    opaque += 1
                        assert actual == struct.pack('<49152H', *wanted), (version, flags, bank, background)
                        assert writes == expected_writes
                        assert bytes(uc.mem_read(HEADER, len(descriptor))) == descriptor
                        assert bytes(uc.mem_read(HEADER - 16, 16)) == bytes(uc.mem_read(HEADER + len(descriptor), 16)) == b'\xA5' * 16
                        assert bytes(uc.mem_read(DEST - 16, 16)) == bytes(uc.mem_read(DEST + DEST_BYTES, 16)) == b'\xA5' * 16
                        ink_visible = bool(flags & 256 or colors[9] & 0x8000)
                        background_visible = bool(flags & 256 or colors[0] & 0x8000)
                        contrast = ink_visible and (colors[9] & 32767) != ((colors[0] if background_visible else background) & 32767)
                        cases.append({'version': version, 'flags': flags, 'palette_bank': bank,
                            'background': background, 'whole49152_word_sha256': sha(actual),
                            'all_destination_words_write_coverage_guards_and_source_bytes_exact': True,
                            'opaque_source_pixels': opaque, 'index9_palette_word': colors[9],
                            'index0_palette_word': colors[0], 'glyph_index_written': ink_visible,
                            'glyph_index_has_RGB5_contrast': contrast})
                        if background == BACKGROUNDS[0] and bank in (0, 9, 74, 82):
                            im = Image.new('RGB', (256, 192))
                            im.putdata(rgb(wanted))
                            path = ROOT / f'{version}_flags{flags}_bank{bank}_CONTROLLED_NATIVE.png'
                            im.save(path)
                            previews.append({'path': str(path), 'sha256': sha(path.read_bytes()),
                                'controlled_native_paint_not_a_gameplay_capture': True})
                print('V672 complete native bank range0..82:', version, 'flags', flags, flush=True)
    finally:
        active = False
        uc.hook_del(wh)
        uc.hook_del(rh)
        save(ROOT / 'paint_research.json', {'completed_cases': cases, 'executed_addresses': sorted(executed),
            'explicit_descriptor_modes_not_original_legacy_consumer': True})
    assert len(cases) == 664 and len(previews) == 16
    for address in executed:
        assert bytes(uc.mem_read(address, 4)) == bytes(original_uc.mem_read(address, 4)), hex(address)
    # Primary ink9/background0 classes match, not the antialiased source masks.
    by_key = {(c['version'], c['flags'], c['palette_bank'], c['background']): c for c in cases}
    for mode in (4, 260):
        for bank in range(83):
            for background in BACKGROUNDS:
                a, b = (by_key[v, mode, bank, background] for v in ('original_Japanese', 'current_English'))
                assert all(a[k] == b[k] for k in ('index9_palette_word', 'index0_palette_word',
                    'glyph_index_written', 'glyph_index_has_RGB5_contrast'))
    save(ROOT / 'native_embedded_paint_proof.json', {'candidate': str(ROM),
        'candidate_sha256': pre['candidate_sha256'], 'source_archive': '/GRP/CMMNIMG.DK4',
        'original_and_current_palette_block4_exact': True,
        'all131072_current_atlas_indices_exact_to_loose_marker_and_frame_halves': True,
        'all131072_clean_atlas_indices_exact_to_original_loose_halves': True,
        'palette_sha256': sha(palette), 'current_packed_indices_sha256': sha(packed),
        'original_packed_indices_sha256': sha(old_packed), 'source_crop_XYWH': list(RECT),
        'supplied_destination_XY': list(ORIGIN), 'caption_cells': captions,
        'all307_complete_current_compact_font_pixels_exact': True,
        'primary_ink9_and_background0_alpha_contrast_classes_exact_for_all83_banks_two_modes_two_backgrounds': True,
        'original_antialias_shade_masks_not_equated_to_current_monochrome_font': True,
        'cases': cases, 'all32636928_destination_words_exact': True,
        'no_output_read_or_outside_destination_crop_or_source_write': True,
        'original_painter_clipper_full_return_ABI_and_executed_code_exact': True,
        'previews': previews, 'explicit_scratch_header_and_both_flags_not_source_bound_legacy_setup': True,
        'no_original_archive_loader_descriptor_creator_parent_GPU_gameplay_or_unused_art_claim': True,
        'no_palette_conversion_invented_no_ROM_or_registry_changed': True,
        'all18_plaques_incomplete22_historical_requirements_retained': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V672 controlled original/current embedded paints pass; actual legacy parent remains open.', flush=True)


if __name__ == '__main__':
    main()
