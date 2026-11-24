"""Verify Athens Market refusal, investment cancellation, and settlement."""

import json
from pathlib import Path

from PIL import Image, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch

from scripts import observe_athens_trade_20261124 as play
from scripts import verify_riga_trade_deck_20261124 as evidence
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write

OUT = evidence.OUT.with_name("athens_market_investment_20261124.json")
SHEET = OUT.with_suffix(".png")
END = 32390
HOLDS = {
    761: ((25990, 28790, 31590), ("Palace",),
          ("Sorry. Please sign a contract", "at the Palace, then come back."),
          "The apology gives a courteous refusal and explains the two next steps. The full Palace substitution stays with its preposition."),
    762: ((27190, 29990), (),
          ("You need market share to trade.", "You still want to invest?",
           "That's generous of you.", "How much will you put in?"),
          "Four complete lines carry the rule, surprise, appreciation and amount question. The renewed offer makes sense after the player cancels."),
    746: ((27990,), (), ("Just browsing?",),
          "The disappointed but mild question fits when the player closes the amount selector without paying."),
    747: ((30790,), (), ("Thanks. We'll put it to good use.",),
          "The thanks and promise follow payment. The trader does not promise a contract or market share in return."),
}
SOURCE_MEANINGS = {
    761: "Sorry. Make a contract at the named facility, then come back.",
    762: "You're offering to invest even though you can't trade without a share? That's unusually kind. How much will you invest?",
    746: "Were you just looking?",
    747: "Thanks. We'll make good use of it.",
}
FIGURES = ((25990, "Trade requires a contract"), (27190, "Investment without market share"),
           (27590, "Projected amount and funds"), (27990, "Cancel without paying"),
           (30790, "Confirm the investment"), (31590, "Trade still requires a contract"))


def main():
    release = read(play.earlier.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.earlier.current.ROM) == release["candidate_sha256"]

    capture = play.ROOT / "capture/capture_report.json"
    journal = play.ROOT / "capture/navigation_command_journal.json"
    report, commands, previous = map(read, (capture, journal, play.PRIOR))
    assert report["ROM_sha256"] == commands["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == commands["last_command_frame"] == END
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"][:len(previous["scripted_input_schedule"])] == previous["scripted_input_schedule"]
    assert list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines())) == [
        entry["command"] for entry in commands["commands_received"]] == list(play.MARKET_ACTIONS)
    assert all(entry["validation_passed"] for entry in commands["commands_received"])
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert digest(donor["source"]) == donor["source_sha256"] == previous["battery_save_preloaded"]["source_sha256"]

    panels = evidence.panels
    frames = panels.shots(report, "_navigation.png")
    pictures = {frame: panels.picture(shot) for frame, shot in frames.items()}
    prior = panels.shots(previous, "_navigation.png")
    assert panels.picture(prior[play.END]).tobytes() == pictures[play.END].tobytes()

    source, current = map(NdsImage.open, (CLEAN, play.earlier.current.ROM))
    clean_arm, arm = (rom.read_file(play.earlier.current.ARM) for rom in (source, current))
    path = play.earlier.current.COMMON
    archive = current.read_file(path)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    clean_rows = evidence.base.common_message_entries(source.read_file(path), clean_arm)
    installed_rows = evidence.base.common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)

    records = []
    for key, (observed, args, lines, rationale) in HOLDS.items():
        clean, installed = clean_rows[key], installed_rows[key]
        assert clean.text.count(b"%s") == installed.text.count(b"%s") == len(args)
        rendered = installed.text % tuple(arg.encode("ascii") for arg in args)
        assert rendered.decode("ascii").split() == " ".join(lines).split()
        masks = [dict(capture=frames[frame], body_ink_pixels=panels.exact_body(font, lines, pictures[frame]),
                      nameplate=panels.nameplate(font, "Trader", pictures[frame])) for frame in observed]
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=path,
            clean_Japanese=clean.text.decode("cp932"), source_meaning=SOURCE_MEANINGS[key],
            english=" ".join(installed.text.decode("ascii").split()),
            speaker="Trader", context="The Athens Market trader handles Trade without a contract, a cancelled investment and a paid investment.",
            runtime_arguments=args, lines=lines, decision="retention", localization_note=rationale, review=dict.fromkeys(GATES, True),
            source_reference=evidence.source_ref(clean), current_reference=evidence.source_ref(installed),
            installed_reference=evidence.source_ref(installed), holds=masks))

    wallet = {frame: panels.find_mask(font, str(total), pictures[frame], (55, 348, 139, 366))
              for frame, total in ((26390, 7776), (28390, 7776), (31190, 6350), (31990, 6350), (END, 6350))}
    choices = {frame: [panels.find_mask(font, label, pictures[frame], area) for label, area in (
                    ("Investment", (64, 329, 131, 346)), ("1426", (153, 329, 184, 346)),
                    ("Funds", (64, 346, 139, 366)), ("6350", (134, 346, 192, 366)))]
               for frame in (27590, 30390)}
    assert 7776 - 1426 == 6350

    sheet = Image.new("RGB", (768, 808), "#263238")
    labels = ImageDraw.Draw(sheet)
    for index, (frame, title) in enumerate(FIGURES):
        x, y = index % 3 * 256, index // 3 * 404
        labels.text((x + 4, y + 4), title, fill="white")
        sheet.paste(pictures[frame], (x, y + 20))
    sheet.save(SHEET)
    result = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], release=reference(play.earlier.current.RELEASE),
        method="Ordinary controller inputs from the byte-exact Athens battery save. Displayed text is matched to exact stored bodies and native font pixels.",
        ordinary_gameplay=True, native_request_trace=False, hardware_observed=False, ROM_changed=False, new_editorial_credit=0,
        original_input_and_frame_exact_match=True, records=records, wallet=wallet, amount_choices=choices,
        investment_payment=1426, trade_refused_after_payment=True,
        donor=reference(donor["source"]), evidence=list(map(reference, (capture, journal, play.PRIOR, play.CONTROLLER))),
        contact_sheet=reference(SHEET), unvisited=["Athens Trade with a contract", "Other investment amounts and alternate trader replies"])
    validate_natural_dialogue_batch(result)
    write(OUT, result)
    print("Verified four retained Athens Market records across seven holds and the 1,426-gold settlement.")


if __name__ == "__main__":
    main()
