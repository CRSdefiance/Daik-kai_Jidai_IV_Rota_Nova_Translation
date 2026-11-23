"""Verify the accepted Azores answer, complete panels, and development transition."""

import json
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.replay_azores_words_adaptive_20261123 import ANSWER, ANSWER_SOURCE, RELEASE, ROOT
from scripts.reconcile_editorial_acceptance_20261123 import ARM, OUT, digest, read, reference
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import REPORT as VOYAGE, body_mask, load_exact, text_at
from scripts.verify_village_visits_v664 import model


REPORT = OUT.with_name("ordinary_azores_promised_words_20261123.json")
SHEET = REPORT.with_suffix(".png")


def main():
    assert not REPORT.exists() and not SHEET.exists()
    capture = ROOT / "capture"
    receipt, terminal_path, progress_path = (capture / "capture_report.json", ROOT / "terminal.json",
                                             capture / "controller_progress.json")
    release, voyage, run, terminal, progress, manuscript = map(read, (
        RELEASE, VOYAGE, receipt, terminal_path, progress_path, ANSWER_SOURCE))
    assert digest(release["candidate"]) == release["candidate_sha256"] == voyage["candidate_sha256"]
    assert release["candidate_sha256"] == run["ROM_sha256"] == terminal["candidate_sha256"]
    assert terminal["ordinary_controller_inputs"] and run["cold_boot"] and not run["savestate_loaded"]
    assert not run["callback_errors"] and not any(value for key, value in run.items() if key.startswith("synthetic_"))
    assert terminal["copied_save_sha256"] == voyage["original_lisbon_save"]["sha256"]
    assert all(digest(path) == sha for path, sha in terminal["evidence"].items())
    assert not progress["error"] and [r["entry"] for r in progress["entered_character_states"]] == [
        ANSWER[:i] for i in range(len(ANSWER) + 1)]
    for typed in progress["entered_character_states"]:
        assert digest(typed["RAM"]) == typed["RAM_sha256"] and typed["complete108x11_input_foreground_and_blank_cells_exact"]
    assert progress["phases"]["menu_return"] == terminal["total_frames"] == run["frames"]
    calls = [r for r in terminal["common_requests"] if r["message_ID"] == 296]
    assert [r["PC"] for r in calls] == [0x0205528C, 0x020534F4]
    assert calls[0]["frame"] == calls[1]["frame"] < progress["phases"]["confirmation"]
    shots = {r["frame"]: r for r in run["frames_captured"] if r["path"].endswith("_navigation.png")}
    snapshots = {r["frame"]: r for r in run["read_only_pause_RAM_snapshots"]}
    clean, candidate = map(NdsImage.open, ("work/clean.nds", release["candidate"]))
    source, arm = clean.read_file(ARM), candidate.read_file(ARM)
    assert source[0x78AF4:0x78B24] == arm[0x78AF4:0x78B24]
    font = GameAsciiFont.from_arm9(arm)
    audit = {}
    sheet = Image.new("RGB", (556, 442), "#28313b")
    captions = ImageDraw.Draw(sheet)
    expected = {
        "confirmation": ("Is Terceira all right?",),
        "clue": ('They say it means "the island where', 'Angra do Heroismo is located".'),
        "facilities_notice": ("Starting with your next visit, you", "can use the trading post, tavern,", "and other facilities."),
        "menu_return": ("Set Sail",),
    }
    for i, (phase, lines) in enumerate(expected.items()):
        frame = progress["phases"][phase]
        shot, snapshot = shots[frame], snapshots[frame]
        assert digest(shot["path"]) == shot["PNG_sha256"]
        with Image.open(shot["path"]) as photo:
            screen = photo.convert("RGB")
        raw = load_exact(snapshot)
        stock = model(arm, raw, 13, "Azores", True)
        assert stock["native_development"] == (0 if phase == "confirmation" else 2)
        if phase == "menu_return":
            ink, bounds = complete_mask(font, "Set Sail", screen, 104, 283, (8, 8, 8))
            glyphs = [dict(text="Set Sail", ink_pixels=ink, bounds=bounds)]
            body_hex = None
        else:
            rendered = text_at(raw, unpack_from("<I", arm, 0x54450)[0])
            assert tuple(line.strip() for line in rendered.decode("ascii").split("\n")) == lines
            glyphs = body_mask(font, screen, lines)
            body_hex = rendered.hex()
        audit[phase] = dict(stock=stock, full_glyphs=glyphs, rendered_body_hex=body_hex, screenshot=shot, snapshot=snapshot)
        x, y = 8 + 272 * (i % 2), 218 * (i // 2)
        captions.text((x, y + 8), phase.replace("_", " "), fill="white")
        sheet.paste(screen.crop((0, 192, 256, 384)), (x, y + 24))
    answer, = [r for r in manuscript["records"] if r["kind"] == "ANSWER" and r["index"] == 13]
    clue, = [r for r in manuscript["records"] if r["kind"] == "CLUE" and r["index"] == 13]
    assert answer["english"] == ANSWER and all(answer["review"].values()) and all(clue["review"].values())
    assert clue["english"] in " ".join(expected["clue"])
    sheet.save(SHEET)
    result = dict(candidate_sha256=release["candidate_sha256"], correct_answer_supported=answer,
        correct_answer_clue=clue, exact_runtime_entry_and_each_prefix=progress["entered_character_states"],
        confirmation_common_calls=calls, observed_panels=audit,
        ordinary_approach_and_promised_words_accepted=True, next_visit_facilities_notice_observed=True,
        future_visit_and_hardware_unvisited=True, new_editorial_credit=0, sheet=reference(SHEET),
        evidence=[reference(path) for path in (RELEASE, VOYAGE, receipt, terminal_path, progress_path, ANSWER_SOURCE)])
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified all eight input letters, source-backed confirmation and clue, and native development 0 to 2.")


if __name__ == "__main__":
    main()
