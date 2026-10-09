from __future__ import annotations

import struct
from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from dk4tool.graphics.pxl import bgr555
from dk4tool.scan.compression_probe import compress_lz10, decompress_lz10


def _next_power_of_two(value: int) -> int:
    return 1 << max(3, (value - 1).bit_length())


@dataclass
class FlsTexture:
    index: int
    flags: int
    width: int
    height: int
    palette: list[tuple[int, int, int, int]]
    indices: bytearray

    def render(self) -> Image.Image:
        image = Image.new("RGBA", (self.width, self.height))
        image.putdata([self.palette[index] for index in self.indices])
        return image

    def replace_with_lines(
        self,
        lines: list[str],
        maximum_size: int = 12,
        *,
        background_index: int | None = None,
        color_index: int | None = None,
        outline_index: int | None = None,
        layout_width: int | None = None,
    ) -> None:
        luminance = [
            (red * 299 + green * 587 + blue * 114) // 1000
            for red, green, blue, _ in self.palette
        ]
        background = (
            min(range(len(self.palette)), key=luminance.__getitem__)
            if background_index is None
            else background_index
        )
        foreground = (
            max(range(len(self.palette)), key=luminance.__getitem__)
            if color_index is None
            else color_index
        )
        for name, index in (
            ("background", background),
            ("foreground", foreground),
            ("outline", outline_index),
        ):
            if index is not None and not 0 <= index < len(self.palette):
                raise ValueError(f"FLS {name} palette index is out of range: {index}")
        draw_width = self.width if layout_width is None else layout_width
        if not 1 <= draw_width <= self.width:
            raise ValueError(f"FLS layout width is out of range: {draw_width}")
        self.indices[:] = bytes([background]) * len(self.indices)

        mask = Image.new("L", (self.width, self.height))
        draw = ImageDraw.Draw(mask)
        line_height = max(1, self.height // max(1, len(lines)))
        for line_number, line in enumerate(lines):
            box_top = line_number * line_height
            box_bottom = (
                self.height if line_number == len(lines) - 1 else (line_number + 1) * line_height
            )
            font = None
            bounds = None
            for size in range(maximum_size, 5, -1):
                candidate = ImageFont.load_default(size=size)
                candidate_bounds = candidate.getbbox(line)
                if (
                    candidate_bounds[2] - candidate_bounds[0] <= draw_width - 8
                    and candidate_bounds[3] - candidate_bounds[1] <= box_bottom - box_top
                ):
                    font = candidate
                    bounds = candidate_bounds
                    break
            if font is None or bounds is None:
                raise ValueError(f"FLS subtitle does not fit: {line!r}")
            text_width = bounds[2] - bounds[0]
            text_height = bounds[3] - bounds[1]
            x = (draw_width - text_width) // 2 - bounds[0]
            y = box_top + (box_bottom - box_top - text_height) // 2 - bounds[1]
            draw.text((x, y), line, font=font, fill=255)

        if outline_index is not None:
            outline_data = mask.filter(ImageFilter.MaxFilter(3)).load()
            for y in range(self.height):
                for x in range(self.width):
                    if outline_data[x, y] >= 128:
                        self.indices[y * self.width + x] = outline_index

        mask_data = mask.load()
        for y in range(self.height):
            for x in range(self.width):
                if mask_data[x, y] >= 128:
                    self.indices[y * self.width + x] = foreground


class FlsArchive:
    def __init__(self, data: bytes):
        self.source = data
        self.compressed_storage = bool(struct.unpack_from("<I", data)[0] & 0x80)
        self.table_offset, self.count, self.data_offset = struct.unpack_from("<III", data, 4)
        self.records = [
            list(struct.unpack_from("<6I", data, self.table_offset + index * 24))
            for index in range(self.count)
        ]
        self.textures: dict[int, FlsTexture] = {}

    def texture(self, index: int) -> FlsTexture:
        if index in self.textures:
            return self.textures[index]
        flags, dimensions, palette_offset, palette_size, pixels_offset, pixels_size = self.records[index]
        if self.compressed_storage:
            palette_data = decompress_lz10(self.source[self.data_offset + palette_offset :])
            pixels = decompress_lz10(self.source[self.data_offset + pixels_offset :])
        else:
            palette_data = self.source[self.data_offset + palette_offset : self.data_offset + palette_offset + palette_size]
            pixels = self.source[self.data_offset + pixels_offset : self.data_offset + pixels_offset + pixels_size]
            if len(palette_data) != palette_size or len(pixels) != pixels_size:
                raise ValueError("Uncompressed FLS slot extends beyond the source file")
        palette = [
            bgr555(value)
            for (value,) in struct.iter_unpack("<H", palette_data[: len(palette_data) & ~1])
        ]
        if len(palette) == 16:
            indices = bytearray(len(pixels) * 2)
            for position, value in enumerate(pixels):
                indices[position * 2] = value & 0x0F
                indices[position * 2 + 1] = value >> 4
        elif len(palette) == 256:
            indices = bytearray(pixels)
        else:
            raise ValueError(f"unsupported FLS palette size: {len(palette)}")

        visible_height = dimensions & 0xFFFF
        height = _next_power_of_two(max(8, visible_height))
        if self.compressed_storage:
            height = min(256, height)
        if len(indices) % height:
            raise ValueError("FLS texture dimensions do not divide its pixels")
        width = len(indices) // height
        texture = FlsTexture(index, flags, width, height, palette, indices)
        self.textures[index] = texture
        return texture

    def to_bytes(self) -> bytes:
        output = bytearray(self.source)
        for index, texture in self.textures.items():
            if len(texture.palette) == 16:
                pixels = bytearray(len(texture.indices) // 2)
                for position in range(len(pixels)):
                    pixels[position] = (
                        texture.indices[position * 2] | texture.indices[position * 2 + 1] << 4
                    )
            else:
                pixels = texture.indices
            compressed = compress_lz10(bytes(pixels)) if self.compressed_storage else bytes(pixels)
            pixels_offset = self.records[index][4]
            slot_size = self.records[index][5]
            if len(compressed) > slot_size:
                raise ValueError(
                    f"FLS asset {index} needs {len(compressed)} bytes; slot has {slot_size}"
                )
            start = self.data_offset + pixels_offset
            output[start : start + slot_size] = compressed + bytes(slot_size - len(compressed))
        return bytes(output)
