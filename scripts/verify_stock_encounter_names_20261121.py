"""Verify stock encounter names through the original victory and inspection paths."""

from hashlib import sha256
from pathlib import Path
from struct import pack

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R5, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.special_battle_target_names_v1 import CALL, TABLE, WRAPPER
from scripts import stage_battle_dialogue_followup_20261119 as battle
from scripts import stage_stock_encounter_names_20261121 as stage
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.record_navigation_v327 import dark_text
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.verify_captain_biographies_v1 import captured, shots
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_special_target_labels_20261115 import native_copy, verify_label
from scripts.verify_specialized_ship_labels_20261115 import get_catalogue


ROOT, base = stage.ROOT, stage.base
PROOF = ROOT / "stock_encounter_verification.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
INSPECTION_CAPTURE = ROOT / "ghost_settled/capture/capture_report.json"
FOLLOWUP_REVIEW = Path("releases/all_routes_editorial_20261119_battle_dialogue_followup_candidate/verification/registered_review.json")
SHEET = ROOT / "ghost_ship_inspection.png"


def read_ram(snapshot):
    raw = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and len(raw) == 0x400000
    assert sha256(raw).hexdigest() == snapshot["sha256"]
    return raw


def models(runtime, arm, staged, draft):
    old_cpu = get_machine(runtime.arm, runtime.raw)
    new_cpu = get_machine(arm, read_ram(staged["read_only_RAM_snapshot"]))
    old_classes, old_models, old_root = get_catalogue(old_cpu, runtime.arm)
    classes, records, root = get_catalogue(new_cpu, arm)
    assert old_root == root and old_classes == classes
    indexes = [r["model_ID"] for r in draft["records"]]
    assert [i for i, (a, b) in enumerate(zip(old_models, records, strict=True)) if a != b] == indexes
    cpu, get = new_cpu
    for row in draft["records"]:
        index = row["model_ID"]
        a, b = old_models[index], records[index]
        expected = bytes.fromhex(row["staged_reference"]["exact_hex"])
        assert bytes(cpu.mem_read(row["staged_reference"]["address"], len(expected))) == expected
        assert a[8:27] == bytes.fromhex(row["current_reference"]["exact_hex"]).ljust(19, b"\0")
        assert b[8:27] == expected.ljust(19, b"\0")
        assert a[:8] == b[:8] and a[27:] == b[27:]
        model = root + 4 + 140 * index
        assert get(0x1A4E0, model) == model + 8 and get(0x11DB0, model) == row["class_ID"]
    return dict(classes_checked=len(classes), models_checked=len(records), exclusively_changed_model_name_fields=indexes)


