"""Bind the Nagasaki Inn dream to its complete clean and current exchange."""

import json
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_nagasaki_dream_20261123 as run
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_lisbon_seoul_trend_gameplay_20261121 import mask_check
from scripts.verify_moonlit_violin_20261121 import bytes_for


OUT = panels.OUT.with_name("nagasaki_dream_current_20261123.json")
PRIOR = Path("translations/maria390_B152_B175_integrated_final_review_v1.json")
STORY, BLOCK = "/data/SC3.DK4", 171
FRAMES = dict(zip((9, 13, 17, 21, 25, 29, 33, 37, 41, 48, 52, 71, 75, 79, 83), range(8440, 11241, 200), strict=True))
PROPOSALS = {
    29: ("...You're a namahage!", ("a namahage",),
         "A contraction makes the startled recognition sound spoken. Keep the pause and the source cultural name."),
    52: ("A dream?", (),
         "The brief self-question sounds natural as Yukihisa wakes and wonders what he experienced."),
    83: ("I'll give this to the admiral tomorrow morning.", ("to the admiral", "tomorrow morning"),
         "Restore the specific next morning in Yukihisa's quiet planning. His spoken reference to the object remains unnamed."),
    94: ("...So what is it?!", (),
         "Angelo returns to his unanswered question about the object after Yukihisa's aside. Keep the interruption and the frustrated emphasis."),
}


