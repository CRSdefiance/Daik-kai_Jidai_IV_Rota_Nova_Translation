"""Stage four ordinary Amsterdam story findings inside their existing allocations."""

from argparse import ArgumentParser
from pathlib import Path
import sys
from types import FunctionType, SimpleNamespace

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_fleet_diversion_release_20261125 as checks
from scripts import headless_desmume_v193 as harness
from scripts import register_cartridge_title_20261123 as registry_guards
from scripts import stage_square_country_briefings_20261115 as native
from scripts import verify_amsterdam_hodram_arrival_20261125 as review
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, NdsImage, REGISTRY, digest, read, reference, sha256, write


parent, panels = review.play.current, review.panels
ROOT = Path(".codex-release-work/amsterdam_hodram_wraps_20261125").resolve()
ROM, STORED = ROOT / "Amsterdam_Hodram_Wraps_STAGED.nds", ROOT / "stored_proof.json"
OUT = review.OUT.with_name("amsterdam_hodram_wraps_preflight_20261125.json")
STORY = review.PATH
CAPTURE = ROOT / "paired"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE, QA = ROOT / "startup/capture/capture_report.json", ROOT / "qa_passed.xml"
FINAL_REPLAY_FRAME = 34100
DRAFTS = {
    (44, 29): ("This is my turf. You can't barge in and trade here!",
               ("This is my turf.", "You can't barge in and trade here!"),
               "Lil claims the port as hers and warns Hodram against trading without her say-so. Her threat continues as one sentence."),
    (44, 49): ("Aha! You're a military man. Soldiers, explorers, pirates... Is everybody trading these days?",
               ("Aha! You're a military man.", "Soldiers, explorers, pirates...", "Is everybody trading these days?"),
               "Lil recognizes a military man and mockingly lists the three groups she sees taking up trade. Her question stays on one line."),
    (44, 53): ("Outsiders keep barging in on us merchants. They act like they own the place. I'm sick of it!",
               ("Outsiders keep barging in", "on us merchants.", "They act like they own the place.", "I'm sick of it!"),
               "Her complaint keeps the repeated encroachment on merchants, the outsiders' arrogance and her personal frustration."),
    (137, 89): ("Sea trade thrives in many Mediterranean nations. Lisbon and Seville are big ports. We may find good recruits there.",
                ("Sea trade thrives in many", "Mediterranean nations.", "Lisbon and Seville are big ports.", "We may find good recruits there."),
                "Gerhard explains why he expects capable recruits in the region and offers Lisbon and Seville as leads. The geographic term and the prospects stay together."),
}


def fit_layout(renderer, context, kanji, body, extent, lines):
    raster = panels.story_display.display.raster
    clean_page, = raster(context, kanji, renderer, body, list(lines), 1)
    # The fixed allocation belongs to the command, not the prose. If tail
    # padding would advance the fourth row again, leave it before line breaks.
    missing = extent - len(body)
    pieces = body.split(b"\n")
    remaining = missing
    distributed = list(pieces)
    for index, piece in enumerate(pieces):
        padding = min(remaining, max(33 - len(piece), 0))
        distributed[index] = piece + b" " * padding
        remaining -= padding
    attempts = [body.ljust(extent, b" ")]
    if remaining == 0:
        attempts.append(b"\n".join(distributed))
    for proposed in attempts:
        try:
            page, = raster(context, kanji, renderer, proposed, list(lines), 1)
        except AssertionError:
            continue
        assert page["native_plane_hex"] == clean_page["native_plane_hex"] and len(proposed) == extent
        return proposed, page
    raise ValueError(f"No native padding for {len(body)} visible-layout bytes in a {extent}-byte command")


