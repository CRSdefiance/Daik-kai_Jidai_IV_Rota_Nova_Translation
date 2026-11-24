"""Stage and verify the Riga Cargo Setup warning against the native modal."""

import sys
from argparse import ArgumentParser
from struct import unpack_from
from types import FunctionType, SimpleNamespace

from PIL import Image, ImageChops, ImageDraw
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_SP

from scripts import observe_riga_shipyard_20261124 as baseline
from scripts import plan_literal_static_layout_v1 as modal
from scripts import preflight_riga_palace_wording_20261124 as tools
from scripts import register_palace_investment_wording_20261124 as parent
from scripts import stage_tunis_shop_advice_20261124 as release_checks
from scripts import verify_palace_investment_replay_20261124 as playback
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.stage_cartridge_title_20261123 import CLEAN, GATES, REGISTRY, NdsImage, digest, read, reference, sha256, write

ARM, COMMON = parent.ARM, parent.COMMON
ROOT = parent.ROM.parent.with_name("editorial_20261124_riga_cargo_storage")
ROM = ROOT / "Cargo_Storage_Warning_STAGED.nds"
OUT, PAIRED = ROOT / "cargo_storage_warning_native.json", ROOT / "paired_gameplay.json"
PATCH, REBUILT, PATCH_PROOF = (ROOT / name for name in ("translation.xdelta", "clean_rebuilt.nds", "clean_patch_proof.json"))
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
played = SimpleNamespace(RELEASE=parent.RELEASE)
KEY = 268
DRAFT = "There's cargo in storage. Finish?"
HOLDS = (13600, 14400)
WRAPPER, FORMAT_END = 0x0205466C, 0x0205479C
HISTORICAL = "translations/editorial_checkpoints/SharedText_20261110_v1/shipyard_fleet_setup_context_v1.json"
CAPTURE = baseline.ROOT / "capture/capture_report.json"
panels = tools.observed.panels
KEEP = {
    657: ((5200,), "Shopkeeper", ("You're a sailor, aren't you?", "Try the Market for bulk trade."),
          "The question keeps the shopkeeper's casual recognition. The next sentence directs bulk traders to the Market."),
    656: ((6400,), "Shopkeeper", ("We only sell retail.",),
          "The brief answer explains the Square shop's retail-only policy in ordinary terms."),
    691: ((7200, 9600), "Shopkeeper", ("Sweden only recently gained", "independence from the Kalmar Union", "with Denmark and Norway."),
          "The rumor preserves the recency of Sweden's independence and names the Union and both other countries."),
    815: ((16000,), "Port Worker", ("You have no cargo.",),
          "The worker tells the player plainly why Cargo Setup cannot reopen once the two lots have been left behind."),
}


def text_ref(entry):
    return panels.text_reference(entry) | {"exact_hex": entry.text.hex()}


