"""Resolve scoped legacy setup, save, and recruitment display paths."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import check_damaged_save_digits_20261120 as damage
from scripts import observe_legacy_checksum_path_20261123 as corrupt
from scripts import observe_legacy_setup_paths_20261123 as live
from scripts import verify_early_setup_current_20261122 as early
from scripts import verify_title_reports_label_20261123 as options
from scripts.reconcile_gallery_caption_dispositions_20261123 import WORKLIST, picture
from scripts.reconcile_promotional_display_paths_20261123 import OUT as PROMO, rgb5
from scripts.reconcile_story_still_label_dispositions_20261123 import previous, verify_commands
from scripts.seal_shared_text_source_v1 import reference


base, current, native = live.base, live.current, live.current.native
OUT = WORKLIST.with_name("legacy_setup_and_recruitment_20261123.json")
SHEET = OUT.with_suffix(".png")
ART = {3500: 234, 3515: 238}
RELEASES = Path("releases")
HISTORICAL = {
    "angelo": RELEASES / "all_routes_editorial_20261123_hodram_recruitment_and_sails_candidate",
    "samwell": RELEASES / "all_routes_editorial_20261123_rafael_mediterranean_followups_candidate",
    "checksum": RELEASES / "all_routes_editorial_20261120_damaged_save_digits_candidate",
}
FINDINGS = {
    100: "The verified DS editor offers First Name, Middle Name, Last Name, Company, and Birthday. This setup flow has no three-skill selector.",
    101: "The editor asks whether all character details are OK through COMMON 120. The stored skill-specific confirmation has its own three substitutions.",
    102: "The Sound screen gives music and sound effects their own working volume controls and returns to the three original Options entries.",
    103: "The birthday instruction has an independent DS owner. Edit Birthday opens the calendar, then displays the new date in the editor.",
    117: "The verified checksum failure displays the separate numbered DS warning. The shorter archive string describes corruption alone.",
    330: "The Sound screen adjusts music volume with a meter. The stored on/off question describes a separate interaction.",
    331: "The sound-effects volume changes independently and returns to its original value. The stored on/off question was never selected on this path.",
    332: "The clean and installed title Options menus have three original descriptors, none for vibration. The stored question is outside this menu's display path.",
    333: "The DS Sailing Help control has its own ARM9 prompt. Both displayed state orders and the cancel path retain their original behavior.",
}


def read_capture(case, release, scheduler):
    root = live.ROOT / case
    paths = [root / p for p in ("terminal.json", "requests.json", "capture/capture_report.json", "source_contract.json")]
    terminal, trace, report, contract = map(base.load, paths)
    events, frames, end, _, donor = scheduler(case)
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert report["frames"] == terminal["completed_frames"] == end and report["scripted_input_schedule"] == events
    assert report["exact_requested_capture_frames"] == frames
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert bool(report.get("battery_save_preloaded")) == bool(donor)
    if donor:
        preload = report["battery_save_preloaded"]
        assert preload["copied_byte_exact_before_cold_boot"] and preload["source_sha256"] == donor["source_sha256"]
    assert all(base.digest(p) == digest for p, digest in terminal["evidence"].items())
    assert base.digest(paths[-1]) == trace["source_contract_sha256"]
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert len(trace["source_requests"]) == terminal["COMMON_requests"]
    held = {r["frame"]: r for r in report["frames_captured"] if r["path"].endswith("_cold_boot.png")}
    assert set(frames) <= held.keys()
    return trace, held, {str(p): base.digest(p) for p in paths}


def registered_review(directory):
    path = directory / "verification/registered_review.json"
    assert base.digest(path) == base.load(directory / "checksums.json")["verification/registered_review.json"]
    return base.load(path), path


def setup_evidence(ja, en, jp, installed, release):
    previous = base.load(early.OUTPUT)
    trace, frames, inputs = read_capture("setup", release, live.schedule)
    assert [r["message_ID"] for r in trace["source_requests"]] == [120] * 4
    assert not trace["rows"]
    for old in previous["character_editor"]["matches_prior_framebuffers"]:
        assert picture(old).tobytes() == picture(frames[old["frame"]]).tobytes()
    fields = previous["current_registered_editor_fields"]
    for field in fields:
        assert all(field["review"].values())
        source, active = field["source_reference"], field["current_reference"]
        ptr, start, length = (source[k] for k in ("pointer_field", "ARM9_offset", "allocation"))
        assert unpack_from("<I", ja, ptr) == unpack_from("<I", en, ptr) == (0x02000000 + start,)
        assert ja[start:start + length].hex() == source["raw_hex"]
        assert native.digest(en[active["start"]:active["end"]]) == active["sha256"]
    row, = [r for r in previous["active_retained_records"] if r["message_ID"] == 120]
    assert jp[120].text.hex() == row["source_hex"] and installed[120].text.hex() == row["current_hex"]
    assert all(row["review"].values())
    selected = {str(n): frames[n] for n in (2200, 4191, 4991, 5391, 6191, 6591)}
    return dict(exact_two_screen_holds=13, gameplay="Ordinary character setup and cancellation from New Game.",
        two_native_request_pairs=trace["source_requests"], verified_editor_fields=fields,
        actual_confirmation=dict(message_ID=120, english=row["english"], source_reference=reference(jp[120]),
            installed_reference=reference(installed[120]), review=row["review"]), samples=selected), inputs


def options_evidence(ja, en, installed, release):
    trace, frames, inputs = read_capture("options", release, live.schedule)
    requests = trace["source_requests"]
    assert len(requests) == 10 and {r["message_ID"] for r in requests} == {3251}
    assert not trace["rows"]
    a, b = (options.stage.menu(arm) for arm in (ja, en))
    assert [{k: v for k, v in r.items() if k != "text_hex"} for r in a] == [
        {k: v for k, v in r.items() if k != "text_hex"} for r in b]
    assert [bytes.fromhex(r["text_hex"]).decode("ascii") for r in b] == ["Sound", "Reports", "Sailing Help"]
    old = base.load(options.LIVE)
    font = GameAsciiFont.from_arm9(en)
    images = {n: picture(ref) for n, ref in frames.items()}
    for row in old["options_holds"]:
        assert images[row["frame"]].tobytes() == picture(row["held_frames"][1]).tobytes()
    rows, cases = options.state_checks(ja, en, images, font)
    assert cases == old["toggle_holds"]
    for sample, reduced, restored, box in ((3000, 3400, 5800, (24, 320, 103, 338)),
                                           (3000, 4200, 5000, (152, 320, 231, 338))):
        origin, middle, end = (images[n].crop(box).tobytes() for n in (sample, reduced, restored))
        assert origin != middle and origin == end
    assert images[12200].tobytes() == picture(old["title_return_frame"]).tobytes()
    track, = [r for r in base.load(early.OUTPUT)["active_retained_records"] if r["message_ID"] == 3251]
    assert installed[3251].text.hex() == track["current_hex"] and all(track["review"].values())
    title_ink = []
    x0, _ = track["native_center"]
    expected = {(x0 + i * 5 + x, 259 + y) for i, ch in enumerate(track["english"])
                for x in range(6) for y in range(11) if font.decode(ch).getpixel((x, y))}
    for n in (3000, 3400, 3800, 4200, 5000, 5400, 5800):
        actual = {(x, y) for x in range(128) for y in range(258, 271)
                  if images[n].getpixel((x, y)) == (230, 230, 230)}
        assert actual == expected
        title_ink.append(dict(frame=n, ink_pixels=len(actual)))
    return dict(gameplay="Ordinary title Options and Sound Setup, both toggle directions and cancellation.",
        clean_native_menu=a, installed_native_menu=b, exact_menu_holds=len(old["options_holds"]),
        actual_toggle_owners=rows, request_pairs=requests, complete_music_title_masks=title_ink,
        complete_toggle_holds=cases, both_volume_meters_restored=True, title_return=frames[12200],
        samples={str(n): frames[n] for n in (3000, 6600, 9800, 10600, 11400)}), inputs


def checksum_evidence(ja, en, release):
    trace, frames, run = read_capture("corrupt_slot", release, corrupt.schedule)
    assert not trace["source_requests"]
    fixture = base.load(corrupt.FIXTURE)
    branch, modal = trace["rows"]
    assert branch["frame"] == modal["frame"] and branch["slot"] == fixture["slot_index"] == 0
    for k in ("stored", "calculated"):
        assert branch[k] == fixture["native_checksum_results"][1][k]
    assert branch["stored"] != branch["calculated"]
    earlier, prior_path = registered_review(HISTORICAL["checksum"])
    row, = earlier["records"]
    assert all(row["review"].values())
    ref = row["current_reference"]
    start = ref["suffix_offset"]
    source = bytes.fromhex(ref["source_suffix_hex"])
    target = bytes.fromhex(ref["current_suffix_hex"])
    assert ja[start:start + len(source)] == source and en[start:start + len(target)] == target
    call = ref["address"] - 0x02000000
    assert en[call:call + 4].hex() == ref["target_hex"]
    expected = b"1" + target.rstrip(b"\0")
    assert bytes.fromhex(modal["body_hex"]) == expected
    font = GameAsciiFont.from_arm9(en)
    first, second = expected.decode("ascii").split("\n")
    glyphs = damage.font_points(font, first, 22, 297) | damage.font_points(font, second.lstrip(), 22, 313)
    for frame in (3700, 3800):
        image = picture(frames[frame])
        actual = {(x, y) for x in range(10, 246) for y in range(294, 355)
                  if image.getpixel((x, y)) == damage.prior.INK}
        assert actual == glyphs
    for frame in (4200, 4400, 4700, 5100):
        picture(frames[frame])
    assert picture(frames[4200]).tobytes() == picture(frames[4400]).tobytes()
    run.update({str(p): base.digest(p) for p in (corrupt.FIXTURE, prior_path)})
    return dict(gameplay="Original Continue controls with the existing one-bit checksum fixture.",
        native_branch=branch, native_modal=modal, actual_warning=row, complete_glyph_pixels=len(glyphs),
        COMMON_requests=0, observed_warning_holds=[frames[3700], frames[3800]],
        slot_and_title_returns=[frames[n] for n in (4200, 4400, 4700, 5100)]), run


def stored_record(key, source, active, inventory, binding):
    row = inventory[key]
    jp, en = source[key], active[key]
    assert (jp.text.hex(), en.text.hex()) == (row["source_hex"], row["installed_hex"])
    assert reference(jp) == row["source_reference"] and reference(en) == row["installed_reference"] == binding[key]["installed"]
    assert binding[key]["exact_body_retained"]
    return dict(message_ID=key, file_path=current.COMMON, source_reference=reference(jp),
        installed_reference=reference(en), source_Japanese=jp.text.decode("cp932"),
        installed_text=en.text.decode("cp932"), source_hex=jp.text.hex(), installed_hex=en.text.hex(),
        source_review=row["earlier_draft"], other_direct_COMMON_display_unverified=True)


def exact_story_context(row, clean, active):
    for image, ref in ((clean, row["source_reference"]), (active, row["registered_reference"])):
        block = native.IlnkContainer.parse(image.read_file(row["file_path"])).blocks[row["block"]]
        command = bytes.fromhex(ref["exact_command_hex"])
        start = ref["command_offset"]
        assert native.digest(block) == ref["block_sha256"]
        assert block[start:start + len(command)] == command
    return {k: row[k] for k in ("id", "speaker", "Japanese", "english", "source_reference", "registered_reference", "review")}


def recruitment_evidence(clean, active, ja, en):
    history = base.load(previous.OUTPUT)
    assets = {r["image_index"]: r for r in history["assets"] if r["image_index"] in ART.values()}
    plan = {index: [r["source"] for r in asset["commands"] if r["source"]["path"].startswith("/data/")]
            for index, asset in assets.items()}
    assert all(len(v) == 4 and len({r["path"] for r in v}) == 4 for v in plan.values())
    clean_hits, clean_count = verify_commands(plan, clean, ja, "clean")
    active_hits, active_count = verify_commands(plan, active, en, "installed")
    assert clean_count == active_count == 8 and clean_hits == plan
    expected = {k: previous.image_requests(data, sorted(assets)) for k, data in (("clean", ja), ("active", en))}
    assert expected == {"clean": 4, "active": 4}
    results = {}
    for key, index in ART.items():
        art = assets[index]
        path = art["filename"]
        japanese, installed = (img.read_file(path) for img in (clean, active))
        assert path == f"/evstill/evstill{index:03}.pxl"
        assert japanese == installed and native.digest(japanese) == art["asset_hashes"]["clean"]
        assert [(r["path"], r["block"], r["command_hex"]) for r in active_hits[index]] == [
            (r["path"], r["block"], r["command_hex"]) for r in clean_hits[index]]
        results[key] = dict(artwork_path=path, exact_archive_sha256=native.digest(installed),
            clean_story_commands=clean_hits[index], installed_story_commands=active_hits[index],
            offline_original_loads_per_ROM=2, candidate_asset_pixels_match_clean=True)
    angelo, angelo_proof = registered_review(HISTORICAL["angelo"])
    hit, = [r for r in angelo["focused_gameplay"]["ordinary_story_observations"] if r["id"] == "DK4_MES_B158_R0039"]
    speech, = [r for r in angelo["records"] if r["id"] == hit["id"]]
    assert hit["exact_complete_body_mask"] and hit["speaker"] == speech["speaker"] == "Angelo Puccini"
    art = PxlImage.from_bytes(active.read_file(results[3500]["artwork_path"])).render()
    assert rgb5(picture(hit["capture"]).crop((0, 0, 256, 192))).tobytes() == rgb5(art).tobytes()
    results[3500].update(prior_ordinary_gameplay=hit, exact_upper_RGB5_pixels=49152,
        story_context=exact_story_context(speech, clean, active),
        disposition="The original four route recruitment scenes load Angelo's entrance portrait independently.")
    samwell, samwell_proof = registered_review(HISTORICAL["samwell"])
    turn, = [r for r in samwell["records"] if r["id"] == "DK4_MES_B172_R0062"]
    assert turn["observed_focused"]["exact_complete_body_mask"] and "えっへん" in turn["Japanese"]
    results[3515].update(prior_focused_context=turn["observed_focused"], registered_excerpt=turn["english"],
        story_context=exact_story_context(turn, clean, active),
        disposition="The native recruiting branches load Samwell's standing pose. His later Ahem confirms the label's self-satisfied tone.",
        current_asset_reached_in_prior_screenshot=False)
    paths = (previous.OUTPUT, angelo_proof, samwell_proof)
    return results, {str(p): base.digest(p) for p in paths}


def write_sheet(setup, options_live, checksum, art, active):
    panels = [(name, picture(sample)) for name, sample in (
        ("Birthday in current setup", setup["samples"]["4191"]),
        ("Current Sound Setup", options_live["samples"]["3000"]),
        ("Sailing Help confirmation", options_live["samples"]["9800"]),
        ("Current checksum warning", checksum["observed_warning_holds"][0]),
        ("Angelo in ordinary gameplay", art[3500]["prior_ordinary_gameplay"]["capture"]))]
    panels.append(("Samwell's original image, decoded offline", PxlImage.from_bytes(active.read_file(art[3515]["artwork_path"])).render()))
    sheet = Image.new("RGB", (768, 404 * 2), "#1f2830")
    draw = ImageDraw.Draw(sheet)
    for i, (label, panel) in enumerate(panels):
        x, y = i % 3 * 256, i // 3 * 404
        draw.text((x + 4, y + 3), label, fill="white")
        sheet.paste(panel, (x, y + 19))
    sheet.save(SHEET)


def main():
    release, review, state, inventory = map(base.load, (current.RELEASE, current.REVIEW, PROMO, WORKLIST))
    assert release["candidate_sha256"] == review["candidate_sha256"] == base.digest(current.ROM)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"] == inventory["clean_sha256"]
    predecessor = base.load(current.parent.RELEASE)
    assert state["candidate_sha256"] == predecessor["candidate_sha256"] == release["predecessor"]["candidate_sha256"]
    assert all(release[k] == predecessor[k] for k in ("target_ARM9_sha256", "target_COMMON_sha256", *(
        f"target_SC{i}_sha256" for i in range(4))))
    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, en = (img.read_file(current.ARM) for img in (clean, active))
    common = active.read_file(current.COMMON)
    assert native.digest(en) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    worklist = {r["message_ID"]: r for r in inventory["records"]}
    binding = {r["message_ID"]: r for r in review["shared_consumer_binding"]["records"]}
    before = set(state["remaining_outside_checked_title_content"])
    assert len(before) == 38 and len(worklist) == len(binding) == 276
    setup, setup_files = setup_evidence(ja, en, source, installed, release)
    options_live, options_files = options_evidence(ja, en, installed, release)
    checksum, checksum_files = checksum_evidence(ja, en, release)
    art, art_files = recruitment_evidence(clean, active, ja, en)
    rows = []
    for n in sorted(FINDINGS.keys() | ART.keys()):
        row = stored_record(n, source, installed, worklist, binding)
        row.update(verified_scoped_path=FINDINGS[n] if n in FINDINGS else art[n]["disposition"])
        if n in art:
            row["story_art"] = art[n]
        elif n == 117:
            row["display_proof"] = "checksum"
        else:
            row["display_proof"] = "setup" if n in (100, 101, 103) else "options"
        rows.append(row)
    added = {r["message_ID"] for r in rows}
    assert len(added) == 11 and added <= before
    write_sheet(setup, options_live, checksum, art, active)
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], source_storage_inventory=len(worklist),
        reviewed_entries=rows, remaining_without_scoped_disposition=sorted(before - added),
        character_setup=setup, options_and_sound=options_live, checksum=checksum,
        fresh_ordinary_controller_runs=2, fresh_focused_checksum_fixtures=1,
        fresh_native_story_loader_blocks_per_ROM=8, new_ROM=False, new_dialogue_credit=0, hardware=False,
        direct_COMMON_references_remain_tracked=True, sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence=setup_files | options_files | checksum_files | art_files | {str(p): base.digest(p) for p in (
            PROMO, WORKLIST, early.OUTPUT, options.LIVE, current.RELEASE, current.REVIEW, Path(__file__))}))
    print(f"Verified {len(added)} further display scopes; {len(before - added)} entries still need a scoped disposition.")


if __name__ == "__main__":
    main()
