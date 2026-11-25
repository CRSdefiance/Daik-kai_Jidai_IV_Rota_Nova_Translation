"""Bind the revised Palace substitution and the following Athens contract exchange."""

import json
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import observe_athens_palace_contract_20261124 as play
from scripts import preflight_ceuta_contract_refusal_20261124 as preflight
from scripts import verify_riga_trade_deck_20261124 as review
from scripts import verify_syracuse_local_purchase_20261124 as market
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write
from scripts.verify_commodity_private_market_live_v354 import exact_label


OUT = review.OUT.with_name("athens_palace_contract_current_20261124.json")
panels = review.panels
REVISED = (25990, 28790, 31590)
RULER = Path("translations/editorial_checkpoints/SharedText_20261110_v1/ruler_and_ritual_nameplates_review_20261115_v1.json")
END = 44390
HOLDS = ((33590, 1156), (33990, 1157), (34790, 1158), (35590, 1156), (35990, 1157), (36790, 1159),
         (38390, 8), (41590, 11), (42390, 11), (42790, 9))
TEXT = {
    1156: ("Local Lord", ("1213",), ("You'd like to trade here? Hmm...", "Very well. The minimum contract fee",
           "is 1213 gold coins."), "The local lord considers the request, allows it and states the exact minimum payment.",
           "The measured hesitation suits the audience, and 'minimum contract fee' stays together above the complete amount."),
    1157: ("Local Lord", (), ("Your fee sets your market share.", "How much will you offer?"),
           "The contract payment determines the share, and the local lord asks Hodram to name his offer.",
           "The short rule and full question lead cleanly into the amount selector without promising a particular share."),
    1158: ("Local Lord", (), ("Bah! Make up your mind.",), "The local lord scolds Hodram for his indecision.",
           "The burst of impatience fits when Hodram walks back the offer and leaves without paying."),
    1159: ("Local Lord", (), ("Very well. You may trade", "in this city."), "The local lord grants permission to trade in Athens.",
           "The formal assent closes the deal and makes the permission and its local scope clear."),
    8: ("Trader", (), ("Need help?",), "The trader asks what the customer needs.",
        "The brisk greeting works after the contract and gives Hodram the floor to choose Trade."),
    11: ("Charles Rochefort", (), ("Will this be all right?",), "Charles politely asks for approval of the pending deal.",
         "The deferential question fits Charles and applies to both sides of the mixed deal."),
    9: ("Trader", (), ("Thanks! Come again.",), "The trader thanks the customer and welcomes a return visit.",
        "The brief, friendly farewell suits the completed sale and purchase."),
}


def matching_market(release, frames, calls, font):
    old_report = read(play.HISTORY)
    old = panels.shots(old_report, "_navigation.png")
    exact = [frame for frame in (*play.HOLDS, play.FIRST_PAUSE) if frame not in REVISED]
    for frame in exact:
        assert old[frame]["framebuffer_sha256"] == frames[frame]["framebuffer_sha256"], frame
        panels.picture(frames[frame])
    lines = preflight.EXPECTED["Palace"]
    revised = []
    for frame in REVISED:
        before, after = panels.picture(old[frame]), panels.picture(frames[frame])
        delta = ImageChops.difference(before, after).getbbox()
        assert delta and 16 <= delta[0] < delta[2] <= 245 and 296 <= delta[1] < delta[3] <= 360
        native = [row for row in calls if row["message_ID"] == preflight.KEY and 0 < frame - row["frame"] < 400]
        getter, copier = native
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["caller_LR"] == 0x02053FF8
        revised.append(dict(frame=frame, previous_capture=old[frame], current_capture=frames[frame], difference_box=delta,
            lines=lines, arguments=["Palace"], exact_body_pixels=panels.exact_body(font, lines, after),
            exact_nameplate=panels.nameplate(font, "Trader", after), native_requests=native))
    return dict(exact_companion_frames=exact, current_refusal_holds=revised, earlier_market_checkpoint=reference(play.prior.OUT),
                registered_review=reference(play.current.REVIEW), confirmed_build=release["candidate_sha256"])


def capture(release):
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, refs = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    report = read(refs["capture"]["path"])
    previous = read(play.HISTORY)
    earlier = previous["scripted_input_schedule"]
    assert report["scripted_input_schedule"][:len(earlier)] == earlier
    assert refs["donor"]["sha256"] == previous["battery_save_preloaded"]["source_sha256"]
    commands = list(map(json.loads, play.CONTROLLER.read_text("utf-8").splitlines()))
    assert commands[:len(play.OPENING)] == list(play.OPENING)
    assert max(frames) == commands[-2]["until"] == END
    prior_holds = panels.shots(report, "_cold_boot.png")
    assert set(play.HOLDS) <= prior_holds.keys()
    frames.update({frame: prior_holds[frame] for frame in play.HOLDS})
    assert not {284, 318, 750, 751, 752} & {row["message_ID"] for row in calls}
    return frames, calls, refs, commands


