"""Adjudicate the shared Gallery duplicates against the displayed title in each slot."""

from collections import defaultdict
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.gallery_caption_bounds import validate
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_gallery_caption_dispositions_20261123 as playback
from scripts.inventory_common_scene_caption_duplicates import captions as clean_captions
from scripts.replay_visible_gallery_captions_v2 import caption as verify_caption
from scripts.seal_shared_text_source_v1 import reference


base, current = playback.base, playback.current
SHA = current.native.digest
BASE = 0x02000000
WORKLIST = Path("translations/editorial_checkpoints/shared_display_20261123/current_shared_display_evidence_20261123.json")
PACKAGE = Path("releases/all_routes_editorial_20261111_visible_gallery_captions_candidate")
EDITORIAL = PACKAGE / "verification/registered_caption_review.json"
OUT = WORKLIST.with_name("gallery_caption_display_dispositions_20261123.json")
SHEET = OUT.with_suffix(".png")
ROOT = playback.ROOT / playback.CASE


def picture(shot):
    assert base.digest(shot["path"]) == shot["PNG_sha256"]
    with Image.open(shot["path"]) as source:
        return source.convert("RGB")


def release_inputs():
    release, integrated = map(base.load, (current.RELEASE, current.REVIEW))
    assert base.digest(current.ROM) == integrated["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.native.CLEAN) == release["clean_input_sha256"]
    terminal_path, report_path, trace_path = (ROOT / name for name in (
        "terminal.json", "capture/capture_report.json", "requests.json"))
    terminal, report, trace = map(base.load, (terminal_path, report_path, trace_path))
    assert terminal["ROM_sha256"] == report["ROM_sha256"] == release["candidate_sha256"]
    assert all(base.digest(p) == digest for p, digest in terminal["evidence"].items())
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    schedule, required, end, _, donor = playback.schedule(playback.CASE)
    assert report["frames"] == terminal["completed_frames"] == end and report["scripted_input_schedule"] == schedule
    assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    contract = base.load(ROOT / "source_contract.json")
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert trace["source_contract_sha256"] == base.digest(ROOT / "source_contract.json")
    assert trace["rows"] == terminal["caption_calls"] and len(trace["source_requests"]) == terminal["COMMON_requests"]
    shots = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}
    assert set(required) <= shots.keys()
    return release, integrated, terminal, trace, shots, terminal_path


def catalogue(clean, current_rom, arm):
    source = clean.read_file(current.ARM)
    assert base.digest(EDITORIAL) == base.load(PACKAGE / "checksums.json")["verification/registered_caption_review.json"]
    earlier = base.load(EDITORIAL)
    rows = {(r["route"], r["position"]): r for r in earlier["records"]}
    originals = {(r["route_index"], r["index"]): r for r in clean_captions(source)}
    outcome = {}
    for row in validate(arm):
        route, position = key = row["route"], row["position"]
        approved, old = rows[key], originals[key]
        registered = approved["registered_reference"]
        assert all(approved["review"].values()) and approved["english"] == row["English"]
        assert old["offset"] == approved["source_reference"]["offset"]
        assert old["source_hex"] == approved["source_reference"]["original_hex"]
        assert old["japanese"] == approved["source_Japanese"]
        assert registered["stored_hex"] == (row["English"].encode("ascii") + b"\0").hex()
        assert row["field"] == registered["field"] == old["pointer_field"] and row["pointer"] == registered["pointer"]
        assert approved["output_bounds"] == row["bounds"]
        field = 0x432DC + route * 8
        clean_image_table, clean_title_table = unpack_from("<2I", source, field)
        image_table, title_table = unpack_from("<2I", arm, field)
        assert image_table == clean_image_table and title_table == clean_title_table
        assert row["field"] == title_table + position * 4 - BASE
        image_id, = unpack_from("<I", arm, image_table + position * 4 - BASE)
        old_image_id, = unpack_from("<I", source, clean_image_table + position * 4 - BASE)
        assert image_id == old_image_id
        image_file = f"/evstill/evstill{image_id:03d}.pxl"
        assert image_file == approved["original_scene_image"]
        asset = clean.read_file(image_file)
        assert asset == current_rom.read_file(image_file)
        outcome[key] = row | dict(id=approved["id"], gallery_table=title_table,
            source_hex=old["source_hex"], source_Japanese=old["japanese"], source_reference=approved["source_reference"],
            current_reference=dict(pointer_field=BASE + row["field"], text_pointer=row["pointer"],
                text_hex=registered["stored_hex"]), source_meaning=approved["source_meaning"],
            context=approved["context"], localization_note=approved["localization_note"], review=approved["review"],
            earlier_editorial_decision=approved["decision"], original_scene_image=image_file, image_sha256=SHA(asset),
            matching_COMMON_keys=approved["matching_COMMON_keys"])
    assert len(outcome) == len(rows) == len(originals) == 164
    return outcome


