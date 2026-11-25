"""Source-derived bounded software sampling for axis-aligned opaque photos.

Research implementation of the pinned core's clipping/edge interpolants. It is
not a generic DS GPU emulator. Each failed comparison remains in the output.
"""

import math
import struct
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/ending_gpu_state_v630')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ending_gpu_v630_maria')


def f32(value):
    return struct.unpack('<f', struct.pack('<f', value))[0]


def geometry(raw):
    version, count = struct.unpack_from('<2I', raw)
    assert version == 4 and count <= 80000 and 8 + count * 39 + 4 <= len(raw)
    vertices = [list(struct.unpack_from('<6f', raw, 8 + i * 39)) for i in range(count)]
    colors = [list(raw[8 + i * 39 + 24:8 + i * 39 + 27]) for i in range(count)]
    position = 8 + count * 39
    polys = struct.unpack_from('<I', raw, position)[0]
    position += 4
    assert polys <= 20000 and position + polys * 36 <= len(raw)
    rows = []
    for i in range(polys):
        words = struct.unpack_from('<I4H4I2f', raw, position + i * 36)
        assert words[0] in (3, 4) and all(j < count for j in words[1:1 + words[0]])
        rows.append({'indices': list(words[1:1 + words[0]]), 'attributes': words[5],
                     'texture_parameter': words[6], 'palette': words[7], 'viewport': words[8],
                     'vertices': [vertices[j] for j in words[1:1 + words[0]]],
                     'vertex_colors_RGB6': [colors[j] for j in words[1:1 + words[0]]]})
    return rows


def clip(vertices):
    # gfx3d.cpp clipPoint/ClipperPlane: inside->outside interpolation; force
    # the intersected coordinate to the plane. The order is left/right/bottom/
    # top/front/back. These source photos have constant homogeneous w=1.
    for coord, which in ((0, -1), (0, 1), (1, -1), (1, 1), (2, -1), (2, 1)):
        result = []
        for old, new in zip(vertices, vertices[1:] + vertices[:1], strict=True):
            out_old = old[coord] < -old[3] if which == -1 else old[coord] > old[3]
            out_new = new[coord] < -new[3] if which == -1 else new[coord] > new[3]
            if out_old != out_new:
                inside, outside = (new, old) if out_old else (old, new)
                win, wout = which * inside[3], which * outside[3]
                ratio = f32(f32(inside[coord] - win) /
                            f32(f32(wout - win) - f32(outside[coord] - inside[coord])))
                point = [f32(a + f32(f32(b - a) * ratio)) for a, b in zip(inside, outside, strict=True)]
                point[coord] = which * point[3]
                result.append(point)
            if not out_new:
                result.append(new)
        vertices = result
        if not vertices:
            break
    return vertices


def rgb_palette(texture):
    result = []
    for r, g, b, alpha in texture.palette:
        r, g, b = ((v * 31 + 127) // 255 for v in (r, g, b))
        g6 = (g << 1) | (g >> 4)
        result.append((r * 255 // 31, g6 * 255 // 63, b * 255 // 31))
    return result


def sample(poly, texture):
    assert poly['attributes'] >> 16 & 31 == 31
    assert poly['viewport'] == 0xBFFF0000
    assert all(v[3] == 1 for v in poly['vertices'])
    projected = []
    for vertex in clip(poly['vertices']):
        x, y, _z, w, u, v = vertex
        # performCoordAdjustment calls iround(), whose actual source is a
        # truncating int cast, not mathematical rounding to nearest.
        sx = f32(f32(f32(x + w) / f32(2 * w)) * 256)
        sy = f32(192 - f32(f32(f32(y + w) / f32(2 * w)) * 192))
        projected.append([int(f32(sx * 16)), int(f32(sy * 16)), u, v])
    assert len(projected) == 4
    xs, ys = sorted({v[0] for v in projected}), sorted({v[1] for v in projected})
    assert len(xs) == len(ys) == 2
    corners = {(v[0], v[1]): v for v in projected}
    tl, tr, bl, br = (corners[x, y] for x, y in ((xs[0], ys[0]), (xs[1], ys[0]),
                                                (xs[0], ys[1]), (xs[1], ys[1])))
    x0, x1 = (math.ceil(v / 16) for v in xs)
    y0, y1 = (math.ceil(v / 16) for v in ys)
    assert 0 <= x0 < x1 <= 256 and 0 <= y0 < y1 <= 192
    width = x1 - x0
    dy = f32(1 / f32((ys[1] - ys[0]) / 16))
    yprestep = f32((y0 * 16 - ys[0]) / 16)
    left_step = [f32(dy * f32(b - a)) for a, b in zip(tl[2:], bl[2:], strict=True)]
    right_step = [f32(dy * f32(b - a)) for a, b in zip(tr[2:], br[2:], strict=True)]
    left = [f32(a + f32(yprestep * step)) for a, step in zip(tl[2:], left_step, strict=True)]
    right = [f32(a + f32(yprestep * step)) for a, step in zip(tr[2:], right_step, strict=True)]
    result = [(0, 0, 0)] * (256 * 192)
    palette = rgb_palette(texture)
    sampled = []
    for y in range(y0, y1):
        uv = left[:]
        steps = [f32(f32(b - a) * f32(1 / width)) for a, b in zip(left, right, strict=True)]
        for x in range(x0, x1):
            sx, sy = (math.floor(value) for value in uv)
            # Source texture parameter is clamp in each axis, no wrap/flip.
            sx, sy = max(0, min(texture.width - 1, sx)), max(0, min(texture.height - 1, sy))
            index = sy * texture.width + sx
            result[y * 256 + x] = palette[texture.indices[index]]
            sampled.append(index)
            uv = [f32(a + step) for a, step in zip(uv, steps, strict=True)]
        left = [f32(a + step) for a, step in zip(left, left_step, strict=True)]
        right = [f32(a + step) for a, step in zip(right, right_step, strict=True)]
    return result, {'clipped_projected_vertices_FX4_UV': projected, 'painted_bounds': [x0, y0, x1, y1],
                    'distinct_source_texels': len(set(sampled)),
                    'source_texel_for_negative_control': sampled[len(sampled) // 2]}


def main():
    rom = NdsImage.open('out/all_routes_combined_v627_candidate.nds')
    tex = FlsArchive(rom.read_file('/FLS/M32.fls')).texture(4)
    rows = []
    for frame in (8320, 8640, 8960, 9280, 9360, 9600, 10240):
        path = CAP / f'capture_gpu_state_{frame:06d}/gpu_geometry_chunk91.bin'
        polys = geometry(path.read_bytes())
        photo = [p for p in polys if p['texture_parameter'] == 0x52D00004 and p['palette'] == 2]
        assert len(photo) == 1
        predicted, details = sample(photo[0], tex)
        image = Image.open(CAP / f'frame_{frame:06d}_cold_boot.png').convert('RGB').crop((0, 0, 256, 192))
        actual = list(image.get_flattened_data())
        differences = [i for i, (a, b) in enumerate(zip(actual, predicted, strict=True)) if a != b]
        row = {'frame': frame, **details, 'RGB_differences': len(differences),
               'first_differing_pixels': [(i % 256, i // 256, actual[i], predicted[i]) for i in differences[:8]]}
        rows.append(row)
        preview = Image.new('RGB', (256, 192))
        preview.putdata(predicted)
        preview.save(ROOT / f'M32_{frame:06d}_CLIPPED_SOURCE_REPLAY.png')
    save(ROOT / 'clipped_sampling_diagnostic.json', rows)
    print([(r['frame'], r['RGB_differences']) for r in rows])


if __name__ == '__main__':
    main()
