"""Bind the ordinary Nagasaki Yard visit to clean text and current glyphs."""

import json
from itertools import product
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_nagasaki_shipyard_20261124 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.finish_refit_display_v712 import BOX, WHITE
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_crew_policy_matrix_v657 import find_complete
from scripts.verify_regional_ui_v616 import glyphs
from scripts.verify_shipyard_gameplay_v760 import BODY, independent_font


OUT = panels.OUT.with_name("nagasaki_shipyard_20261124.json")
END = 25320
REQUESTS = (786, 265, 785, 788, 789, 788, 790, 1266, 1287, 1285, 1284, 1284, 1266, 1264, 1265, 1264)
REFIT = {16920: 1287, 17320: 1285, 17720: 1284}
PROPOSALS = {
    1264: "Which ship do you want to rename?",
    1285: "Lateen sails excel upwind. Never mount a square sail behind one.",
    1287: "With a following wind, square sails work well. Never mount a lateen sail ahead of one.",
}
HOLDS = (
    (7320, 786, "Shipwright", ("1", "30"), "The two labels preserve the mast count and durability, including a ship with only one mast."),
    (7720, 265, "", (), "The short confirmation asks exactly what the next input will do."),
    (9320, 785, "Shipwright", (), "The shipwright asks which existing design to duplicate. The ensuing list contains both existing ships."),
    (11320, 788, "Shipwright", (), "The sale question opens the list of eligible ships with a direct, conversational question."),
    (12120, 789, "Shipwright", ("7500 gold coins",), "The tentative price sounds like a spoken offer. The amount and currency come from the existing localized argument."),
    (14520, 790, "Shipwright", (), "The direct answer says both ships are in good repair. It avoids promising any work."),
    (16120, 1266, "Shipwright", (), "The complete question makes clear the player is choosing the ship for equipment work."),
    (16920, 1287, "", (), "Keep the following-wind advantage and the restriction on a lateen sail ahead. Rephrase to keep the start of the instruction together."),
    (17320, 1285, "", (), "Keep the upwind advantage and the restriction on a square sail behind. Rephrase to keep the start of the instruction together."),
    (17720, 1284, "", (), "The short two-line explanation states exactly what the inspected cannon control changes."),
    (20120, 1264, "Shipwright", (), "The question wraps before ‘to rename?’ A direct question in the same voice as the sale prompt keeps the action together."),
    (20920, 1265, "Shipwright", (), "The next line invites Maria to choose any name. It belongs after ship selection and before the keyboard."),
)
NATIVE_DIGITS = str.maketrans("0123456789", "０１２３４５６７８９")


