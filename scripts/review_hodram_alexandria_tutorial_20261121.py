"""Review the complete arrival warning, recruitment, and ship lesson."""
from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import checkpoint_hodram_alexandria_arrival_20261121 as arrival
from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_alexandria_dialogue_20261121 as parent
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/hodram_alexandria_tutorial_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v4.json"
BLOCKS = ((), (51, 167), (), ())
CONTEXT = ("Hodram's port warning and Cesare's recruitment and ship advice.",) * 4
SCENES = {
    51: "The Port Worker warns the arriving fleet off. Hodram asks why, the worker stays vague, and the crew reacts without naming the person.",
    167: "Hodram and Charles meet Cesare looking for the Elysion. Hodram recruits him for his knowledge and command experience. Cesare offers an optional lesson on choosing ships for trade, equipment, distance, and battle.",
}
PRIOR = {51: Path("translations/hodram_B51_contextual_final_review_v1.json"),
         167: Path("translations/hodram_B151_B170_contextual_final_review_v1.json")}

# None keeps the wording and revisits its line breaks.
EDITS = {
    51: {
        6: ("I don't know what you're planning in the southern Mediterranean. Take my advice and leave.",
            ("I don't know what you're planning", "the southern Mediterranean.", "Take my advice and leave."),
            "Keep the worker's blunt warning, his uncertainty about the fleet's plans, and the geographic phrase."),
        14: ("There's someone around here who's bad news. Trust me, you'd be safer in another sea.",
             ("who's bad news.", "you'd be safer in another sea."),
             "Keep the threatening person unnamed and the advice grounded in the crew's safety."),
    },
    167: {
        5: ("Alexandria... Quite a few ships in port. Hm? What's that?",
            ("Quite a few ships in port.", "Hm? What's that?"),
            "Restore Hodram's observation about the number of ships before his attention shifts to Cesare."),
        17: ("Looks like it. You there. Are you looking for something?", ("Are you looking for something?",),
             "Hodram agrees with Charles, then addresses the stranger directly. Keep the query together."),
        28: (None, ("sailed the seven seas.",), "Preserve Cesare's affectionate pairing of himself with his ship and keep the familiar expression together."),
        42: (None, ("You sailed the whole world?",), "Hodram tests the literal claim about the seven seas. Keep the second question together."),
        56: ("You know those lands. And you've been a captain...", ("You know those lands.", "you've been a captain..."),
             "Make both qualifications explicit as Hodram considers inviting Cesare aboard."),
        60: ("Here's a proposal. Join my ship and help me with my work.", ("Here's a proposal.", "help me with my work."),
             "Restore Hodram's matter-of-fact offer to take Cesare aboard if he helps with his work."),
        67: ("Ha! I knew you'd say that, Admiral FI!", ("I knew you'd say that,", "Admiral FI!"),
             "Give Charles's amused reply a subject and preserve his rank of address and the given-name substitution."),
        86: ("Oh, Admiral. May I offer some advice on choosing ships?", ("advice on choosing ships?",),
             "Keep Cesare's polite request and the subject of the lesson he is about to offer."),
        92: ("Listen", (), "Use a bare action verb to match Skip. Preserve the selection index and original branch."),
        122: ("You don't need more ships just to sign deals with new towns and open trade routes. With a one percent share, you can buy only one to five units of trade goods.",
              ("You don't need more ships", "sign deals", "with new towns", "open trade routes.", "With a one percent share,", "one to five units"),
              "Keep the opening recommendation and the numerical limit in separate thoughts. The small share limits purchases while the player is expanding trade."),
        125: ("Once your market share grows and you can buy more goods, it's time to buy a ship.",
              ("your market share grows", "you can buy more goods,", "it's time to buy a ship."),
              "Keep the increase in market share and the larger purchase volume as the reason to buy a ship."),
        132: ("Buy a ship your market share and budget can support. Otherwise you'll need more sailors for a ship you can't fill.",
              ("your market share", "budget can support.", "Otherwise you'll need more sailors", "a ship you can't fill."),
              "Keep the two sizing limits and the mismatch between cargo purchases and sailors. Let the consequence read as a full thought."),
        135: ("Price gives you an idea of size. Under 5,000 is small, 10,000 to 20,000 is medium, and over 50,000 is large.",
              ("Under 5,000 is small,", "10,000 to 20,000 is medium,", "over 50,000 is large."),
              "Keep the three original ranges and the fact that price is an indicator. Leave the source's gaps between ranges intact."),
        138: ("Small ships are cheap. Even when funds are tight, they let you add cargo space to your fleet.",
              ("Small ships are cheap.", "Even when funds are tight,", "cargo space to your fleet."),
              "Keep the affordable option and its cargo benefit. Read the opening of the second sentence together."),
        145: ("Medium ships have two or three masts. The ones with three are faster, but they need more sail handlers.",
              ("two or three masts.", "The ones with three", "more sail handlers."),
              "Keep the mast counts and the trade-off between speed and crew assignments."),
        148: ("Refit for up to five cargo holds. If you won't fight for a while, skip marine quarters and batteries.",
              ("Refit for up to five cargo holds.", "If you won't fight for a while,", "skip marine quarters and batteries."),
              "Keep the original upper limit and the condition for leaving out combat rooms."),
        151: ("To open a route to a distant town, add more supply holds. That lets you sail much farther.",
              ("To open a route to a distant town,", "add more supply holds.", "That lets you sail much farther."),
              "Restore distant towns and route opening as the purpose of expanding supplies."),
        157: ("Equip at least your flagship with marine quarters and armed batteries. It'll be hard to win at sea without them.",
              ("at least your flagship", "marine quarters", "armed batteries.", "win at sea without them."),
              "Preserve the minimum flagship recommendation and Cesare's warning that victories will be difficult."),
        163: ("You'll move up to large ships. Planning to form regional fleets? You could keep your medium ships.",
              ("move up to large ships.", "Planning to form regional fleets?", "You could keep your medium ships."),
              "Keep the later upgrade and the reason to keep the old ships. Express the alternative to selling as keeping them."),
        166: ("That's all my advice. I'll get ready to sail. Until later!",
              ("That's all my advice.", "I'll get ready to sail."),
              "Close the optional lesson in Cesare's courteous voice and preserve his next action."),
    },
}

