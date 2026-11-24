"""Trace the five archived COMMON payloads through storage and the native getter."""

from collections import Counter
from pathlib import Path
from struct import unpack_from

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import MESSAGE_COUNT, common_message_entries
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_azores_wording_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, sha256, write


COMMON = "/COMMON/MESFILE.DK4"
ARM = "/__arm9__.bin"
KEYS = (284, 318, 750, 751, 752)
GETTER = 0x0205528C
RELEASE = Path("releases/all_routes_editorial_20261124_yard_numerals_candidate/verification/registered_release_verification.json")
OUT = Path("translations/editorial_checkpoints/shared_display_20261123/archived_message_storage_20261124.json")


def offsets(payload, target):
    start = payload.find(target)
    while start != -1:
        yield start
        start = payload.find(target, start + 1)


def payloads(image):
    for file_id, path, payload in image.iter_files():
        yield dict(path=path, file_id=file_id), payload
    for path, payload in image.iter_components():
        yield dict(path=path), payload
    for processor, overlays in (("ARM9", image.rom.loadArm9Overlays()), ("ARM7", image.rom.loadArm7Overlays())):
        for number, overlay in overlays.items():
            if overlay.compressed:
                yield dict(processor=processor, decompressed_overlay=number, file_id=overlay.fileID), bytes(overlay.data)


def inventory(image, *, clean):
    common = image.read_file(COMMON)
    arm = image.read_file(ARM)
    directory = common_message_entries(common, arm, clean=True) if clean else common_rows(common, arm)
    assert len(directory) == MESSAGE_COUNT
    blocks = IlnkContainer.parse(common).blocks
    block_starts = unpack_from(f"<{len(blocks) + 1}I", common, 8)
    archived = {}
    for key in KEYS:
        row = directory[key]
        start, end = row.block_offset, row.block_offset + len(row.text)
        assert start < end <= row.copy_end and blocks[row.block][start:end] == row.text
        terminator_is_stored = blocks[row.block][end:end + 1] == b"\0"
        assert terminator_is_stored or end == row.copy_end
        owners = [slot.message_id for slot in directory if slot.block == row.block
                  and slot.block_offset < end and start < slot.copy_end]
        assert owners == [key], (key, owners)
        archived[key] = dict(block=row.block, record=row.record_index, offset_in_record=row.start,
                             block_offset=start, copy_end=row.copy_end, visible_end=end,
                             terminator_is_stored=terminator_is_stored,
                             archive_offset=block_starts[row.block] + start, arm9_table_offset=row.table_offset,
                             exact_hex=row.text.hex(), text=row.text.decode("cp932"), native_copy_owners=owners,
                             exact_payload_occurrences=[])

    paths, asset_count = [], 0
    for ref, raw in payloads(image):
        asset_count += 1
        paths.extend(ref | {"offset": at} for at in offsets(raw.upper(), b"\\COMMON\\MESFILE.DK4\0"))
        for key, result in archived.items():
            target = directory[key].text
            for at in offsets(raw, target):
                end = at + len(target)
                result["exact_payload_occurrences"].append(ref | {"offset": at, "followed_by_NUL": raw[end:end + 1] == b"\0"})
    assert paths == [{"path": ARM, "offset": 0x1435BC}]
    for result in archived.values():
        occurrences = result["exact_payload_occurrences"]
        assert occurrences == [{"path": COMMON, "file_id": 337, "offset": result["archive_offset"],
                                "followed_by_NUL": result["terminator_is_stored"]}]
    return directory, dict(archive_sha256=sha256(common).hexdigest(), arm9_sha256=sha256(arm).hexdigest(),
                           native_slots_checked=len(directory), stored_assets_scanned=asset_count,
                           archive_filename_occurrences=paths, archived_records=archived)


def load_adjacent_records(ctx, directory):
    groups = {block: [row for row in directory if row.block == block] for block in (4, 9)}
    warm = [row for rows in groups.values() for row in rows]
    queries = warm + [directory[key] for key in (750, 284, 751, 318, 752, 284)]
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    observed = Counter()
    key_reads = []
    previous_block = None
    for row in queries:
        previous = len(provider.reads)
        pointer = get(GETTER - 0x02000000, row.message_id)
        actual = bytes(cpu.mem_read(pointer, len(row.text) + 1))
        assert actual == row.text + b"\0", (row.message_id, pointer, actual.hex())
        reads = provider.reads[previous:]
        assert bool(reads) == (previous_block != row.block)
        previous_block = row.block
        observed[row.block] += 1
        if row.message_id in KEYS:
            key_reads.append(dict(message_ID=row.message_id, block=row.block, pointer=pointer,
                                  body_and_terminator_hex=actual.hex(), file_reads=reads))
    assert bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    return dict(getter=GETTER, requests=len(queries), distinct_ids=len(warm), requests_by_block=dict(observed),
                exact_archived_reads=key_reads, file_reads=provider.reads, file_opens=provider.opens,
                registered_native_input=ctx.receipt() | {"captain": 3})


def main():
    release = read(RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"]
    ctx = RegisteredRuntime(RELEASE, release["own_registered_startup"], captain=3)
    _, clean = inventory(NdsImage.open(CLEAN), clean=True)
    directory, installed = inventory(ctx.image, clean=False)
    assert installed["archive_sha256"] == release["target_COMMON_sha256"]
    assert installed["arm9_sha256"] == release["target_ARM9_sha256"]
    native = load_adjacent_records(ctx, directory)
    print({"requests": native["requests"], "distinct_ids": native["distinct_ids"], "file_reads": len(native["file_reads"]),
           "clean_matches": {key: len(row["exact_payload_occurrences"]) for key, row in clean["archived_records"].items()},
           "installed_matches": {key: len(row["exact_payload_occurrences"]) for key, row in installed["archived_records"].items()}})
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
                    release=reference(RELEASE), clean=clean, installed=installed, native_offline=native,
                    asset_search_scope="Exact raw message bodies in NitroFS, CPU binaries and decompressed CPU overlays.",
                    remaining="A gameplay caller could still compute or forward one of the five IDs. The direct getter fixture does not activate or identify such a path.",
                    ROM_changed=False, ordinary_gameplay=False, new_editorial_credit=0))


if __name__ == "__main__":
    main()
