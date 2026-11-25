"""Verify the level-up digit change in native execution and ordinary gameplay."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack_from
from unicodedata import normalize

from PIL import Image, ImageChops, ImageDraw

from scripts import stage_levelup_numerals_20261125 as build
from scripts import stage_market_trade_dialogue_20261115 as native
from scripts import verify_lisbon_guild_bargaining_replay_20261125 as paired
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, sha256, write


NATIVE = build.ROOT / "levelup_numerals_native_20261125.json"
OUT = paired.OUT.with_name("levelup_numerals_paired_20261125.json")
SHEET = OUT.with_suffix(".png")
ROW_COUNTS = ([1], [2], [4], [4, 1], [4, 2], [4, 2])
AMOUNTS = (
    (0, 0, 0, 0, 0, 2),
    (0, 2, 0, 3, 0, 0),
    (1, 2, 0, 0, 3, 2),
    (0, 3, 2, 1, 3, 2),
    (3, 3, 3, 3, 3, 3),
    (9, 10, 99, 100, 255, 2),
)


def native_checks():
    proof, release = map(read, (build.PROOF, build.current.RELEASE))
    parent = native.RegisteredRuntime(build.current.RELEASE, release["own_registered_startup"], captain=3)
    clean, candidate = map(NdsImage.open, (CLEAN, build.ROM))
    original_arm = clean.read_file(build.current.ARM)
    target_arm, edit = build.proposed_arm9(original_arm, parent.arm)
    assert edit == proof["edit"] and target_arm == candidate.read_file(build.current.ARM)
    assert parent.common == candidate.read_file(build.current.COMMON)
    assert parent.image.read_file("/GRP/KANJI.FNT") == candidate.read_file("/GRP/KANJI.FNT")
    target = native.with_components(parent, target_arm, parent.common)
    offset = edit["offset"]
    assert target.raw[offset:offset + 4] == bytes.fromhex(edit["before_hex"])
    target.raw = target.raw[:offset] + target_arm[offset:offset + 4] + target.raw[offset + 4:]
    messages = build.growth.common_message_entries
    jp = messages(clean.read_file(build.current.COMMON), original_arm)[336]
    layout = slice(native.DIRECTORY_OFFSET, native.TABLE_OFFSET)
    en = native.owned_entries(parent.common, parent.arm, sha256(parent.arm[layout]).hexdigest())[336]
    assert jp.text.decode("cp932") == "%sが\n%s上がりました！"
    assert en.text == b"%s increased by %s!"
    cases, previews = [], []
    raster = build.growth.get_raster(target.image)
    for sequence, (amounts, splits) in enumerate(zip(AMOUNTS, ROW_COUNTS, strict=True), 1):
        a, before_raw, before_body, before_reads = build.growth.native_growth(parent, amounts, en.text)
        b, after_raw, after_body, after_reads = build.growth.native_growth(target, amounts, en.text)
        assert a != b and before_reads == after_reads
        assert [(name, normalize("NFKC", number.decode("cp932")).encode("ascii")) for name, number in a] == b
        assert [number for _, number in b] == [str(number).encode("ascii") for number in amounts if number]
        if sequence == 1:
            assert b == [(b"Luck", b"2")]
        before_pages = build.growth.page_masks(parent, before_body)
        after_pages = build.growth.page_masks(target, after_body)
        assert [len(page["rows"]) for page in before_pages] == [len(page["rows"]) for page in after_pages] == splits
        remaining = after_body
        for page_number, page in enumerate(after_pages, 1):
            plane, used = raster(target_arm, remaining, build.growth.ENTRY, size=(228, 64), complete=False,
                                 instruction_limit=2000000)
            assert used == page["consumed_bytes"] and sha256(plane).hexdigest() == page["native_plane_sha256"]
            remaining = remaining[used:]
            previews.append((f"336, case {sequence}, page {page_number}", plane))
        assert not remaining
        cases.append(dict(amounts=amounts, supplied_numeric_stress=sequence == len(AMOUNTS),
            argument_names=[name.decode("ascii") for name, _ in b], before_raw=before_raw.hex(), after_raw=after_raw.hex(),
            formatted_before=before_body.hex(), formatted_after=after_body.hex(),
            native_before=before_pages, native_after=after_pages, directory_reads=after_reads))
    sheets = native.portrait_sheets(build.ROOT, previews)
    write(NATIVE, dict(stage=reference(build.PROOF), candidate=proof["candidate"], parent=proof["parent"],
        clean_reference=paired.panels.text_reference(jp) | {"exact_hex": jp.text.hex()},
        installed_reference=paired.panels.text_reference(en) | {"exact_hex": en.text.hex()},
        stat_gain_template_unchanged=True, exact_native_cases=cases, native_pages=len(previews), native_previews=sheets,
        original_four_plus_two_pagination_preserved=True, ordinary_gameplay=False))
    print(f"Six native level-up cases passed with {len(previews)} complete proposed pages.")


def replay_checks():
    proof, source, prior = map(read, (build.PROOF, build.current.review.OUT, build.current.gameplay.OUT))
    old, new = map(read, (prior["replay"]["path"], build.CAPTURE / "capture_report.json"))
    assert prior["replay"] == reference(prior["replay"]["path"]) and prior["ordinary_gameplay"]
    assert new["ROM_sha256"] == proof["candidate"]["sha256"] == digest(build.ROM)
    assert old["ROM_sha256"] == proof["parent"]["sha256"] == digest(build.current.ROM)
    for field in ("core_DLL_sha256", "core_options", "scripted_input_schedule", "frames"):
        assert old[field] == new[field]
    for run in (old, new):
        assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
        assert not any(value for key, value in run.items() if key.startswith("synthetic_"))
    previous_donor, donor = (run["battery_save_preloaded"] for run in (old, new))
    assert previous_donor["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
    panels = paired.panels
    before, after = (panels.shots(report, "_cold_boot.png") for report in (old, new))
    frames = build.current.replay.FRAMES
    assert set(frames) <= set(before) & set(after)
    companions = [frame for frame in frames if frame != build.HOLD]
    for frame in companions:
        diff = ImageChops.difference(panels.picture(before[frame]), panels.picture(after[frame]))
        assert diff.getbbox() is None, (frame, diff.getbbox())
    previous_text = source["stat_growth_glyph_lead"]
    assert bytes.fromhex(previous_text["formatted_hex"]) == b" Luck increased by \x82Q!"
    arm = NdsImage.open(build.ROM).read_file(build.current.ARM)
    snapshot, = (row for row in new["read_only_pause_RAM_snapshots"] if row["frame"] == build.HOLD)
    raw = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and len(raw) == snapshot["bytes"] == 0x400000
    assert sha256(raw).hexdigest() == snapshot["sha256"]
    offsets = [unpack_from("<I", arm, offset)[0] - build.BASE for offset in (0x5444C, 0x54450)]
    values = [raw[at:at + 256].split(b"\0", 1)[0] for at in offsets]
    assert values == [b" Luck increased by 2!"] * 2
    left, right = (panels.picture(shots[build.HOLD]) for shots in (before, after))
    glyphs = panels.exact_body(paired.GameAsciiFont.from_arm9(arm), ("Luck increased by 2!",), right)
    delta = ImageChops.difference(left, right)
    delta.paste((0, 0, 0), paired.ADVANCE)
    change = delta.getbbox()
    x0, y0, x1, y1 = paired.BODY
    assert change and x0 <= change[0] < change[2] <= x1 and y0 <= change[1] < change[3] <= y1
    sheet = Image.new("RGB", (1024, 410), "#263238")
    draw = ImageDraw.Draw(sheet)
    for index, (label, frame) in enumerate((("Guild candidate", left), ("Stat numeral candidate", right))):
        x = index * 512
        draw.text((x + 10, 7), label, fill="white")
        sheet.paste(frame.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x, 22))
    sheet.save(SHEET)
    write(OUT, dict(candidate=proof["candidate"], parent=proof["parent"], ordinary_gameplay=True,
        exact_companion_frames=companions, frame=build.HOLD, previous_expansion_hex=previous_text["expansion_hex"],
        fixed_expansion_hex=values[0].hex(), fixed_formatted_hex=values[1].hex(), changed_body_bounds=change,
        previous_frame=before[build.HOLD], candidate_frame=after[build.HOLD], exact_glyph_check=glyphs,
        snapshot=snapshot, sheet=reference(SHEET), baseline=prior["replay"],
        replay=reference(build.CAPTURE / "capture_report.json")))
    print(f"Observed Julio's ASCII Luck gain and {len(companions)} pixel-exact companion screens.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("native", "replay"))
    {"native": native_checks, "replay": replay_checks}[parser.parse_args().action]()
