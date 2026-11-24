"""Verify Riga's rumor, paid round, repeat recruitment and crew assignment."""

import json
from itertools import product

from PIL import Image, ImageDraw

from scripts import observe_riga_tavern_20261124 as play
from scripts import verify_nagasaki_tavern_20261124 as prior
from scripts.probe_map_tooltip_cp932_pixels import expected_pixels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write


panels = prior.panels
OUT = prior.OUT.with_name("riga_tavern_current_20261124.json")
SHEET = OUT.with_suffix(".png")
END = 15600
GERHARD, BAR, PATRON = "Gerhard Adernkatz", "Barkeep", "Patron"
HOLDS = (
    (4000, 51, BAR, (), ("Welcome! What will you have?",), "A warm greeting gives the player space to order."),
    (4800, 53, BAR, (), ("5 coins.",), "The short reply works as a spoken price and matches the actual charge."),
    (5200, 821, BAR, ("Argot", "Amsterdam", "trader"), ("Argot from Amsterdam is a trader", "with real pull here."),
     "Real pull conveys influence in the area. The line keeps the trader, the home city, and the occupation."),
    (6400, 852, GERHARD, ("204",), ("It looks like it'll cost 204 gold.", "Is that all right?"),
     "Gerhard gives the estimate before asking for consent. Amount and currency stay together."),
    (7600, 852, GERHARD, ("204",), ("It looks like it'll cost 204 gold.", "Is that all right?"),
     "The same polite estimate applies when the player reopens the offer."),
    (8000, 865, "Hodram Bergstrom", (), ("Drinks for everyone!",), "The quick call suits a round offered to the entire room."),
    (8400, 872, BAR, ("Bergstrom",), ("This round's on Bergstrom. Enjoy!",),
     "The barkeep announces who pays and invites the patrons to enjoy it. The established surname substitution applies."),
    (8800, 874, PATRON, (), ("Whoa! Really? Thanks for the round!", "Mighty generous of you!"),
     "The patron moves from surprise to thanks and then offers an appreciative aside."),
    (9200, 880, PATRON, ("Clifford", "London"), ("Word is, Clifford has a fleet", "heading to London."),
     "Word is keeps the news as hearsay. The fleet's destination and direction stay clear."),
    (10400, 890, GERHARD, ("1020",), ("I'll recruit crew for 1020 gold.",),
     "The first mate states the plan and cost before the player's choice."),
    (10800, 897, GERHARD, (), ("Who wants to sail with the Admiral?",),
     "The question fits a call for volunteers. Admiral matches the original form of address."),
    (11200, 907, PATRON, (), ("Aye!",), "The brief response fits a volunteer answering from the crowd."),
    (11600, 904, GERHARD, ("56",), ("We've got 56 willing to join.",),
     "The reply gives the first volunteer total without implying they are already assigned."),
    (12000, 1042, GERHARD, ("49",), ("There's room for 49 more aboard.", "Shall I recruit more?"),
     "The follow-up repeats more immediately. Keep the exact room and Gerhard's polite offer to continue."),
    (12400, 904, GERHARD, ("64",), ("We've got 64 willing to join.",),
     "The same report naturally gives the new total after another attempt."),
    (13200, 71, GERHARD, ("120",), ("Is it all right to leave １２０", "of our sailors unassigned?"),
     "The confirmation asks permission to leave the specified sailors unassigned. The wide numeral differs from the surrounding font."),
    (15200, 71, GERHARD, ("15",), ("Is it all right to leave １５", "of our sailors unassigned?"),
     "The wording works after the flagship assignment. The smaller figure still uses the wider font."),
)


