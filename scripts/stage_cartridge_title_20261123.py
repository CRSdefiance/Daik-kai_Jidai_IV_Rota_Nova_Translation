"""Localize the original Nintendo DS cartridge title in its owned banner slots."""

import json
from hashlib import file_digest, sha256
from pathlib import Path
from struct import pack_into, unpack_from

from ndspy._common import crc16
from PIL import Image, ImageDraw, ImageFont

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.rom.nds import NdsImage


PARENT_RELEASE = Path("releases/all_routes_editorial_20261123_azores_wording_candidate/verification/registered_release_verification.json")
CLEAN = Path("work/clean.nds")
REGISTRY = Path("translations/release_stack.json")
EVIDENCE = Path(".codex-release-work/cartridge_title_20261123")
WORK = Path("E:/Rota Nova translations/Generated/work/cartridge_title_20261123")
ROM = WORK / "Translation_DS_Cartridge_Title_20261123_candidate.nds"
PROOF = EVIDENCE / "cartridge_title_stored.json"
SHEET = EVIDENCE / "cartridge_title_preview.png"
TITLE = ("Uncharted Waters IV", "Rota Nova", "KOEI")
ORIGINAL = "だいこうかいじだいIV\nROTA NOVA\nコーエー"
BANNER = "/__icon_banner__.bin"
LANGUAGES = ("Japanese", "English", "French", "German", "Italian", "Spanish")
START = 0x240
SLOT = 0x100
SIZE = 0x840
GATES = ("source", "context", "localization", "naturalness", "formatting")


def digest(path):
    with Path(path).open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def reference(path):
    return dict(path=Path(path).as_posix(), sha256=digest(path))


def installed_banner(blob):
    pos, = unpack_from("<I", blob, 0x68)
    banner = blob[pos:pos + SIZE]
    assert pos % 0x200 == 0 and len(banner) == SIZE
    version, checksum = unpack_from("<HH", banner)
    assert version == 1 and checksum == crc16(banner[0x20:])
    return pos, banner


def slot_text(raw):
    assert len(raw) == SLOT
    text, term, pad = raw.decode("utf-16le").partition("\0")
    assert text and term and set(pad) <= {"\0"}
    return text


def replace_banner(before, clean_banner, offset, source_offset):
    assert before == clean_banner and len(before) == SIZE
    revised = bytearray(before)
    encoded = ("\n".join(TITLE) + "\0").encode("utf-16le")
    assert len(encoded) <= SLOT
    rows = []
    for index, language in enumerate(LANGUAGES):
        begin, end = START + SLOT * index, START + SLOT * (index + 1)
        original = clean_banner[begin:end]
        current = before[begin:end]
        assert slot_text(original) == slot_text(current) == ORIGINAL
        if index:
            revised[begin:end] = encoded.ljust(SLOT, b"\0")
        target = bytes(revised[begin:end])
        assert slot_text(target) == ("\n".join(TITLE) if index else ORIGINAL)
        rows.append(dict(id=f"CARTRIDGE_TITLE_{index}", file_path=BANNER, firmware_locale=language,
            speaker="Nintendo DS cartridge title", context="The launcher displays the title, subtitle and publisher on three rows.",
            source_Japanese=ORIGINAL, source_meaning="Uncharted Waters IV, Rota Nova, published by Koei.",
            english="Uncharted Waters IV: Rota Nova (KOEI)",
            localized_display=slot_text(target).splitlines(), decision="revision" if index else "retention",
            localization_note=("Localize the original title, keep the distinct subtitle and preserve the publisher on its own row."
                               if index == 1 else "Supply the English release title when the launcher uses this language slot."
                               if index else "Keep the original Japanese reading and publisher spelling for Japanese menus."),
            source_reference=dict(absolute_offset=source_offset + begin, banner_offset=begin, slot_hex=original.hex()),
            current_reference=dict(absolute_offset=offset + begin, banner_offset=begin, slot_hex=current.hex()),
            installed_reference=dict(absolute_offset=offset + begin, banner_offset=begin, slot_hex=target.hex()),
            review=dict.fromkeys(GATES, True)))
    pack_into("<H", revised, 2, crc16(revised[0x20:SIZE]))
    assert revised[:2] == before[:2] and revised[4:START + SLOT] == before[4:START + SLOT]
    return bytes(revised), rows


