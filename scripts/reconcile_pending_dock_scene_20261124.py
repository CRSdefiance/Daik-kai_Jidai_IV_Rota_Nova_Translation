"""Bind the pending dock request to its scene-manager inputs and ordinary Copenhagen trace."""

from argparse import ArgumentParser
from struct import iter_unpack, pack, unpack_from
from types import FunctionType

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE

from scripts import observe_copenhagen_dock_producer_20261124 as previous
from scripts import register_claudio_opening_wrap_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write
from scripts.verify_personal_gameplay_v841 import get_machine


ROOT = current.ROM.parent.with_name("editorial_20261124_pending_dock_scene")
OUT = previous.OUT.with_name("pending_dock_scene_current_20261124.json")
BASE = previous.trace.BASE
ENTRY, STAGE, TRANSFER = 0x02090AA4, 0x02021D0C, 0x02021B80
INPUT, MODE_READ, CALLBACK, REPLACE = 0x02021D2C, 0x02021D60, 0x02021DB4, 0x02021BD8
RESULT, PENDING, ACCEPT = previous.previous.RETURN, previous.previous.PENDING, previous.previous.ACCEPT
REQUEST_CTOR = 0x020904CC
VALUES = previous.VALUES | {MODE_READ: 4, CALLBACK: 4, REPLACE: 6}
HOOKS = {STAGE: (0x02021D04, 0x02090B2C, 0x02090CD4, 0x02090D44, 0x02090DCC,
                 0x02090E4C, 0x02090F98, 0x02091008),
         TRANSFER: (0x020294A0, 0x02029630, 0x02029730)}
SPANS = ((TRANSFER, 0x02021C14), (STAGE, 0x02021E20), (0x02023260, 0x0202326C),
         (0x02029434, 0x020294AC), (0x0202961C, 0x0202963C), (0x0202971C, 0x0202973C),
         (0x02090298, 0x020902F8), (0x020903AC, 0x020903C4), (0x020904BC, 0x02090514),
         (0x02090518, 0x02090540), (0x02090844, 0x020908F0), (ENTRY, 0x02090C18))
SCRATCH, REQUEST = 0x023F0200, 0x023F0280
REPLACEMENT_SOURCES = {
    0x020294A0: "Existing protagonist docking byte in a type-1 request",
    0x02029630: "Type 0 around the requested fleet",
    0x02029730: "Type 0 with fleet index 39",
}


def replacement_sources(arm):
    expected = {
        0x02021BD0: ("ldr", "r2, [r4, #8]"),
        REPLACE: ("str", "r2, [r0, #0x43c]"),
        0x0202944C: ("bl", "#0x2034674"),
        0x02029474: ("ldrb", "r1, [r1, #0x3c]"),
        0x02029494: ("bl", "#0x20904cc"),
        0x02029624: ("bl", "#0x2090518"),
        0x02029720: ("mov", "r1, #0x27"),
        0x02029724: ("bl", "#0x2090518"),
        0x020904D0: ("mov", "r3, #1"),
        0x020904D8: ("str", "r3, [r0, #4]"),
        0x020904DC: ("str", "r1, [r0, #8]"),
        0x0209052C: ("mov", "r2, #0"),
        0x02090530: ("str", "r2, [r4, #4]"),
        0x02090538: ("str", "r0, [r4, #8]"),
        0x02090860: ("cmp", "r1, #1"),
        0x020908CC: ("ldr", "r5, [r6, #0x2c]"),
    }
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for pc, operation in expected.items():
        ins, = decoder.disasm(arm[pc - BASE:pc - BASE + 4], pc)
        assert (ins.mnemonic, ins.op_str) == operation, (hex(pc), ins.mnemonic, ins.op_str)
    return dict(source_by_direct_caller=REPLACEMENT_SOURCES, instruction_bindings=expected)


def run():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    playback = previous.playback
    observer = FunctionType(previous.previous.observer.__code__, vars(previous.previous) | dict(VALUES=VALUES))
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=previous.previous.original.schedule,
                                 observer=observer, FOCUS={49, 65}, __file__=__file__)
    FunctionType(playback.main.__code__, scope)("landing")


def caller_census(image):
    found = {entry: [] for entry in HOOKS}
    literals = []
    for name, base, raw in previous.trace.loaded_components(image):
        for offset, (word,) in enumerate(iter_unpack("<I", raw[:len(raw) & ~3])):
            pc = base + offset * 4
            dest = previous.trace.direct_bl_target(word, pc)
            if dest in found:
                found[dest].append((name, pc))
            if word & ~1 in HOOKS:
                literals.append((name, pc, word))
    assert found == {entry: [("arm9_section_0", pc) for pc in addresses] for entry, addresses in HOOKS.items()}
    assert not literals
    return found


