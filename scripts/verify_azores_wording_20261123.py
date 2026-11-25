"""Verify Azores wording in ordinary controller replays and native name cases."""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import arm_const as registers

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import headless_desmume_v193 as harness
from scripts import stage_azores_wording_20261123 as stage
from scripts.observe_lisbon_azores_voyage_20261123 import DONOR
from scripts.probe_button_prompt_native import STACK
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_lisbon_azores_voyage_20261123 import (
    REPORT, body_mask, load_exact, text_at, town,
)
from scripts.verify_personal_gameplay_v841 import get_machine


PREVIOUS = Path(".codex-release-work/shared_display_20261123")
REPLAYS = {
    "decline": ("lisbon_azores", (3200, 8300, 8420, 8550, 8750, 9100, 9620, 9840, 10700, 10980, 11500)),
    "accept": ("azores_words_adaptive_store/live_qualified", (8420, 8550, 9620, 9840, 12320, 12600, 12880, 13160)),
}
REVISED_PAGES = {
    8420: (297, ("Discovered the Azores.",)),
    8550: (70, ("Shall we stop at the Azores?",)),
    9620: (stage.RANK_ID, ("Admiral, the village chief asks to", "hear the promised words.")),
}
OUTPUT = stage.ROOT / "staged/native_and_ordinary_proof.json"
R = tuple(getattr(registers, f"UC_ARM_REG_R{i}") for i in range(13))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def old_replay(case):
    return PREVIOUS / REPLAYS[case][0] / "capture/capture_report.json"


def new_replay(case):
    return stage.ROOT / "ordinary" / case / "capture/capture_report.json"


def replay(case):
    old = stage.read(old_replay(case))
    assert old["battery_save_preloaded"]["source_sha256"] == stage.digest(DONOR)
    out = new_replay(case).parents[1]
    out.mkdir(parents=True)
    inputs = out / "inputs.json"
    write_json(inputs, old["scripted_input_schedule"])
    sys.argv = [__file__, "--rom", str(stage.ROM), "--out", str(out / "capture"),
        "--frames", str(old["frames"]), "--inputs-json", str(inputs), "--press-start", "-1",
        "--capture-every", "999999", "--capture-at", *map(str, REPLAYS[case][1]),
        "--battery-save", str(DONOR), "--touchscreen"]
    harness.main()


def native_call(cpu, site, obj, getter, flags):
    values = (obj, getter, *(0xA5A50000 + i for i in range(2, 13)))
    cpu.reg_write(registers.UC_ARM_REG_CPSR, flags)
    cpu.reg_write(registers.UC_ARM_REG_SP, STACK)
    for reg, value in zip(R, values, strict=True):
        cpu.reg_write(reg, value)
    cpu.emu_start(site, site + 4, count=80)
    assert cpu.reg_read(registers.UC_ARM_REG_PC) == site + 4
    assert cpu.reg_read(registers.UC_ARM_REG_LR) == site + 4
    assert cpu.reg_read(registers.UC_ARM_REG_SP) == STACK
    return ([cpu.reg_read(reg) for reg in R], cpu.reg_read(registers.UC_ARM_REG_CPSR))


def name_matrix(image, proof, review):
    release, observed = stage.read(stage.RELEASE), stage.read(REPORT)
    current = stage.NdsImage.open(release["candidate"]).read_file(stage.ARM)
    arm, common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    hold = next(row for row in observed["records"] if row["key"] == 70)
    raw = load_exact(hold["snapshot"])
    old, get = get_machine(current, raw)
    cpu, _ = get_machine(arm, raw)
    runtime = proof["runtime"]
    sites = runtime["native_call_sites"]
    for site in sites:
        cpu.mem_write(site, arm[site - stage.BASE:site - stage.BASE + 4])
    cpu.mem_write(runtime["runtime_entry"], bytes.fromhex(runtime["helper_hex"]))
    root = get(0xCB118)
    rows, pages = [], []
    templates = stage.common_rows(common, arm)
    raster = town.font_tools(image)[0]
    kanji = image.read_file("/GRP/KANJI.FNT")
    for name in review["village_names"]:
        obj = get(0xCACAC, root, name["index"])
        getter, bare = name["native_getter"], name["name_address"]
        argument = "the Azores" if bare == stage.AZORES_VILLAGE else name["English"]
        selected = runtime["alias_address"] if bare == stage.AZORES_VILLAGE else bare
        for flags in range(16):
            cpsr = 0x1F | flags << 28
            for site in sites:
                previous_regs, previous_cpsr = native_call(old, site, obj, getter, cpsr)
                new_regs, new_cpsr = native_call(cpu, site, obj, getter, cpsr)
                assert previous_regs[0] == bare and new_regs[0] == selected
                assert previous_regs[1:] == new_regs[1:] and previous_cpsr == new_cpsr
        assert bytes(cpu.mem_read(selected, len(argument) + 1)) == argument.encode("ascii") + b"\0"
        for key, (english, _) in stage.DOCK.items():
            body, lines = town.native_layout(cpu, templates[key].text, key, (argument,))
            assert " ".join(lines) == english % argument and len(lines) == 1
            plane, codes = town.render_portrait(raster, arm, kanji, body)
            assert [item["code"] for item in codes] == town.glyph_codes(body)
            if argument == "the Azores" or (key in (69, 70) and len(argument) >= 12):
                pages.append((f"{key} {argument}", plane))
            rows.append(dict(message_ID=key, village=name["English"], formatted_argument=argument,
                             lines=lines, native_glyph_plane_sha256=stage.digest_bytes(bytes(plane))))
    return rows, town.portrait_sheets(OUTPUT.parent, pages)


