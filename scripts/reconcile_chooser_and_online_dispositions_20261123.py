"""Bind existing editorial reviews to the observed chooser and Extras screens."""

from collections import defaultdict
from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_chooser_and_online_dispositions_20261123 as live
from scripts import register_about_extras_20261114 as extras
from scripts import register_captain_biographies_v1 as bios
from scripts import register_visible_online_captions_v1 as guide
from scripts.checkpoint_online_gallery_current_20261114 import GUIDE_COPY_GROUPS
from scripts.reconcile_gallery_caption_dispositions_20261123 import OUT as GALLERY, WORKLIST, picture
from scripts.review_visible_online_captions_v1 import BASE, COLOR, DESCRIPTORS, complete_mask
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_extras_tie_in_20261114 import check_page
from scripts.verify_captain_biographies_v1 import mask, native_selector


base, current = live.base, live.current
sha = current.native.digest
PROMOTIONAL = Path("translations/common_online_promotional_manuscript_v3.json")
OUT = GALLERY.with_name("chooser_and_online_dispositions_20261123.json")
SHEET = OUT.with_suffix(".png")
SAME_ONLINE_HEADINGS = (3289, 3291, 3293, 3305)


def validated_review(path):
    checksum_path = path.parent.parent / "checksums.json"
    key = path.relative_to(checksum_path.parent).as_posix()
    assert base.digest(path) == base.load(checksum_path)[key]
    return base.load(path)["records"]


