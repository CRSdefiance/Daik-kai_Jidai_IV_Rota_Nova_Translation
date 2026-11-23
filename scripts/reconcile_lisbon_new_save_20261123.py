"""Review the current New Game and ordinary cartridge save paths for COMMON 124."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import checkpoint_ending_save_20261120 as earlier_save
from scripts import observe_create_save_lisbon_20261123 as live
from scripts import reconcile_opening_label_dispositions_20261123 as opening
from scripts.checkpoint_market_shared_consumers_20261114 import font_mask
from scripts.reconcile_legacy_fleet_and_quit_paths_20261123 import (
    WORKLIST, base, common_message_entries, current, native, owned_entries, picture, stored_record,
    DIRECTORY_OFFSET, TABLE_OFFSET,
)
from scripts.reconcile_title_variant_display_20261123 import OUT as PREVIOUS


OUT = PREVIOUS.with_name("lisbon_new_save_20261123.json")
SHEET = OUT.with_suffix(".png")
START, END = 0xA000, 0x14000
SYSTEM = 0x3C000
WORDS = ("DK4_SAVE_SELECT_TITLE", "DK4_SAVE_UNUSED", "DK4_SAVE_CREATE_CONFIRM",
         "DK4_SAVE_PROGRESS_ACTION", "DK4_SAVE_PROGRESS_FORMAT")


def verify_write(report):
    copy = report["battery_save_preloaded"]
    assert copy["copied_byte_exact_before_cold_boot"] and not copy["savestate_loaded"]
    source, result = map(Path, (copy["source"], copy["destination"]))
    before, after = source.read_bytes(), result.read_bytes()
    assert native.digest(before) == copy["source_sha256"]
    assert len(before) == len(after) == copy["bytes"] == 262266
    assert before[:START] == after[:START] and before[END:SYSTEM] == after[END:SYSTEM]
    assert before[START:END] == b"\xff" * (END - START)
    slot = after[START:END]
    assert slot[:4] == b"DK4R"
    checksum, = unpack_from("<I", slot, 4)
    assert checksum == sum(n if n < 128 else n - 256 for n in slot[8:]) & 0xFFFFFFFF
    metadata = [(SYSTEM + i, a, b) for i, (a, b) in enumerate(zip(before[SYSTEM:], after[SYSTEM:], strict=True)) if a != b]
    assert metadata == [(0x3C004, 246, 247), (0x3C043, 0, 1)]
    return dict(donor=str(source), donor_sha256=copy["source_sha256"], preserved_result=str(result),
        result_sha256=native.digest(after), selected_slot=2, exact_slot_span=[START, END],
        written_slot_checksum=checksum, checksum_matches_native_signed_byte_sum=True,
        bytes_changed_in_selected_slot=sum(a != b for a, b in zip(before[START:END], slot, strict=True)),
        system_metadata_changes=metadata)


def save_text(ja, en):
    records = {r["id"]: r for r in base.load(earlier_save.OUTPUT)["records"] if "id" in r}
    verified = []
    for key in WORDS:
        old = records[key]
        context = "Original save-slot picker reached from the Lisbon System menu." if key in WORDS[:2] else old["context"]
        row = earlier_save.arm_record(key, old["source_reference"]["pointer_field"] - earlier_save.BASE,
            ja, en, old["english"], old["localization_note"], context, old["runtime_substitutions"])
        assert row["source_reference"] == old["source_reference"] and row["review"] == old["review"]
        assert row["source_hex"] == old["source_hex"] and row["current_hex"] == old["current_hex"]
        verified.append(row)
    return verified


def review_holds(shots, en):
    frames = (4800, 5600, 6000, 6400, 6800, 6840, 7700)
    images = {frame: picture(shots[frame]) for frame in frames}
    # The comparison isolates the changed selection highlight on the same unused row.
    cancel_diff = ImageChops.difference(images[6400], images[5600]).getbbox()
    assert cancel_diff == (0, 228, 256, 256)
    assert images[6000].tobytes() == images[6800].tobytes()
    system_diff = ImageChops.difference(images[4800], images[7700]).getbbox()
    assert system_diff == (101, 248, 155, 268)
    font = GameAsciiFont.from_arm9(en)
    verified = []
    for frame in (6000, 6800):
        text = "Create a new save?"
        count = font_mask(images[frame], font, text, 16, 297, (14, 296, 240, 310), (0, 8, 0))
        verified.append(dict(frame=frame, lines=[text], body_glyph_ink=count, capture=shots[frame]))
    lines = ("Save in progress.", "Do not turn off.")
    counts = [font_mask(images[6840], font, text, 56, y, (55, y, 204, y + 11), (0, 8, 0))
              for text, y in zip(lines, (277, 289), strict=True)]
    verified.append(dict(frame=6840, lines=list(lines), glyph_ink_by_row=counts, capture=shots[6840]))
    samples = ((5600, "Unused slot selected"), (6000, "Original Yes/No confirmation"), (6400, "After cancelling"),
               (6800, "Confirmation after selecting again"), (6840, "Cartridge write status"), (7700, "Back in System"))
    sheet = Image.new("RGB", (768, 808), "#172630")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, label) in enumerate(samples):
        x, y = i % 3 * 256, i // 3 * 404
        draw.text((x + 4, y + 3), label, fill="white")
        sheet.paste(images[frame], (x, y + 19))
    sheet.save(SHEET)
    return verified, dict(captures={frame: shots[frame] for frame in frames},
        cancel_return_changed_selection_row=cancel_diff, system_return_changed_save_highlight=system_diff)


def main():
    release, review, state, inventory, start = map(base.load,
        (current.RELEASE, current.REVIEW, PREVIOUS, WORKLIST, opening.OUT))
    ours = release["candidate_sha256"]
    assert base.digest(current.ROM) == ours == review["candidate_sha256"] == state["candidate_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.parent.ROM) == start["candidate_sha256"] == release["predecessor"]["candidate_sha256"]
    clean, active, before = map(base.NdsImage.open, (native.CLEAN, current.ROM, current.parent.ROM))
    files, predecessor = map(native.files, (active, before))
    assert files.keys() == predecessor.keys()
    assert {key for key in files if files[key] != predecessor[key]} == {"/_pxl/online/Online61.pxl", "/_pxl/online/Online62.pxl"}
    early = start["checked_runs"]["rafael"]
    assert early["battery_save_source"] is None and [r["message_ID"] for r in early["COMMON_requests"]] == [120, 120]
    assert all(base.digest(path) == sha for path, sha in early["evidence"].items())
    ja, en = (img.read_file(current.ARM) for img in (clean, active))
    common = active.read_file(current.COMMON)
    assert native.digest(en) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    worklist = {r["message_ID"]: r for r in inventory["records"]}
    binding = {r["message_ID"]: r for r in review["shared_consumer_binding"]["records"]}
    record = stored_record(124, source, installed, worklist, binding)
    record["verified_scoped_path"] = ("Rafael can open a new game from blank battery state. The ordinary DS Save action "
        "creates a cartridge save through its existing slot confirmation and write status.")
    folder = live.ROOT / "create"
    report_path = folder / "capture/capture_report.json"
    terminal_path = folder / "terminal.json"
    trace_path = folder / "requests.json"
    report, trace, terminal = map(base.load, (report_path, trace_path, terminal_path))
    events, requested, end, _, donor = live.schedule("create")
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == ours
    assert report["frames"] == terminal["completed_frames"] == end
    assert report["scripted_input_schedule"] == events and report["exact_requested_capture_frames"] == requested
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert not trace["source_requests"] and not terminal["COMMON_requests"] and not trace["errors"] and not trace["mismatches"]
    assert trace["all_host_slots_restored_and_core_file_exact"]
    assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    assert trace["source_contract_sha256"] == base.digest(folder / "source_contract.json")
    assert base.load(folder / "source_contract.json")["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert all(base.digest(path) == sha for path, sha in terminal["evidence"].items())
    write, retentions = verify_write(report), save_text(ja, en)
    holds, transitions = review_holds(opening.frames(report), en)
    remaining = set(state["remaining_without_scoped_disposition"])
    assert len(remaining) == 14 and 124 in remaining
    base.save(OUT, dict(candidate_sha256=ours, reviewed_entries=[record],
        remaining_without_scoped_disposition=sorted(remaining - {124}), observed_ordinary_save=True,
        observed_earlier_ordinary_new_game_on_exact_dependencies=early, current_save_write=write,
        retained_active_prose=retentions, complete_glyph_holds=holds, gameplay_transitions=transitions,
        new_ROM=False, hardware=False, sheet=dict(path=str(SHEET), sha256=base.digest(SHEET)),
        evidence={str(path): base.digest(path) for path in (PREVIOUS, opening.OUT, WORKLIST, current.RELEASE,
            current.REVIEW, earlier_save.OUTPUT, report_path, terminal_path, trace_path, Path(__file__))}))
    print(f"Verified ordinary new-slot save, original checksum, cancel and return; {len(remaining) - 1} shared entries remain.")


if __name__ == "__main__":
    main()