def main():
    release = read(parent.RELEASE)
    assert digest(parent.ROM) == release["candidate_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] and not ROOT.exists()
    source, target = map(NdsImage.open, (CLEAN, parent.ROM))
    clean, before = map(native.files, (source, target))
    arm = before[parent.ARM]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert registry_guards.right_bound(arm, release["right_bound_configuration"])["matched_repair_spans"] == 8
    kanji = target.read_file("/GRP/KANJI.FNT")
    context = SimpleNamespace(arm=arm, image=target)
    renderer = panels.town.clipped_renderer(context)
    clean_bank, bank = (IlnkContainer.parse(data[STORY]) for data in (clean, before))
    pending, previews = [], []
    for receipt in (review.OUT, review.APOLOGY_OUT):
        seen = read(receipt)
        assert seen["candidate_sha256"] == release["candidate_sha256"]
        for row in seen["records"]:
            key = row["block"], int(row["id"].rsplit("_R", 1)[1])
            if key not in DRAFTS:
                continue
            assert row["decision"] == "wrap revision needed" and row["review"]["formatting"] is False
            block, number = key
            original, installed = (bytes.fromhex(row[field]["exact_command_hex"])
                                   for field in ("source_reference", "installed_reference"))
            at = row["installed_reference"]["command_offset"]
            clean_at = row["source_reference"]["command_offset"]
            assert original == clean_bank.blocks[block][clean_at:clean_at + len(original)]
            assert installed == bank.blocks[block][at:at + len(installed)]
            assert installed[:6] == original[:6] and installed[:5] == b"\0\x40\xff\xff\0" and installed.endswith(b"\0")
            current_body, source_body = map(panels.bytes_for, (installed, original))
            assert not any(token in raw for token in (b"FI", b"FO", b"FA", b"FU", b"%") for raw in (source_body, current_body))
            prose, lines, reason = DRAFTS[key]
            protected = lines[1:] if block == 137 or number == 29 else lines
            draft = row | dict(english=prose, protected_phrases=protected)
            formatted, plan = panels.layout.plan_progressive(draft, installed[5], current_body, source_body)
            assert tuple(plan["lines"]) == lines and plan["expected_native_pages"] == 1, (key, plan["lines"])
            assert len(formatted) <= len(current_body) and formatted.isascii() and b"\0" not in formatted
            try:
                fitted, page = fit_layout(renderer, context, kanji, formatted, len(current_body), lines)
            except (ValueError, AssertionError) as error:
                raise ValueError(f"Native allocation failed for B{block} R{number}") from error
            plane = bytes.fromhex(page["native_plane_hex"])
            assert page["native_independent_plane_equal"] and len(plane) == 216 * 64
            # Portrait sheets use a 228-pixel canvas. The story renderer's
            # proven drawable area is the leftmost 216 pixels.
            preview = b"".join(plane[offset:offset + 216] + bytes(12) for offset in range(0, len(plane), 216))
            previews.append((f"B{block} R{number}", preview))
            suffix = installed[6 + len(current_body):]
            assert suffix.startswith(b"\0")
            replacement = installed[:6] + fitted + suffix
            assert len(replacement) == len(installed)
            payload = bank.blocks[block]
            bank.blocks[block] = payload[:at] + replacement + payload[at + len(installed):]
            pending.append(row | dict(english=prose, localization_note=reason, decision="revision proposed",
                exact_proposed_command_hex=replacement.hex(), formatter_plan=plan, native_preview_sha256=sha256(plane).hexdigest(),
                same_speaker_controls=True, same_extent=True, substitution_count=0,
                review=dict.fromkeys(GATES, True) | {"formatting": False}))
    assert len(pending) == len(DRAFTS)
    archive = bank.to_bytes()
    directory_end = 8 + (len(bank.blocks) + 1) * 4
    assert archive[:directory_end] == before[STORY][:directory_end] and len(archive) == len(before[STORY])
    old = IlnkContainer.parse(before[STORY])
    assert {i for i, (a, b) in enumerate(zip(old.blocks, bank.blocks, strict=True)) if a != b} == {44, 137}
    for row in pending:
        ref = row["current_reference"]
        block, at = row["block"], ref["command_offset"]
        payload = bank.blocks[block]
        current = bytes.fromhex(ref["exact_command_hex"])
        assert payload[at:at + len(current)].hex() == row["exact_proposed_command_hex"]
        bank.blocks[block] = payload[:at] + current + payload[at + len(current):]
    assert bank.to_bytes() == before[STORY]
    target.replace_file(STORY, archive)
    after = native.files(target)
    assert before.keys() == after.keys() and {key for key in before if before[key] != after[key]} == {STORY}
    guard_spec = read(REGISTRY)["profiles"][release["profile"]]["source25_multiarchive_guard"]
    guard = bind_registered_story_percent_guard(guard_spec)(clean, after)
    assert not any(guard["source_bound_new_command_counts"].values())
    data = bytes(target.rom.save())
    target.replace_file(STORY, before[STORY])
    assert sha256(target.rom.save()).hexdigest() == release["candidate_sha256"]
    ROOT.mkdir()
    ROM.write_bytes(data)
    sheets = native.portrait_sheets(ROOT, previews)
    write(OUT, dict(parent=reference(parent.ROM), candidate=reference(ROM), records=pending, native_previews=sheets,
        source_reviews=[reference(review.OUT), reference(review.APOLOGY_OUT)], offline_native_validation=True,
        ordinary_replay_pending=True, new_editorial_credit=0))
    write(STORED, dict(candidate=reference(ROM), parent=reference(parent.ROM), proposal=reference(OUT),
        target_archive_sha256=sha256(archive).hexdigest(), exact_parent_inverse=True, changed_blocks=[44, 137],
        unchanged_story_directory=True, updated_internal_file=STORY, format_guard=guard))
    print("Staged four complete Amsterdam story reflows in their existing allocations.")


def replay():
    baseline_path = review.play.ROOT / "capture/capture_report.json"
    parent_report, stored = map(read, (baseline_path, STORED))
    assert digest(parent.ROM) == parent_report["ROM_sha256"] == stored["parent"]["sha256"]
    assert stored["candidate"] == reference(ROM)
    assert parent_report["cold_boot"] and not parent_report["savestate_loaded"] and not parent_report["callback_errors"]
    assert not any(value for key, value in parent_report.items() if key.startswith("synthetic_"))
    donor = parent_report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    schedule = [event for event in parent_report["scripted_input_schedule"] if event["start"] <= FINAL_REPLAY_FRAME]
    frames = sorted(frame for frame in panels.shots(parent_report, "_navigation.png") if 10800 <= frame <= FINAL_REPLAY_FRAME)
    assert frames[-1] == FINAL_REPLAY_FRAME
    inputs = ROOT / "inputs.json"
    write(inputs, schedule)
    old_args = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(CAPTURE), "--frames", str(FINAL_REPLAY_FRAME),
                    "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                    "--battery-save", donor["source"], "--touchscreen", "--capture-at", *map(str, frames)]
        harness.main()
    finally:
        sys.argv = old_args
    report = read(CAPTURE / "capture_report.json")
    assert report["ROM_sha256"] == stored["candidate"]["sha256"] and report["frames"] == FINAL_REPLAY_FRAME
    assert report["scripted_input_schedule"] == schedule and not report["callback_errors"]
    assert digest(donor["source"]) == donor["source_sha256"]


def release_checks(action):
    inputs = SimpleNamespace(draft=SimpleNamespace(current=parent), PROOF=STORED, ROM=ROM)
    scope = vars(checks) | dict(stage=inputs, PATCH=PATCH, REBUILT=REBUILT, PATCH_PROOF=PATCH_PROOF,
                                STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(checks.main.__code__, scope)(action)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", nargs="?", default="stage", choices=("stage", "replay", "patch", "startup"))
    action = parser.parse_args().action
    if action in ("patch", "startup"):
        release_checks(action)
    else:
        {"stage": main, "replay": replay}[action]()
