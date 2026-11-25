"""Determine whether the System menu's Save-disabled scene selects the exhibition warning."""

from itertools import product
from pathlib import Path
from struct import pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from dk4tool.script.common_message_table import common_message_entries
from scripts import checkpoint_exhibition_quit_warning_20261115 as draft
from scripts import checkpoint_retail_exit_scope_20261119 as retail
from scripts import reconcile_ceuta_archived_dialogue_20261124 as continuity
from scripts import register_lisbon_purser_refit_20261124 as current
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, REGISTRY, digest, read, reference, sha256, write


OUT = continuity.OUT.with_name("exhibition_quit_scene_gate_20261124.json")
BASE, SESSION = retail.BASE, retail.SESSION
SPANS = {
    "System popup and Quit helper": (0x0203FAA0, 0x0203FC40),
    "Session getter and literal": (0x0203F0F8, 0x0203F104),
    "Two scene constructors": (0x020904CC, 0x02090540),
    "Scene dispatch and phase reset": (0x020906D8, 0x02090730),
    "Native Yes/No entry": (0x0205466C, 0x0205468C),
}
BRANCHES = {
    0x0203FAC8: ("ldr", "r0, [r0, #8]"),
    0x0203FACC: ("cmp", "r0, #0"),
    0x0203FAD8: ("ldr", "r0, [r0, #0xc]"),
    0x0203FADC: ("cmp", "r0, #1"),
    0x0203FAE4: ("streq", "r0, [sp, #0x18]"),
    0x0203FBC0: ("bl", "#0x203fc08"),
    0x0203FC18: ("ldr", "r1, [r1, #0x54]"),
    0x0203FC1C: ("cmp", "r1, #1"),
    0x0203FC28: ("ldr", "r0, [pc, #0xc]"),
    0x0203FC2C: ("bl", "#0x205466c"),
    0x020904D8: ("str", "r3, [r0, #4]"),
    0x020904DC: ("str", "r1, [r0, #8]"),
    0x02090530: ("str", "r2, [r4, #4]"),
    0x02090538: ("str", "r0, [r4, #8]"),
    0x020906E0: ("ldr", "r2, [r4, #8]"),
    0x020906E4: ("cmp", "r2, #0"),
    0x020906EC: ("cmp", "r2, #1"),
}
HEADERS = (0, 1, 0xFFFFFFFF)
PHASES = (0, 1, 2, 3, 4, 5, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF)


def lock_spans(clean, installed, resident):
    locks = {}
    for name, (lo, hi) in SPANS.items():
        sections = [blob[lo - BASE:hi - BASE] for blob in (clean, installed, resident)]
        assert sections[0] == sections[1] == sections[2] and len(sections[0]) == hi - lo, name
        locks[name] = dict(start=lo, end=hi, bytes=sections[0].hex(), sha256=sha256(sections[0]).hexdigest())
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    for pc, expected in BRANCHES.items():
        instruction, = decoder.disasm(installed[pc - BASE:pc - BASE + 4], pc)
        assert (instruction.mnemonic, instruction.op_str) == expected, (hex(pc), instruction.op_str)
    assert unpack_from("<I", installed, 0x3F100) == (SESSION,)
    assert unpack_from("<2I", installed, 0x3FC38) == (SESSION, 319)
    return locks


def cases(arm):
    cpu = retail.machine(arm)
    results = []
    for first, second, phase, accept in product(HEADERS, HEADERS, PHASES, (False, True)):
        choices = (2, 4) if phase == 1 and not accept else (2,)
        trial = retail.run_case(cpu, arm, choices, mode=phase, header=(first, second), confirm=accept)
        assert trial["COMMON_arguments"] == ([319] if phase == 1 else [])
        assert trial["final_mode"] == (1 if phase == 1 and not accept else 0)
        available = trial["menus"][0]["rows"][0]["flags"][0]
        assert available == int((first, second) != (0, 1))
        data = bytes(cpu.mem_read(SESSION + 8, 8))
        assert data == pack("<2I", first, second)
        results.append(dict(scene_type=first, scene_argument=second, phase=phase, accepted=accept,
            first_menu_save_flag=available, offered_COMMON=trial["COMMON_arguments"], resulting_phase=trial["final_mode"],
            select_again_after_decline=len(trial["menus"]) == 2))
    return results


def main():
    release = read(current.RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    startup = read(release["own_registered_startup"])
    assert digest(release["own_registered_startup"]) == release["own_registered_startup_sha256"]
    snapshot = startup["read_only_snapshot"]
    raw = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and sha256(raw).hexdigest() == snapshot["sha256"]
    clean, candidate = map(NdsImage.open, (CLEAN, current.ROM))
    old_arm, arm = (rom.read_file(current.ARM) for rom in (clean, candidate))
    stock, installed = (rom.read_file(current.COMMON) for rom in (clean, candidate))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    assert sha256(installed).hexdigest() == release["target_COMMON_sha256"]
    spans = lock_spans(old_arm, arm, raw)
    header_matrix = cases(old_arm)
    assert header_matrix == cases(arm)
    ja = common_message_entries(stock, old_arm)
    en = common_rows(installed, arm)
    runtime = RegisteredRuntime(current.RELEASE, release["own_registered_startup"], captain=startup["actual_captain_getter"])
    assert runtime.arm == arm and runtime.common == installed and runtime.raw == raw
    live_template = draft.current_template(runtime, SESSION + 0x54, en[319])
    assert bytes.fromhex(live_template["complete_template_hex"]) == b"Quit the game?\0"
    assert en[318].text != en[319].text and ja[318].text != ja[319].text
    before = read(continuity.OUT)
    archived = [284, 318, 750, 751, 752]
    assert all(continuity.valencia.review.source_ref(en[n]) == before["archived_records"][str(n)]["installed_reference"]
               for n in archived)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_input_sha256=release["clean_input_sha256"],
        authoritative_release=reference(current.RELEASE), earlier_system_review=reference(retail.OUTPUT),
        earlier_archived_inventory=reference(continuity.OUT), installed_and_resident_spans=spans,
        system_branch_instructions=BRANCHES, observed_startup_words=unpack_from("<2I", raw, SESSION + 8 - BASE),
        tested_header_partitions=dict(scene_type="zero or nonzero", scene_argument="one or other",
            quit_phase="one or other", accept="false or true"), clean_and_installed_identical_matrix=header_matrix,
        live_startup_template=live_template,
        exact_source_and_current={n: dict(source_hex=ja[n].text.hex(), clean_Japanese=ja[n].text.decode("cp932"),
            current_hex=en[n].text.hex(), english=en[n].text.decode("cp932")) for n in (318, 319)},
        disposition=dict(COMMON_318="Excluded from the in-game System Quit dispatcher in all tested branch classes.",
            other_display_paths_open=True, archived_storage_exact_on_latest=archived), ordinary_gameplay=False,
        ROM_changed=False, new_editorial_credit=0))
    print(f"Verified {len(header_matrix)} System exit cases per ROM. Only the active phase opens COMMON 319.")


if __name__ == "__main__":
    main()
