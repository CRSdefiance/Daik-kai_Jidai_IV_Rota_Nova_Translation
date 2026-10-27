"""Source-specific reveal lettering; covered scenery is approximate.

Only the two pinned comic frames may use this rule. Creature/people pixels
are protected independently of text color. No native geometry is inferred.
"""

import hashlib
import math
import struct

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FRAME_BYTES = 153600
BLOCK_SHA = 'c95b9d4b968638d488158c8971c03f4116ac6e6ceb8a6863a4de5a1b05b54464'
SPECS = {
    6: ('えっ！', 'Huh?!', [43, 99, 105, 125], 9),
    7: ('ばあ～～ん！', 'TA-DA!', [0, 0, 320, 114], 28),
}
# Source silhouette vertices include visible outlines and their fringe. These
# are preservation bounds, not a reconstruction of the creature's anatomy.
FOREGROUND = [
    [(116, 29), (121, 26), (128, 28), (131, 41), (134, 51),
     (140, 62), (142, 67), (131, 73), (118, 75), (115, 63)],
    [(174, 27), (181, 27), (187, 32), (191, 46), (191, 59),
     (187, 69), (185, 73), (175, 72), (172, 61)],
    [(100, 94), (110, 82), (121, 73), (130, 67), (146, 63),
     (148, 54), (150, 49), (157, 47), (162, 55), (162, 61),
     (172, 65), (185, 70), (198, 80), (207, 90), (218, 99),
     (228, 102), (233, 111), (230, 120), (94, 120), (94, 103)],
]


def channels(word):
    return tuple((word >> (c * 5)) & 31 for c in range(3))


def mix(a, b, alpha):
    return (a & 32768) | sum(round((x * (255 - alpha) + y * alpha) / 255) << (c * 5)
                             for c, (x, y) in enumerate(zip(channels(a), channels(b), strict=True)))


def protected_mask():
    result = Image.new('L', (320, 240))
    draw = ImageDraw.Draw(result)
    for polygon in FOREGROUND:
        draw.polygon(polygon, fill=255)
    return result.filter(ImageFilter.MaxFilter(3))