def live_baseline(release, source, installed, font):
    capture = read(CAPTURE)
    terminal = baseline.ROOT / "terminal.json"
    journal = baseline.ROOT / "capture/navigation_command_journal.json"
    requests = baseline.ROOT / "trace/requests.json"
    final, trace, commands = map(read, (terminal, requests, journal))
    donor = capture["battery_save_preloaded"]
    assert capture["ROM_sha256"] == final["candidate_sha256"] == commands["ROM_sha256"] == release["candidate_sha256"]
    assert capture["frames"] == commands["last_command_frame"] == final["total_frames"] == 16000
    assert capture["cold_boot"] and not capture["savestate_loaded"] and final["ordinary_controller_inputs"]
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == final["copied_save_sha256"] == donor["source_sha256"]
    assert all(digest(path) == sha for path, sha in final["evidence"].items())
    assert not trace["errors"] and not trace["mismatches"] and trace["all_host_slots_restored_and_core_file_exact"]
    assert all(row["validation_passed"] for row in commands["commands_received"])
    got = trace["source_requests"]
    frames = panels.shots(capture, "_navigation.png")
    expected = {frame: key for key, (holds, *_) in KEEP.items() for frame in holds} | dict.fromkeys(HOLDS, KEY)
    assert got == final["common_requests"] and len(got) == 2 * len(expected)
    seen = {}
    old_lines = ("There's still cargo aboard.", "Continue?")
    for (frame, key), (getter, copier) in zip(sorted(expected.items()), zip(got[::2], got[1::2], strict=True), strict=True):
        assert getter["PC"] == 0x0205528C and copier == getter | {"PC": 0x020534F4}
        assert getter["message_ID"] == key and 0 < frame - getter["frame"] < 400
        assert getter["caller_LR"] == (WRAPPER + 20 if key == KEY else 0x02053FF8)
        lines = old_lines if key == KEY else KEEP[key][2]
        assert installed[key].text.decode("ascii").split() == " ".join(lines).split()
        screen = panels.picture(frames[frame])
        evidence = dict(capture=frames[frame], actual_lines=lines, requests=[getter, copier],
                        body_ink_pixels=panels.exact_body(font, lines, screen))
        if key == KEY:
            evidence["choices"] = [panels.find_mask(font, label, screen, area) for label, area in
                                   (("No", (123, 360, 160, 377)), ("Yes", (190, 360, 225, 377)))]
        else:
            evidence["nameplate"] = panels.nameplate(font, KEEP[key][1], screen)
        seen[frame] = evidence
    screens = {f: panels.picture(frames[f]) for f in (12800, 13200, 14000, 14800)}
    storage = (0, 279, 62, 309)
    slots = [screens[f].crop(storage) for f in (12800, 13200, 14000)]
    assert slots[0].tobytes() != slots[1].tobytes() == slots[2].tobytes()
    labels = [screens[frame].crop((0, 259, 119, 275)).tobytes() for frame in (12800, 13200, 14000)]
    assert labels[0] == labels[1] == labels[2]
    assert screens[14800].tobytes() == panels.picture(frames[11600]).tobytes()
    retained = [
        dict(id=f"COMMON_MESSAGE_{key}", message_ID=key, speaker=speaker,
             context="Riga Square retail shops" if key != 815 else "Riga Port Cargo Setup after confirming Finish",
             clean_Japanese=source[key].text.decode("cp932"), english=installed[key].text.decode("ascii").strip(),
             source_reference=text_ref(source[key]), current_reference=text_ref(installed[key]),
             installed_reference=text_ref(installed[key]), observed=[seen[f] for f in holds],
             decision="retention", localization_note=reason, review=dict.fromkeys(GATES, True))
        for key, (holds, speaker, _, reason) in KEEP.items()
    ]
    return dict(ordinary_gameplay=True, donor=reference(donor["source"]), evidence=list(map(reference, (CAPTURE, requests, journal, terminal))),
                retained=retained, warning=[seen[f] for f in HOLDS],
                storage=dict(before_unload=12800, after_unload=13200, after_No=14000,
                             Yes_returned_to_port=14800, reopen_without_cargo=16000,
                             matching_unloaded_and_No_region=storage, temporary_storage_label_sha256=sha256(labels[0]).hexdigest(),
                             identical_storage_mask_sha256=sha256(slots[1].tobytes()).hexdigest()))


def verify_native(ctx, target, deployed, body):
    cpu, get, provider = target.machine(ctx.arm, deployed, target.raw, target.plan)
    address = get(0x5528C, KEY)
    assert bytes(cpu.mem_read(address, len(body) + 1)) == body + b"\0" and provider.reads
    cpu.reg_write(UC_ARM_REG_R0, KEY)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.emu_start(WRAPPER, FORMAT_END, count=3000000)
    expanded, display = unpack_from("<2I", ctx.arm, 0x54890)
    assert bytes(cpu.mem_read(expanded, len(body) + 1)) == body + b"\0"
    formatted = bytes(cpu.mem_read(display, 256)).split(b"\0", 1)[0]
    raster, _, _ = modal.font_tools(ctx.image)
    font = modal.GameAsciiFont.from_arm9(ctx.arm)
    plane, lines, origins, glyphs = modal.render(raster, font, ctx.arm, formatted)
    assert lines == [DRAFT] and (glyphs[0]["code"], glyphs[-1]["code"]) == (ord("T"), ord("?"))
    sheet = ROOT / "cargo_storage_native.png"
    paper = Image.frombytes("L", (modal.WIDTH, modal.HEIGHT), bytes(255 - 255 * ink for ink in plane))
    paper.resize((modal.WIDTH * 3, modal.HEIGHT * 3), Image.Resampling.NEAREST).save(sheet)
    return dict(lines=lines, origins=origins, formatted_hex=formatted.hex(), native_ink_sha256=sha256(plane).hexdigest(),
                native_glyph_count=len(glyphs), complete_glyphs_bounds_and_words=True, pages=1), reference(sheet)


