"""Separate village and graphics values from COMMON requests and bind Lil artwork."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack, unpack_from
from types import FunctionType

from PIL import Image
from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R6, UC_ARM_REG_R7

from dk4tool.graphics.fls import FlsArchive
from scripts import observe_online_gallery_common_v1 as replay
from scripts import observe_setup_save_common_v1 as trace
from scripts import reconcile_shared_display_20261121 as worklist
from scripts import register_map_cluster_suffix_20261121 as current
from scripts.probe_button_prompt_native import BASE, call, machine


base, native = current.base, current.native
ROOT = Path("work/shared_numeric_and_lil_artwork_20261121")
OUTPUT = worklist.OUTPUT.with_name("shared_numeric_and_lil_artwork_20261121_v1.json")
TITLE = Path("work/analysis/opening_composition_v646/full_composition_results.json")
OLD_VILLAGE = Path("work/analysis/village_location_v606/original_village_records.json")
OPENING = worklist.OUTPUT.with_name("opening_scene_labels_20261115_v1.json")
MOVIE = "/FLS/M28.fls"
IMG = (2367, 2400, 2440, 2480, 2520, 2560, 2600, 2640, 2683)
VILLAGE_INIT, VILLAGE_TABLE, VILLAGE_MODEL = 0xCAE00, 0x15AFB0, 0xCACAC
PARAMETER_WRITE = (0x66C20, 0x66F48, 0xF39C4)
BUS = 0x04000470
PRIORITY = (284, 304, 3456)
RUNNING_FRAME, RUNNING_TEXTURE = 2480, 48


def title_replay():
    assert not ROOT.exists()
    get_schedule = lambda case: ([], list(IMG), 2701, TITLE, None)
    run = FunctionType(replay.main.__code__, vars(replay) | dict(ROOT=ROOT, parent=current,
        observer=trace.scoped_observer, get_schedule=get_schedule, FOCUS=set(PRIORITY), __file__=__file__))
    run("title")


def village_parameter(arm, prior_records):
    u = machine(arm)
    assert unpack_from("<I", arm, 0xCAE9C) == (BASE + VILLAGE_TABLE,)
    call(u, VILLAGE_INIT, ())
    output = []
    for index in (0, 14):
        row = VILLAGE_TABLE + 44 * index
        source = row + 20
        assert unpack_from("<I", arm, source) == (284,)
        call(u, VILLAGE_MODEL, (0, index))
        address = u.reg_read(UC_ARM_REG_R0)
        value, = unpack_from("<I", bytes(u.mem_read(address + 0x1C, 4)))
        assert value == 284 << 4
        previous = prior_records[index]
        assert address == previous["object"]
        assert value == unpack_from("<I", bytes.fromhex(previous["record_hex"]), 0x1C)[0]
        output.append(dict(village_ID=index, clean_name=previous["source_name"], descriptor_address=BASE+row,
            descriptor_field=BASE+source, value=284, model_address=address, initialized_field=address+0x1C,
            initialized_value=value, native_read=BASE+0xCAE44, native_store=BASE+0xCAE4C))
    return output


def graphics_parameters(arm):
    u = machine(arm)
    u.mem_map(0x04000000, 0x1000)
    output, writes = [], []
    hook = u.hook_add(UC_HOOK_MEM_WRITE,
        lambda _, _access, at, size, value, _data: writes.append((at, size, value)), begin=BUS, end=BUS+3)
    try:
        for at in PARAMETER_WRITE:
            writes.clear()
            u.reg_write(UC_ARM_REG_R7, 1)
            u.reg_write(UC_ARM_REG_R6, 1)
            u.emu_start(BASE+at, BASE+at+28, count=12)
            assert len(writes) == 3 and all(a == BUS and size == 4 for a, size, _ in writes)
            assert [value for _, _, value in writes][1:] == [304, 0xFFFFFFFA]
            output.append(dict(instruction_start=BASE+at, immediate_instruction=BASE+at+12,
                I_O_write_address=BUS, writes=tuple(writes)))
    finally:
        u.hook_del(hook)
    return output


def bound_references(clean, active):
    workflow = worklist.workflow
    common, arm = clean.read_file(worklist.COMMON), clean.read_file(native.ARM)
    source = workflow.common_message_entries(common, arm)
    installed = worklist.entries(active)
    pending = {row["message_ID"]: row for row in base.load(worklist.OUTPUT)["records"]}
    references = []
    for key in PRIORITY:
        row = pending[key]
        assert workflow.reference(source[key]) == row["source_reference"]
        assert workflow.reference(installed[key]) == row["current_reference"]
        assert source[key].text.hex() == row["source_hex"] and installed[key].text.hex() == row["current_hex"]
        references.append({k: row[k] for k in ("message_ID", "source_reference", "current_reference", "source_hex", "current_hex", "draft")})
    return references


def running_artwork(clean, active, candidate):
    folder = ROOT / "title"
    terminal, report, traced = map(base.load, (folder / "terminal.json",
        folder / "capture/capture_report.json", folder / "requests.json"))
    assert terminal["ROM_sha256"] == report["ROM_sha256"] == candidate
    assert report["frames"] == terminal["completed_frames"] == 2701
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["scripted_input_schedule"]
    assert not report.get("battery_save_preloaded") and not report["callback_errors"]
    assert traced["all_host_slots_restored_and_core_file_exact"] and not traced["errors"] and not traced["mismatches"]
    assert traced["callbacks"] == terminal["COMMON_requests"] == len(traced["source_requests"]) == 0
    assert all(base.digest(p) == digest for p, digest in terminal["evidence"].items()
               if Path(p).resolve() != Path(__file__).resolve())
    before, after = (FlsArchive(rom.read_file(MOVIE)) for rom in (clean, active))
    source, current_texture = (archive.texture(RUNNING_TEXTURE) for archive in (before, after))
    assert source == current_texture and (source.width, source.height) == (256, 256)
    frame, = [item for item in report["frames_captured"] if item["frame"] == RUNNING_FRAME]
    assert base.digest(frame["path"]) == frame["PNG_sha256"]
    clean_upper = source.render().convert("RGB").crop((0, 0, 256, 192))
    with Image.open(frame["path"]) as display:
        actual_upper = display.convert("RGB").crop((0, 0, 256, 192))
    to_native = bytes(value >> 3 for value in range(256))
    projected = clean_upper.tobytes().translate(to_native)
    assert len(projected) == 3 * 49152 and projected == actual_upper.tobytes().translate(to_native)
    old_title = base.load(OPENING)["ordinary_emulator_runs"]["title"]
    earlier, = [item["current"] for item in old_title["held_frames"] if item["frame"] == 2683 and item["match"]]
    named_frame, = [item for item in report["frames_captured"] if item["frame"] == 2683]
    assert all(base.digest(r["path"]) == r["PNG_sha256"] for r in (earlier, named_frame))
    with Image.open(earlier["path"]) as first, Image.open(named_frame["path"]) as second:
        assert first.convert("RGB").crop((0, 0, 256, 192)).tobytes() == second.convert("RGB").crop((0, 0, 256, 192)).tobytes()
    return dict(path=MOVIE, texture_index=RUNNING_TEXTURE,
        clean_asset_sha256=native.digest(clean.read_file(MOVIE)), installed_asset_sha256=native.digest(active.read_file(MOVIE)),
        exact_top_screen_pixels_at_native_precision=49152, held_frame=frame,
        complete_animated_names=dict(frame=named_frame, matches_earlier_upper_display=True, names=["Lil Argot", "Camille Overijssel"]),
        actual_emulator_title_without_input=True, trace_terminal=str(folder / "terminal.json"),
        source_Japanese="走るリルとカミル", english_draft="Lil and Camille Running",
        editorial_decision="Keep the action and both approved names. The painting shows Lil and Camille running together.",
        stored_COMMON_display_owner="open", original_COMMON_requests=0)


def checkpoint():
    assert not OUTPUT.exists()
    release, ledger = map(base.load, (current.RELEASE, base.LEDGER))
    assert release["candidate_sha256"] == ledger["current_integrated_candidate"]["sha256"] == base.digest(current.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    assert release["clean_input_sha256"] == base.digest(native.CLEAN)
    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    source, installed = (rom.read_file(native.ARM) for rom in (clean, active))
    assert native.digest(installed) == release["target_ARM9_sha256"]
    prior_records = base.load(OLD_VILLAGE)["records"]
    villages = village_parameter(source, prior_records)
    assert villages == village_parameter(installed, prior_records)
    graphics = graphics_parameters(source)
    assert graphics == graphics_parameters(installed)
    references = bound_references(clean, active)
    art = running_artwork(clean, active, release["candidate_sha256"])
    artwork_entry, = [row for row in references if row["message_ID"] == 3456]
    assert bytes.fromhex(artwork_entry["source_hex"]).decode("cp932") == art["source_Japanese"]
    assert artwork_entry["draft"]["english"] == art["english_draft"]
    original_worklist = base.load(worklist.OUTPUT)
    priority = original_worklist["first_investigation_list"]
    assert 3456 in priority and len(priority) == 35
    assert len(original_worklist["records"]) == 276 == ledger["pending_shared_consumer_checkpoint_20261114"]["remaining_total"]
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        prior_worklist=str(worklist.OUTPUT), prior_worklist_sha256=base.digest(worklist.OUTPUT), exact_references=references,
        offline_village_parameter_matches=villages, offline_graphics_write_matches=graphics,
        title_artwork_association={"3456": art}, other_unassociated_priority_entries=[n for n in priority if n != 3456],
        remaining_graphics_or_data_word_matches_unclassified={"284":[0x0216C7BC, 0x0216CD70],"304":[0x0216C3A4, 0x0216C924]},
        proof_scope="Original village initialization and isolated I/O writer fragments. The title trace covers cold boot and the sampled title scene.",
        new_emulator_observations=1, additional_editorial_credit=0, open_stored_COMMON_display_references=276, full_goal_complete=False))
    print("Verified two village parameters, three graphics-register writes, and the exact Lil and Camille title artwork.")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--replay", action="store_true")
    if parser.parse_args().replay:
        title_replay()
    else:
        checkpoint()


if __name__ == "__main__":
    main()
