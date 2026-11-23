"""Revisit Julio's full Deck lesson with exact clean and installed text references."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as intake
from scripts import register_save_location_labels_20261119 as parent
from scripts.review_rafael_early_phrase_wraps_20261118 import GATES, TOKEN, logical

base, native = intake.base, intake.native
ROOT = Path("work/rafael_deck_lesson_20261119_v2")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v2.json"
BLOCKS = ((43,), (), (), ())
CONTEXT = (
    "Julio checks whether Rafael has followed the lesson. He explains how to assign navigators, "
    "what each Deck job does and which jobs are enough for ordinary sailing. A system panel "
    "then tells Rafael how to open Deck View.",
)
LESSON = {
    7: ("Julio checks that Rafael is following, then introduces the navigators, including himself.",
        "The opening question and 'people like us' keep Julio's direct, familiar teaching voice.",
        None, ()),
    11: ("Assigning people their duties is one of an admiral's important jobs.",
         "The sentence leads with the admiral's responsibility and keeps 'assigning duties' together.",
         "One of an admiral's main jobs is assigning duties.", ("assigning duties.",)),
    14: ("To make the voyage go smoothly, give each navigator a duty while looking at the Deck screen.",
         "Give the reason and the instruction in Julio's spoken voice, using the label the player sees.",
         "Give each navigator a job so the voyage goes smoothly. Let's do that in Deck View.",
         ("Let's do that in Deck View.",)),
    17: ("Julio says Rafael is the captain. A ship needs a captain and cannot sail off by itself.",
         "The repetition makes Julio's point conversationally. Preserve all four rows, the normal F and the live name.",
         None, ()),
    20: ("A Sail Handler adjusts the sails to the wind. Each mast needs one.",
         "The title, explanation and required number are all clear in the right order.",
         None, ()),
    23: ("The Helmsman matters when you want the ship to turn quickly.",
         "Julio describes the role in the circumstances where it matters; the next line expands on skill.",
         "When you need to turn the ship quickly, the Helmsman is the one to count on.",
         ("the Helmsman", "the one to count on.")),
    27: ("A skilled helmsman can maneuver the ship quickly into an advantageous position during battle.",
         "The second sentence develops the previous turn with the maneuvering example and its tactical payoff.",
         None, ()),
    30: ("A ship can sail without a First Mate, but the job enables talks with other powers and reduces fatigue at sea. Julio calls it important work that goes unnoticed.",
         "Make the two benefits easy to follow and keep Julio's warm compliment as its own sentence.",
         "A First Mate is optional, but lets you negotiate with other powers and keeps the crew from tiring so fast at sea. An unsung hero.",
         ("First Mate", "other powers", "An unsung hero.")),
    33: ("A Surveyor allows automatic movement and gives the fleet's latitude and longitude. It is fairly important.",
         "Use the game's Auto Move label so the player can connect the lesson to the command. Keep both coordinates.",
         "With a Surveyor, you can use Auto Move and see the fleet's latitude and longitude. It's an important job.",
         ("Auto Move", "latitude and longitude.", "It's an important job.")),
    37: ("The Lookout reports who other ships belong to at sea and what is happening in towns, among other things.",
         "Use conversational language for ship affiliation and town conditions.",
         "At sea, the Lookout tells you who other ships belong to and what's happening in nearby towns.",
         ("the Lookout", "who other ships belong to")),
    40: ("Those jobs should be enough for ordinary sailing. Julio recommends trying out the others.",
         "The closing advice invites the player to explore the remaining jobs and retains Julio's qualification.",
         "That's about all you need to set sail. Try out the other jobs and see what they do.", ("to set sail.",)),
    45: ("Press X and choose Deck View. It changes navigator assignments.",
         "Keep the on-screen control, exact menu label and plain system voice that follows Julio's explanation.",
         None, ()),
}


def main():
    FunctionType(intake.main.__code__, vars(intake) | globals())()
    source, release = map(base.load, (SOURCE, parent.RELEASE))
    assert source["candidate_sha256"] == release["candidate_sha256"]
    group, = source["groups"]
    assert {r["source_record_index"] for r in group["records"]} == LESSON.keys()
    records = []
    for data in group["records"]:
        idx = data["source_record_index"]
        meaning, note, proposed, phrases = LESSON[idx]
        old = logical(data["current_English"])
        english = proposed or old
        assert data["native_command_word"] == 0x4000 and not data["slots"]
        assert data["selector"] in (6, 254) and (data["selector"] == 254) == (idx == 45)
        assert TOKEN.findall(english) == TOKEN.findall(old) == TOKEN.findall(data["Japanese"])
        if proposed is not None:
            assert english.isascii() and english != old and data["selector"] == 6
        source_ref, current_ref = (dict(file_path=group["file_path"], block=43, offset=data[f"{side}_offset"],
            command_offset=data[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
            exact_stored_hex=bytes([data["selector"]]).hex() + data[f"{side}_body_hex"])
            for side in ("source", "current"))
        source_ref["record_index"] = idx
        records.append(dict(id=f"DK4_MES_B43_R{idx:04}", file_path=group["file_path"], route=0, block=43,
            kind="system-FE" if idx == 45 else "progressive", native_command_word=0x4000,
            source_selector=data["selector"], native_slots=[], source_reference=source_ref,
            current_reference=current_ref, source_hex=source_ref["exact_stored_hex"],
            current_hex=current_ref["exact_stored_hex"], Japanese=data["Japanese"], previous_English=old,
            english=english, speaker="System" if idx == 45 else "Julio Erneco", source_meaning=meaning,
            context=CONTEXT[0], localization_note=note, protected_phrases=list(phrases),
            finding="prose" if proposed else "retention", decision="revision" if proposed else "retention",
            review=dict.fromkeys(GATES, True) | {"formatting": False}))
    base.save(OUTPUT, dict(source_packet_sha256=base.digest(SOURCE), previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], translation_policy="natural-dialogue-v2",
        target_locale="en-US", encoder="dialogue-relocatable-v1", review_gates=GATES, records=records,
        new_coverage_credit=0, formatting_and_registration_pending=True))
    print("Reviewed Julio's complete 12-turn Deck lesson.")


if __name__ == "__main__":
    main()