def stage():
    release = read(parent.RELEASE)
    assert digest(parent.ROM) == release["candidate_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    startup = read(release["own_registered_startup"])
    ctx = tools.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=startup["actual_captain_getter"])
    clean = NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = tools.observed.tools.common_message_entries(clean.read_file(COMMON), clean_arm)
    installed = tools.recruit.catalogue(ctx.arm, ctx.common)
    assert sha256(ctx.arm).hexdigest() == release["target_ARM9_sha256"] and sha256(ctx.common).hexdigest() == release["target_COMMON_sha256"]
    old, ja = installed[KEY], source[KEY]
    binding, = (r for r in read(HISTORICAL)["records"] if r["message_ID"] == KEY)
    caller, = binding["native_callers"]
    start = caller["code_start"] - 0x02000000
    code = bytes.fromhex(caller["exact_hex"])
    assert caller["call"] == 0x020836E0 and caller["target"] == WRAPPER
    assert ctx.arm[start:start + len(code)] == clean_arm[start:start + len(code)] == code
    assert ja.text.hex() == binding["source_hex"]
    assert all(byte >= 32 or byte == 10 for byte in old.text) and b"%" not in ja.text + old.text
    body = DRAFT.encode("ascii").ljust(len(old.text), b" ")
    assert len(body) == len(old.text) and b"%" not in body and b"\n" not in body
    live = live_baseline(release, source, installed, modal.GameAsciiFont.from_arm9(ctx.arm))
    deployed, rows, allocation = tools.owned_deployment(ctx.common, ctx.arm, installed, {KEY: body})
    assert {a.message_id for a, b in zip(installed, rows, strict=True) if a != b} == {KEY}
    assert allocation[KEY]["new_null_fields"] == 0
    reverted, _, _ = tools.owned_deployment(deployed, ctx.arm, rows, {KEY: old.text})
    assert bytes(reverted) == ctx.common
    target = tools.with_components(ctx, ctx.arm, deployed)
    ROOT.mkdir(exist_ok=True)
    result, sheet = verify_native(ctx, target, deployed, body)
    ctx.image.replace_file(COMMON, deployed)
    candidate = bytes(ctx.image.rom.save())
    ctx.image.replace_file(COMMON, reverted)
    assert sha256(ctx.image.rom.save()).hexdigest() == release["candidate_sha256"]
    if ROM.exists():
        assert ROM.read_bytes() == candidate
    else:
        with ROM.open("xb") as stream:
            stream.write(candidate)
    record = dict(id=f"COMMON_MESSAGE_{KEY}", file_path=COMMON, message_id=KEY, english=DRAFT,
                  speaker="Cargo Setup confirmation", context="Finish after unloading cargo into Temporary Storage.",
                  source_meaning="Some cargo remains. Is it all right to continue?",
                  clean_Japanese=ja.text.decode("cp932"), native_callers=[caller], arguments=[],
                  source_reference=text_ref(ja), current_reference=text_ref(old), installed_reference=text_ref(rows[KEY]),
                  decision="revision", localization_note="Name the visible storage row and use Finish to match the command. Keep the source's confirmation question and the existing No and Yes choices.",
                  review=dict.fromkeys(GATES, True) | {"formatting": False}, cases=[result])
    write(OUT, dict(candidate=str(ROM), candidate_sha256=digest(ROM), predecessor_sha256=release["candidate_sha256"],
                    clean_input_sha256=release["clean_input_sha256"], target_ARM9_sha256=release["target_ARM9_sha256"],
                    target_COMMON_sha256=sha256(deployed).hexdigest(), exact_parent_reserialize=True,
                    allocations=allocation, records=[record], sheets=[sheet], native_pages=1,
                    baseline=live, translation_policy="natural-dialogue-v2", encoder="dialogue-relocatable-v1", target_locale="en-US",
                    review_gates=list(GATES), visual_review_complete=False, paired_gameplay_complete=False, registered=False))
    print("Staged COMMON 268 with a complete native modal page and exact predecessor inverse.")


