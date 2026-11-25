"""Rebind the remaining Hodram wrap leads to the registered cumulative ROM."""

from pathlib import Path

from scripts import register_hodram_b221_b260_wrap_fixes_20261123 as current


base, native = current.base, current.native
PACKET = current.stage.paired.OUTPUT
QUEUE = Path("translations/editorial_checkpoints/hodram_b221_b260_wrap_fixes_20261123/current_wrap_queue.json")
OUTPUT = PACKET.with_name("b261_b310_current_binding.json")
ARCHIVE = current.stage.ARCHIVE


def verify_command(block, row, side):
    start = row[f"{side}_command_offset"]
    command = bytes.fromhex(row[f"{side}_command_hex"])
    assert block[start:start + len(command)] == command, (side, row["id"])


def main():
    packet, queue, release = map(base.load, (PACKET, QUEUE, current.RELEASE))
    assert base.digest(current.ROM) == queue["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(current.parent.ROM) == packet["candidate_sha256"] == release["predecessor"]["candidate_sha256"]
    assert base.digest(native.CLEAN) == packet["clean_sha256"] == release["clean_input_sha256"]
    clean, installed = (base.NdsImage.open(path).read_file(ARCHIVE) for path in (native.CLEAN, current.ROM))
    assert native.digest(installed) == release["target_SC1_sha256"]
    source_blocks, current_blocks = (native.IlnkContainer.parse(data).blocks for data in (clean, installed))
    remaining = {(row["file_path"], row["block"], row["offset"])
                 for row in queue["records"] if "reviewed" not in row}
    bound, reviewed = [], 0
    for group in packet["groups"]:
        block = group["block"]
        if not 261 <= block <= 310:
            continue
        assert group["file_path"] == ARCHIVE and group["source_archive_sha256"] == native.digest(clean)
        a, b = source_blocks[block], current_blocks[block]
        assert native.digest(a) == group["source_block_sha256"]
        assert native.digest(b) == group["current_block_sha256"]
        for row in group["records"]:
            verify_command(a, row, "source")
            verify_command(b, row, "current")
        leads = group["open_wrap_leads"]
        for row in leads:
            remaining.remove((ARCHIVE, block, row["offset"]))
        reviewed += len(group["records"])
        bound.append(dict(block=block, source_block_sha256=native.digest(a), current_block_sha256=native.digest(b),
                          bound_records=len(group["records"]), open_wrap_leads=[row["id"] for row in leads]))
    assert not remaining and len(bound) == 14 and reviewed == 305
    assert sum(len(row["open_wrap_leads"]) for row in bound) == 17
    proof = dict(candidate_sha256=release["candidate_sha256"], source_packet=str(PACKET), source_packet_sha256=base.digest(PACKET),
                 queue_sha256=base.digest(QUEUE), archive=ARCHIVE, clean_archive_sha256=native.digest(clean),
                 installed_archive_sha256=native.digest(installed), groups=bound, bound_records=reviewed,
                 all_source_and_installed_commands_exact=True, editorial_decisions_pending=True)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == proof
    else:
        base.save(OUTPUT, proof)
    print("Bound 305 exact texts and 17 open wrap leads across 14 unchanged Hodram exchanges.")


if __name__ == "__main__":
    main()
