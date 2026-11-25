"""Verify the ordinary Azores buy, sell, decline, and town return."""

from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_azores_trade_20261125 as play
from scripts import verify_riga_trade_deck_20261124 as review
from scripts import verify_seoul_tavern_decline_20261123 as live
from scripts import verify_syracuse_local_purchase_20261124 as market
from scripts.stage_azores_wording_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = review.OUT.with_name("azores_trade_current_20261125.json")
PANELS = review.panels
HOLDS = {
    746: ((15590,), "Trader", "Just browsing?", "The trader asks if the visitor was only window-shopping.",
          "The short question keeps the trader's mild disappointment when the player finishes an empty deal."),
    8: ((16400,), "Trader", "Need help?", "The trader asks if the visitor needs anything.",
        "The brief greeting fits the return visit and lets Hodram choose the single service."),
    17: ((18560, 19100), "Manuel Almeida", "Does this look all right?",
         "Manuel politely asks the captain if the proposed deal is acceptable.",
         "The unhurried question suits Manuel and invites approval of the purchase and sales together."),
    9: ((19370,), "Trader", "Thanks! Come again.", "The trader thanks the customer and asks for future business.",
        "The familiar farewell sounds natural at settlement and matches the trader's brisk greeting."),
}
BEFORE, SALE, COST, SETTLED = 39333, 4200, 377, 43156
PENDING = (BEFORE, SALE, COST, SETTLED)
KEEP = ((15050, "Full cargo, Wine selected"), (15590, "Finish an empty deal"), (15860, "Trade-only menu"),
        (18020, "Sell both Iron Ore lots"), (18290, "Wine staged in cargo"), (18560, "Confirm the mixed deal"),
        (18830, "No keeps both entries"), (19370, "Yes settles the deal"), (19910, "Wine aboard after reopening"),
        (20450, "Return to the Azores"))


def item_name(clean, installed):
    slot, base = 0x0215F464, 0x02000000
    result = []
    for data, address, text in ((clean, 0x0215CB78, "鷹の島の酒"), (installed, 0x0215C890, "Azores Wine")):
        assert unpack_from("<I", data, slot - base) == (address,)
        encoded = text.encode("cp932") + b"\0"
        at = address - base
        assert data[at:at + len(encoded)] == encoded
        result.append(dict(name=text, pointer_field=slot, address=address, exact_hex=encoded.hex()))
    return dict(commodity_index=113, source=result[0], current=result[1], installed=result[1], decision="retention",
                context="The village's own drink is selected as a purchase and then displayed in the ship's cargo.",
                localization_note="The established name ties the drink to the town whose specialty it is and fits both Trade displays.",
                review=dict.fromkeys(GATES, True))


def held_dialogue(source, installed, frames, screens, trace, snapshots, font):
    rows, used = [], []
    for key, (holds, speaker, text, meaning, reason) in HOLDS.items():
        ja, en = source[key], installed[key]
        assert b"%" not in ja.text + en.text and en.text.decode("ascii").strip() == text
        samples = []
        for frame in holds:
            native = live.read_ram(snapshots[frame])
            assert live.text_at(native, unpack_from("<I", native, 0x54450)[0]).decode("ascii").strip() == text
            read_call, copy_call = [r for r in trace if r["message_ID"] == key and 0 < frame - r["frame"] < 270]
            assert read_call["PC"] == 0x0205528C and copy_call == read_call | {"PC": 0x020534F4}
            used.extend((read_call, copy_call))
            samples.append(dict(frame=frames[frame], native_requests=[read_call, copy_call],
                                complete_body=PANELS.exact_body(font, (text,), screens[frame]),
                                complete_nameplate=PANELS.nameplate(font, speaker, screens[frame])))
        rows.append(dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, file_path=play.current.COMMON, speaker=speaker,
                         context="Hodram uses the developed Azores Market. An empty deal precedes the wine purchase and Iron Ore sale.",
                         clean_Japanese=ja.text.decode("cp932"), english=text, source_meaning=meaning, localization_note=reason,
                         source_reference=review.source_ref(ja), current_reference=review.source_ref(en),
                         installed_reference=review.source_ref(en), decision="retention",
                         review=dict.fromkeys(GATES, True), observations=samples))
    assert sorted(used, key=lambda event: event["frame"]) == trace
    return rows


