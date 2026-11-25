"""Bound the stock file-by-ID and byte-range routes around the COMMON reader."""

from pathlib import Path
from struct import iter_unpack, pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_ARCH_ARM, UC_MODE_ARM, Uc
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R5, UC_ARM_REG_R6
from unicorn.arm_const import UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_SP

from scripts.checkpoint_pending_shared_native_20261115 import branch_hits, components
from scripts.inventory_native_common_calls import locally_resolved_argument
from scripts.reconcile_archived_message_arguments_20261124 import addressing_candidates
from scripts.reconcile_archived_message_reader_20261124 import linked_immediates
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


ROOT = Path("translations/editorial_checkpoints/shared_display_20261123")
OUT = ROOT / "archived_common_filesystem_paths_20261124.json"
RELEASE = Path("releases/all_routes_editorial_20261124_maria_captured_ship_candidate/verification/registered_release_verification.json")
ARM = "/__arm9__.bin"
COMMON = "/COMMON/MESFILE.DK4"
BASE, SIZE = 0x02000000, 0x400000
STACK, VIEW = 0x023D1000, 0x023D2000
ARCHIVE, BOOT_HEADER = 0x0237576C, 0x027FFE00
FILENAME, FILE_ID, BYTE_RANGE, DISPATCH = 0x020DED50, 0x020DEDA0, 0x020DEE1C, 0x020DE5F4
ID_SITES = {0x020DED78, 0x020DF768, 0x020DF850, 0x020DF9B8, 0x020EA8B4, 0x020EC99C}
RANGE_SITES = {0x020DE374, 0x020DE3D8, 0x020DF94C}
OVERLAY_FILE_CALLS = (0x020DF768, 0x020DF850, 0x020DF9B8)
SDK_COMMANDS = {0x020DED14: 8, 0x020DEDDC: 6, 0x020DEE3C: 7, 0x020DEF0C: 0, 0x020DF08C: 4}
AUDIO_CALLS = (0x02001490, 0x020014A8, 0x020014C0)
AUDIO_SLOT = 0x0237A640
AUDIO_FILENAME = "/sound_data.sdat"
WRITER = 0x020EA638

LOCKS = (
    (0x02001474, 0x020014C4), (0x0200155C, 0x02001564),
    (0x020DE318, 0x020DE43C), (0x020DE444, 0x020DE4B8),
    (0x020DED08, 0x020DEF10), (0x020DF07C, 0x020DF09C),
    (0x020DF104, 0x020DF2C4), (0x020DF73C, 0x020DFA28),
    (0x020EA2DC, 0x020EA2FC), (0x020EA638, 0x020EA650),
    (0x020EA86C, 0x020EA8F4), (0x020EAEFC, 0x020EB038),
    (0x020EC928, 0x020EC9C0),
)


def from_arm(arm, start, end):
    return arm[start - BASE:end - BASE]


def words(raw, address, count, base=BASE):
    return unpack_from(f"<{count}I", raw, address - base)


def edges(image, targets):
    return sorted({(owner, pc, dest, kind) for owner, base, data in components(image.rom)
                   for pc, dest, kind in branch_hits(data, base, targets) + list(linked_immediates(data, base, targets))})


def arm_calls(rows, target):
    matched = [(owner, pc, kind) for owner, pc, dest, kind in rows if dest == target]
    assert all(owner == "ARM9 section 0" and kind == "arm_bl" for owner, _, kind in matched)
    return {pc for _, pc, _ in matched}


def source_census(clean, candidate, before, after):
    audio_constructors = {0x020EA86C, 0x020EA650, WRITER, 0x020EA2DC}
    targets = {FILENAME, FILE_ID, BYTE_RANGE, DISPATCH, *audio_constructors}
    original, installed = [edges(rom, targets) for rom in (clean, candidate)]
    assert original == installed
    assert all(not addressing_candidates(rom, targets) for rom in (clean, candidate))
    assert len(arm_calls(original, FILENAME)) == 25
    assert arm_calls(original, FILE_ID) == ID_SITES and arm_calls(original, BYTE_RANGE) == RANGE_SITES
    assert arm_calls(original, DISPATCH) == SDK_COMMANDS.keys()
    assert arm_calls(original, 0x020EA86C) == set(AUDIO_CALLS)
    assert arm_calls(original, 0x020EA650) == {0x020EA8D8}
    assert arm_calls(original, WRITER) == {0x020EAFF8, 0x020EB020}
    assert arm_calls(original, 0x020EA2DC) == {0x020EC98C}
    locks = []
    for start, end in LOCKS:
        body = from_arm(before, start, end)
        assert len(body) == end - start and body == from_arm(after, start, end)
        locks.append(dict(start=start, end=end, exact_sha256=sha256(body).hexdigest()))
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    for site, opcode in SDK_COMMANDS.items():
        start = site - 16
        context = decoder.disasm(from_arm(after, start, site), start)
        assert locally_resolved_argument(context, after, BASE, "r1") == opcode
    return dict(exact_branch_edges=original, byte_locks=locks, dispatch_opcodes=SDK_COMMANDS,
                alternate_simple_address_sources=[], file_id_calls=sorted(ID_SITES), byte_range_calls=sorted(RANGE_SITES))


