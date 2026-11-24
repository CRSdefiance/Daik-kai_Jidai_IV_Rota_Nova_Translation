"""Match the ordinary Lisbon choice and its independent reply to clean and installed text."""

import json
import re
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from dk4tool.formats.ilnk import IlnkContainer
from scripts import check_rafael_B84_training_gameplay_20261122 as menu
from scripts import observe_rafael_prepare_alone_20261123 as run
from scripts import register_rafael_proof_and_financing_20261122 as source
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_lisbon_seoul_trend_gameplay_20261121 import mask_check
from scripts.verify_moonlit_violin_20261121 import bytes_for


OUT = panels.OUT.with_name("rafael_prepare_alone_current_20261123.json")
STORY, BLOCK = "/data/SC0.DK4", 44
RESPONSE = "DK4_MES_B44_R0479"
ANCHORS = {424, 428, 431, 436, 439, 446, 449, 464, 469, 479}
NAMES = {b"FI": b"Rafael", b"FA": b"Castor", b"FO": b"Castor Co."}
CHOICE_FRAMES = (32225, 32395)
RESPONSE_FRAME = 32615
RETURN_FRAME = 32900


def get_capture(release):
    report = read(run.REPORT)
    journal_path = run.REPORT.with_name("navigation_command_journal.json")
    journal = read(journal_path)
    assert report["ROM_sha256"] == journal["ROM_sha256"] == release["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report.get("battery_save_preloaded")
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    prefix_path = run.ROOT / "inputs.json"
    prefix = read(prefix_path)
    assert report["scripted_input_schedule"][:len(prefix)] == prefix
    commands = [json.loads(line) for line in run.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [r["command"] for r in journal["commands_received"]]
    assert commands[-1] == {"stop": True} and all(row["validation_passed"] for row in journal["commands_received"])
    assert [r["buttons"] for r in commands[:3]] == [["DOWN"], ["A"], ["A"]]
    assert journal["last_command_frame"] == report["frames"] == RETURN_FRAME
    return report, [reference(p) for p in (run.REPORT, journal_path, prefix_path, run.CONTROLLER, run.SOURCE)]


def choices(bank, original, reviewed, font, pictures, shots):
    retained = reviewed["retained_native_controls"]["original_choice"]
    captions = retained["captions"]
    assert [row["slot"] for row in captions] == [0, 1] and all(all(row["review"].values()) for row in captions)
    text = [row["english"] for row in captions]
    assert text == ["Ask him.", "Prepare alone."]
    stored = bytes.fromhex(retained["exact_retained_object_hex"])
    at = retained["stored_offset"]
    assert bank[at:at + len(stored)] == stored and [name.decode("ascii") for name in labels(stored)] == text
    for row in captions:
        ref = row["source_reference"]
        clean = bytes.fromhex(ref["exact_command_hex"])
        start = ref["command_offset"]
        assert original[start:start + len(clean)] == clean
        assert labels(clean)[row["slot"]].decode("cp932") == row["Japanese"]
    visible = [menu.captions(font, pictures[n], text) for n in CHOICE_FRAMES]
    palettes = [[r["background"] for r in rows] for rows in visible]
    assert palettes[1][1] == menu.MENU_HIGHLIGHT
    assert palettes[0][1] == palettes[1][0] != menu.MENU_HIGHLIGHT
    return dict(selected_slot=1, selected_caption=text[1], original_menu_offset=at, exact_installed_command=stored.hex(),
        source_and_installed_captions=captions, observed=[dict(capture=shots[n], captions=p) for n, p in zip(CHOICE_FRAMES, visible, strict=True)])


def story(clean, current, release, pictures, shots):
    assert digest(source.REVIEW) == read(source.PACKAGE / "checksums.json")["verification/registered_review.json"]
    reviewed = read(source.REVIEW)
    arm = current.read_file(run.active.ARM)
    name_font = GameAsciiFont.from_arm9(arm)
    font = current.read_file("/GRP/KANJI.FNT")
    before, after = (IlnkContainer.parse(image.read_file(STORY)).blocks[BLOCK] for image in (clean, current))
    paint = panels.town.clipped_renderer(SimpleNamespace(image=current, arm=arm))
    decisions = []
    for row in reviewed["records"]:
        if row["block"] != BLOCK or int(row["id"].rsplit("_R", 1)[1]) not in ANCHORS:
            continue
        src, ref = row["source_reference"], row["registered_reference"]
        a, b = (bytes.fromhex(x["exact_command_hex"]) for x in (src, ref))
        assert before[src["command_offset"]:src["command_offset"] + len(a)] == a
        assert after[ref["command_offset"]:ref["command_offset"] + len(b)] == b
        assert a[:6] == b[:6] and row["review"] == dict.fromkeys(GATES, True)
        text = re.sub(rb"\b(FI|FA|FO)\b", lambda token: NAMES[token[0]], bytes_for(b))
        display = paint(arm, font, text)
        page, = display["pages"]
        assert display["complete_consumed_bytes"] == len(text) and page["native_independent_plane_equal"]
        plane = bytes.fromhex(page["native_plane_hex"])
        matched = next((frame for frame in sorted(pictures) if mask_check(plane, 216, pictures[frame])), None)
        decisions.append(dict(id=row["id"], block=BLOCK, file_path=STORY, english=row["english"],
            Japanese=row["Japanese"], speaker=row["speaker"],
            source_meaning=row["source_meaning"], context=row["context"], localization_note=row["localization_note"],
            historical_decision=row["decision"], source_reference=src, current_reference=ref | dict(
                candidate_sha256=release["candidate_sha256"], block_sha256=sha256(after).hexdigest(),
                archive_sha256=release["target_SC0_sha256"]), captured=shots.get(matched),
            complete_nameplate=panels.nameplate(name_font, row["speaker"], pictures[matched]) if matched else None,
            complete_native_page_sha256=sha256(plane).hexdigest(), review=row["review"]))
    assert len(decisions) == len(ANCHORS)
    found = [row for row in decisions if row["captured"]]
    missed = [row["id"] for row in decisions if not row["captured"]]
    by_id = {r["id"]: r for r in found}
    assert by_id[RESPONSE]["captured"]["frame"] == RESPONSE_FRAME
    assert "DK4_MES_B44_R0464" in missed and "DK4_MES_B44_R0469" in missed
    assert by_id["DK4_MES_B44_R0449"]["captured"]["frame"] < CHOICE_FRAMES[0]
    selection = choices(after, before, reviewed, name_font, pictures, shots)
    town = panels.find_mask(name_font, "Lisbon", pictures[RETURN_FRAME], (67, 16, 108, 32))
    return decisions, found, missed, selection, town


def main():
    release = read(run.active.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    report, evidence = get_capture(release)
    shots = {r["frame"]: r for r in report["frames_captured"] if r["frame"] >= min(run.PREFIX_HOLDS)}
    pictures = {n: panels.picture(row) for n, row in shots.items()}
    clean, installed = map(NdsImage.open, (CLEAN, release["candidate"]))
    decisions, found, missed, selection, town = story(clean, installed, release, pictures, shots)
    visuals = [(f"{r['captured']['frame']} / {r['speaker']}", pictures[r["captured"]["frame"]]) for r in found]
    visuals += [(f"Choice / {n}", pictures[n]) for n in CHOICE_FRAMES]
    sheets = FunctionType(panels.sheets_for.__code__, vars(panels) | {"OUT": OUT})
    rendered = sheets("rafael_prepare_alone", visuals, (0, 272, 256, 380))
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_new_game=True,
        installed_source_ledger=reference(source.REVIEW), context_records=decisions, observations=found,
        unvisited_speeches=missed, selection=selection,
        return_to_Lisbon=dict(capture=shots[RETURN_FRAME], heading_glyphs=town), evidence=evidence,
        sheets=rendered, full_route_complete=False, new_editorial_credit=0))
    print(f"Verified {len(found)} story holds, both complete captions and Julio's independent reply from New Game.")


if __name__ == "__main__":
    main()