def make_sheets(screens):
    paths = []
    for start in range(0, len(KEEP), 6):
        cells = KEEP[start:start + 6]
        image = Image.new("RGB", (768, 404 * ((len(cells) + 2) // 3)), "#263238")
        captions = ImageDraw.Draw(image)
        for index, (frame, label) in enumerate(cells):
            x, y = 256 * (index % 3), 404 * (index // 3)
            captions.text((x + 4, y + 4), label, fill="white")
            image.paste(screens[frame], (x, y + 20))
        path = OUT.with_name(f"azores_trade_current_{start // 6 + 1}_20261125.png")
        image.save(path)
        paths.append(reference(path))
    return paths


def main():
    release = read(play.current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(play.current.ROM) == release["candidate_sha256"]
    scope = vars(PANELS) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, evidence = FunctionType(PANELS.capture.__code__, scope)(play.ROOT.name, release)
    run = read(evidence["capture"]["path"])
    baseline = read(play.HISTORY)
    assert digest(play.HISTORY) == play.VISIT_SHA
    prefix = [r for r in baseline["scripted_input_schedule"] if r["start"] <= play.FIRST_PAUSE]
    assert run["scripted_input_schedule"][:len(prefix)] == prefix
    assert max(frames) == 20450 and evidence["donor"]["sha256"] == baseline["battery_save_preloaded"]["source_sha256"]
    screens = {frame: PANELS.picture(shot) for frame, shot in frames.items()}
    first = PANELS.shots(baseline, "_navigation.png")[play.FIRST_PAUSE]
    assert frames[play.FIRST_PAUSE]["framebuffer_sha256"] == first["framebuffer_sha256"]

    original, image = (NdsImage.open(path) for path in (CLEAN, play.current.ROM))
    arm, archive = (image.read_file(file) for file in (play.current.ARM, play.current.COMMON))
    clean_arm = original.read_file(play.current.ARM)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = common_message_entries(original.read_file(play.current.COMMON), clean_arm)
    installed = common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)
    snapshot = {r["frame"]: r for r in run["read_only_pause_RAM_snapshots"]}
    encountered = [r for r in calls if r["frame"] > play.FIRST_PAUSE]
    assert {284, 318, 750, 751, 752}.isdisjoint(r["message_ID"] for r in calls)
    records = held_dialogue(source, installed, frames, screens, encountered, snapshot, font)
    figures = {
        15050: (BEFORE, 0, 0, BEFORE), 15320: (BEFORE, 0, 0, BEFORE), 16940: (BEFORE, 0, 0, BEFORE),
        18020: (BEFORE, SALE, 0, BEFORE + SALE), 18290: PENDING, 18560: PENDING, 18830: PENDING, 19100: PENDING,
        19910: (SETTLED, 0, 0, SETTLED),
    }
    assert BEFORE + SALE - COST == SETTLED
    ledgers = {frame: market.exact_ledger(font, screens[frame], amounts) for frame, amounts in figures.items()}
    cash = {frame: live.cash_state(arm, snapshot[frame])[-1] for frame in (15050, 15860, 18830, 19640, 20180, 20450)}
    assert list(cash.values()) == [BEFORE, BEFORE, BEFORE, SETTLED, SETTLED, SETTLED]
    masks = {frame: market.prior.exact_label(screens[frame], font, f"Azores Wine\n  Liquor {rate}%",
                                            (144, 127), (144, 126, 256, 162))
             for frame, rate in ((15050, 100), (18020, 100), (18290, 100), (18830, 100), (19910, 101))}
    choices = {frame: [PANELS.find_mask(font, label, screens[frame], box) for label, box in
                       (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))] for frame in (18560, 19100)}
    # Compare the commodity's icon interior, clear of cursor and grade numerals.
    crops = [screens[frame].crop((89, 237, 103, 250)).tobytes() for frame in (18020, 18290, 18830, 19910)]
    assert crops[0] != crops[1] == crops[2] == crops[3]
    town = PANELS.find_mask(font, "Azores", screens[20450], (33, 13, 143, 31))
    proof = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
                 review_gates=list(GATES), candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
                 exact_previous_deal_frame=True, evidence=evidence, source_gameplay_prefix=reference(play.HISTORY),
                 context="Ordinary controls on a byte-exact Lisbon save sail to the Azores and complete a village trade.",
                 records=records, azores_wine=item_name(clean_arm, arm), exact_goods_info=masks, choice_glyphs=choices,
                 prices=dict(iron_ore_sales=SALE, azores_wine_purchase=COST, wallet_before=BEFORE, wallet_after=SETTLED),
                 exact_ledger_masks=ledgers, exact_wallets=cash, wine_icon_persists=True, return_to_town=town,
                 contact_sheets=make_sheets(screens), frames={frame: frames[frame] for frame, _ in KEEP},
                 archived_messages_unobserved=[284, 318, 750, 751, 752],
                 unvisited=["Other villages and transaction variants", "Other archived-message routes", "Physical hardware"],
                 ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(proof)
    write(OUT, proof)
    print("Verified five Azores dialogue holds, nine exact ledgers, and the settled cargo and wallet.")


if __name__ == "__main__":
    main()
