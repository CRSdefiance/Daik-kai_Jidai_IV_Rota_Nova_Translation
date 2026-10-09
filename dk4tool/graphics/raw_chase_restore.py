"""Source-bounded chase calls; covered photograph/outline reconstruction is approximate."""

import struct
from collections import Counter
from itertools import pairwise

from PIL import Image, ImageDraw

from dk4tool.graphics.raw_caption_restore import restore_caption

SOURCE_EDGE = [(100, 10), (73, 36), (90, 28), (87, 45), (102, 41),
               (94, 56), (109, 63), (93, 65), (105, 76), (90, 78), (107, 109)]


def channels(word):
    return tuple((word >> (c * 5)) & 31 for c in range(3))


def restore_chase_call(row, source_region, source_block, frame_bytes):
    if row.get('image_index') != 5 or row.get('source_ink') not in ('black', 'red'):
        raise ValueError('Chase restoration requires reviewed source call')
    x0, y0, x1, y1 = row['box']
    width, height = x1 - x0, y1 - y0
    ink_box = row.get('source_ink_box', row['box'])
    if not x0 <= ink_box[0] < ink_box[2] <= x1 or not y0 <= ink_box[1] < ink_box[3] <= y1:
        raise ValueError('Source call ink box escapes ownership')
    old = [v for v, in struct.iter_unpack('<H', source_region)]
    target = struct.unpack('<76800H', source_block[5 * frame_bytes:6 * frame_bytes])
    donor = struct.unpack('<76800H', source_block[4 * frame_bytes:5 * frame_bytes])
    red = row['source_ink'] == 'red'
    seed = set()
    for i, word in enumerate(old):
        r, g, b = channels(word)
        x, y = x0 + i % width, y0 + i // width
        is_ink = r >= g + 4 and r >= b + 4 if red else max(r, g, b) < 15 and max(r, g, b) - min(r, g, b) <= 2
        if (is_ink and ink_box[0] <= x < ink_box[2] and ink_box[1] <= y < ink_box[3]
                and not (y == 51 and 52 <= x < 269 and word == 1057)):
            seed.add(i)
    mask = seed.copy()
    fringe = 3 if red else 2
    protected_outline = set()
    for i, word in enumerate(old):
        if not red or not 8 <= max(channels(word)) <= 30 or max(channels(word)) - min(channels(word)) > 1:
            continue
        x, y = x0 + i % width, y0 + i // width
        white_neighbors = sum(min(channels(target[(y + dy) * 320 + x + dx])) >= 30
                              for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                              if 0 <= x + dx < 320 and 0 <= y + dy < 240)
        if white_neighbors >= 1 or not (52 <= x < 269 and 51 <= y < 192):
            protected_outline.add(i)
    for i in seed:
        x, y = i % width, i // width
        for dx in range(-fringe, fringe + 1):
            for dy in range(-fringe, fringe + 1):
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    adjacent = (y + dy) * width + x + dx
                    if old[adjacent] != 32767:
                        mask.add(adjacent)
    mask.difference_update(protected_outline)
    counts = [[Counter() for _ in range(32)] for _ in range(3)]
    training = []
    for y in range(52, 191):
        for x in range(53, 268):
            if y < 114 and not 110 <= x < 169:
                continue
            a, b = channels(donor[y * 320 + x]), channels(target[y * 320 + x])
            if min(a) >= 16:
                continue  # original frame4's white creator/title overlays
            training.append((a, b))
            for c in range(3):
                counts[c][a[c]][b[c]] += 1
    mapping = [[h.most_common(1)[0][0] if h else None for h in bank] for bank in counts]
    disagreement = sum(any(mapping[c][a[c]] != b[c] for c in range(3)) for a, b in training)
    background_donor = list(donor)
    title_box = (33, 24, 230, 61)
    title_raw = struct.pack('<7289H', *(donor[y * 320 + x] for y in range(24, 61) for x in range(33, 230)))
    title_background, _ = restore_caption({'image_index': 4, 'box': list(title_box), 'background': 15855},
                                          title_raw, source_block, frame_bytes)
    for i, word in enumerate(title_background):
        background_donor[(24 + i // 197) * 320 + 33 + i % 197] = word
    outline_mask = Image.new('L', (width * 4, height * 4))
    ImageDraw.Draw(outline_mask).line([((x - x0) * 4, (y - y0) * 4) for x, y in SOURCE_EDGE], fill=255, width=4)
    outline_alpha = outline_mask.resize((width, height), Image.Resampling.LANCZOS).tobytes()

    def white_foreground(x, y):
        for (ax, ay), (bx, by) in pairwise(SOURCE_EDGE[4:]):
            if ay <= y <= by:
                edge_x = ax + (bx - ax) * (y - ay) / (by - ay)
                return x < edge_x
        return False
    restored = old.copy()
    approximate, inferred_white = [], []
    for i in sorted(mask):
        x, y = x0 + i % width, y0 + i // width
        if not (52 <= x < 269 and 51 <= y < 192):
            value = 32767
        else:
            neighbors = []
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                xx, yy = x + dx, y + dy
                while 0 <= xx < 320 and 0 <= yy < 240:
                    local = (yy - y0) * width + xx - x0
                    if not (x0 <= xx < x1 and y0 <= yy < y1 and local in mask):
                        neighbors.append((abs(xx - x) + abs(yy - y), target[yy * 320 + xx]))
                        break
                    xx += dx; yy += dy
            if red and white_foreground(x, y):
                value = 32767
                inferred_white.append(i)
            elif y == 51:
                value = 1057
            else:
                a = channels(background_donor[y * 320 + x])
                mapped = tuple(mapping[c][a[c]] for c in range(3))
                if min(a) < 16 and all(v is not None for v in mapped):
                    value = sum(v << (c * 5) for c, v in enumerate(mapped))
                elif neighbors:
                    value = min(neighbors, key=lambda pair: pair[0])[1] & 32767
                else:
                    raise ValueError('Chase restoration lacks source background')
            approximate.append(i)
        if red and outline_alpha[i]:
            alpha = outline_alpha[i]
            value = sum(round((c * (255 - alpha) + 16 * alpha) / 255) << (index * 5)
                        for index, c in enumerate(channels(value)))
        restored[i] = (old[i] & 0x8000) | value
    return restored, {'source_glyph_mask_indices': sorted(mask), 'source_ink_seed_indices': sorted(seed),
                          'protected_outline_indices': sorted(protected_outline),
                          'covered_outline_path_inferred_from_visible_source': SOURCE_EDGE if red else [],
                          'covered_outline_recovery_is_exact': False,
                          'source_antialias_fringe_radius': fringe, 'approximate_background_indices': approximate,
                          'inferred_white_foreground_indices': inferred_white, 'donor_frame_index': 4,
                          'donor_training_pairs': len(training), 'donor_inexact_training_pairs': disagreement,
                          'concealed_original_recovered': False}
