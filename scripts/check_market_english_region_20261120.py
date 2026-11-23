"""Verify the Market Info region renderer and the paired ordinary London replay."""

from pathlib import Path
from struct import pack, unpack, unpack_from

from PIL import Image, ImageChops, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_FP, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_market_english_region_20261120 as replay
from scripts import stage_market_english_region_20261120 as stage
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.probe_button_prompt_native import STACK
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_forces_relationships_20261115 import HEADER, VIEW, font_points
from scripts.verify_personal_gameplay_v841 import get_machine


BASE, ROOT, base = stage.BASE, stage.ROOT, stage.base
PROOF, NATIVE_SHEET, SHEET = (ROOT / name for name in ("verification.json", "native_regions.png", "london_comparison.png"))
HEADER_RECT, TERRITORIES = 0x11AFA4, 21
BOX = (10, 90, 118, 102)
COMPANIONS = {
    0x1223E4: ("アレキサンドリア", "Alexandria"),
    0x122504: ("サン＝ジョルジェ", "Sao Jorge"),
}
MEANINGS = (
    "Use English for the cultural region associated with England in this setting.",
    "Keep Flanders as the historical trading region named by the source.",
    "German describes the cultural region without introducing modern borders.",
    "Nordic retains the wider northern European area without naming a specific country.",
    "Use the established name Portugal for its regional market group.",
    "Spain names the same regional grouping used in Iberian trade.",
    "Italy names the region without implying a unified state in this period.",
    "Greece names the source cultural area without adding a political claim.",
    "Turkey is the established geographic label for this regional market group.",
    "Egypt is the source area and the established English name.",
    "West Africa keeps the direction and the regional scope.",
    "East Africa keeps it distinct from the separately listed western market group.",
    "Arab describes the cultural region without limiting it to the Arabian Peninsula.",
    "India names the original regional grouping and matches the geographic terminology.",
    "Indochina keeps the source geographic grouping used by this market table.",
    "Indonesia is the established geographic label for the island group in this market.",
    "China is the source region and the form used elsewhere in the interface.",
    "Korea keeps the source region without imposing a modern political division.",
    "Japan is the source region and the form used elsewhere in the interface.",
    "Caribbean denotes the sea and island market group rather than one settlement.",
    "Mexico keeps this market group distinct from the separately listed Caribbean.",
)


def string(arm, field):
    pointer, = unpack_from("<I", arm, field)
    offset = pointer - BASE
    assert 0 < offset < len(arm)
    raw = arm[offset:arm.index(0, offset) + 1]
    return dict(pointer_field_offset=field, text_offset=offset, exact_hex=raw.hex(),
                text=raw[:-1].decode("cp932"))


