"""Source-derived white-caption masks; concealed scenery is explicitly approximate."""

import struct
from collections import Counter

PHOTO_BOXES = {4: (52, 51, 269, 192), 10: (52, 43, 269, 184)}


def restore_caption(row, source_region, source_block, frame_bytes):
    frame = row["image_index"]
    if frame not in PHOTO_BOXES or row.get("background") != 15855:
        raise ValueError("Caption restoration requires reviewed gray-canvas comic")
    photo = PHOTO_BOXES[frame]
    x0, y0, x1, y1 = row["box"]
    width = x1 - x0
    words = list(struct.unpack('<76800H', source_block[frame * frame_bytes:(frame + 1) * frame_bytes]))
    old = [v for v, in struct.iter_unpack('<H', source_region)]
    def channels(word):
        return tuple((word >> (c * 5)) & 31 for c in range(3))
    # Bright neutral ink is distinct from the dim photograph/15-level gray canvas.
    mask = {i for i, word in enumerate(old) if min(channels(word)) >= 16
            and max(channels(word)) - min(channels(word)) <= 1}
    # Composite antialias edges inherit the photograph's hue and can fall below
    # the neutral threshold. Review requires the whole two-pixel source fringe.
    seeds = mask.copy()
    for i in seeds:
        x, y = i % width, i // width
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if 0 <= x + dx < width and 0 <= y + dy < y1 - y0:
                    adjacent = (y + dy) * width + x + dx
                    if old[adjacent] != 15855:
                        mask.add(adjacent)
    # Source antialias on a photo border can be dimmer than the canvas. Only
    # include altered border pixels connected to the already selected lettering.
    px0, py0, px1, py1 = photo
    donor_index = 5 if frame == 4 else 9
    donor = struct.unpack('<76800H', source_block[donor_index * frame_bytes:(donor_index + 1) * frame_bytes])

    def donor_clear(x, y):
        # Frame5's upper speech/call overlays obscure this same photograph.
        return frame == 10 or y >= 114 or 110 <= x < 170

    counts = [[Counter() for _ in range(32)] for _ in range(3)]
    pairs = []
    for y in range(py0 + 1, py1 - 1):
        for x in range(px0 + 1, px1 - 1):
            if not donor_clear(x, y):
                continue
            i = (y - y0) * width + x - x0
            target_rgb = channels(words[y * 320 + x])
            if (x0 <= x < x1 and y0 <= y < y1 and i in mask) or min(target_rgb) >= 16:
                continue
            donor_rgb = channels(donor[y * 320 + x])
            pairs.append((donor_rgb, target_rgb))
            for c in range(3):
                counts[c][donor_rgb[c]][target_rgb[c]] += 1
    mapping = [[hist.most_common(1)[0][0] if hist else None for hist in bank] for bank in counts]
    disagreements = sum(any(mapping[c][a[c]] != b[c] for c in range(3)) for a, b in pairs)
    border_seed = mask.copy()
    border_references = {
        'top': Counter(words[py0 * 320 + x] for x in range(px0, px1)).most_common(1)[0][0],
        'bottom': Counter(words[(py1 - 1) * 320 + x] for x in range(px0, px1)).most_common(1)[0][0],
        'left': Counter(words[y * 320 + px0] for y in range(py0 + 1, py1 - 1)).most_common(1)[0][0],
        'right': Counter(words[y * 320 + px1 - 1] for y in range(py0 + 1, py1 - 1)).most_common(1)[0][0],
    }

    def border_word(x, y):
        side = 'top' if y == py0 else 'bottom' if y == py1 - 1 else 'left' if x == px0 else 'right'
        return border_references[side]
    for y in range(y0, y1):
        for x in range(x0, x1):
            if ((x in (px0, px1 - 1) and py0 <= y < py1)
                    or (y in (py0, py1 - 1) and px0 <= x < px1)):
                i = (y - y0) * width + x - x0
                expected_border = border_word(x, y)
                connected = any((y + dy - y0) * width + x + dx - x0 in border_seed
                                for dy in range(-2, 3) for dx in range(-2, 3)
                                if x0 <= x + dx < x1 and y0 <= y + dy < y1)
                if old[i] != expected_border and len(set(channels(old[i]))) == 1 and connected:
                    mask.add(i)
    restored = old.copy()
    estimated = []
    donor_estimated = []
    border, canvas = [], []
    for i in sorted(mask):
        x, y = x0 + i % width, y0 + i // width
        if not px0 <= x < px1 or not py0 <= y < py1:
            value = 15855
            canvas.append(i)
        elif x in (px0, px1 - 1) or y in (py0, py1 - 1):
            value = border_word(x, y)
            border.append(i)
        else:
            donor_rgb = channels(donor[y * 320 + x])
            mapped = tuple(mapping[c][donor_rgb[c]] for c in range(3))
            if donor_clear(x, y) and all(v is not None for v in mapped):
                value = sum(v << (c * 5) for c, v in enumerate(mapped))
                restored[i] = (old[i] & 0x8000) | value
                estimated.append(i)
                donor_estimated.append(i)
                continue
            samples = []
            for direction in (-1, 1):
                xx = x + direction
                while px0 < xx < px1 - 1:
                    candidate = words[y * 320 + xx]
                    ci = (y - y0) * width + xx - x0
                    if not (x0 <= xx < x1 and ci in mask):
                        samples.append((abs(xx - x), channels(candidate)))
                        break
                    xx += direction
            if not samples:
                raise ValueError("Caption restoration lacks adjacent source scenery")
            if len(samples) == 1:
                rgb = samples[0][1]
            else:
                (da, a), (db, b) = samples
                rgb = tuple(round((a[c] * db + b[c] * da) / (da + db)) for c in range(3))
            value = sum(v << (c * 5) for c, v in enumerate(rgb))
            estimated.append(i)
        restored[i] = (old[i] & 0x8000) | value
    return restored, {"source_glyph_mask_indices": sorted(mask),
                      "exact_gray_canvas_restoration_indices": canvas,
                      "source_reference_border_restoration_indices": border,
                      "initial_glyph_fringe_mask_indices": sorted(border_seed),
                      "source_border_reference_words": border_references,
                      "estimated_scenery_indices": estimated,
                      "estimated_scenery_is_recovered_original": False,
                      "source_photo_donor_image_index": donor_index,
                      "donor_estimated_scenery_indices": donor_estimated,
                      "donor_training_sample_pairs": len(pairs),
                      "donor_modal_mapping_inexact_training_pairs": disagreements,
                      "donor_is_exact_original_recovery": False,
                      "source_antialias_fringe_radius": 2,
                      "photo_box": photo}
