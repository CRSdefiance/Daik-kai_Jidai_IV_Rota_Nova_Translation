"""Trace the first ordinary Copenhagen dock request, from port selection to the fleet byte."""

from argparse import ArgumentParser
from struct import iter_unpack
from types import FunctionType

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from PIL import ImageChops

from scripts import observe_copenhagen_dock_input_20261124 as previous
from scripts import register_riga_recruitment_20261124 as current
from scripts.reconcile_fleet_force_dock_20261124 import trace
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write

ROOT = current.ROM.parent.with_name("editorial_20261124_copenhagen_dock_producer")
RUN = ROOT / "landing"
OUT = previous.OUT.with_name("copenhagen_dock_producer_20261124.json")
playback = previous.playback
SELECT, CHOSEN, EDGE = 0x02078E78, 0x020790F8, 0x02078174
INPUT = 0x02021D2C
VALUES = previous.VALUES | {SELECT: 4, CHOSEN: 5, EDGE: 5, INPUT: 9}
MAKE_PORT_REQUEST = 0x020904CC
MAKERS = {
    0x02029494: "Copies the current fleet docking byte. An at-sea result reads the same fleet's saved byte.",
    EDGE: "Takes the route endpoint returned by the active fleet route object's virtual method.",
    CHOSEN: "Takes the nearby port selector's result after the user accepts the Dock prompt.",
    0x020902B8: "Copies the current scene request object's value.",
    0x020912E8: "Copies the current dock index while initializing the scene.",
}
SPANS = ((0x02029434, 0x020294A4), (0x02034674, 0x02034688), (0x02078100, 0x02078144),
         (0x02078168, 0x02078184), (0x02078C60, 0x02078E7C), (0x02079074, 0x020790AC),
         (0x020790EC, 0x02079108), (0x02090298, 0x020902BC), (0x020903AC, 0x020903B4),
         (0x020904CC, 0x02090514), (0x020912C0, 0x020912F8), (0x02021D0C, 0x02021E20),
         (0x02090B0C, 0x02090B90))


def run():
    assert digest(REGISTRY) == read(current.RELEASE)["registry_sha256"]
    observer = FunctionType(previous.observer.__code__, vars(previous) | dict(VALUES=VALUES))
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=previous.original.schedule,
                                 observer=observer, FOCUS={49, 65}, __file__=__file__)
    FunctionType(playback.main.__code__, scope)("landing")


def direct_makers(image):
    found, pointers = [], []
    for component, base, data in trace.loaded_components(image):
        for i, (word,) in enumerate(iter_unpack("<I", data[:len(data) & ~3])):
            pc = base + 4 * i
            if trace.direct_bl_target(word, pc) == MAKE_PORT_REQUEST:
                found.append((component, pc))
            if word in (MAKE_PORT_REQUEST, MAKE_PORT_REQUEST | 1):
                pointers.append((component, pc, word))
    assert found == [("arm9_section_0", pc) for pc in sorted(MAKERS)] and not pointers
    return found


