"""Rebind four prepared Hodram and Lil scenes to the latest registered candidate."""

from pathlib import Path

from scripts import register_rafael_six_followup_exchanges_20261122 as active
from scripts.cleanup_rafael_six_followup_exchanges_20261122 import QUEUE


base, native = active.base, active.native
EARLIER = Path("translations/editorial_checkpoints/palace_and_london_20261122")
PACKETS = {
    "hodram_pirates": (1, 17, 73),
    "hodram_cristina_recruitment": (1, 85, 56),
    "lil_rumor": (2, 26, 111),
    "lil_rafael_introduction": (2, 133, 50),
}
OUTPUT = Path("translations/editorial_checkpoints/hodram_and_lil_followups_20261122/paired_source.json")


def main():
    assert not OUTPUT.exists()
    release, queue = map(base.load, (active.RELEASE, QUEUE))
    candidate = base.digest(active.ROM)
    assert release["candidate_sha256"] == queue["candidate_sha256"] == candidate
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, current = map(base.NdsImage.open, (native.CLEAN, active.ROM))
    inventory, _, _ = native.scoped_inventory()
    arms = clean.read_file(native.ARM), current.read_file(native.ARM)
    rechecked = []
    for packet_name, (route, number, count) in PACKETS.items():
        path = EARLIER / f"{packet_name}_paired_source.json"
        evidence = base.load(path)
        assert evidence["clean_sha256"] == release["clean_input_sha256"]
        previous, = evidence["groups"]
        archive = f"/data/SC{route}.DK4"
        assert (previous["file_path"], previous["block"]) == (archive, number)
        raw = [image.read_file(archive) for image in (clean, current)]
        original, installed = [native.IlnkContainer.parse(data).blocks[number] for data in raw]
        source_hash, installed_hash = [native.digest(data) for data in raw]
        assert source_hash == previous["source_archive_sha256"]
        assert installed_hash == release[f"target_SC{route}_sha256"]
        assert native.digest(original) == previous["source_block_sha256"]
        assert native.digest(installed) == previous["current_block_sha256"]
        source, target = [{r["offset"]: r for r in inventory(arm, block)[0]}
                          for arm, block in zip(arms, (original, installed), strict=True)]
        assert len(source) == len(target) == previous["native_commands"]
        records, wrap_leads = [], []
        by_offset = {}
        for row in previous["records"]:
            left = source[row["source_command_offset"]]
            right = target[row["current_command_offset"]]
            assert left["word"] == right["word"] == row["native_command_word"]
            for block, side in ((original, "source"), (installed, "current")):
                at = row[f"{side}_offset"]
                content = bytes.fromhex(row[f"{side}_body_hex"])
                if row["selector"] is not None:
                    assert block[at] == row["selector"]
                    at += 1
                assert block[at:at+len(content)] == content and block[at+len(content)] == 0
            records.append(row | dict(source_command_hex=left["whole_command_hex"],
                                      current_command_hex=right["whole_command_hex"]))
            by_offset[row["current_offset"]] = row
        assert len(records) == count
        for lead in queue["records"]:
            if (lead["file_path"], lead["block"]) != (archive, number) or "reviewed" in lead:
                continue
            row = by_offset[lead["offset"]]
            assert row["current_body_hex"] == lead["stored_body_hex"]
            wrap_leads.append(dict(offset=lead["offset"], source_record_index=row["source_record_index"], rows=lead["rows"]))
        rechecked.append(previous | dict(current_archive_sha256=installed_hash, earlier_pair=str(path),
            earlier_pair_sha256=base.digest(path), earlier_candidate_sha256=evidence["candidate_sha256"],
            exact_block_unchanged=True, records=records, open_wrap_leads=wrap_leads))
    assert sum(len(group["records"]) for group in rechecked) == 290
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        profile=release["profile"], groups=rechecked, contextual_review_pending=True, new_review_credit=0))
    print("Bound all 290 source and current texts across four Hodram and Lil exchanges.")


if __name__ == "__main__":
    main()
