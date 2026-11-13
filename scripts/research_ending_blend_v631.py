"""Bounded original M30 source planes and native six-bit alpha composition."""

import math
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.rom.nds import NdsImage
from scripts.research_photo_sampler_v630 import clip, f32, geometry
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/ending_gpu_v631')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ending_gpu_v631_hodram_adjacent')
BINDINGS = {(0x4C000000, 0): 0, (0x52500004, 2): 1, (0x52501004, 34): 2,
            (0x52502004, 66): 3, (0x6DD03004, 98): 4, (0x52D03404, 100): 5}


def plane(poly, texture):
    vertices = clip(poly['vertices'])
    if len(vertices) < 3:
        return [None] * (256 * 192)
    points = []
    for x, y, _z, w, u, v in vertices:
        assert w == 1
        sx = f32(f32(f32(x + w) / f32(2 * w)) * 256)
        sy = f32(192 - f32(f32(f32(y + w) / f32(2 * w)) * 192))
        points.append([int(f32(sx * 16)), int(f32(sy * 16)), u, v])
    xs, ys = sorted({p[0] for p in points}), sorted({p[1] for p in points})
    if len(xs) < 2 or len(ys) < 2:
        return [None] * (256 * 192)
    assert len(points) == 4 and len(xs) == len(ys) == 2
    corners = {(p[0], p[1]): p for p in points}
    tl, tr, bl, br = (corners[x, y] for x, y in ((xs[0], ys[0]), (xs[1], ys[0]),
                                                (xs[0], ys[1]), (xs[1], ys[1])))
    x0, x1 = (math.ceil(x / 16) for x in xs)
    y0, y1 = (math.ceil(y / 16) for y in ys)
    assert 0 <= x0 <= x1 <= 256 and 0 <= y0 <= y1 <= 192
    if x0 == x1 or y0 == y1:
        return [None] * (256 * 192)
    dy = f32(1 / f32((ys[1] - ys[0]) / 16))
    prestep = f32((y0 * 16 - ys[0]) / 16)
    ls = [f32(dy * f32(b - a)) for a, b in zip(tl[2:], bl[2:], strict=True)]
    rs = [f32(dy * f32(b - a)) for a, b in zip(tr[2:], br[2:], strict=True)]
    left = [f32(a + f32(prestep * s)) for a, s in zip(tl[2:], ls, strict=True)]
    right = [f32(a + f32(prestep * s)) for a, s in zip(tr[2:], rs, strict=True)]
    output = [None] * (256 * 192)
    for y in range(y0, y1):
        uv = left[:]
        steps = [f32(f32(b - a) * f32(1 / (x1 - x0))) for a, b in zip(left, right, strict=True)]
        for x in range(x0, x1):
            sx, sy = (math.floor(value) for value in uv)
            sx, sy = max(0, min(texture.width - 1, sx)), max(0, min(texture.height - 1, sy))
            output[y * 256 + x] = sy * texture.width + sx
            uv = [f32(a + s) for a, s in zip(uv, steps, strict=True)]
        left = [f32(a + s) for a, s in zip(left, ls, strict=True)]
        right = [f32(a + s) for a, s in zip(right, rs, strict=True)]
    return output


def sixbit_palette(texture):
    values = []
    for color in texture.palette:
        five = [(v * 31 + 127) // 255 for v in color[:3]]
        values.append(tuple(2 * v + (1 if v else 0) for v in five))
    return values


def compose(polys, movie):
    # These source polygons have strictly ordered constant depths, flat white
    # lighting and at most one translucent photo over opaque painted scenery.
    # This is a bounded compositor for that case, not arbitrary DS depth/alpha.
    result, depth = [(0, 0, 0)] * (256 * 192), [float('inf')] * (256 * 192)
    counts = []
    for poly in polys:
        binding = (poly['texture_parameter'], poly['palette'])
        assert binding in BINDINGS
        texture_id = BINDINGS[binding]
        tex = movie.texture(texture_id)
        assert poly['vertex_colors_RGB6'] == [[63, 63, 63]] * len(poly['vertices'])
        assert poly['attributes'] >> 4 & 3 == 0
        alpha = poly['attributes'] >> 16 & 31
        assert alpha
        z = poly['vertices'][0][2]
        assert all(v[2] == z for v in poly['vertices'])
        transparent_zero = bool(poly['texture_parameter'] & (1 << 29))
        palette = sixbit_palette(tex)
        locations = plane(poly, tex)
        drawn = 0
        for position, source in enumerate(locations):
            if source is None or z > depth[position]:
                continue
            index = tex.indices[source]
            if transparent_zero and index == 0:
                continue
            color = palette[index]
            if alpha == 31:
                result[position] = color
                depth[position] = z
            else:
                a = alpha + 1
                result[position] = tuple((a * s + (32 - a) * d) >> 5
                                         for s, d in zip(color, result[position], strict=True))
            drawn += 1
        counts.append({'texture': texture_id, 'alpha': alpha, 'drawn_pixels': drawn})
    rgb = []
    for r6, g6, b6 in result:
        r, g, b = r6 >> 1, g6 >> 1, b6 >> 1
        g_out = (g << 1) | (g >> 4)
        rgb.append((r * 255 // 31, g_out * 255 // 63, b * 255 // 31))
    return rgb, counts


def main():
    movie = FlsArchive(NdsImage.open('out/all_routes_combined_v627_candidate.nds').read_file('/FLS/M30.fls'))
    results = []
    for source_frame in (13358, 13359, 13360):
        polys = geometry((CAP / f'capture_gpu_state_{source_frame:06d}/gpu_geometry_chunk91.bin').read_bytes())
        predicted, counts = compose(polys, movie)
        frame = source_frame + 2
        actual = list(Image.open(CAP / f'frame_{frame:06d}_cold_boot.png').convert('RGB').crop((0, 0, 256, 192)).get_flattened_data())
        diff = [i for i, (a, b) in enumerate(zip(actual, predicted, strict=True)) if a != b]
        results.append({'source_geometry_frame': source_frame, 'display_frame': frame,
                        'RGB_differences': len(diff), 'draws': counts,
                        'first_differences': [(i % 256, i // 256, actual[i], predicted[i]) for i in diff[:8]]})
        im = Image.new('RGB', (256, 192))
        im.putdata(predicted)
        im.save(ROOT / f'M30_{frame:06d}_SOURCE_BLEND_REPLAY.png')
    save(ROOT / 'source_blend_diagnostic.json', results)
    print([(r['display_frame'], r['RGB_differences']) for r in results])


if __name__ == '__main__':
    main()