def inferred_args(arm, kanji, row, samples, screen):
    """Find the unique ASCII/full-width combination from the complete body mask."""
    observed = {(x, y) for x in range(BODY[0], BODY[2]) for y in range(BODY[1], BODY[3]) if screen.getpixel((x, y)) == (0, 8, 0)}
    matches = []
    for values in product(*(tuple(dict.fromkeys((s, s.translate(NATIVE_DIGITS)))) for s in samples)):
        args = tuple(s.encode("cp932") for s in values)
        line = (row.text % args).strip().decode("cp932")
        plane = independent_font(arm, kanji, (line,))
        wide = set()
        column = 6
        for glyph in line:
            width = 6 * len(glyph.encode("cp932"))
            if width == 12:
                wide.update(range(column, column + width))
            column += width
        expected = {(16 + i % 228, 296 + i // 228 + (i % 228 not in wide)) for i, value in enumerate(plane) if value == 1}
        if expected == observed:
            matches.append((line, values, [a.hex() for a in args], len(expected)))
    result, = matches
    return result


def exact_refit(font, text, screen):
    left, top, right, bottom = BOX
    lines = text.decode("ascii").splitlines()
    assert 1 <= len(lines) <= 5 and all(len(line) <= 28 for line in lines)
    expected = {(left + x, top + 12 * i + y) for i, line in enumerate(lines) for x, y in glyphs(font, line)}
    observed = {(x, y) for x in range(left, right) for y in range(top, bottom) if screen.getpixel((x, y)) == WHITE}
    shifted = {(x, y + 1) for x, y in expected}
    assert observed in (expected, shifted), (lines, len(observed), len(expected), sorted(observed ^ shifted)[:12])
    return lines, len(observed)


def main():
    active = play.current
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    paths = [play.ROOT / name for name in ("capture/capture_report.json", "trace/requests.json", "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, paths)
    assert capture["ROM_sha256"] == terminal["candidate_sha256"] == journal["ROM_sha256"] == release["candidate_sha256"]
    assert terminal["ordinary_controller_inputs"] and capture["cold_boot"] and not capture["savestate_loaded"]
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    commands = [json.loads(line) for line in play.CONTROLLER.read_text("utf-8").splitlines()]
    assert commands == [r["command"] for r in journal["commands_received"]] and all(r["validation_passed"] for r in journal["commands_received"])
    assert capture["frames"] == terminal["total_frames"] == journal["last_command_frame"] == END
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == terminal["common_requests"] and tuple(r["message_ID"] for r in calls if r["PC"] == 0x0205528C) == REQUESTS
    frames = panels.shots(capture, "_navigation.png")
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    earlier = panels.shots(read(play.HISTORY), "_cold_boot.png")
    assert frames[3720]["framebuffer_sha256"] == earlier[3720]["framebuffer_sha256"]
    assert all(frames[a]["framebuffer_sha256"] == frames[b]["framebuffer_sha256"] for a, b in ((11320, 12520), (16120, 18520), (20120, 21720)))

    clean, image = map(NdsImage.open, (CLEAN, active.ROM))
    original_arm, arm = [rom.read_file(active.ARM) for rom in (clean, image)]
    font = GameAsciiFont.from_arm9(arm)
    kanji = image.read_file("/GRP/KANJI.FNT")
    source = common_message_entries(clean.read_file(active.COMMON), original_arm)
    installed = common_rows(image.read_file(active.COMMON), arm)
    rows, portraits = [], []
    for frame, key, speaker, values, rationale in HOLDS:
        ja, en, screen = source[key], installed[key], screens[frame]
        assert ja.text.count(b"%s") == en.text.count(b"%s") == len(values)
        requests = [r for r in calls if r["message_ID"] == key and 0 < frame - r["frame"] <= 400]
        first, second = requests
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
        args, native_hex = (), []
        if values:
            line, args, native_hex, ink = inferred_args(arm, kanji, en, values, screen)
            lines = [line]
        elif frame in REFIT:
            assert REFIT[frame] == key
            lines, ink = exact_refit(font, en.text, screen)
        else:
            english = en.text.decode("ascii").strip()
            separate = {1264: ["Which ship would you like", "to rename?"]}
            lines = separate.get(key, [english])
            assert " ".join(lines) == english
            ink = panels.exact_body(font, lines, screen)
        review = dict.fromkeys(GATES, True)
        decision = "retention"
        if key in PROPOSALS:
            decision = "revision proposed"
            review["formatting"] = False
        rows.append(dict(message_ID=key, decision=decision, rationale=rationale, speaker=speaker,
            Japanese=ja.text.decode("cp932"), English=en.text.decode("ascii").strip(), source=panels.text_reference(ja), installed=panels.text_reference(en),
            review=review, proposed_english=PROPOSALS.get(key), actual_lines=lines, substituted_values=args, substituted_hex=native_hex,
            complete_foreground_pixels=ink, nameplate=panels.nameplate(font, speaker, screen), requests=requests, capture=frames[frame]))
        if frame not in REFIT:
            portraits.append((f"{frame} / COMMON {key}", screen))

    source_config = Path("translations/shipyard_ui_arm9_v1.json")
    cancel, = [r for r in read(source_config)["records"] if r["id"] == "DK4_YARD_CANCEL_REMODEL_PROMPT"]
    ja_literal, en_literal = bytes.fromhex(cancel["source_hex"]), cancel["english"].encode("ascii") + b"\0"
    assert original_arm[cancel["offset"]:cancel["offset"] + len(ja_literal)] == ja_literal
    offset = arm.index(en_literal)
    assert arm.count(en_literal) == 1 and offset == 0x133130
    cancel = dict(source=cancel, installed=dict(offset=offset, exact_hex=en_literal.hex()), Japanese=ja_literal.rstrip(b"\0").decode("cp932"),
        English=cancel["english"], visible_choice=True, decision="retention", review=dict.fromkeys(GATES, True),
        rationale="The cancellation question uses the existing Remodel command label and confirms before discarding the screen state.",
        complete_foreground_pixels=panels.exact_body(font, [cancel["english"]], screens[18120]), capture=frames[18120])
    portraits.append(("18120 / Cancel remodeling?", screens[18120]))
    sheets = panels.sheets_for("nagasaki_yard_dialogue", portraits)
    refit_sheet = OUT.with_name("nagasaki_yard_refit_returns_20261124.png")
    visual = Image.new("RGB", (1024, 816), "#263238")
    draw = ImageDraw.Draw(visual)
    sample_frames = {6920: "Standard stock", 9720: "Special design choice", 11720: "Sale quote list", 16920: "Square sail",
                     17320: "Lateen sail", 17720: "Cannon Type", 21320: "Ship Name keyboard", END: "Return to Nagasaki"}
    for index, (frame, title) in enumerate(sample_frames.items()):
        x, y = 256 * (index % 4), 408 * (index // 4)
        draw.text((x + 4, y + 4), title, fill="white")
        visual.paste(screens[frame], (x, y + 20))
    visual.save(refit_sheet)
    balances = [dict(frame=frame, **panels.find_mask(font, "38493", screens[frame], (38, 348, 136, 367)))
                for frame in (3720, 6120, 10520, 13720, 18920, END)]
    returned = dict(frame=END, title=find_complete(font, "Nagasaki", screens[END], (45, 14, 123, 32)), capture=frames[END])
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True, records=rows, fixed_ARM9_prompt=cancel,
        replay_commands=commands, exact_source_requests=calls, wallet_balances=balances, returned_to_town=returned,
        completed_no_purchase_sale_rename_refit=True, current_quotes_may_use_original_fullwidth_numeric_arguments=True,
        unvisited=["Completing a sale, equipment refit or rename", "Buying past the confirmation", "Damaged ships", "Captain and Arrange options"],
        ROM_changed=False, new_editorial_credit=0, evidence=list(map(reference, (*paths, play.HISTORY, active.RELEASE, source_config, refit_sheet))) + sheets))
    print("Verified the Nagasaki Yard visit and recorded three layout revisions for native preflight.")


if __name__ == "__main__":
    main()
