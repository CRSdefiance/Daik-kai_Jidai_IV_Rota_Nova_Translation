"""Review the four Alexandria cooking exchanges against the identical source turns."""
from collections import Counter
from pathlib import Path
from types import FunctionType
import re

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_rafael_mediterranean_dialogue_20261121 as parent
from scripts.review_company_name_dialogue_20261121 import GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/alexandria_dialogue_20261121")
SOURCE, OUTPUT = ROOT / "paired_source.json", ROOT / "contextual_review_v1.json"
PREVIOUS = Path("releases/all_routes_editorial_20261115_town_trend_exchanges_candidate/verification/registered_review.json")
BLOCKS = ((198,), (190,), (186,), (159,))
CONTEXT = ("The owner thinks her customers want sweeter food. The cook questions that, asks how, and gives in as she leaves it to him. The impersonal notice forecasts a possible trend.",) * 4
MILD = ("Yes! Our customers won't settle for a flavor this mild. It has to be sweeet! Sweet!",
        ("a flavor this mild.", "It has to be sweeet! Sweet!"),
        "Use the same customer complaint and deliberately stretched catchphrase as in the other copies.")
CLOSING = ("Sweet, remember? I'm counting on you! Oh-ho-ho-ho!",
           ("Sweet, remember?", "I'm counting on you!", "Oh-ho-ho-ho!"),
           "Keep the borrowed catchphrase, her expectation of the cook, and the affected laugh.")
FORECAST = ("Sweets may catch on in Alexandria.", ("in Alexandria.",),
            "Keep the forecast tentative and use the same town and trend wording as the other copies.")
REVISIONS = {
    0: {3: MILD, 6: ("Then how should we make it sweeter?", ("Then how should we make it sweeter?",),
                     "Let the cook's dry reply lead straight into the full question about method."), 11: CLOSING},
    1: {5: ("Of course! I said so, didn't I?", ("I said so, didn't I?",),
            "Use the punch line already read in the other three copies. Her own word is the basis for her certainty."),
        12: FORECAST},
    2: {1: ("Hmm... Something's missing. I know! It needs to be sweeter!",
            ("Something's missing.", "It needs to be sweeter!"),
            "Let the owner discover the missing quality herself and give the cook a clear word to echo."),
        2: ("Sweeter?", ("Sweeter?",), "The cook questions the owner's newly stated preference in a dry one-word echo."),
        3: MILD, 11: CLOSING},
    3: {12: FORECAST},
}
RETENTIONS = {
    1: "The pause, realization and request for a sweeter result establish the owner's delivery.",
    2: "The cook's brief echo continues the immediately preceding line without adding an objection.",
    3: "The customers' dissatisfaction motivates the affectionate but overstated pronunciation of Sweet.",
    4: "The cook's skeptical question leaves room for the owner's self-assured reply.",
    5: "The owner takes her own judgment as decisive, setting up the question about method.",
    6: "The cook asks how to make the dish sweeter without claiming to know the answer.",
    7: "The owner leaves the method to the cook while keeping the curt, familiar tone.",
    8: "The pause before the first double acknowledgment carries the cook's resignation.",
    9: "The owner claims the trend is certain, which the later public notice qualifies.",
    10: "The cook repeats his acknowledgment more quickly as the exchange winds down.",
    11: "The owner's reminder, expectation and laugh repeat her earlier mannerisms.",
    12: "The impersonal system notice keeps the Alexandria trend tentative.",
}


def main():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__, vars(pairing) | globals())()
    source, release = map(base.load, (SOURCE, parent.RELEASE))
    candidate = release["candidate_sha256"]
    assert candidate == source["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == source["clean_sha256"] == base.digest(native.CLEAN)
    prior = {(r["route"], r["source_reference"]["offset"]): r for r in base.load(PREVIOUS)["records"]
             if r["group"] == 159}
    all_rows = []
    for entries in zip(*(group["records"] for group in source["groups"]), strict=True):
        assert len({(e["Japanese"], e["selector"], e["native_command_word"]) for e in entries}) == 1
    for group in source["groups"]:
        route, number, path = group["route"], group["block"], group["file_path"]
        for ordinal, entry in enumerate(group["records"], 1):
            previous = prior.pop((route, entry["source_offset"]))
            selector = entry["selector"]
            assert previous["Japanese"] == entry["Japanese"] and previous["source_selector"] == selector
            assert all(previous["review"].values()) and entry["native_command_word"] == 0x4000
            current = logical(entry["current_English"])
            proposed = REVISIONS[route].get(ordinal)
            english, phrases, note = proposed or (current, (), RETENTIONS[ordinal])
            assert (english != current) == bool(proposed), (route, ordinal, current)
            assert not TOKEN.findall(english) and not TOKEN.findall(current)
            refs = {side: dict(file_path=path, block=number, offset=entry[f"{side}_offset"],
                               command_offset=entry[f"{side}_command_offset"],
                               archive_sha256=group[f"{side}_archive_sha256"], block_sha256=group[f"{side}_block_sha256"],
                               exact_hex=f"{selector:02x}" + entry[f"{side}_body_hex"])
                    for side in ("source", "current")}
            assert refs["source"]["exact_hex"] == previous["source_hex"]
            row = dict(id=previous["id"], file_path=path, route=route, block=number, ordinal=ordinal,
                       source_record_index=entry["source_record_index"], native_command_word=0x4000, native_slots=[],
                       kind="system-FE" if selector == 254 else "progressive", source_selector=selector,
                       source_reference=refs["source"], current_reference=refs["current"], source_hex=refs["source"]["exact_hex"],
                       current_hex=refs["current"]["exact_hex"], Japanese=entry["Japanese"], previous_English=current,
                       english=english, speaker=previous["speaker"], context=CONTEXT[route],
                       source_meaning=previous["source_meaning"], localization_note=note, protected_phrases=list(phrases),
                       decision="revision" if proposed else "retention",
                       review=dict.fromkeys(GATES, True) | {"formatting": not proposed})
            all_rows.append(row)
    assert len(all_rows) == 48 and not prior
    decisions = dict(Counter(row["decision"] for row in all_rows))
    assert decisions == {"revision": 10, "retention": 38}
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1",
        target_locale="en-US", review_gates=GATES, previous_sha256=candidate,
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE), source_packet_sha256=base.digest(SOURCE),
        previous_review=str(PREVIOUS), previous_review_sha256=base.digest(PREVIOUS), records=all_rows, decisions=decisions,
        new_editorial_credit=0, status="Contextual review complete. Changed displays await native verification."))
    print("Reviewed 48 turns and planned 10 revisions across the four Alexandria copies.")


if __name__ == "__main__":
    main()
