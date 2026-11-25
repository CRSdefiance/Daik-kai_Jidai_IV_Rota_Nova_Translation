"""Check the complete Options menu, both toggle directions and the sound controls."""

from inspect import getsource
from pathlib import Path
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import ImageChops

from scripts import checkpoint_gallery_options_legacy_20261114 as old_checks
from scripts import observe_options_paths_20261123 as play
from scripts import probe_options_narrow_prompts as options
from scripts import stage_title_reports_label_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
LIVE = stage.ROOT / "verified_options.json"
MENU_FRAMES = (2600, 6200, 6600, 7400, 8200, 9000, 9400, 10200, 11000, 11800)
PROMPTS = {
    "reports": ((7000, 7800), 8600, 0x3FDD0,
        "Display the current income-and-expense reporting setting and ask to switch it.",
        "Reports identifies the recurring notices. The direct question and state order fit a Yes/No choice."),
    "sailing": ((9800, 10600), 11400, 0x3FD4C,
        "Display the current at-sea operation help setting and ask to switch it.",
        "Sailing Help matches the menu label. The question preserves the current setting and proposed new value."),
}
HISTORICAL = Path("translations/editorial_checkpoints/SharedText_20261110_v1/options_legacy_observed_consumers_20261114_v1.json")
BASELINE_DRIVER = play.ROOT / "options/original_replay.py"


def exact_string(arm, ptr):
    start = ptr - options.BASE
    text, delim, _ = arm[start:start+96].partition(b"\0")
    assert delim and text
    return text


def run_data(root, sha):
    def source_path(path):
        if root == play.ROOT and Path(path).resolve() == Path(play.__file__).resolve():
            return str(BASELINE_DRIVER)
        return path

    # The baseline was captured before the same runner gained its staged-ROM
    # option. Verify its original source bytes and retain that version.
    contract = checked_text(getsource(old_checks.verify_report), {
        'base.digest(path)==expected for path,expected in terminal["evidence"].items()':
            'base.digest(source_path(path))==expected for path,expected in terminal["evidence"].items()',
    })
    scope = vars(old_checks) | dict(source_path=source_path)
    exec(compile(contract, __file__ + "::replay-evidence", "exec"), scope)
    module = SimpleNamespace(ROOT=root, schedule=play.schedule)
    terminal, calls, frames = scope["verify_report"](module, "options", {"candidate_sha256": sha})
    assert terminal["COMMON_requests"] == len(calls) == 10 and not terminal["target_COMMON_calls"]
    assert [call["message_ID"] for call in calls] == [3251] * 10
    for lookup, copy in zip(calls[::2], calls[1::2], strict=True):
        assert (lookup["PC"], copy["PC"]) == (0x0205528C, 0x020534F4)
        assert lookup["caller_LR"] == copy["caller_LR"] and lookup["frame"] == copy["frame"]
    return calls, frames, {source_path(path): sha for path, sha in terminal["evidence"].items()}


def state_checks(clean, active, images, font):
    rows, cases = [], []
    for kind, (on, off, pointer, meaning, note) in PROMPTS.items():
        old_ptr, new_ptr = [unpack_from("<I", arm, pointer)[0] for arm in (clean, active)]
        ja, en = exact_string(clean, old_ptr), exact_string(active, new_ptr)
        assert ja.count(b"%s") == en.count(b"%s") == 2
        expected = options.PROMPTS[kind][2]
        assert en.decode("ascii") == expected
        for frame in (*on, off):
            current, proposed = ("Off", "On") if frame == off else ("On", "Off")
            text = expected % (current, proposed)
            size = old_checks.font_mask(images[frame], font, text, 16, 297, (16, 296, 237, 350), (0, 8, 0))
            cases.append(dict(frame=frame, kind=kind, arguments=[current, proposed], english=text, complete_ink=size))
        cpu_outcomes = [options.respond(active, kind, flags, yes) for flags in (0, 1, 2, 3, 255) for yes in (False, True)]
        rows.append(dict(id=f"DK4_OPTIONS_{'REPORT' if kind == 'reports' else 'SAIL_HELP'}_PROMPT",
            file_path=stage.ARM, decision="retention", source_Japanese=ja.decode("cp932"),
            source_reference=dict(pointer_field=pointer, offset=old_ptr-options.BASE, hex=ja.hex()),
            current_reference=dict(pointer_field=pointer, offset=new_ptr-options.BASE, hex=en.hex()),
            installed_reference=dict(pointer_field=pointer, offset=new_ptr-options.BASE, hex=en.hex()),
            english=expected, source_meaning=meaning, localization_note=note,
            context="The Options toggle offers Yes to switch and No to return to the menu.",
            offline_preference_responses=cpu_outcomes, review=dict.fromkeys(stage.town.GATES, True)))
    return rows, cases


