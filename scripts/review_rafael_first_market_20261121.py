"""Review both branches of Rafael's first Market lesson against clean Japanese."""
from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import stage_london_guild_assignments_20261118 as planner
from scripts import register_rafael_harbor_exchange_20261121 as parent
from scripts import verify_rafael_preparation_gameplay_20261121 as replay
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("out/rafael_first_market_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/rafael_first_market_20261121_v2.json")
PREVIOUS = Path("releases/all_routes_editorial_20261119_story_market_terms_candidate/verification/registered_review.json")
BLOCKS = ((137,), (), (), ())
CONTEXT = ("Julio teaches Rafael about routes, cargo capacity and market share. Rafael can ask how to increase his share. Julio then returns to the immediate task and sends the player into the Trade screen.",) * 4
FRAMES = {6: 37355, 9: 37615, 13: 37875, 16: 38135, 19: 38395, 22: 38655,
          26: 38915, 30: 39175, 44: 39695, 48: 39955, 52: 40215, 60: 40475}
MENU = 39435
EDITS = {
    6: ("Buy low, sell high. That's how trading works.",
        ("Buy low, sell high.", "That's how trading works."),
        "Keep the familiar maxim and give Julio's conversational explanation a full line."),
    16: ("Check each town's prices. See if you can turn a big profit.",
         ("each town's prices.", "See if you can turn a big profit."),
         "The clean line suggests trying for a large profit. Keep the town-by-town comparison and the invitation to try."),
    19: (None, ("saffron or almonds", "selling them in Ceuta."),
         "Both Lisbon goods and the example sale in Ceuta are clearly stated. Keep the two goods together."),
    26: (None, ("one cargo hold.", "how much you can buy."),
         "The existing wording defines one unit before explaining capacity. Keep the unit's name together."),
    30: (None, ("Market share", "how much you can trade at once.", "The greater your share,", "the more you can trade."),
         "Keep the existing comparison and the term Rafael can ask about. Keep each half of the comparison intact."),
    48: ("If there's unclaimed market share, you can earn some by investing at the Palace or the Market.",
         ("If there's unclaimed market share,", "at the Palace or the Market."),
         "Preserve the availability condition and both menu labels. Keep the condition's key phrase together."),
    52: (None, ("Don't worry about that just yet.", "made some money", "have more ships.", "First, give trading a try."),
         "Keep both reasons to wait and Julio's practical encouragement. The final invitation is a separate thought."),
}


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__, vars(pairing) | globals())()
    packet, earlier, live = map(base.load, (SOURCE, PREVIOUS, replay.REPORT))
    assert packet["candidate_sha256"] == live["ROM_sha256"] == base.digest(parent.ROM)
    shots = {r["frame"]: r for r in live["frames_captured"]}
    group, = packet["groups"]
    old = {row["source_reference"]["offset"]: row for row in earlier["records"]
           if row["file_path"] == group["file_path"] and row["block"] == group["block"]}
    rows, plans = [], {}
    for entry in group["records"]:
        prior = old.pop(entry["source_offset"])
        number, selector = entry["source_record_index"], entry["selector"]
        assert entry["Japanese"] == prior["Japanese"] and all(prior["review"].values())
        japanese, current = (bytes.fromhex(entry[f"{side}_body_hex"]) for side in ("source", "current"))
        prefix = b"" if selector is None else bytes([selector])
        assert prior["source_hex"] == (prefix + japanese).hex()
        previous_english = logical(entry["current_English"])
        assert previous_english == prior["english"]
        replacement, phrases, reason = EDITS.get(number, (None, (), prior["localization_note"]))
        refs = {side: dict(file_path=group["file_path"], block=137, offset=entry[f"{side}_offset"],
                           command_offset=entry[f"{side}_command_offset"],
                           archive_sha256=group[f"{side}_archive_sha256"],
                           block_sha256=group[f"{side}_block_sha256"], exact_hex=(prefix + value).hex())
                for side, value in (("source", japanese), ("current", current))}
        changed = number in EDITS
        capture = shots[MENU if selector is None else FRAMES[number]]
        assert base.digest(capture["path"]) == capture["PNG_sha256"]
        row = dict(id=prior["id"], file_path=group["file_path"], route=0, block=137,
                   source_record_index=number, native_command_word=entry["native_command_word"],
                   native_slots=entry["slots"], source_selector=selector, kind=prior["kind"],
                   source_reference=refs["source"], current_reference=refs["current"],
                   source_hex=(prefix + japanese).hex(), current_hex=(prefix + current).hex(),
                   Japanese=entry["Japanese"], previous_English=previous_english,
                   english=replacement or previous_english, speaker=prior["speaker"], context=CONTEXT[0],
                   source_meaning=prior["source_meaning"], localization_note=reason,
                   protected_phrases=list(phrases), previous_capture=capture,
                   decision="revision" if changed else "retention",
                   finding="prose and wrap" if replacement else "wrap" if changed else "retention",
                   review=dict.fromkeys(GATES, True) | {"formatting": not changed})
        if changed:
            assert selector == 6
            body, plan = planner.plan_progressive(row, selector, current, japanese)
            assert body.rstrip(b" ") != current.rstrip(b" ") and plan["expected_native_pages"] == 1
            plans[row["id"]] = plan
            print(row["id"], plan["lines"])
        rows.append(row)
    assert len(rows) == 14 and len(plans) == len(EDITS) and not old
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=GATES, previous_sha256=packet["candidate_sha256"],
        previous_registry_sha256=base.digest(base.REGISTRY), source_packet=str(SOURCE),
        source_packet_sha256=base.digest(SOURCE), records=rows, plans=plans,
        decisions=dict(Counter(row["decision"] for row in rows)),
        findings=dict(Counter(row["finding"] for row in rows)), previous_gameplay_report=str(replay.REPORT),
        previous_gameplay_report_sha256=base.digest(replay.REPORT), new_editorial_credit=0,
        status="Contextual review complete. Revised layout and gameplay checks pending."))


if __name__ == "__main__":
    main()
