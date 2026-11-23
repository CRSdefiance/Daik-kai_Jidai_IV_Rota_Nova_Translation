"""Bind the retail town trend events to the current text and play evidence."""

from pathlib import Path
from struct import unpack_from

from dk4tool.formats.ilnk import IlnkContainer
from scripts.observe_baltic_seoul_town_20261123 import ROOT as TOWN_RUNS
from scripts.observe_seoul_tavern_decline_20261123 import RELEASE
from scripts.play_special_target_battle_20261123 import ROOT as BATTLE_RUNS
from scripts.reconcile_class_names_20261123 import c_string, type_name, word
from scripts.reconcile_retail_event_coverage_20261123 import (
    ARCHIVE_LOADER_SPANS, BOOK, STORY_COUNTS, TREND_PROOF, index_events,
)
from scripts.stage_azores_wording_20261123 import ARM, BASE, digest_bytes
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram


OUT = Path("translations/editorial_checkpoints/shared_display_20261123/town_trend_catalogue_current_20261123.json")
RELEASES = Path("releases")
DEPENDENCIES = (
    "20261123_hodram_late_story_wraps", "20261122_hodram_B181_B200",
    "20261122_istanbul_tobacco", "20261122_osaka_glass",
    "20261122_lil_lessons_and_maria_scenes", "20261121_athens_london_trends",
    "20261121_alexandria_dialogue", "20261121_lisbon_fragrance_wraps", "20261121_hodram_execution",
)


def verification(name):
    return RELEASES / f"all_routes_editorial_{name}_candidate/verification"


def seals(name):
    path = verification(name) / "registered_release_verification.json"
    info = read(path)
    assert digest(info["candidate"]) == info["candidate_sha256"]
    return info, reference(path)


def town_names(image, capture_path, frame, allowed_hash):
    arm = image.read_file(ARM)
    run = read(capture_path)
    assert run["ROM_sha256"] == allowed_hash and run["cold_boot"] and not run["savestate_loaded"]
    sample, = [row for row in run["read_only_pause_RAM_snapshots"] if row["frame"] == frame]
    raw = read_ram(sample)
    assert arm[0xCB178:0xCB184] == raw[0xCB178:0xCB184]
    _, get = get_machine(arm, raw)
    towns = get(0xCB178)
    assert type_name(raw, word(raw, towns + 4 + 114 * 108)) == "6CAdman"
    names = []
    for index in range(114):
        obj = towns + 4 + index * 108
        vtable = word(raw, obj)
        assert type_name(raw, vtable) == "5CTown"
        getter = word(raw, vtable + 8)
        pointer = get(getter - BASE, obj)
        raw_name = c_string(raw, pointer, 128)
        names.append(dict(town=index, original_name_getter=getter, string_address=pointer,
                          exact_hex=raw_name.hex(), name=raw_name[:-1].decode("cp932")))
    return names, dict(capture=reference(capture_path), read_only_frame=sample)


def archive_blocks(image, route):
    return IlnkContainer.parse(image.read_file(f"/data/SC{route}.DK4")).blocks


def is_trend(event_bytes, row):
    _, kind, start, size, *_ = row
    if kind != 7 or size != 12:
        return False
    descriptor, = unpack_from("<I", event_bytes, start + 4)
    facility = (descriptor >> 16) & 15
    comparison = (descriptor >> 22) & 3
    calendar = event_bytes[start + 8:start + 12].hex()
    return not descriptor & (1 << 24) and (facility, comparison, calendar) in {
        (0, 1, "ff1fffff"), (4, 1, "ff1fffff"), (0, 3, "ff120bff")}


def editorial_dependencies():
    deps = {}
    for name in DEPENDENCIES:
        info, release = seals(name)
        review = verification(name) / "registered_review.json"
        assert digest(review) == read(verification(name).parent / "checksums.json")["verification/registered_review.json"]
        image = NdsImage.open(info["candidate"])
        deps[name] = (info, release, reference(review), [archive_blocks(image, route) for route in range(4)])
    return deps


def admitted_gameplay(deps):
    amsterdam = BOOK / "amsterdam_bread_gameplay_20261121_v1.json"
    old = read(amsterdam)
    assert old["natural_activation"] and old["ordinary_new_game_and_square_inputs"]
    assert old["event"]["native_event_completion"] == 1 and len(old["panels"]) == 13
    yield 2, "amsterdam", old["event"]["source_event"], amsterdam, "20261121_hodram_execution"
    seoul = BOOK / "lisbon_seoul_trend_gameplay_20261121_v1.json"
    old = read(seoul)
    assert old["natural_activation"] and old["all_changes_from_ordinary_play"]
    run, = [r for r in old["town_runs"] if r["city"] == "seoul"]
    assert run["event"]["completion_getter"] == 1 and run["finished_recruitment_before_trend"]
    yield 3, "seoul", run["event"]["original_event"], seoul, "20261121_hodram_execution"
    lisbon = verification("20261121_lisbon_fragrance_wraps") / "verified_lisbon.json"
    old = read(lisbon)
    assert old["natural_activation"] and old["original_notice_dismissal_and_Square_return"]
    assert old["event"]["completion_getter"] == 1
    yield 1, "lisbon", old["event"]["original_event"], lisbon, "20261121_lisbon_fragrance_wraps"
    european = verification("20261121_athens_london_trends") / "verified_trends.json"
    old = read(european)
    assert old["natural_activation"] and old["exact_native_glyph_matches"]
    for city, result in old["original_event_completion"].items():
        assert result["completion_getter"] == 1
        yield 1, city, result["original_event"], european, "20261121_athens_london_trends"
    istanbul = verification("20261122_istanbul_tobacco") / "verified_ordinary_square.json"
    old = read(istanbul)
    assert old["natural_square_activation"] and old["native_completion"]["completion_getter"] == 1
    # This replay is sealed against the Osaka Glass predecessor. Its Hodram
    # Istanbul block is also exact on the subsequent Istanbul release.
    assert old["candidate_sha256"] == deps["20261122_osaka_glass"][0]["candidate_sha256"]
    yield 1, "istanbul", old["event"], istanbul, "20261122_osaka_glass"


