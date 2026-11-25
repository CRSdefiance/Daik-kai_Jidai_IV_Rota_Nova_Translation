"""Verify naturally active Trends, Price Info and the Athens Market return."""

import json
from inspect import getsource
from pathlib import Path
from struct import unpack_from

from dk4tool.dialogue.font_audit import GameAsciiFont
from PIL import Image, ImageDraw

from scripts import observe_athens_active_trend_20261124 as play
from scripts import stage_market_info_trends_20261115 as heading
from scripts import verify_current_european_trends_20261123 as trend
from scripts import verify_riga_trade_deck_20261124 as evidence
from scripts import verify_syracuse_investment_20261124 as prices
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write
from scripts.verify_market_info_trends_20261115 import BOX, font_mask
from scripts.verify_personal_gameplay_v841 import get_machine

OUT = evidence.OUT.with_name("athens_ordinary_market_trends_20261124.json")
SHEET = OUT.with_suffix(".png")
BASE = 0x02000000
END = 25590
MANUSCRIPT = Path("translations/commodity_name_manuscript_v343.json")
PRICE = Path("translations/editorial_checkpoints/shared_display_20261123/price_info_descriptions_review_20261123.json")
EXCHANGE = (
    (18390, 8, "Trader", ("Need help?",),
     "The brief question invites the visitor to choose a Market service."),
    (19990, 18, "Trader", ("There's a fee for each price check.", "Which town did you have in mind?"),
     "One sentence explains the fee rule and the next asks which town to inspect. Athens's local rate is shown separately as zero coins."),
    (23990, 245, "Price Info", ("Rubies from Iceland.", "Ruby is the red variety of corundum."),
     "The catalogue's short origin tag preserves Iceland. The second line gives the source's complete mineral definition and keeps 'red variety of corundum' together."),
)
panels = evidence.panels


def snapshot(report, frame):
    snap, = [entry for entry in report["read_only_pause_RAM_snapshots"] if entry["frame"] == frame]
    raw = Path(snap["path"]).read_bytes()
    assert snap["read_only_export"] and len(raw) == 0x400000 and sha256(raw).hexdigest() == snap["sha256"]
    return snap, raw


def commodity(index, clean_arm, cpu, get, reviewed):
    record = reviewed[index]
    field = record["pointer_field"]
    clean_address, = unpack_from("<I", clean_arm, field)
    clean_raw = record["Japanese"].encode("cp932") + b"\0"
    assert clean_arm[clean_address - BASE:clean_address - BASE + len(clean_raw)] == clean_raw
    p = get(0xCD1AC, index)
    pointer, = unpack_from("<I", cpu.mem_read(p, 4))
    expected = record["English"].encode("ascii") + b"\0"
    assert bytes(cpu.mem_read(pointer, len(expected))) == expected
    return dict(index=index, clean_Japanese=record["Japanese"], english=record["English"],
        source_reference=dict(offset=clean_address - BASE, pointer_field=field, exact_hex=clean_raw.hex()),
        installed_reference=dict(runtime_pointer=pointer, runtime_slot=p, exact_hex=expected.hex()))


def market_trends(arm, clean_arm, report, catalogue):
    holds = {}
    for frame in (play.FIRST, 21190, 22390, 23590, 23990, END):
        snap, raw = snapshot(report, frame)
        cpu, get = get_machine(arm, raw)
        local = get(0xB65E4)
        town = get(0xB6618)
        assert local == 19 and town == get(0xCB178) + 4 + 108 * local
        codes = []
        for n in (0, 1):
            addr = get(0xB30EC, town, n)
            product, quantity = cpu.mem_read(addr, 2)
            assert get(0xB31E0, town, product) == quantity and quantity
            codes.append(dict(index=n, address=addr, commodity=product, strength=quantity))
        assert [(r["commodity"], r["strength"]) for r in codes] == [(89, 59), (73, 1)]
        holds[frame] = dict(snapshot=snap, port=local, municipal_trend_slots=codes,
            registered_names=[commodity(idx, clean_arm, cpu, get, catalogue) for idx in (89, 73)])
    return holds, commodity(108, clean_arm, cpu, get, catalogue)


