"""Bind every retail event selector to its reviewed clean and installed story block."""

import json
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.reconcile_editorial_acceptance_20261123 import ARM, OUT, RELEASES, digest, read, reference


PACKAGE = RELEASES / "all_routes_editorial_20261123_supply_ratio_hint_candidate"
RELEASE = PACKAGE / "verification/registered_release_verification.json"
BOOK = OUT.parent.parent / "SharedText_20261110_v1"
TREND_PROOF = BOOK / "town_trend_event_entries_20261121_v1.json"
RETAIL_PROOF = BOOK / "retail_story_archive_selection_20261121_v1.json"
OBSERVED = OUT.with_name("ordinary_shared_encounters_20261123.json")
REPORT = OUT.with_name("retail_event_coverage_current_20261123.json")
HEADER_SIZE = 96
STORY_COUNTS = (343, 325, 336, 303)
ARCHIVE_LOADER_SPANS = ((0x24134, 0x241CC), (0x24214, 0x24230),
                        (0xD0398, 0xD0520), (0xD1EE0, 0xD2128), (0x134530, 0x134590))


def index_events(data, script_count):
    assert data[:2] == b"VE" and unpack_from("<I", data, 4)[0] == len(data) - HEADER_SIZE
    counts = unpack_from("<9H", data, 10)
    assert unpack_from("<H", data, 8)[0] == sum(counts) == script_count
    starts = unpack_from("<10I", data, 40)
    action_start, action_end = unpack_from("<2I", data, 0x4C)
    assert action_start == starts[-1] <= action_end <= len(data) - HEADER_SIZE
    events = []
    for category, count in enumerate(counts):
        offset, end = (HEADER_SIZE + starts[i] for i in (category, category + 1))
        assert HEADER_SIZE <= offset <= end <= HEADER_SIZE + action_start
        for _ in range(count):
            assert offset + 8 <= end
            first, second = unpack_from("<2I", data, offset)
            length = (second & 255) * 4
            assert 8 <= length <= end - offset
            action = action_start + 2 * ((first >> 16) & 0x3FFF)
            assert action_start <= action <= action_end - 2
            action += HEADER_SIZE
            opcode, = unpack_from("<H", data, action)
            assert opcode >> 12 == 2
            block = opcode & 0xFFF
            events.append([len(events), category, offset, length, action, opcode, block])
            offset += length
        assert offset == end
    assert sorted(row[-1] for row in events) == list(range(script_count))
    return events


def main():
    assert not REPORT.exists()
    release = read(RELEASE)
    candidate = release["candidate_sha256"]
    assert digest(release["candidate"]) == candidate
    assert digest("work/clean.nds") == release["clean_input_sha256"]
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    clean, current = map(NdsImage.open, ("work/clean.nds", release["candidate"]))
    clean_arm, installed_arm = (image.read_file(ARM) for image in (clean, current))
    trend, retail, ordinary = map(read, (TREND_PROOF, RETAIL_PROOF, OBSERVED))
    for start, stop in ARCHIVE_LOADER_SPANS:
        assert clean_arm[start:stop] == installed_arm[start:stop]
    for dependency in trend["clean_identical_native_dependencies"]:
        start, stop = (dependency[key] - 0x02000000 for key in ("address", "end_exclusive"))
        assert sha256(installed_arm[start:stop]).hexdigest() == dependency["sha256"]
    route_receipt = PACKAGE / "verification/current_route_coverage_20261123.json"
    assert digest(route_receipt) == read(PACKAGE / "checksums.json")[route_receipt.relative_to(PACKAGE).as_posix()]
    routes = read(route_receipt)
    assert routes["exact_credited_clean_positions"] == 24092 and routes["manifest_prefix_exact"]
    results = []
    for route, expected in enumerate(STORY_COUNTS):
        ev, sc = (f"/data/{kind}{route}.DK4" for kind in ("EV", "SC"))
        prior = trend["routes"][route]
        assert prior["route"] == route and prior["event_archive"] == ev and prior["scene_archive"] == sc
        original_events, events = (image.read_file(ev) for image in (clean, current))
        assert original_events == events and sha256(events).hexdigest() == prior["archive_sha256"]
        original_scene, scene = (image.read_file(sc) for image in (clean, current))
        assert sha256(scene).hexdigest() == release[f"target_SC{route}_sha256"] == routes["routes"][sc]["installed_archive_sha256"]
        assert len(IlnkContainer.parse(original_scene).blocks) == len(IlnkContainer.parse(scene).blocks) == expected
        entries = index_events(events, expected)
        for formerly in prior["entries"]:
            event_id, category, offset, size, action, opcode, block = entries[formerly["event_ID"]]
            assert (event_id, category, offset, action, opcode, block) == (
                formerly["event_ID"], formerly["category"], formerly["event_record_offset"], formerly["action_offset"],
                int(formerly["action_word"], 16), formerly["script_block"])
            assert events[offset:offset + size].hex() == formerly["record_hex"]
        case = retail["versions"]["registered"]["cases"][route]
        assert case["source"] == sc
        alternate = case["test_archive"]
        alt = current.read_file(alternate)
        assert alt == clean.read_file(alternate) and sha256(alt).hexdigest() == case["test_archive_sha256"]
        results.append(dict(event_file=ev, clean_and_installed_event_sha256=prior["archive_sha256"],
            script_file=sc, clean_script_sha256=sha256(original_scene).hexdigest(),
            installed_script_sha256=sha256(scene).hexdigest(), event_to_block_mapping=entries,
            bound_prior_town_trend_events=len(prior["entries"]), alternate_story_archive=alternate,
            alternate_story_archive_sha256=case["test_archive_sha256"]))

    assert ordinary["natural_encounters_observed"] and ordinary["ordinary_battery_save_gameplay"]
    assert sum(len(route["event_to_block_mapping"]) for route in results) == 1307
    report = dict(candidate_sha256=candidate, clean_input_sha256=release["clean_input_sha256"],
        exact_credited_clean_story_positions=routes["exact_credited_clean_positions"],
        event_mapping_columns=["event_ID", "category", "record_offset", "record_bytes", "action_offset", "action_word", "scene_block"],
        event_to_reviewed_script_block_count=1307, scopes=results, bound_prior_town_trend_events=80,
        four_stock_archive_loader_compatibility=dict(exact_code_spans=ARCHIVE_LOADER_SPANS,
            prior_offline_tests=reference(RETAIL_PROOF), potential_other_callers_outside_test=True),
        prior_observed_gameplay=dict(receipt=reference(OBSERVED), cases=list(ordinary["cases"]),
            common_holds=ordinary["common_holds"], story_holds=ordinary["story_holds"],
            unvisited_variants=ordinary["unvisited_variants"]),
        bound_evidence=[reference(path) for path in (RELEASE, route_receipt, TREND_PROOF)],
        current_new_gameplay=False, new_editorial_credit=0)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("All 1,307 retail event entries map one to one to the reviewed story blocks. Carried forward 80 exact town trend entries.")


if __name__ == "__main__":
    main()