def victory_arguments(arm, inspection, rows):
    snap, = [r for r in inspection["read_only_pause_RAM_snapshots"] if r["frame"] == 5700]
    initial, = [r for r in inspection["read_only_pause_RAM_snapshots"] if r["frame"] == 4800]
    actual, unregistered = read_ram(snap), read_ram(initial)
    assert all(raw[0x71D74:0x71DC0] == arm[0x71D74:0x71DC0] for raw in (actual, unregistered))
    fixture, = inspection["synthetic_condition_fixtures"]
    results = {}
    for row in rows:
        index = row["model_ID"]
        observed = index == fixture["original_existing_model_ID"]
        cpu, get = get_machine(arm, actual if observed else unregistered)
        fleets = get(0xCB1A8)
        fleet = fleets + 4 + 39 * 132
        if not observed:
            # Run the same original initializer with another stock model in the offline copy.
            assert not get(0x36C70, fleet + 12)
            assert bytes(cpu.mem_read(fleet + 16, 1)) == b"\x95"
            cpu.mem_write(fleet + 16, bytes([index]))
            cpu.mem_write(fleet + 0x34, pack("<2i", *fixture["target_point"]))
            assert get(0x2D1CC, fleets, 1, 39, 1) == 1
        mobile = get(0x36C70, fleet + 12)
        assert mobile and bytes(cpu.mem_read(fleet + 16, 1)) == bytes([index])
        model = get(0x36C94, fleet + 12)
        assert model == get(0xCB148) + 4 + 140 * index
        assert get(0xAB128, mobile) == row["class_ID"]
        expected = row["english"].encode("ascii") + b"\0"
        held = []

        def observe(core, pc, _size, _data):
            pointer = core.reg_read(UC_ARM_REG_R2)
            assert pointer == model + 8
            assert bytes(core.mem_read(pointer, len(expected))) == expected
            if pc == WRAPPER:
                assert core.reg_read(UC_ARM_REG_R0) == 1 and core.reg_read(UC_ARM_REG_R1) == TABLE
                assert core.reg_read(UC_ARM_REG_LR) == CALL + 4
                core.emu_stop()
            held.append(dict(pc=pc, pointer=pointer, exact_hex=expected.hex()))

        for pc in (CALL, WRAPPER):
            cpu.hook_add(UC_HOOK_CODE, observe, begin=pc, end=pc)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_LR, STOP)
        cpu.reg_write(UC_ARM_REG_R5, 0)
        cpu.emu_start(stage.BASE + 0x71D74, STOP, count=20000)
        assert cpu.reg_read(UC_ARM_REG_PC) == WRAPPER and [r["pc"] for r in held] == [CALL, WRAPPER]
        results[index] = dict(model_ID=index, class_ID=row["class_ID"], arguments=held,
                              installed_name_hex=expected[:-1].hex(), actual_inspection_model=observed)
    return results, [snap, initial]


def render_victory_portraits(runtime, arm, arguments):
    ctx = battle.with_components(runtime, arm, runtime.common)
    workflow = battle.workflow
    directory = sha256(arm[workflow.DIRECTORY_OFFSET:workflow.TABLE_OFFSET]).hexdigest()
    common = workflow.owned_entries(runtime.common, arm, directory)
    previous = base.load(FOLLOWUP_REVIEW)
    group, = [g for g in base.load(battle.battle.OUTPUT)["native_context"] if g["argument_kind"] == "special"]
    caller, = group["native_callers"]
    group = group | {"consumer": caller["consumer"]}
    painter, _, _ = workflow.font_tools(runtime.image)
    kanji = runtime.image.read_file("/GRP/KANJI.FNT")
    select = battle.original.original_portraits()
    cases, pages = [], []
    for row in previous["records"]:
        n = row["message_ID"]
        if not 2187 <= n <= 2191:
            continue
        entry = common[n]
        assert entry.text.hex() == row["staged_hex"] and entry.text.count(b"%s") == 1
        actor = next(i for i, _, msg in group["original_voice_choices"] if msg == n)
        for earlier in row["native_displays"]:
            old_sample = earlier["sample"]
            model = old_sample["model_ID"]
            data = arguments[model]["installed_name_hex"]
            args = (bytes.fromhex(data),)
            assert args[0] == bytes.fromhex(old_sample["arguments"][0])
            sample = old_sample | {"current_hex": data}
            result = select(ctx, row, group, entry.text, actor, args, sample)
            display = result.pop("display")
            expected = row["english"].encode("ascii") % args
            assert b" ".join(display.split()) == expected
            lines = [line.strip() for line in display.decode("ascii").splitlines()]
            assert 0 < len(lines) <= 4 and all(0 < len(line) <= 36 for line in lines)
            assert any(args[0].decode("ascii") in line for line in lines)
            pixels, glyphs = battle.render_portrait(painter, arm, kanji, display)
            assert [g["code"] for g in glyphs] == workflow.glyph_codes(display)
            assert (glyphs[0]["code"], glyphs[-1]["code"]) == (expected[0], expected[-1])
            ink = sha256(pixels).hexdigest()
            assert display.hex() == earlier["display_hex"] and ink == earlier["ink_sha256"]
            pages.append((f"{n} / model {model}", pixels))
            cases.append(dict(message_ID=n, model_ID=model, registered_template_reference=workflow.reference(entry),
                              lines=lines, exact_ink_hash=ink, original_dispatch=result))
    assert len(cases) == len(pages) == 25
    return cases, battle.portrait_sheets(ROOT, pages)


