"""Pair Rafael's remaining midroute wrap leads with their complete exchanges."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path

from scripts import cleanup_hodram_early_and_midroute_wraps_20261122 as checkpoint
from scripts import register_hodram_early_and_midroute_wraps_20261122 as release
from scripts.pair_rafael_charlotte_and_maria_20261122 import RELATIVE, jump, logical_end, text_records

base, native = release.base, release.native
ARCHIVE = "/data/SC0.DK4"
BLOCKS = (100, 101, 102, 103, 104, 105, 108, 115, 117, 118, 120, 128, 133, 136)
EARLIER = tuple(
    Path(f"translations/rafael_{part}_contextual_final_review_{version}.json")
    for part, version in (("B85_B100", "v1"), ("B101_B120", "v1"), ("B121_B140", "v2"))
)
OUTPUT = Path("translations/editorial_checkpoints/rafael_midroute_exchanges_20261122/paired_source.json")
PARENT_QUEUE = Path(
    "translations/editorial_checkpoints/rafael_fleet_and_crew_exchanges_20261122/current_wrap_queue.json"
)


def bind_block(number, blocks, arms, archive_hashes, old_rows, leads, inventory):
    original, current = blocks
    clean_commands, current_commands = (inventory(arm, block)[0] for arm, block in zip(arms, blocks, strict=True))
    assert [r["word"] for r in clean_commands] == [r["word"] for r in current_commands]
    offsets = {left["offset"]: right["offset"] for left, right in zip(clean_commands, current_commands, strict=True)}
    offsets[logical_end(original)] = logical_end(current)
    rows, wrap_leads, branches = [], [], 0
    for source, installed in zip(clean_commands, current_commands, strict=True):
        word = source["word"]
        at, stored = source["offset"], installed["offset"]
        left, right = (bytes.fromhex(command["whole_command_hex"]) for command in (source, installed))
        assert offsets[at + source["native_extent"]] == stored + installed["native_extent"]
        assert [offsets[value] for value in source["ancestor_0100_offsets"]] == installed["ancestor_0100_offsets"]
        if word in RELATIVE:
            assert offsets[jump(left, at)] == jump(right, stored)
            branches += 1
        if word not in (0x4000, 0x4100, 0x2100, 0x2200):
            continue
        if word == 0x4000:
            assert left[:6] == right[:6]
        for (src_pos, actor, jp, slots), (dst_pos, installed_actor, en, installed_slots) in zip(
            text_records(left, word), text_records(right, word), strict=True
        ):
            assert (actor, slots) == (installed_actor, installed_slots)
            clean_at, current_at = at + src_pos, stored + dst_pos
            old = old_rows.pop(clean_at)
            if actor is None:
                assert old["source_index"] == slots[0]
                assert left.hex() == old["source_choice_object_hex"]
            selector = bytes([actor]) if actor is not None else b""
            assert (selector + jp).hex() == old["source_hex"]
            ident = old["id"]
            rows.append(dict(
                id=ident, speaker=old["speaker"], kind=old["kind"], selector=actor, slots=slots,
                source_record_index=old["source_reference"].get("record_index"), native_command_word=word,
                source_offset=clean_at, current_offset=current_at, source_command_offset=at,
                current_command_offset=stored, source_body_hex=jp.hex(), current_body_hex=en.hex(),
                source_command_hex=left.hex(), current_command_hex=right.hex(),
                Japanese=jp.decode("cp932"), current_English=en.decode("cp932"),
            ))
            if lead := leads.pop(current_at, None):
                assert lead["stored_body_hex"] == en.hex()
                wrap_leads.append(dict(id=ident, offset=current_at, rows=lead["rows"]))
    assert not old_rows and not leads, (number, list(old_rows), list(leads))
    return dict(
        route=0, file_path=ARCHIVE, block=number, records=rows, open_wrap_leads=wrap_leads,
        native_commands=len(clean_commands), relative_branches=branches,
        source_block_sha256=native.digest(original), current_block_sha256=native.digest(current),
        source_archive_sha256=archive_hashes[0], current_archive_sha256=archive_hashes[1],
    )


def main(check_parent=False):
    selected = release.parent if check_parent else release
    registered, queue = (base.load(path) for path in (selected.RELEASE, PARENT_QUEUE if check_parent else checkpoint.QUEUE))
    candidate = base.digest(selected.ROM)
    assert candidate == queue["candidate_sha256"] == registered["candidate_sha256"]
    assert base.digest(base.REGISTRY) == registered["registry_sha256"]
    assert base.digest(native.CLEAN) == registered["clean_input_sha256"]
    images = [base.NdsImage.open(path) for path in (native.CLEAN, selected.ROM)]
    arms = [image.read_file(native.ARM) for image in images]
    archives = [image.read_file(ARCHIVE) for image in images]
    archive_hashes = [native.digest(data) for data in archives]
    assert archive_hashes[1] == registered["target_SC0_sha256"]
    banks = [native.IlnkContainer.parse(data).blocks for data in archives]
    inventory, _, _ = native.scoped_inventory()
    previous = [row for path in EARLIER for row in base.load(path)["records"] if row.get("block") in BLOCKS]
    groups = []
    for number in BLOCKS:
        old_rows = {r["source_reference"]["offset"]: r for r in previous if r["block"] == number}
        leads = {r["offset"]: r for r in queue["records"]
                 if r["file_path"] == ARCHIVE and r["block"] == number and "reviewed" not in r}
        groups.append(bind_block(number, [bank[number] for bank in banks], arms, archive_hashes,
                                 old_rows, leads, inventory))
    counts = Counter(row["kind"] for group in groups for row in group["records"])
    wrap_count = sum(len(group["open_wrap_leads"]) for group in groups)
    assert counts == {"progressive": 258, "system-FE": 17, "typed-choice-label": 5} and wrap_count == 21
    if not check_parent:
        assert not OUTPUT.exists()
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        base.save(OUTPUT, dict(
            candidate_sha256=candidate, clean_sha256=registered["clean_input_sha256"], groups=groups,
            profile=registered["profile"], earlier_reviews={str(path): base.digest(path) for path in EARLIER},
            contextual_review_pending=True, new_review_credit=0,
        ))
    print(f"Bound {sum(counts.values())} Rafael texts and {wrap_count} open wraps in {len(groups)} complete exchanges.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--check-parent", action="store_true")
    main(parser.parse_args().check_parent)