def replay():
    edit, old = read(OUT), read(CAPTURE)
    donor = old["battery_save_preloaded"]
    assert digest(ROM) == edit["candidate_sha256"] and old["ROM_sha256"] == edit["predecessor_sha256"]
    assert digest(donor["source"]) == donor["source_sha256"]
    directory = ROOT / "riga"
    directory.mkdir()
    inputs = directory / "inputs.json"
    write(inputs, old["scripted_input_schedule"])
    original = sys.argv
    try:
        sys.argv = [__file__, "--rom", str(ROM), "--out", str(directory), "--frames", str(old["frames"]),
                    "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen", "--press-start", "-1",
                    "--capture-every", "999999", "--capture-at", *map(str, sorted(panels.shots(old, "_navigation.png")))]
        playback.harness.main()
    finally:
        sys.argv = original


def verify_replay():
    edit, old = read(OUT), read(CAPTURE)
    new_path = ROOT / "riga/capture_report.json"
    new = read(new_path)
    assert new["ROM_sha256"] == digest(ROM) == edit["candidate_sha256"] and old["ROM_sha256"] == edit["predecessor_sha256"]
    assert new["frames"] == old["frames"] and new["scripted_input_schedule"] == old["scripted_input_schedule"]
    for report in (old, new):
        assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
        assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
        assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert old["battery_save_preloaded"]["source_sha256"] == new["battery_save_preloaded"]["source_sha256"]
    before, after = (panels.shots(report, suffix) for report, suffix in ((old, "_navigation.png"), (new, "_cold_boot.png")))
    assert before.keys() <= after.keys()
    font = modal.GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file(ARM))
    figures = Image.new("RGB", (1024, 476), "#263238")
    labels = ImageDraw.Draw(figures)
    revised, unchanged = [], []
    for frame in sorted(before):
        a, b = (panels.picture(rows[frame]) for rows in (before, after))
        box = ImageChops.difference(a, b).getbbox()
        if frame not in HOLDS:
            assert box is None, (frame, box)
            unchanged.append(frame)
            continue
        assert box and 16 <= box[0] < box[2] <= 245 and 296 <= box[1] < box[3] <= 343
        lines = edit["records"][0]["cases"][0]["lines"]
        pixels = panels.exact_body(font, lines, b)
        assert a.crop((102, 354, 245, 378)).tobytes() == b.crop((102, 354, 245, 378)).tobytes()
        revised.append(dict(frame=frame, message_id=KEY, lines=lines, bounds=box, body_ink_pixels=pixels,
                            old=before[frame], new=after[frame], choices_exact=True))
        for side, (label, screen) in enumerate((("Previous", a), ("Candidate", b))):
            x, y = side * 512, (len(revised) - 1) * 238
            labels.text((x + 6, y + 4), f"{label} / {frame}", fill="white")
            figures.paste(screen.crop((0, 276, 256, 384)).resize((512, 216), Image.Resampling.NEAREST), (x, y + 20))
    assert tuple(row["frame"] for row in revised) == HOLDS and {13200, 14000, 14800, 16000} <= set(unchanged)
    sheet = ROOT / "cargo_storage_paired.png"
    figures.save(sheet)
    write(PAIRED, dict(candidate_sha256=edit["candidate_sha256"], predecessor_sha256=edit["predecessor_sha256"],
                       ordinary_gameplay=True, previous=reference(CAPTURE), candidate=reference(new_path),
                       changed_holds=len(revised), unchanged_holds=len(unchanged), revised=revised,
                       unchanged_frames=unchanged, sheets=[reference(sheet)]))
    print(f"Verified {len(revised)} changed Cargo Setup holds and {len(unchanged)} matching companion frames.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "replay", "verify", "patch", "startup"))
    action = parser.parse_args().action
    if action in ("patch", "startup"):
        FunctionType(release_checks.release_check.__code__, vars(release_checks) | globals())(read(OUT), action)
    else:
        {"stage": stage, "replay": replay, "verify": verify_replay}[action]()
