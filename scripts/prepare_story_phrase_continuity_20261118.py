"""Bind high-confidence phrase-wrap leads to complete source and installed exchanges."""

from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_story_tag_wraps_20261118 as parent

ROOT = Path("work/story_phrase_continuity_20261118")
SOURCE = ROOT / "paired_source.json"
# These offsets identify stored selectors in the registered Story Tag Wraps ROM.
LEADS = (
    {52: (99,), 58: (681,), 93: (597,), 143: (4267,), 152: (1557, 1781), 176: (1099,),
     186: (1895,), 243: (99,), 249: (427,), 252: (661,), 303: (331,), 322: (657,)},
    {240: (315,), 251: (47,), 294: (459,), 314: (33,)},
    {92: (215,), 133: (345,), 237: (351,), 248: (99,), 317: (33,)},
    {61: (1167, 2297), 174: (367,), 209: (559, 1097), 210: (373,), 286: (33,), 295: (13,), 298: (1143,)},
)
CONTEXT = ("Rafael", "Hodram", "Lil", "Maria")
BLOCKS = tuple(tuple(route) for route in LEADS)


def main():
    prepare = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    if not SOURCE.exists():
        prepare()
    packet = paired.base.load(SOURCE)
    assert packet["candidate_sha256"] == paired.base.digest(parent.ROM)
    matched = {}
    for g in packet["groups"]:
        key = g["route"], g["block"]
        wanted = LEADS[key[0]][key[1]]
        selected = [r for r in g["records"] if r["current_offset"] in wanted]
        assert [r["current_offset"] for r in selected] == list(wanted)
        assert all(r["native_command_word"] == 0x4000 for r in selected)
        matched[key] = len(selected)
    assert len(matched) == 28 and sum(matched.values()) == 31


if __name__ == "__main__":
    main()
