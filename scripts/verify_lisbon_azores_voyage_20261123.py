"""Verify the ordinary Azores visit, full display fields, and two source findings."""

import json
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.observe_lisbon_azores_voyage_20261123 import DONOR, RELEASE, ROOT
from scripts.read_lisbon_azores_navigation_20261123 import position
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, COMMON, OUT, digest, read, reference
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_ordinary_azores_voyage_20261123 import town
from scripts.verify_regional_ui_v616 import glyphs


REPORT = OUT.with_name("ordinary_lisbon_azores_20261123.json")
SHEET = REPORT.with_suffix(".png")
HOLDS = {
    3750: (85, ("38",), "", "The estimate communicates the approximate duration."),
    4500: (86, ("1", "16", "Sky: Sunny", "Lisbon"), "", "The date, weather and town keep their original sequence."),
    8300: (1314, (), "Gerhard Adernkatz", "The lookout alerts the admiral immediately."),
    8420: (297, ("Azores",), "", "Use the Azores in the complete discovery sentence."),
    8550: (70, ("Azores",), "Manuel Almeida", "Include the article in speech and ask directly about docking."),
    9100: (1328, (), "Manuel Almeida", "His response preserves gratitude and names both supplies."),
    9620: (0x78C48, (), "Manuel Almeida", "The source addresses the admiral, as in Gerhard's warning."),
    9840: (0xAEA40, (), "", "The prompt tells the player what to enter."),
    10700: (296, ("a",), "", "The system confirms the exact entered text before submission."),
    10980: (0x78C58, (), "Manuel Almeida", "The original outcome says the chief left without assigning blame."),
    11500: (1356, ("５",), "Manuel Almeida", "The gift amount and reason remain explicit."),
}
REVISION_LEADS = {
    297: "Discovered the Azores.",
    70: "Shall we dock at the Azores?",
    0x78C48: "Admiral, the village chief asks to hear the promised words.",
}
INK = (0, 8, 0)


def load_exact(row):
    path = Path(row["path"])
    assert digest(path) == row["sha256"]
    return path.read_bytes()


def text_at(data, address):
    offset = address - BASE
    assert 0 <= offset < len(data) - 256
    raw, zero, _ = data[offset:offset + 256].partition(b"\0")
    assert raw and zero
    return raw


def body_mask(font, image, lines):
    expected, line_checks = set(), []
    for row, text in enumerate(lines):
        matches = []
        for x in (16, 22):
            y = 297 + row * 16
            try:
                ink, bounds = complete_mask(font, text, image, x, y, INK)
            except ValueError:
                continue
            matches.append((x, y, ink, bounds))
        (x, y, ink, bounds), = matches
        expected.update((x + dx, y + dy) for dx, dy in glyphs(font, text))
        line_checks.append(dict(text=text, ink_pixels=ink, bounds=bounds))
    actual = {(x, y) for x in range(16, 245) for y in range(296, 346) if image.getpixel((x, y)) == INK}
    assert actual == expected
    return line_checks


