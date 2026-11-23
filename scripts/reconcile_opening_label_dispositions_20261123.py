"""Bind stored opening labels to independently observed movie artwork."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import observe_opening_label_dispositions_20261123 as live
from scripts import reconcile_shared_movie_labels_20261123 as movie
from scripts.reconcile_gallery_caption_dispositions_20261123 import WORKLIST, picture
from scripts.reconcile_story_still_label_dispositions_20261123 import OUT as STILL_CHECKPOINT
from scripts.seal_shared_text_source_v1 import reference


base, current, native = live.base, live.current, live.current.native
OUT = WORKLIST.with_name("opening_label_dispositions_20261123.json")
SHEET = OUT.with_suffix(".png")
HISTORICAL = movie.BOOK / "opening_scene_display_scope_20261119_v1.json"
COMPOSITION_PROOF = live.COMPOSITION.with_name("opening_composition_proof.json")
TITLE_PATH = "/FLS/M28.fls"
VARIANTS_OPEN = {3577, 3578, *range(3594, 3601)}


def frames(report):
    return {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}


def checked_run(case, release, pending):
    folder = live.ROOT / case
    report_path, trace_path, terminal_path = (folder / name for name in (
        "capture/capture_report.json", "requests.json", "terminal.json"))
    report, trace, terminal = map(base.load, (report_path, trace_path, terminal_path))
    scheduler, holds, end, _, donor = live.schedule(case)
    assert release["candidate_sha256"] == report["ROM_sha256"] == terminal["ROM_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["frames"] == end == terminal["completed_frames"]
    assert report["scripted_input_schedule"] == scheduler and report["exact_requested_capture_frames"] == holds
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert bool(report.get("battery_save_preloaded")) == bool(donor)
    if donor:
        preload = report["battery_save_preloaded"]
        assert preload["copied_byte_exact_before_cold_boot"] and preload["source_sha256"] == donor["source_sha256"]
    assert all(base.digest(path) == digest for path, digest in terminal["evidence"].items())
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["mismatches"] and not trace["errors"]
    contract = folder / "source_contract.json"
    assert base.digest(contract) == trace["source_contract_sha256"]
    assert base.load(contract)["ARM9_sha256"] == release["target_ARM9_sha256"]
    requests = trace["source_requests"]
    assert requests == terminal["target_COMMON_calls"] and len(requests) == terminal["COMMON_requests"]
    assert not pending.intersection(row["message_ID"] for row in requests)
    if case == "title":
        assert not requests
    else:
        assert len(requests) == 2 and {row["message_ID"] for row in requests} == {120}
        assert {row["PC"] for row in requests} == set(live.trace.REQUESTS)
        assert requests[0]["frame"] == requests[1]["frame"]
    assert set(holds) <= frames(report).keys()
    receipt = dict(source="cold boot with controller input" if scheduler else "unattended title playback",
        completed_frames=end, held_frames=holds, COMMON_requests=requests, pending_label_requests=0,
        battery_save_source=donor["source_sha256"] if donor else None,
        evidence=terminal["evidence"] | {str(terminal_path): base.digest(terminal_path)})
    return receipt, report


def title_pixels(report):
    proof = base.load(COMPOSITION_PROOF)
    assert proof["results_sha256"] == base.digest(live.COMPOSITION)
    baseline = proof["reports"]["baseline"]
    assert base.digest(baseline["path"]) == baseline["sha256"]
    earlier = base.load(baseline["path"])
    for key in ("core_DLL_sha256", "core_options", "scripted_input_schedule"):
        assert earlier[key] == report[key], key
    shots, old = frames(report), frames(earlier)
    for frame, shot in shots.items():
        assert picture(shot).tobytes() == picture(old[frame]).tobytes(), frame
    anchors = live.title_anchors()
    bound = {i: dict(frame=v["frame"], alpha=v["weight"][0], drawn_pixels=v["weight"][1]) for i, v in anchors.items()}
    return bound, dict(exact_RGB_frame_count=len(shots), pixels_per_frame=256 * 384,
        earlier_report=baseline, matched_frames={n: r["PNG_sha256"] for n, r in shots.items()})


def exact_storage(key, sources, installed, stored, reviewer):
    jp, en, evidence = sources[key], installed[key], stored[key]
    assert jp.text == en.text and jp.text.hex() == evidence["source_hex"] == evidence["installed_hex"]
    assert reference(jp) == evidence["source_reference"]
    assert reference(en) == evidence["installed_reference"] == reviewer[key]["installed"]
    assert reviewer[key]["exact_body_retained"]
    return dict(message_ID=key, file_path=current.COMMON, clean_reference=reference(jp),
        installed_reference=reference(en), Japanese=jp.text.decode("cp932"), exact_stored_hex=jp.text.hex(),
        other_direct_COMMON_consumers_unverified=True)


def verify_movie_data(clean, rom, prior, title_anchors, title_shots, rafael_shots):
    artwork_rows = {}
    for row in prior["records"]:
        key = row["message_ID"]
        if key not in movie.ASSOCIATIONS:
            continue
        art = row["separate_artwork_path"]
        path, index = movie.ASSOCIATIONS[key]
        assert (path, index) == (art["file_path"], art["texture_index"])
        for image, name in ((clean, "clean_sha256"), (rom, "current_sha256")):
            data = image.read_file(path)
            assert native.digest(data) == art[name]
            tex = FlsArchive(data).texture(index)
            assert native.digest(tex.render().tobytes()) == art["exact_visible_texture_sha256"]
        for prop in ("earlier_ordinary_New_Game_hold", "earlier_ordinary_title_hold", "complete_approved_names"):
            if prop in art:
                picture(art[prop])
        artwork_rows[key] = art
    assert set(artwork_rows) == set(movie.ASSOCIATIONS)
    earlier_harbor = artwork_rows[3394]["earlier_ordinary_New_Game_hold"]
    harbor = rafael_shots[earlier_harbor["frame"]]
    assert picture(earlier_harbor).crop((0, 0, 256, 192)).tobytes() == picture(harbor).crop((0, 0, 256, 192)).tobytes()
    artwork_rows[3394]["current_upper_screen_verified"] = harbor
    artwork_rows[3456]["current_title_hold"] = title_shots[title_anchors[48]["frame"]]
    return artwork_rows


def verify_saved_commands(prior, clean, rom):
    for label, image in (("clean", clean), ("current", rom)):
        rows = prior["checked_movie_commands"][label]
        assert sorted(r["arguments"][0] for r in rows) == [20, 21, 23, 23]
        for row in rows:
            path, number, offset = (row[name] for name in ("file_path", "block", "offset"))
            block = native.IlnkContainer.parse(image.read_file(path)).blocks[number]
            assert native.digest(block) == row["block_sha256"]
            assert block[offset:offset + 2].hex() == row["command_hex"]
    return prior["checked_movie_commands"]


def tulip_movie(clean, rom):
    """Verify the exact nested scene operand with the original native decoder."""
    path, story, number = "/FLS/M27.fls", "/data/SC2.DK4", 70
    walk = movie.scene.explicit_walk()
    commands = {}
    clean_art, current_art = (image.read_file(path) for image in (clean, rom))
    assert clean_art == current_art
    for label, image, ancestor, offset in (("clean", clean, 5460, 5634), ("installed", rom, 5728, 5880)):
        arm = image.read_file(current.ARM)
        block = native.IlnkContainer.parse(image.read_file(story)).blocks[number]
        outer = walk(arm, block)
        assert outer["error"] is None
        entry, = (r for r in outer["rows"] if r["offset"] == ancestor)
        length = unpack_from("<H", block, ancestor + 2)[0]
        assert entry["word"] == 0x0100 and entry["native_extent"] == length + 4
        start = ancestor + 4
        inner = walk(arm, block[:4] + pack("<2H", length, 0) + block[start:start + length])
        assert inner["error"] is None
        relocated = offset - start + 8
        opcode, = (r for r in inner["rows"] if r["offset"] == relocated)
        call, = (r for r in inner["native_movie_requests"] if r["source_offset"] == relocated)
        assert (opcode["word"], opcode["native_extent"]) == (0x4907, 2)
        assert call["args"] == [27, 0, 1, 0]
        assert not any(r["source_offset"] == relocated and r["PC"] in live.trace.REQUESTS
                       for r in inner["opaque_effect_bridges"])
        commands[label] = dict(file_path=story, block=number, block_sha256=native.digest(block),
            branch_offset=ancestor, offset=offset, command_hex=block[offset:offset + 2].hex(), arguments=call["args"])
    texture = FlsArchive(current_art).texture(0).render()
    return dict(file_path=path, texture_index=0, exact_clean_and_installed_archive_sha256=native.digest(clean_art),
        texture_sha256=native.digest(texture.tobytes()), offline_native_commands=commands,
        observed_in_current_gameplay=False), texture


def contact_sheet(title_shots, anchors, artwork, tulip_texture):
    samples = [(name, title_shots[anchors[i]["frame"]]) for i, name in (
        (3, "Opening sea"), (22, "Rafael Castor"), (46, "Hodram Joakim Bergstrom"),
        (48, "Lil and Camille"), (72, "Lil Argot and Camille Overijssel"), (76, "Sera"),
        (82, "Maria and the rose"), (148, "The adversaries"), (149, "Irene in the study"),
        (157, "Setting sail"), (158, "Evening"), (160, "Night"), (169, "The finale"))]
    samples += [("Rafael harbor", artwork[3394]["current_upper_screen_verified"]),
                ("Earlier Rafael hold", artwork[3397]["earlier_ordinary_New_Game_hold"])]
    sheet = Image.new("RGB", (1024, 4 * 214), "#1f2830")
    draw = ImageDraw.Draw(sheet)
    for index, (name, shot) in enumerate(samples):
        x, y = (index % 4) * 256, (index // 4) * 214
        draw.text((x + 6, y + 4), name, fill="white")
        sheet.paste(picture(shot).crop((0, 0, 256, 192)), (x, y + 20))
    draw.text((3 * 256 + 6, 3 * 214 + 4), "Tulips (decoded source texture)", fill="white")
    sheet.paste(tulip_texture.crop((0, 0, 256, 192)), (3 * 256, 3 * 214 + 20))
    sheet.save(SHEET)


def main():
    release, integrated = map(base.load, (current.RELEASE, current.REVIEW))
    assert base.digest(current.ROM) == release["candidate_sha256"] == integrated["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, rom = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    clean_common, current_common = (image.read_file(current.COMMON) for image in (clean, rom))
    clean_arm, current_arm = (image.read_file(current.ARM) for image in (clean, rom))
    assert native.digest(current_arm) == release["target_ARM9_sha256"]
    jp = common_message_entries(clean_common, clean_arm)
    en = owned_entries(current_common, current_arm, native.digest(current_arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    installed = {r["message_ID"]: r for r in integrated["shared_consumer_binding"]["records"]}
    stored = {r["message_ID"]: r for r in base.load(WORKLIST)["records"]}
    pending = set(base.load(STILL_CHECKPOINT)["remaining_needing_distinct_disposition"])
    assert len(pending) == 100 and len(stored) == len(installed) == 276
    scopes, reports = {}, {}
    for case in live.CASES:
        scopes[case], reports[case] = checked_run(case, release, pending)
    anchors, pixel_proof = title_pixels(reports["title"])
    title_shots = frames(reports["title"])
    earlier = base.load(HISTORICAL)
    clean_title, current_title = (image.read_file(TITLE_PATH) for image in (clean, rom))
    title_hashes = dict(clean=native.digest(clean_title), installed=native.digest(current_title))
    assert title_hashes["installed"] == earlier["original_visible_asset_sha256"][TITLE_PATH]
    rows = []
    for old in earlier["records"]:
        key = old["message_ID"]
        if key in VARIANTS_OPEN:
            continue
        row = exact_storage(key, jp, en, stored, installed)
        assert (old["Japanese"], old["source_hex"], old["reviewed_English"]) == (
            row["Japanese"], row["exact_stored_hex"], stored[key]["earlier_draft"]["english"])
        asset = old["artwork_association"]
        assert asset["path"] == TITLE_PATH and not asset["exact_label_to_texture_pointer_proven"]
        textures = asset["related_texture_indices"]
        proven = {i: anchors[i] for i in textures if i in anchors}
        assert proven
        rows.append(row | dict(reviewed_English_draft=old["reviewed_English"], retention_reason=old["reason"],
            manuscript_review=old["review"], disposition="Identified artwork sequence in the observed title movie.",
            visual_basis=asset["visual_basis"], related_texture_indices=textures, observed_texture_anchors=proven,
            exact_variant_pointer_proven=False))
    assert len(rows) == 28
    prior = base.load(movie.OUT)
    artwork = verify_movie_data(clean, rom, prior, anchors, title_shots, frames(reports["rafael"]))
    commands = verify_saved_commands(prior, clean, rom)
    for key, art in artwork.items():
        row = exact_storage(key, jp, en, stored, installed)
        earlier_draft = stored[key]["earlier_draft"]
        rows.append(row | dict(reviewed_English_draft=earlier_draft["english"],
            manuscript_review=earlier_draft["review"], artwork=art,
            disposition="Independent movie artwork matches the scene described by the stored label."))
    tulips, texture = tulip_movie(clean, rom)
    earlier_draft = stored[3480]["earlier_draft"]
    rows.append(exact_storage(3480, jp, en, stored, installed) | dict(reviewed_English_draft=earlier_draft["english"],
        manuscript_review=earlier_draft["review"], artwork=tulips,
        disposition="The original and installed story branches load the full-frame tulip field as movie 27."))
    resolved = {r["message_ID"] for r in rows}
    assert len(resolved) == 33 and resolved <= pending
    contact_sheet(title_shots, anchors, artwork, texture)
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        checked_runs=scopes, exact_title_comparison=pixel_proof, title_asset_sha256=title_hashes,
        prior_native_story_commands=commands, label_dispositions=sorted(rows, key=lambda row: row["message_ID"]),
        source_storage_inventory=len(stored), completed_prior_display_dispositions=len(stored) - len(pending),
        remaining_needing_distinct_disposition=sorted(pending - resolved), ambiguous_title_labels=sorted(VARIANTS_OPEN),
        new_prose_revisions=0, new_dialogue_credit=0, hardware=False, global_absence_claim=False,
        representative_sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence={str(path): base.digest(path) for path in (HISTORICAL, COMPOSITION_PROOF, live.COMPOSITION,
            STILL_CHECKPOINT, movie.OUT, WORKLIST)}))
    print(f"Verified {len(resolved)} scoped label dispositions; {len(pending - resolved)} remain.")


if __name__ == "__main__":
    main()
