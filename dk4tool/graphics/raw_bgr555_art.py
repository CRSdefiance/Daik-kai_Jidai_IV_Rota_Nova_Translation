"""Bounded artwork edits to the reviewed, headerless legacy gallery block.

The partition is an inspected storage interpretation, not native loader proof.
Never infer dimensions from arbitrary raw blocks or reinterpret a PXL header.
"""

import hashlib
import json
import struct
import zlib
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_caption_restore import restore_caption
from dk4tool.graphics.raw_chase_restore import restore_chase_call
from dk4tool.graphics.raw_maria_tiles import render_maria_speech, render_maria_tiles
from dk4tool.graphics.raw_reveal_comic import render_reveal

FORMAT = "dk4-ilnk-raw-bgr555-art-batch-v1"
BLOCK_SHA = "c95b9d4b968638d488158c8971c03f4116ac6e6ceb8a6863a4de5a1b05b54464"
FRAME_BYTES = 320 * 240 * 2


def sha(data):
    return hashlib.sha256(data).hexdigest()


def render_region_payload(row, source_region: bytes, batch, source_block=None):
    """Recreate full English from the exact font; payload checks alone are insufficient."""
    font_path = Path(batch["font_file_path"])
    if sha(font_path.read_bytes()) != batch["font_sha256"]:
        raise ValueError("Raw BGR555 English font identity differs")
    rule = row.get("background_rule")
    if rule == "source-reveal-comic-v7":
        return render_reveal(row, source_region, batch, source_block)
    if rule == "source-maria-decorative-title-v6":
        return render_maria_tiles(row, source_region, batch, source_block)
    if rule == "source-maria-chinese-bubble-v6":
        return render_maria_speech(row, source_region, batch, source_block)
    if rule not in {"neutral-ink-erasure-protect-connected-art-v1", "background-aware-connected-art-v2",
                    "source-white-caption-mask-local-scenery-v3", "source-chase-call-mask-background-v4",
                    "source-chase-bubble-interior-v4"}:
        raise ValueError("Raw BGR555 background ownership rule differs")
    x0, y0, x1, y1 = row["box"]
    width, height = x1 - x0, y1 - y0
    pixel_width, pixel_height = width, height
    text_box = row.get("text_box", [0, 0, width, height])
    if (not isinstance(text_box, list) or len(text_box) != 4
            or not 0 <= text_box[0] < text_box[2] <= width
            or not 0 <= text_box[1] < text_box[3] <= height):
        raise ValueError("Caption text box escapes ownership")
    tx, ty, tw, th = text_box
    width, height = tw - tx, th - ty
    rotation = int(row.get("rotation", 0))
    if rotation not in (0, -90):
        raise ValueError("Raw BGR555 artwork rotation differs")
    if rotation and row.get("text_box") is not None:
        raise ValueError("Caption text box cannot use rotation")
    if rotation == -90:
        width, height = height, width
    bg = int(row["background"])
    size_start = int(row["size"])
    if not 0 <= bg < 32768 or not 4 <= size_start <= 64:
        raise ValueError("Raw BGR555 background/font size differs")
    ink = int(row.get("ink_word", 0 if bg == 32767 else 32767))
    if not 0 <= ink < 32768:
        raise ValueError("Raw BGR555 ink color differs")
    for size in range(size_start, 3, -1):
        font = ImageFont.truetype(str(font_path), size)
        lines, current = [], ""
        for word in row["english"].split():
            trial = (current + " " + word).strip()
            if font.getlength(trial) > width - 2 and current:
                lines.append(current)
                current = word
            else:
                current = trial
        lines.append(current)
        boxes = [font.getbbox(line) for line in lines]
        line_height = max(b[3] - b[1] for b in boxes)
        total_height = len(lines) * line_height + (len(lines) - 1) * 2
        if any(b[2] - b[0] > width - 2 for b in boxes) or total_height > height - 2:
            continue
        mask = Image.new("L", (width, height))
        draw = ImageDraw.Draw(mask)
        top = (height - total_height) // 2
        glyphs = []
        for line, bounds in zip(lines, boxes, strict=True):
            left = (width - (bounds[2] - bounds[0])) // 2 - bounds[0]
            y = top - bounds[1]
            draw.text((left, y), line, font=font, fill=255)
            for index, character in enumerate(line):
                if character == " ":
                    continue
                gx = left + font.getlength(line[:index])
                box = font.getbbox(character)
                if gx + box[0] < 0 or gx + box[2] > width or y + box[1] < 0 or y + box[3] > height:
                    raise ValueError("Individual English glyph would be clipped")
                glyph = Image.new("L", (width, height))
                ImageDraw.Draw(glyph).text((gx, y), character, font=font, fill=255)
                if glyph.getbbox() is None:
                    raise ValueError("Dropped/blank individual English character")
                glyphs.append({"character": character, "bbox": glyph.getbbox()})
            top += line_height + 2
        break
    else:
        raise ValueError("Complete English phrase does not fit")
    if rotation == -90:
        mask = mask.transpose(Image.Transpose.ROTATE_270)
        glyphs = [dict(g, bbox=(height - g["bbox"][3], g["bbox"][0],
                                height - g["bbox"][1], g["bbox"][2])) for g in glyphs]
    width, height = pixel_width, pixel_height
    if row.get("text_box") is not None:
        physical_mask = Image.new("L", (width, height))
        physical_mask.paste(mask, (tx, ty))
        mask = physical_mask
        glyphs = [dict(g, bbox=(g["bbox"][0] + tx, g["bbox"][1] + ty,
                                g["bbox"][2] + tx, g["bbox"][3] + ty)) for g in glyphs]
    if len(source_region) != width * height * 2:
        raise ValueError("Source text plane extent differs")
    source_words = [v for v, in struct.iter_unpack("<H", source_region)]
    if rule == "source-chase-call-mask-background-v4":
        if source_block is None or sha(source_block) != BLOCK_SHA:
            raise ValueError("Chase restoration requires exact original block")
        restored, restoration = restore_chase_call(row, source_region, source_block, FRAME_BYTES)
        payload = []
        outline = set(restoration['protected_outline_indices'])
        for i, (old, background, alpha) in enumerate(zip(source_words, restored, mask.tobytes(), strict=True)):
            if alpha and i in outline:
                raise ValueError("New call letters cover original bubble outline")
            if alpha and y0 + i // width == 51:
                raise ValueError("New call letters cover photo border")
            new = (old & 0x8000) | sum(round((((background >> (c * 5)) & 31) * (255 - alpha)
                                           + ((ink >> (c * 5)) & 31) * alpha) / 255) << (c * 5) for c in range(3))
            payload.append(new)
        return struct.pack(f"<{len(payload)}H", *payload), {
            "font_size": size, "automatic_lines": lines, "full_mask_sha256": sha(mask.tobytes()),
            "full_ink_box": mask.getbbox(), "visible_characters": glyphs,
            "rotation": rotation, "restoration": restoration,
        }
    if rule == "source-white-caption-mask-local-scenery-v3":
        if source_block is None or sha(source_block) != BLOCK_SHA:
            raise ValueError("Caption restoration requires exact original block")
        restored, restoration = restore_caption(row, source_region, source_block, FRAME_BYTES)
        payload = []
        px0, py0, px1, py1 = restoration["photo_box"]
        for i, (old, background, alpha) in enumerate(zip(source_words, restored, mask.tobytes(), strict=True)):
            x, y = x0 + i % width, y0 + i // width
            if alpha and px0 <= x < px1 and py0 <= y < py1:
                raise ValueError("New caption letters overlap original photo or border")
            new = (old & 0x8000) | sum(round((((background >> (c * 5)) & 31) * (255 - alpha)
                                           + ((ink >> (c * 5)) & 31) * alpha) / 255) << (c * 5) for c in range(3))
            payload.append(new)
        return struct.pack(f"<{len(payload)}H", *payload), {
            "font_size": size, "automatic_lines": lines, "full_mask_sha256": sha(mask.tobytes()),
            "full_ink_box": mask.getbbox(), "visible_characters": glyphs,
            "rotation": rotation, "restoration": restoration,
        }
    channel_words = [[(v >> (c * 5)) & 31 for c in range(3)] for v in source_words]
    bg_channels = [(bg >> (c * 5)) & 31 for c in range(3)]
    protected_offsets = {i for i, channels in enumerate(channel_words) if max(channels) - min(channels) > 2}
    pending = deque(protected_offsets)
    while pending:
        i = pending.popleft()
        x, y = i % width, i // width
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if not 0 <= x + dx < width or not 0 <= y + dy < height:
                    continue
                adjacent = (y + dy) * width + x + dx
                connected_foreground = (
                    max(channel_words[adjacent]) < 30 if rule == "neutral-ink-erasure-protect-connected-art-v1"
                    else max(abs(v - b) for v, b in zip(channel_words[adjacent], bg_channels, strict=True)) > 2
                )
                if adjacent not in protected_offsets and connected_foreground:
                    protected_offsets.add(adjacent)
                    pending.append(adjacent)
    # Retain the faint one-pixel antialias fringe around each connected art edge.
    expanded = set(protected_offsets)
    for i in protected_offsets:
        x, y = i % width, i // width
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if 0 <= x + dx < width and 0 <= y + dy < height:
                    adjacent = (y + dy) * width + x + dx
                    if source_words[adjacent] != bg:
                        expanded.add(adjacent)
    protected_offsets = expanded
    if rule == "source-chase-bubble-interior-v4":
        if (row.get("image_index") != 5 or bg != 32767 or ink != 0
                or row["box"] not in ([20, 15, 73, 91], [230, 18, 268, 92])):
            raise ValueError("Bubble interior requires reviewed chase artwork")
        # Both locked rectangles are reviewed white text interiors. Tiny red-call
        # fringe in the left text plane is old lettering, not portrait artwork.
        protected_offsets = set()
    for box in row.get("protected_source_boxes", []):
        if (not isinstance(box, list) or len(box) != 4
                or not x0 <= box[0] < box[2] <= x1 or not y0 <= box[1] < box[3] <= y1):
            raise ValueError("Protected source box escapes ownership")
        bx0, by0, bx1, by1 = box
        protected_offsets.update((y - y0) * width + x - x0
                                 for y in range(by0, by1) for x in range(bx0, bx1))
    payload, protected = [], 0
    for i, (old, alpha) in enumerate(zip(source_words, mask.tobytes(), strict=True)):
        if i in protected_offsets:
            if alpha:
                raise ValueError("New letters cover protected connected portrait art")
            new = old
            protected += 1
        else:
            new = (old & 0x8000) | sum(round((((bg >> (c * 5)) & 31) * (255 - alpha)
                                          + ((ink >> (c * 5)) & 31) * alpha) / 255) << (c * 5) for c in range(3))
        payload.append(new)
    return struct.pack(f"<{len(payload)}H", *payload), {
        "font_size": size, "automatic_lines": lines, "full_mask_sha256": sha(mask.tobytes()),
        "full_ink_box": mask.getbbox(), "visible_characters": glyphs,
        "protected_colored_indices": protected, "rotation": rotation,
    }