def main():
    assert not REPORT.exists() and not SHEET.exists()
    report_file, terminal_file = ROOT / "capture/capture_report.json", ROOT / "terminal.json"
    release, report, terminal = map(read, (RELEASE, report_file, terminal_file))
    assert release["candidate_sha256"] == digest(release["candidate"]) == report["ROM_sha256"] == terminal["candidate_sha256"]
    assert release["clean_input_sha256"] == digest("work/clean.nds")
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["frames"] == terminal["total_frames"] == 11750
    assert terminal["ordinary_controller_inputs"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert digest(DONOR) == report["battery_save_preloaded"]["source_sha256"] == terminal["copied_save_sha256"]
    assert all(digest(p) == sha for p, sha in terminal["evidence"].items())
    frames = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_navigation.png")}
    snapshots = {r["frame"]: r for r in report["read_only_pause_RAM_snapshots"]}
    clean, image = map(NdsImage.open, ("work/clean.nds", release["candidate"]))
    source_arm, arm = clean.read_file(ARM), image.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), source_arm)
    common = image.read_file(COMMON)
    assert sha256(common).hexdigest() == release["target_COMMON_sha256"]
    installed = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    font = GameAsciiFont.from_arm9(arm)
    rows, screens = [], {}
    for frame, (key, args, speaker, note) in HOLDS.items():
        shot = frames[frame]
        with Image.open(shot["path"]) as original:
            panel = original.convert("RGB")
        assert digest(shot["path"]) == shot["PNG_sha256"] and panel.size == (256, 384)
        screens[frame] = panel
        raw = load_exact(snapshots[frame])
        plain, rendered = (text_at(raw, unpack_from("<I", arm, off)[0]) for off in (0x5444C, 0x54450))
        matches = []
        byte_args = tuple(value.encode("cp932") for value in args)
        if key < 3668:
            matches = [r for r in terminal["common_requests"] if r["message_ID"] == key and r["frame"] < frame]
            assert [r["PC"] for r in matches] == [0x0205528C, 0x020534F4]
            jp, english = source[key].text, installed[key].text
            jp_ref, en_ref = town.reference(source[key]), town.reference(installed[key])
            file = COMMON
        else:
            source_ptr, current_ptr = (unpack_from("<I", code, key)[0] for code in (source_arm, arm))
            jp, english = text_at(source_arm, source_ptr), text_at(raw, current_ptr)
            jp_ref = dict(pointer_file_offset=key, text_address=source_ptr)
            en_ref = dict(pointer_file_offset=key, text_address=current_ptr, initialized_RAM=True)
            file = ARM
        assert jp.count(b"%s") == english.count(b"%s") == len(byte_args)
        assert (english % byte_args).split() == plain.split() == rendered.split()
        lines = [text.strip() for text in rendered.decode("cp932").split("\n")]
        if frame == 11500:
            raster, kanji = town.font_tools(image)[0], image.read_file("/GRP/KANJI.FNT")
            plane, codes = town.render_portrait(raster, arm, kanji, rendered)
            assert [glyph["code"] for glyph in codes] == town.glyph_codes(rendered)
            actual = panel.crop((16, 296, 244, 360)).get_flattened_data()
            assert len(actual) == len(plane) == 228 * 64
            pale_ink = (197, 198, 197)
            assert bytes(bool(value) for value in plane) == bytes(pixel in (INK, pale_ink) for pixel in actual)
            assert actual.count(pale_ink) == 20
            glyph_proof = dict(native_raster_sha256=sha256(bytes(plane)).hexdigest(), glyphs=len(codes),
                               pale_numeral_ink_pixels=20)
        else:
            glyph_proof = dict(full_ASCII_lines=body_mask(font, panel, lines))
        if speaker:
            ink, bounds = complete_mask(font, speaker, panel, 16, 277, (98, 97, 98))
            glyph_proof["nameplate"] = dict(ink=ink, bounds=bounds)
        rows.append(dict(frame=frame, file_path=file, key=key, source_reference=jp_ref, installed_reference=en_ref,
            source_hex=jp.hex(), source_Japanese=jp.decode("cp932"), installed_hex=english.hex(),
            speaker=speaker or "System", arguments=args, shown=lines, caller_requests=matches,
            decision="revision lead" if key in REVISION_LEADS else "retention",
            proposal=REVISION_LEADS.get(key), localization_note=note, exact_visible_glyphs=glyph_proof,
            review=dict(source=True, context=True, localization=key not in REVISION_LEADS,
                        naturalness=key not in REVISION_LEADS, formatting=True),
            screenshot=shot, snapshot=snapshots[frame]))
    positions = {f: position(Path(snapshots[f]["path"])) for f in (4500, 6450, 8300, 9300, 11750)}
    assert positions[8300]["sailors"] == positions[11750]["sailors"] == 39
    assert positions[8300]["water_and_food"] == (42, 43) and positions[9300]["water_and_food"] == (150, 150)
    assert positions[8300]["azores_point"] == (16864, 5696)
    assert sum((x-y)**2 for x, y in zip(positions[8300]["ship_position"], positions[8300]["azores_point"], strict=True)) < 72**2
    samples = (8300, 8420, 8550, 9100, 9620, 10700, 10980, 11500)
    sheet = Image.new("RGB", (2 * 272 + 12, 4 * 218), "#28313b")
    title = ImageDraw.Draw(sheet)
    for n, frame in enumerate(samples):
        x, y = 8 + 272 * (n % 2), 218 * (n // 2)
        title.text((x, y + 4), str(frame), fill="white")
        sheet.paste(screens[frame].crop((0, 192, 256, 384)), (x, y + 23))
    sheet.save(SHEET)
    result = dict(candidate_sha256=release["candidate_sha256"], ordinary_replay=True, original_lisbon_save=reference(DONOR),
        records=rows, fleet_positions_and_supplies=positions, discovered_and_docked_azores=True,
        filled_food_and_water_in_original_menu=True, entered_English_letter_and_confirmed=True, rejected_words_observed=True,
        departed_after_gift_notice=True, gameplay_outside_this_run=["accepted Promised Words", "developed facilities", "hardware"],
        goal_complete=False, new_editorial_credit=0, sheet=reference(SHEET),
        evidence=terminal["evidence"] | {str(terminal_file): digest(terminal_file), str(RELEASE): digest(RELEASE)})
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified the full ordinary Azores visit and three lines that need source or language corrections.")


if __name__ == "__main__":
    main()
