"""Review the ordinary Riga mixed deal, departure sequence, and paired Deck help."""

import json
from argparse import ArgumentParser

from PIL import Image, ImageChops, ImageDraw

from scripts import stage_deck_skill_guidance_20261124 as build
from scripts import verify_syracuse_local_purchase_20261124 as trade
from scripts.stage_cartridge_title_20261123 import GATES, NdsImage, digest, read, reference, sha256, write

play, panels = build.play, build.panels
base = trade.prior
OUT = base.OUT.with_name("riga_trade_and_departure_20261124.json")
SHEET = OUT.with_suffix(".png")
PAIRED = build.ROOT / "deck_skill_guidance_paired.json"
PAIRED_SHEET = build.ROOT / "deck_skill_guidance_paired.png"
ARCHIVED = {284, 318, 750, 751, 752}
HOLDS = {
    4400: (8, "Trader", (), ("Need help?",), "The brief greeting invites the customer to choose a service."),
    6800: (11, "Gerhard Adernkatz", (), ("Will this be all right?",),
           "The polite question fits Gerhard and asks for approval of both trades together."),
    7200: (9, "Trader", (), ("Thanks! Come again.",), "The trader thanks the customer and invites a return after settlement."),
    9600: (28, "Port Worker", (), ("You need more sailors on one ship.", "Check fleet setup before you sail."),
           "The worker names the shortage and gives a practical next step without outlawing departure."),
    10000: (814, "Port Worker", (), ("Your sailors look tired.", "Why not let them rest at the inn?"),
            "The worker follows with an optional recommendation and gives the player a place to rest."),
    10400: (85, None, ("78",), ("Sailing days left: about 78.",),
            "The last departure panel gives the remaining sailing time as an estimate."),
    14000: (1494, "Manuel Almeida", (), ("Just watch how I handle this wheel!",),
            "The confident challenge suits Manuel while the player is checking his Helm assignment."),
    14800: (86, None, ("2", "10", "Sky: Cloudy", "Riga"), ("2/10", "Sky: Cloudy", "Departed Riga."),
            "The log preserves the date, weather, and departure port as three distinct facts."),
}


def source_ref(entry):
    return panels.text_reference(entry) | dict(exact_hex=entry.text.hex())


def glyph_mask(font, text, screen, rect, color, xs, ys):
    actual = {(x, y) for y in range(rect[1], rect[3]) for x in range(rect[0], rect[2])
              if screen.getpixel((x, y)) == color}
    matches = [(x, y) for x in xs for y in ys if actual == build.historical.ink(font, text, x, y)]
    match, = matches
    return dict(origin=match, ink_pixels=len(actual), rect=rect, color=color)


