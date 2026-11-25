"""Verify the cancelled offer, investment, low-funds reply, and free local quote."""

import json
from types import FunctionType

from PIL import Image, ImageDraw

from scripts import observe_syracuse_investment_20261124 as play
from scripts import verify_syracuse_services_20261124 as prior
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


panels = prior.panels
OUT = prior.OUT.with_name("syracuse_investment_current_20261124.json")
SHEET = OUT.with_suffix(".png")
END = 14500
HOLDS = ((5700, 8), (6900, 762), (8100, 746), (9300, 762),
         (10500, 747), (11700, 762), (12100, 748), (13300, 18))
ARCHIVED = {284, 318, 750, 751, 752}
QUOTE_COLOR = (0, 8, 0)
REVIEW = {
    8: prior.REVIEW[8],
    18: ("Trader", (), ("There's a fee for each price check.", "Which town did you have in mind?"),
         "The trader says each price check has a viewing fee and asks which town the player wants to look up.",
         "The two complete sentences introduce the fee before asking the player for a town. The map then quotes the actual amount."),
    746: ("Trader", (), ("Just browsing?",),
          "The trader asks if the player was only looking after the offer is withdrawn.",
          "The brief, mildly disappointed question suits a merchant who waited for a decision."),
    747: ("Trader", (), ("Thanks. We'll put it to good use.",),
          "The trader expresses gratitude and promises to put the investment to good use.",
          "The warmth follows naturally once the player commits the money, and the promise stays intact."),
    748: ("Trader", (), ("Huh? Sorry, that won't be enough.", "Come back when you've earned more."),
          "The trader is surprised, apologizes that the amount is insufficient, and asks the player to return with more gold.",
          "The surprised reaction softens into an apology. The invitation to return has a complete line and matches the original condition."),
    762: ("Trader", (), ("You need market share to trade.", "You still want to invest?",
                       "That's generous of you.", "How much will you put in?"),
          "Without market share the player cannot trade. The trader expresses surprise and appreciation before asking for the investment amount.",
          "The prohibition, surprise, praise, and question each have a complete line. The same reply fits each visit because the player still has no share."),
}


