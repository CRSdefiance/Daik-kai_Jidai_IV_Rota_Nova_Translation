"""Bind Rafael's next ten complete exchanges to the current cumulative ROM."""

from collections import Counter
from pathlib import Path

from scripts import cleanup_hodram_recruitment_and_sails_20261123 as checkpoint
from scripts import register_hodram_recruitment_and_sails_20261123 as release
from scripts.prepare_london_guild_assignments_20261118 import text_records

base, native = release.base, release.native
ARCHIVE = "/data/SC0.DK4"
BLOCKS = (144, 146, 148, 149, 153, 154, 155, 156, 157, 160)
EARLIER = Path("translations/rafael_B141_B160_final_review_v1.json")
OUTPUT = Path("translations/editorial_checkpoints/rafael_basra_and_map_keys_20261123/paired_source.json")


def main():
    assert not OUTPUT.exists()
    manifest, queue, former = map(base.load, (release.RELEASE, checkpoint.QUEUE, EARLIER))
    target = base.digest(release.ROM)
    assert target == manifest["candidate_sha256"] == queue["candidate_sha256"]
    assert base.digest(base.REGISTRY) == manifest["registry_sha256"]
    assert base.digest(release.MANIFEST) == manifest["manifest_sha256"]
    assert base.digest(native.CLEAN) == manifest["clean_input_sha256"]
    clean, current = (base.NdsImage.open(path) for path in (native.CLEAN, release.ROM))
    arm = [image.read_file(native.ARM) for image in (clean, current)]
    raw = [image.read_file(ARCHIVE) for image in (clean, current)]
    hashes = [native.digest(data) for data in raw]
    assert hashes[1] == manifest["target_SC0_sha256"]
    assert native.digest(arm[1]) == manifest["target_ARM9_sha256"]
    banks = [native.IlnkContainer.parse(data).blocks for data in raw]
    inventory, _, _ = native.scoped_inventory()
    groups = []
    for block in BLOCKS:
        payload = [bank[block] for bank in banks]
        commands = [inventory(a, data)[0] for a, data in zip(arm, payload, strict=True)]
        assert [row["word"] for row in commands[0]] == [row["word"] for row in commands[1]]
        indices = [{row["offset"]: i for i, row in enumerate(bank)} for bank in commands]
        owners = {row["source_reference"]["offset"]: row for row in former["records"] if row["block"] == block}
        lead_by_offset = {row["offset"]: row for row in queue["records"]
            if row["file_path"] == ARCHIVE and row["block"] == block and "reviewed" not in row}
        records, leads = [], []
        for left, right in zip(*commands, strict=True):
            word = left["word"]
            if word not in (0x4000, 0x2100):
                assert word not in (0x4100, 0x2200)
                continue
            assert [indices[0][at] for at in left["ancestor_0100_offsets"]] == [
                indices[1][at] for at in right["ancestor_0100_offsets"]]
            bodies = [text_records(bytes.fromhex(row["whole_command_hex"]), word) for row in (left, right)]
            for (source_at, source_actor, ja, slots), (current_at, actor, en, current_slots) in zip(*bodies, strict=True):
                assert (source_actor, slots) == (actor, current_slots)
                source_offset, current_offset = left["offset"] + source_at, right["offset"] + current_at
                owner = owners.pop(source_offset)
                assert (owner.get("source_selector") if word == 0x2100 else owner["source_selector"]) == actor
                prefix = bytes([actor]) if actor is not None else b""
                assert owner["source_hex"] == (prefix + ja).hex()
                ident = owner["id"]
                if lead := lead_by_offset.pop(current_offset, None):
                    assert lead["stored_body_hex"] == en.hex()
                    leads.append(dict(id=ident, offset=current_offset, rows=lead["rows"]))
                records.append(dict(id=ident, speaker=owner["speaker"], selector=actor, slots=slots,
                    source_record_index=owner["source_reference"].get("record_index"), native_command_word=word,
                    source_offset=source_offset, current_offset=current_offset, source_command_offset=left["offset"],
                    current_command_offset=right["offset"], source_body_hex=ja.hex(), current_body_hex=en.hex(),
                    source_command_hex=left["whole_command_hex"], current_command_hex=right["whole_command_hex"],
                    Japanese=ja.decode("cp932"), current_English=en.decode("cp932")))
        assert not owners and not lead_by_offset and leads
        groups.append(dict(route=0, file_path=ARCHIVE, block=block, records=records, open_wrap_leads=leads,
            earlier_scene_context=next(row["context"] for row in former["records"] if row["block"] == block),
            source_block_sha256=native.digest(payload[0]), current_block_sha256=native.digest(payload[1]),
            source_archive_sha256=hashes[0], current_archive_sha256=hashes[1]))
    counts = Counter(row["native_command_word"] for group in groups for row in group["records"])
    leads = sum(len(group["open_wrap_leads"]) for group in groups)
    assert counts == {0x4000: 207, 0x2100: 6} and leads == 14
    OUTPUT.parent.mkdir(exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=target, clean_sha256=manifest["clean_input_sha256"], groups=groups,
        earlier_review=dict(path=str(EARLIER), sha256=base.digest(EARLIER)),
        wrap_queue_sha256=base.digest(checkpoint.QUEUE), contextual_review_pending=True, new_editorial_credit=0))
    print(f"Bound {sum(counts.values())} texts and {leads} wrap leads across Rafael's Basra and Map Key exchanges.")


if __name__ == "__main__":
    main()