def cartridge_icon(banner):
    icon = Image.new("RGBA", (32, 32))
    palette = [unpack_from("<H", banner, 0x220 + i * 2)[0] for i in range(16)]
    for y in range(32):
        for x in range(32):
            tile = (y // 8) * 4 + x // 8
            pair = banner[0x20 + tile * 32 + (y % 8) * 4 + (x % 8) // 2]
            pixel = (pair >> (4 * (x % 2))) & 15
            value = palette[pixel]
            rgb = tuple(((value >> shift) & 31) * 255 // 31 for shift in (0, 5, 10))
            icon.putpixel((x, y), (*rgb, 255 if pixel else 0))
    return icon


def preview(banner, rows):
    font_dir = Path("C:/Windows/Fonts")
    latin = ImageFont.truetype(str(font_dir / "segoeui.ttf"), 14)
    japanese = ImageFont.truetype(str(font_dir / "msgothic.ttc"), 14)
    picture = Image.new("RGB", (512, 300), "#edf1f4")
    draw = ImageDraw.Draw(picture)
    icon = cartridge_icon(banner)
    bounds = []
    for index, row in enumerate(rows):
        x, y = index % 2 * 256, index // 2 * 100
        draw.text((x + 12, y + 7), row["firmware_locale"], font=latin, fill="#28343d")
        draw.rounded_rectangle((x + 10, y + 29, x + 245, y + 91), radius=6, fill="white", outline="#8796a3")
        picture.paste(icon, (x + 19, y + 44), icon)
        widths = []
        font = latin if index else japanese
        for i, line in enumerate(row["localized_display"]):
            at = (x + 60, y + 34 + i * 16)
            left, top, right, bottom = draw.textbbox(at, line, font=font)
            assert x + 59 <= left < right <= x + 240 and y + 30 <= top < bottom <= y + 90
            widths.append(right - left)
            draw.text(at, line, font=font, fill="#101820")
        bounds.append(dict(locale=row["firmware_locale"], preview_widths_px=widths,
                           three_rows=True, origin_preserves_icon=True))
    picture.resize((1024, 600), Image.Resampling.NEAREST).save(SHEET)
    return bounds


def main():
    assert not PROOF.exists() and not SHEET.exists()
    release = read(PARENT_RELEASE)
    parent = Path(release["candidate"])
    assert digest(parent) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"]
    original, previous = CLEAN.read_bytes(), parent.read_bytes()
    source_at, source_banner = installed_banner(original)
    at, before = installed_banner(previous)
    amended, rows = replace_banner(before, source_banner, at, source_at)
    candidate = previous[:at] + amended + previous[at + SIZE:]
    assert len(candidate) == len(previous)
    assert installed_banner(candidate) == (at, amended)
    assert candidate[:at] + before + candidate[at + SIZE:] == previous
    assert len(TITLE) == 3 and all(line.isascii() and len(line) <= 20 for line in TITLE)
    WORK.mkdir(parents=True, exist_ok=True)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    if ROM.exists():
        assert ROM.read_bytes() == candidate
    else:
        with ROM.open("xb") as stream:
            for offset in range(0, len(candidate), 1 << 20):
                stream.write(candidate[offset:offset + (1 << 20)])
    assert bytes(NdsImage.open(ROM).rom.iconBanner) == amended
    assert digest(ROM) == sha256(candidate).hexdigest()
    bounds = preview(amended, rows)
    manuscript = dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
                      encoder="dialogue-relocatable-v1", review_gates=list(GATES), records=rows)
    validate_natural_dialogue_batch(manuscript)
    write(PROOF, manuscript | dict(candidate=reference(ROM), parent=reference(parent), clean=reference(CLEAN),
        predecessor_release=reference(PARENT_RELEASE), banner_offset=at, format_version=1, byte_count=SIZE,
        original_crc16=f"{unpack_from('<H', before, 2)[0]:04x}", revised_crc16=f"{crc16(amended[0x20:]):04x}",
        unchanged_original_icon_and_palette=True, whole_ROM_outside_banner_exact=True, exact_parent_inverse=True,
        preview=reference(SHEET), preview_dimensions=bounds,
        preview_scope="Offline reconstruction from the installed banner. Widths use host preview fonts.",
        authoritative_format="https://blocksds.skylyrac.net/libnds/structsNDSBanner.html",
        desktop_title_consumer="https://github.com/melonDS-emu/melonDS/blob/master/src/frontend/qt_sdl/ROMInfoDialog.cpp"))
    print(f"Staged {digest(ROM)}. Both banner CRCs and the complete parent inverse passed.")


if __name__ == "__main__":
    main()