def ghost_inspection(arm, report):
    fixture, = report["synthetic_condition_fixtures"]
    assert fixture["original_existing_model_ID"] == 153 and fixture["all_other4MiB_bytes_exact"]
    assert fixture["target_model_link_fixture"] and fixture["original_class_ID"] == 38
    data = native_copy(arm, report, "Ghost Ship", 38)
    frames = shots(report)
    font = GameAsciiFont.from_arm9(arm)
    before, status, after = [captured(frames[n]) for n in (5700, 6300, 6750)]
    masks = [verify_label(font, image, "Ghost Ship") for image in (before, after)]
    notice = dark_text(font, "You can't view that information!", status, (12, 291, 250, 327))
    sheet = Image.new("RGB", (1020, 217), "#263238")
    draw = ImageDraw.Draw(sheet)
    for i, (title, image) in enumerate((("Selected Ghost Ship", before), ("Inspection notice", status),
                                        ("Returned to Info Mode", after))):
        x = 4 + 340 * i
        draw.text((x, 5), title, fill="white")
        crop = image.crop((0, 254, 256, 378))
        sheet.paste(crop.resize((330, 160), Image.Resampling.NEAREST), (x, 24))
    sheet.save(SHEET)
    evidence = {frames[n]["path"]: frames[n]["PNG_sha256"] for n in (5700, 6300, 6750)}
    return dict(runtime_copy=data, complete_masks=masks, notice=notice, original_model_link_fixture=True,
                natural_spawn=False, natural_victory=False, returned_to_Info_Mode=True), evidence


def main():
    assert not PROOF.exists()
    draft = base.load(stage.PROOF)
    candidate = draft["candidate_sha256"]
    startup, inspection = map(base.load, (STARTUP_CAPTURE, INSPECTION_CAPTURE))
    for report in (startup, inspection):
        assert report["ROM_sha256"] == candidate and report["cold_boot"] and not report["savestate_loaded"]
        assert not report["callback_errors"]
        source = report["battery_save_preloaded"]
        assert source["copied_byte_exact_before_cold_boot"]
        assert base.digest(source["source"]) == source["source_sha256"]
    assert base.digest(stage.ROM) == candidate and startup["frames"] == 31000 and inspection["frames"] == 6750
    arm = base.NdsImage.open(stage.ROM).read_file(stage.ARM)
    previous = base.load(stage.parent.RELEASE)
    runtime = RegisteredRuntime(stage.parent.RELEASE, previous["own_registered_startup"], captain=3)
    assert runtime.arm[0x71D74:0x71DC0] == arm[0x71D74:0x71DC0]
    catalogue = models(runtime, arm, startup, draft)
    selection, snapshots = victory_arguments(arm, inspection, draft["records"])
    portraits, sheets = render_victory_portraits(runtime, arm, selection)
    gameplay, pictures = ghost_inspection(arm, inspection)
    evidence = {str(p): base.digest(p) for p in (STARTUP_CAPTURE, INSPECTION_CAPTURE, FOLLOWUP_REVIEW,
        Path(startup["read_only_RAM_snapshot"]["path"]), *(Path(r["path"]) for r in snapshots))}
    base.save(PROOF, dict(candidate_sha256=candidate, parent_sha256=previous["candidate_sha256"],
        catalogue=catalogue, original_victory_provider=selection, native_victory_portraits=portraits,
        actual_inspection=gameplay, hardware=False, evidence=evidence | pictures,
        sheets={p["path"]: p["sha256"] for p in sheets} | {str(SHEET): base.digest(SHEET)}))
    print("Verified five initialized model names, 25 native victory portraits and the live Ghost Ship inspection.")


if __name__ == "__main__":
    main()
