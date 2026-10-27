"""Guarded whole-image synchronization into consecutive rectangular OBJ banks."""

import hashlib

from dk4tool.graphics.pxl import PxlImage

FORMAT = "dk4-obj-banked-pxl-sync-v1"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def apply_banked_sync(batch, source, reference):
    if batch.get("format") != FORMAT:
        raise ValueError("Unsupported banked OBJ sync format")
    if digest(source) != batch.get("source_file_sha256"):
        raise ValueError("Banked OBJ source hash mismatch")
    if digest(reference) != batch.get("source_image_sha256"):
        raise ValueError("Banked OBJ reference hash mismatch")
    fields = {}
    for key in ("target_offset", "bank_width", "bank_height", "bank_count", "blank_index"):
        value = batch.get(key)
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{key} must be an integer")
        fields[key] = value
    offset, width, height, count, blank = (fields[k] for k in
                                         ("target_offset", "bank_width", "bank_height", "bank_count", "blank_index"))
    if offset < 0 or offset % 32 or width <= 0 or height <= 0 or count <= 0:
        raise ValueError("Invalid OBJ bank bounds")
    if width % 8 or height % 8 or not 0 <= blank <= 15:
        raise ValueError("Invalid OBJ tile alignment or blank index")
    size = width * height * count // 2
    if offset + size > len(source) or size != batch.get("target_region_bytes"):
        raise ValueError("Banked OBJ destination range exceeds source or declared extent")
    if digest(source[offset:offset + size]) != batch.get("source_region_sha256"):
        raise ValueError("Banked OBJ region hash mismatch")
    image = PxlImage.from_bytes(reference)
    if image.bits_per_pixel != 4 or image.width != width * count or not 0 < image.height <= height:
        raise ValueError("Reference image does not fit complete OBJ banks")
    if [image.width, image.height] != batch.get("source_image_extent"):
        raise ValueError("Reference image extent differs")
    if not set(image.indices) <= set(batch.get("allowed_indices", [])) or blank not in batch.get("allowed_indices", []):
        raise ValueError("Reference image uses an undeclared palette role")
    padded = bytearray([blank]) * (image.width * height)
    padded[:len(image.indices)] = image.indices
    packed = bytearray()
    for bank in range(count):
        for ty in range(height // 8):
            for tx in range(width // 8):
                for y in range(8):
                    row = (ty * 8 + y) * image.width + bank * width + tx * 8
                    for x in range(0, 8, 2):
                        packed.append(padded[row + x] | padded[row + x + 1] << 4)
    assert len(packed) == size
    result = source[:offset] + packed + source[offset + size:]
    assert len(result) == len(source)
    if not isinstance(batch.get("record_id"), str) or not batch["record_id"]:
        raise ValueError("Banked OBJ sync requires a record ID")
    return result, [batch["record_id"]]
