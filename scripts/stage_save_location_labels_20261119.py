"""Stage the Save/Load location separator and a clearer Load heading."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from scripts import register_save_dialogue_followup_20261119 as parent
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

base, native = parent.base, parent.native
ARM, COMMON, CLEAN = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN
GATES = parent.stage.GATES
ROOT = Path("work/save_location_labels_20261119")
ROM = ROOT / "Save_Location_Labels_RESEARCH_ONLY.nds"
PROOF = ROOT / "staged.json"
LEAD = parent.stage.ROOT / "at_sea_spacing_lead.json"
SOURCE = parent.stage.SOURCE
DETAILS = (
    ("DK4_SAVE_AT_SEA", 0xEF6C0, " At Sea", "At Sea",
     "Assembled after the sea area on an occupied Save row.",
     "Keep the accurate At Sea label and add the separator at the same boundary used by Docked."),
    ("DK4_LOAD_AT_SEA", 0xEFF3C, " At Sea", "At Sea",
     "Assembled after the sea area on an occupied Load row.",
     "Keep the accurate At Sea label and use the same separator as the Save list."),
    ("DK4_SAVE_DOCKED", 0xEF6C4, None, "Docked",
     "Assembled after the port on an occupied Save row.",
     "Docked states the ship's status directly. The existing leading separator keeps it clear of the port name."),
    ("DK4_LOAD_DOCKED", 0xEFF40, None, "Docked",
     "Assembled after the port on an occupied Load row.",
     "Docked matches the Save list and already has the correct boundary after the port name."),
    ("DK4_SAVE_SELECT_TITLE", 0xEF6B0, None, "Select a save slot.",
     "Displayed over the Save slot list before the player chooses a destination.",
     "Keep the concise instruction. The user selects a slot, which can be empty or occupied."),
    ("DK4_LOAD_SELECT_TITLE", 0xEF6B4, "Select a save to load.", "Select a save to load.",
     "Displayed over the Load slot list before the player chooses saved progress.",
     "Name the saved game directly in natural English and keep the original instruction to select one."),
)
LOCATIONS = ((0xEF560, 0xEF5AC), (0xEFEB4, 0xEFF00))


def digest(raw):
    return sha256(raw).hexdigest()


def rendered_arguments(runtime, case, region):
    entry, end = LOCATIONS[case]
    cpu, _, provider = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R0, region & 0xFFFFFFFF)
    pieces = []

    def capture(u, pc, size, _):
        at = u.reg_read(UC_ARM_REG_R1)
        assert BASE <= at < BASE + len(runtime.arm)
        data = bytes(u.mem_read(at, 40)).split(b"\0", 1)[0]
        assert data and data.isascii()
        pieces.append((at, data.decode("ascii")))
        # Stop at the painter's input boundary, then let the selector continue.
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    cpu.hook_add(UC_HOOK_CODE, capture, begin=0x020D5404, end=0x020D5404)
    cpu.emu_start(BASE + entry, BASE + end, count=256)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE + end
    assert not provider.reads and not provider.opens
    runtime.calls.clear()
    return pieces


def main():
    assert not ROOT.exists()
    previous = base.load(parent.RELEASE)
    runtime = RegisteredRuntime(parent.RELEASE, previous["own_registered_startup"], captain=3)
    assert base.digest(base.REGISTRY) == previous["registry_sha256"]
    assert base.digest(CLEAN) == previous["clean_input_sha256"]
    lead = base.load(LEAD)
    assert lead["candidate_sha256"] == previous["candidate_sha256"]
    assert base.digest(lead["save_slot_live_capture"]["path"]) == lead["save_slot_live_capture"]["PNG_sha256"]
    clean = base.NdsImage.open(CLEAN).read_file(ARM)
    arm = runtime.arm
    for start, stop in ((0x945B4, 0x945DC), (0xEF458, 0xEF478), *LOCATIONS):
        assert clean[start:stop] == arm[start:stop]
    source = {r["id"]:r for r in base.load(SOURCE)["records"]}
    records = []
    changed = bytearray(arm)
    owned = {}

    def row(key, clean_offset, original, offset, allocation, pointer, replacement, prose, context, note, decision):
        current = arm[offset:offset+allocation]
        assert current.isascii() and b"\0" in current
        new = current if replacement is None else replacement.encode("ascii").ljust(allocation, b"\0")
        assert len(new) == allocation
        if new != current:
            assert allocation not in (0, 1) and new.endswith(b"\0")
            assert offset not in owned
            changed[offset:offset+allocation] = new
            owned[offset] = allocation
        source_ref = dict(offset=clean_offset, allocation=len(original), pointer_field=BASE+pointer, ARM9_sha256=digest(clean))
        current_ref = dict(offset=offset, allocation=allocation, pointer_field=BASE+pointer, ARM9_sha256=digest(arm))
        assert original == clean[clean_offset:clean_offset+len(original)]
        records.append(dict(id=key, file_path=ARM, speaker="Save and Load interface", context=context,
            source_Japanese=original.split(b"\0",1)[0].decode("cp932"),
            source_meaning=prose if not key.endswith("SELECT_TITLE") else "Choose the slot or saved game for this operation.",
            localization_note=note, decision=decision, english=prose, source_reference=source_ref,
            current_reference=current_ref, source_hex=original.hex(), current_hex=current.hex(), staged_hex=new.hex(),
            runtime_substitutions=[], review=dict.fromkeys(GATES, True) | {"formatting":False}))

    for key, ptr, replacement, prose, context, note in DETAILS:
        history = source[key]
        at = history["offset"]
        original = bytes.fromhex(history["source_hex"])
        assert unpack_from("<I",arm,ptr)[0] == unpack_from("<I",clean,ptr)[0] == BASE+at
        current = arm[at:arm.index(0,at)]
        assert current.decode("ascii") == history["english"]
        span = max(len(current), len(replacement or "")) + 1
        assert span <= len(original) and arm[at+len(current):at+span] == bytes(span-len(current))
        row(key,at,original,at,span,ptr,replacement,prose,context,note,
            "retention" if replacement is None else "spacing" if key.endswith("AT_SEA") else "revision")

    table = unpack_from("<I",arm,0x945D8)[0] - BASE
    assert table == unpack_from("<I",clean,0x945D8)[0] - BASE
    pointer = table + 4*52
    src_offset = unpack_from("<I",clean,pointer)[0] - BASE
    installed = unpack_from("<I",arm,pointer)[0] - BASE
    old_label = arm[installed:arm.index(0,installed)+1]
    assert old_label == b"SE Asia \0"
    assert [n for n in range(0,len(arm)-3,4) if unpack_from("<I",arm,n)[0]==BASE+installed] == [pointer]
    original = clean[src_offset:clean.index(0,src_offset)+1]
    row("ARM9_SE_ASIA_REGION_NAME",src_offset,original,installed,len(old_label),pointer,"SE Asia","SE Asia",
        "The Southeast Asia region label returned by the region lookup used by both slot lists.",
        "Keep the established abbreviation. Give the status suffix responsibility for the separator, as with the six other stock regions.",
        "spacing")
    final = bytes(changed)
    staged = with_components(runtime,final,runtime.common)
    ram = bytearray(staged.raw)
    for at, span in owned.items():
        assert ram[at:at+span] == arm[at:at+span]
        ram[at:at+span] = final[at:at+span]
    staged.raw = bytes(ram)
    output = []
    for case in range(2):
        for code in [*range(7),7,65535]:
            old = rendered_arguments(runtime,case,code)
            new = rendered_arguments(staged,case,code)
            assert [address for address,_ in old] == [address for address,_ in new]
            assert new[-1][1] == " At Sea"
            if code < 7:
                assert len(new) == 2 and new[0][1] == old[0][1].strip()
                composed = "".join(t for _,t in new)
                assert composed == new[0][1] + " At Sea"
            else:
                assert len(new) == 1 and new[0][1].strip() == "At Sea"
                composed = new[0][1]
            width = len(composed) * 6
            assert width <= 96 and all(32 <= ord(ch) <= 126 for ch in composed)
            output.append(dict(consumer=["Save","Load"][case],region=code,previous_arguments=old,
                staged_arguments=new,combined=composed,maximum_width_px=width,
                original_region_and_suffix_selectors_executed=True,painter_arguments_observed_offline=True))
    for at, span in owned.items():
        changed[at:at+span] = arm[at:at+span]
    assert bytes(changed) == arm and len(owned) == 4
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM,final)
    candidate = bytes(image.rom.save())
    image.replace_file(ARM,arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    base.save(PROOF,dict(candidate=str(ROM),candidate_sha256=digest(candidate),parent_sha256=previous["candidate_sha256"],
        target_ARM9_sha256=digest(final),target_COMMON_sha256=previous["target_COMMON_sha256"],
        clean_input_sha256=previous["clean_input_sha256"],translation_policy="natural-dialogue-v2",
        target_locale="en-US",encoder="dialogue-relocatable-v1",review_gates=GATES,records=records,
        entire_parent_inverse=True,slots_changed=owned,stock_and_fallback_painter_arguments=output,
        lead=dict(path=str(LEAD),sha256=base.digest(LEAD))))
    print("Four localized fields staged. All seven stock sea areas and the unnamed fallback verified at both native painter inputs.")


if __name__ == "__main__":
    main()

