"""Document the observed title and original story paths for the last artwork leads."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageDraw

from scripts import checkpoint_story_still_commands_20261120 as story
from scripts import reconcile_opening_label_dispositions_20261123 as opening
from scripts.reconcile_legacy_setup_and_recruitment_20261123 import registered_review
from scripts.reconcile_legacy_fleet_and_quit_paths_20261123 import (
    WORKLIST, base, common_message_entries, current, native, owned_entries, picture, stored_record,
    DIRECTORY_OFFSET, TABLE_OFFSET,
)
from scripts.reconcile_market_exit_current_20261123 import OUT as PREVIOUS
from scripts.reconcile_title_variant_display_20261123 import OUT as CURRENT_TITLE


OUT = PREVIOUS.with_name("final_shared_artwork_leads_20261123.json")
SHEET = OUT.with_suffix(".png")
TITLE_FRAMES = {2179: (47, "Harbor approach"), 2543: (48, "Lil and Camille running"),
                2819: (73, "Village attack"), 3135: (74, "Sera close-up")}
DRAFTS = {
    3401: ("Hans and Arcadius", "Keep the name used in the archived label. It does not name Eirene after the reveal."),
    3490: ("Maria and Clifford", "The Japanese identifies the two people. It gives neither a rank nor a relationship."),
    3577: ("A Slave Ship Calls at Port", "Calls at port preserves the ship's action without identifying the port or the people aboard."),
    3578: ("A Peaceful Landscape", "Peaceful preserves the quiet mood without specifying where the scene takes place."),
}
STORY = {
    3401: ("palace_eirene_pereira_london", "/data/SC0.DK4", 145, (8, 9, 126, 126),
           ("DK4_MES_B145_R0122", "DK4_MES_B145_R0157"), "DK4_MES_B145_R0157"),
    3490: ("maria_B21_B32", "/data/SC3.DK4", 30, (),
           ("DK4_MES_B30_R0005", "DK4_MES_B30_R0009", "DK4_MES_B30_R0020"), "DK4_MES_B30_R0020"),
}


def title_segment(clean, active, older, latest):
    old_rom = base.NdsImage.open(current.parent.ROM)
    before, after = map(native.files, (old_rom, active))
    assert before.keys() == after.keys()
    assert {key for key in before if before[key] != after[key]} == {"/_pxl/online/Online61.pxl", "/_pxl/online/Online62.pxl"}
    path = opening.TITLE_PATH
    assert older["title_asset_sha256"] == {"clean": native.digest(clean.read_file(path)), "installed": native.digest(after[path])}
    assert not latest["fresh_unattended_title_replay"]["COMMON_requests"]
    title = older["checked_runs"]["title"]
    assert title["completed_frames"] == 7400 and not title["COMMON_requests"]
    assert all(base.digest(f) == value for f, value in title["evidence"].items())
    report_path = opening.live.ROOT / "title/capture/capture_report.json"
    shots = opening.frames(base.load(report_path))
    results_path = opening.live.COMPOSITION
    assert base.digest(results_path) == base.load(opening.COMPOSITION_PROOF)["results_sha256"]
    rows = {r["display_frame"]: r for r in base.load(results_path)["cases"]
            if r["source_movie"] == path and 2179 <= r["display_frame"] <= 3135}
    assert len(rows) == 36 and all(r["whole49152_RGB_pixels_exact_without_exclusions"] for r in rows.values())

    def visible(row):
        return {x["texture"] for x in row["native_draws"] if x["alpha"] and x["drawn_pixels"]}

    assert set.union(*(visible(row) for row in rows.values())) == set(range(47, 75))
    samples = []
    for frame, (index, label) in TITLE_FRAMES.items():
        shot = shots[frame]
        assert index in visible(rows[frame]) and shot["PNG_sha256"] == older["exact_title_comparison"]["matched_frames"][str(frame)]
        picture(shot)
        samples.append(dict(subject=label, texture_index=index, capture=shot))
    return dict(observed_earlier_on_matching_title_dependencies=True, composed_frames_reviewed=36,
        visible_texture_indices=list(range(47, 75)), original_title_COMMON_requests=0,
        observed_current_title_COMMON_requests=0, current_title_asset_sha256=native.digest(after[path]),
        visual_samples=samples, per_label_artwork_alignment_unverified=True)


def visual_commands(walk, arm, block):
    _, stills, unresolved = story.commands(walk, arm, block)
    assert not unresolved

    def nested_trace(start, end):
        native_rows = walk(arm, block[:4] + pack("<2H", end - start, 0) + block[start:end])
        assert native_rows["error"] is None
        assert not native_rows["native_movie_requests"]
        images = [(start + bridge["source_offset"] - 8, bridge["args"][1])
                  for bridge in native_rows["opaque_effect_bridges"] if bridge["PC"] == 0x02028AA8]
        for row in native_rows["rows"]:
            if row["word"] == 0x0100:
                opening = start + row["offset"] - 8
                length, = unpack_from("<H", block, opening + 2)
                assert row["native_extent"] == length + 4
                images.extend(nested_trace(opening + 4, opening + 4 + length))
        return images

    length, = unpack_from("<H", block, 4)
    assert sorted(nested_trace(8, 8 + length)) == sorted((r["byte_offset"], r["image_index"]) for r in stills.values())
    return list(stills.values())


def story_exchange(spec, clean, active):
    name, path, block_number, assets, refs, sample_id = spec
    review, review_path = registered_review(Path("releases") / f"all_routes_editorial_20261122_{name}_candidate")
    scope, evidence = {}, {str(review_path): base.digest(review_path)}
    walk = story.explicit_walk()
    blocks = []
    for label, image in (("clean", clean), ("installed", active)):
        arm = image.read_file(current.ARM)
        archive = image.read_file(path)
        block = native.IlnkContainer.parse(archive).blocks[block_number]
        commands = visual_commands(walk, arm, block)
        assert tuple(x["image_index"] for x in commands) == assets
        scope[label] = dict(archive_sha256=native.digest(archive), block_sha256=native.digest(block), stills=commands, movies=[])
        blocks.append(block)
    for index in set(assets):
        art = f"/evstill/evstill{index:03}.pxl"
        assert clean.read_file(art) == active.read_file(art)
    rows = {r["id"]: r for r in review["records"] if r.get("file_path") == path and r.get("block") == block_number}
    for row in rows.values():
        assert all(row["review"].values())
        assert row["source_reference"]["block_sha256"] == scope["clean"]["block_sha256"]
        assert row["registered_reference"]["block_sha256"] == scope["installed"]["block_sha256"]
    approved = []
    for key in refs:
        row = rows[key]
        source, installed = row["source_reference"], row["registered_reference"]
        command = bytes.fromhex(installed["exact_command_hex"])
        offset = installed["command_offset"]
        assert blocks[1][offset:offset + len(command)] == command
        if "exact_command_hex" in source:
            command = bytes.fromhex(source["exact_command_hex"])
            offset = source["command_offset"]
            assert blocks[0][offset:offset + len(command)] == command
        else:
            body = bytes.fromhex(source["exact_body_hex"])
            offset = source["offset"]
            assert blocks[0][offset] == row["source_selector"] and blocks[0][offset + 1:offset + 1 + len(body)] == body
        approved.append({k: row[k] for k in ("id", "speaker", "source_selector", "Japanese", "english",
                                           "source_reference", "registered_reference", "review")})
    report = review.get("focused_gameplay")
    if report is None:
        report_path = Path(review["Maria_replay"])
        report = base.load(report_path)
        evidence[str(report_path)] = base.digest(report_path)
    assert report["candidate_sha256"] == review["candidate_sha256"]
    assert report["initialized_excerpts"] and not report["natural_story_triggers_claimed"]
    sample, = [row for row in report["observations"] if row["id"] == sample_id]
    picture(sample["capture"])
    return dict(file_path=path, block=block_number, native_command_paths=scope,
        independently_reviewed_inline_speeches=approved, earlier_focused_screenshot=sample,
        current_story_block_matches_earlier_focus=True, exact_stored_label_to_image_unverified=True,
        new_gameplay_runs=0), evidence


def sheet(title, scenes):
    examples = [(r["subject"], r["capture"]) for r in title["visual_samples"]]
    examples += [(f"{sample['independently_reviewed_inline_speeches'][-1]['speaker']} dialogue fixture",
                  sample["earlier_focused_screenshot"]["capture"]) for sample in scenes.values()]
    panel = Image.new("RGB", (768, 430), "#172630")
    draw = ImageDraw.Draw(panel)
    for i, (name, capture) in enumerate(examples):
        x, y = (i % 3) * 256, (i // 3) * 215
        draw.text((x + 5, y + 2), name, fill="white")
        image = picture(capture)
        y0 = 192 if i >= 4 else 0
        panel.paste(image.crop((0, y0, 256, y0 + 192)), (x, y + 16))
    panel.save(SHEET)


def main():
    release, review, prior, inventory, older, title = map(base.load,
        (current.RELEASE, current.REVIEW, PREVIOUS, WORKLIST, opening.OUT, CURRENT_TITLE))
    ours = release["candidate_sha256"]
    assert base.digest(current.ROM) == ours == review["candidate_sha256"] == prior["candidate_sha256"] == title["candidate_sha256"]
    assert base.digest(current.parent.ROM) == older["candidate_sha256"] == release["predecessor"]["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, en = (img.read_file(current.ARM) for img in (clean, active))
    common = active.read_file(current.COMMON)
    assert native.digest(en) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    reference = {r["message_ID"]: r for r in inventory["records"]}
    binding = {r["message_ID"]: r for r in review["shared_consumer_binding"]["records"]}
    assert set(prior["remaining_without_scoped_disposition"]) == DRAFTS.keys()
    title_path = title_segment(clean, active, older, title)
    scenes, evidence = {}, {}
    for key, spec in STORY.items():
        scenes[key], files = story_exchange(spec, clean, active)
        evidence.update(files)
    results = []
    for key, (draft, reason) in DRAFTS.items():
        row = stored_record(key, source, installed, reference, binding)
        assert row["source_review"]["english"] == draft and row["source_hex"] == row["installed_hex"]
        assert base.digest(row["source_review"]["path"]) == row["source_review"]["sha256"]
        row.update(draft_english_retained=draft, retention_reason=reason, native_direct_label_display_unverified=True,
            scope="The DS title composes the associated opening sequence from textures without a COMMON label lookup."
            if key not in STORY else "The tested original story exchange shows both identities through inline dialogue. The archived art association is still open.")
        results.append(row)
    sheet(title_path, scenes)
    base.save(OUT, dict(candidate_sha256=ours, records=results, title_display_scope=title_path, related_story_exchanges=scenes,
        remaining_without_scoped_disposition=sorted(STORY), exact_archived_artwork_identities_open=sorted(DRAFTS),
        new_gameplay_runs=0, new_ROM=False, hardware=False, sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence=evidence | {str(p): base.digest(p) for p in (PREVIOUS, WORKLIST, opening.OUT, CURRENT_TITLE,
            current.RELEASE, current.REVIEW, Path(__file__))}))
    print("Bound both title descriptions to their verified display scope and narrowed both story label leads.")


if __name__ == "__main__":
    main()
