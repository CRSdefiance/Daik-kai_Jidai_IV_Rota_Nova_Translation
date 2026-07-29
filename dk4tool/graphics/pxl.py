from __future__ import annotations

import struct
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFilter, ImageFont

Box = tuple[int, int, int, int]


def bgr555(value: int) -> tuple[int, int, int, int]:
    red = (value & 0x1F) * 255 // 31
    green = ((value >> 5) & 0x1F) * 255 // 31
    blue = ((value >> 10) & 0x1F) * 255 // 31
    return red, green, blue, 255


@dataclass
class PxlImage:
    source: bytes
    bits_per_pixel: int
    width: int
    height: int
    pixels_offset: int
    palette: list[tuple[int, int, int, int]]
    indices: bytearray

    @classmethod
    def from_bytes(cls, data: bytes) -> PxlImage:
        depth, width_words, height, palette_offset, pixels_offset = struct.unpack_from(
            "<5I", data
        )
        bits_per_pixel = depth & 0xFF
        if bits_per_pixel not in (4, 8):
            raise ValueError(f"unsupported PXL depth: {bits_per_pixel}")

        palette_size = 32 if bits_per_pixel == 4 else 512
        palette_data = data[palette_offset : palette_offset + palette_size]
        palette = [bgr555(value) for (value,) in struct.iter_unpack("<H", palette_data)]
        packed = data[pixels_offset:]
        width = width_words * (4 if bits_per_pixel == 4 else 2)
        if bits_per_pixel == 4:
            indices = bytearray(len(packed) * 2)
            for position, value in enumerate(packed):
                indices[position * 2] = value & 0x0F
                indices[position * 2 + 1] = value >> 4
        else:
            indices = bytearray(packed)

        expected = width * height
        if len(indices) != expected:
            raise ValueError(f"pixel size mismatch: expected {expected}, found {len(indices)}")
        return cls(data, bits_per_pixel, width, height, pixels_offset, palette, indices)

    def to_bytes(self) -> bytes:
        if self.bits_per_pixel == 4:
            packed = bytearray(len(self.indices) // 2)
            for position in range(len(packed)):
                packed[position] = (
                    self.indices[position * 2] | self.indices[position * 2 + 1] << 4
                )
        else:
            packed = self.indices
        if len(packed) != len(self.source) - self.pixels_offset:
            raise ValueError("PXL rebuild changed the packed pixel size")
        return self.source[: self.pixels_offset] + bytes(packed)

    def render(self) -> Image.Image:
        image = Image.new("RGBA", (self.width, self.height))
        image.putdata([self.palette[index] for index in self.indices])
        return image

    def clear(self, box: Box, color_index: int = 0) -> None:
        left, top, right, bottom = box
        for y in range(top, bottom):
            start = y * self.width + left
            self.indices[start : start + right - left] = bytes([color_index]) * (
                right - left
            )

    def erase_dark_text(self, box: Box, threshold: int = 135) -> None:
        left, top, right, bottom = box
        luminance = [
            (red * 299 + green * 587 + blue * 114) // 1000
            for red, green, blue, _ in self.palette
        ]
        for y in range(top, bottom):
            row_start = y * self.width
            safe = [
                x
                for x in range(left, right)
                if luminance[self.indices[row_start + x]] >= threshold
            ]
            if not safe:
                continue
            for x in range(left, right):
                position = row_start + x
                if luminance[self.indices[position]] < threshold:
                    nearest = min(safe, key=lambda candidate: abs(candidate - x))
                    self.indices[position] = self.indices[row_start + nearest]

    def erase_palette_indices(self, box: Box, erased: set[int]) -> None:
        """Erase selected text colors while retaining the nearest row background."""
        left, top, right, bottom = box
        for y in range(top, bottom):
            row_start = y * self.width
            safe = [
                x
                for x in range(left, right)
                if self.indices[row_start + x] not in erased
            ]
            if not safe:
                continue
            for x in range(left, right):
                position = row_start + x
                if self.indices[position] in erased:
                    nearest = min(safe, key=lambda candidate: abs(candidate - x))
                    self.indices[position] = self.indices[row_start + nearest]

    def draw_text(
        self,
        box: Box,
        text: str,
        color_index: int,
        *,
        outline_index: int | None = None,
        maximum_size: int = 13,
    ) -> None:
        left, top, right, bottom = box
        box_width = right - left
        box_height = bottom - top
        font = None
        text_box = None
        for size in range(maximum_size, 5, -1):
            candidate = ImageFont.load_default(size=size)
            bounds = candidate.getbbox(text)
            if bounds[2] - bounds[0] <= box_width and bounds[3] - bounds[1] <= box_height:
                font = candidate
                text_box = bounds
                break
        if font is None or text_box is None:
            raise ValueError(f"text does not fit {box}: {text!r}")

        mask = Image.new("L", (box_width, box_height))
        draw = ImageDraw.Draw(mask)
        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]
        x = (box_width - text_width) // 2 - text_box[0]
        y = (box_height - text_height) // 2 - text_box[1]
        draw.text((x, y), text, font=font, fill=255)

        if outline_index is not None:
            outline = mask.filter(ImageFilter.MaxFilter(3))
            self._paste_mask(box, outline, outline_index)
        self._paste_mask(box, mask, color_index)

    def _paste_mask(self, box: Box, mask: Image.Image, color_index: int) -> None:
        left, top, _, _ = box
        mask_data = mask.load()
        for y in range(mask.height):
            for x in range(mask.width):
                if mask_data[x, y] >= 128:
                    self.indices[(top + y) * self.width + left + x] = color_index