def card_metadata(path, image):
    with Path(path).open("rb") as rom:
        header = rom.read(0x80)
        pairs = list(iter_unpack("<2I", header[0x40:0x60]))
        rom.seek(pairs[1][0])
        fat = list(iter_unpack("<2I", rom.read(pairs[1][1])))
    assert len(fat) == len(image.rom.files)
    identifiers = image.path_map()
    common_id = identifiers[COMMON]
    common_span = fat[common_id]
    assert common_span[1] - common_span[0] == len(image.read_file(COMMON))
    overlay_ids = []
    overlay_tables = tuple(bytes(table) for table in (image.rom.arm9OverlayTable, image.rom.arm7OverlayTable))
    for (_, length), table in zip(pairs[2:], overlay_tables, strict=True):
        assert length == len(table) and length % 32 == 0
        overlay_ids.extend(fields[6] for fields in iter_unpack("<8I", table))
    assert common_id == 337 and overlay_ids == [0] and identifiers[AUDIO_FILENAME] == 2
    assert image.read_file(AUDIO_FILENAME)[:4] == b"SDAT" and image.read_file(COMMON)[:4] != b"SDAT"
    assert all(not length or start + length <= common_span[0] or start >= common_span[1] for start, length in pairs)
    assert all(fat[ident][1] <= common_span[0] or fat[ident][0] >= common_span[1] for ident in (0, 2))
    return dict(header=header, metadata=pairs, overlay_tables=overlay_tables,
                common_id=common_id, common_span=common_span,
                overlay_file_ids=overlay_ids, sound_file_id=identifiers[AUDIO_FILENAME])


def cpu_for(resident):
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.mem_map(BASE, SIZE)
    cpu.mem_write(BASE, resident)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    return cpu


def boot_and_ranges(arm, card):
    results = []
    fnt, fat, *tables = card["metadata"]
    for mode in (0, 1, 2):
        cpu = cpu_for(arm)
        cpu.mem_map(0x027FC000, 0x4000)
        cpu.mem_write(0x027FFC40, pack("<H", mode))
        cpu.mem_write(BOOT_HEADER, card["header"])
        cpu.emu_start(0x020DF178, 0x020DE444, count=160)
        assert cpu.reg_read(UC_ARM_REG_PC) == 0x020DE444
        values = tuple(cpu.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3))
        supplied = unpack_from("<2I", cpu.mem_read(STACK, 8))
        expected = (0, 0, 0, 0) if mode == 2 else (fat[0], fat[1], fnt[0], fnt[1])
        assert values == (ARCHIVE, 0, *expected[:2]) and supplied == expected[2:]
        attachments = unpack_from("<4I", cpu.mem_read(0x0237575C, 16))
        assert attachments == ((0xFFFFFFFF, 0) * 2 if mode == 2 else (0,) * 4)
        results.append(dict(startup_mode=mode, fat=expected[:2], fnt=expected[2:], attached_overlay_entries=attachments))

    cpu = cpu_for(arm)
    # The preload helper receives these offsets before replacing them with RAM pointers.
    cpu.mem_write(ARCHIVE + 0x20, pack("<4I", *fat, *fnt))
    cpu.reg_write(UC_ARM_REG_R7, ARCHIVE)
    ranges = []
    for start, stop, pair in ((0x020DE358, 0x020DE374, fat), (0x020DE3B4, 0x020DE3D8, fnt)):
        cpu.emu_start(start, stop, count=20)
        args = (cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2), cpu.reg_read(UC_ARM_REG_R3))
        assert args == (ARCHIVE, pair[0], sum(pair))
        ranges.append(dict(call_site=stop, byte_range=args[1:]))

    for processor, pair in enumerate(tables):
        for index in (0, 1, 337):
            cpu = cpu_for(arm)
            cpu.mem_write(STACK + 0x70, pack("<4I", *(value for region in tables for value in region)))
            for reg, val in ((UC_ARM_REG_R1, processor), (UC_ARM_REG_R2, index), (UC_ARM_REG_R3, ARCHIVE)):
                cpu.reg_write(reg, val)
            cpu.emu_start(0x020DF8F8, 0x020DF91C, count=32)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x020DF91C
            assert (cpu.reg_read(UC_ARM_REG_R5), cpu.reg_read(UC_ARM_REG_R6)) == (pair[1], pair[0])
            assert cpu.reg_read(UC_ARM_REG_R7) == index * 32 and cpu.reg_read(UC_ARM_REG_R8) == ARCHIVE
            rejected = bool(cpu.reg_read(UC_ARM_REG_CPSR) & (1 << 29))
            assert rejected == (index * 32 >= pair[1])
            if rejected:
                ranges.append(dict(overlay_processor=processor, index=index, rejected=True))
                continue
            cpu.emu_start(0x020DF934, 0x020DF94C, count=16)
            args = (cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2), cpu.reg_read(UC_ARM_REG_R3))
            assert args == (ARCHIVE, pair[0] + index * 32, sum(pair))
            ranges.append(dict(call_site=0x020DF94C, overlay_processor=processor, index=index, byte_range=args[1:]))
    return dict(bootstrap=results, native_ranges=ranges)