def inputs():
    release = read(play.current.RELEASE)
    assert digest(play.current.ROM) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    frames, calls, refs, commands = capture(release)
    clean, rom = map(NdsImage.open, (CLEAN, play.current.ROM))
    old_arm, arm = (image.read_file(play.current.ARM) for image in (clean, rom))
    archive = rom.read_file(play.current.COMMON)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = review.base.common_message_entries(clean.read_file(play.current.COMMON), old_arm)
    installed = review.base.common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)
    registered, = (row for row in read(play.current.REVIEW)["records"] if row["message_ID"] == preflight.KEY)
    assert review.source_ref(source[preflight.KEY]) == registered["source_reference"]
    assert review.source_ref(installed[preflight.KEY]) == registered["installed_reference"]
    assert installed[preflight.KEY].text.decode("ascii").strip() == preflight.DRAFT
    assert set(registered["review"]) == set(GATES) and all(registered["review"].values())
    before = matching_market(release, frames, calls, font)
    role = local_lord(old_arm, arm, release)
    return release, frames, calls, refs, commands, source, installed, font, before, role


def local_lord(clean_arm, arm, release):
    earlier, = (row for row in read(RULER)["records"] if row["actor_ID"] == 126)
    assert earlier["source_Japanese"] == "地方領主" and earlier["english"] == "Local Lord"
    field, = (row for row in earlier["source_actor_fields"] if row["field"] == "primary")
    at = field["ARM9_pointer_field_offset"]
    clean = field["clean"]
    assert unpack_from("<I", clean_arm, at)[0] == clean["pointer"]
    length = clean["byte_length"]
    assert clean_arm[clean["offset"]:clean["offset"] + length + 1] == bytes.fromhex(clean["hex"]) + b"\0"
    boot = read(release["own_registered_startup"])
    assert digest(release["own_registered_startup"]) == release["own_registered_startup_sha256"]
    snapshot = boot["read_only_snapshot"]
    resident = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and sha256(resident).hexdigest() == snapshot["sha256"]
    current, = unpack_from("<I", arm, at)
    assert current == unpack_from("<I", resident, at)[0]
    visible = b"Local Lord\0"
    relative = current - 0x02000000
    assert resident[relative:relative + len(visible)] == visible
    return dict(actor_ID=126, title=earlier["english"], clean_Japanese=earlier["source_Japanese"],
                decision="retention", rationale="The label names a regional ruler, consistent with the clean title and contract scene.",
                clean_reference=clean, installed_reference=dict(pointer=current, pointer_field_offset=at, exact_bytes=visible.hex()),
                previous_review=reference(RULER), startup_snapshot=snapshot, review=dict.fromkeys(GATES, True))


def contract_and_trade(source, installed, frames, screens, calls, font):
    new = [row for row in calls if row["frame"] > play.FIRST_PAUSE]
    assert len(new) == 2 * len(HOLDS)
    records = {}
    for (hold, key), (getter, copier) in zip(HOLDS, zip(new[::2], new[1::2], strict=True), strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["message_ID"] == key and 0 < hold - getter["frame"] < 400
        assert getter["caller_LR"] == (0x02053D10 if key == 11 else 0x02053FF8)
        ja, en = source[key], installed[key]
        speaker, arguments, lines, gloss, note = TEXT[key]
        english = " ".join(en.text.decode("ascii").split())
        assert en.text.count(b"%s") == ja.text.count(b"%s") == len(arguments)
        assert (english % arguments).split() == " ".join(lines).split()
        if key not in records:
            stage = ("The Athens Palace contract after Hodram's investment, including cancellation and payment."
                     if key >= 1156 else "Hodram's first Athens Trade after receiving permission. The deal includes a sale and a purchase.")
            records[key] = dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=play.current.COMMON,
                context=stage, english=english, speaker=speaker, clean_Japanese=ja.text.decode("cp932"),
                source_meaning=gloss, localization_note=note, decision="retention", review=dict.fromkeys(GATES, True),
                source_reference=review.source_ref(ja), current_reference=review.source_ref(en),
                installed_reference=review.source_ref(en), holds=[])
        records[key]["holds"].append(dict(capture=frames[hold], arguments=arguments, lines=lines, native_requests=[getter, copier],
            exact_body_pixels=panels.exact_body(font, lines, screens[hold]),
            exact_nameplate=panels.nameplate(font, speaker, screens[hold])))
    return list(records.values())


