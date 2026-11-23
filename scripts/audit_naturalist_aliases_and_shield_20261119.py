"""Check the revised Athens pages and their original speech-to-modal transition."""

from argparse import ArgumentParser
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import audit_Rafael_B48_actual_v8053 as historical
from scripts import audit_ceuta_lesson_20261119 as original
from scripts import audit_rafael_sailing_modes_playback_20261119 as display
from scripts import replay_naturalist_aliases_and_shield_20261119 as play
from scripts import verify_naturalist_aliases_and_shield_20261119 as offline

base, build = play.base, play.build
PROOF = play.ROOT / "verified_athens.json"
STARTUP = build.ROOT / "own_startup_verification.json"


def gameplay():
    assert not PROOF.exists()
    folder = play.ROOT / "route0_English"
    terminal_path = folder / "terminal.json"
    terminal = base.load(terminal_path)
    assert terminal["terminal"] and terminal["frames"] == 40001 and terminal["all_callbacks_readonly_andhost_slots_restored"]
    evidence = {str(terminal_path): base.digest(terminal_path)}
    for key in ("report", "observer", "run_plan"):
        path = terminal[key]
        assert base.digest(path) == terminal[key + "_sha256"]
        evidence[path] = terminal[key + "_sha256"]
    report, trace, plan = (base.load(terminal[key]) for key in ("report", "observer", "run_plan"))
    setup, painter, name_proof = map(base.load, (play.FIXTURES, offline.PROOF, historical.FONT))
    fixture, = setup["fixtures"]
    assert base.digest(play.FIXTURE) == fixture["research_ROM_sha256"] == report["ROM_sha256"]
    assert setup["exact_candidate_inverse"] and base.digest(build.ROM) == setup["candidate_sha256"] == painter["candidate_sha256"]
    assert plan["displayed_original_block"] == 48 and plan["entry_opening_block"] == 44
    assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(plan["inputs"]) and base.digest(plan["inputs"]) == plan["inputs_sha256"]
    assert not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]
    pictures = display.captures(report)
    names = {r["actor_ID"]: r for r in name_proof["name_planes"]}
    resident = {r["offset"]: r for r in fixture["all_fixture_commands"]}
    words = {r["fixture_command_offset"]: r for r in fixture["original_text_records"]}
    revised = {r["id"]: r["pages"][0] for r in painter["revisions"]
               if r["file_path"] == "/data/SC0.DK4" and r["id"].startswith("DK4_MES_B48_")}
    assert len(revised) in {16, 17}
    speeches, holds, omitted, frames, offsets = [], [], [], [], []
    exit_frame = None
    for returned in trace["rows"]:
        source = returned["source"]
        if returned["kind"] != "after_command" or (
            source.get("classification"), source.get("route"), source.get("block")
        ) != ("original_SC_cache", 0, 44):
            continue
        entered = trace["rows"][returned["entry_row"]]
        assert source["whole_resident_payload_exact_ROM"] and source["actual_sha256"] == source["registered_sha256"]
        assert returned["CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback"]
        at, word = source["instruction_offset"], source["first_word"]
        assert word == resident[at]["word"] == entered["source"]["first_word"]
        assert not offsets or at == offsets[-1][0] + offsets[-1][1]
        offsets.append((at, returned["decoded_length"]))
        if word == 0:
            assert returned["result_words"][0] == 0
            exit_frame = returned["frame"]
            break
        if at in words:
            record = words[at]
            ident, selector = record["id"], record["source_selector"]
            speeches.append(ident)
            if ident not in revised:
                continue
            try:
                frame = display.matching_frame(revised[ident], selector, entered["frame"], returned["frame"], pictures, names)
            except AssertionError as error:
                omitted.append(dict(id=ident, speaker=selector, initial_frame=entered["frame"],
                                    return_frame=returned["frame"], mismatch=str(error)))
                continue
            holds.append(dict(id=ident, frame=frame["frame"], capture=frame["path"], capture_sha256=frame["PNG_sha256"],
                complete_body_and_name_mask=True, speaker=selector, name=None if selector == 254 else names[selector]["text"]))
            frames.append((ident, pictures[frame["frame"]][1]))
    assert exit_frame is not None and len(speeches) == len(set(speeches))
    checked = {r["id"] for r in holds}
    required = {"DK4_MES_B48_R0167", "DK4_MES_B48_R0431", "DK4_MES_B48_R0438"}
    if not required <= checked:
        raise AssertionError((required - checked, omitted))
    assert not omitted or len(holds) >= 10
    later = min(n for n in pictures if n > exit_frame + 50)
    frames.append(("After the original scene return", pictures[later][1]))
    sheets = []
    for start in range(0, len(frames), 6):
        batch = frames[start:start + 6]
        sheet = Image.new("RGB", (1040, ((len(batch) + 1) // 2) * 404), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (label, image) in enumerate(batch):
            x, y = (i % 2) * 520, (i // 2) * 404
            draw.text((x + 4, y + 2), label, fill="white")
            sheet.paste(image.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x + 4, y + 16))
        path = folder / f"athens_playback_{1 + start // 6}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    evidence.update({str(p): base.digest(p) for p in (play.FIXTURES, play.FIXTURE, offline.PROOF, historical.FONT)})
    for actor in {r["speaker"] for r in holds if r["speaker"] != 254}:
        p = names[actor]["native_plane"]
        evidence[p] = names[actor]["native_plane_sha256"]
    base.save(PROOF, dict(candidate_sha256=setup["candidate_sha256"], revised_pages_verified=len(holds),
        paths=[dict(speeches=speeches, source_commands_visited=len(offsets) - 10, checked_revisions=holds,
                    exit_frame=exit_frame, rendered_mismatches=omitted, sheets=sheets, post_return=pictures[later][0])],
        natural_activation=False, hardware=False, evidence=evidence))
    print(f"Verified {len(holds)} revised Athens pages, both revised modal notices and the original return.")


def startup():
    scope = vars(original) | {"play": play, "build": build, "STARTUP": STARTUP, "__file__": __file__}
    FunctionType(original.startup.__code__, scope)()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("gameplay", "startup"))
    globals()[parser.parse_args().action]()
