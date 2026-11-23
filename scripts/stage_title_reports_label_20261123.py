"""Match the title Options label to the Reports confirmation and in-game label."""

from argparse import ArgumentParser
from pathlib import Path
from struct import unpack, unpack_from
from types import FunctionType

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from scripts import register_square_and_market_reward_wraps_20261123 as parent
from scripts.probe_button_prompt_native import BASE, machine


base, native, town = parent.base, parent.native, parent.stage.town
ARM, COMMON, CLEAN = parent.ARM, parent.COMMON, parent.stage.CLEAN
ROOT = Path(".codex-release-work/title_reports_label_20261123/staged")
ROM, PROOF = ROOT / "Title_Reports_Label_STAGED.nds", ROOT / "stored_proof.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
KEY = "DK4_OPTIONS_REPORT_MENU"
FIELD, END = 0x137984, 0x137990
HANDLERS = (0x021078B8, 0x0203FD54, 0x0203FCD0)
LABELS = (0x137990, FIELD, 0x137A78)
HISTORICAL = Path("translations/options_arm9.json")


def menu(arm):
    cpu = machine(arm)
    # Stop at the original widget boundary after the retail handler has
    # selected its three descriptors and their count.
    cpu.emu_start(0x0203EC10, 0x02051F4C, count=40)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x02051F4C
    table = cpu.reg_read(UC_ARM_REG_R0)
    count = cpu.reg_read(UC_ARM_REG_R1)
    assert (table, count) == (0x02115374, 3)
    labels = []
    for index, offset in enumerate(LABELS):
        desc = table + index * 16
        ptr, *flags = unpack("<4I", cpu.mem_read(desc, 16))
        assert ptr == BASE + offset and flags == [1, 1, 0]
        raw, sep, _ = bytes(cpu.mem_read(ptr, 16)).partition(b"\0")
        assert sep
        labels.append(dict(field=offset, descriptor=desc, pointer=ptr, handler=HANDLERS[index], text_hex=raw.hex()))
    return labels


def reviewed_slot(clean, arm):
    spec, = [r for r in base.load(HISTORICAL)["records"] if r["id"] == KEY]
    assert spec["offset"] == FIELD and spec["english"] == "Report"
    assert clean[FIELD:END] == bytes.fromhex(spec["source_hex"]).ljust(END - FIELD, b"\0")
    assert arm[FIELD:END] == b"Report".ljust(END - FIELD, b"\0")
    assert clean[0x138614:0x13861C] == bytes.fromhex(spec["source_hex"])
    assert arm[0x138614:0x13861C] == b"Reports\0"
    spans = ((0x3EC10, 0x3EC84), (0x115374, 0x1153A4), (0x3FCD0, 0x3FDD0), (0x3FDD4, 0x3FDD8))
    assert all(arm[lo:hi] == clean[lo:hi] for lo, hi in spans)
    # The accepted Available Companions layer moved the English Reports prompt.
    assert [unpack_from("<I", data, 0x3FDD0)[0] for data in (clean, arm)] == [0x02138844, 0x02138830]
    assert arm[0x138830:0x138850].partition(b"\0")[0] == b"Reports are %s. Change to %s?"
    replacement = b"Reports".ljust(END - FIELD, b"\0")
    revised = arm[:FIELD] + replacement + arm[END:]
    assert [i for i, (a, b) in enumerate(zip(arm, revised, strict=True)) if a != b] == [FIELD + 6]
    picked = [menu(a) for a in (clean, arm, revised)]
    assert [[bytes.fromhex(row["text_hex"]).decode(encoding) for row in rows]
            for rows, encoding in zip(picked, ("cp932", "ascii", "ascii"), strict=True)] == [
                ["サウンド", "収支報告", "洋上操作説明"], ["Sound", "Report", "Sailing Help"], ["Sound", "Reports", "Sailing Help"]]
    assert picked[1][::2] == picked[2][::2]
    return revised, picked


def stage():
    assert not ROM.exists() and not PROOF.exists()
    release = base.load(parent.RELEASE)
    previous = base.digest(parent.ROM)
    assert previous == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(CLEAN) == release["clean_input_sha256"]
    source, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    clean_arm, arm = (obj.read_file(ARM) for obj in (source, image))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    revised, selections = reviewed_slot(clean_arm, arm)
    first = native.files(image)
    image.replace_file(ARM, revised)
    final = native.files(image)
    assert first.keys() == final.keys() and {p for p in first if first[p] != final[p]} == {ARM}
    guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(source), final)
    assert not any(guard["source_bound_new_command_counts"].values())
    data = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True, exist_ok=True)
    ROM.write_bytes(data)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=previous,
        clean_sha256=release["clean_input_sha256"], target_ARM9_sha256=native.digest(revised),
        target_COMMON_sha256=release["target_COMMON_sha256"], whole_parent_inverse=True,
        source25=guard, native_title_menu_selections=selections,
        record=dict(id=KEY, file_path=ARM, offset=FIELD, exclusive_slot_end=END,
            source_hex=clean_arm[FIELD:END].hex(), current_hex=arm[FIELD:END].hex(), installed_hex=revised[FIELD:END].hex(),
            source_meaning="Open the income-and-expense reports setting.",
            context="The middle Options row opens the Reports confirmation. The feature can be turned on or off.",
            localization_note="Use Reports for the recurring notices, matching the original function, the confirmation and the in-game label.",
            source_Japanese="収支報告", previous_English="Report", english="Reports", decision="revision"),
        prior_label=dict(path=str(HISTORICAL), sha256=base.digest(HISTORICAL))))
    print(f"Staged {base.digest(ROM)} with one owned byte change and three original Options descriptors.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("stage", "patch", "startup"))
    action = parser.parse_args().action
    if action == "stage":
        stage()
    else:
        step = getattr(parent.parent.parent.staged.prior.release_tools, action)
        FunctionType(step.__code__, step.__globals__ | globals())()
