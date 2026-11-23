"""Verify Hodram's tactics page, modal, live surname, and the two opaque cries."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import audit_ceuta_lesson_20261119 as original
from scripts import audit_rafael_sailing_modes_playback_20261119 as display
from scripts import replay_hodram_early_confrontations_20261119 as play
from scripts import verify_hodram_early_confrontations_20261119 as offline

base, build = play.base, play.build
PROOF = play.ROOT / "verified_excerpts.json"
STARTUP = build.ROOT / "own_startup_verification.json"
OLD = Path("work/Hodram_B0_B41_clean_20261107")
NAMES = OLD / "actual_name_inputs_v1/proposed_planes.json"
PRIOR_LAYOUT = OLD / "storage_inputs_v2/native_pages.json"
FORM = "DK4_MES_B29_R0074"
SURNAME = "DK4_MES_B33_R0005"


def shout_frame(page, name, before, after, pictures):
    plane = bytes.fromhex(page["native_plane_hex"])
    assert len(plane) == 216 * 64 and set(plane) <= {0, 1, 15}
    ink = bytes(v == 1 for v in plane)
    shadow = bytes(v == 15 for v in plane)
    path = Path(name["native_plane"])
    assert base.digest(path) == name["native_plane_sha256"]
    header = {(i % 216, i // 216) for i, v in enumerate(path.read_bytes()) if v}
    for frame, (capture, image) in pictures.items():
        if not before + 25 < frame < after - 4:
            continue
        crop = image.crop((16, 296, 232, 360)).get_flattened_data()
        if bytes(rgb == display.DARK for rgb in crop) != ink:
            continue
        assert bytes(rgb == (197, 198, 197) for rgb in crop) == shadow
        found = {(x - 16, y - 276) for y in range(276, 289)
                 for x in range(14, 18 + name["original_pair_flush_width"])
                 if image.getpixel((x, y)) == display.STEEL}
        assert found == header
        return capture
    raise AssertionError((before, after, name["text"]))


def gameplay():
    assert not PROOF.exists()
    folder = play.ROOT / "route1_English"
    terminal_path = folder / "terminal.json"
    terminal = base.load(terminal_path)
    assert terminal["terminal"] and terminal["frames"] == play.FRAMES and terminal["all_callbacks_readonly_andhost_slots_restored"]
    evidence = {str(terminal_path): base.digest(terminal_path)}
    for key in ("report", "observer", "run_plan"):
        path = terminal[key]
        assert base.digest(path) == terminal[key + "_sha256"]
        evidence[path] = terminal[key + "_sha256"]
    report, trace, plan = (base.load(terminal[key]) for key in ("report", "observer", "run_plan"))
    setup, painter, name_proof, earlier = map(base.load, (play.FIXTURES, offline.PROOF, NAMES, PRIOR_LAYOUT))
    fixture, = setup["fixtures"]
    assert base.digest(play.FIXTURE) == fixture["research_ROM_sha256"] == report["ROM_sha256"]
    assert setup["exact_candidate_inverse"] and base.digest(build.ROM) == setup["candidate_sha256"] == painter["candidate_sha256"]
    assert plan["entry_opening_block"] == play.ENTRY and plan["route"] == 1
    assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
    assert report["scripted_input_schedule"] == base.load(plan["inputs"]) and base.digest(plan["inputs"]) == plan["inputs_sha256"]
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]
    prior, = (r for r in earlier["records"] if r["id"] == FORM)
    assert len(prior["complete_native_English_display"]["pages"]) == 2
    prior_bytes = next(r["current_hex"] for r in base.load(build.review.OUTPUT)["records"] if r["id"] == FORM)
    assert bytes.fromhex(prior_bytes).rstrip(b" ") == bytes.fromhex(prior["compiled_hex"]).rstrip(b" ")
    assert base.digest(name_proof["name_decisions"]) == name_proof["name_decisions_sha256"]
    name_planes = {r["text"]: r for r in name_proof["planes"]}
    names = {}
    for row in base.load(name_proof["name_decisions"])["records"]:
        name = name_planes[row["english"]]
        if "native_events" in name:
            names[row["actor_ID"]] = name | {"original_pair_flush_width": 6 + max(e["x"] for e in name["native_events"])}
    pictures = display.captures(report)
    bank = {r["offset"]: r for r in fixture["all_fixture_commands"]}
    words = {r["offset"]: r for r in fixture["original_text_records"]}
    changed = {r["id"]: (r["hodram_surname_pages"] if r["id"] == SURNAME else r["pages"])[0] for r in painter["revisions"]}
    shouts = painter["opaque_retention_display"]
    speeches, holds, opaque, frames, offsets = [], [], [], [], []
    exit_frame, tactics_advances = None, None
    for returned in trace["rows"]:
        source = returned["source"]
        if returned["kind"] != "after_command" or (
            source.get("classification"), source.get("route"), source.get("block")
        ) != ("original_SC_cache", 1, play.ENTRY):
            continue
        entered = trace["rows"][returned["entry_row"]]
        assert source["whole_resident_payload_exact_ROM"]
        assert source["actual_sha256"] == source["registered_sha256"] == fixture["fixture_block_sha256"]
        assert returned["CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback"]
        at, word = source["instruction_offset"], source["first_word"]
        assert word == bank[at]["word"] == entered["source"]["first_word"]
        assert not offsets or at == offsets[-1][0] + offsets[-1][1]
        offsets.append((at, returned["decoded_length"]))
        if word == 0:
            assert returned["result_words"][0] == 0
            exit_frame = returned["frame"]
            break
        if at not in words:
            continue
        row = words[at]
        ident, selector = row["id"], row["source_selector"]
        speeches.append(ident)
        if ident not in changed and ident not in shouts:
            continue
        start, end = entered["frame"], returned["frame"]
        if ident in shouts:
            frame = shout_frame(shouts[ident]["page"], names[selector], start, end, pictures)
        else:
            frame = display.matching_frame(changed[ident], selector, start, end, pictures, names)
        receipt = dict(id=ident, frame=frame["frame"], capture=frame["path"], capture_sha256=frame["PNG_sha256"],
            complete_body_and_name_mask=True, speaker=selector)
        (opaque if ident in shouts else holds).append(receipt)
        frames.append((ident, pictures[frame["frame"]][1]))
        if ident == FORM:
            tactics_advances = [r["start"] for r in report["scripted_input_schedule"]
                                if r["buttons"] == ["A"] and frame["frame"] < r["start"] <= end]
    assert exit_frame is not None and speeches == [r["id"] for r in fixture["original_text_records"]]
    assert len(holds) == 10 and {r["id"] for r in opaque} == offline.OPAQUE
    assert len(tactics_advances) == 1
    later = min(n for n in pictures if n > exit_frame + 50)
    frames.append(("After the original opening exit", pictures[later][1]))
    sheets = []
    for start in range(0, len(frames), 6):
        batch = frames[start:start + 6]
        sheet = Image.new("RGB", (1040, ((len(batch) + 1) // 2) * 404), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (label, image) in enumerate(batch):
            x, y = (i % 2) * 520, (i // 2) * 404
            draw.text((x + 4, y + 2), label, fill="white")
            sheet.paste(image.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 16))
        path = folder / f"hodram_playback_{1 + start // 6}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    evidence.update({str(p): base.digest(p) for p in (play.FIXTURES, play.FIXTURE, offline.PROOF, NAMES, PRIOR_LAYOUT)})
    for actor in {r["speaker"] for r in holds + opaque if r["speaker"] != 254}:
        p = names[actor]["native_plane"]
        evidence[p] = names[actor]["native_plane_sha256"]
    base.save(PROOF, dict(candidate_sha256=setup["candidate_sha256"], revised_pages_verified=len(holds),
        paths=[dict(speeches=speeches, checked_revisions=holds, opaque_retained_shouts=opaque,
                    exit_frame=exit_frame, sheets=sheets, post_return=pictures[later][0])],
        tactics_transition=dict(previous_pages=2, revised_pages=1, one_A_after_complete_panel=tactics_advances[0]),
        natural_activation=False, hardware=False, evidence=evidence))
    print("Verified 10 revised Hodram pages, both opaque cries, live surname, one-page tactics and the original return.")


def startup():
    scope = vars(original) | {"play": play, "build": build, "STARTUP": STARTUP, "__file__": __file__}
    FunctionType(original.startup.__code__, scope)()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
