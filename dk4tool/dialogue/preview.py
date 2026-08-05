from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .codec import parse_markup
from .font_audit import GameAsciiFont
from .model import DialogueToken
from .profiles import DialogueProfile


def visible_lines(tokens: list[DialogueToken]) -> list[str]:
    lines = [""]
    for token in tokens:
        if token.kind == "line_break":
            lines.append("")
        elif token.kind == "text":
            lines[-1] += token.value
        elif token.kind == "macro":
            lines[-1] += f"<{token.value}>"
        elif token.kind == "speaker":
            lines[-1] += f"<SPEAKER {token.value}>"
        elif token.kind == "raw_control":
            lines[-1] += f"<{token.raw.hex().upper()}>"
        elif token.kind == "align":
            lines[-1] += f"<ALIGN {token.value}>"
        elif token.kind == "end":
            lines[-1] += "<END>"
    return lines


def render_dialogue_preview(
    text: str,
    profile: DialogueProfile,
    destination: Path,
    *,
    arm9: bytes | None = None,
) -> None:
    """Render a diagnostic preview using exact game glyphs when ARM9 is supplied."""

    scale = 3
    margin = 10
    width = (profile.window_width_px + margin * 2) * scale
    height = max(96, 16 + profile.max_lines * profile.line_height_px) * scale
    image = Image.new("RGB", (width, height), (239, 232, 201))
    draw = ImageDraw.Draw(image)
    draw.rectangle((3, 3, width - 4, height - 4), outline=(62, 51, 28), width=3)
    font = ImageFont.load_default(size=12 * scale)
    game_font = GameAsciiFont.from_arm9(arm9) if arm9 is not None else None
    tokens = parse_markup(text)
    x = margin * scale
    line = 0
    y = (8 + line * profile.line_height_px) * scale
    right_edge = (margin + profile.window_width_px) * scale
    draw.line((right_edge, 4, right_edge, height - 5), fill=(178, 55, 43), width=1)
    annotations: list[str] = []
    for token in tokens:
        if token.kind == "line_break":
            line += 1
            x = margin * scale
            y = (8 + line * profile.line_height_px) * scale
            continue
        if token.kind == "text":
            for character in token.value:
                color = (178, 20, 20) if x >= right_edge else (20, 20, 18)
                if game_font is not None and ord(character) < 0x80:
                    glyph = game_font.decode(character).resize(
                        (6 * scale, 11 * scale), resample=Image.Resampling.NEAREST
                    )
                    ink = Image.new("RGB", glyph.size, color)
                    image.paste(ink, (x, y), glyph)
                else:
                    draw.text((x, y), character, fill=color, font=font)
                x += profile.glyph_width(character) * scale
        elif token.kind == "macro":
            macro_width = profile.macro_width(token.value) * scale
            draw.rectangle((x, y, x + macro_width - 1, y + 12 * scale), outline=(42, 92, 150))
            draw.text((x + 2, y), token.value, fill=(42, 92, 150), font=font)
            x += macro_width
        elif token.kind == "raw_control":
            annotations.append(f"HEX:{token.value}")
        elif token.kind == "speaker":
            annotations.append(f"SPEAKER:{token.value}")
        elif token.kind == "align":
            annotations.append(f"ALIGN:{token.value}")
    if annotations:
        draw.text(
            (margin * scale, height - 14 * scale),
            " | ".join(annotations),
            fill=(110, 55, 145),
            font=font,
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination)
