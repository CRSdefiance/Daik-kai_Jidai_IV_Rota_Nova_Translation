"""Bind Rafael's Charlotte and first East Asia exchanges to the active release."""

from pathlib import Path

from scripts import cleanup_hodram_and_lil_followups_20261122 as checkpoint
from scripts import register_hodram_and_lil_followups_20261122 as release
from scripts.prepare_london_guild_assignments_20261118 import text_records
from scripts.stage_forest_expeditions_20261118 import RELATIVE, jump, logical_end


base, native = release.base, release.native
ARCHIVE = "/data/SC0.DK4"
BLOCKS = {67: 64, 70: 42, 71: 13, 72: 15}
EARLIER = Path("translations/rafael_B61_B80_contextual_final_review_v1.json")
OUTPUT = Path("translations/editorial_checkpoints/rafael_charlotte_and_maria_20261122/paired_source.json")


def scene_packet(number, banks, arms, old_rows, leads, archive_hashes, inventory):
    original, current = (bank[number] for bank in banks)
    source_commands, current_commands = (inventory(arm, block)[0] for arm, block in zip(arms, (original, current), strict=True))
    assert [r["word"] for r in source_commands] == [r["word"] for r in current_commands]
    addresses = {a["offset"]: b["offset"] for a, b in zip(source_commands, current_commands, strict=True)}
    addresses[logical_end(original)] = logical_end(current)
    owners, revision_leads, branch_count = [], [], 0
    for source, target in zip(source_commands, current_commands, strict=True):
        word = source["word"]
        at, stored = source["offset"], target["offset"]
        left, right = (bytes.fromhex(c["whole_command_hex"]) for c in (source, target))
        assert addresses[at + source["native_extent"]] == stored + target["native_extent"]
        assert [addresses[p] for p in source["ancestor_0100_offsets"]] == target["ancestor_0100_offsets"]
        if word in RELATIVE:
            assert addresses[jump(left, at)] == jump(right, stored)
            branch_count += 1
        if word not in (0x4000, 0x2100, 0x4100):
            continue
        for (src_off, actor, japanese, slots), (dst_off, other, english, target_slots) in zip(
            text_records(left, word), text_records(right, word), strict=True,
        ):
            assert (actor, slots) == (other, target_slots)
            old = old_rows.pop(at + src_off)
            assert bytes.fromhex(old["source_hex"]) == bytes([actor]) + japanese
            assert word == 0x4000 and left[:6] == right[:6]
            owner = dict(id=old["id"], speaker=old["speaker"], selector=actor, slots=slots,
                source_record_index=old["source_reference"]["record_index"], native_command_word=word,
                source_offset=at+src_off, current_offset=stored+dst_off, source_command_offset=at, current_command_offset=stored,
                source_body_hex=japanese.hex(), current_body_hex=english.hex(), source_command_hex=left.hex(),
                current_command_hex=right.hex(), Japanese=japanese.decode("cp932"), current_English=english.decode("cp932"))
            if lead := leads.pop(stored + dst_off, None):
                assert lead["stored_body_hex"] == english.hex()
                revision_leads.append(dict(id=owner["id"], offset=lead["offset"], rows=lead["rows"]))
            owners.append(owner)
    assert not old_rows and not leads and len(owners) == BLOCKS[number]
    return dict(route=0, file_path=ARCHIVE, block=number, records=owners, open_wrap_leads=revision_leads,
        native_commands=len(source_commands), relative_branches=branch_count,
        source_block_sha256=native.digest(original), current_block_sha256=native.digest(current),
        source_archive_sha256=archive_hashes[0], current_archive_sha256=archive_hashes[1])


def main():
    assert not OUTPUT.exists()
    registered, queue = (base.load(path) for path in (release.RELEASE, checkpoint.QUEUE))
    candidate = base.digest(release.ROM)
    assert registered["candidate_sha256"] == queue["candidate_sha256"] == candidate
    assert base.digest(base.REGISTRY) == registered["registry_sha256"]
    assert base.digest(native.CLEAN) == registered["clean_input_sha256"]
    clean, current = map(base.NdsImage.open, (native.CLEAN, release.ROM))
    arms = [image.read_file(native.ARM) for image in (clean, current)]
    archives = [image.read_file(ARCHIVE) for image in (clean, current)]
    archive_hashes = [native.digest(data) for data in archives]
    assert archive_hashes[1] == registered["target_SC0_sha256"]
    banks = [native.IlnkContainer.parse(data).blocks for data in archives]
    inventory, _, _ = native.scoped_inventory()
    older = base.load(EARLIER)["records"]
    groups = []
    for number in BLOCKS:
        old_rows = {r["source_reference"]["offset"]: r for r in older if r.get("block") == number}
        leads = {r["offset"]: r for r in queue["records"] if r["file_path"] == ARCHIVE
                 and r["block"] == number and "reviewed" not in r}
        groups.append(scene_packet(number, banks, arms, old_rows, leads, archive_hashes, inventory))
    assert sum(len(group["open_wrap_leads"]) for group in groups) == 8
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=registered["clean_input_sha256"],
        profile=registered["profile"], groups=groups, earlier_review=str(EARLIER), earlier_review_sha256=base.digest(EARLIER),
        contextual_review_pending=True, new_review_credit=0))
    print("Bound 134 texts and eight wrap leads in four complete Rafael exchanges.", flush=True)


if __name__ == "__main__":
    main()