def reveal_background(words):
    """Fit visible paper seams, then estimate only masked background pixels."""
    seeds = Image.new('L', (320, 240))
    sp = seeds.load()
    for i, word in enumerate(words[:320 * 114]):
        r, g, b = channels(word)
        if g >= r + 2 and r >= b + 2:
            sp[i % 320, i // 320] = 255
    silhouette = protected_mask().tobytes()
    # Separate the actual blue body / brown-gold horns from green lettering
    # within the broad preservation bounds. Dots in old lettering are paper,
    # not foreground. Neutral outlines follow adjacent foreground colors.
    protection = Image.new('L', (320, 240))
    pp = protection.load()
    for i, word in enumerate(words[:320 * 114]):
        r, g, b = channels(word)
        if silhouette[i] and (b >= r + 2 or (r >= g + 2 and r >= b + 1)
                              or (r >= g and r < 27 and g >= b + 4)):
            pp[i % 320, i // 320] = 255
    near = protection.filter(ImageFilter.MaxFilter(3)).tobytes()
    for i, word in enumerate(words[:320 * 114]):
        r, g, b = channels(word)
        if silhouette[i] and near[i] and max(r, g, b) < 10 and g <= r:
            pp[i % 320, i // 320] = 255
    # Independently reviewed core rectangles include mixed edge colors that
    # are not captured by the hue classifier. Preserve every original word.
    for box in [(119, 34, 129, 62), (178, 35, 185, 62), (152, 56, 159, 94),
                (119, 75, 185, 114)]:
        ImageDraw.Draw(protection).rectangle((box[0], box[1], box[2] - 1, box[3] - 1), fill=255)
    mask = seeds.filter(ImageFilter.MaxFilter(9))
    # Fill small dot/hollow islands enclosed by the decorated source lettering.
    marked = bytearray(mask.tobytes())
    visited = set()
    for y in range(114):
        for x in range(320):
            i = y * 320 + x
            if marked[i] or i in visited:
                continue
            todo, group, edge = [i], [], False
            visited.add(i)
            while todo:
                j = todo.pop()
                group.append(j)
                xx, yy = j % 320, j // 320
                edge |= xx in (0, 319) or yy in (0, 113)
                for nx, ny in ((xx - 1, yy), (xx + 1, yy), (xx, yy - 1), (xx, yy + 1)):
                    k = ny * 320 + nx
                    if 0 <= nx < 320 and 0 <= ny < 114 and not marked[k] and k not in visited:
                        visited.add(k)
                        todo.append(k)
            if not edge and len(group) <= 350:
                for j in group:
                    marked[j] = 255
    protect = protection.tobytes()
    for i in range(len(marked)):
        if protect[i] or i // 320 >= 114:
            marked[i] = 0
    # Initial source-visible top/side seam geometry. Refit against unoccluded
    # samples; no assertion of exact hidden original pixels is made.
    lines = [(52.71, .4696), (100.85, .27), (145., 0.),
             (181.72, -.1742), (230.20, -.4354), (289.03, -.7241),
             (-11., .87), (-94., 1.27), (356., -1.06), (461., -1.60)]
    samples = []
    paper = (22396, 19992)
    excluded = seeds.filter(ImageFilter.MaxFilter(9)).tobytes()
    for y in range(110):
        last = None
        for x in range(320):
            i = y * 320 + x
            if excluded[i] or protect[i]:
                last = None
                continue
            c = channels(words[i])
            distances = [max(abs(a - b) for a, b in zip(c, channels(w), strict=True)) for w in paper]
            cls = distances.index(min(distances)) if min(distances) <= 1 else None
            if cls is None:
                continue
            if last and last[1] != cls and x - last[0] <= 4:
                samples.append(((x + last[0]) / 2, y))
            last = (x, cls)
    fits = []
    for intercept, slope in lines:
        points = [(x, y) for x, y in samples if abs(x - intercept - slope * y) <= 2]
        if len(points) >= 8:
            mx = sum(x for x, _ in points) / len(points)
            my = sum(y for _, y in points) / len(points)
            den = sum((y - my) ** 2 for _, y in points)
            if den:
                slope = sum((x - mx) * (y - my) for x, y in points) / den
                intercept = mx - slope * my
        fits.append((intercept, slope, len(points)))
    result = list(words)
    for i, alpha in enumerate(marked):
        if not alpha:
            continue
        x, y = i % 320, i // 320
        # Below source paper, old letter fringe covers water. Use the nearest
        # unmasked same-row blue/gray sea sample, retaining all unmasked water.
        def horizon(xx):
            return 108 - .125 * xx if xx < 145 else 74 + .113 * xx
        if y >= horizon(x):
            donors = []
            for xx in (range(70) if x < 145 else range(240, 320)):
                yy = min(239, y + max(0, math.ceil(horizon(xx) - horizon(x))))
                j = yy * 320 + xx
                r, g, b = channels(words[j])
                if not marked[j] and not protect[j] and b >= r + 1 and b >= 14:
                    donors.append((xx, yy))
            if donors:
                xx, yy = min(donors, key=lambda p: abs(p[0] - x))
                result[i] = words[yy * 320 + xx]
                continue
        seams = sorted(a + b * y for a, b, _ in fits)
        # Include seams outside the frame: each crossing of the left edge
        # changes the initial paper color automatically, without row stripes.
        cls = 1
        for edge in seams:
            if edge <= x:
                cls = 1 - cls
        result[i] = paper[cls]
    return result, marked, protect, fits


def render_reveal(row, source_region, batch, source_block):
    if source_block is None or hashlib.sha256(source_block).hexdigest() != BLOCK_SHA:
        raise ValueError('Reveal requires exact original block')
    index = row.get('image_index')
    if index not in SPECS:
        raise ValueError('Reveal source frame differs')
    source_text, english, box, size = SPECS[index]
    if (row.get('source_text') != source_text or row.get('english') != english
            or row.get('box') != box or row.get('size') != size):
        raise ValueError('Reveal source/text/format contract differs')
    frame = source_block[index * FRAME_BYTES:(index + 1) * FRAME_BYTES]
    words = list(struct.unpack('<76800H', frame))
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0
    exact = struct.pack(f'<{width * height}H', *(words[y * 320 + x]
                        for y in range(y0, y1) for x in range(x0, x1)))
    if source_region != exact:
        raise ValueError('Reveal source region differs')
    if index == 7:
        restored, erased, protected, fits = reveal_background(words)
        lettering_box = (78, 1, 242, 24)
    else:
        restored, erased, protected, fits = list(words), bytearray(76800), bytes(76800), []
        old_ink = Image.new('L', (320, 240))
        for y in range(101, 124):
            for x in range(92, 103):
                c = channels(words[y * 320 + x])
                if max(c) < 22 and max(c) - min(c) < 6:
                    old_ink.putpixel((x, y), 255)
        fringe = old_ink.filter(ImageFilter.MaxFilter(5)).tobytes()
        for y in range(100, 124):
            for x in range(91, 104):
                i = y * 320 + x
                if not fringe[i]:
                    continue
                donors = [xx for xx in range(90, 105) if not fringe[y * 320 + xx]
                          and channels(words[y * 320 + xx])[2] >= channels(words[y * 320 + xx])[0] + 2
                          and channels(words[y * 320 + xx])[2] > 15]
                xx = min(donors, key=lambda xx: abs(xx - x)) if donors else 90
                erased[i] = 255
                restored[i] = words[y * 320 + xx]
        lettering_box = (45, 108, 87, 123)
    font = ImageFont.truetype(batch['font_file_path'], size)
    mask = Image.new('L', (320, 240))
    bounds = font.getbbox(english)
    left = (lettering_box[0] + lettering_box[2] - (bounds[2] - bounds[0])) // 2 - bounds[0]
    top = (lettering_box[1] + lettering_box[3] - (bounds[3] - bounds[1])) // 2 - bounds[1]
    ImageDraw.Draw(mask).text((left, top), english, font=font, fill=255)
    glyphs = []
    for j, character in enumerate(english):
        glyph = Image.new('L', (320, 240))
        ImageDraw.Draw(glyph).text((left + font.getlength(english[:j]), top), character, font=font, fill=255)
        bbox = glyph.getbbox()
        if bbox is None or bbox[0] < x0 or bbox[1] < y0 or bbox[2] > x1 or bbox[3] > y1:
            raise ValueError('Reveal complete glyph escapes bounds')
        glyphs.append({'character': character, 'bbox': bbox})
    alpha = mask.tobytes()
    outline = mask.filter(ImageFilter.MaxFilter(3)).tobytes() if index == 7 else bytes(76800)
    payload = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            i = y * 320 + x
            if (alpha[i] or outline[i]) and protected[i]:
                raise ValueError('English lettering covers original creature')
            if index == 6 and alpha[i] and x >= 88:
                raise ValueError('Reaction lettering overlaps original photo')
            word = restored[i]
            if outline[i]:
                word = mix(word, 5285, outline[i])
            if alpha[i]:
                # Source green ink with cream dots, keeping the decorated effect.
                ink = 22396 if index == 7 and (x % 7 - 3) ** 2 + (y % 7 - 3) ** 2 <= 2 else (8846 if index == 7 else 0)
                word = mix(word, ink, alpha[i])
            payload.append(word)
    return struct.pack(f'<{len(payload)}H', *payload), {
        'font_size': size, 'automatic_lines': [english], 'full_ink_box': mask.getbbox(),
        'full_mask_sha256': hashlib.sha256(alpha).hexdigest(), 'visible_characters': glyphs,
        'erased_indices': [i for i, v in enumerate(erased) if v],
        'protected_indices': [i for i, v in enumerate(protected) if v], 'paper_fits': fits,
        'original_hidden_scenery_recovered': False, 'actual_native_display_verified': False,
        'brown_water_marks_retained': index == 6}
