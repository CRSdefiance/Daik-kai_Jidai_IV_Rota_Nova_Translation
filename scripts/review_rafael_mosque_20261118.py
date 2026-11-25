"""Bind the fresh Rafael mosque and detour decisions to the paired source."""

from collections import defaultdict
from pathlib import Path
from types import FunctionType

from scripts import prepare_mosque_temple_shipyard_20261118 as current
from scripts import review_jungle_caves_20261118 as binder

base, parent = current.paired.base, current.parent
SOURCE = current.ROOT / "paired_source.json"
SOURCE_SHA = "76dede3dafcc34f418b14147aa42ffa03c26bc81426924cf5635ef0473be2c3e"
FOLDER = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
DECISIONS = FOLDER / "rafael_mosque_decisions_v3.txt"
OUTPUT = FOLDER / "rafael_mosque_20261118_prose_v3.json"
HISTORY = Path("translations/rafael_B301_B320_integrated_final_review_v1.json")
BLOCKS = (current.BLOCKS[0], (), (), ())


def main():
    assert base.digest(SOURCE) == SOURCE_SHA
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert packet["complete_source_current_binding"]
    notes, edits, phrases = DECISIONS.read_text(encoding="utf-8-sig").strip().split("\n\n")
    notes, phrases = notes.splitlines(), phrases.splitlines()
    edit_map = {(int(pos), 0): text for pos, text in (line.split("|") for line in edits.splitlines())}
    history, checksum = binder.binder.index_history(HISTORY), base.digest(HISTORY)
    rows = []
    done = set()
    review = FunctionType(binder.review_one.__code__, vars(binder) | {
        "NOTES": notes, "EDITS": edit_map, "PHRASES": phrases,
    })
    for group in packet["groups"]:
        if group["route"] != 0:
            continue
        block = group["block"]
        assert block in BLOCKS[0]
        for raw in group["records"]:
            pos = len(rows) + 1
            old = history[block, raw["source_offset"]]
            item = review(raw, group, old, pos, HISTORY, checksum)
            item["context"] = old["context"]
            item["source_meaning"] = old["source_meaning"]
            if item["decision"] == "revision":
                done.add((pos, 0))
            elif pos == 37:
                item["manual_break_reason"] = notes[pos - 1]
            rows.append(item)
    assert len(rows) == len(notes) == 139 and done == edit_map.keys()
    assert len({r["id"] for r in rows}) == len(rows)
    assert not OUTPUT.exists()
    base.save(OUTPUT, dict(translation_policy="natural-dialogue-v2", target_locale="en-US",
        source_packet=str(SOURCE), source_packet_sha256=SOURCE_SHA, previous_sha256=release["candidate_sha256"],
        previous_registry_sha256=release["registry_sha256"], clean_input_sha256=release["clean_input_sha256"],
        formatting_and_registration_pending=True, additional_review_credit=0, records=rows))
    print(binder.binder.Counter((r["kind"], r["decision"]) for r in rows))


if __name__ == "__main__":
    main()