def gameplay(catalogue, traces, shots, font):
    by_table = {(row["gallery_table"], row["position"]): key for key, row in catalogue.items()}
    by_route = defaultdict(list)
    for call in traces:
        assert call["PC"] == 0x02043008
        key = by_table[call["gallery_table"], call["gallery_position"]]
        row = catalogue[key]
        assert (call["pointer"], call["text"], call["x"]) == (row["pointer"], row["English"], row["bounds"][0])
        by_route[row["route"]].append((key, call))

    views, examples = {}, []
    assert set(by_route) == set(range(4))
    frame = 3200
    for route, count in enumerate(playback.CAPTIONS_PER_ROUTE):
        if route:
            frame += 2 * playback.STEP
        group = by_route[route]
        assert len(group) == count
        entry_position = group[0][0][1]
        assert [key[1] for key, _ in group] == [(entry_position + n) % count for n in range(count)]
        start_frame = frame
        entered = [key for key, call in group if call["frame"] <= start_frame]
        start = entered[-1][1]
        calls = dict(group)
        for step in range(count):
            key = route, (start + step) % count
            call = calls[key]
            interval = 200 if frame == 3200 else playback.STEP
            if route and frame == start_frame:
                # The route may open on touch before the following A press.
                interval *= 2
            wrapped_from_entry = key in entered[:-1]
            if not wrapped_from_entry:
                assert frame - interval < call["frame"] <= frame, (key, call["frame"], frame)
            assigned = shots[frame]
            screen = picture(assigned)
            row = catalogue[key]
            mark = verify_caption(font, row["English"], screen)
            assert [mark["bounds"][0], mark["bounds"][2]] == row["bounds"]
            views[key] = dict(capture=assigned, original_native_draw=call, complete_glyph_mask=mark,
                first_draw_before_collection_and_hold_after_wrap=wrapped_from_entry)
            if frame == start_frame:
                examples.append((row, screen))
            frame += playback.STEP
        wrapped, first = picture(shots[frame]), picture(shots[start_frame])
        assert wrapped.crop((0, 0, 256, 192)).tobytes() == first.crop((0, 0, 256, 192)).tobytes()
        start_row = catalogue[route, start]
        assert verify_caption(font, start_row["English"], wrapped) == views[route, start]["complete_glyph_mask"]
        views[route, start]["wraparound_capture"] = shots[frame]
        frame += playback.STEP * 2
    assert len(views) == len(catalogue)
    return views, examples


