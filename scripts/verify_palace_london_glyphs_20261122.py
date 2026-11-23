"""Check every new story glyph and the PNGs used for visual review."""

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import stage_palace_eirene_pereira_london_20261122 as stage
from scripts.verify_all_items_gallery_v535 import glyph_pixels


OUTPUT = stage.ROOT / "glyph_and_sheet_verification.json"
WIDTH, HEIGHT = 216, 64
COLORS = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}


def verify():
    report = stage.base.load(stage.NATIVE)
    candidate = stage.base.digest(stage.ROM)
    assert candidate == report["candidate_sha256"]
    arm = stage.base.NdsImage.open(stage.ROM).read_file("/__arm9__.bin")
    font = GameAsciiFont.from_arm9(arm)
    pages = [
        (row["id"], row["route"], layout["scope"], page)
        for row in report["records"] for layout in row["layouts"] for page in layout["pages"]
    ]
    assert len(pages) == report["pages"]
    checked = []
    for index, (record, route, scope, page) in enumerate(pages):
        plane = bytes.fromhex(page["native_plane_hex"])
        expected = set()
        glyphs = page["events"]
        assert len(plane) == WIDTH * HEIGHT and glyphs
        for glyph in glyphs:
            assert glyph["kind"] == "ascii"
            x, y = glyph["x"], glyph["y"] + 1
            expected.update(glyph_pixels(font, b"", (), chr(glyph["code"]), x, y, 6))
        pixels = {(i % WIDTH, i // WIDTH) for i, value in enumerate(plane) if value}
        assert expected == pixels, (route, record, scope)
        assert all(0 <= x < WIDTH and 0 <= y < HEIGHT for x, y in expected)
        sheet_number, slot = divmod(index, 8)
        sheet = report["sheets"][sheet_number]
        assert stage.base.digest(sheet["path"]) == sheet["sha256"]
        x, y = (slot % 2) * 444 + 4, (slot // 2) * 154 + 21
        preview = Image.new("RGB", (WIDTH, HEIGHT))
        preview.putdata([COLORS[p] for p in plane])
        with Image.open(sheet["path"]) as contact:
            crop = contact.crop((x, y, x + WIDTH * 2, y + HEIGHT * 2))
            assert crop.tobytes() == preview.resize((WIDTH * 2, HEIGHT * 2), Image.Resampling.NEAREST).tobytes()
        checked.append(dict(route=route, id=record, scope=scope, glyphs=len(glyphs), ink=len(pixels),
                            contact_sheet=sheet))
    stage.base.save(OUTPUT, dict(candidate_sha256=candidate, native_report_sha256=stage.base.digest(stage.NATIVE),
                                pages=checked, complete_font_pixels=True, exact_contact_sheet_pixels=True))
    print(f"Every glyph and contact-sheet crop matched for {len(checked)} pages.", flush=True)


if __name__ == "__main__":
    verify()
