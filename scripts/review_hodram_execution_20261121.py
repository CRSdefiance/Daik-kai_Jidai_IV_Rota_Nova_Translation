"""Review the full interruption of Hodram's public execution."""

from collections import Counter
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as pairing
from scripts import register_moonlit_violin_20261121 as parent
from scripts.review_company_name_dialogue_20261121 import ACTORS, GATES, TOKEN, logical


base, native = parent.base, parent.native
ROOT = Path("work/hodram_execution_dialogue_20261121")
SOURCE = ROOT / "paired_source.json"
OUTPUT = ROOT / "contextual_review.json"
PROGRESSIVE = ROOT / "progressive_storage_review.json"
BLOCKS = ((), (40,), (), ())
CONTEXT = ("", "The Pasha corners and orders the public execution of Hodram. "
    "Cannon fire interrupts the attack, and the Pasha orders his fleets to cover the retreat. "
    "Hodram taunts him about the execution and calls on him to fight.", "", "")
NOTES = """
6|An opponent orders Hodram to stop.|The abrupt command begins the confrontation.
11|Hodram reacts in silence.|The two marks register surprise without adding a spoken line.
15|The opponent tells Hodram that he has nowhere to escape.|The brief gloat makes the encirclement explicit.
19|The Pasha laughs at Hodram, dismisses his surname and says his exploits end here.|Keep the sneer as a dismissive question with the player's live surname and give the final boast a natural cadence.
27|Hodram concludes that the Pasha has no intention of sharing the Mediterranean.|The grudging conclusion goes beyond the present ambush and names the region.
45|The officer stammers that they are surrounded and marvels at the number of fleets.|The formal choice keeps both the stammer and the danger.
46|The officer reports the encirclement and the many fleets.|The short alarm suits this alternative.
47|The officer cries out before reporting the many fleets around them.|Keep the initial cry distinct from the other alarms.
48|The officer reacts with an incredulous question and sees many fleets.|The question mark and exclamation preserve the startled delivery.
49|The officer stammers twice, reporting enemies all around and a lot of fleets.|The contracted wording suits the rougher of the alternate voices.
50|The officer stammers before reporting that many fleets surround them.|The complete sentences preserve the report and astonishment.
51|The officer blurts out that they are surrounded by a great many fleets.|The breathless exclamations fit the youthful wording.
52|The more formal officer stammers twice as they report the encirclement.|Keep the formal second clause distinct from the other voices.
55|Hodram dismisses the fleets as a disorderly mass and orders a breakout.|The contempt and immediate command are both audible.
58|The Pasha laughs at Hodram's nerve and challenges whether he knows whom he is dealing with.|Keep the bombastic laugh and the natural shortened question.
61|Hodram calls the general ill-mannered.|His understated sarcasm answers the Pasha's bluster.
65|The Pasha orders a public execution and tells every ship to charge.|A separate command gives the order its abrupt force.
68|A voice cries out as the cannon fire begins.|The prolonged cry preserves the commotion.
72|The Pasha demands to know what happened.|The short question fits the sudden interruption.
76|The sailor reports that cannon fire is coming from town.|The hesitation preserves his alarm and retains the title Pasha.
79|The Pasha stammers and demands an explanation for the unexpected fire.|The compact questions preserve the shock and his demand for a cause.
82|The sailor says he does not know and thinks someone seized the town's gun batteries.|His stammer and uncertainty stay intact, and the batteries remain a specific installation.
88|The source marks the speaker's words as unintelligible amid the commotion.|The same two circles and cross preserve the incomplete information before Hodram reacts.
92|A second unintelligible cry is drawn out.|The full original sequence preserves the contrast with the shorter first cry without inventing speech.
96|Hodram reacts as he sees something amid the fire.|His unfinished question preserves the uncertainty.
100|Another voice gives a prolonged cry.|The cry keeps the exchange moving into the retreat order.
111|The Pasha tells Mushari's fleet to respond and orders a full-speed withdrawal.|Both brief orders already read as complete commands. Keep the single-fleet branch.
116|The Pasha sends Mushari's and Arnajud's fleets to return fire and orders a full-speed withdrawal.|Keep both fleet names and the entire urgent withdrawal command together.
125|Hodram asks what became of the public execution and challenges the commander.|The dry question and short challenge give his taunt room.
129|The Pasha accepts the challenge and threatens to make Hodram cough up blood.|Keep the coarse threat together after his angry invitation.
"""
EDITS = {
    19: ("Ha ha ha! FA, is it? Your legend ends here!", ("FA, is it?", "Your legend ends here!"), "prose"),
    116: (None, ("Withdraw at full speed!",), "wrap"),
    129: (None, ("I'll make you cough up blood!",), "wrap"),
}