def main():
    assert not LIVE.exists()
    stored = base.load(stage.PROOF)
    clean, before, current = map(base.NdsImage.open, (stage.CLEAN, stage.parent.ROM, stage.ROM))
    source, old_arm, arm = [obj.read_file(stage.ARM) for obj in (clean, before, current)]
    assert stage.native.digest(arm) == stored["target_ARM9_sha256"]
    assert stage.reviewed_slot(source, old_arm)[0] == arm
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    older, newer = (run_data(root, sha) for root, sha in ((play.ROOT, stored["predecessor_sha256"]),
        (stage.ROOT / "playing", stored["candidate_sha256"])))
    assert older[0] == newer[0] and older[1].keys() == newer[1].keys()
    evidence = older[2] | newer[2]
    for run in (older, newer):
        evidence.update({shot["path"]: shot["PNG_sha256"] for shot in run[1].values()})
    a, b = [{n: old_checks.screen(shot) for n, shot in run[1].items()} for run in (older, newer)]
    font, old_font = [old_checks.GameAsciiFont.from_arm9(data) for data in (arm, old_arm)]
    assert all(font.decode(c).tobytes() == old_font.decode(c).tobytes() for c in "Reports")
    rows, toggle_holds = state_checks(source, arm, b, font)
    for index, key, meaning, reason in (
        (0, "SOUND", "Open the sound controls.", "Sound clearly names the menu with both music and effects controls."),
        (2, "SAIL_HELP", "Open the at-sea operation help setting.", "Sailing Help describes the feature and matches its confirmation."),
    ):
        ja, en, revised = [group[index] for group in stored["native_title_menu_selections"]]
        assert en == revised
        rows.append(dict(id=f"DK4_OPTIONS_{key}_MENU", file_path=stage.ARM, decision="retention",
            source_Japanese=bytes.fromhex(ja["text_hex"]).decode("cp932"),
            english=bytes.fromhex(en["text_hex"]).decode("ascii"),
            source_reference=ja, current_reference=en, installed_reference=revised,
            source_meaning=meaning, localization_note=reason, context="The original title Options menu.",
            review=dict.fromkeys(stage.town.GATES, True)))
    options_holds = []
    for frame in a:
        diff = ImageChops.difference(a[frame], b[frame]).getbbox()
        if frame not in MENU_FRAMES:
            assert diff is None, (frame, diff)
            continue
        assert diff and 92 < diff[0] < diff[2] < 164 and 278 <= diff[1] < diff[3] <= 298
        ink = [old_checks.font_mask(image[frame], font, text, 128-3*len(text), 283,
            (92, 278, 164, 298), (8, 8, 8)) for text, image in (("Report", a), ("Reports", b))]
        for text, y, rect in (("Sound", 263, (92, 258, 164, 278)), ("Sailing Help", 303, (92, 298, 164, 318))):
            old_checks.font_mask(b[frame], font, text, 128-3*len(text), y, rect, (8, 8, 8))
        options_holds.append(dict(frame=frame, complete_ink_pixels=ink, exact_changed_range=diff,
            held_frames=[older[1][frame], newer[1][frame]]))
    for start, reduced, end, box in ((3000, 3400, 5800, (24, 320, 103, 338)),
                                    (3000, 4200, 5000, (152, 320, 231, 338))):
        original, middle, restored = (b[n].crop(box).tobytes() for n in (start, reduced, end))
        assert original != middle and original == restored
    original_scope = base.load(HISTORICAL)
    japanese = stage.town.common_message_entries(clean.read_file(stage.COMMON), source)
    deployed = stage.parent.parent.stage.observed.prior.shared.paired.prior.entries(current)
    legacy = original_scope["checked_pending_legacy_keys"]
    for row in legacy:
        key = row["message_ID"]
        assert japanese[key].text.hex() == row["source_hex"] and deployed[key].text.hex() == row["current_hex"]
        row["current_reference"] = stage.town.reference(deployed[key])
    assert {row["message_ID"] for row in legacy} == play.prior.FOCUS
    # Both runs use ordinary inputs and no imported save. The retained prompts
    # use their original handlers; the report pointer follows the accepted relocation.
    images = [(f"Options {frame}", (a[frame], b[frame])) for frame in (6600, 7000, 8600, 9800, 11400)]
    renderer = stage.parent.live.render_sheet
    bound = FunctionType(renderer.__code__, vars(stage.parent.live) | dict(stage=stage))
    sheets = bound("options", images)
    evidence.update({str(HISTORICAL): base.digest(HISTORICAL), str(stage.PROOF): base.digest(stage.PROOF)})
    base.save(LIVE, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        ordinary_title_options=True, hardware=False, audio_output_assessed=False, options_holds=options_holds,
        toggle_holds=toggle_holds, prompt_retentions=rows, sound_meters_restored=True, title_return_frame=newer[1][12200],
        original_COMMON_calls=newer[0], legacy_options_keys=[row | {"observed_in_current_title_Options": False} for row in legacy],
        open_for_unverified_consumers=True, sheets=sheets, evidence=evidence))
    print(f"Verified {len(options_holds)} complete menu labels and six state prompts across the paired replays.")


if __name__ == "__main__":
    main()
