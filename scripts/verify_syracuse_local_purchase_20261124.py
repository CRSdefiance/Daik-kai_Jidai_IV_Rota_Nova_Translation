"""Verify the Syracuse zero deal, sale, and local purchase on the Maria build."""

from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageDraw

from scripts import observe_syracuse_local_purchase_20261124 as play
from scripts import verify_syracuse_services_20261124 as prior


ROOT = play.ROOT.with_name("syracuse_receipt_and_purchase_20261124")
OUT = prior.OUT.with_name("syracuse_local_purchase_20261124.json")
SHEET = OUT.with_suffix(".png")
END = 20100
HOLDS = (*prior.HOLDS[:7], (12900, 746), (14900, 11), (15300, 9),
         (18100, 11), (18900, 11), (19300, 9))
REVIEWS = prior.REVIEW | {
    746: ("Trader", (), ("Just browsing?",),
          "The merchant pauses and asks whether the visitor was only looking.",
          "The short question carries the merchant's mild disappointment when Finish closes an empty deal."),
    11: ("Charles Rochefort", (), ("Will this be all right?",),
         "Charles politely asks whether the player approves the deal.",
         "The deferential question suits Charles and applies naturally to both a sale and a purchase."),
    9: ("Trader", (), ("Thanks! Come again.",),
        "The trader thanks the customer and invites them to return.",
        "The short farewell suits the same trader after either successful transaction."),
}
FRAMES = ((12900, "Finish with an empty deal"), (14900, "Confirm the Iron Ore sale"),
          (15700, "Market after the sale"), (17700, "Wheat staged in Cargo"),
          (18100, "Confirm the Wheat purchase"), (18500, "No keeps the pending purchase"),
          (19300, "Yes settles the purchase"), (20100, "Return to Syracuse"))


def exact_ledger(font, screen, values):
    return [prior.panels.find_mask(font, str(value), screen, (62, y, 117, y + 14))
            for y, value in zip((36, 52, 68, 84), values, strict=True)]


def main():
    release = prior.read(play.active.RELEASE)
    assert prior.digest(prior.REGISTRY) == release["registry_sha256"]
    assert prior.digest(prior.CLEAN) == release["clean_input_sha256"]
    assert prior.digest(release["candidate"]) == release["candidate_sha256"]
    capture = FunctionType(prior.panels.capture.__code__,
                           vars(prior.panels) | dict(observed=SimpleNamespace(ROOT=ROOT.parent)))
    frames, calls, evidence = capture(ROOT.name, release)
    assert max(frames) == END and prior.digest(prior.DONOR) == evidence["donor"]["sha256"]
    screens = {frame: prior.panels.picture(shot) for frame, shot in frames.items()}

    clean, active = map(prior.NdsImage.open, (prior.CLEAN, release["candidate"]))
    arm, archive = active.read_file(prior.ARM), active.read_file(prior.COMMON)
    assert prior.panels.sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert prior.panels.sha256(archive).hexdigest() == release["target_COMMON_sha256"]
    clean_rows = prior.common_message_entries(clean.read_file(prior.COMMON), clean.read_file(prior.ARM))
    installed_rows = prior.common_rows(archive, arm)
    del clean, active
    font = prior.GameAsciiFont.from_arm9(arm)
    dialogue = FunctionType(prior.dialogue.__code__, vars(prior) | dict(HOLDS=HOLDS, REVIEW=REVIEWS))
    selected = dialogue(clean_rows, installed_rows, frames, calls, screens, font)
    for row in selected:
        if row["message_ID"] < 1156:
            row["context"] = ("After the Palace contract, the Trader handles an empty deal and the completed "
                              "transactions while Charles asks for approval before settlement.")
    archived = {284, 318, 750, 751, 752}
    assert archived.isdisjoint(row["message_ID"] for row in calls)
    for entry in selected:
        assert all(entry["review"].values())

    ledger = {frame: exact_ledger(font, screens[frame], amounts) for frame, amounts in {
        12500: (36913, 0, 0, 36913), 14900: (36913, 1789, 0, 38702),
        17700: (38702, 0, 442, 38260), 18100: (38702, 0, 442, 38260),
        18500: (38702, 0, 442, 38260), 18900: (38702, 0, 442, 38260),
    }.items()}
    wallet = {frame: prior.panels.find_mask(font, total, screens[frame], (55, 348, 139, 366))
              for frame, total in ((13300, "36913"), (15700, "38702"),
                                   (19700, "38260"), (END, "38260"))}
    assert 36913 + 1789 == 38702 and 38702 - 442 == 38260
    choices = {frame: [prior.panels.find_mask(font, label, screens[frame], box) for label, box in
                      (("No", (118, 360, 165, 376)), ("Yes", (188, 360, 235, 376)))]
               for frame in (14900, 18100, 18900)}
    wheat = {frame: prior.exact_label(screens[frame], font, "Wheat\n  Food 97%",
                                    (144, 127), (144, 126, 256, 162))
             for frame in (17700, 18500)}
    wheat_slot = (119, 236, 139, 254)
    crop = {frame: screens[frame].crop(wheat_slot).tobytes() for frame in (17300, 17700, 18500, 19300)}
    assert crop[17300] != crop[17700] == crop[18500] == crop[19300]
    town = prior.panels.find_mask(font, "Syracuse", screens[END], (32, 14, 140, 31))

    sheet = Image.new("RGB", (768, 1212), "#263238")
    labels = ImageDraw.Draw(sheet)
    for index, (frame, title) in enumerate(FRAMES):
        x, y = index % 3 * 256, index // 3 * 404
        labels.text((x + 3, y + 3), title, fill="white")
        sheet.paste(screens[frame], (x, y + 20))
    sheet.save(SHEET)
    result = dict(
        translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
        review_gates=list(prior.GATES), records=selected,
        method="Ordinary controls from the byte-exact Syracuse battery save. No memory or state edits.",
        release=prior.reference(play.active.RELEASE), candidate_sha256=release["candidate_sha256"],
        clean_rom_sha256=release["clean_input_sha256"], evidence=evidence, requests=calls,
        ledger=ledger, wallet=wallet, choices=choices, wheat_goods_info=wheat, return_to_town=town,
        held_wheat=dict(region=wheat_slot, retained_after_no_and_settlement=True),
        contact_sheet=prior.reference(SHEET), archived_messages_unobserved=sorted(archived),
        unvisited=["Purchase bargaining", "Other conditional Market responses", "Physical hardware"],
        ROM_changed=False, new_editorial_credit=0,
    )
    prior.validate_natural_dialogue_batch(result)
    prior.write(OUT, result)
    print(f"Verified {len(selected)} retained records in {len(HOLDS)} holds and a 442-gold purchase.")


if __name__ == "__main__":
    main()