def main():
    assert not OUTPUT.exists() and not PROGRESSIVE.exists()
    if not SOURCE.exists():
        FunctionType(pairing.main.__code__, vars(pairing) | dict(
            parent=parent, ROOT=ROOT, BLOCKS=BLOCKS, CONTEXT=CONTEXT))()
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert packet["clean_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    actors = base.load(ACTORS)["records"]
    notes = {}
    for line in NOTES.strip().splitlines():
        idx, meaning, reason = line.split("|")
        notes[int(idx)] = (meaning, reason)
    group, = packet["groups"]
    route, block, path = (group[k] for k in ("route", "block", "file_path"))
    assert (route, block) == (1, 40)
    records = []
    for row in group["records"]:
        idx, selector, word = (row[k] for k in ("source_record_index", "selector", "native_command_word"))
        assert word in (0x4000, 0x4100) and (word == 0x4100) == bool(row["slots"])
        current = logical(row["current_English"])
        prose, phrases, finding = EDITS.get(idx, (None, (), "retention"))
        wording = current if prose is None else prose
        assert TOKEN.findall(wording) == TOKEN.findall(current) == TOKEN.findall(row["Japanese"])
        meaning, reason = notes.pop(idx)
        kind = "progressive" if word == 0x4000 else "styled"
        name = actors[selector]["current_consumers"][0]["text"] if kind == "progressive" else "Conditional crew voice"
        refs = {side: dict(file_path=path, block=block, offset=row[f"{side}_offset"],
            command_offset=row[f"{side}_command_offset"], archive_sha256=group[f"{side}_archive_sha256"],
            block_sha256=group[f"{side}_block_sha256"],
            exact_stored_hex=bytes([selector]).hex() + row[f"{side}_body_hex"])
            for side in ("source", "current")}
        refs["source"]["record_index"] = idx
        if idx in (88, 92):
            assert row["Japanese"] == current and refs["source"]["exact_stored_hex"] == refs["current"]["exact_stored_hex"]
        records.append(dict(id=f"DK4_MES_B{block}_R{idx:04}", file_path=path, route=route, block=block,
            kind=kind, native_command_word=word, source_selector=selector, native_slots=row["slots"],
            source_reference=refs["source"], current_reference=refs["current"],
            source_hex=refs["source"]["exact_stored_hex"], current_hex=refs["current"]["exact_stored_hex"],
            Japanese=row["Japanese"], english=wording, previous_English=current, context=CONTEXT[route],
            speaker=name, source_meaning=meaning, localization_note=reason, protected_phrases=list(phrases),
            finding=finding, decision="revision" if idx in EDITS else "retention",
            review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert not notes and len(records) == 30 and sum(r["kind"] == "styled" for r in records) == 8
    common = dict(previous_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        previous_registry_sha256=release["registry_sha256"], source_packet=str(SOURCE),
        source_packet_sha256=base.digest(SOURCE), translation_policy="natural-dialogue-v2", target_locale="en-US",
        encoder="dialogue-relocatable-v1", review_gates=GATES, new_coverage_credit=0)
    base.save(OUTPUT, common | dict(records=records, decisions=dict(Counter(r["decision"] for r in records))))
    base.save(PROGRESSIVE, common | dict(records=[r for r in records if r["kind"] == "progressive"]))
    print("Reviewed all 30 execution-scene entries, including the eight crew alternatives.")


if __name__ == "__main__":
    main()
