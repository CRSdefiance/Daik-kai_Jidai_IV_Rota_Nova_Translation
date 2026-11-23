"""Review the sailing lesson against the clean Japanese and verified on-screen headings."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as intake
from scripts import register_rafael_first_voyage_20261119 as parent
from scripts import register_sailing_mode_prose_20261118 as mode_review
from scripts.review_rafael_early_phrase_wraps_20261118 import GATES, TOKEN, logical

base, native = intake.base, intake.native
ROOT = Path("work/rafael_sailing_modes_review_20261119")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v2.json"
BLOCKS = ((46,), (), (), ())
CONTEXT = (
    "Hayreddin has just saved the crew. Julio warns Rafael that another fleet may challenge them and "
    "offers to explain the other things they can do at sea. Rafael can accept or decline. The system "
    "walks through the three modes, then Julio tells Rafael to stay alert.",
)
SPEAKERS = {0: "Rafael", 5: "Claudio", 6: "Julio Erneco", 254: "System", None: "Rafael"}

LESSON = {
    15: ("Claudio lets out a breath and credits Hayreddin with saving their lives.",
         "The short sigh and direct thanks fit the relief after the encounter.", None),
    18: ("Rafael agrees quietly.", "The pause lets Julio follow with a warning.", None),
    23: ("Julio thinks another fleet may pick a fight sooner than expected.",
         "Keep the uncertainty and let the warning follow Claudio's relief.",
         "At this rate, some enemy fleet might pick a fight with us sooner than we expect."),
    27: ("Julio suggests teaching Rafael what else can be done at sea.",
         "Keep his plain setup for the two choices.", None),
    32: ("Rafael accepts the offer.", "The short, polite answer agrees to hear the lesson.", None),
    34: ("Rafael says he knows enough already.", "The polite refusal plays as the alternative answer.", None),
    41: ("Julio offers to explain viewing surroundings, initiating combat and searching.",
         "Introduce the three actions in ordinary speech before the system gives their formal labels.",
         "I'll show you how to check what's nearby, start a battle, and search."),
    44: ("To see detailed information on a nearby town or fleet, or initiate combat, the player must select a target.",
         "Use town and fleet consistently and put the selection rule first.",
         "Pick a town or fleet first if you want to find out more about it or start a battle."),
    47: ("Exploring along the coast may turn up various things.",
         "Julio's suggestion preserves the location and the uncertainty.", None),
    51: ("The player can view information about nearby towns and fleets while at sea.",
         "Use town, as in the preceding instruction, and lead with what the player can learn.",
         "At sea, you can view details about nearby towns and fleets."),
    54: ("Pressing Y shows the magnifying glass for the information mode.",
         "Match the actual Info Mode heading and retain the icon the player sees.",
         "Press Y to enter Info mode. Look for the magnifying glass."),
    58: ("Put the magnifying glass over a town or fleet and press A to see details.",
         "Refer to the named icon and retain both actions in order.",
         "Move the magnifying glass over a town or fleet and press A to view details."),
    62: ("The player's ship can initiate combat against towns or other fleets.",
         "The existing short notice names both targets and keeps the possibility open.", None),
    65: ("While the magnifying glass is visible, L changes to the sword icon for combat mode.",
         "Use both verified mode headings and retain the specific L transition.",
         "In Info mode, press L to switch to Declare War mode. Look for the sword icon."),
    68: ("Put the sword over the town or fleet and press A to attack.",
         "Direct the player to the correct target and button without adding a step to the Japanese.",
         "To attack a town or fleet, move the sword over it and press A."),
    72: ("To search for items and supplies at sea, press R while the magnifying glass is active.",
         "Use the visible Info label and preserve the R transition and both search objectives.",
         "Press R in Info mode to search for items or supplies."),
    76: ("The gray frame identifies Search mode.",
         "The two short sentences give the icon before its meaning.", None),
    80: ("Press A to search the land within the gray frame.",
         "The current instruction already gives the exact action and scope.", None),
    83: ("L and R switch among the three modes.",
         "Use the same three mode names shown in the game.",
         "Press L or R to switch between Info, Declare War, and Search."),
    87: ("L cycles from information to combat to search.",
         "Use the menu headings and preserve the L order exactly.",
         "Press L to cycle from Info to Declare War to Search."),
    91: ("R or Y cycles from information to search to combat.",
         "Retain both buttons, the order and the verified headings.",
         "Press R or Y to cycle from Info to Search to Declare War."),
    95: ("Julio asks whether Rafael has understood.",
         "The two brief questions suit the end of Julio's lesson.", None),
    98: ("Rafael says yes and thanks Julio.",
         "The simple courtesy answers Julio directly.", None),
    105: ("Julio accepts the answer and emphatically warns Rafael to stay alert at sea.",
          "Keep the warning and Julio's familiar tone. The break leaves the warning easy to read.", None),
    109: ("Rafael acknowledges the warning.", "A short answer closes the exchange aloud.", None),
    117: ("Rafael thinks to himself that someday, surely, he will succeed.",
          "Keep the private aside unfinished. The Japanese leaves the object implicit.", None),
}


def mode_headings():
    picture_reviews = base.load(mode_review.REVIEW)
    arm = base.NdsImage.open(parent.ROM).read_file(native.ARM)
    headings = {}
    for record in picture_reviews["records"]:
        ref = record["registered_reference"]
        start = ref["offset"]
        assert native.digest(arm[start:start+ref["bytes"]]) == ref["packed_sha256"]
        assert all(record["review"].values())
        headings[record["heading"]] = ref
    assert set(headings) == {"Info Mode", "Declare War Mode", "Search Mode"}
    return dict(path=mode_review.REVIEW.as_posix(), sha256=base.digest(mode_review.REVIEW),
                current_exact_packed_headings=headings)


def main():
    assert not OUTPUT.exists()
    headings = mode_headings()
    if not SOURCE.exists():
        FunctionType(intake.main.__code__, vars(intake) | globals())()
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert release["candidate_sha256"] == packet["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    group, = packet["groups"]
    assert {d["source_record_index"] for d in group["records"]} == LESSON.keys()
    records = []
    for raw in group["records"]:
        idx = raw["source_record_index"]
        word, selector = raw["native_command_word"], raw["selector"]
        meaning, note, proposed = LESSON[idx]
        old = logical(raw["current_English"])
        english = proposed or old
        assert english.isascii() and TOKEN.findall(english) == TOKEN.findall(old) == TOKEN.findall(raw["Japanese"])
        assert (word == 0x2100) == (selector is None) == (idx in (32, 34))
        assert word in (0x4000, 0x2100)
        kind = "typed-choice-label" if selector is None else "system-FE" if selector == 254 else "progressive"
        prefix = "" if selector is None else bytes([selector]).hex()
        src, cur = (dict(file_path=group["file_path"], block=46, offset=raw[f"{side}_offset"],
            command_offset=raw[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
            exact_stored_hex=prefix + raw[f"{side}_body_hex"]) for side in ("source", "current"))
        src["record_index"] = idx
        if selector is None:
            src["source_index"] = cur["source_index"] = raw["slots"][0]
        phrases = [p for p in ("Declare War", "magnifying glass", "Look for the sword icon.",
                              "Look for the magnifying glass.", "press A to view details.") if p in english]
        records.append(dict(id=f"DK4_MES_B46_R{idx:04}", file_path=group["file_path"], route=0, block=46,
            kind=kind, source_selector=selector, native_command_word=word, native_slots=raw["slots"],
            source_reference=src, current_reference=cur, source_hex=src["exact_stored_hex"],
            current_hex=cur["exact_stored_hex"], Japanese=raw["Japanese"], previous_English=old,
            english=english, speaker=SPEAKERS[selector], source_meaning=meaning, context=CONTEXT[0],
            localization_note=note, protected_phrases=phrases, finding="prose" if proposed else "retention",
            decision="revision" if proposed else "retention", review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert len(records) == 26 and all((r["english"] != r["previous_English"]) == (r["decision"] == "revision") for r in records)
    counts = Counter((r["kind"], r["decision"]) for r in records)
    base.save(OUTPUT, dict(source_packet_sha256=base.digest(SOURCE), previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=GATES, records=records, current_mode_headings=headings,
        new_coverage_credit=0, formatting_and_registration_pending=True))
    print(dict(counts))


if __name__ == "__main__":
    main()
