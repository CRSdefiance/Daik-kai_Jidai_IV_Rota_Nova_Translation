"""Bind Maria's B116 contextual draft and prove ownership of its four story panels."""

from pathlib import Path

from scripts import register_hodram_sera_nagarpur_and_kuhn_20261122 as parent


base, native = parent.base, parent.native
ARCHIVE, BLOCK = "/data/SC3.DK4", 116
PAIRED = Path("translations/editorial_checkpoints/palace_and_london_20261122/maria_B116_paired_source.json")
EARLIER = Path("translations/maria330_integrated_final_review_v1.json")
MANUSCRIPT = Path(__file__).with_name("maria_admiral_story_20261122.md")
OUTPUT = Path("translations/editorial_checkpoints/maria_admiral_story_20261122/contextual_draft.json")


def main():
    release, paired, prior = map(base.load, (parent.RELEASE, PAIRED, EARLIER))
    assert release["candidate_sha256"] == base.digest(parent.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == paired["clean_sha256"] == base.digest(native.CLEAN)
    assert (ARCHIVE, BLOCK) == (paired["file_path"], paired["block"])
    source, current = (base.NdsImage.open(path).read_file(ARCHIVE) for path in (native.CLEAN, parent.ROM))
    source_block, current_block = (native.IlnkContainer.parse(data).blocks[BLOCK] for data in (source, current))
    assert native.digest(source) == paired["source_archive_sha256"]
    assert native.digest(source_block) == paired["source_block_sha256"]
    assert native.digest(current_block) == paired["current_block_sha256"]
    original_pages = {row["id"]: row["registered_native_pages"] for row in prior["records"]
                      if row["id"] in {"DK4_MES_B116_R0041", "DK4_MES_B116_R0051"}}
    assert len(original_pages) == 2
    decisions = {}
    for line in MANUSCRIPT.read_text(encoding="utf-8").splitlines():
        if line.startswith("| R") and not line.startswith("| Record"):
            record, english, reason = (part.strip() for part in line.split("|")[1:-1])
            decisions["DK4_MES_B116_" + record] = dict(english=english, reason=reason)

    records, continuation_offsets = [], []
    for row in paired["records"]:
        record = row["id"]
        proposal = decisions.pop(record)
        retain = proposal["english"].startswith("Retain ")
        for label, block in (("source", source_block), ("current", current_block)):
            offset = row[label + "_command_offset"]
            command = bytes.fromhex(row[label + "_command_hex"])
            assert block[offset:offset + len(command)] == command
            assert command[5] == row["source_selector"]
        pages = original_pages.get(record, [])
        if pages:
            assert retain and len(pages) == 2 and row["source_selector"] == 254
            assert pages[0]["header_offset"] == row["current_command_offset"]
            for page in pages:
                start, body = page["offset"], bytes.fromhex(page["exact_stored_hex"])
                assert start == page["header_offset"] + 5 and body[0] == 254
                assert current_block[start:start + len(body)] == body and current_block[start + len(body)] == 0
                assert current_block[start - 5:start] == bytes.fromhex("0040ffff00")
            continuation_offsets.append(pages[1]["header_offset"])
        records.append(row | dict(decision="retention" if retain else "prose", finding=proposal["reason"],
                                  proposed_English=None if retain else proposal["english"], exact_registered_pages=pages))
    assert not decisions and len(records) == 26
    assert continuation_offsets == paired["retained_continuation_offsets"]
    assert sum(row["decision"] == "prose" for row in records) == 8
    proof = dict(candidate_sha256=release["candidate_sha256"], clean_sha256=paired["clean_sha256"],
                 source_archive_sha256=native.digest(source), current_archive_sha256=native.digest(current),
                 source_block_sha256=native.digest(source_block), current_block_sha256=native.digest(current_block),
                 paired_source=str(PAIRED), paired_source_sha256=base.digest(PAIRED),
                 manuscript=str(MANUSCRIPT), manuscript_sha256=base.digest(MANUSCRIPT), file_path=ARCHIVE, block=BLOCK,
                 records=records, proven_continuation_offsets=continuation_offsets,
                 fresh_formatting_and_registered_integration_pending=True, new_release_credit=0)
    assert not OUTPUT.exists()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT, proof)
    print("Bound all 26 B116 records and both two-page owners. Eight dialogue drafts await native formatting.")


if __name__ == "__main__":
    main()