def shared_dispositions(release, integrated, clean, current_rom, arm, titles, views):
    source_arm = clean.read_file(current.ARM)
    original = common_message_entries(clean.read_file(current.COMMON), source_arm)
    raw = current_rom.read_file(current.COMMON)
    assert SHA(raw) == release["target_COMMON_sha256"]
    installed = owned_entries(raw, arm, SHA(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    earlier = base.load(WORKLIST)
    assert earlier["clean_sha256"] == release["clean_input_sha256"]
    bound = {r["message_ID"]: r for r in integrated["shared_consumer_binding"]["records"]}
    proved, remaining = [], []
    for row in earlier["records"]:
        key = row["message_ID"]
        jp, en = original[key], installed[key]
        expected = bound.pop(key)
        assert expected["exact_body_retained"]
        assert row["source_reference"] == reference(jp) and row["source_hex"] == jp.text.hex()
        assert row["installed_reference"] == expected["installed"] == reference(en)
        assert row["installed_hex"] == en.text.hex()
        matches = row.get("independent_gallery_draw_sources", [])
        if not matches:
            remaining.append(key)
            continue
        assert jp.text == en.text
        exact = []
        for match in matches:
            previous = match["current"]
            gallery_key = previous["route"], previous["position"]
            title = titles[gallery_key]
            assert key in title["matching_COMMON_keys"]
            assert match["clean"]["text_hex"] == title["source_hex"] == row["source_hex"]
            assert title["English"] == row["earlier_draft"]["english"]
            assert (title["pointer"], title["bounds"][0], title["English"].encode("ascii").hex()) == (
                previous["pointer"], previous["draw_x"], previous["text_hex"])
            exact.append(dict(caption_id=title["id"], route=gallery_key[0], position=gallery_key[1],
                context=title["context"], english=title["English"], source_meaning=title["source_meaning"],
                source_reference=title["source_reference"], installed_reference=title["current_reference"],
                localization_note=title["localization_note"], review=title["review"],
                draw_pointer=views[gallery_key]["original_native_draw"]["pointer"],
                displayed_frame=views[gallery_key]["capture"]["frame"]))
        proved.append(dict(message_ID=key, file_path=current.COMMON, source_Japanese=jp.text.decode("cp932"),
            source_reference=reference(jp), installed_reference=reference(en), exact_COMMON_hex=jp.text.hex(),
            visible_content_disposition="Exact text match to separately stored, reviewed and observed Gallery title.",
            gallery_records=exact, direct_COMMON_display_outside_gallery="Unverified. Reopen if a distinct caller is found."))
    assert not bound and len(proved) == 123 and len(remaining) == 153
    return proved, remaining


def main():
    release, integrated, terminal, trace, shots, terminal_path = release_inputs()
    clean, rom = map(base.NdsImage.open, (current.native.CLEAN, current.ROM))
    arm = rom.read_file(current.ARM)
    assert SHA(arm) == release["target_ARM9_sha256"]
    titles = catalogue(clean, rom, arm)
    views, examples = gameplay(titles, trace["rows"], shots, GameAsciiFont.from_arm9(arm))
    in_gallery = [row for row in trace["source_requests"] if row["frame"] >= 3001]
    assert not in_gallery
    proved, remaining = shared_dispositions(release, integrated, clean, rom, arm, titles, views)
    sheet = Image.new("RGB", (1040, 828), "#263238")
    put = ImageDraw.Draw(sheet)
    for n, (row, screen) in enumerate(examples):
        x, y = n % 2 * 520, n // 2 * 414
        put.text((x + 5, y + 4), row["id"] + " / " + row["English"], fill="white")
        sheet.paste(screen, (x + 6, y + 24))
        strip = screen.crop((14, 251, 242, 284)).resize((456, 66), Image.Resampling.NEAREST)
        sheet.paste(strip, (x + 36, y + 340))
    sheet.save(SHEET)
    evidence = terminal["evidence"] | {str(p): base.digest(p) for p in
        (terminal_path, WORKLIST, current.RELEASE, current.REVIEW, EDITORIAL, SHEET,
         Path(playback.__file__), Path(__file__))}
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        actual_gallery_navigation=True, prepared_unlock_save=True, earned_unlock=False, hardware=False,
        observed_caption_positions=164, direct_COMMON_requests_in_gallery=[], all_stored_reference_keys_preserved=276,
        shared_visible_content_dispositions=proved, needing_distinct_editorial_disposition=remaining,
        native_draws=[titles[k] | views[k] for k in sorted(titles)], new_dialogue_credit=0,
        representative_sheet=str(SHEET), evidence=evidence))
    print("Verified all 164 displayed Gallery captions and adjudicated 123 exact stored duplicates.")


if __name__ == "__main__":
    main()
