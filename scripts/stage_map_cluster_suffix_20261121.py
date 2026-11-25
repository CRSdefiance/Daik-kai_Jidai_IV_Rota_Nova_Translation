"""Prepare the source-bound World Map clustered-marker wording."""

from pathlib import Path
from struct import pack, unpack_from

from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES
from scripts import observe_regional_finance_text_20261121 as context
from scripts.checkpoint_pending_shared_native_20261115 import components, find
from scripts.execute_map_entity_tooltip_copy import ACTOR, ARGUMENTS, BASE, STACK, STOP, machine_for
from scripts.probe_button_prompt_native import call


parent = context.current
base, native = parent.base, parent.native
ROOT = Path("work/map_cluster_suffix_20261121")
ROM = ROOT / "World_Map_Cluster_Suffix_STAGED.nds"
PROOF = ROOT / "stored_proof.json"
OFFSET, CAPACITY, LITERAL = 0x14C0E4, 8, 0x8BEA8
SELECTOR, BUFFER, NAME_GETTER = 0x8BDEC, 0x022A44EC, ACTOR + 0x80
SUFFIX = b" + more"


def native_name_test(arm, name, grouped, suffix):
    cpu = machine_for(arm)
    cpu.mem_write(ACTOR, pack("<I", ACTOR + 0x40))
    cpu.mem_write(ACTOR + 0x48, pack("<I", NAME_GETTER))
    cpu.mem_write(ARGUMENTS, name + b"\0")
    output = BUFFER + 12
    cpu.mem_write(BUFFER, bytes(12) + b"\xa5" * 128)
    selected = []

    def get_name(machine, pc, _size, _data):
        assert pc == NAME_GETTER and machine.reg_read(UC_ARM_REG_R0) == ACTOR
        selected.append(pc)
        machine.reg_write(UC_ARM_REG_R0, ARGUMENTS)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    cpu.hook_add(UC_HOOK_CODE, get_name, begin=NAME_GETTER, end=NAME_GETTER)
    addresses = call(cpu, SELECTOR, (0, ACTOR, 0, int(grouped)))
    assert selected == [NAME_GETTER] and 0x0208BE28 in addresses and 0x020ABFCC in addresses
    assert cpu.reg_read(UC_ARM_REG_SP) == STACK and cpu.reg_read(UC_ARM_REG_PC) == STOP
    assert cpu.reg_read(UC_ARM_REG_R0) == output
    expected = name + (suffix if grouped else b"") + b"\0"
    assert bytes(cpu.mem_read(BUFFER, 12)) == bytes(8) + pack("<I", 1)
    assert bytes(cpu.mem_read(output, 128)) == expected + b"\xa5" * (128-len(expected))
    return dict(grouped=grouped, supplied_name_hex=name.hex(), expected_exact=expected.hex(),
                complete_native_selector_and_formatter=True)


def main():
    assert not ROOT.exists()
    review, release, ledger = map(base.load, (context.CHECKPOINT, parent.RELEASE, base.LEDGER))
    candidate = release["candidate_sha256"]
    assert candidate == base.digest(parent.ROM) == ledger["current_integrated_candidate"]["sha256"] == review["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    visual = review["ordinary_regional_replay"]["view_frame"]
    assert base.digest(visual["path"]) == visual["sha256"]
    clean, original, staged = map(base.NdsImage.open, (native.CLEAN, parent.ROM, parent.ROM))
    prior = native.files(original)
    source, installed = clean.read_file(native.ARM), prior[native.ARM]
    assert native.digest(installed) == release["target_ARM9_sha256"]
    assert source[OFFSET:OFFSET + CAPACITY] == 'など'.encode('cp932').ljust(CAPACITY, b"\0")
    assert installed[OFFSET:OFFSET + CAPACITY] == b" etc.\0\0\0"
    assert source[SELECTOR:LITERAL + 16] == installed[SELECTOR:LITERAL + 16]
    assert unpack_from("<4I", installed, LITERAL) == (BASE + OFFSET, BASE + OFFSET + CAPACITY, BUFFER, BASE + OFFSET + 12)
    assert source[OFFSET + CAPACITY:OFFSET + 16] == installed[OFFSET + CAPACITY:OFFSET + 16] == b"\0\0\0\0%s%s"
    for image in (clean, original):
        hits = [(label, address + i, displacement) for displacement in range(CAPACITY)
                for label, address, part in components(image.rom)
                for i in find(part, pack("<I", BASE + OFFSET + displacement)) if i % 4 == 0]
        assert hits == [("ARM9 section 0", BASE + LITERAL, 0)]

    new = SUFFIX + b"\0"
    assert len(new) == CAPACITY
    arm = installed[:OFFSET] + new + installed[OFFSET + CAPACITY:]
    assert bytes(MainCodeFile(arm, BASE).save()) == arm
    assert arm[:OFFSET] == installed[:OFFSET] and arm[OFFSET + CAPACITY:] == installed[OFFSET + CAPACITY:]
    manifest = base.load(parent.MANIFEST)
    assert base.digest(parent.MANIFEST) == release["manifest_sha256"]
    assert manifest["checks"]["registered_runtime_bounds_and_complete_parent_target_inverse"]
    names = (b"A", b"Manuel Fleet", b"Bergstrom Fleet", b"ABCDEFGHIJKLMNOP Fleet", b"Port of the Longest Name")
    cases = [native_name_test(a, name, grouped, suffix)
             for a, suffix in ((installed, b" etc."), (arm, SUFFIX))
             for grouped in (False, True) for name in names]
    staged.replace_file(native.ARM, arm)
    after = native.files(staged)
    assert prior.keys() == after.keys() and {p for p in prior if prior[p] != after[p]} == {native.ARM}
    output = bytes(staged.rom.save())
    staged.replace_file(native.ARM, installed)
    assert bytes(staged.rom.save()) == parent.ROM.read_bytes()

    record = dict(id="DK4_MAP_MULTIPLE_CITIES", file_path=native.ARM, speaker="World Map marker",
        context="The map shows one name for a cluster. A plain marker still shows just its name.",
        source_meaning="The named marker has other entries at the same point.",
        english="+ more", stored_suffix=SUFFIX.decode('ascii'), previous_english="etc.",
        localization_note="Keep the name visible and use a short map label to signal additional entries without claiming a count or type.",
        source_reference=dict(offset=OFFSET, pointer_literal=LITERAL, exact_hex=source[OFFSET:OFFSET + CAPACITY].hex()),
        current_reference=dict(offset=OFFSET, pointer_literal=LITERAL, exact_hex=installed[OFFSET:OFFSET + CAPACITY].hex()),
        staged_reference=dict(offset=OFFSET, pointer_literal=LITERAL, exact_hex=new.hex()),
        review=dict.fromkeys(sorted(REQUIRED_REVIEW_GATES), True) | {"formatting": False})
    ROOT.mkdir()
    ROM.write_bytes(output)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=candidate,
        native_cases=cases, ARM9_sha256=native.digest(arm), inverse_verified=True,
        translation_policy="natural-dialogue-v2", target_locale="en-US", encoder="dialogue-relocatable-v1",
        review_gates=sorted(REQUIRED_REVIEW_GATES), records=[record], source_checkpoint=str(context.CHECKPOINT),
        native_raster_and_revised_gameplay_pending=True))
    print("Staged one map suffix. The native selector and formatter passed 20 complete field cases.")


if __name__ == "__main__":
    main()
