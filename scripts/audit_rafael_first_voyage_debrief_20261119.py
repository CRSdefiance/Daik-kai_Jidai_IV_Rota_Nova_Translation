"""Audit the ordinary opening pages, original menu, and return into the tutorial."""

from argparse import ArgumentParser
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from scripts import audit_ceuta_lesson_20261119 as startup_template
from scripts import audit_rafael_sailing_modes_playback_20261119 as display
from scripts import replay_rafael_first_voyage_debrief_20261119 as play
from scripts import verify_rafael_first_voyage_debrief_20261119 as offline
from scripts.verify_all_items_gallery_v535 import glyph_pixels

base, build = play.base, play.build
PROOF = play.ROOT / "verified_departure.json"
STARTUP = build.ROOT / "own_startup_verification.json"
REQUIRED = {17, 152, 268, 308, 316, 327, 397, 464, 469}


def frames_in(pictures, before, after):
    return [(n, shot, image) for n, (shot, image) in sorted(pictures.items())
            if before + 25 < n < after - 4]


def gameplay():
    assert not PROOF.exists()
    folder = play.ROOT / "route0_English"
    terminal_path = folder / "terminal.json"
    terminal = base.load(terminal_path)
    assert terminal["terminal"] and terminal["frames"] == play.FRAMES
    assert terminal["all_callbacks_readonly_andhost_slots_restored"]
    evidence = {str(terminal_path): base.digest(terminal_path)}
    for key in ("report", "observer", "run_plan"):
        path = terminal[key]
        assert base.digest(path) == terminal[key + "_sha256"]
        evidence[path] = terminal[key + "_sha256"]
    report, trace, plan = (base.load(terminal[k]) for k in ("report", "observer", "run_plan"))
    stage, painter = map(base.load, (build.PROOF, offline.PROOF))
    assert report["ROM_sha256"] == stage["candidate_sha256"] == painter["candidate_sha256"] == base.digest(build.ROM)
    assert plan["original_natural_New_Game_entry"] and plan["entry_opening_block"] == 44
    assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(plan["inputs"]) and base.digest(plan["inputs"]) == plan["inputs_sha256"]
    assert not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]
    group, = (g for g in stage["groups"] if g["block"] == 44)
    resident = {r["stored_offset"]: r for r in group["commands"]}
    revised = {r["id"]: r["pages"][0] for r in painter["revisions"] if r["id"].startswith("DK4_MES_B44_")}
    pictures = display.captures(report)
    font = GameAsciiFont.from_arm9(base.NdsImage.open(build.ROM).read_file(build.native.ARM))
    names = {0: "Rafael Castor", 4: "Janus Pasar", 5: "Claudio Manaus", 6: "Julio Erneco"}
    name_ink = {actor: glyph_pixels(font, b"", (), name, 16, 277, 6) for actor, name in names.items()}
    speeches, holds, samples, skipped = [], [], [], []
    choice = None
    exit_frame = None
    for returned in trace["rows"]:
        source = returned["source"]
        if returned["kind"] != "after_command" or (
            source.get("classification"), source.get("route"), source.get("block")
        ) != ("original_SC_cache", 0, 44):
            continue
        entered = trace["rows"][returned["entry_row"]]
        assert source["whole_resident_payload_exact_ROM"] and source["actual_sha256"] == source["registered_sha256"] == group["after"]
        assert returned["CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback"]
        at, word = source["instruction_offset"], source["first_word"]
        command = resident[at]
        assert command["word"] == word == entered["source"]["first_word"]
        if word == 0:
            assert returned["result_words"][0] == 0
            exit_frame = returned["frame"]
            break
        if word == 0x2100:
            text = [r.decode("ascii") for r in labels(bytes.fromhex(command["stored"]))]
            assert text == ["Ask him.", "Prepare alone."]
            assert command["stored"] == command["current"]
            assert returned["result_words"] == [2, 0]
            n, shot, image = frames_in(pictures, entered["frame"], returned["frame"])[-1]
            choice = dict(labels=text, selected=0, capture=shot)
            samples.append(("Guided preparation choice", image))
        if word != 0x4000:
            continue
        ident, = command["record_ids"]
        speeches.append(ident)
        if ident not in revised:
            continue
        actor = bytes.fromhex(command["stored"])[5]
        plane = bytes.fromhex(revised[ident]["native_plane_hex"])
        assert len(plane) == 216 * 64 and set(plane) == {0, 1}
        expected = b"".join(plane[i:i + 216] + bytes(12) for i in range(0, len(plane), 216))
        for n, shot, image in frames_in(pictures, entered["frame"], returned["frame"]):
            actual = bytes(c == (0, 8, 0) for c in image.crop((16, 296, 244, 360)).get_flattened_data())
            if actual != expected:
                continue
            width = len(names[actor]) * 6
            actual_name = {(x, y) for y in range(276, 289) for x in range(14, 18 + width)
                           if image.getpixel((x, y)) == (98, 97, 98)}
            assert actual_name == name_ink[actor], (ident, n, actor)
            holds.append(dict(id=ident, frame=n, capture=shot["path"], capture_sha256=shot["PNG_sha256"],
                              complete_body_and_name_mask=True, name=names[actor]))
            if int(ident.rsplit("_R", 1)[1]) in REQUIRED:
                samples.append((ident, image))
            break
        else:
            skipped.append(ident)
    assert exit_frame is not None and choice is not None and len(speeches) == len(set(speeches))
    assert {f"DK4_MES_B44_R{n:04}" for n in REQUIRED} <= {r["id"] for r in holds}, skipped
    after = min(n for n in pictures if n > exit_frame + 55)
    samples.append(("After the normal tutorial return", pictures[after][1]))
    sheets = []
    for start in range(0, len(samples), 6):
        batch = samples[start:start + 6]
        sheet = Image.new("RGB", (1040, ((len(batch) + 1) // 2) * 404), "#263238")
        pen = ImageDraw.Draw(sheet)
        for i, (label, image) in enumerate(batch):
            x, y = (i % 2) * 520, (i // 2) * 404
            pen.text((x + 4, y + 2), label, fill="white")
            sheet.paste(image.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 16))
        path = folder / f"rafael_departure_{1 + start // 6}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    evidence.update({str(p): base.digest(p) for p in (play.SETUP, offline.PROOF, build.PROOF)})
    base.save(PROOF, dict(candidate_sha256=stage["candidate_sha256"], revised_pages_verified=len(holds),
        paths=[dict(speeches=speeches, checked_revisions=holds, exit_frame=exit_frame, sheets=sheets,
                    post_return=pictures[after][0], revised_pages_without_complete_hold=skipped)],
        actual_stock_names=offline.STOCK, guided_choice=choice, natural_activation=True,
        hardware=False, evidence=evidence))
    print(f"Ordinary Rafael opening reached {len(speeches)} turns and verified {len(holds)} revised pages.")


def startup():
    FunctionType(startup_template.startup.__code__, vars(startup_template) | globals())()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
