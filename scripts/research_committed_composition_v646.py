"""Bind committed polygons to complete source-native VRAM views, not PNG colors."""

import struct
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.rom.nds import NdsImage
from dk4tool.scan.compression_probe import decompress_lz10
from scripts.research_ending_blend_v631 import plane
from scripts.research_ending_transitions_v642 import compose
from scripts.verify_ending_photo_markers_v594 import find_live
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/opening_composition_v646')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/opening_composition_v646_committed_v2')


def render_order(committed):
    """Pinned gfx3d_GenerateRenderLists/gfx3d_ysort_compare, not submission order."""
    packed = Path(committed['files']['committed_polygons_native.bin']['path']).read_bytes()
    state = Path(committed['files']['committed_state_native.bin']['path']).read_bytes()
    manual = struct.unpack_from('<I', state, 44)[0]
    assert manual in (0, 1)
    polys = committed['polygons']
    opaque = [i for i, p in enumerate(polys) if p['attributes'] >> 16 & 31 == 31]
    translucent = [i for i, p in enumerate(polys) if p['attributes'] >> 16 & 31 < 31]

    def key(index):
        low, high = struct.unpack_from('<2f', packed, index * 40 + 32)
        assert low <= high
        return high, low, index

    opaque.sort(key=key)
    if not manual:
        translucent.sort(key=key)
    order = opaque + translucent
    return [polys[i] for i in order], {'manual_translucent_sort': bool(manual),
        'original_polygon_order': order, 'source': 'gfx3d.cpp gfx3d_GenerateRenderLists/gfx3d_ysort_compare',
        'opaque_first_then_translucent_maxY_minY_stable_index': True}


def vram_bindings(committed, movie):
    if not hasattr(movie, '_v646_palettes'):
        movie._v646_palettes = {i: decompress_lz10(movie.source[movie.data_offset + r[2]:])
                               for i, r in enumerate(movie.records)}
    vram = Path(committed['files']['source_lcdc_vram.bin']['path']).read_bytes()
    io = Path(committed['files']['source_arm9_io.bin']['path']).read_bytes()
    regs = [io[0x240 + i + (i >= 7)] for i in range(9)]
    assert regs == [0x83, 0x8B, 0x84, 0x81, 0x82, 0, 0x83, 0, 0x82]
    # Source MMU.cpp maps A/B to texture slots0/1 and G to texture palette slot0.
    bindings, rows = {}, []
    for poly in committed['polygons']:
        param, pal = poly['texture_parameter'], poly['palette']
        key = param, pal
        if key in bindings:
            continue
        kind, width, height = param >> 26 & 7, 8 << (param >> 20 & 7), 8 << (param >> 23 & 7)
        assert kind in (3, 4) and not param & 0xF0000
        offset, per_byte = (param & 65535) * 8, 2 if kind == 3 else 1
        assert offset + width * height // per_byte <= 0x40000
        packed = vram[offset:offset + width * height // per_byte]
        indices = bytes(x for b in packed for x in (b & 15, b >> 4)) if kind == 3 else packed
        palette_offset, candidates = 0x94000 + pal * 16, []
        for index, record in enumerate(movie.records):
            texture = movie.texture(index)
            nw, nh = record[0] >> 16, record[1] & 65535
            if (texture.width, texture.height) != (width, height):
                continue
            if len(texture.palette) != (16 if kind == 3 else 256):
                continue
            assert 0 < nw <= width and 0 < nh <= height
            palette = movie._v646_palettes[index]
            assert len(palette) == record[3] and palette_offset + len(palette) <= 0x98000
            if vram[palette_offset:palette_offset + len(palette)] != palette:
                continue
            if all(indices[y * width:y * width + nw] == texture.indices[y * width:y * width + nw]
                   for y in range(nh)):
                candidates.append(index)
        assert candidates, ('No complete source-native texture/palette match', key)
        selected = candidates[0]
        texture, record = movie.texture(selected), movie.records[selected]
        nw, nh = record[0] >> 16, record[1] & 65535
        for same in committed['polygons']:
            if (same['texture_parameter'], same['palette']) != key:
                continue
            sampled = plane(same, texture)
            assert all(p is None or (p % width < nw and p // width < nh) for p in sampled)
        bindings[key] = selected
        rows.append({'texture_parameter': param, 'palette': pal, 'source_equivalence_candidates': candidates,
            'native_source_size': [nw, nh], 'native_source_index_cells_exact': nw * nh,
            'complete_original_palette_bytes_exact': len(texture.palette) * 2,
            'every_sampled_texel_inside_verified_native_extent': True,
            'unused_power_of_two_padding_not_assumed_uploaded': True})
    return bindings, rows


def main():
    report = read(CAP / 'capture_report.json')
    rom = NdsImage.open('out/all_routes_combined_v640_candidate.nds')
    movie_sources = {p: rom.read_file(p) for p in ('/FLS/M28.fls', '/FLS/logo.fls')}
    movies = {p: FlsArchive(s) for p, s in movie_sources.items()}
    shots = {s['frame']: s for s in report['frames_captured']}
    rows = []
    for state in report['read_only_capture_GPU_states']:
        frame = state['frame']
        committed = read(state['read_only_committed_geometry']['path'])
        raw = Path(state['files']['arm9_main_ram.bin']['path']).read_bytes()
        active = [p for p, source in movie_sources.items() if find_live(raw, source)]
        assert len(active) == 1
        movie = movies[active[0]]
        bindings, sources = vram_bindings(committed, movie)
        expected, draws = compose(committed['polygons'], movie, bindings)
        comparisons = []
        for lag in range(4):
            if frame + lag not in shots:
                continue
            image = Image.open(shots[frame + lag]['path']).convert('RGB').crop((0, 0, 256, 192))
            actual = list(image.get_flattened_data())
            comparisons.append({'lag': lag, 'RGB_differences': sum(a != b for a, b in zip(expected, actual, strict=True))})
        print(frame, [[d['texture'], d['alpha']] for d in draws], comparisons, flush=True)
        rows.append({'frame': frame, 'actual_live_movie': active[0], 'source_VRAM_bindings': sources, 'native_source_draws': draws,
                     'comparisons': comparisons})
    save(ROOT / 'committed_composition_diagnostic.json', {'cases': rows,
        'texture_and_palette_binding_independent_of_screenshot': True,
        'not_yet_a_final_verification': True})


if __name__ == '__main__':
    main()
