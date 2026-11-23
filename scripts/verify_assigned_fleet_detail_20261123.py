"""Verify the assigned Fleet Info reproduction and retain its source and replay evidence."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageChops, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts.observe_assigned_fleet_detail_20261123 import ROOT, RELEASE
from scripts.probe_button_prompt_native import call, machine
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, write
from scripts.verify_captain_biographies_v1 import captured
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_plaque_release_v247 import find_mask


OUT = Path("translations/editorial_checkpoints/shared_display_20261123/assigned_fleet_detail_20261123.json")
ARM = "/__arm9__.bin"
PANELS = (12000, 12400)


def capture(root, end):
    paths = [root / name for name in (
        "capture/capture_report.json", "terminal.json", "trace/requests.json", "trace/source_contract.json",
        "capture/navigation_command_journal.json", "controller.jsonl",
    )]
    run, terminal, trace, contract, journal = map(read, paths[:-1])
    assert run["cold_boot"] and not run["savestate_loaded"] and not run["callback_errors"]
    assert not any(v for k, v in run.items() if k.startswith("synthetic_"))
    assert run["frames"] == terminal["total_frames"] == end
    assert terminal["ordinary_controller_inputs"] and not terminal["common_requests"]
    assert trace["rows"] == terminal["fleet_trace"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(paths[3])
    assert all(row["validation_passed"] for row in journal["commands_received"])
    donor = run["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert digest(donor["source"]) == donor["source_sha256"] == terminal["copied_save_sha256"]
    frames = {row["frame"]: row for row in run["frames_captured"] if row["path"].endswith("_navigation.png")}
    owner_calls = {row["owner"]: row for row in trace["rows"]}
    assert set(PANELS) <= frames.keys()
    assert owner_calls["regional_order_selection"]["frame"] < owner_calls["legacy_fleet_factory"]["frame"]
    assert owner_calls["legacy_fleet_factory"]["LR"] == 0x020407E4
    assert "missionary_name_getter" not in owner_calls
    return dict(run=run, bindings=[reference(path) for path in paths], owner_calls=owner_calls, frames=frames,
                donor=reference(donor["source"]), donor_path=donor["destination"])


def format_checks(arm, destination_catalogue):
    cpu = machine(arm)
    args, buffer, string = 0x02411000, 0x02412000, 0x02413000
    target = 0x021370F8
    finance, = unpack_from("<I", arm, 0x38E00)
    assert finance == 0x0213710C
    sentinel = b"\xA5" * 128

    def format_result(pointer, arguments):
        cpu.mem_write(args, pack(f"<{len(arguments)}I", *arguments))
        cpu.mem_write(buffer, sentinel)
        call(cpu, 0xCE898, (buffer, pointer, args))
        result = bytes(cpu.mem_read(buffer, len(sentinel)))
        value, _, tail = result.partition(b"\0")
        assert tail == sentinel[len(value) + 1:]
        return value

    samples = []
    for amount in (0, 7, 67, 765, 7654, 76543, 765432, 7654321, 76543210, 765432109, 0xFFFFFFFF):
        values = (amount, 0xFFFFFFFF - amount, amount // 100)
        actual = format_result(finance, values).decode("ascii")
        expected = f"Income  {values[0]:11d}Expenses{values[1]:11d}\nInvested{values[2]:11d}"
        assert actual == expected
        first, last = actual.split("\n")
        assert len(first) * 6 == 228 and len(last) * 6 == 114
        samples.append(dict(amounts=values, rendered_output=actual, bounds=[228, 24]))
    names = []
    for entry in destination_catalogue["offline"]["installed"]["destinations"][:115]:
        name = bytes.fromhex(entry["exact_hex"])
        assert name.endswith(b"\0")
        cpu.mem_write(string, name)
        value = format_result(target, (string,))
        assert value == b"To: " + name[:-1]
        width = sum(6 if ord(c) < 128 else 12 for c in value.decode("cp932"))
        assert width <= 174
        names.append(dict(destination=entry["destination"], output_hex=value.hex(), width_px=width,
                          conditional_legacy_label=entry["destination"] == 114))
    return dict(finance_cases=samples, destination_names=names, native_formatter=0x020CE898,
                observation="Offline native substitution and allocation checks. Live pixels are verified separately.")


def verify_packed(rom, staged, original):
    arm = NdsImage.open(rom).read_file(ARM)
    font = GameAsciiFont.from_arm9(arm)
    detail, report = [captured(staged["frames"][n]) for n in PANELS]
    names = find_mask(font, "To: Stockholm", detail, (78, 242, 237, 260))
    level = find_mask(font, "Level   30", detail, (76, 79, 153, 99))
    assert ImageChops.difference(captured(original["frames"][12000]), detail).getbbox()[0] >= 78
    rows = ("Income", "Expenses", "Invested")
    glyphs = []
    for i, label in enumerate(rows):
        y = 269 + i * 14
        label_ink, label_bounds = complete_mask(font, label, report, 86, y, (230, 230, 230))
        amount_ink, amount_bounds = complete_mask(font, "0", report, 194, y, (230, 230, 230))
        glyphs.append(dict(label=label, label_ink=label_ink, label_bounds=label_bounds,
                           displayed_amount=0, amount_ink=amount_ink, amount_bounds=amount_bounds))
    assert len({g["amount_bounds"][0] for g in glyphs}) == 1
    changed = ImageChops.difference(report, detail).getbbox()
    assert changed is not None and changed[0] >= 74 and changed[1] >= 258 and changed[2] <= 212
    return dict(destination=names, retained_level=level, report_rows=glyphs, report_box_diff=changed,
                offline=format_checks(arm, read("translations/editorial_checkpoints/shared_display_20261123/fleet_destination_name_caller_20261123.json")))

def verify():
    release = read(RELEASE)
    original = capture(ROOT, 12400)
    assert original["run"]["ROM_sha256"] == release["candidate_sha256"] == digest(release["candidate"])
    assert release["clean_input_sha256"] == digest(CLEAN)
    stock, parent = (NdsImage.open(p).read_file(ARM) for p in (CLEAN, release["candidate"]))
    records = []
    for frame, owner, at, source, english, note in (
        (12000, "target_city_format", 0x1370F8, "目標街：%s", "To: %s",
         "A compact destination field for the selected fleet's current target port. Keep the game-supplied town name."),
        (12400, "finance_format", 0x137118, "収入額%8lu支出額%8lu投資額%8lu", "Income / Expenses / Invested",
         "Match the terminology used on the modern regional panel. Keep all three unsigned amounts in the original order."),
    ):
        call = original["owner_calls"][owner]
        assert call["pointer"] == 0x02000000 + at
        stored = bytes.fromhex(call["value_hex"]) + b"\0"
        assert stored == source.encode("cp932") + b"\0"
        assert stock[at:at+len(stored)] == parent[at:at+len(stored)] == stored
        records.append(dict(source=dict(component=ARM, offset=at, exact_hex=stored.hex(), Japanese=source),
            current=dict(component=ARM, offset=at, exact_hex=stored.hex(), frame=original["frames"][frame]),
            runtime=call, proposed_English=english, localization_note=note,
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    trials = {}
    for code, name, rom_name, observation in (
        ("fixed_slots", "Compact fixed-slot trial", "Assigned_Fleet_Info_STAGED.nds",
         "Destination is complete. Unequal label widths shift the third label across two report rows."),
        ("aligned_report", "Wide horizontal trial", "Assigned_Fleet_Info_Aligned_STAGED.nds",
         "Destination, Income and Expenses are complete. The third row begins Invested but source X wraps into earlier text."),
        ("stacked_report", "Native rows trial", "Assigned_Fleet_Info_STAGED.nds",
         "Destination and first row are complete. The Expenses E and lower part of Invested are missing."),
        ("packed_report", "Two source rows trial", "Assigned_Fleet_Info_STAGED.nds",
         "Read the attached pixels and validate the complete row masks before registration."),
    ):
        root = ROOT / code
        replay = ROOT.with_name(f"fleet_info_{code}_replay")
        if not (replay / "terminal.json").exists():
            continue
        staged = capture(replay, 12800)
        rom = root / rom_name
        assert staged["run"]["ROM_sha256"] == digest(rom) == read(root / "stage.json")["staged"]["sha256"]
        assert staged["donor"] == original["donor"]
        assert [staged["frames"][n]["framebuffer_sha256"] for n in range(10600, 11801, 200)] == [
            original["frames"][n]["framebuffer_sha256"] for n in range(10600, 11801, 200)]
        assert ImageChops.difference(captured(staged["frames"][12000]), captured(original["frames"][12000])).getbbox()[1] >= 238
        assert ImageChops.difference(captured(staged["frames"][12600]), captured(staged["frames"][12000])).getbbox() is None
        assert staged["frames"][12800]["framebuffer_sha256"] == original["frames"][11800]["framebuffer_sha256"]
        trials[code] = dict(name=name, observation=observation, rom=reference(rom), stage=reference(root / "stage.json"),
            evidence=staged["bindings"], captures=[staged["frames"][n] for n in PANELS], seven_prechange_frames_match=True,
            report_closes_to_exact_fleet_detail=True, fleet_detail_closes_to_exact_list=True)
        if code == "packed_report":
            trials[code]["formatted"] = verify_packed(rom, staged, original)
            trials[code]["observation"] = "All labels, numeric columns and return transitions pass."

    groups = [("Registered Seoul ROM", [original["frames"][n] for n in PANELS])]
    groups.extend((item["name"], item["captures"]) for item in trials.values())
    sheet = Image.new("RGB", (522 * len(groups), 350), "#263238")
    labels = ImageDraw.Draw(sheet)
    for index, (title, frames) in enumerate(groups):
        x = index * 522 + 5
        labels.text((x, 6), title, fill="white")
        for box, y, frame in (((0, 192, 256, 267), 22, frames[0]), ((0, 240, 256, 318), 184, frames[1])):
            section = captured(frame).crop(box)
            sheet.paste(section.resize((section.width * 2, section.height * 2), Image.Resampling.NEAREST), (x, y))
    image_path = OUT.with_suffix(".png")
    sheet.save(image_path)
    write(OUT, dict(registered_release=reference(RELEASE), original_ROM_sha256=original["run"]["ROM_sha256"],
        player_path="Assign Manuel Fleet to patrol Stockholm. Open Info, Fleet Info, Manuel Fleet, then Report.",
        cold_boot_and_ordinary_controller_input_after_prepared_save=True, existing_fleet_from_prepared_save=original["donor"],
        hardware=False, reproduced_on_registered_ROM=True, records=records, baseline_evidence=original["bindings"],
        prior_focus=reference("translations/editorial_checkpoints/shared_display_20261123/fleet_destination_name_caller_20261123.json"),
        trials=trials, screenshot=reference(image_path), registered_ROM_changed=False, new_editorial_credit=0,
        full_goal_complete=False))
    print("Verified the two untranslated Fleet Info fields and sealed the exact source, trace and paired frames.")


if __name__ == "__main__":
    verify()
