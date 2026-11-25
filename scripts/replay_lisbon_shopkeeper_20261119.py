"""Observe the Lisbon Square shopkeeper on the exact registered Deck candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path

from PIL import Image

from scripts import checkpoint_joined_actor_names_20261119 as review
from scripts import observe_lisbon_voyage_and_osaka_20261115 as lisbon
from scripts import observe_online_gallery_common_v1 as playback
from scripts.checkpoint_amsterdam_square_current_20261114 import body_mask
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_personal_gameplay_v841 import get_machine

base = review.base
FOLDER = review.ROOT / "lisbon"
PROOF = review.ROOT / "lisbon_shopkeeper_gameplay.json"


def schedule(case):
    events, frames, _, source, donor = lisbon.schedule(case)
    return [r for r in events if r["start"] <= 9401], [n for n in frames if n <= 9550], 9601, source, donor


def capture():
    assert not FOLDER.exists()
    wrapper = checked_text(getsource(playback.main), {
        "    installed = []": '    argv.append("--dump-capture-ram")\n    installed = []',
    })
    scope = vars(playback) | dict(ROOT=review.ROOT, parent=review.current, observer=scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(wrapper, __file__ + "::ordinary-lisbon", "exec"), scope)
    scope["main"]("lisbon")


def verify():
    assert not PROOF.exists()
    observed = base.load(review.OUTPUT)
    release = base.load(review.current.RELEASE)
    files = [FOLDER / path for path in ("capture/capture_report.json", "requests.json", "terminal.json", "inputs.json")]
    report, trace, terminal, inputs = map(base.load, files)
    events, frames, end, source, donor = schedule("lisbon")
    assert report["ROM_sha256"] == terminal["ROM_sha256"] == observed["candidate_sha256"] == release["candidate_sha256"]
    assert report["frames"] == terminal["completed_frames"] == end
    assert report["scripted_input_schedule"] == events == inputs
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert base.digest(donor["source"]) == report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    arm = base.NdsImage.open(review.current.ROM).read_file(review.current.stage.ARM)
    font = review.GameAsciiFont.from_arm9(arm)
    shots = {row["frame"]: row for row in report["frames_captured"]}
    snapshots = {row["frame"]: row for row in report["read_only_capture_RAM_snapshots"]}
    requests = [r for r in trace["source_requests"] if r["PC"] == 0x0205528C]
    pending = {r["message_ID"] for r in base.load(review.current.stage.PENDING)["records"]}
    assert not pending.intersection(r["message_ID"] for r in trace["source_requests"])
    expected_holds = {5150: 656, 5950: 657, 6750: 685, 7550: 656, 8350: 657}
    assert [r["message_ID"] for r in requests] == list(expected_holds.values())
    prior = {r["message_ID"]: r for r in base.load(review.square.REVIEW)["records"]}
    common = base.NdsImage.open(review.current.ROM).read_file(review.current.stage.COMMON)
    workflow = review.current.stage.workflow
    directory = review.native.digest(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET])
    entries = workflow.owned_entries(common, arm, directory)
    cases, evidence = [], {str(p): base.digest(p) for p in (*files, source, review.OUTPUT, review.square.REVIEW)}
    for frame, expected in expected_holds.items():
        assert frame in frames
        request = max((r for r in requests if r["frame"] < frame), key=lambda r: r["frame"])
        assert 0 < frame - request["frame"] <= 150 and request["message_ID"] == expected
        shot, ram = shots[frame], snapshots[frame]
        assert base.digest(shot["path"]) == shot["PNG_sha256"]
        assert base.digest(ram["path"]) == ram["sha256"] and ram["read_only_export"]
        cpu, get = get_machine(arm, Path(ram["path"]).read_bytes())
        assert get(0xB65E4) == 11
        town = get(0xB6618)
        actor = get(0xB2D28, town, 0)
        obj = get(0xB2CD8, town, 0)
        assert actor == 83 and obj == get(0xCB184) + 4 + 32*actor
        assert review.labels.read_text(cpu, get(review.GETTERS["dialogue"], obj)) == "Shopkeeper"
        assert review.labels.read_text(cpu, get(review.GETTERS["joined_full"], obj)) == "Shopkeeper ヨーロッパ女"
        with Image.open(shot["path"]) as opened:
            img = opened.convert("RGB")
        ink, bounds = complete_mask(font, "Shopkeeper", img, 16, 277, (98, 97, 98))
        assert ink == 135
        assert all(prior[expected]["registered_reference"][key] == value
                   for key, value in workflow.reference(entries[expected]).items())
        assert entries[expected].text.hex() == prior[expected]["staged_hex"]
        body = body_mask(img, font, prior[expected]["visible_lines"])
        cases.append(dict(frame=frame, town_ID=11, stock_square_actor=actor, requested_message=expected,
            observed_ordinary_short_nameplate="Shopkeeper", complete_glyph_pixels=ink, bounds=bounds, body=body, capture=shot["path"],
            source_reference=prior[expected]["source_reference"], current_reference=workflow.reference(entries[expected]),
            source_Japanese=prior[expected]["clean_Japanese"], retention_reason=prior[expected]["localization_note"]))
        evidence.update({shot["path"]: shot["PNG_sha256"], ram["path"]: ram["sha256"]})
    base.save(PROOF, dict(candidate_sha256=report["ROM_sha256"], observations=cases,
        ordinary_inputs=True, used_existing_battery_save=True, savestate=False, hardware=False, evidence=evidence,
        pending_shared_keys_requested=0))
    print("Lisbon's original Square selector identifies actor 83. All five observed replies use the complete plain Shopkeeper nameplate.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("capture", "verify"), nargs="?", default="capture")
    globals()[parser.parse_args().action]()