def transaction(font, screens, frames):
    assert 6350 - 1213 == 5137 and 2 * 2256 == 4512 and 5137 + 4512 - 2992 == 6657
    unchanged = ((33190, 35190), (34390, 36390), (41190, 41990), (41590, 42390))
    assert all(screens[a].tobytes() == screens[b].tobytes() for a, b in unchanged)
    cash = {frame: panels.find_mask(font, str(value), screens[frame], (55, 348, 139, 366))
            for frame, value in ((33190, 6350), (35190, 6350), (37190, 5137), (43190, 6657), (END, 6657))}
    charge = [panels.find_mask(font, value, screens[34390], bounds) for value, bounds in
              (("1213", (148, 329, 188, 346)), ("5137", (148, 346, 188, 365)))]
    ledger_values = {39190: (5137, 0, 0, 5137), 40390: (5137, 4512, 0, 9649), 41190: (5137, 4512, 2992, 6657),
                     41990: (5137, 4512, 2992, 6657), 43590: (6657, 0, 0, 6657)}
    ledger = {frame: market.exact_ledger(font, screens[frame], values) for frame, values in ledger_values.items()}
    goods = {frame: exact_label(screens[frame], font, text, (144, 127), (144, 126, 256, 162)) for frame, text in
             ((39190, "Iron Ore\n  Ore 94%"), (39590, "Artwork\n  Luxury 95%"), (39990, "Statues\n  Luxury 95%"),
              (43590, "Artwork\n  Luxury 96%"))}
    choices = [panels.find_mask(font, label, screens[41590], rect) for label, rect in
               (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
    after_contract = screens[37590]
    share_digit = panels.find_mask(font, "1", after_contract, (119, 126, 129, 142))
    # The town panel supplies the percent sign as a separate, wider glyph.
    region = (129, 127, 140, 140)
    white = (230, 230, 230)
    pixels = {(x, y) for x in range(region[0], region[2]) for y in range(region[1], region[3])
              if after_contract.getpixel((x, y)) == white}
    earlier_percent = {(x, y) for x in range(region[0], region[2]) for y in range(region[1], region[3])
                       if after_contract.getpixel((x, y - 28)) == white}
    assert pixels == earlier_percent and len({x for x, _ in pixels}) == 9
    share = dict(value="1%", digit=share_digit, exact_native_percent_ink_pixels=len(pixels), percent_bounds=region)
    return dict(balance_after_investing=6350, contract_payment=1213, balance_after_contract=5137,
                market_share=share, cancelled_contract_and_declined_trade_repeat_frames=unchanged,
                balances=cash, contract_amount_and_projected_funds=charge, trade_ledger=ledger,
                goods_info=goods, choices=choices, two_iron_ore_units_sold=4512,
                artwork_bought=2992, settled_balance=6657, reopened_cargo=frames[43590], return_to_town=frames[END])


def sheets(screens):
    groups = (
        ((25990, "Palace requirement"), (33590, "Minimum payment"), (33990, "Share terms"),
         (34790, "Cancel the offer"), (36790, "Trade permission"), (37590, "One percent market share")),
        ((39590, "Artwork Goods Info"), (39990, "Statues Goods Info"), (41190, "Pending mixed deal"),
         (41590, "Confirm both sides"), (42790, "Trader's farewell"), (43590, "Artwork aboard after settlement")),
    )
    results = []
    for page, group in enumerate(groups, 1):
        sheet = Image.new("RGB", (768, 808), "#263238")
        draw = ImageDraw.Draw(sheet)
        for index, (frame, title) in enumerate(group):
            x, y = index % 3 * 256, index // 3 * 404
            draw.text((x + 4, y + 4), title, fill="white")
            sheet.paste(screens[frame], (x, y + 20))
        path = OUT.with_name(f"athens_palace_contract_current_{page}_20261124.png")
        sheet.save(path)
        results.append(reference(path))
    return results


def main():
    release, frames, calls, refs, commands, source, installed, font, prior, role = inputs()
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    rows = contract_and_trade(source, installed, frames, screens, calls, font)
    role["observed_nameplates"] = [hold["exact_nameplate"] for row in rows if row["speaker"] == "Local Lord"
                                   for hold in row["holds"]]
    packet = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        ordinary_gameplay=True, comparison=prior, records=rows, role_title=role, transaction=transaction(font, screens, frames),
        original_controller_prefix=reference(play.HISTORY), additional_controller_commands=commands, evidence=refs,
        ROM_changed=False, new_editorial_credit=0, unvisited=["Alternate contract amounts", "Other market goods decisions", "Physical hardware"])
    validate_natural_dialogue_batch(packet)
    packet["review_sheets"] = sheets(screens)
    write(OUT, packet)
    print("Verified three revised Palace holds, the exact companion screens, the 1,213-gold contract and the settled Athens trade.")


if __name__ == "__main__":
    main()