def main():
    release = read(RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(release["manifest"]) == release["manifest_sha256"]
    manifest = read(release["manifest"])
    reviews = {Path(p) for p in manifest["batches"]}
    clean, current = map(NdsImage.open, (CLEAN, release["candidate"]))
    original_arm, arm = (image.read_file(ARM) for image in (clean, current))
    assert digest_bytes(arm) == release["target_ARM9_sha256"]
    trend = read(TREND_PROOF)
    native = {}
    for dependency in trend["clean_identical_native_dependencies"]:
        start, end = (dependency[k] - BASE for k in ("address", "end_exclusive"))
        assert arm[start:end] == original_arm[start:end]
        assert digest_bytes(arm[start:end]) == dependency["sha256"]
        native[f"0x{start+BASE:08X}"] = dependency
    assert all(arm[start:end] == original_arm[start:end] for start, end in ARCHIVE_LOADER_SPANS)
    clean_names, clean_game = town_names(
        clean, BATTLE_RUNS / "clean_fish_approach/capture/capture_report.json", 4800, release["clean_input_sha256"])
    current_names, current_game = town_names(
        current, TOWN_RUNS / "riga/capture/capture_report.json", 3200, release["predecessor"]["candidate_sha256"])
    deps = editorial_dependencies()
    assert all(Path(review["path"]) in reviews for _, _, review, _ in deps.values())
    ordinary = {}
    for route, city, event, path, key in admitted_gameplay(deps):
        info, tested_build, _, scripts = deps[key]
        assert read(path)["candidate_sha256"] == info["candidate_sha256"]
        ordinary[(route, event["event_ID"])] = dict(city=city, source_event=event, gameplay_receipt=reference(path),
            tested_release=tested_build, observed_block_sha256=digest_bytes(scripts[route][event["script_block"]]))
    results, appears = [], set()
    for route, count in enumerate(STORY_COUNTS):
        prefix = f"/data/EV{route}.DK4"
        event_bytes = current.read_file(prefix)
        assert clean.read_file(prefix) == event_bytes
        jp, en = (archive_blocks(image, route) for image in (clean, current))
        fixed = [row for row in index_events(event_bytes, count) if is_trend(event_bytes, row)]
        earlier = trend["routes"][route]
        assert digest_bytes(event_bytes) == earlier["archive_sha256"] and len(fixed) == len(earlier["entries"]) == 20
        for orig, event in zip(fixed, earlier["entries"], strict=True):
            event_id, kind, start, size, action, opcode, block = orig
            assert (event_id, kind, start, action, opcode, block) == (event["event_ID"], event["category"],
                event["event_record_offset"], event["action_offset"], int(event["action_word"], 16), event["script_block"])
            assert event_bytes[start:start + size].hex() == event["record_hex"]
            earlier_block = event["prior_review"]
            assert digest_bytes(jp[block]) == earlier_block["clean_block_sha256"]
            installed = digest_bytes(en[block])
            assert event["facility"] in (0, 4)
            town = event["town"]
            appears.add(town)
            record = dict(route=route, town=town, English=current_names[town]["name"], Japanese=clean_names[town]["name"],
                          event_archive=prefix, script_archive=earlier["scene_archive"], original_event=event,
                          installed_block_sha256=installed)
            if installed == earlier_block["current_block_sha256"]:
                record["installed_editorial_binding"] = dict(type="exact earlier block", source=reference(TREND_PROOF))
            else:
                match = next((key for key, (_, _, _, scripts) in deps.items() if scripts[route][block] == en[block]), None)
                assert match, (route, block, installed)
                _, build, notes, _ = deps[match]
                record["installed_editorial_binding"] = dict(type="exact later registered block", release=build, review=notes)
            if observation := ordinary.pop((route, event_id), None):
                assert observation["source_event"]["record_hex"] == event["record_hex"]
                assert observation["city"] == record["English"].lower()
                record["ordinary_play"] = observation | dict(
                    same_installed_dialogue_bytes=observation["observed_block_sha256"] == installed)
            results.append(record)
    assert not ordinary and len(appears) == 20 and len(results) == 80
    riga, = [row for row in current_names if row["name"] == "Riga"]
    assert riga["town"] == 10 and riga["town"] not in appears
    write(OUT, dict(release=reference(RELEASE), exact_candidate_sha256=release["candidate_sha256"],
                    original_selector_dependencies=native, town_table=dict(clean=clean_names, installed=current_names,
                    original_snapshot=clean_game, installed_snapshot=current_game),
                    cities_without_authored_event=[row["name"] for row in current_names if row["town"] not in appears],
                    records=results, current_ordinary_trend_runs=0, earlier_ordinary_event_count=6,
                    other_activation_scope="See each town's focused or offline verification. The census supplies no new ordinary activation.",
                    Riga_scope=dict(town=riga, authored_events_on_four_routes=0,
                                    retained_name_reason="Riga is the established English name for リガ and matches the complete town heading."),
                    new_editorial_credit=0, full_goal_complete=False))
    print(f"{len(results)} selectors in {len(appears)} towns. Six ordinary activations on record.")


if __name__ == "__main__":
    main()