def native(arm, clean, previous, raw):
    assert unpack_from("<7I", arm, HEADER_RECT) == (1, 10, 90, 0, 0, 108, 12)
    width, height = BOX[2] - BOX[0], BOX[3] - BOX[1]
    byte_count = width * height // 2
    ctx = STACK + 0x12C
    header = pack("<5I", 4, width // 4, height, 20, 20)
    guards = b"\xa5" * 16
    cpu, get = get_machine(arm, raw)
    font = GameAsciiFont.from_arm9(arm)
    root = get(0xCB178)
    towns = {i: [] for i in range(TERRITORIES)}
    for i in range(90):
        town = root + 4 + 108 * i
        towns[get(0xB51B4, town)].append((i, town))
    assert all(towns.values())
    sheet = Image.new("RGB", (690, 7 * 61), "#273034")
    captions = ImageDraw.Draw(sheet)
    records = []
    for culture, groups in towns.items():
        field = stage.FIELD + culture * 256
        original, prior, installed = (string(a, field) for a in (clean, previous, arm))
        name = installed["text"]
        assert name.isascii() and (prior == installed if culture else name == stage.ENGLISH)
        if culture == 0:
            assert original == prior and original["text"] == stage.SOURCE
        expected = f"{name} Region"
        assert len(expected) * 6 <= width
        x = (width - len(expected) * 6) // 2
        expected_pixels = font_points(font, expected, x, 1)

        def draw(u, _pc, _size, _user):
            pointer = u.reg_read(UC_ARM_REG_R1)
            assert u.reg_read(UC_ARM_REG_R0) == ctx
            assert bytes(u.mem_read(pointer, len(expected) + 1)) == expected.encode("ascii") + b"\0"
            assert unpack("<2i", u.mem_read(ctx + 0x24, 8)) == (x, 0)
            draws.append(pointer)

        for index, town in groups:
            obj = get(0xB5188, town)
            assert unpack("<I", cpu.mem_read(obj + 4, 4))[0] == BASE + installed["text_offset"]
            cpu.mem_write(HEADER - 16, guards + header + bytes(byte_count) + guards)
            get(0xD3D80, VIEW)
            cpu.mem_write(STACK, pack("<4I", width, height, 0, 0))
            get(0xD3AFC, VIEW, HEADER, 0, 0)
            get(0xD5160, ctx, VIEW, 1)
            cpu.reg_write(UC_ARM_REG_FP, town)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            draws = []
            hook = cpu.hook_add(UC_HOOK_CODE, draw, begin=0x020D5404, end=0x020D5404)
            try:
                cpu.emu_start(0x020BE9B8, 0x020BEA08, count=200000)
            finally:
                cpu.hook_del(hook)
            assert len(draws) == 1 and cpu.reg_read(UC_ARM_REG_PC) == 0x020BEA08
            assert cpu.reg_read(UC_ARM_REG_SP) == STACK
            assert cpu.mem_read(HEADER - 16, 16) == cpu.mem_read(HEADER + 20 + byte_count, 16) == guards
            assert cpu.mem_read(HEADER, 20) == header
            pixels = bytes(p for b in cpu.mem_read(HEADER + 20, byte_count) for p in (b & 15, b >> 4))
            actual = {(i % width, i // width) for i, p in enumerate(pixels) if p}
            assert actual == expected_pixels and set(pixels) == {0, 1}, (index, name)

        px, py = culture % 3 * 230 + 6, culture // 3 * 61
        captions.text((px, py + 3), f"{culture:02d}  {expected}", fill="white")
        mask = Image.frombytes("L", (width, height), pixels).point(lambda p: 240 if p else 35)
        sheet.paste(mask.resize((width * 2, height * 2), Image.Resampling.NEAREST), (px, py + 22))
        records.append(dict(id=f"DK4_MARKET_CULTURAL_REGION_{culture:02d}", speaker="Market Info",
            source_reference=original, current_reference=prior, target_reference=installed,
            source_meaning=f"{original['text']} is the cultural area used by the selected town's market.",
            context="Cultural-region label above the goods and trend tables in the selected town's Market Info report.",
            english=expected, localization_note=MEANINGS[culture], decision="revision" if culture == 0 else "retention",
            review=dict.fromkeys(stage.parent.batch.GATES, True), one_line=True, text_pixels=len(actual),
            viewport_width=width, original_town_indices=[i for i, _ in groups]))
    sheet.save(NATIVE_SHEET)
    assert sum(len(r["original_town_indices"]) for r in records) == 90
    return records


def gameplay(reports, arm):
    before, revised = reports
    assert before["scripted_input_schedule"] == revised["scripted_input_schedule"]
    assert before["core_DLL_sha256"] == revised["core_DLL_sha256"] and before["core_options"] == revised["core_options"]
    assert all(r["cold_boot"] and not r["savestate_loaded"] and not r["callback_errors"] for r in reports)
    assert not any(v for r in reports for k, v in r.items() if k.startswith("synthetic_"))
    for report in reports:
        donor = report["battery_save_preloaded"]
        assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    before_shots, after_shots = map(shots, reports)
    font = GameAsciiFont.from_arm9(arm)
    holding, evidence = [], {}
    comparison = Image.new("RGB", (520, 394), "#273034")
    captions = ImageDraw.Draw(comparison)
    for frame in replay.FRAMES:
        earlier, later = before_shots[frame], after_shots[frame]
        old, new = map(captured, (earlier, later))
        evidence.update({earlier["path"]: earlier["PNG_sha256"], later["path"]: later["PNG_sha256"]})
        diff = ImageChops.difference(old, new).getbbox()
        if diff is None:
            continue
        assert diff[0] >= BOX[0] and diff[1] >= BOX[1] and diff[2] <= BOX[2] and diff[3] <= BOX[3], (frame, diff)
        ink = font_mask(new, font, "English Region", 22, 91, BOX, (230, 230, 230))
        assert ink > 0
        if not holding:
            for n, (label, screen) in enumerate((("Before", old), ("Revised", new))):
                captions.text((n * 260 + 6, 1), label, fill="white")
                comparison.paste(screen, (n * 260, 10))
        holding.append(dict(frame=frame, complete_pixels=ink, image_change_bounds=diff))
    assert holding and holding[-1]["frame"] < replay.FRAMES[-1]
    comparison.save(SHEET)
    return holding, evidence


def main():
    assert not any(path.exists() for path in (PROOF, NATIVE_SHEET, SHEET))
    staged = base.load(stage.PROOF)
    report_paths = [ROOT.parent / f"{version}_report/capture/capture_report.json" for version in ("parent", "revised")]
    reports = [base.load(path) for path in report_paths]
    assert [r["ROM_sha256"] for r in reports] == [staged["parent_sha256"], staged["candidate_sha256"]]
    arm, clean, prior = [base.NdsImage.open(path).read_file(stage.ARM) for path in (stage.ROM, stage.CLEAN, stage.parent.ROM)]
    holds, evidence = gameplay(reports, arm)
    first = holds[0]["frame"]
    ram, = [r for r in reports[1]["read_only_capture_RAM_snapshots"] if r["frame"] == first]
    assert ram["read_only_export"] and base.digest(ram["path"]) == ram["sha256"]
    rows = native(arm, clean, prior, Path(ram["path"]).read_bytes())
    alias_rows = []
    for offset, (jp, en) in COMPANIONS.items():
        source, previous, current = (string(a, offset) for a in (clean, prior, arm))
        assert source["text"] == jp and previous == current and current["text"] == en
        alias_rows.append(dict(source=source, previous=previous, current=current,
            disposition="Already localized in the stored actor field before this batch."))
    evidence.update({str(p): base.digest(p) for p in report_paths})
    evidence[ram["path"]] = ram["sha256"]
    base.save(PROOF, dict(candidate_sha256=staged["candidate_sha256"], parent_sha256=staged["parent_sha256"],
        records=rows, actual_London_report_holds=holds, checked_ordinary_return=True, hardware=False,
        retrospective_actor_alias_references=alias_rows, evidence=evidence,
        sheets={str(p): base.digest(p) for p in (NATIVE_SHEET, SHEET)}))
    print(f"Verified {len(rows)} regional headings for 90 towns and {len(holds)} ordinary London report holds.")


if __name__ == "__main__":
    main()
