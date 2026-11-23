"""Pair the next London guild assignments with their registered current commands."""

from collections import Counter
from pathlib import Path
from struct import unpack_from

from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from scripts import register_forest_expeditions_20261118 as parent


base, native, stage = parent.base, parent.native, parent.stage
ROOT = Path("work/london_guild_assignments_source_20261118")
BLOCKS = ((294, 295, 296, 297, 298, 299, 300), (292, 293), (284, 285, 286, 287),
          (253, 254, 255, 256, 257, 258))
CONTEXT = (
    "The summons and commission lead into the ruins, the displaced officiant, the cult and its riddle. Follow the townspeople's clues, the measurement of the shadows and the return to the guild.",
    "The guildmaster requests help with reports of a sea creature. Review the initial account, the offer and conditions, the response to the defeat, and the rumor he offers afterward. The subsequent inland search is a separate scene.",
    "The guild asks for two holds of wine. The crew reminds Lil about the consignment, the market takes delivery, and the discussion after the handover connects to the later rumor.",
    "The guildmaster asks Maria for a remedy for his navigators' scurvy. Follow variants for finding the remedy, the month-long loan, the crew reminders, and the return and map discussion.",
)


def text_records(raw, word):
    if word == stage.SPEECH:
        return [(5, raw[5], raw[6:raw.index(0, 6)], [])]
    if word == stage.STYLE:
        slots, bodies = parent.display.unpack(raw)
        return [(20 + at, raw[19], bodies[at], [i for i, offset in enumerate(slots) if offset == at])
                for at in sorted(bodies)]
    count, header = count_and_base(raw)
    result = labels(raw)
    assert count == len(result)
    return [(header + unpack_from("<H", raw, 2 + 2 * i)[0], None, value, [i])
            for i, value in enumerate(result)]


def main():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, current = map(base.NdsImage.open, (native.CLEAN, parent.ROM))
    arms = [image.read_file(native.ARM) for image in (clean, current)]
    assert native.digest(arms[1]) == release["target_ARM9_sha256"]
    inventory, _, _ = native.scoped_inventory()
    groups = []
    for route, indices in enumerate(BLOCKS):
        path = f"/data/SC{route}.DK4"
        archives = [image.read_file(path) for image in (clean, current)]
        banks = [native.IlnkContainer.parse(archive).blocks for archive in archives]
        for n in indices:
            japanese, english = [bank[n] for bank in banks]
            a, b = [inventory(arm, block)[0] for arm, block in zip(arms, (japanese, english), strict=True)]
            before = stage.offsets(a, stage.logical_end(japanese))
            after = stage.offsets(b, stage.logical_end(english))
            assert list(before.values()) == list(after.values())
            records = []
            for original, target in zip(a, b, strict=True):
                word, src, dst = original["word"], original["offset"], target["offset"]
                assert word == target["word"], (path, n, src, dst)
                assert [before[p] for p in original["ancestor_0100_offsets"]] == [
                        after[p] for p in target["ancestor_0100_offsets"]]
                if word not in (stage.SPEECH, stage.STYLE, *stage.MENU):
                    continue
                orig, cur = [bytes.fromhex(command["whole_command_hex"]) for command in (original, target)]
                for jp, en in zip(text_records(orig, word), text_records(cur, word), strict=True):
                    pos, selector, value, slots = jp
                    old_at, old_selector, old_value, old_slots = en
                    assert selector == old_selector and slots == old_slots
                    words = value.decode("cp932")
                    localized = old_value.decode("cp932")
                    records.append(dict(file_path=path, block=n, source_command_offset=src,
                        current_command_offset=dst, source_offset=src + pos, current_offset=dst + old_at,
                        source_record_index=japanese[:src + pos].count(b"\0"),
                        native_command_word=word, selector=selector, slots=slots, source_body_hex=value.hex(),
                        current_body_hex=old_value.hex(), Japanese=words, current_English=localized))
            counts = dict(Counter(hex(row["native_command_word"]) for row in records))
            groups.append(dict(route=route, block=n, file_path=path, context=CONTEXT[route],
                source_block_sha256=native.digest(japanese), current_block_sha256=native.digest(english),
                source_archive_sha256=native.digest(archives[0]), current_archive_sha256=native.digest(archives[1]),
                native_commands=len(a), counts=counts, records=records))
    ROOT.mkdir()
    base.save(ROOT / "paired_source.json", dict(clean_sha256=release["clean_input_sha256"],
        candidate_sha256=release["candidate_sha256"], profile=release["profile"], groups=groups,
        complete_source_current_binding=True, editorial_review_pending=True, new_coverage_credit=0))
    print(f"Paired {sum(len(g['records']) for g in groups)} records in {len(groups)} blocks.", flush=True)


if __name__ == "__main__":
    main()
