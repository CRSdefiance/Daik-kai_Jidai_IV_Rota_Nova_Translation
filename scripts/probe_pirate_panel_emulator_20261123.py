"""Run the original alternate-battle screen in a disclosed DeSmuME fixture."""

from argparse import ArgumentParser
import ctypes as ct
import json
from pathlib import Path
from struct import pack, unpack
import sys

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.rom.nds import NdsImage
from scripts import headless_desmume_v193 as harness
from scripts.inspect_committed_gpu_v646 import ImageReader
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.probe_pirate_affiliation_20261123 import ENGLISH, JAPANESE, SLOT
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, PACKAGE, digest, read, reference
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = Path(".codex-release-work/shared_display_20261123/alternate_battle_panel_v2")
RELEASE = PACKAGE / "verification/registered_release_verification.json"
STAGED = Path(".codex-release-work/pirate_affiliation_20261123/staged")
DEPARTURE = Path("work/analysis/full_fleet_battle_v652/departure_prefix.json")
STAFFING = Path("work/analysis/full_fleet_battle_v652/staffing_proof.json")
PUMP = 0x020CF7A4
ENTRY, STATE = 0x023FD000, 0x023FD0F0
PREPARE, ACTOR, FRAMES = 4800, 27, 6700
CAPTURES = (4800, 4801, 4900, 5000, 5150, 5300, 5450, 5600, 5900, 6200, FRAMES)


def branch(pc, destination):
    assert pc % 4 == destination % 4 == 0 and abs(destination - pc) < 0x2000000
    return 0xEA000000 | ((destination - pc - 8) >> 2) & 0xFFFFFF


def helper(arm):
    assert all(not (part.ramAddress < STATE + 16 and ENTRY < part.ramAddress + len(part.data) + part.bssSize)
               for part in MainCodeFile(arm, BASE).sections)
    assert arm[PUMP - BASE:PUMP - BASE + 4] == bytes.fromhex("30402de9")
    site = 0x02073DE0
    assert direct_bl_target(unpack("<I", arm[site - BASE:site - BASE + 4])[0], site) == 0x0200A54C
    code = f"""
    push {{r0-r12, lr}}
    mrs r4, cpsr
    push {{r4, r5}}
    ldr r5, state
    ldr r0, [r5]
    cmp r0, #1
    bne resume
    mov r0, #2
    str r0, [r5]
    sub sp, sp, #8
    mov r0, #{ACTOR}
    mov r1, #0
    mov r2, #0
    add r3, r5, #4
    add r4, r5, #8
    str r4, [sp]
    ldr r4, variant
    str r4, [sp, #4]
    bl 0x0200A54C
    add sp, sp, #8
    mov r0, #3
    str r0, [r5]
    resume:
    pop {{r4, r5}}
    msr cpsr_f, r4
    pop {{r0-r12, lr}}
    push {{r4, r5, lr}}
    b {PUMP + 4:#x}
    state: .word {STATE:#x}
    variant: .word 0x191
    """
    raw = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(code, ENTRY)[0])
    assert len(raw) < STATE - ENTRY
    return raw.ljust(STATE - ENTRY, b"\0") + pack("<4I", 1, 0, 0, 0)


def install_fixture(core, arm, label):
    image = ImageReader(core)
    ram = image.anchor("WRAM", 1, 0x400000)
    memory = image.read(ram, 0x400000)
    cpu, get = get_machine(arm, memory)
    fleet = get(0xCB1A8) + 0x2090
    crew = [member for slot in range(4, 31) if (member := get(0x82BC4, fleet, slot)) not in (24, 208)]
    actor = get(0xCB184) + 4 + ACTOR * 32
    nickname = bytes(cpu.mem_read(get(0x7ED88, actor), 32)).split(b"\0", 1)[0]
    assert len(crew) >= 4 and get(0x7F244) == 1
    assert get(0x7EE08, actor) == ACTOR and get(0x7E958, actor) == 21 and nickname.startswith(b"Aziza")
    payload = helper(arm)
    location = ram + ENTRY - BASE
    original = image.read(location, len(payload))
    installed = arm[SLOT:SLOT + len(JAPANESE)]
    assert installed in (JAPANESE, ENGLISH)
    assert not any(original) and memory[SLOT:SLOT + len(JAPANESE)] == installed
    pump_ptr = ram + PUMP - BASE
    assert image.read(pump_ptr, 4) == arm[PUMP - BASE:PUMP - BASE + 4]
    ct.memmove(location, payload, len(payload))
    if installed != label:
        ct.memmove(ram + SLOT, label, len(label))
    ct.memmove(pump_ptr, pack("<I", branch(PUMP, ENTRY)), 4)
    return image, location, pump_ptr, ram + SLOT, original, crew, nickname.decode("cp932")