def mixed_body(screen, arm, kanji, lines):
    """Match both source font families across the complete dialogue plane."""
    color = (0, 8, 0)
    actual = {(x, y) for x in range(16, 245) for y in range(296, 360) if screen.getpixel((x, y)) == color}
    matches = []
    for starts, wide_y in product(product((16, 20, 22), repeat=len(lines)), (-1, 0)):
        events = []
        for row, (start, raw_line) in enumerate(zip(starts, lines, strict=True)):
            x = start
            for char in raw_line:
                raw = char.encode("cp932")
                wide = len(raw) == 2
                events.append(dict(kind="cp932" if wide else "ascii", code=int.from_bytes(raw, "big"),
                                   x=x, y=105 + 16 * row + (wide_y if wide else 0), style=1))
                x += 6 * len(raw)
            assert x <= 245
        pixels = expected_pixels(arm, kanji, events, 4)
        expected = {(x, y) for x in range(16, 245) for y in range(296, 360)
                    if (pixels[((y - 192) * 256 + x) // 2] >> (x % 2 * 4)) & 15 == 1}
        if expected == actual:
            matches.append(dict(ink_pixels=len(actual), start_pixels=starts, wide_offset_y=wide_y,
                                wide_codes=[g["code"] for g in events if g["kind"] == "cp932"]))
    match, = matches
    return match


def main():
    active = play.current
    release = read(active.RELEASE)
    assert digest(active.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    paths = [play.ROOT / name for name in ("capture/capture_report.json", "trace/requests.json",
             "capture/navigation_command_journal.json", "terminal.json")]
    capture, trace, journal, terminal = map(read, paths)
    assert capture["ROM_sha256"] == journal["ROM_sha256"] == terminal["candidate_sha256"] == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert terminal["ordinary_controller_inputs"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    donor = capture["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"] == read(play.PRIOR)["visits"]["riga"]["donor"]["sha256"]
    assert donor["copied_byte_exact_before_cold_boot"]
    commands = [json.loads(line) for line in play.CONTROLLER.read_text(encoding="utf-8").splitlines()]
    assert commands == [r["command"] for r in journal["commands_received"]]
    assert commands[:len(play.OPENING)] == list(play.OPENING) and commands[-1] == {"stop": True}
    assert all(row["validation_passed"] for row in journal["commands_received"])
    assert capture["frames"] == journal["last_command_frame"] == terminal["total_frames"] == END
    assert all(digest(path) == value for path, value in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    calls = trace["source_requests"]
    assert calls == terminal["common_requests"] and len(calls) == len(HOLDS) * 2
    assert tuple(r["message_ID"] for r in calls[::2]) == tuple(key for _, key, *_ in HOLDS)
    frames = panels.shots(capture, "_navigation.png")
    screens = {n: panels.picture(shot) for n, shot in frames.items()}
    clean, current = map(NdsImage.open, (CLEAN, active.ROM))
    ja_arm, arm = [i.read_file(active.ARM) for i in (clean, current)]
    jp = prior.common_message_entries(clean.read_file(active.COMMON), ja_arm)
    en = prior.common_rows(current.read_file(active.COMMON), arm)
    font = prior.GameAsciiFont.from_arm9(arm)
    kanji = current.read_file("/GRP/KANJI.FNT")
    rows = {}
    for (frame, key, speaker, args, lines, note), (getter, copier) in zip(HOLDS, zip(calls[::2], calls[1::2], strict=True), strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert 0 < frame - getter["frame"] < 400
        a, b = jp[key], en[key]
        assert a.text.count(b"%s") == len(args) + (key == 872) and b.text.count(b"%s") == len(args)
        normalized = " ".join(lines).translate(str.maketrans("０１２３４５６７８９", "0123456789"))
        assert (b.text % tuple(value.encode("ascii") for value in args)).decode("ascii").split() == normalized.split()
        try:
            mask = mixed_body(screens[frame], arm, kanji, lines) if key == 71 else dict(ink_pixels=panels.exact_body(font, lines, screens[frame]))
        except (ValueError, AssertionError) as error:
            raise AssertionError((frame, key, lines)) from error
        review = dict.fromkeys(GATES, True)
        if key in (71, 1042):
            review["naturalness" if key == 1042 else "formatting"] = False
        record = rows.setdefault(key, dict(id=f"COMMON_MESSAGE_{key}", file_path=active.COMMON, message_ID=key, speaker=speaker,
            clean_Japanese=a.text.decode("cp932"), english=b.text.decode("ascii").strip(),
            source_reference=panels.text_reference(a) | dict(exact_hex=a.text.hex()),
            current_reference=panels.text_reference(b) | dict(exact_hex=b.text.hex()),
            installed_reference=panels.text_reference(b) | dict(exact_hex=b.text.hex()),
            context="Riga Tavern, from the barkeep’s local tip and the purchased round through recruitment and assigning sailors.",
            localization_note=note, decision="retention" if all(review.values()) else "revision proposed", review=review, holds=[]))
        record["holds"].append(dict(frame=frame, capture=frames[frame], args=args, lines=lines, mask=mask,
                                    complete_nameplate=panels.nameplate(font, speaker, screens[frame]), requests=[getter, copier]))

    wallets = {frame: panels.find_mask(font, str(value), screens[frame], (56, 348, 140, 367))
               for frame, value in ((3200, 44552), (5600, 44547), (6800, 44547), (9600, 44343))}
    choices = {frame: [panels.find_mask(font, choice, screens[frame], box) for choice, box in
                        (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
               for frame in (6400, 7600, 10400, 12000, 13200, 15200)}
    crew = {frame: [prior.find_complete(font, str(value), screens[frame], box)
                    for value, box in zip(counts, ((85, 18, 125, 36), (212, 18, 255, 36)), strict=True)]
            for frame, counts in ((12800, (19, 120)), (15600, (124, 15)))}
    assert 44552 - 5 == 44547 and 44547 - 204 == 44343 and 19 + 120 == 124 + 15

    selected = ((5200, "Barkeep’s tip"), (9200, "Patron’s rumor"), (11600, "First recruitment total"),
                (12000, "Keep looking"), (12400, "Second recruitment total"), (13200, "Wide unassigned count"))
    sheet = Image.new("RGB", (1024, 720), "#263238")
    labels = ImageDraw.Draw(sheet)
    for index, (frame, label) in enumerate(selected):
        x, y = (index % 2) * 512, (index // 2) * 240
        labels.text((x + 4, y + 4), label, fill="white")
        sheet.paste(screens[frame].crop((0, 274, 256, 384)).resize((512, 220), Image.Resampling.NEAREST), (x, y + 20))
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        donor=reference(donor["source"]), controller=reference(play.CONTROLLER), original_native_requests=calls,
        verified_common_records=list(rows.values()), wallet_balances=wallets, choices=choices, visible_crew=crew,
        volunteers=[56, 64], capacity_followup=49, total_assigned_and_unassigned=139,
        source_release=reference(active.RELEASE), sheet=reference(SHEET), evidence=list(map(reference, paths)),
        archived_ids_seen=sorted(set(rows) & {284, 318, 750, 751, 752}), ROM_changed=False, new_editorial_credit=0))
    print(f"Verified {len(rows)} Riga dialogue records in {len(HOLDS)} holds, including both wide-numeral warnings.")


if __name__ == "__main__":
    main()