def exact_name(font, screen, text):
    region, color = (143, 207, 256, 222), (230, 230, 230)
    x0, y0, x1, y1 = region
    actual = {(x, y) for x in range(x0, x1) for y in range(y0, y1) if screen.getpixel((x, y)) == color}
    for advance in (5, 6):
        points = {(n * advance + x, y) for n, char in enumerate(text)
                  for x in range(6) for y in range(11) if font.decode(char).getpixel((x, y))}
        origin = (min(x for x, _ in actual) - min(x for x, _ in points),
                  min(y for _, y in actual) - min(y for _, y in points))
        if actual == {(x + origin[0], y + origin[1]) for x, y in points}:
            return dict(text=text, origin=origin, native_advance=advance, ink_pixels=len(actual), region=region)
    raise AssertionError(f"Incomplete native commodity label {text}")


def main():
    release = read(play.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    capture = play.ROOT / "capture/capture_report.json"
    journal = play.ROOT / "capture/navigation_command_journal.json"
    report, commands, old = map(read, (capture, journal, play.PRIOR))
    assert report["ROM_sha256"] == release["candidate_sha256"] == commands["ROM_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert report["frames"] == commands["last_command_frame"] == END
    authored = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert authored == [entry["command"] for entry in commands["commands_received"]]
    assert all(entry["validation_passed"] for entry in commands["commands_received"])
    assert report["scripted_input_schedule"][:len(old["scripted_input_schedule"])] == old["scripted_input_schedule"]
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]

    original, candidate = map(NdsImage.open, (CLEAN, play.current.ROM))
    clean_arm, arm = (rom.read_file(heading.ARM) for rom in (original, candidate))
    common_path = play.current.COMMON
    archive = candidate.read_file(common_path)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"] and sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = evidence.base.common_message_entries(original.read_file(common_path), clean_arm)
    installed = evidence.base.common_rows(archive, arm)
    frames = panels.shots(report, "_navigation.png")
    pictures = {f: panels.picture(data) for f, data in frames.items()}
    before = panels.shots(old, "_cold_boot.png")
    assert panels.picture(before[play.FIRST]).tobytes() == pictures[play.FIRST].tobytes()
    catalogue = {r["index"]: r for r in read(MANUSCRIPT)["records"]}
    slots, named = market_trends(arm, clean_arm, report, catalogue)
    assert [r["english"] for r in slots[21190]["registered_names"]] == ["Armor", "Rubies"]
    event_archive = candidate.read_file(trend.EVENT)
    assert event_archive == original.read_file(trend.EVENT)
    event, = [r["original_event"] for r in read(trend.CATALOGUE)["records"] if r["route"] == 1 and r["English"] == "Athens"]
    earned = trend.previous.event_completion(arm, {"read_only_RAM_snapshot": slots[play.FIRST]["snapshot"]},
        event_archive, event, trend.PLANS["athens"])

    old_heading = clean_arm[heading.OFFSET:heading.OFFSET + heading.SLOT]
    current_heading = arm[heading.OFFSET:heading.OFFSET + heading.SLOT]
    assert old_heading == heading.JAPANESE.encode("cp932").ljust(8, b"\0")
    assert current_heading == b"Trends\0\0"
    assert unpack_from("<I", clean_arm, heading.POINTER) == unpack_from("<I", arm, heading.POINTER) == (BASE + heading.OFFSET,)
    font = GameAsciiFont.from_arm9(arm)
    ink = {f: font_mask(pictures[f], font, "Trends", 80, 211, BOX, (230, 230, 230)) for f in (21190, 22390, 23590, 24390)}
    assert set(ink.values()) == {74}
    records = [
        dict(id=heading.RECORD, file_path=heading.ARM, clean_Japanese=heading.JAPANESE, english="Trends",
             context="Market Info with ordinary municipal trends in Athens.",
             source_reference=dict(offset=heading.OFFSET, exact_hex=old_heading.hex()),
             current_reference=dict(offset=heading.OFFSET, exact_hex=current_heading.hex()),
             installed_reference=dict(offset=heading.OFFSET, exact_hex=current_heading.hex()),
             observed_frames=list(ink), complete_native_masks=ink, decision="retention",
             localization_note="The short heading matches the Square label for popular goods and reads cleanly on the active report.",
             review=dict.fromkeys(GATES, True)),
        named | dict(id="COMMODITY_108", file_path=heading.ARM, context="The Price Info item chooser.",
            current_reference=named["installed_reference"], observed_frame=23590,
            mask=exact_name(font, pictures[23590], "Fire and Ice Rubies"), decision="retention",
            localization_note="The name preserves the fire-and-ice contrast of the Japanese commodity name in full.",
            review=dict.fromkeys(GATES, True)),
    ]
    previous, = (r for r in read(PRICE)["records"] if r["message_id"] == 245)
    assert previous["Japanese"] == source[245].text.decode("cp932") and previous["english"].split() == installed[245].text.decode("ascii").split()
    for frame, key, speaker, lines, reason in EXCHANGE:
        a, b = source[key], installed[key]
        assert a.text.count(b"%") == b.text.count(b"%") == 0
        assert " ".join(lines).split() == b.text.decode("ascii").split()
        mask = panels.exact_body(font, lines, pictures[frame])
        name = panels.nameplate(font, speaker, pictures[frame]) if key != 245 else None
        records.append(dict(id=f"COMMON_MESSAGE_{key}", file_path=common_path, message_ID=key, speaker=speaker,
            clean_Japanese=a.text.decode("cp932"), english=" ".join(lines), context="The Athens Market and Price Info exchange.",
            source_reference=evidence.source_ref(a), current_reference=evidence.source_ref(b), installed_reference=evidence.source_ref(b),
            capture=frames[frame], native_body_pixels=mask, native_nameplate=name,
            decision="retention", localization_note=reason, review=dict.fromkeys(GATES, True)))
    assert pictures[23590].tobytes() == pictures[24390].tobytes()
    assert pictures[22390].tobytes() == pictures[24790].tobytes()
    wallet = {f: panels.find_mask(font, "7776", pictures[f], (55, 348, 137, 367)) for f in (18790, END)}
    quote_recipe = checked_text(getsource(prices.map_quote), {
        "Syracuse": "Athens", "(90, 248, 214, 266)": "(135, 248, 236, 266)",
        "min(x for x, _ in actual), 254": "min(x for x, _ in actual), 249",
    })
    quote_scope = vars(prices).copy()
    exec(compile(quote_recipe, __file__ + "::compact-quoted-fee", "exec"), quote_scope)
    quote = quote_scope["map_quote"](pictures[20390], arm, candidate.read_file("/GRP/KANJI.FNT"), compact=True)
    ink_price = panels.find_mask(font, "9500", pictures[23590], (144, 345, 174, 362))

    sheet = Image.new("RGB", (1024, 409), "#263238")
    titles = ImageDraw.Draw(sheet)
    for i, (frame, title) in enumerate(((20390, "Athens report quote"), (21190, "Ordinary active Trends"),
                                       (23590, "Fire and Ice Rubies"), (23990, "Full description"))):
        x = i * 256
        titles.text((x + 5, 5), title, fill="white")
        sheet.paste(pictures[frame], (x, 24))
    sheet.save(SHEET)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        release=reference(play.current.RELEASE), evidence=list(map(reference, (capture, journal, play.CONTROLLER, play.PRIOR, MANUSCRIPT, PRICE))),
        donor=reference(donor["source"]), initial_square_exact_match=True, natural_trend_event=earned,
        confirmed_active_town_records=slots, records=records, quote=quote, wallet=wallet, price_pixels=ink_price,
        returns=[24390, 24790, 25190, END], contact_sheet=reference(SHEET), ROM_changed=False, new_editorial_credit=0))
    print("Verified the naturally active Athens trend report, five retained text records, and the zero-fee return.")


if __name__ == "__main__":
    main()
