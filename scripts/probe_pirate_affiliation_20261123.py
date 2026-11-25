"""Render the original Pirate branch over a controlled native portrait-label plane."""

import json
from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R10, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, HEADER, STACK, VIEW, call, machine
from scripts.reconcile_editorial_acceptance_20261123 import ARM, OUT, PACKAGE, digest, read, reference


REPORT = OUT.with_name("pirate_affiliation_native_20261123.json")
SHEET = REPORT.with_suffix(".png")
WIDTH, HEIGHT = 108, 12
START, END, DRAW = 0xBBFC, 0xBC48, 0xD5404
SLOT = 0x1305F4
JAPANESE = bytes.fromhex("8a4391af00000000")
ENGLISH = b"Pirate\0\0"


def render(arm, memory, kanji, text):
    cpu = machine(arm)
    cpu.mem_write(BASE, memory)
    font_pointer, = unpack_from("<I", arm, 0xD19B8)
    assert BASE + len(arm) <= font_pointer < HEADER - len(kanji)
    cpu.mem_write(font_pointer, kanji)
    panel, actor = VIEW + 0x1000, VIEW + 0x2000
    size = WIDTH * HEIGHT // 2
    header = pack("<5I", 4, WIDTH // 4, HEIGHT, 20, 20)
    guard = b"\xA5" * 16
    cpu.mem_write(HEADER - 16, guard + header + bytes(size) + guard)
    call(cpu, 0xD3D80, (VIEW,))
    cpu.mem_write(STACK, pack("<4I", WIDTH, HEIGHT, 0, 0))
    call(cpu, 0xD3AFC, (VIEW, HEADER, 0, 0))
    context = STACK + 0xF4
    call(cpu, 0xD5160, (context, VIEW, 1))
    assert unpack_from("<3I", cpu.mem_read(context + 0x1C, 12)) == (0, 0, 0)
    cpu.mem_write(panel + 0x920, pack("<I", actor))
    cpu.mem_write(actor + 5, b"\x15")
    assert bytes(cpu.mem_read(BASE + SLOT, len(JAPANESE))) == JAPANESE
    cpu.mem_write(BASE + SLOT, text)
    cpu.reg_write(UC_ARM_REG_R10, panel)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    draws = []

    def observe(core, _address, _size, _data):
        pointer = core.reg_read(UC_ARM_REG_R1)
        draws.append((core.reg_read(UC_ARM_REG_R0), pointer, bytes(core.mem_read(pointer, len(text)))))

    hook = cpu.hook_add(UC_HOOK_CODE, observe, begin=BASE + DRAW, end=BASE + DRAW)
    try:
        cpu.emu_start(BASE + START, BASE + END, count=100000)
    finally:
        cpu.hook_del(hook)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE + END and cpu.reg_read(UC_ARM_REG_SP) == STACK
    assert draws == [(context, BASE + SLOT, text)]
    assert bytes(cpu.mem_read(HEADER - 16, 16 + len(header))) == guard + header
    assert bytes(cpu.mem_read(HEADER + len(header) + size, 16)) == guard
    packed = bytes(cpu.mem_read(HEADER + len(header), size))
    pixels = bytes(nibble for byte in packed for nibble in (byte & 15, byte >> 4))
    assert any(pixels)
    return pixels


def main():
    assert not REPORT.exists() and not SHEET.exists()
    release = read(PACKAGE / "verification/registered_release_verification.json")
    startup_file = Path(release["own_registered_startup"])
    assert digest(startup_file) == release["own_registered_startup_sha256"]
    startup = read(startup_file)
    assert startup["cold_boot"] and startup["candidate_sha256"] == release["candidate_sha256"]
    snapshot = startup["read_only_snapshot"]
    memory_path = Path(snapshot["path"])
    memory = memory_path.read_bytes()
    assert snapshot["read_only_export"] and len(memory) == snapshot["bytes"] == 0x400000
    assert sha256(memory).hexdigest() == snapshot["sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    image = NdsImage.open(release["candidate"])
    arm = image.read_file(ARM)
    kanji = image.read_file("/GRP/KANJI.FNT")
    assert len(kanji) == 3340 * 22
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert memory[START:END] == arm[START:END]

    before, after = (render(arm, memory, kanji, text) for text in (JAPANESE, ENGLISH))
    font = GameAsciiFont.from_arm9(arm)
    expected = {(col * 6 + x, y + 1) for col, char in enumerate("Pirate")
                for glyph in (font.decode(char),) for y in range(11) for x in range(6) if glyph.getpixel((x, y))}
    actual = {(index % WIDTH, index // WIDTH) for index, value in enumerate(after) if value}
    assert actual == expected and set(after) == {0, 1}
    assert any(x < 6 for x, _ in actual) and any(x >= 30 for x, _ in actual)
    bounds = Image.frombytes("L", (WIDTH, HEIGHT), after).getbbox()
    assert bounds == (0, 1, 34, max(y for _, y in expected) + 1)

    sheet = Image.new("RGB", (WIDTH * 4 + 40, 178), "#242a34")
    heading = ImageDraw.Draw(sheet)
    for row, (label, pixels) in enumerate((("Installed ROM", before), ("English proposal in emulator memory", after))):
        y = 12 + row * 85
        heading.text((20, y), label, fill="white")
        plane = Image.frombytes("L", (WIDTH, HEIGHT), pixels).point(lambda value: 42 if value else 225)
        sheet.paste(plane.resize((WIDTH * 4, HEIGHT * 4), Image.Resampling.NEAREST).convert("RGB"), (20, y + 20))
    sheet.save(SHEET)
    evidence = {"candidate_sha256": release["candidate_sha256"], "startup_receipt": reference(startup_file),
                "initialized_snapshot": snapshot, "supplied_Kanji_asset_sha256": sha256(kanji).hexdigest(),
                "caller": [BASE + START, BASE + END],
                "painter": BASE + DRAW, "affiliation_fixture": 21, "source_ARM9_offset": SLOT,
                "installed_text": JAPANESE.rstrip(b"\0").decode("cp932"), "installed_slot_hex": JAPANESE.hex(),
                "proposed_text": "Pirate", "proposed_slot_hex": ENGLISH.hex(), "one_line_surface": [WIDTH, HEIGHT],
                "proposed_ink_bounds": bounds, "proposed_exact_native_font_pixels": len(actual),
                "complete_leading_and_trailing_glyphs": True, "packed_bitmap_guards_intact": True,
                "installed_bitmap_sha256": sha256(before).hexdigest(), "proposal_bitmap_sha256": sha256(after).hexdigest(),
                "sheet": reference(SHEET), "ordinary_gameplay": False, "registered_ROM_changed": False}
    REPORT.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"The stock Pirate branch paints both labels in the fixture. All {len(actual)} English pixels match.")


if __name__ == "__main__":
    main()
