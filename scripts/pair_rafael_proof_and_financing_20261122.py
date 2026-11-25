"""Bind Rafael's next two early-game exchanges and financing choice."""

from pathlib import Path

from scripts import register_rafael_athens_and_maria_crew_20261122 as release
from scripts.prepare_london_guild_assignments_20261118 import text_records
from scripts.stage_forest_expeditions_20261118 import RELATIVE, jump, logical_end


base, native = release.base, release.native
ARCHIVE = "/data/SC0.DK4"
OUTPUT = Path("translations/editorial_checkpoints/rafael_proof_and_financing_20261122/paired_source.json")
BRIEFING = Path(__file__).with_name("rafael_proof_briefing_20261122.md")
EARLIER = {
    41: Path("translations/rafael_B36_B41_contextual_final_review_v1.json"),
    44: Path("translations/rafael_opening_contextual_final_review_v1.json"),
}


def main():
    assert not OUTPUT.exists()
    registered = base.load(release.RELEASE)
    assert base.digest(release.ROM) == registered["candidate_sha256"]
    assert base.digest(base.REGISTRY) == registered["registry_sha256"]
    assert base.digest(native.CLEAN) == registered["clean_input_sha256"]
    images = tuple(map(base.NdsImage.open, (native.CLEAN, release.ROM)))
    archives = tuple(image.read_file(ARCHIVE) for image in images)
    assert native.digest(archives[1]) == registered["target_SC0_sha256"]
    banks = [native.IlnkContainer.parse(a).blocks for a in archives]
    arms = [image.read_file(native.ARM) for image in images]
    inventory, _, _ = native.scoped_inventory()
    reports, known_leads = [], []
    for number, earlier in EARLIER.items():
        banks_for_block = [bank[number] for bank in banks]
        groups = [inventory(arm, data)[0] for arm, data in zip(arms, banks_for_block, strict=True)]
        source, current = groups
        assert [c["word"] for c in source] == [c["word"] for c in current]
        corresponding = dict(zip((c["offset"] for c in source), (c["offset"] for c in current), strict=True))
        corresponding[logical_end(banks_for_block[0])] = logical_end(banks_for_block[1])
        earlier_names = {r["id"]: r.get("speaker") for r in base.load(earlier)["records"]
                         if r.get("block") == number}
        records, jump_count = [], 0
        for clean, active in zip(source, current, strict=True):
            at, active_at = clean["offset"], active["offset"]
            command = clean["word"]
            raw, translated = (bytes.fromhex(c["whole_command_hex"]) for c in (clean, active))
            assert corresponding[at + clean["native_extent"]] == active_at + active["native_extent"]
            assert [corresponding[p] for p in clean["ancestor_0100_offsets"]] == active["ancestor_0100_offsets"]
            if command in RELATIVE:
                assert corresponding[jump(raw, at)] == jump(translated, active_at)
                jump_count += 1
            if command not in (0x4000, 0x2100):
                continue
            for left, right in zip(text_records(raw, command), text_records(translated, command), strict=True):
                offset, selector, original, slots = left
                en_offset, en_selector, installed, en_slots = right
                assert (selector, slots) == (en_selector, en_slots)
                if command == 0x4000:
                    assert raw[:6] == translated[:6]
                    ordinal = banks_for_block[0][:at+5].count(b"\0")
                    ident = f"DK4_MES_B{number}_R{ordinal:04d}"
                else:
                    ident = f"SC0_B{number}_NATIVE_CHOICE_{at}_{slots[0]}"
                records.append(dict(id=ident, speaker=earlier_names.get(ident), opcode=command,
                    source_selector=selector, slots=slots, Japanese=original.decode("cp932"),
                    English=installed.decode("cp932"),
                    source_reference=dict(command_offset=at, offset=at+offset, exact_command_hex=raw.hex(),
                                          exact_body_hex=original.hex()),
                    current_reference=dict(command_offset=active_at, offset=active_at+en_offset,
                                           exact_command_hex=translated.hex(), exact_body_hex=installed.hex())))
                if active_at+en_offset in {949, 2091, 4851, 5439}:
                    known_leads.append(ident)
        reports.append(dict(block=number, records=records, complete_command_count=len(source), relative_sites=jump_count,
            source_block_sha256=native.digest(banks_for_block[0]), current_block_sha256=native.digest(banks_for_block[1]),
            earlier_review=str(earlier), earlier_review_sha256=base.digest(earlier)))
    assert [sum(r["opcode"] == 0x4000 for r in group["records"]) for group in reports] == [27, 115]
    assert [r["slots"] for r in reports[-1]["records"] if r["opcode"] == 0x2100] == [[0], [1]]
    assert len(set(known_leads)) == 4
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=registered["candidate_sha256"], clean_sha256=registered["clean_input_sha256"],
        file_path=ARCHIVE, source_archive_sha256=native.digest(archives[0]), current_archive_sha256=native.digest(archives[1]),
        groups=reports, known_wrap_leads=known_leads, briefing_manuscript=str(BRIEFING),
        briefing_manuscript_sha256=base.digest(BRIEFING), new_release_credit=0))
    print("Bound both early exchanges, all 142 text owners, both financing captions, and four wrap leads.")


if __name__ == "__main__":
    main()