def offline(arm, raw):
    cpu, call = get_machine(arm, raw)
    manager = unpack_from("<I", arm, 0x90C14)[0] + 0x2438
    mode = unpack_from("<I", arm, 0x21E18)[0] + 0x54
    # Disable only the scene event loop in the copied RAM. Its ordinary active
    # behavior is checked in the Copenhagen trace, without changing mode.
    cpu.mem_write(mode, pack("<I", 0))
    stage_calls = []
    hook = cpu.hook_add(UC_HOOK_CODE, lambda uc, pc, size, data: stage_calls.append(pc),
                        begin=STAGE, end=STAGE)
    select = pack("<I", unpack_from("<I", arm, 0x904F0)[0])
    payload = (0x11111111, 0x22222222, 0x33333333)
    before = bytes([0xE5]) * 64

    def check(active, kind, argument):
        stage_calls.clear()
        view = before[:8] + pack("<I", active) + before[12:]
        cpu.mem_write(SCRATCH, view + before)
        cpu.mem_write(REQUEST, bytes(len(select) + 28))
        if kind == 1:
            call(REQUEST_CTOR - BASE, REQUEST, argument, 13)
            assert bytes(cpu.mem_read(REQUEST, 16)) == select + pack("<3I", kind, argument, 13)
        request = select + pack("<7I", kind, argument, 13, *payload, 0)
        cpu.mem_write(REQUEST, request)
        result = call(ENTRY - BASE, SCRATCH, REQUEST)
        written = 8 if active == kind else 0x28
        assert result == int(active != kind)
        assert bytes(cpu.mem_read(SCRATCH, 128)) == (view + before)[:written] + request[4:] + (view + before)[written + 28:]
        assert bytes(cpu.mem_read(REQUEST, len(request))) == request
        forwarded = active == 0 and kind == 1
        assert stage_calls == ([STAGE] if forwarded else [])
        if forwarded:
            assert bytes(cpu.mem_read(manager, 28)) == request[4:]
        return dict(active_type=active, incoming_type=kind, input_value=argument,
                    written_offset=written + 4, output_value=argument, invoked_scene_manager=forwarded)

    try:
        inputs = [*range(256), 256, 0x1000072, 0xFFFFFFFF]
        results = [check(0, 1, value) for value in inputs]
        gates = [check(active, kind, 114) for active in (0, 1, 2, 3) for kind in (0, 1, 2, 3)]
    finally:
        cpu.hook_del(hook)
    for at, size in ((SCRATCH, 128), (REQUEST, 32), (manager, 28), (mode, 4)):
        cpu.mem_write(at, raw[at - BASE:at - BASE + size])
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw
    return dict(mode_address=mode, temporary_mode=0, scene_manager_argument_address=manager + 4,
                byte_and_wide_inputs=results, active_and_incoming_type_cases=gates)


def bound_ordinary(release):
    root = ROOT / "landing"
    capture, request_file = root / "capture/capture_report.json", root / "requests.json"
    prior = read(previous.OUT)
    report, requests, older = map(read, (capture, request_file, prior["replay"]["path"]))
    assert digest(prior["replay"]["path"]) == prior["replay"]["sha256"]
    assert report["ROM_sha256"] == release["candidate_sha256"] and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == older["scripted_input_schedule"]
    assert requests["all_host_slots_restored_and_core_file_exact"] and not requests["errors"] and not requests["mismatches"]
    donor = report["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert donor["source_sha256"] == older["battery_save_preloaded"]["source_sha256"]
    panels = previous.previous.baseline.panels
    original, installed = (panels.shots(row, "_cold_boot.png") for row in (older, report))
    holds = prior["matching_gameplay_holds"]
    for frame in holds:
        assert installed[frame]["framebuffer_sha256"] == original[frame]["framebuffer_sha256"]
        assert digest(installed[frame]["path"]) == installed[frame]["PNG_sha256"]
    chain = [prior["native_request_input"], *prior["inherited_docking_chain"]]
    assert all(row in requests["rows"] for row in chain)
    scene_records = [row for row in requests["rows"] if row["PC"] in (INPUT, MODE_READ, CALLBACK, REPLACE, RESULT)]
    assert not any(row["PC"] == REPLACE for row in scene_records)
    entries = []
    for frame in (4016, 4017, 4409, 5209):
        scoped = [row for row in scene_records if row["frame"] == frame]
        assert [row["PC"] for row in scoped] == [INPUT, MODE_READ, CALLBACK, RESULT]
        given, mode_record, _, returned = scoped
        assert given["value"] == returned["value"] == 9 and mode_record["value"] == 1
        assert given["LR"] - 4 in HOOKS[STAGE]
        entries.append(dict(frame=frame, original_call=given["LR"] - 4, observed_registers=scoped))
    assert len(scene_records) == 4 * len(entries)
    return dict(ordinary_gameplay=True, matching_holds=holds, scene_entries=entries, ordinary_replacement_events=[],
                destination_value=9, native_dock_write=chain[-1],
                evidence=list(map(reference, (capture, request_file, donor["source"], previous.OUT))))


def verify():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    roms = tuple(map(NdsImage.open, (CLEAN, current.ROM)))
    just_before, arm = (rom.read_file(current.ARM) for rom in roms)
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    callers = caller_census(roms[1])
    assert callers == caller_census(roms[0])
    startup = read(release["own_registered_startup"])
    assert startup["candidate_sha256"] == release["candidate_sha256"] and startup["cold_boot"] and not startup["savestate"]
    assert digest(release["own_registered_startup"]) == release["own_registered_startup_sha256"]
    snapshot = startup["read_only_snapshot"]
    raw = previous.trace.read_ram(snapshot)
    code = []
    for lo, hi in SPANS:
        installed = previous.trace.code_at(arm, lo, hi)
        assert installed == previous.trace.code_at(just_before, lo, hi) == previous.trace.code_at(raw, lo, hi), hex(lo)
        code.append(dict(start=lo, end=hi, exact_hex=installed.hex()))
    focused = offline(arm, raw)
    ordinary = bound_ordinary(release)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        exact_clean_installed_resident_spans=code, aligned_callers=callers, startup_snapshot=snapshot,
        kind_one_constructor=REQUEST_CTOR, authored_callback=replacement_sources(arm),
        offline_without_scene_event_loop=focused, ordinary_scene_loop=ordinary,
        reachability_open=["Other ordinary scenes and indirect producers of fleet docking and destination values"],
        ROM_changed=False, new_editorial_credit=0))
    print("Verified the pending scene type gate, 275 supplied native request cases, and the ordinary Copenhagen producer.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("run", "verify"))
    globals()[parser.parse_args().action]()
