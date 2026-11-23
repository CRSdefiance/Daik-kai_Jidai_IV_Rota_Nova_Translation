"""Verify Lil's real poem pages, name substitution, and return after the fixture."""

from argparse import ArgumentParser
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import audit_ceuta_lesson_20261119 as startup_template
from scripts import audit_rafael_sailing_modes_playback_20261119 as display
from scripts import replay_manuel_poem_cross_route_20261119 as play
from scripts import verify_manuel_poem_cross_route_20261119 as offline
from scripts.verify_all_items_gallery_v535 import glyph_pixels

base, build = play.base, play.build
PROOF = play.ROOT / "verified_aftermath.json"
STARTUP = build.ROOT / "own_startup_verification.json"
STANZAS = ("DK4_MES_B11_R0044", "DK4_MES_B11_R0047", "DK4_MES_B11_R0051")


def gameplay():
    assert not PROOF.exists()
    folder = play.ROOT / "route2_English"
    terminal_path = folder / "terminal.json"
    terminal = base.load(terminal_path)
    assert terminal["terminal"] and terminal["frames"] == play.FRAMES
    assert terminal["all_callbacks_readonly_andhost_slots_restored"]
    evidence = {str(terminal_path): base.digest(terminal_path)}
    for key in ("report", "observer", "run_plan"):
        path = terminal[key]
        assert base.digest(path) == terminal[key + "_sha256"]
        evidence[path] = terminal[key + "_sha256"]
    report, trace, plan = (base.load(terminal[key]) for key in ("report", "observer", "run_plan"))
    setup, native = map(base.load, (play.FIXTURES, offline.PROOF))
    fixture, = setup["fixtures"]
    assert base.digest(play.FIXTURE) == fixture["research_ROM_sha256"] == report["ROM_sha256"]
    assert setup["exact_candidate_inverse"] and base.digest(build.ROM) == setup["candidate_sha256"] == native["candidate_sha256"]
    assert (plan["route"], plan["displayed_original_block"], plan["entry_opening_block"]) == (2, 11, 22)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(plan["inputs"]) and base.digest(plan["inputs"]) == plan["inputs_sha256"]
    assert not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]

    pictures = display.captures(report)
    font = GameAsciiFont.from_arm9(base.NdsImage.open(build.ROM).read_file(build.native.ARM))
    actor_names = {2: "Lil Argot", 9: "Camille Overijssel", 23: "Manuel Almeida"}
    name_ink = {n: glyph_pixels(font, b"", (), name, 16, 277, advance=6) for n, name in actor_names.items()}
    resident = {r["offset"]: r for r in fixture["all_fixture_commands"]}
    words = {r["fixture_command_offset"]: r for r in fixture["original_text_records"]}
    revised = {r["id"]: r["pages"][0] for r in native["revisions"] if r["file_path"] == play.FILE}
    assert len(revised) == 8
    speeches, holds, frames, commands = [], [], [], []
    exit_frame = None
    for returned in trace["rows"]:
        source = returned["source"]
        if returned["kind"] != "after_command" or (
            source.get("classification"), source.get("route"), source.get("block")
        ) != ("original_SC_cache", 2, 22):
            continue
        entered = trace["rows"][returned["entry_row"]]
        assert source["whole_resident_payload_exact_ROM"] and source["actual_sha256"] == source["registered_sha256"]
        assert returned["CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback"]
        at, word = source["instruction_offset"], source["first_word"]
        assert word == resident[at]["word"] == entered["source"]["first_word"]
        assert not commands or at > commands[-1]
        commands.append(at)
        if word == 0:
            assert returned["result_words"][0] == 0
            exit_frame = returned["frame"]
            break
        if at not in words:
            continue
        record = words[at]
        ident, selector = record["id"], record["source_selector"]
        speeches.append(ident)
        if ident not in revised:
            continue
        plane = bytes.fromhex(revised[ident]["native_plane_hex"])
        assert len(plane) == 216 * 64 and set(plane) == {0, 1}
        wanted = b"".join(plane[i:i+216] + bytes(12) for i in range(0, len(plane), 216))
        interval = (entered["frame"], returned["frame"])
        for n, (frame, image) in sorted(pictures.items()):
            if not interval[0] + 25 < n < interval[1] - 4:
                continue
            body = bytes(c == (0, 8, 0) for c in image.crop((16, 296, 244, 360)).get_flattened_data())
            if body != wanted:
                continue
            width = len(actor_names[selector]) * 6
            name = {(x, y) for y in range(276, 289) for x in range(14, 18 + width)
                    if image.getpixel((x, y)) == (98, 97, 98)}
            assert name == name_ink[selector], (ident, n)
            presses = [e["start"] for e in report["scripted_input_schedule"]
                       if n < e["start"] <= interval[1] and e["buttons"] == ["A"]]
            holds.append(dict(id=ident, frame=n, capture=frame["path"], capture_sha256=frame["PNG_sha256"],
                              complete_body_and_name_mask=True, speaker=selector,
                              name=actor_names[selector], A_presses_from_hold_to_return=presses))
            frames.append((ident, image))
            break
        else:
            raise AssertionError((ident, interval))
    assert exit_frame is not None and len(speeches) == len(set(speeches)) == 15
    assert {r["id"] for r in holds} == revised.keys()
    first = speeches.index(STANZAS[0])
    assert tuple(speeches[first:first + 3]) == STANZAS
    assert all(len(r["A_presses_from_hold_to_return"]) == 1 for r in holds if r["id"] in STANZAS)
    no, = (r for r in holds if r["id"] == "DK4_MES_B11_R0066")
    assert no["name"] == "Camille Overijssel"
    later = min(n for n in pictures if n > exit_frame + 100)
    frames.append(("After the original New Game return", pictures[later][1]))
    sheets = []
    for start in range(0, len(frames), 6):
        batch = frames[start:start + 6]
        sheet = Image.new("RGB", (1040, ((len(batch) + 1) // 2) * 404), "#263238")
        pen = ImageDraw.Draw(sheet)
        for i, (label, image) in enumerate(batch):
            x, y = (i % 2) * 520, (i // 2) * 404
            pen.text((x + 4, y + 2), label, fill="white")
            sheet.paste(image.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 16))
        out = folder / f"lil_aftermath_{1 + start // 6}.png"
        sheet.save(out)
        sheets.append(dict(path=str(out), sha256=base.digest(out)))
    evidence.update({str(p): base.digest(p) for p in (play.FIXTURES, play.FIXTURE, offline.PROOF)})
    base.save(PROOF, dict(candidate_sha256=setup["candidate_sha256"], revised_pages_verified=len(holds),
        paths=[dict(speeches=speeches, checked_revisions=holds, exit_frame=exit_frame, sheets=sheets,
                    post_return=pictures[later][0], rendered_mismatches=[])],
        actual_FI_substitution=dict(record=no["id"], name="Lil", exact_visible_glyphs=True),
        each_stanza_advanced_once_by_A=True, natural_activation=False, hardware=False, evidence=evidence))
    print("Verified all eight revised Lil pages, one press per stanza, live Lil substitution and the original return.")


def startup():
    FunctionType(startup_template.startup.__code__, vars(startup_template) | globals())()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