def map_quote(screen, arm, kanji, *, compact=False):
    text = "Syracuse: 0 coins" if compact else "Syracuse: ０ coins"
    area = (90, 248, 214, 266)
    actual = {(x, y) for x in range(area[0], area[2]) for y in range(area[1], area[3])
              if screen.getpixel((x, y)) == QUOTE_COLOR}
    origin = min(x for x, _ in actual), 254
    x, y = origin
    events = []
    for character in text:
        raw = character.encode("cp932")
        wide = len(raw) == 2
        events.append(dict(kind="cp932" if wide else "ascii",
                           code=int.from_bytes(raw, "big"), x=x, y=y - 192 - int(wide), style=1))
        x += len(raw) * 6
    assert x <= area[2]
    pixels = expected_pixels(arm, kanji, events, 4)
    expected = {(column, row) for column in range(area[0], area[2]) for row in range(area[1], area[3])
                if (pixels[((row - 192) * 256 + column) // 2] >> (column % 2 * 4)) & 15 == 1}
    assert actual == expected, (len(actual - expected), len(expected - actual))
    return dict(text=text, origin=origin, native_glyph_events=events, complete_ink_pixels=len(actual),
                exact_source_font_plane=True, cp932_full_width_amount=not compact)


def main():
    release = read(play.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    paths = [play.ROOT / name for name in ("capture/capture_report.json", "trace/requests.json",
             "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, paths)
    assert capture["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"] == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["callback_errors"] and not capture["savestate_loaded"]
    assert terminal["ordinary_controller_inputs"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    assert capture["frames"] == journal["last_command_frame"] == terminal["total_frames"] == END
    assert all(digest(p) == value for p, value in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    commands = [json.loads(line) for line in play.CONTROLLER.read_text(encoding="utf-8").splitlines()]
    assert commands == [r["command"] for r in journal["commands_received"]]
    assert commands[:len(play.OPENING)] == list(play.OPENING) and commands[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"] == read(play.PREVIOUS)["evidence"]["donor"]["sha256"]

    raw_calls = trace["source_requests"]
    assert raw_calls == terminal["common_requests"] and ARCHIVED.isdisjoint(row["message_ID"] for row in raw_calls)
    assert tuple(row["message_ID"] for row in raw_calls[::2]) == tuple(key for _, key in HOLDS)
    frames = panels.shots(capture, "_navigation.png")
    screens = {frame: panels.picture(path) for frame, path in frames.items()}
    clean, installed = map(NdsImage.open, (CLEAN, play.current.ROM))
    old_arm, arm = (image.read_file(prior.ARM) for image in (clean, installed))
    assert old_arm[0xBC908:0xBC98C] == arm[0xBC908:0xBC98C]
    font = prior.GameAsciiFont.from_arm9(arm)
    jp = prior.common_message_entries(clean.read_file(prior.COMMON), old_arm)
    en = prior.common_rows(installed.read_file(prior.COMMON), arm)
    verify = FunctionType(prior.dialogue.__code__, vars(prior) | dict(HOLDS=HOLDS, REVIEW=REVIEW))
    records = verify(jp, en, frames, raw_calls, screens, font)
    for record in records:
        record["context"] = ("The Trader greets Maria before three visits to Invest. She cancels a large offer, pays it on the "
                             "next visit, and then has too little gold to invest again. She opens and leaves Price Info afterward.")

    wallets = {frame: panels.find_mask(font, str(value), screens[frame], (54, 348, 137, 366))
               for frame, value in ((6100, 38371), (8500, 38371), (10900, 1473), (12500, 1473), (14100, 1473), (END, 1473))}
    values = {7300: (1942, 36429), 7700: (36898, 1473), 10100: (36898, 1473)}
    amount_views = {frame: [
        panels.find_mask(font, str(amount), screens[frame], rect)
        for amount, rect in zip(pair, ((134, 327, 192, 348), (134, 346, 192, 364)), strict=True)
    ] for frame, pair in values.items()}
    assert all(sum(pair) == 38371 for pair in values.values())
    assert 1473 < 1942 and 38371 - 36898 == 1473
    quote = map_quote(screens[13700], arm, installed.read_file("/GRP/KANJI.FNT"))
    town = panels.find_mask(font, "Syracuse", screens[END], (26, 12, 129, 32))

    selected = ((7700, "Projected investment"), (8100, "Withdraw the offer"), (10500, "Accept the investment"),
                (11700, "Return to Invest"), (12100, "Insufficient funds"), (13700, "Free local quote"))
    sheet = Image.new("RGB", (768, 808), "#263238")
    labels = ImageDraw.Draw(sheet)
    for index, (frame, label) in enumerate(selected):
        x, y = (index % 3) * 256, (index // 3) * 404
        labels.text((x + 4, y + 4), label, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    sheet.save(SHEET)
    result = dict(
        translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), records=records, candidate_sha256=release["candidate_sha256"],
        release=reference(play.current.RELEASE), controller=reference(play.CONTROLLER),
        ordinary_gameplay=True, original_battery_save=reference(donor["source"]),
        native_requests=raw_calls, wallet_masks=wallets, investment_amount_and_projected_funds=amount_views,
        low_funds=dict(message_ID=748, capture=frames[12100], original_ARM9_range=[0x020BC908, 0x020BC98C]),
        amount_paid=36898, local_quote=quote, return_to_Syracuse=town, contact_sheet=reference(SHEET),
        evidence=list(map(reference, paths)), absent_archived_ids=sorted(ARCHIVED), ROM_changed=False, new_editorial_credit=0,
    )
    prior.validate_natural_dialogue_batch(result)
    write(OUT, result)
    print(f"Verified {len(records)} retained lines in {len(HOLDS)} gameplay holds, including the native insufficient-funds reply.")


if __name__ == "__main__":
    main()
