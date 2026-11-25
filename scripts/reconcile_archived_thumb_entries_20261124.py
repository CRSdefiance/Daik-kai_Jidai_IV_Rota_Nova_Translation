"""Check short Thumb branches and potential interworking into archived COMMON callers."""

from struct import iter_unpack

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import reconcile_archived_message_reader_20261124 as prior
from scripts import reconcile_tunis_editorial_acceptance_20261124 as previous_acceptance
from scripts import register_lisbon_roster_galley_20261124 as current
from scripts import verify_archived_message_storage_20261124 as archive
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write


OUT = prior.OUT.with_name("archived_thumb_entry_scope_20261124.json")
FIRST, LAST = 0x02052D00, 0x02055900
KEYS = (284, 318, 750, 751, 752)
BASE = prior.BASE


def signed_branch(half):
    if half & 0xF800 == 0xE000:
        field, modulus = half & 0x7FF, 0x800
    elif 0xD000 <= half < 0xDE00:
        field, modulus = half & 0xFF, 0x100
    else:
        return None
    return field - modulus if field & (modulus // 2) else field


def scan(image, destinations):
    window = set(range(FIRST, LAST, 2))
    short, interworking, mode_words, from_outside = [], [], [], []
    for name, base, data in prior.reader.inventory.components(image.rom):
        interworking.extend((name, *item) for item in prior.linked_immediates(data, base, window))
        for index, (half,) in enumerate(iter_unpack("<H", data[:len(data) & ~1])):
            offset = signed_branch(half)
            if offset is not None:
                pc = base + index * 2
                to = pc + 4 + offset * 2
                if to in destinations and not prior.START <= pc < prior.END:
                    short.append((name, pc, to))
                if to in window and not FIRST <= pc < LAST:
                    from_outside.append((name, pc, to))
        for lane in range(4):
            aligned = data[lane:lane + ((len(data) - lane) & ~3)]
            mode_words.extend((name, base + lane + 4 * index, word)
                              for index, (word,) in enumerate(iter_unpack("<I", aligned))
                              if word & 1 and word - 1 in window)
    return short, interworking, mode_words, from_outside


def arm_overlaps(findings, clean, installed):
    codec = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    overlaps = []
    for name, pc, target in findings:
        assert name == "ARM9 section 0"
        start = pc & ~3
        raw = installed[start - BASE:start - BASE + 4]
        assert raw == clean[start - BASE:start - BASE + 4]
        inst, = codec.disasm(raw, start)
        overlaps.append(dict(halfword_address=pc, apparent_thumb_target=target, ARM_word_address=start,
                             exact_hex=raw.hex(), ARM_decode=f"{inst.mnemonic} {inst.op_str}"))
    return overlaps


def main():
    release, bounded, storage = map(read, (current.RELEASE, prior.bounded.OUT, archive.OUT))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"] and bounded["archived_ids"] == list(KEYS)
    clean, installed = map(NdsImage.open, (CLEAN, current.ROM))
    census = read(prior.bounded.prior.OUT)["references"]
    wrappers = {row["entry"] for row in census}
    assert len(wrappers) == 13
    continuity = previous_acceptance.archived_arguments(clean, installed, release)
    assert continuity["aligned_callers"] == len(census) == bounded["fully_bounded_census_sites"] == 827
    targets = wrappers | set(range(prior.START, prior.END, 2))
    before, after = (scan(image, targets) for image in (clean, installed))
    assert before[0] == after[0] and len(after[0]) == 51
    assert before[1] == [] and after[1] == [prior.DUEL_REFERENCE]
    assert before[2] == after[2] == []
    assert before[3] == after[3]
    assert prior.references(clean, wrappers, installed=False) == [prior.EXPECTED[0]]
    assert continuity["reader_references"] == [prior.EXPECTED[0], prior.DUEL_REFERENCE]
    arm = installed.read_file(current.ARM)
    ja = clean.read_file(current.ARM)
    assert all(pc % 4 == 2 and FIRST <= pc < LAST for _, pc, _ in after[0])
    overlaps = arm_overlaps(after[0], ja, arm)
    outside = arm_overlaps(after[3], ja, arm)
    _, current_storage = archive.inventory(installed, clean=False)
    assert current_storage["archive_sha256"] == release["target_COMMON_sha256"]
    references = {}
    for key in KEYS:
        old = storage["installed"]["archived_records"][str(key)]
        native = current_storage["archived_records"][key]
        assert native["exact_hex"] == old["exact_hex"]
        references[key] = dict(original=storage["clean"]["archived_records"][str(key)], installed=native)
    write(OUT, dict(
        candidate_sha256=release["candidate_sha256"], original_and_current_archive_refs=references,
        reader_and_wrappers=sorted(wrappers), checked_thumb_entry_interval=[FIRST, LAST],
        exact_shared_short_halfword_overlaps=overlaps, adjacent_short_encodings_into_interval=outside,
        odd_address_words_at_any_byte_alignment=after[2],
        clean_long_Thumb_or_ARM_BLX_immediates=before[1], installed_long_Thumb_or_ARM_BLX_immediates=after[1],
        matching_prior_census_sites=continuity["aligned_callers"], bound_argument_continuity=continuity,
        existing_bound_arguments=reference(prior.bounded.OUT), exact_reader_scope=reference(prior.OUT),
        storage_proof=reference(archive.OUT),
        scope="The only long Thumb or ARM immediate interworking entry found in the interval is the registered duel helper. The stored short encodings preserve their complete ARM words. Arbitrary computed target addresses remain open.",
        new_editorial_credit=0, ordinary_gameplay_added=False, ROM_changed=False,
    ))
    print(f"Checked {len(overlaps)} short encodings, {len(outside)} adjacent encodings, and {len(census)} prior sites.")


if __name__ == "__main__":
    main()
