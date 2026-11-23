"""Pair question-tag and phrase-wrap leads with their complete source exchanges."""

import sys
from pathlib import Path
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as paired
from scripts import register_late_trade_exchanges_20261118 as parent

ROOT = Path("work/story_tag_wraps_source_20261118")
# Offsets identify the selector bytes in the registered Late Trade Exchanges ROM.
LEADS = (
    {49: 2617, 70: 2217, 82: 17, 84: 5135},
    {85: 2701, 147: 17, 242: 959},
    {26: 1611, 66: 683, 72: 2741, 129: 161, 151: 2111, 183: 945, 186: 297, 215: 183, 220: 127},
    {188: 187},
)
# B84 has two intentional current-only page commands, so it needs its existing
# split-page mapping before it can join a source-aligned build.
SPECIALIZED = {(0, 84)}
BLOCKS = tuple(tuple(block for block in route if (i, block) not in SPECIALIZED)
               for i, route in enumerate(LEADS))
CONTEXT = ("Rafael", "Hodram", "Lil", "Maria")
SOURCE = ROOT / "paired_source.json"
EXTENDED = ROOT / "paired_source_with_training.json"


def add_training_offer():
    base, native = paired.base, paired.native
    assert not EXTENDED.exists()
    packet = base.load(SOURCE)
    release = base.load(parent.RELEASE)
    assert packet["candidate_sha256"] == release["candidate_sha256"] == base.digest(parent.ROM)
    assert packet["clean_sha256"] == base.digest(native.CLEAN)
    path = "/data/SC0.DK4"
    inventory, _, _ = native.scoped_inventory()
    inputs = []
    for rom in (native.CLEAN, parent.ROM):
        image = base.NdsImage.open(rom)
        archive = image.read_file(path)
        block = native.IlnkContainer.parse(archive).blocks[84]
        arm = image.read_file(native.ARM)
        commands, _ = inventory(arm, block)
        inputs.append((archive, block, commands))
    src, cur = inputs
    rows = []
    for match, (archive, block, commands) in zip((5192, 5130), inputs, strict=True):
        position = next(i for i, cmd in enumerate(commands) if cmd["offset"] == match)
        assert [cmd["word"] for cmd in commands[position - 3:position + 6]] == [
            0x6004, 0xA000, 0x6109, 0x4000, 0xA000, 0x2200, 0x200, 0x300, 0x400]
        cmd = commands[position]
        raw = bytes.fromhex(cmd["whole_command_hex"])
        assert raw[:6] == bytes.fromhex("0040ffff0010") and cmd["offset"] == match
        rows.append((match, raw[6:raw.index(0, 6)]))
    (j, ja), (e, en) = rows
    assert src[1][:j + 5].count(b"\0") == 417 and e + 5 == LEADS[0][84]
    record = dict(file_path=path, block=84, source_command_offset=j, current_command_offset=e,
                  source_offset=j + 5, current_offset=e + 5, source_record_index=417, native_command_word=0x4000,
                  selector=16, slots=[], source_body_hex=ja.hex(), current_body_hex=en.hex(),
                  Japanese=ja.decode("cp932"), current_English=en.decode("cp932"))
    packet["groups"].append(dict(route=0, block=84, file_path=path, context="Gerhard offers to train Rafael.",
        source_block_sha256=native.digest(src[1]), current_block_sha256=native.digest(cur[1]),
        source_archive_sha256=native.digest(src[0]), current_archive_sha256=native.digest(cur[0]),
        native_commands=len(cur[2]), counts={"0x4000": 1}, records=[record],
        prior_intentional_added_pages_preserved=True, source_and_current_offer_choice_sequence_bound=True))
    base.save(EXTENDED, packet)


if __name__ == "__main__":
    if sys.argv[1:] == ["--extend-training"]:
        add_training_offer()
        sys.exit()
    read_pairs = FunctionType(paired.main.__code__, vars(paired) | {
        "ROOT": ROOT, "BLOCKS": BLOCKS, "CONTEXT": CONTEXT, "parent": parent,
    })
    read_pairs()
    data = paired.base.load(ROOT / "paired_source.json")
    for group in data["groups"]:
        route, block = group["route"], group["block"]
        position = LEADS[route][block]
        [record] = [row for row in group["records"] if row["current_offset"] == position]
        assert record["native_command_word"] == 0x4000
