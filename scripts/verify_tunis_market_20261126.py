"""Verify Tunis's no-contract Market dialogue and the paid Syracuse price report."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.common_message_table import common_message_entries
from scripts import check_market_english_region_20261120 as region
from scripts import verify_tunis_recruitment_20261125 as review
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, write


panels, active = review.panels, review.play.current
ROOT = review.play.ROOT.with_name("tunis_market_20261126")
OUT = panels.OUT.with_name("tunis_market_current_20261126.json")
REGION_REVIEW = Path("releases/all_routes_editorial_20261120_market_english_region_candidate/verification/registered_review.json")
TRADE = "Tunis Market. The trader welcomes Hodram and refuses Trade until he has a contract at the Palace."
INVEST = "Tunis Market. The trader offers to accept an investment despite Hodram having no share. Hodram backs out of the amount selector."
INFO = "Tunis Market. Hodram opens Market Info, selects Syracuse on the map, and returns after reading its prices."
HOLDS = {
    8: ((5480,), "Trader", (), ("Need help?",), TRADE, "The trader asks what the visitor wants.",
        "The brief greeting invites a choice from the Market menu."),
    761: ((5920,), "Trader", ("Palace",), ("Sorry. Once you sign a contract", "at the Palace, come back."), TRADE,
          "The trader apologizes and asks the visitor to return after signing a contract at the named facility.",
          "The apology and referral give the player the next step, with the Palace name preserved in full."),
    762: ((6560,), "Trader", (), ("You need market share to trade.", "You still want to invest?",
          "That's generous of you.", "How much will you put in?"), INVEST,
          "The trader is surprised that the visitor wants to invest despite being unable to trade without a share, then asks how much.",
          "The short conversational beats preserve the trader's surprise and appreciative tone before opening the amount selector."),
    746: ((7000,), "Trader", (), ("Just browsing?",), INVEST, "The trader asks if the visitor was merely looking.",
          "The dry question fits the cancelled investment and leads back to the menu."),
    18: ((8320,), "Trader", (), ("There's a fee for each price check.", "Which town did you have in mind?"), INFO,
         "The trader explains that the fee is assessed each time and asks which town to look up.",
         "Both thoughts fit in complete lines. The map that follows shows the exact fee for each town, including zero for Tunis."),
}


def main():
    release = read(active.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(active.ROM) == release["candidate_sha256"]
    scope = vars(panels) | dict(observed=SimpleNamespace(ROOT=ROOT.parent))
    frames, calls, evidence = FunctionType(panels.capture.__code__, scope)(ROOT.name, release)
    assert max(frames) == 9860 and [r["message_ID"] for r in calls[::2]] == [0, 8, 761, 762, 746, 18]
    for first, second in zip(calls[::2], calls[1::2], strict=True):
        assert first["PC"] == 0x0205528C and second == first | {"PC": 0x020534F4}
    clean, current = map(NdsImage.open, (CLEAN, active.ROM))
    source_arm, arm = (image.read_file(active.ARM) for image in (clean, current))
    source = common_message_entries(clean.read_file(active.COMMON), source_arm)
    installed = panels.common_rows(current.read_file(active.COMMON), arm)
    font = GameAsciiFont.from_arm9(arm)
    screens = {n: panels.picture(row) for n, row in frames.items()}
    records, figures = review.review_common_holds(HOLDS, source, installed, font, frames, screens, calls)
    wallets = {frame: panels.find_mask(font, str(gold), screens[frame], (60, 346, 138, 366))
               for frame, gold in ((4200, 7056), (6140, 7056), (7660, 7056), (9640, 6856), (9860, 6856))}
    assert all(wallets.values())
    title = panels.find_mask(font, "Italy Region", screens[9200], region.BOX)
    assert title
    prior, = [row for row in read(REGION_REVIEW)["records"] if row["english"] == "Italy Region"]
    field = prior["source_reference"]["pointer_field_offset"]
    assert region.string(source_arm, field) == prior["source_reference"]
    assert region.string(arm, field) == prior["target_reference"]
    records.append(prior | dict(context=INFO, current_reference=prior["target_reference"],
        installed_reference=prior["target_reference"], decision="retention",
        observations=[dict(capture=frames[9200], heading_mask=title)]))
    batch = dict(translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=list(GATES), records=records, candidate_sha256=release["candidate_sha256"], ordinary_gameplay=True,
        evidence=evidence, native_requests=calls, wallets=wallets,
        quoted_local_report=dict(port="Tunis", coins=0, capture=frames[8540]),
        paid_report=dict(port="Syracuse", coins=200, picker=frames[8980], report=frames[9200], wallet_after=6856),
        controller_commands=[r["command"] for r in read(evidence["journal"]["path"])["commands_received"]],
        unvisited=["Contract-enabled Tunis Deal screen", "Paying for a Tunis investment", "Other Price Info regions"],
        ROM_changed=False, new_editorial_credit=0)
    validate_natural_dialogue_batch(batch)
    sheets = panels.sheets_for("tunis_market_dialogue_20261126", figures)
    sheets += panels.sheets_for("tunis_market_price_report_20261126", [
        ("Tunis / 0 coins", screens[8540]), ("Syracuse / 200 coins", screens[8980]),
        ("Returned to Market / 6,856 gold", screens[9640]),
    ], crop=(0, 192, 256, 384))
    sheets += panels.sheets_for("tunis_market_price_report_20261126_view", [
        ("Syracuse Price Info / Italy Region", screens[9200]),
    ], crop=(0, 0, 256, 192))
    write(OUT, batch | {"figures": sheets})
    print("Verified five Tunis market messages, the Italy Region label and the 200-gold deduction.")


if __name__ == "__main__":
    main()
