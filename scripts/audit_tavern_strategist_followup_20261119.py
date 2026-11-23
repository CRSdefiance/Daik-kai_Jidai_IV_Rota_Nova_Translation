"""Certify actual Tavern scheme pages, choice cancellation and startup."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
import re
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from scripts import audit_ceuta_lesson_20261119 as original
from scripts import replay_tavern_strategist_followup_20261119 as play
from scripts import verify_scheme_gameplay_v776 as native
from scripts import verify_tavern_strategist_followup_20261119 as offline

base, build = play.base, play.build
PROOF = play.ROOT / "verified_london_schemes.json"
STARTUP = build.ROOT / "own_startup_verification.json"
SCENES = {
    6000: (909, ()), 7200: (915, (b"Lure Fleet",)),
    16400: (921, ()), 17200: (941, (b"Clifford", b"London")), 17600: (941, (b"Clifford", b"London")),
    23200: (949, (b"Argot Co.", b"Clifford")),
    28400: (927, ()), 29600: (957, (b"London", b"Clifford")), 30000: (957, (b"London", b"Clifford")),
}


def gameplay():
    assert not PROOF.exists()
    terminal_path = play.ROOT / "terminal.json"
    terminal = base.load(terminal_path)
    assert terminal["terminal"] and terminal["frames"] == play.FRAMES
    report_path = Path(terminal["report"])
    assert base.digest(report_path) == terminal["report_sha256"]
    report = base.load(report_path)
    assert report["ROM_sha256"] == terminal["candidate_sha256"] == base.digest(build.ROM)
    assert report["scripted_input_schedule"] == base.load(play.INPUTS) and base.digest(play.INPUTS) == terminal["controls_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and donor["source"] != donor["destination"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    fixture, = report["synthetic_strategist_room_assignment_fixtures"]
    assert fixture["frame"] == 3200 and fixture["only_three_assignment_bytes_one_XP_word_one_calendar_word_owned"]
    assert fixture["all_other4MiB_bytes_exact"] and fixture["calendar_days_advanced"] == 11

    proof, painter = map(base.load, (build.PROOF, offline.PROOF))
    assert proof["candidate_sha256"] == painter["candidate_sha256"] == report["ROM_sha256"]
    draft = {r["message_ID"]: r for r in proof["records"]}
    image = base.NdsImage.open(build.ROM)
    arm, common, kanji = (image.read_file(p) for p in (build.ARM, build.COMMON, "/GRP/KANJI.FNT"))
    wf = build.workflow
    entries = wf.owned_entries(common, arm, build.native.digest(arm[wf.DIRECTORY_OFFSET:wf.TABLE_OFFSET]))
    blocks = build.native.IlnkContainer.parse(common).blocks
    formatted_ptr, wrapped_ptr, owner = [unpack_from("<I", arm, off)[0] for off in (0x5444C, 0x54450, 0x552A0)]
    layouts, _ = native.formatter()
    screenshots = {r["frame"]: r for r in report["frames_captured"]}
    ram_meta = {r["frame"]: r for r in report["read_only_capture_RAM_snapshots"] + report["read_only_pause_RAM_snapshots"]}

    def ram(frame):
        entry = ram_meta[frame]
        data = Path(entry["path"]).read_bytes()
        assert entry["read_only_export"] and len(data) == 0x400000
        assert build.native.digest(data) == entry["sha256"]
        return data

    _, expected_fixture = play.scoped_expert(arm, ram(3200), True)
    assert fixture == expected_fixture | {"frame": 3200}
    holds = []
    for frame, (ident, expected) in SCENES.items():
        raw = ram(frame)
        capture = screenshots[frame]
        assert base.digest(capture["path"]) == capture["PNG_sha256"]
        template = entries[ident].text
        assert native.cstring(raw, owner + 0x2030) == template and raw.count(blocks[entries[ident].block]) == 1
        pattern = b"(.*?)".join(re.escape(part) for part in template.split(b"%s"))
        match = re.fullmatch(pattern, native.cstring(raw, formatted_ptr))
        assert match is not None and match.groups() == expected, (frame, ident, expected)
        row = draft[ident]
        cpu = native.machine(arm)
        cpu.mem_write(0x02000000, raw)
        displayed = layouts(cpu, row | {"source_voice_table": row["original_voice_table"]}, expected)
        formatted = bytes.fromhex(displayed["formatted_hex"])
        assert formatted == native.cstring(raw, wrapped_ptr), (frame, ident, displayed["lines"])
        plane = offline.native_portrait(arm, kanji, formatted, displayed["lines"])
        wanted = {(16 + i % 228, 296 + i // 228) for i, v in enumerate(plane) if v == 1}
        with Image.open(capture["path"]) as file:
            rendered = file.convert("RGB")
        actual = {(x, y) for y in range(294, 366) for x in range(16, 244)
                  if rendered.getpixel((x, y)) == (0, 8, 0)}
        assert actual == wanted, (frame, ident, len(wanted - actual), len(actual - wanted))
        holds.append(dict(frame=frame, message_ID=ident, arguments=[v.decode("ascii") for v in expected],
            lines=displayed["lines"], capture=capture, complete_body_mask=True))
    start_state = native.state(arm, ram(3200))
    after = {f: native.state(arm, ram(f))["cash"] for f in (18000, 24000, 30400, 31200)}
    assert start_state["cash"] == 40659 and set(after.values()) == {40644}
    # The text buffer persists after dismissal. Check the live menu surfaces.
    transitions = {}
    for frame in (18000, 24000, 30400, 30800, 31200):
        entry = screenshots[frame]
        assert base.digest(entry["path"]) == entry["PNG_sha256"]
        with Image.open(entry["path"]) as captured:
            transitions[frame] = captured.convert("RGB").crop((0, 192, 256, 384))
    assert len({transitions[frame].tobytes() for frame in (18000, 24000, 30400)}) == 1
    town_highlight = (60, 50, 104, 66)
    delta = ImageChops.difference(transitions[30800], transitions[31200])
    assert delta.getbbox() == town_highlight
    returned = screenshots[31200]
    live_ids = {r["message_ID"] for r in holds} & {r["message_ID"] for r in painter["revisions"]}
    assert live_ids == {909, 915, 927, 941, 957}
    frames = [(f"COMMON {row['message_ID']} at {row['frame']}", row["capture"]) for row in holds]
    frames.append(("Tavern menu after all three cancellations", screenshots[30400]))
    frames.append(("London town after leaving the Tavern", returned))
    sheets = []
    for start in range(0, len(frames), 6):
        group = frames[start:start + 6]
        sheet = Image.new("RGB", (1040, ((len(group) + 1) // 2) * 404), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (label, data) in enumerate(group):
            x, y = (i % 2) * 520, (i // 2) * 404
            draw.text((x + 4, y + 2), label, fill="white")
            with Image.open(data["path"]) as opened:
                image = opened.convert("RGB").crop((0, 192, 256, 384))
            sheet.paste(image.resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 16))
        path = play.ROOT / f"london_schemes_replay_{1 + start // 6}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    evidence = {str(p): base.digest(p) for p in (terminal_path, report_path, build.PROOF, offline.PROOF, play.INPUTS)}
    for frame in {3200, 18000, 24000, 30400, 31200, *SCENES}:
        data = ram_meta[frame]
        evidence[data["path"]] = data["sha256"]
    for frame in transitions:
        data = screenshots[frame]
        evidence[data["path"]] = data["PNG_sha256"]
    base.save(PROOF, dict(candidate_sha256=report["ROM_sha256"], holds=holds, revised_IDs=sorted(live_ids),
        cash_at_each_cancellation=after, fixture=fixture, terminal_town=returned, sheets=sheets,
        same_tavern_menu_after_cancellation=[18000, 24000, 30400],
        terminal_town_highlight_only_pixels=list(town_highlight),
        natural_eligibility=False, hardware=False, evidence=evidence))
    print("Verified five revised Tavern records, both argument orders, and the original cancellations.")


def startup():
    source = getsource(original.startup).replace("proof['predecessor_sha256']", "proof['previous_sha256']")
    scope = vars(original) | {"play": play, "build": build, "STARTUP": STARTUP, "__file__": __file__}
    exec(compile(source, __file__ + "::same-startup-contract", "exec"), scope)
    scope["startup"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
