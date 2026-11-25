"""Bind the 20 reviewed town trends to the original retail event records."""

from pathlib import Path
from struct import unpack_from

from scripts import replay_amsterdam_bread_20261121 as replay


base, native = replay.base, replay.active.parent.native
BOOK = Path("translations/editorial_checkpoints/SharedText_20261110_v1")
EARLIER = BOOK / "town_trend_exchange_coverage_20261121_v1.json"
OUTPUT = BOOK / "town_trend_event_entries_20261121_v1.json"
CLEAN_ARCHIVE_DATA_AT = 96


def get_events(archive, blocks):
    counts = unpack_from("<9H", archive, 10)
    starts = unpack_from("<10I", archive, 40)
    action_start, action_end = unpack_from("<2I", archive, 0x4C)
    action_base = CLEAN_ARCHIVE_DATA_AT + action_start
    event_id = 0
    hits = []
    for category, count in enumerate(counts):
        offset = CLEAN_ARCHIVE_DATA_AT + starts[category]
        for _ in range(count):
            first, second = unpack_from("<2I", archive, offset)
            size = (second & 255) * 4
            assert size >= 8
            action_index = (first >> 16) & 0x3FFF
            action_offset = action_base + 2 * action_index
            assert action_offset + 2 <= CLEAN_ARCHIVE_DATA_AT + action_end
            action, = unpack_from("<H", archive, action_offset)
            if action >> 12 == 2 and (block := action & 4095) in blocks:
                assert size == 12 and not (second & 1 << 24) and category == 7
                hits.append(dict(event_ID=event_id, event_record_offset=offset,
                    action_index=action_index, action_offset=action_offset, action_word=f"{action:04x}",
                    record_hex=archive[offset:offset+size].hex(), script_block=block,
                    category=category, town=(second >> 8) & 255, facility=(second >> 16) & 15,
                    date_comparison=(second >> 22) & 3, date_fields_hex=archive[offset+8:offset+12].hex(),
                    prior_review=blocks[block]))
            event_id += 1
            offset += size
        assert offset == CLEAN_ARCHIVE_DATA_AT + starts[category+1]
    assert len(hits) == 20 and {r["script_block"] for r in hits} == set(blocks)
    return hits


def main():
    assert not OUTPUT.exists()
    release = base.load(replay.active.RELEASE)
    assert base.digest(replay.active.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    earlier = base.load(EARLIER)
    clean, current = map(base.NdsImage.open, (native.CLEAN, replay.active.ROM))
    clean_arm, arm = [image.read_file(native.ARM) for image in (clean, current)]
    assert native.digest(arm) == release["target_ARM9_sha256"]
    spans = ((0x220D8, 0x22ECC), (0x2324C, 0x23260), (0x82F80, 0x82F88), (0x90D8C, 0x90E14), (0xCCEAC, 0xCCED8))
    assert all(arm[a:b] == clean_arm[a:b] for a,b in spans)
    routes = []
    for route in range(4):
        events, scripts = (f"/data/{file}{route}.DK4" for file in ("EV", "SC"))
        original, active = [image.read_file(events) for image in (clean, current)]
        assert original == active
        clean_blocks, current_blocks = [native.IlnkContainer.parse(image.read_file(scripts)).blocks
                                        for image in (clean, current)]
        review = {g["block"]: g for g in earlier["groups"] if g["file_path"] == scripts}
        for block, row in review.items():
            assert native.digest(current_blocks[block]) == row["current_block_sha256"]
            assert native.digest(clean_blocks[block]) == row["clean_block_sha256"]
        bound = get_events(original, review)
        assert sum(row["date_fields_hex"] == "ff1fffff" and row["date_comparison"] == 1 for row in bound) == 19
        assert [(row["town"], row["date_fields_hex"]) for row in bound if row["date_comparison"] == 3] == [(7, "ff120bff")]
        routes.append(dict(route=route,event_archive=events,scene_archive=scripts,archive_sha256=native.digest(active),
                           entries=bound))
    assert len({tuple((r["town"], r["facility"], r["date_comparison"], r["date_fields_hex"]) for r in route["entries"])
                for route in routes}) == 1
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        previous_coverage_sha256=base.digest(EARLIER), routes=routes, exact_event_entries=80,
        same_day_of_month_as_birthday_per_route=19, separate_stockholm_date_rule_per_route=1,
        clean_identical_native_dependencies=[dict(address=0x2000000+a, end_exclusive=0x2000000+b,
                                                  sha256=native.digest(arm[a:b])) for a,b in spans],
        evidence_scope="Original event storage, native date comparison, facility and town selectors. Gameplay is separate."))
    print("Bound all 80 source-identical event entries with exact conditions and reviewed story blocks.")


if __name__ == "__main__":
    main()

