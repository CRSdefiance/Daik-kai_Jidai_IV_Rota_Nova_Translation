import pytest

from dk4tool.dialogue.font_audit import (
    ASCII_FONT_OFFSET,
    SJIS_GLYPH_COUNT,
    SJIS_MAP_OFFSET,
    GameAsciiFont,
    RawFontGeometry,
    audit_standard_font,
    decode_glyph,
    glyph_count,
)


def test_raw_16_by_11_font_decoding_uses_msb_first_rows():
    data = bytes([0x80, 0x01] + [0] * 20)
    glyph = decode_glyph(data, 0)

    assert glyph.getpixel((0, 0))
    assert glyph.getpixel((15, 0))
    assert not glyph.getpixel((1, 0))


def test_raw_font_glyph_count_ignores_padding_tail():
    geometry = RawFontGeometry()
    assert glyph_count(bytes(geometry.bytes_per_cell * 3 + 7)) == 3


def test_game_ascii_font_decodes_six_pixels_from_each_eleven_byte_glyph():
    arm9 = bytearray(ASCII_FONT_OFFSET + 95 * 11)
    arm9[ASCII_FONT_OFFSET] = 0x84
    font = GameAsciiFont.from_arm9(bytes(arm9))
    glyph = font.decode("!")

    assert glyph.size == (6, 11)
    assert glyph.getpixel((0, 0))
    assert glyph.getpixel((5, 0))
    assert not glyph.getpixel((1, 0))
    assert not font.decode(" ").getbbox()


def test_game_ascii_font_rejects_non_ascii_character():
    arm9 = bytearray(ASCII_FONT_OFFSET + 95 * 11)
    arm9[ASCII_FONT_OFFSET] = 0x80
    font = GameAsciiFont.from_arm9(bytes(arm9))
    with pytest.raises(ValueError, match="outside"):
        font.decode("é")


def test_font_audit_reports_fixed_renderer_metrics_and_matching_font_size():
    arm9 = bytearray(SJIS_MAP_OFFSET + SJIS_GLYPH_COUNT * 2)
    signatures = {
        0xD1674: "0C5085E2",
        0xD169C: "065085E2",
        0xD1748: "0B0051E3",
        0xD1804: "0B005AE3",
        0xD1828: "210050E3",
        0xD1830: "7F0050E3",
        0xD1840: "0B20A0E3",
    }
    for offset, value in signatures.items():
        arm9[offset : offset + 4] = bytes.fromhex(value)
    for index in range(SJIS_GLYPH_COUNT):
        arm9[SJIS_MAP_OFFSET + index * 2 : SJIS_MAP_OFFSET + index * 2 + 2] = (
            index.to_bytes(2, "little")
        )
    report = audit_standard_font(bytes(arm9), bytes(SJIS_GLYPH_COUNT * 22))

    assert report["all_renderer_signatures_match"]
    assert report["ascii"]["advance_px"] == 6
    assert report["shift_jis"]["advance_px"] == 12
    assert report["shift_jis"]["font_size_matches_map"]
    assert report["layout"]["story_dialogue_content_width_px"] == 216
    assert report["layout"]["story_dialogue_ascii_cells"] == 36
    assert report["layout"]["shared_dialogue_content_width_px"] == 216
    assert report["layout"]["shared_dialogue_ascii_cells"] == 36