RETENTIONS = {
    51: {10: "The short question prompts the worker's explanation.",
         32: "Charles echoes the worker's vague description without identifying the person.",
         39: "Gerhard keeps his possible recognition private and tentative."},
    167: {
        9: "Cesare's address to the missing Elysion reveals his distress and affection.",
        13: "Charles notices the search and opens the exchange with Hodram.",
        21: "Cesare's emphatic reply immediately names the ship and keeps his polite address.",
        24: "Hodram's silent question lets Cesare explain the loss.",
        31: "The survivor and the loss of the ship remain distinct, and the trailing thought invites a response.",
        35: "Charles checks that the lost ship is the goal of the search.",
        39: "The repeated unsuccessful search makes Cesare's frustration plain.",
        45: "Cesare confirms his travels and names Asia and the New World.",
        48: "Hodram's terse question asks about Cesare's shipboard role.",
        52: "Cesare gives his original rank confidently, answering Hodram directly.",
        64: "Hodram makes finding the ship a possibility while traveling with him.",
        70: "Cesare's startled acceptance keeps his eagerness and courteous address.",
        73: "Hodram brings Cesare aboard, introduces himself with both name substitutions, and puts his trust in him.",
        77: "Cesare answers the introduction with his full name and a respectful address.",
        81: "Charles welcomes Cesare and answers his introduction with his own name.",
        94: "Skip is a clear action for declining the optional advice.",
        104: "Cesare takes the refusal gracefully and praises Hodram for having his own principles.",
        108: "Cesare leaves to prepare for departure when the player skips the lesson.",
        118: "The short pause lets Cesare gather his thoughts before beginning his advice.",
        129: "The topic sentence names both purchasing factors before explaining them.",
        141: "The next upgrade follows the increase in funds from trading.",
        154: "The change from peaceful trade to conflict explains why large ships are needed.",
        160: "The comparison keeps the price and capacity advantages of two medium ships over one large ship.",
    },
}


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__, vars(pairing) | globals())()
    packet, old_packet, release, live = map(base.load, (SOURCE, arrival.SOURCE, parent.RELEASE, arrival.OUTPUT))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    assert live["source_packet_sha256"] == base.digest(arrival.SOURCE)
    assert live["ordinary_sailing_and_story_activation"]
    shown = {r["id"]: r["actual_complete_pages"] for r in live["full_body_matches"]}
    shown.update({r["id"]: [r["frame"]] for r in live["displayed_captions"]})
    rows = []
    for group, old in zip(packet["groups"], old_packet["groups"], strict=True):
        path, number = group["file_path"], group["block"]
        assert (path, number, group["source_block_sha256"], group["current_block_sha256"], group["records"]) == (
            old["file_path"], old["block"], old["source_block_sha256"], old["current_block_sha256"], old["records"])
        historical = {r["source_reference"]["offset"]: r for r in base.load(PRIOR[number])["records"] if r["block"] == number}
        for entry in group["records"]:
            index, selector = entry["source_record_index"], entry["selector"]
            prior = historical.pop(entry["source_offset"])
            assert prior["source_Japanese"] == entry["Japanese"] and prior.get("source_selector") == selector
            assert all(prior["review"].values())
            current = logical(entry["current_English"])
            revision = EDITS[number].get(index)
            if revision:
                new, phrases, note = revision
            else:
                new, phrases, note = None, (), RETENTIONS[number][index]
            english = new or current
            assert TOKEN.findall(entry["Japanese"]) == TOKEN.findall(current) == TOKEN.findall(english)
            leading = "" if selector is None else f"{selector:02x}"
            intent = {side: dict(file_path=path, block=number, offset=entry[f"{side}_offset"],
                                 command_offset=entry[f"{side}_command_offset"],
                                 archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                                 exact_hex=leading + entry[f"{side}_body_hex"]) for side in ("source", "current")}
            rows.append(dict(id=prior["id"], file_path=path, route=1, block=number, source_record_index=index,
                native_command_word=entry["native_command_word"], native_slots=entry["slots"], source_selector=selector,
                kind="typed-choice-label" if selector is None else "progressive",
                source_reference=intent["source"], current_reference=intent["current"],
                source_hex=intent["source"]["exact_hex"], current_hex=intent["current"]["exact_hex"],
                Japanese=entry["Japanese"], previous_English=current, english=english, speaker=prior["speaker"],
                context=SCENES[number], source_meaning=prior["source_meaning"], localization_note=note,
                protected_phrases=list(phrases), previous_gameplay=shown.get(prior["id"], []),
                review=dict.fromkeys(GATES, True) | {"formatting": not bool(revision)},
                decision="revision" if revision else "retention",
                finding="choice caption" if revision and selector is None else "prose and wrap" if new
                    else "wrap" if revision else "retention"))
        assert not historical
    assert len(rows) == 48
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=GATES, previous_sha256=packet["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        source_gameplay=str(arrival.OUTPUT), source_gameplay_sha256=base.digest(arrival.OUTPUT), records=rows,
        decisions=dict(Counter(row["decision"] for row in rows)), findings=dict(Counter(row["finding"] for row in rows)),
        new_editorial_credit=0, status="Contextual review complete. Revised pages and caption await native verification."))
    print(f"Reviewed {len(rows)} records across both complete exchanges.")


if __name__ == "__main__":
    main()