def capture(case, release):
    folder = live.ROOT / case
    path, report_path, requests = (folder / p for p in ("terminal.json", "capture/capture_report.json", "requests.json"))
    receipt, report, trace = map(base.load, (path, report_path, requests))
    schedule, held, end, _, donor = live.schedule(case)
    assert release["candidate_sha256"] == receipt["ROM_sha256"] == report["ROM_sha256"]
    assert report["frames"] == receipt["completed_frames"] == end and report["scripted_input_schedule"] == schedule
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert bool(report.get("battery_save_preloaded")) == bool(donor)
    if donor:
        copied = report["battery_save_preloaded"]
        assert copied["source_sha256"] == donor["source_sha256"] and copied["copied_byte_exact_before_cold_boot"]
    assert all(base.digest(p) == digest for p, digest in receipt["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["mismatches"] and not trace["errors"]
    assert trace["source_contract_sha256"] == base.digest(folder / "source_contract.json")
    assert base.load(folder / "source_contract.json")["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert trace["rows"] == receipt["caption_calls"]
    assert receipt["COMMON_requests"] == len(trace["source_requests"]) and not receipt["target_COMMON_calls"]
    frames = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    assert set(held) <= frames.keys()
    return receipt, frames, receipt["evidence"] | {str(path): base.digest(path)}


def proof_row(row, source_reference, installed_reference, **extra):
    assert all(row["review"].values())
    return {key: row[key] for key in ("id", "context", "source_meaning", "english", "localization_note", "review")} | dict(
        decision="retain_registered_english", source_reference=source_reference, installed_reference=installed_reference,
        **extra)


def bios_proof(clean, arm, font, release, frames, pictures):
    startup_path = Path(release["own_registered_startup"])
    assert base.digest(startup_path) == release["own_registered_startup_sha256"]
    startup = base.load(startup_path)
    assert startup["candidate_sha256"] == release["candidate_sha256"] and startup["cold_boot"] and not startup["savestate"]
    snapshot = startup["read_only_snapshot"]
    assert snapshot["read_only_export"] and base.digest(snapshot["path"]) == snapshot["sha256"]
    raw = Path(snapshot["path"]).read_bytes()
    assert len(raw) == snapshot["bytes"] == 0x400000
    indexed = {r["chooser_index"]: r for r in validated_review(bios.REVIEW)}
    proof, samples = {}, defaultdict(list)
    for frame, index in live.STATES:
        row = indexed[index]
        shot = picture(frames[frame])
        checked = mask(font, row["staged_rows"], shot)
        if not samples[index]:
            pictures.append((row["actor"], shot.crop((0, 324, 256, 368))))
        samples[index].append(dict(screenshot=frames[frame], glyph_mask=checked))
    assert len(indexed) == len(samples) == 4
    before, after = (frames[f] for f in (2200, 5500))
    selected_new_game, returned = map(picture, (before, after))
    delta = ImageChops.difference(selected_new_game, returned).getbbox()
    assert delta == (98, 228, 158, 268)
    for point, color in (((100, 239), (0, 165, 172)), ((100, 259), (205, 198, 180))):
        assert returned.getpixel(point) == color and selected_new_game.getpixel(point) != color
    for index, row in indexed.items():
        ref = row["registered_reference"]
        at, field = ref["ARM9_offset"], ref["pointer_field"] - BASE
        assert unpack_from("<I", arm, field)[0] == ref["runtime_address"] == BASE + at
        payload = bytes.fromhex(ref["exact_hex"])
        assert len(payload) == ref["byte_count"] and arm[at:at + len(payload)] == payload
        assert payload.endswith(b"\0") and payload[:-1].decode("ascii").split() == row["english"].split()
        clean_lines = row["source_line_references"]
        for line in clean_lines:
            jp = bytes.fromhex(line["clean_hex"])
            lo = line["ARM9_offset"]
            assert clean[lo:lo + len(jp)] == jp and jp.decode("cp932") == line["Japanese"]
        selection = native_selector(arm, raw, row)
        assert selection["selected_address"] == ref["runtime_address"]
        assert len({v["glyph_mask"]["ink_mask_sha256"] for v in samples[index]}) == 1
        proof[104 + index] = proof_row(row, clean_lines, ref, chooser_index=index, speaker=row["actor"],
            displayed_rows=row["staged_rows"], source_Japanese="".join(line["Japanese"] for line in clean_lines),
            live_holds=samples[index], offline_selected_owner=selection, earlier_review=str(bios.REVIEW))
    return proof, dict(menu_before=before, back_return=after, changed_highlight_bounds=delta,
        return_highlights_continue=True, offline_RAM_source=snapshot), startup_path


def guide_proof(clean, arm, font, rom, earlier_pages, receipt, frames, pictures):
    trace = {r["pointer"]: r for r in receipt["caption_calls"]}
    assert len(trace) == len(receipt["caption_calls"]) == 13
    holds = {r["id"]: r for r in earlier_pages}
    pages = {}
    for row, group in zip(validated_review(guide.REVIEW), GUIDE_COPY_GROUPS, strict=True):
        r = row["registered_reference"]
        source, installed = row["source_reference"], bytes.fromhex(r["stored_hex"])
        field = DESCRIPTORS[row["original_category"]]
        assert arm[field:field + 12] == clean[field:field + 12]
        _, table, count = unpack_from("<3I", arm, field)
        index = row["original_page"]
        assert 0 <= index < count
        ptr = table - BASE + 4 * index
        assert unpack_from("<I", arm, ptr) == unpack_from("<I", clean, ptr) == (r["pointer"],)
        start = r["offset"]
        assert clean[start:start + len(bytes.fromhex(source["original_hex"]))].hex() == source["original_hex"]
        assert arm[start:start + len(installed)] == installed
        old = holds[row["id"]]
        assert old["COMMON_IDs"] == list(group) and old["clean_Japanese"] == row["source_Japanese"]
        asset = row["background"]
        assert asset == old["source_artwork"] and sha(rom.read_file(asset)) == old["same_artwork_sha256"]
        shot = frames[old["frame"]]
        event = trace[r["pointer"]]
        x = 128 - 3 * len(row["english"])
        assert event["frame"] < shot["frame"] and event["PC"] == live.replay.ONLINE
        assert event["text"] == row["english"] and event["x"] == x
        screen = picture(shot)
        count, bounds = complete_mask(font, row["english"], screen, x, 205, COLOR)
        assert count == old["glyph_pixels"] and list(bounds) == old["bounds"]
        pages[row["id"]] = proof_row(row, source, r | dict(pointer_field=BASE + ptr), source_Japanese=row["source_Japanese"],
            related_COMMON_records=list(group), earlier_review=str(guide.REVIEW), observed_native_draw=event,
            complete_glyph_count=count, glyph_bounds=list(bounds), screenshot=shot, artwork_path=asset)
        if any(n in SAME_ONLINE_HEADINGS for n in group):
            pictures.append((row["english"], screen.crop((0, 195, 256, 227))))
    assert len(pages) == 13
    return pages


def extras_proof(clean, arm, font, previous, frames, pictures):
    holds = {r["id"]: r for r in previous}
    pages = {}
    for row in validated_review(extras.REVIEW):
        ref, original = row["registered_reference"], row["current_reference"]
        at, field, start = ref["ARM9_offset"], ref["pointer_field"], original["ARM9_offset"]
        assert unpack_from("<I", arm, field) == (BASE + at,)
        assert unpack_from("<I", clean, field) == (BASE + start,)
        expected, source = bytes.fromhex(ref["exact_stored_hex"]), bytes.fromhex(row["source_hex"])
        assert arm[at:at + len(expected)] == expected and clean[start:start + len(source)] == source
        earlier = holds[row["id"]]
        shot = frames[earlier["frame"]]
        image = picture(shot)
        counts = check_page(image, font, row["lines"])
        assert counts == earlier["complete_row_pixels"] == row["candidate_glyph_counts"]
        pages[row["id"]] = proof_row(row, dict(ARM9_offset=start, clean_hex=row["source_hex"]), ref,
            screenshot=shot, source_Japanese=row["source_Japanese"], english_lines=row["lines"],
            earlier_review=str(extras.REVIEW), complete_row_pixels=counts)
        if earlier["page"] in (2, 3):
            pictures.append((f"About Extras / page {earlier['page']}", image.crop((0, 225, 256, 325))))
    assert len(pages) == 6
    return pages


def main():
    release, registered, worklist, gallery, older = map(base.load,
        (current.RELEASE, current.REVIEW, WORKLIST, GALLERY, PROMOTIONAL))
    candidate = release["candidate_sha256"]
    assert base.digest(current.ROM) == registered["candidate_sha256"] == candidate == gallery["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.native.CLEAN) == release["clean_input_sha256"] == worklist["clean_sha256"] == older["clean_sha256"]
    clean, rom = map(base.NdsImage.open, (current.native.CLEAN, current.ROM))
    source_arm, arm = (im.read_file(current.ARM) for im in (clean, rom))
    source = common_message_entries(clean.read_file(current.COMMON), source_arm)
    common = rom.read_file(current.COMMON)
    assert sha(arm) == release["target_ARM9_sha256"] and sha(common) == release["target_COMMON_sha256"]
    installed = owned_entries(common, arm, sha(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    font, pictures = GameAsciiFont.from_arm9(arm), []
    runs = {case: capture(case, release) for case in ("chooser", "online", "tie_in_advance")}
    bios_rows, nav, startup = bios_proof(source_arm, arm, font, release, runs["chooser"][1], pictures)
    online, online_frames, _ = runs["online"]
    pages = guide_proof(source_arm, arm, font, rom, older["actual_independent_guide_pages"], online, online_frames, pictures)
    assert not runs["chooser"][0]["caption_calls"] and not runs["tie_in_advance"][0]["caption_calls"]
    tie = extras_proof(source_arm, arm, font, older["actual_independent_about_extras_pages"], runs["tie_in_advance"][1], pictures)
    pending = {r["message_ID"]: r for r in worklist["records"]}
    bound = {r["message_ID"]: r for r in registered["shared_consumer_binding"]["records"]}
    decisions, related, review_drafts = [], [], {r["message_ID"]: r for r in older["records"]}
    matched_pages = {n: p for p in pages.values() for n in p["related_COMMON_records"]}
    for key in (*bios_rows, *review_drafts):
        work = pending[key]
        jp, en = source[key], installed[key]
        assert reference(jp) == work["source_reference"] and jp.text.hex() == work["source_hex"]
        assert reference(en) == work["installed_reference"] == bound[key]["installed"]
        assert en.text.hex() == work["installed_hex"] and bound[key]["exact_body_retained"]
        jp_text = jp.text.decode("cp932")
        proof = dict(message_ID=key, file_path=current.COMMON, clean_Japanese=jp_text, source_reference=reference(jp),
            source_hex=jp.text.hex(), installed_reference=reference(en), installed_hex=en.text.hex())
        if key in bios_rows:
            biography = bios_rows[key]
            assert jp_text.replace("\n", "").replace("。", "") == biography["source_Japanese"]
            assert work["separate_chooser_biography_review"] == biography["id"]
            decisions.append(proof | dict(displayed_owner=biography["id"],
                visible_content_disposition="Chooser biography matches the full Japanese wording once line breaks and sentence periods are removed."))
            continue
        draft = review_drafts[key]
        assert draft["clean_Japanese"] == jp_text and draft["clean_hex"] == jp.text.hex() == en.text.hex()
        owners = [pages.get(ident) or tie[ident] for ident in draft["independently_displayed_related_ARM9_owners"]]
        if key <= 3316:
            assert owners == [matched_pages[key]]
        if key in SAME_ONLINE_HEADINGS:
            visible, = owners
            assert "".join(visible["source_Japanese"].split()) == "".join(jp_text.split())
            decisions.append(proof | dict(displayed_owner=visible["id"],
                visible_content_disposition="The independent Online heading matches the stored Japanese after removing spacing."))
        else:
            assert all("".join(visible["source_Japanese"].split()) != "".join(jp_text.split()) for visible in owners)
            related.append(proof | dict(related_displayed_owners=[visible["id"] for visible in owners],
                source_draft=dict(path=str(PROMOTIONAL), english=draft["english"], review=draft["review"]),
                display_disposition="Open for the distinct COMMON wording or fuller text."))
    prior = {r["message_ID"] for r in gallery["shared_visible_content_dispositions"]}
    now = {r["message_ID"] for r in decisions}
    assert len(related) == 27 and len(now) == 8 and not prior & now
    remaining = sorted(set(pending) - prior - now)
    assert len(pending) == 276 and len(remaining) == 145
    sheet = Image.new("RGB", (1032, 412), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (label, art) in enumerate(pictures):
        x, y = i % 4 * 258, i // 4 * 137
        draw.text((x + 3, y + 5), label, fill="white")
        sheet.paste(art, (x + 1, y + 26))
    sheet.save(SHEET)
    evidence = {str(p): base.digest(p) for p in
        (WORKLIST, GALLERY, PROMOTIONAL, bios.REVIEW, guide.REVIEW, extras.REVIEW, current.RELEASE, current.REVIEW,
         SHEET, startup, Path(live.__file__), Path(__file__))}
    for _, _, refs in runs.values():
        evidence.update(refs)
    base.save(OUT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        source_storage_inventory=276, prior_gallery_dispositions=len(prior), confirmed_visible_aliases=decisions,
        remaining_needing_distinct_disposition=remaining, evidenced_related_but_distinct=related,
        chooser_biographies=list(bios_rows.values()), chooser_menu_navigation=nav, online_pages=list(pages.values()),
        about_extras_pages=list(tie.values()), COMMON_lookups_by_run={case: items[0]["COMMON_requests"] for case, items in runs.items()},
        choice_runs_use_original_inputs=True, prepared_chooser_unlock=True, earned_unlock=False, hardware=False,
        exact_stored_references_preserved_for_all=276, new_dialogue_credit=0, visual_sheet=str(SHEET), evidence=evidence))
    print("Verified four chooser biographies, 19 Extras screens, and eight additional display dispositions.")


if __name__ == "__main__":
    main()
