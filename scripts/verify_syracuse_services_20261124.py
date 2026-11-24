"""Verify the ordinary Syracuse contract and two answers to the cargo sale."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import observe_syracuse_services_20261124 as play
from scripts import verify_genoa_copenhagen_town_20261123 as panels
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_azores_wording_20261123 import ARM, COMMON
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_commodity_private_market_live_v354 import exact_label


OUT = panels.OUT.with_name("syracuse_contract_and_trade_20261124.json")
DONOR = Path("E:/Rota Nova translations/Saves/hodram-syracuse-full-hull-lookout-v474.dsv")
END = 16500
HOLDS = ((6100, 1156), (6500, 1157), (7300, 1158), (8100, 1156), (8500, 1157), (9300, 1159),
         (10900, 8), (14500, 11), (15300, 11), (15700, 9))
REVIEW = {
    1156: ("King", ("1458",), ("You'd like to trade here? Hmm...", "Very well. The minimum contract fee", "is 1458 gold coins."),
           "The king considers the request, permits negotiations, and states the minimum payment in gold.",
           "The pauses and short assent suit the king's measured speech. The exact fee and its status as the minimum stay explicit."),
    1157: ("King", (), ("Your fee sets your market share.", "How much will you offer?"),
           "The king offers a share proportional to the payment and asks what the visitor will pay.",
           "The separate lines distinguish the rule from the decision and keep the question whole."),
    1158: ("King", (), ("Bah! Make up your mind.",),
           "The exasperated king calls the visitor indecisive.",
           "The abrupt interjection and imperative preserve his impatience after the player cancels."),
    1159: ("King", (), ("Very well. You may trade", "in this city."),
           "The king grants permission to trade in this city.",
           "The formal assent closes the negotiation. The native wrap keeps the entire location phrase together."),
    8: ("Trader", (), ("Need help?",),
        "The trader asks what the visitor needs.",
        "A brief welcome gives the player the floor before the newly available Trade option."),
    11: ("Charles Rochefort", (), ("Will this be all right?",),
         "The crew member politely asks if the player approves.",
         "The deferential question suits Charles and leaves both answers open. The original Yes and No choices stay visible."),
    9: ("Trader", (), ("Thanks! Come again.",),
        "The trader thanks the customer and invites a return.",
        "The brief farewell follows settlement and acknowledges the completed sale without adding a promise."),
}


def dialogue(source, installed, frames, calls, screens, font):
    records = {}
    assert len(calls) == 2 * len(HOLDS)
    for (frame, key), (getter, copier) in zip(HOLDS, zip(calls[::2], calls[1::2], strict=True), strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["message_ID"] == key and 0 < frame - getter["frame"] < 400
        ja, en = source[key], installed[key]
        speaker, arguments, lines, meaning, rationale = REVIEW[key]
        english = en.text.decode("ascii").strip()
        assert en.text and ja.text.count(b"%s") == en.text.count(b"%s") == len(arguments)
        assert (english % arguments).split() == " ".join(lines).split()
        observed = dict(frame=frame, capture=frames[frame], native_lines=lines, arguments=arguments,
                        body_pixels=panels.exact_body(font, lines, screens[frame]),
                        nameplate=panels.nameplate(font, speaker, screens[frame]), requests=[getter, copier])
        if key not in records:
            current = panels.text_reference(en) | dict(exact_hex=en.text.hex())
            context = ("The Palace exchange covers the contract offer and both outcomes."
                       if key >= 1156 else "The newly authorized Market exchange covers a cargo sale and both confirmation outcomes.")
            records[key] = dict(id=f"COMMON_MESSAGE_{key}", file_path=COMMON, message_ID=key,
                clean_Japanese=ja.text.decode("cp932"), source_reference=panels.text_reference(ja) | dict(exact_hex=ja.text.hex()),
                current_reference=current, installed_reference=current, english=english, speaker=speaker, context=context,
                source_meaning=meaning, localization_note=rationale, decision="retention",
                review=dict.fromkeys(GATES, True), holds=[])
        records[key]["holds"].append(observed)
    return list(records.values())


def market(screens, font):
    boxes = {
        14100: ("36913", "3578", "0", "40491"),
        14900: ("36913", "3578", "0", "40491"),
    }
    masks = {frame: [panels.find_mask(font, text, screens[frame], (62, y, 117, y + 14))
                     for y, text in zip((36, 52, 68, 84), values, strict=True)]
             for frame, values in boxes.items()}
    goods = {}
    for frame, pane, text in ((11700, "Cargo", "Iron Ore\n  Ore 71%"), (12100, "Local", "Wheat\n  Food 97%")):
        goods[pane] = exact_label(screens[frame], font, text, (144, 127), (144, 126, 256, 162))
    choices = {frame: [panels.find_mask(font, label, screens[frame], rect) for label, rect in
                        (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
               for frame in (14500, 15300)}
    return dict(ledger=masks, goods_info=goods, choices=choices,
                sale_proceeds=3578, scene="No kept the pending sale. Yes completed it.")


def main(output_dir=OUT.parent):
    release = read(play.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=play.ROOT.parent))
    frames, calls, evidence = FunctionType(panels.capture.__code__, scope)(play.ROOT.name, release)
    assert max(frames) == END and digest(DONOR) == evidence["donor"]["sha256"]
    screens = {frame: panels.picture(shot) for frame, shot in frames.items()}
    clean, installed = map(NdsImage.open, (CLEAN, release["candidate"]))
    before, arm = clean.read_file(ARM), installed.read_file(ARM)
    archive = installed.read_file(COMMON)
    assert panels.sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert panels.sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(COMMON), before)
    current = common_rows(archive, arm)
    font = GameAsciiFont.from_arm9(arm)
    del clean, installed
    rows = dialogue(source, current, frames, calls, screens, font)
    market_proof = market(screens, font)
    wallet = {frame: panels.find_mask(font, text, screens[frame], (55, 348, 139, 366)) for frame, text in
              ((4900, "38371"), (7700, "38371"), (9700, "36913"), (END, "40491"))}
    quote = panels.find_mask(font, "1458", screens[6900], (150, 328, 190, 347))
    share = dict(observed="1%", frame=9700, capture=frames[9700])
    city = panels.find_mask(font, "Syracuse", screens[END], (32, 14, 140, 31))
    assert 38371 - 1458 == 36913 and 36913 + market_proof["sale_proceeds"] == 40491
    archived = {284, 318, 750, 751, 752}
    assert archived.isdisjoint(row["message_ID"] for row in calls)
    output = output_dir / OUT.name
    draw = FunctionType(panels.sheets_for.__code__, vars(panels) | dict(OUT=output),
                        argdefs=panels.sheets_for.__defaults__)
    selected = ((6100, "Minimum fee"), (6500, "Market share terms"), (7300, "Contract canceled"),
                (9300, "Permission granted"), (10900, "Market welcome"), (14500, "Sale confirmation"),
                (15300, "Sale confirmed again"), (15700, "Sale completed"))
    sheets = draw("syracuse_contract_and_sale", [(label, screens[frame]) for frame, label in selected])
    sheets.extend(draw("syracuse_local_and_cargo", [("Cargo Iron Ore", screens[11700]),
                       ("Local Wheat", screens[12100]), ("Contract granted 1% share", screens[9700]),
                       ("Return to town", screens[END])], crop=(0, 80, 256, 192)))
    for sheet in sheets:
        sheet["path"] = (OUT.parent / Path(sheet["path"]).name).as_posix()
    result = dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(GATES), records=rows, candidate_sha256=release["candidate_sha256"], release=reference(play.RELEASE),
        clean_rom_sha256=release["clean_input_sha256"], original_donor=reference(DONOR), capture_evidence=evidence,
        route="Ordinary game controls from a byte-exact existing Syracuse battery save", original_requests=calls,
        market=market_proof, palace=dict(minimum_contract_amount=quote, fee_paid=1458, earned_trade_share=share, wallet=wallet),
        return_to_town=city, visual_sheets=sheets, archived_messages_unobserved=sorted(archived),
        unvisited=["Completed Local purchase", "Other conditional Market and Palace outcomes", "Handheld play"],
        ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(result)
    write(output, result)
    print(f"Verified {len(rows)} retained records in {len(HOLDS)} held pages and both sale answers.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUT.parent)
    main(parser.parse_args().output_dir)
