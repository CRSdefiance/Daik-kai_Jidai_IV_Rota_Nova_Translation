"""Rebind Hodram's next full exchanges, original notices, and native choices."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path

from scripts import register_rafael_fleet_and_crew_exchanges_20261122 as release
from scripts.prepare_london_guild_assignments_20261118 import text_records


base, native = release.base, release.native
ARCHIVE = "/data/SC1.DK4"
CHECKPOINTS = {
    "B0_B23": (5, 6, 7, 15, 23),
    "B24_B53": (26,),
    "B54_B60": (56,),
    "B71_B80": (72, 73, 75, 76, 78, 79),
    "B81_B89": (84, 87, 89),
    "B91_B110": (91, 95),
}
OUTPUT = Path("translations/editorial_checkpoints/hodram_early_and_midroute_wraps_20261122/paired_source.json")
PREVIOUS_QUEUE = Path("translations/editorial_checkpoints/rafael_charlotte_and_maria_20261122/current_wrap_queue.json")
QUEUE = release.stage.BATCH / "current_wrap_queue.json"


def bind_block(number, records, blocks, archive_hashes, arms, leads):
    original, current = blocks
    block_hashes = [native.digest(payload) for payload in blocks]
    inventory, _, _ = native.scoped_inventory()
    commands = [
        {command["offset"]:command for command in inventory(arm, block)[0]}
        for arm, block in zip(arms, blocks, strict=True)
    ]
    by_source = {}
    rebased_leads = []
    for entry in records:
        source, registered = (entry[key] for key in ("source_reference", "registered_reference"))
        assert source["archive_sha256"] == archive_hashes[0]
        assert [source["block_sha256"], registered["block_sha256"]] == block_hashes
        left, right = (commands[n][ref["command_offset"]] for n, ref in enumerate((source, registered)))
        word, selector, slots = (entry[key] for key in ("native_command_word", "selector", "slots"))
        assert left["word"] == right["word"] == word
        raw, stored = (bytes.fromhex(command["whole_command_hex"]) for command in (left, right))
        assert stored.hex() == registered["exact_command_hex"]
        selected = []
        for command, data, ref in ((left, raw, source), (right, stored, registered)):
            rel, actor, body, instance = next(r for r in text_records(data, word) if r[0] == ref["offset"]-command["offset"])
            assert (actor, instance) == (selector, slots)
            selected.append(body)
        meaning, current_body = selected
        assert meaning.hex() == source["exact_body_hex"]
        prefix = bytes([selector]) if selector is not None else b""
        assert (prefix + current_body).hex() == registered["exact_stored_hex"]
        ident = entry["id"]
        assert source["offset"] not in by_source
        by_source[source["offset"]] = dict(id=ident, speaker=entry["speaker"], selector=selector, slots=slots,
            source_record_index=int(ident.rsplit("_R", 1)[1]) if ident.startswith("DK4_MES_") else None,
            native_command_word=word, source_offset=source["offset"], current_offset=registered["offset"],
            source_command_offset=left["offset"], current_command_offset=right["offset"],
            source_body_hex=meaning.hex(), current_body_hex=current_body.hex(), source_command_hex=raw.hex(),
            current_command_hex=stored.hex(), Japanese=meaning.decode("cp932"), current_English=current_body.decode("cp932"))
        if lead := leads.pop(registered["offset"], None):
            assert lead["stored_body_hex"] == current_body.hex()
            rebased_leads.append(dict(id=ident, offset=lead["offset"], rows=lead["rows"]))
    assert not leads
    expected_source = {command["offset"] + part[0] for command in commands[0].values()
                       if command["word"] in (0x4000, 0x4100, 0x2100)
                       for part in text_records(bytes.fromhex(command["whole_command_hex"]), command["word"])}
    assert by_source.keys() == expected_source
    return dict(route=1, file_path=ARCHIVE, block=number, records=[by_source[k] for k in sorted(by_source)],
        open_wrap_leads=rebased_leads, source_block_sha256=block_hashes[0], current_block_sha256=block_hashes[1],
        source_archive_sha256=archive_hashes[0], current_archive_sha256=archive_hashes[1],
        source_and_current_native_command_counts=[len(bank) for bank in commands])


def main(check_only=False):
    registered = base.load(release.parent.RELEASE if check_only else release.RELEASE)
    candidate_rom = release.stage.ROM if check_only else release.ROM
    candidate = base.digest(candidate_rom)
    queue = base.load(PREVIOUS_QUEUE if check_only else QUEUE)
    if not check_only:
        assert not OUTPUT.exists() and queue["candidate_sha256"] == candidate == registered["candidate_sha256"]
        assert base.digest(base.REGISTRY) == registered["registry_sha256"]
    assert base.digest(native.CLEAN) == registered["clean_input_sha256"]
    clean, current = [base.NdsImage.open(path) for path in (native.CLEAN, candidate_rom)]
    arms = [image.read_file(native.ARM) for image in (clean, current)]
    files = [image.read_file(ARCHIVE) for image in (clean, current)]
    hashes = [native.digest(data) for data in files]
    assert hashes[1] == registered["target_SC1_sha256"]
    banks = [native.IlnkContainer.parse(data).blocks for data in files]
    groups, references = [], {}
    for tag, numbers in CHECKPOINTS.items():
        path = Path(f"releases/all_routes_editorial_20261122_hodram_{tag}_candidate/verification/registered_review.json")
        proof = base.load(path)
        references[str(path)] = base.digest(path)
        for number in numbers:
            records = [row for row in proof["records"] if row["block"] == number]
            leads = {r["offset"]:r for r in queue["records"] if r["file_path"] == ARCHIVE
                     and r["block"] == number and "reviewed" not in r}
            groups.append(bind_block(number, records, [bank[number] for bank in banks], hashes, arms, leads))
    counts = Counter(r["native_command_word"] for group in groups for r in group["records"])
    lead_count = sum(len(group["open_wrap_leads"]) for group in groups)
    assert sum(counts.values()) == 282 and counts[0x2100] == 4 and lead_count == 24
    if not check_only:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=registered["clean_input_sha256"], groups=groups,
            earlier_reviews=references, contextual_review_pending=True, new_review_credit=0))
    print(f"Bound {sum(counts.values())} Hodram texts, {lead_count} wrap leads and {counts[0x2100]} original choice labels.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("--check-only", action="store_true")
    main(cli.parse_args().check_only)
