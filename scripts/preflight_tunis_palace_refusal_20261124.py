"""Review Palace and Market exchanges and preflight the Guard's revised refusal."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_market_english_region_20261120 as region
from scripts import observe_tunis_market_and_palace_20261124 as played
from scripts import preflight_nagasaki_contract_wrap_20261124 as palace
from scripts import stage_square_trend_dialogue_20261115 as trend
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_trade_good_descriptions_v1 import exact_title


OUT = panels.OUT.with_name("tunis_palace_refusal_preflight_20261124.json")
KEY = 1148
END = 17000
DRAFT = "Too bad. This city has no room for another faction."
REVISED_HOLDS = (13400, 16200)
HISTORICAL_REGION = Path("releases/all_routes_editorial_20261120_market_english_region_candidate/verification/registered_review.json")
HOLDS = {
    5400: (8, "Trader", (), ("Need help?",)),
    6200: (761, "Trader", ("Palace",), ("Sorry. Please sign a contract", "at the Palace, then come back.")),
    7400: (18, "Trader", (), ("There's a fee for each price check.", "Which town did you have in mind?")),
    11400: (761, "Trader", ("Palace",), ("Sorry. Please sign a contract", "at the Palace, then come back.")),
    13400: (KEY, "Guard", (), ("Unfortunately, there's no room", "for another faction to trade", "in this city.")),
    14600: (1151, "King", ("Bergstrom",), ("Ah, Bergstrom! It's generous of you", "to help defend this city when you",
                                         "don't even have a trading", "contract here.")),
    15400: (1160, "King", (), ("Hmm. That's an admirable gesture.", "Very commendable.")),
    16200: (KEY, "Guard", (), ("Unfortunately, there's no room", "for another faction to trade", "in this city.")),
}
REVIEW = {
    8: ("Trader", "The trader asks what the visitor needs.", "The brief welcome leads naturally to the service menu."),
    18: ("Trader", "The price-check fee is assessed per lookup. The trader asks which town to check.",
         "The fee and the question each get a complete line. The local town can still show a zero fee."),
    761: ("Trader", "The trader apologizes and asks the player to get a contract at the named building before returning.",
          "The apology and courteous referral keep the trade restriction clear and give the player the next step."),
    1146: ("Guard", "Existing contracts with several factions leave no opening for another.",
           "The explicit plural contracts explain this separate refusal. Confirmed original alternate source from the Palace ledger."),
    1147: ("Guard", "The town has an exclusive contract with the named faction and cannot contract with others.",
           "The corporate name and exclusive terms remain explicit in this alternate refusal."),
    KEY: ("Guard", "The guard says it is too bad that there is no room for another faction to enter this city.",
          "Too bad keeps the curt opening. The following sentence explains the refusal in two natural rows without stranding the location."),
    1151: ("King", "The ruler is surprised and pleased that the visitor offers to defend the city despite having no trading contract.",
           "Generous expresses the gratitude, and even preserves the ruler's surprise. The captain's family name stays in the greeting."),
    1160: ("King", "The ruler praises the generous gesture.",
           "The formal repetition suits a ruler acknowledging a payment and retains the emphasis of the Japanese."),
}


def ordinary_gameplay(release, font):
    scope = vars(panels) | {"observed": SimpleNamespace(ROOT=played.ROOT.parent)}
    frames, calls, evidence = FunctionType(panels.capture.__code__, scope)(played.ROOT.name, release)
    assert max(frames) == END
    expected = (0, 8, 761, 18, 761, KEY, 1151, 1160, KEY)
    assert tuple(row["message_ID"] for row in calls[::2]) == expected
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    holds = []
    for frame, (key, speaker, args, lines) in HOLDS.items():
        first, second = [row for row in calls if row["message_ID"] == key and 0 < frame - row["frame"] < 400]
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
        screen = screens[frame]
        holds.append(dict(frame=frame, message_ID=key, speaker=speaker, args=args, lines=lines,
            capture=frames[frame], exact_body_ink=panels.exact_body(font, lines, screen),
            nameplate=panels.nameplate(font, speaker, screen), requests=[first, second]))
    money = []
    for frame, coins in ((4200, 7056), (5800, 7056), (10600, 7056), (13000, 7056), (15800, 5706), (END, 5706)):
        mask = panels.find_mask(font, str(coins), screens[frame], (34, 346, 138, 366))
        money.append(dict(frame=frame, coins=coins, mask=mask))
    amount = panels.find_mask(font, "1350", screens[15000], (152, 324, 198, 346))
    heading = panels.find_mask(font, "Egypt Region", screens[8600], region.BOX)
    goods = exact_title(font, "Carpets", screens[9400])
    city = panels.find_mask(font, "Tunis", screens[END], (12, 14, 146, 32))
    return dict(holds=holds, route=evidence, money=money, military_investment_picker=amount,
        region_heading=heading, goods_title=goods, return_to_town=city,
        price_report_used_local_town=True, military_investment_charged=1350)


def main():
    release = read(played.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    runtime = trend.RegisteredRuntime(played.RELEASE, release["own_registered_startup"], captain=3)
    clean = NdsImage.open(CLEAN)
    ja_arm = clean.read_file(trend.ARM)
    arm, common = runtime.arm, runtime.common
    assert trend.digest(arm) == release["target_ARM9_sha256"] and trend.digest(common) == release["target_COMMON_sha256"]
    source = trend.common_message_entries(clean.read_file(trend.COMMON), ja_arm)
    current = trend.owned_entries(common, arm, trend.digest(arm[trend.DIRECTORY_OFFSET:trend.TABLE_OFFSET]))
    assert source[KEY].text.decode("cp932").startswith("残念だったな") and b"%" not in source[KEY].text + current[KEY].text
    font = GameAsciiFont.from_arm9(arm)
    live = ordinary_gameplay(release, font)
    for hold in live["holds"]:
        key, args = hold["message_ID"], hold["args"]
        stored = current[key].text
        assert source[key].text.count(b"%s") == stored.count(b"%s") == len(args)
        assert (stored % tuple(arg.encode("ascii") for arg in args)).decode("ascii").split() == " ".join(hold["lines"]).split()
    region_review = next(row for row in read(HISTORICAL_REGION)["records"] if row["english"] == "Egypt Region")
    field = region_review["source_reference"]["pointer_field_offset"]
    assert region.string(ja_arm, field) == region_review["source_reference"] and region.string(arm, field) == region_review["target_reference"]

    revised = (" " + DRAFT).encode("ascii").ljust(len(current[KEY].text), b" ")
    assert len(revised) == len(current[KEY].text) and revised.isascii()
    target, installed, allocations = trend.owned_deployment(common, arm, current, {KEY: revised})
    assert [a.message_id for a, b in zip(current, installed, strict=True) if a != b] == [KEY]
    historical = {row["message_id"]: row for row in read(palace.BINDINGS)["records"]}
    original = historical[KEY]
    assert original["native_binding"]["parent"] == 0x02054014 and original["native_binding"]["table_or_ID"] == 0
    cpu, get, provider = trend.with_components(runtime, arm, target).machine(arm, target, runtime.raw, runtime.plan)
    address = get(0x5528C, KEY)
    assert bytes(cpu.mem_read(address, len(revised) + 1)) == revised + b"\0" and provider.reads
    layout = palace.native_format()
    painter, _, _ = trend.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    cases, figures = [], []
    for label, payload in (("Current", current[KEY].text), ("Proposed", revised)):
        row = dict(message_id=KEY, native_binding=original["native_binding"], english=payload[1:].decode("ascii"),
                   English_argument_source_indices=[])
        formatted = layout(cpu, row, ())
        raw = bytes.fromhex(formatted["formatted_hex"])
        plane, glyphs = trend.render_portrait(painter, arm, kanji, raw)
        expected = (ord("U"), ord(".")) if label == "Current" else (ord("T"), ord("."))
        assert (glyphs[0]["code"], glyphs[-1]["code"]) == expected and len(plane) == 228 * 64
        assert not formatted["findings"]
        cases.append(dict(label=label, layout=formatted, native_plane_sha256=trend.digest(plane)))
        figures.append((label, plane))
    assert cases[0]["layout"]["lines"] == list(HOLDS[13400][3])
    assert cases[1]["layout"]["lines"] == ["Too bad. This city has no room", "for another faction."]
    root = OUT.with_suffix("")
    root.mkdir(parents=True, exist_ok=True)
    sheets = trend.portrait_sheets(root, figures)
    records = []
    for key, (speaker, meaning, reason) in REVIEW.items():
        is_live = any(row["message_ID"] == key for row in live["holds"])
        records.append(dict(id=f"COMMON_MESSAGE_{key}", message_id=key, message_ID=key, speaker=speaker, file_path=trend.COMMON,
            context="The trader and Palace speak about market access, the selected price report, or the optional military investment.",
            source_meaning=meaning, localization_note=reason, decision="revision" if key == KEY else "retention",
            english=" ".join(installed[key].text.decode("ascii").split()), Japanese=source[key].text.decode("cp932"),
            source_reference=panels.text_reference(source[key]), current_reference=panels.text_reference(current[key]),
            proposed_reference=panels.text_reference(installed[key]),
            source_hex=source[key].text.hex(), current_hex=current[key].text.hex(), proposed_hex=installed[key].text.hex(),
            ordinary_gameplay_observed=is_live, review=dict.fromkeys(GATES, True)))
    manuscript = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", records=records,
                      encoder="dialogue-relocatable-v1", review_gates=list(GATES))
    validate_natural_dialogue_batch(manuscript)
    write(OUT, manuscript | dict(candidate_sha256=release["candidate_sha256"], source_sha256=release["clean_input_sha256"],
        unchanged_ARM9_sha256=trend.digest(arm), proposed_COMMON_sha256=trend.digest(target), allocation=allocations[KEY],
        native_cases=cases, proposed_sheets=sheets, ordinary_gameplay=live,
        inherited_source_and_consumer=reference(palace.BINDINGS), market_region_review=reference(HISTORICAL_REGION),
        ROM_changed=False, new_editorial_credit=0))
    print("Verified eight ordinary portrait holds and the proposed two-line Guard refusal.")


if __name__ == "__main__":
    main()