def replay_proof(font, case):
    old, new = map(stage.read, (old_replay(case), new_replay(case)))
    assert new["cold_boot"] and not new["savestate_loaded"] and not new["callback_errors"]
    assert not any(v for k, v in new.items() if k.startswith("synthetic_"))
    assert new["frames"] == old["frames"]
    assert new["scripted_input_schedule"] == old["scripted_input_schedule"]
    assert new["battery_save_preloaded"]["source_sha256"] == old["battery_save_preloaded"]["source_sha256"]
    assert new["ROM_sha256"] == stage.digest(stage.ROM)
    before = {row["frame"]: row for row in old["frames_captured"]}
    after = {row["frame"]: row for row in new["frames_captured"]}
    displays, retained, pages = [], [], []
    for frame in REPLAYS[case][1]:
        shot = after[frame]
        assert stage.digest(shot["path"]) == shot["PNG_sha256"]
        if frame in REVISED_PAGES:
            key, lines = REVISED_PAGES[frame]
            with Image.open(shot["path"]) as capture:
                panel = capture.convert("RGB")
            proof = body_mask(font, panel, lines)
            if key != 297:
                complete_mask(font, "Manuel Almeida", panel, 16, 277, (98, 97, 98))
            displays.append(dict(frame=frame, key=key, lines=lines, glyphs=proof, screenshot=shot))
            pages.append((frame, panel.crop((0, 256, 256, 384))))
        elif frame in before:
            assert shot["framebuffer_sha256"] == before[frame]["framebuffer_sha256"]
            retained.append(frame)
    assert len(displays) == 3 and len(retained) >= 4
    sheet = Image.new("RGB", (1032, 560), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (frame, panel) in enumerate(pages):
        x, y = i % 2 * 516, i // 2 * 280
        draw.text((x + 5, y + 4), f"{case}, frame {frame}", fill="white")
        sheet.paste(panel.resize((512, 256), Image.Resampling.NEAREST), (x + 4, y + 20))
    path = OUTPUT.parent / f"ordinary_{case}.png"
    sheet.save(path)
    return dict(capture=stage.reference(new_replay(case)), complete_revised_pages=displays,
                matching_transition_frames=retained, sheet=stage.reference(path))


def verify():
    assert not OUTPUT.exists()
    proof, review = map(stage.read, (stage.PROOF, stage.OUTPUT))
    assert stage.digest(stage.ROM) == proof["candidate_sha256"]
    image = stage.NdsImage.open(stage.ROM)
    arm, common = image.read_file(stage.ARM), image.read_file(stage.COMMON)
    assert stage.digest_bytes(arm) == proof["target_ARM9_sha256"]
    assert stage.digest_bytes(common) == proof["target_COMMON_sha256"]
    font = GameAsciiFont.from_arm9(arm)
    names, sheets = name_matrix(image, proof, review)
    observed = {case: replay_proof(font, case) for case in REPLAYS}
    templates = stage.common_rows(common, arm)
    for row in review["records"]:
        row["review"]["formatting"] = True
        if row["id"] in stage.COMMON_IDS:
            entry = templates[stage.COMMON_IDS[row["id"]]]
            row["message_ID"] = entry.message_id
            row["staged_reference"] = town.reference(entry)
            row["staged_hex"] = entry.text.hex()
        else:
            assert row["id"] == stage.RANK_ID
            ptr = stage.POOL + proof["runtime"]["rank_pool_offset"]
            row["staged_reference"] = dict(ARM9_file_offset=row["installed_reference"]["ARM9_file_offset"],
                                            text_address=ptr, pool_offset=proof["runtime"]["rank_pool_offset"])
            row["staged_hex"] = proof["runtime"]["rank_body_hex"]
    review["encoder"] = "dialogue-relocatable-v1"
    validate_natural_dialogue_batch(review)
    write_json(OUTPUT, dict(candidate_sha256=proof["candidate_sha256"], prior_source_review=stage.reference(stage.OUTPUT),
        staged_source_reviewed_records=review["records"], native_name_layouts=names,
        native_getter_and_call_site_flag_cases=24 * 2 * 16, native_context_sheets=sheets, ordinary_replays=observed,
        verified_replay_scope="Emulator controller input from cartridge save. Observed docking voice 70.",
        offline_scope="All 24 native village names and both original getter call sites. All six docking templates and discovery.",
        registered_installation_pending=True, new_editorial_credit=0))
    print(f"{len(names)} native layouts, six complete revised gameplay holds, and both Promised Words outcomes.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=(*REPLAYS, "verify"))
    mode = parser.parse_args().mode
    if mode == "verify":
        verify()
    else:
        replay(mode)
