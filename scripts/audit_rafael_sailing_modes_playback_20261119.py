"""Bind both emulator choice paths and all revised display pages."""

from pathlib import Path

from PIL import Image, ImageDraw

from scripts import replay_rafael_sailing_modes_20261119 as play
from scripts import verify_rafael_sailing_modes_20261119 as offline

base = play.base
PROOF = play.ROOT / "verified_choices.json"
FLOW = Path("work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json")
NAMES = Path("work/analysis/Rafael_B46_source_name_planes_v7946/24_complete_source_pages3_names12_literal_alignments12_FE.json")
DARK = (0, 8, 0)
STEEL = (98, 97, 98)


def captures(report):
    pictures = {}
    for row in report["frames_captured"]:
        path = row["path"]
        assert base.digest(path) == row["PNG_sha256"]
        with Image.open(path) as image:
            pictures[row["frame"]] = (row, image.convert("RGB"))
    return pictures


def matching_frame(page, speaker, before, after, pictures, names):
    fe = speaker == 254
    native = bytes.fromhex(page["native_plane_hex"])
    assert len(native) == 216 * 64 and set(native) == {0, 15 if fe else 1}
    wanted = b"".join(bytes(bool(v) for v in native[y:y+216]) + bytes(12) for y in range(0, len(native), 216))
    name = None if fe else names[speaker]
    if name:
        path = Path(name["native_plane"])
        assert base.digest(path) == name["native_plane_sha256"]
        raw = path.read_bytes()
        expected_name = {(i % 216, i // 216) for i, v in enumerate(raw) if v}
    for n, (frame, image) in pictures.items():
        if not before + 25 < n < after - 4:
            continue
        body = bytes(color == DARK for color in image.crop((16, 296, 244, 360)).get_flattened_data())
        if body != wanted:
            continue
        if fe:
            assert not any(image.getpixel((x, y)) == STEEL for y in range(276, 289) for x in range(14, 244))
        else:
            shown = {(x-16, y-276) for y in range(276, 289)
                     for x in range(14, 18 + name["original_pair_flush_width"])
                     if image.getpixel((x, y)) == STEEL}
            assert shown == expected_name
        return frame
    raise AssertionError((speaker, before, after, sorted(n for n in pictures if before < n < after)))


def path_result(choice, fixture, expected, revised, names):
    folder = play.ROOT / f"route0_English_{choice}"
    terminal_path = folder / "terminal.json"
    terminal = base.load(terminal_path)
    assert terminal["terminal"] and terminal["choice"] == choice and terminal["all_callbacks_readonly_andhost_slots_restored"]
    evidence = {str(terminal_path): base.digest(terminal_path)}
    for label in ("report", "observer", "menu_observer", "run_plan"):
        file = terminal[label]
        assert base.digest(file) == terminal[label + "_sha256"]
        evidence[file] = terminal[label + "_sha256"]
    report, trace, menu, plan = (base.load(terminal[key]) for key in ("report", "observer", "menu_observer", "run_plan"))
    assert report["ROM_sha256"] == fixture["research_ROM_sha256"] and report["cold_boot"]
    assert not report["savestate_loaded"] and not report.get("battery_save_preloaded") and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(plan["inputs"])
    for observer in (trace, menu):
        assert not observer["errors"] and not observer["mismatches"] and observer["all_host_slots_restored_and_core_file_exact"]
    assert {row["text"] for row in menu["rows"]} == {"Please do.", "No, thanks."}
    assert all(r["CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback"]
               and r["bitmap_header_words"][:3] == [4, 64, 36] and r["backing_bytes"] == 4608
               and base.digest(r["backing"]) == r["backing_sha256"] for r in menu["rows"])
    resident = {r["offset"]: r for r in fixture["all_fixture_commands"]}
    original = {r["offset"]: r for r in fixture["command_ids"]}
    words = {r["fixture_command_offset"]: r for r in fixture["original_text_records"]}
    pictures = captures(report)
    holds, speech_ids, commands, frames = [], [], [], []
    menu_hold = None
    exit_frame = None
    for returned in trace["rows"]:
        if returned["kind"] != "after_command":
            continue
        source = returned["source"]
        if (source.get("classification"), source.get("route"), source.get("block")) != ("original_SC_cache", 0, 44):
            continue
        entered = trace["rows"][returned["entry_row"]]
        assert source["whole_resident_payload_exact_ROM"] and source["actual_sha256"] == source["registered_sha256"]
        assert returned["CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback"]
        offset, word = source["instruction_offset"], source["first_word"]
        assert word == resident[offset]["word"] == entered["source"]["first_word"]
        if offset in original:
            commands.append(original[offset]["source_offset"])
        if word == 0x2100:
            assert returned["result_words"] == [2, expected["menu_selection"]]
            menu_frames = [n for n in pictures if entered["frame"]+70 < n < returned["frame"]-12]
            assert menu_frames
            menu_hold = pictures[max(menu_frames)][0]
            frames.append((f"{choice}: retained choices", pictures[menu_hold["frame"]][1]))
        if offset in words:
            row = words[offset]
            ident = row["id"]
            speech_ids.append(ident)
            if ident in revised:
                frame = matching_frame(revised[ident], row["source_selector"], entered["frame"], returned["frame"], pictures, names)
                holds.append(dict(id=ident, frame=frame["frame"], capture=frame["path"],
                                  capture_sha256=frame["PNG_sha256"], complete_mask=True,
                                  speaker=row["source_selector"]))
                frames.append((f"{choice}: {ident}", pictures[frame["frame"]][1]))
        if word == 0:
            assert returned["result_words"] == [0, expected["menu_selection"]]
            exit_frame = returned["frame"]
            break
    assert exit_frame is not None and menu_hold is not None
    assert speech_ids == expected["source_speech_IDs"]
    assert commands == expected["visited_source_command_offsets"]
    later = min(n for n in pictures if n > exit_frame + 50)
    frames.append((f"{choice}: after the original return", pictures[later][1]))
    sheets = []
    for start in range(0, len(frames), 6):
        batch = frames[start:start+6]
        sheet = Image.new("RGB", (1040, ((len(batch)+1)//2)*404), "#263238")
        draw = ImageDraw.Draw(sheet)
        for i, (label, image) in enumerate(batch):
            x, y = (i % 2)*520, (i//2)*404
            draw.text((x+4, y+2), label, fill="white")
            sheet.paste(image.crop((0, 192, 256, 384)).resize((512, 384), Image.Resampling.NEAREST), (x+4, y+16))
        file = folder / f"{choice}_playback_{1+start//6}.png"
        sheet.save(file)
        sheets.append(dict(path=str(file), sha256=base.digest(file)))
    return dict(choice=choice, result=[0, expected["menu_selection"]], menu_selected=expected["menu_selection"],
                menu_capture=menu_hold, exit_frame=exit_frame, speeches=speech_ids, source_commands=commands,
                checked_revisions=holds, sheets=sheets, evidence=evidence)


def main():
    assert not PROOF.exists()
    setup, native, flow, name_proof = map(base.load, (play.FIXTURES, offline.PROOF, FLOW, NAMES))
    fixture, = setup["fixtures"]
    assert base.digest(play.FIXTURE) == fixture["research_ROM_sha256"]
    assert base.digest(play.stage.ROM) == setup["candidate_sha256"] == native["candidate_sha256"]
    revisions = {r["id"]: r["pages"][0] for r in native["revisions"]}
    names = {row["actor_ID"]: row for row in name_proof["name_planes"]}
    paths = [path_result(choice, fixture, expected, revisions, names)
             for choice, expected in zip(("accept", "decline"), flow["source_paths"], strict=True)]
    assert [len(p["speeches"]) for p in paths] == [22, 7]
    assert {r["id"] for p in paths for r in p["checked_revisions"]} == revisions.keys()
    assert len({at for p in paths for at in p["source_commands"]}) == 37
    evidence = {str(p): base.digest(p) for p in (play.FIXTURES, offline.PROOF, FLOW, NAMES)}
    for path in paths:
        evidence.update(path["evidence"])
    base.save(PROOF, dict(candidate_sha256=setup["candidate_sha256"], paths=paths, revised_pages_verified=12,
                          natural_activation=False, hardware=False, evidence=evidence))
    print("Both emulator choices returned through the original controls. All 12 revised panels matched.")


if __name__ == "__main__":
    main()