def audit_code(release):
    clean, active = map(NdsImage.open, (CLEAN, current.ROM))
    before, arm = (img.read_file(current.ARM) for img in (clean, active))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    boot = read(release["own_registered_startup"])
    snap = boot["read_only_snapshot"]
    raw = trace.read_ram(snap)
    assert boot["candidate_sha256"] == release["candidate_sha256"] and boot["cold_boot"] and not boot["savestate"]
    bindings = []
    for start, end in SPANS:
        installed = trace.code_at(arm, start, end)
        assert installed == trace.code_at(before, start, end) == trace.code_at(raw, start, end), hex(start)
        bindings.append(dict(start=start, end=end, exact_hex=installed.hex()))
    assert direct_makers(clean) == direct_makers(active)
    # R4 starts at zero, advances by one and exits on 114. Its only local
    # return-slot store uses r4, while the initial value is 115 (no port).
    expected = {
        0x02078CA8: "mov r4, #0", 0x02078CB0: "mov r0, #0x73", 0x02078CB4: "cmp r4, #0x72",
        0x02078CB8: "str r0, [sp]", 0x02078E64: "strls r4, [sp]", 0x02078E68: "add r4, r4, #1",
        0x02078E6C: "cmp r4, #0x72", 0x02078E74: "ldr r0, [sp]",
        0x02079098: "mov r5, r0", 0x0207909C: "cmp r5, #0x73",
        0x020790F0: "mov r1, r5", 0x020904DC: "str r1, [r0, #8]",
        0x02021D24: "ldr r5, [r3, #8]", 0x02021D2C: "str r5, [r1, #0x43c]",
        0x02021DE0: "ldr r1, [r0, #0x43c]", 0x02021DE4: "str r1, [r5, #8]",
    }
    disasm = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for pc, op in expected.items():
        insn, = disasm.disasm(trace.code_at(arm, pc, pc + 4), pc)
        assert f"{insn.mnemonic} {insn.op_str}" == op
    return dict(spans=bindings, original_type_one_constructors=MAKERS, original_instructions=expected,
                nearby_selector_ports=[0, 113], nearby_selector_no_target=115, original_startup_snapshot=snap)


def verify():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    report_ref, requests_ref = RUN / "capture/capture_report.json", RUN / "requests.json"
    report, trace_report = map(read, (report_ref, requests_ref))
    historic = read(previous.OUT)
    old_report = read(historic["current_capture"]["path"])
    assert digest(historic["current_capture"]["path"]) == historic["current_capture"]["sha256"]
    assert report["ROM_sha256"] == release["candidate_sha256"] and report["cold_boot"] and not report["savestate_loaded"]
    assert not report["callback_errors"] and not any(v for key, v in report.items() if key.startswith("synthetic_"))
    assert trace_report["all_host_slots_restored_and_core_file_exact"] and not trace_report["errors"] and not trace_report["mismatches"]
    schedule, frames, end, _, donor = previous.original.schedule("landing")
    assert report["frames"] == end and report["scripted_input_schedule"] == old_report["scripted_input_schedule"] == schedule
    assert report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    assert digest(donor["source"]) == report["battery_save_preloaded"]["source_sha256"] == historic["original_battery_save"]["sha256"]
    panel = previous.baseline.panels
    left, right = [panel.shots(replay, "_cold_boot.png") for replay in (old_report, report)]
    assert all(ImageChops.difference(panel.picture(left[n]), panel.picture(right[n])).getbbox() is None for n in frames)
    all_rows = trace_report["rows"]
    chain = []
    for pc, old_key in ((previous.RETURN, "native_return"), (previous.PENDING, "internal_pending_store"),
                        (previous.ACCEPT, "accepted_port"), (previous.DOCK, "written_dock")):
        matched, = [row for row in all_rows if row["PC"] == pc and row == historic[old_key]]
        chain.append(matched)
    first = chain[0]["frame"]
    raw, = [row for row in all_rows if row["PC"] == INPUT and row["frame"] == first and row["value"] == 9]
    constructors = [row for row in all_rows if row["PC"] in (CHOSEN, EDGE) and row["value"] == 9 and row["frame"] <= first]
    ingress = constructors[-1]
    assert 4001 <= ingress["frame"] <= first and raw["frame"] == first
    selector = [row for row in all_rows if row["PC"] == SELECT and row["value"] == 9 and row["frame"] <= ingress["frame"]]
    if ingress["PC"] == CHOSEN:
        assert selector
    code = audit_code(release)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        ordinary_gameplay=True, inherited_controller=reference(previous.OUT), replay=reference(report_ref),
        requests=reference(requests_ref), matching_gameplay_holds=list(frames),
        closest_port_selection=selector[-1] if selector else None, first_accepted_request=ingress,
        native_request_input=raw, inherited_docking_chain=chain, offline_code_range_proof=code,
        ordinary_Missionary_observed=False, ROM_changed=False, new_editorial_credit=0))
    print(f"Verified a slot 9 request from native caller {ingress['PC']:#010x} through the full Copenhagen docking chain.")


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("run", "verify"))
    globals()[cli.parse_args().action]()