def checked_capture(release):
    paths = [run.ROOT / path for path in ("capture/capture_report.json", "capture/navigation_command_journal.json",
            "trace/requests.json", "terminal.json")]
    capture, journal, trace, terminal = map(read, paths)
    assert release["candidate_sha256"] == capture["ROM_sha256"] == terminal["candidate_sha256"] == journal["ROM_sha256"]
    assert terminal["ordinary_controller_inputs"] and capture["cold_boot"] and not capture["savestate_loaded"]
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    commands = [json.loads(line) for line in run.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [r["command"] for r in journal["commands_received"]] and commands[-1] == {"stop": True}
    assert all(r["validation_passed"] for r in journal["commands_received"])
    assert capture["frames"] == terminal["total_frames"] == journal["last_command_frame"] == 12640
    assert all(digest(path) == h for path, h in terminal["evidence"].items())
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and donor["source_sha256"] == terminal["copied_save_sha256"]
    assert digest(donor["source"]) == donor["source_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_requests"] == terminal["common_requests"]
    return panels.shots(capture, "_navigation.png"), trace["source_requests"], dict(
        files=[reference(path) for path in paths], save=reference(donor["source"]),
        save_provenance=reference("docs/nagasaki_shiraki_v518_checkpoint.md"))


def command(block, reference_row, body_with_selector, offset_key):
    at = reference_row[offset_key]
    raw = bytes.fromhex(body_with_selector)
    expected = b"\x00\x40\xff\xff\x00" + raw
    assert block[at:at + len(expected)] == expected and block[at + len(expected)] == 0
    end = at + len(expected)
    if end % 2 == 0:
        assert block[end:end+2] == b"\0\0"
        end += 2
    else:
        end += 1
    return block[at:end], dict(command_offset=at, block_sha256=sha256(block).hexdigest(),
                                exact_command_hex=block[at:end].hex())


def story(clean, rom, frames, release):
    jp, en = (image.read_file(STORY) for image in (clean, rom))
    source, current = (IlnkContainer.parse(content).blocks[BLOCK] for content in (jp, en))
    arm = rom.read_file(run.current.ARM)
    font = GameAsciiFont.from_arm9(arm)
    kanji = rom.read_file("/GRP/KANJI.FNT")
    ctx = SimpleNamespace(image=rom, arm=arm)
    paint, fe = panels.town.clipped_renderer(ctx), panels.town.current_fe_painter(ctx)
    inherited = [row for row in read(PRIOR)["records"] if row["block"] == BLOCK]
    assert len(inherited) == 17
    output, images, previews = [], [], []
    for row in inherited:
        key = int(row["id"].rsplit("_R", 1)[1])
        a, src = command(source, row["source_reference"], row["source_hex"], "command_offset")
        installed, = row["registered_native_pages"]
        b, ref = command(current, installed, installed["exact_stored_hex"], "header_offset")
        assert a[:6] == b[:6] and all(row["review"].values())
        text = bytes_for(b)
        assert text.isascii() and " ".join(text.decode("ascii").split()) == row["english"]
        frame, held = FRAMES.get(key), None
        if frame is not None:
            screen = panels.picture(frames[frame])
            if b[5] == 254:
                display = fe(text)
                plane, width = display["physical"], 228
                nameplate = None
            else:
                display = paint(arm, kanji, text)
                page, = display["pages"]
                assert page["native_independent_plane_equal"]
                plane, width = bytes.fromhex(page["native_plane_hex"]), 216
                nameplate = panels.nameplate(font, row["speaker"], screen)
            assert display["complete_consumed_bytes"] == len(text) and mask_check(plane, width, screen), (key, frame)
            held = dict(capture=frames[frame], native_plane_sha256=sha256(plane).hexdigest(), complete_nameplate=nameplate)
            images.append((row["id"], screen))
        note, draft, candidate = row["localization_note"], None, None
        if key in PROPOSALS:
            draft, phrases, note = PROPOSALS[key]
            body, plan = panels.layout.plan_progressive(dict(id=row["id"], english=draft, protected_phrases=phrases),
                b[5], text, bytes_for(a))
            page, = panels.story_display.display.raster(ctx, kanji, paint, body, plan["lines"], 1)
            assert page["native_independent_plane_equal"]
            raw_plane = bytes.fromhex(page["native_plane_hex"])
            previews.append((row["id"], raw_plane))
            candidate = dict(formatter_plan=plan, native_plane_sha256=sha256(raw_plane).hexdigest(),
                physical_source_and_installed_selectors=b[5], fits_current_text_bytes=len(body) <= len(text),
                available_content_bytes=len(text), proposed_content_bytes=len(body),
                stored_and_gameplay_checks_pending=True)
        output.append(dict(id=row["id"], block=BLOCK, context=row["context"], speaker=row["speaker"],
            clean_Japanese=row["source_Japanese"], source_gloss=row["source_meaning"], source_reference=src,
            installed_reference=ref | dict(candidate_sha256=release["candidate_sha256"], archive_sha256=sha256(en).hexdigest()),
            installed_English=text.decode("ascii"), gameplay_observed=frame is not None, display=held,
            decision="revision proposed" if draft else "retention", rationale=note, proposed_English=draft,
            offline_preflight=candidate, review=row["review"] | ({"formatting": False} if draft else {})))

    sheets = panels.sheets_for("nagasaki_dream_ordinary", images)
    folder = OUT.parent / "nagasaki_dream_proposals_20261123"
    folder.mkdir(exist_ok=True)
    contact = panels.story_display.display.inherited.early.contact_sheets
    pages = FunctionType(contact.__code__, contact.__globals__ | {"ROOT": folder})(previews)
    return output, sheets, pages


def main():
    release = read(run.current.RELEASE)
    assert digest(run.current.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    frames, requests, evidence = checked_capture(release)
    clean, rom = map(NdsImage.open, (CLEAN, release["candidate"]))
    rows, sheets, previews = story(clean, rom, frames, release)
    arm = rom.read_file(run.current.ARM)
    font = GameAsciiFont.from_arm9(arm)
    source = common_message_entries(clean.read_file(run.current.COMMON), clean.read_file(run.current.ARM))
    installed = common_rows(rom.read_file(run.current.COMMON), arm)
    award_frame = frames[11440]
    key, = {r["message_ID"] for r in requests if 11240 < r["frame"] <= 11440}
    award = "You got Namahage Cleaver!"
    assert installed[key].text.decode("ascii").strip() % "Namahage Cleaver" == award
    award_details = dict(message_ID=key, clean_Japanese=source[key].text.decode("cp932"),
        source_reference=panels.text_reference(source[key]), installed_reference=panels.text_reference(installed[key]),
        complete_glyphs=panels.exact_body(font, (award,), panels.picture(award_frame)), frame=award_frame,
        decision="retention", rationale="The immediate item-award notice names the reward after the scene, while the spoken reference remains unspecified.",
        review=dict.fromkeys(GATES, True))
    final = panels.picture(frames[12640])
    panels.find_mask(font, "Nagasaki", final, (44, 11, 117, 39))
    end_sheets = panels.sheets_for("nagasaki_dream_award_and_inn",
        [(f"{frame} {label}", panels.picture(frames[frame])) for frame, label in (
        (11440, "reward"), (11640, "Inn returns"), (12040, "price"), (12240, "rest"), (12640, "town"))])
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_controller_gameplay=True,
        changed_ROM=False, exact_story_reference=reference(PRIOR), story=rows, award=award_details,
        returned_to_Inn_and_Nagasaki=frames[12640], observed_story_holds=15,
        unvisited_story_variants=["Both Angelo panels in this exchange"],
        gameplay_sheets=sheets + end_sheets, offline_proposed_pages=previews,
        evidence=evidence, actual_COMMON_requests=requests, new_editorial_credit=0))
    print("Bound the 17-turn dream and verified 15 naturally reached story panels, the cleaver and the Inn return.")


if __name__ == "__main__":
    main()