def boot_memory(arm, raw, card, image):
    fnt, fat, *_ = card["metadata"]
    pointers = words(raw, ARCHIVE + 0x20, 6)
    assert pointers[1::2][:2] == (fat[1], fnt[1]) and pointers[4:] == (fat[0], fnt[0])
    assert words(raw, 0x0237575C, 4) == (0,) * 4
    with Path(image).open("rb") as rom:
        for cache, location in ((pointers[0], fat), (pointers[2], fnt)):
            rom.seek(location[0])
            assert raw[cache - BASE:cache - BASE + location[1]] == rom.read(location[1])
    audio = words(raw, AUDIO_SLOT, 1)[0]
    path_literals = []
    for site in AUDIO_CALLS:
        instruction = site - (24 if site == AUDIO_CALLS[0] else 16)
        opcode = words(arm, instruction, 1)[0]
        assert opcode & 0xFFFFF000 == 0xE59F1000
        literal = instruction + 8 + (opcode & 0xFFF)
        path = words(arm, literal, 1)[0]
        assert from_arm(arm, path, path + 16) == b"sound_data.sdat\0"
        path_literals.append(dict(call_site=site, path_literal=literal, path_address=path))
    assert words(raw, audio + 0x78, 2) == (ARCHIVE, card["sound_file_id"])
    assert from_arm(raw, 0x020EA2DC, 0x020EA2FC) == from_arm(arm, 0x020EA2DC, 0x020EA2FC)
    cpu = cpu_for(raw)
    cpu.reg_write(UC_ARM_REG_R0, VIEW)
    cpu.emu_start(0x020EA2DC, 0x020EA2F4, count=16)
    assert unpack_from("<2I", cpu.mem_read(VIEW, 8)) == (ARCHIVE, card["sound_file_id"])
    return dict(fat_ram_address=pointers[0], fnt_ram_address=pointers[2], exact_startup_metadata_bytes=True,
                audio_filename=AUDIO_FILENAME, audio_path_literals=path_literals, active_startup_sound_object=audio,
                native_audio_reopen_file_id=card["sound_file_id"], overlay_attachment_slots_empty=True)


def overlay_file_arguments(arm, card):
    cases = []
    for processor, table in enumerate(card["overlay_tables"]):
        for offset in range(0, len(table), 32):
            record = table[offset:offset + 32]
            overlay_id, file_id = unpack_from("<I", record)[0], unpack_from("<I", record, 24)[0]
            cpu = cpu_for(arm)
            cpu.mem_write(VIEW, record)
            result = VIEW + 0x40
            cpu.reg_write(UC_ARM_REG_R0, result)
            cpu.reg_write(UC_ARM_REG_R1, VIEW)
            cpu.emu_start(0x020DFA00, 0x020DFA20, count=12)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x020DFA20
            assert unpack_from("<2I", cpu.mem_read(result, 8)) == (ARCHIVE, file_id)
            assert file_id != card["common_id"] and file_id in card["overlay_file_ids"]
            cases.append(dict(processor=processor, overlay_id=overlay_id, opened_file_id=file_id,
                shared_adapter=0x020DFA00, file_open_calls=OVERLAY_FILE_CALLS, exact_row_hex=record.hex()))
    return cases


def main():
    release = read(RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    clean, candidate = [NdsImage.open(path) for path in (CLEAN, release["candidate"])]
    before, after = (image.read_file(ARM) for image in (clean, candidate))
    assert sha256(after).hexdigest() == release["target_ARM9_sha256"]
    census = source_census(clean, candidate, before, after)
    cards = [card_metadata(path, image) for path, image in ((CLEAN, clean), (release["candidate"], candidate))]
    tests = [boot_and_ranges(arm, card) | dict(overlay_file_arguments=overlay_file_arguments(arm, card))
             for arm, card in zip((before, after), cards, strict=True)]
    runtime = RegisteredRuntime(RELEASE, release["own_registered_startup"], captain=3)
    state = boot_memory(after, runtime.raw, cards[1], release["candidate"])
    for card in cards:
        del card["header"], card["overlay_tables"]
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        release=reference(RELEASE), startup=reference(release["own_registered_startup"]),
        sdk=census, clean_card=cards[0], installed_card=cards[1], native_clean_and_installed=tests,
        startup_observed_storage=state, prior_common_archive_reader=reference(ROOT / "archived_message_reader_20261124.json"),
        verifier=reference(Path(__file__)),
        archived_ids=[284, 318, 750, 751, 752], ROM_changed=False, new_editorial_credit=0, gameplay_added=False,
        scope="The original card file-ID and direct range calls. The native startup and SDK tests are offline.",
        remaining="No new direct COMMON file open was identified. Computed message arguments and arbitrary indirect resource paths remain separate."))
    print("Bound the six numeric file opens and three raw byte-range sites to their stock resource paths.")


if __name__ == "__main__":
    main()