def run(case):
    release = read(RELEASE)
    if case == "staged":
        rom = STAGED / "Translation_DS_Pirate_Affiliation_STAGED.nds"
        staged = read(STAGED / "stored_proof.json")
        assert staged["predecessor_sha256"] == release["candidate_sha256"] and staged["exact_parent_inverse"]
        candidate = staged["candidate_sha256"]
    else:
        rom = Path(release["candidate"])
        candidate = release["candidate_sha256"]
    assert digest(rom) == candidate
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    arm = NdsImage.open(rom).read_file(ARM)
    donor = read(STAFFING)["prepared_save"]
    assert digest(donor["path"]) == donor["sha256"]
    folder = ROOT / case
    folder.mkdir(parents=True)
    events = read(DEPARTURE) + [dict(start=n, duration=8, buttons=["A"]) for n in (5501, 5651, 5901, 6051, 6301, 6501)]
    inputs = folder / "inputs.json"
    inputs.write_text(json.dumps(events, indent=2) + "\n", encoding="utf-8")
    label = JAPANESE if case == "installed" else ENGLISH
    stored_label = arm[SLOT:SLOT + len(label)]
    local, previous = harness.ct, sys.argv
    observed, frame, fixture = [], 0, None

    class Loader:
        def __getattr__(self, name):
            return getattr(local, name)

        def CDLL(self, path, *args, **kwargs):
            core = local.CDLL(path, *args, **kwargs)
            if not str(path).lower().endswith("desmume_libretro.dll"):
                return core
            advance = core.retro_run

            def tick():
                nonlocal frame, fixture
                if frame == PREPARE:
                    fixture = install_fixture(core, arm, label)
                advance()
                frame += 1
                if fixture and (not observed or observed[-1]["state"] != 3):
                    image, scratch, pump_ptr, text_ptr, original, _, _ = fixture
                    state = unpack("<3I", image.read(scratch + STATE - ENTRY, 12))
                    if not observed or observed[-1]["state"] != state[0]:
                        observed.append(dict(frame=frame, state=state[0], result_words=state[1:]))
                    if state[0] == 3:
                        ct.memmove(pump_ptr, arm[PUMP - BASE:PUMP - BASE + 4], 4)
                        if stored_label != label:
                            ct.memmove(text_ptr, stored_label, len(stored_label))
                        assert image.read(scratch, STATE - ENTRY) == helper(arm)[:STATE - ENTRY]
                        ct.memmove(scratch, original, len(original))
                        assert image.read(scratch, len(original)) == original

            core.retro_run = tick
            return core

    sys.argv = [harness.__file__, "--rom", str(rom), "--out", str(folder / "capture"),
                "--battery-save", donor["path"], "--touchscreen", "--inputs-json", str(inputs),
                "--frames", str(FRAMES), "--capture-every", "999999", "--capture-at", *map(str, CAPTURES)]
    harness.ct = Loader()
    try:
        harness.main()
    finally:
        harness.ct, sys.argv = local, previous
    report = folder / "capture/capture_report.json"
    finished = read(report)
    assert finished["cold_boot"] and not finished["savestate_loaded"] and not finished["callback_errors"]
    assert finished["frames"] == FRAMES and finished["ROM_sha256"] == candidate
    assert digest(donor["path"]) == donor["sha256"] and digest(rom) == candidate
    assert fixture and any(row["state"] == 2 for row in observed)
    result = dict(candidate_sha256=candidate, capture=reference(report), inputs=reference(inputs),
                  actor=ACTOR, name=fixture[-1], assigned_crew=fixture[-2], label_slot_hex=label.hex(),
                  label_overridden_in_memory=label != stored_label,
                  in_memory_test_entry=0x0200A54C, scratch=[ENTRY, STATE + 16], state_transitions=observed,
                  restored_explicit_fixture_bytes=observed[-1]["state"] == 3, ordinary_gameplay=False)
    (folder / "fixture.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"{case} fixture states: {observed}")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("installed", "english", "staged"))
    run(parser.parse_args().case)