def baseline():
    release = read(build.parent.RELEASE)
    capture = build.BASELINE
    trace = play.ROOT / "trace/requests.json"
    terminal = play.ROOT / "terminal.json"
    journal = play.ROOT / "capture/navigation_command_journal.json"
    report, native, final, commands = map(read, (capture, trace, terminal, journal))
    assert report["ROM_sha256"] == final["candidate_sha256"] == commands["ROM_sha256"] == release["candidate_sha256"] == digest(build.parent.ROM)
    assert final["ordinary_controller_inputs"] and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert not native["errors"] and not native["mismatches"] and native["all_host_slots_restored_and_core_file_exact"]
    assert all(digest(path) == sha for path, sha in final["evidence"].items())
    assert (report["frames"], final["total_frames"], commands["last_command_frame"]) == (17600,)*3
    assert list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines())) == [r["command"] for r in commands["commands_received"]]
    assert all(r["validation_passed"] for r in commands["commands_received"])
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"] == final["copied_save_sha256"]
    frames = panels.shots(report, "_navigation.png")
    screens = {frame: panels.picture(row) for frame, row in frames.items()}
    calls = native["source_requests"]
    assert calls == final["common_requests"] and len(calls) == 2 * (len(HOLDS) + 1)
    assert ARCHIVED.isdisjoint(row["message_ID"] for row in calls)
    clean, current = map(NdsImage.open, (build.CLEAN, build.parent.ROM))
    clean_arm, arm = (image.read_file(build.ARM) for image in (clean, current))
    archive = current.read_file(build.COMMON)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] and sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = base.common_message_entries(clean.read_file(build.COMMON), clean_arm)
    installed = base.common_rows(archive, arm)
    font = base.GameAsciiFont.from_arm9(arm)
    records = []
    for (frame, (key, speaker, args, lines, reason)), (getter, copier) in zip(HOLDS.items(), zip(calls[:-2:2], calls[1:-2:2], strict=True), strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["message_ID"] == key and 0 < frame - getter["frame"] < 400
        ja, en = source[key], installed[key]
        assert en.text.count(b"%s") == ja.text.count(b"%s") == len(args)
        english = en.text.decode("ascii").strip()
        assert (english % args).split() == " ".join(lines).split()
        if key == 1494:
            mask = glyph_mask(font, lines[0], screens[frame], (6, 109, 248, 125), (0, 8, 0), (16,), (113,))
            name = panels.find_mask(font, speaker, screens[frame], (76, 35, 169, 54))
        else:
            mask = panels.exact_body(font, lines, screens[frame])
            name = panels.nameplate(font, speaker, screens[frame]) if speaker else None
        records.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=build.COMMON, message_ID=key, english=english,
            clean_Japanese=ja.text.decode("cp932"), speaker=speaker or "System", context="Riga Trade, departure, or Deck View",
            source_reference=source_ref(ja), current_reference=source_ref(en), installed_reference=source_ref(en),
            observed=dict(capture=frames[frame], requests=[getter, copier], lines=lines, arguments=args, body=mask, name=name),
            localization_note=reason, decision="retention", review=dict.fromkeys(GATES, True)))
    clear = read("translations/deck_view_arm9_v2.json")
    warning, = [r for r in clear["records"] if r["id"] == "DK4_DECK_NO_UNASSIGNED_V2"]
    at = warning["offset"]
    before = bytes.fromhex(warning["source_hex"])
    after = (warning["english"].encode("ascii") + b"\0").ljust(len(before), b"\0")
    assert clean_arm[at:at + len(before)] == before and arm[at:at + len(after)] == after
    records.append(dict(id=warning["id"], file_path=build.ARM, english=warning["english"],
        clean_Japanese=before.split(b"\0")[0].decode("cp932"), speaker="Deck View", context="Assign opens with Unassigned and no eligible crew are available.",
        source_reference=dict(offset=at, exact_hex=before.hex()), current_reference=dict(offset=at, exact_hex=after.hex()),
        installed_reference=dict(offset=at, exact_hex=after.hex()),
        observed=dict(capture=frames[12400], body=panels.exact_body(font, [warning["english"]], screens[12400])),
        decision="retention", localization_note="The short warning names the empty pool and matches the existing Unassigned filter.",
        review=dict.fromkeys(GATES, True)))
    pending = (44552, 2100, 1333, 45319)
    ledger = {f: trade.exact_ledger(font, screens[f], totals) for f, totals in {
        5200: (44552, 0, 0, 44552), 5600: (44552, 2100, 0, 46652), 6400: pending, 6800: pending,
    }.items()}
    wallet = panels.find_mask(font, str(pending[-1]), screens[7600], (55, 348, 139, 366))
    assert pending[0] + pending[1] - pending[2] == pending[3]
    goods = {label: base.exact_label(screens[f], font, text, (144, 127), (144, 126, 256, 162))
             for label, f, text in (("cargo", 5200, "Iron Ore\n  Ore 100%"), ("local", 6000, "Furs\n  Luxury 101%"))}
    choices = [panels.find_mask(font, name, screens[6800], bounds) for name, bounds in
               (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
    sides = ((6800, "Mixed-deal confirmation"), (7600, "Settlement"), (9600, "Crew check"), (10000, "Fatigue advice"),
             (12000, "Deck View"), (14000, "Helm advice"), (14800, "Departed Riga"), (17600, "Ordinary sailing"))
    sheet = Image.new("RGB", (1024, 818), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(sides):
        x, y = i % 4 * 256, i // 4 * 409
        draw.text((x + 6, y + 5), label, fill="white")
        sheet.paste(screens[frame], (x, y + 24))
    sheet.save(SHEET)
    assert [r["message_ID"] for r in calls[-2:]] == [97, 97]
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        release=reference(build.parent.RELEASE), evidence=list(map(reference, (capture, trace, journal, terminal, play.CONTROLLER))),
        donor=reference(donor["source"]), records=records, native_requests=calls, archived_IDs_absent_from_these_requests=sorted(ARCHIVED),
        ledger=ledger, wallet=wallet, choices=choices, goods=goods,
        additional_sea_request=dict(requests=calls[-2:], clean_Japanese=source[97].text.decode("cp932"),
            source_reference=source_ref(source[97]), installed_reference=source_ref(installed[97]), visible_hold_pending=True),
        contact_sheet=reference(SHEET), new_editorial_credit=0, ROM_changed=False))
    print(f"Verified nine retained Riga texts, mixed Trade, both Goods Info masks and the departure transition.")


def paired():
    edit = read(build.OUT)
    current = read(build.BASELINE)
    paths = [build.ROOT / folder / "capture_report.json" for folder in ("riga_parent", "riga")]
    old, new = map(read, paths)
    assert old["ROM_sha256"] == current["ROM_sha256"] == edit["predecessor_sha256"]
    assert new["ROM_sha256"] == edit["candidate_sha256"] == digest(build.ROM)
    for report in (old, new):
        assert report["frames"] == current["frames"] and report["scripted_input_schedule"] == current["scripted_input_schedule"]
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
        assert report["battery_save_preloaded"]["source_sha256"] == current["battery_save_preloaded"]["source_sha256"]
    trace = panels.shots(current, "_navigation.png")
    a, b = [panels.shots(report, "_cold_boot.png") for report in (old, new)]
    assert a.keys() == b.keys() and (trace.keys() | set(build.EXTRA)) <= a.keys()
    font = base.GameAsciiFont.from_arm9(NdsImage.open(build.ROM).read_file(build.ARM))
    before = [row["predecessor_compiled"] for row in edit["records"][2:]]
    after = [row["compiled"] for row in edit["records"][2:]]
    changed, identical = [], []
    for frame in sorted(a):
        previous, candidate = (panels.picture(rows[frame]) for rows in (a, b))
        if frame in trace:
            same = panels.picture(trace[frame])
            assert previous.tobytes() == same.tobytes()
        box = ImageChops.difference(previous, candidate).getbbox()
        if frame not in build.HOLDS:
            assert box is None, (frame, box)
            identical.append(frame)
            continue
        assert box and 0 <= box[0] < box[2] <= 256 and 80 <= box[1] < box[3] <= 128
        old_ink, new_ink = (build.actual_help_pixels(screen) for screen in (previous, candidate))
        assert old_ink == build.help_pixels(font, before) and new_ink == build.help_pixels(font, after)
        changed.append(dict(frame=frame, bounds=box, previous=a[frame], candidate=b[frame], old_ink=len(old_ink), new_ink=len(new_ink)))
    assert tuple(row["frame"] for row in changed) == build.HOLDS
    toast_text = "Gerhard leveled up!"
    earlier = read(OUT)["additional_sea_request"]
    toast = panels.picture(b[17420])
    assert earlier["requests"][0]["frame"] == 17354 and 17420 in identical
    label = glyph_mask(font, toast_text, toast, (74, 260, 194, 274), (0, 8, 0), (80,), (262,))
    raw = bytes.fromhex(earlier["installed_reference"]["exact_hex"])
    assert (raw % b"Gerhard").decode("ascii").strip() == toast_text
    sea_review = dict(earlier, id="COMMON_MESSAGE_97", file_path=build.COMMON, message_ID=97,
        english=raw.decode("ascii"), current_reference=earlier["installed_reference"], actual_text=toast_text,
        visible_hold_pending=False, capture=b[17420], complete_native_toast=label,
        review=dict.fromkeys(GATES, True), speaker="Sea View",
        context="Ordinary sailing after departing Riga, as Gerhard earns a level.",
        decision="retention", localization_note="The short exclamation preserves the level-up result and names the navigator.")
    sheet = Image.new("RGB", (1024, 276), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (label, collection) in enumerate((("Previous", a), ("Current", b))):
        x = 512 * i
        draw.text((x + 6, 5), f"{label} / Riga Deck View", fill="white")
        screen = panels.picture(collection[12000]).crop((0, 0, 256, 128))
        sheet.paste(screen.resize((512, 256), Image.Resampling.NEAREST), (x, 20))
    sheet.save(PAIRED_SHEET)
    write(PAIRED, dict(candidate_sha256=edit["candidate_sha256"], predecessor_sha256=edit["predecessor_sha256"],
        ordinary_gameplay=True, previous=reference(paths[0]), candidate=reference(paths[1]), changed_holds=len(changed),
        revised=changed, unchanged_frames=identical, unchanged_holds=len(identical), sheets=[reference(PAIRED_SHEET)],
        full_help_ink_verified=True, original_trace_gameplay=reference(OUT), sea_level_up=sea_review))
    print(f"Verified {len(changed)} changed Deck help holds and {len(identical)} matching companion screens.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("baseline", "paired"))
    {"baseline": baseline, "paired": paired}[cli.parse_args().action]()
