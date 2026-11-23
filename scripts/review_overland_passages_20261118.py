"""Review the overland forest and desert exchanges against the clean scripts."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import prepare_overland_passages_20261118 as current
from scripts import review_ruins_clues_and_guides_20261118 as previous
from scripts.source_locked_derivation_v5118 import checked_text

base, parent, binder = current.paired.base, current.parent, previous.binder
SOURCE = current.ROOT / "paired_source.json"
SOURCE_SHA = "a28d12a31c8352d1fc62bfc138d2c0ce4df915c5db6dbaaa4a1936331b50bd01"
OUTPUT = Path("translations/editorial_checkpoints/SharedText_20261110_v1/overland_passages_20261118_prose_v5.json")
HISTORY = (
    ("rafael_B301_B320_integrated_final_review_v1.json",),
    ("hodram_B281_B300_integrated_final_review_v1.json", "hodram_B301_B310_integrated_final_review_v1.json"),
    ("lil278_B299_B311_integrated_final_review_v1.json",),
    ("maria359_B253_B274_integrated_final_review_v1.json",),
)
DECISIONS = Path("translations/editorial_checkpoints/SharedText_20261110_v1/overland_passages_decisions_v2.txt")


def main():
    parts = DECISIONS.read_text(encoding="utf-8-sig").strip().split("\n\n")
    notes, edits, phrases = parts
    notes = notes.splitlines()
    assert len(notes) == 320
    edit_map = {}
    for line in edits.splitlines():
        index, routes, english = line.split("|")
        for route in routes:
            key = int(index), int(route)
            assert key not in edit_map
            edit_map[key] = english
    context = vars(binder).copy()
    source = checked_text(getsource(binder.review_one), {
        "if word == 0x2100:": "if word in (0x2100, 0x2200):",
        'if word == 0x2100 else': 'if word in (0x2100, 0x2200) else',
    })
    exec(compile(source, __file__ + "::review-both-native-choice-counts", "exec"), context)
    derive = checked_text(getsource(previous.main), {
        'len(packet["groups"]) == 20': 'len(packet["groups"]) == 16',
        "}) == 350": "}) == 519",
    })
    scope = vars(previous) | globals() | {
        "binder": SimpleNamespace(**context), "NOTES": dict(enumerate(notes, 1)),
        "EDITS": edit_map, "PHRASES": tuple(phrases.splitlines()),
    }
    exec(compile(derive, __file__ + "::overland-packet-ledger", "exec"), scope)
    scope["main"]()


if __name__ == "__main__":
    main()