def apply_raw_bgr555_art(batch_path: Path, source: bytes) -> tuple[bytes, list[str]]:
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    if batch.get("format") != FORMAT or batch.get("source_file_sha256") != sha(source):
        raise ValueError("Raw BGR555 format/source SHA-256 mismatch")
    if (batch.get("file_path") != "/GRP/SLACKIMG.DK4"
            or batch.get("storage_layout") != "reviewed-slackimg19-21x320x240-bgr555"
            or batch.get("editorial_policy") != "natural-dialogue-v2"
            or batch.get("target_locale") != "en-US"):
        raise ValueError("Raw BGR555 reviewed layout/editorial policy differs")
    archive = IlnkContainer.parse(source)
    if len(archive.blocks) != 21 or sha(archive.blocks[19]) != BLOCK_SHA:
        raise ValueError("Raw BGR555 source block differs")
    original = archive.blocks[19]
    if len(original) != 21 * FRAME_BYTES:
        raise ValueError("Raw BGR555 block extent differs")
    records = batch.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("Raw BGR555 artwork requires records")
    output = bytearray(original)
    owned = set()
    ids = []
    for row in records:
        record_id = str(row.get("id", ""))
        frame = int(row.get("image_index", -1))
        if not record_id or record_id in ids or not 0 <= frame < 21:
            raise ValueError("Raw BGR555 duplicate/invalid record or frame")
        if (row.get("source_block_sha256") != BLOCK_SHA
                or row.get("dimensions") != [320, 240] or row.get("block_index") != 19):
            raise ValueError("Raw BGR555 locked dimensions/block differ")
        frame_raw = original[frame * FRAME_BYTES:(frame + 1) * FRAME_BYTES]
        if row.get("source_frame_sha256") != sha(frame_raw):
            raise ValueError("Raw BGR555 source frame differs")
        review = row.get("review", {})
        if any(review.get(k) is not True for k in ("source", "context", "localization", "naturalness", "formatting", "visual")):
            raise ValueError("Raw BGR555 per-record editorial/visual review incomplete")
        if any(not str(row.get(k, "")).strip() for k in ("source_text", "english", "context", "source_meaning", "localization_note")):
            raise ValueError("Raw BGR555 source/English/context missing")
        box = row.get("box")
        if not isinstance(box, list) or len(box) != 4:
            raise ValueError("Raw BGR555 requires a box")
        x0, y0, x1, y1 = map(int, box)
        if not 0 <= x0 < x1 <= 320 or not 0 <= y0 < y1 <= 240:
            raise ValueError("Raw BGR555 artwork box escapes frame")
        offsets = [frame * FRAME_BYTES + (y * 320 + x) * 2 + b
                   for y in range(y0, y1) for x in range(x0, x1) for b in (0, 1)]
        if owned.intersection(offsets):
            raise ValueError("Overlapping raw BGR555 artwork ownership")
        if row.get("source_region_sha256") != sha(bytes(original[i] for i in offsets)):
            raise ValueError("Raw BGR555 source region differs")
        payload = zlib.decompress(bytes.fromhex(row["words_zlib_hex"]))
        if len(payload) != len(offsets) or row.get("words_sha256") != sha(payload):
            raise ValueError("Raw BGR555 artwork payload extent/identity differs")
        expected, _ = render_region_payload(row, bytes(original[i] for i in offsets), batch, original)
        if payload != expected:
            raise ValueError("Raw BGR555 payload differs from complete English glyph raster")
        if any((a ^ b) & 0x8000 for (a,), (b,) in zip(
                struct.iter_unpack("<H", bytes(original[i] for i in offsets)),
                struct.iter_unpack("<H", payload), strict=True)):
            raise ValueError("Raw BGR555 artwork changes unclassified high color bits")
        for offset, value in zip(offsets, payload, strict=True):
            output[offset] = value
        owned.update(offsets)
        ids.append(record_id)
    if any(a != b for i, (a, b) in enumerate(zip(original, output, strict=True)) if i not in owned):
        raise ValueError("Raw BGR555 unowned pixels changed")
    archive.blocks[19] = bytes(output)
    result = archive.to_bytes()
    if len(result) != len(source) or result[:8 + 22 * 4] != source[:8 + 22 * 4]:
        raise ValueError("Raw BGR555 archive header/allocation changed")
    return result, ids
