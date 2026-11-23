"""Use the registered narrow number formatter for the Continue checksum warning."""

from pathlib import Path
from struct import unpack_from

from dk4tool.patch.damaged_save_release import CAPACITY, OFFSET, formatted_suffix
from scripts import register_market_bargaining_20261120 as parent
from scripts import stage_ruin_discovery_display_20261120 as runtime


base, batch = parent.base, runtime.batch
CLEAN, ARM, COMMON = batch.CLEAN, batch.ARM, batch.COMMON
ROOT = Path("work/damaged_save_digits_20261120")
ROM, PROOF = ROOT / "Damaged_Save_Digits_RESEARCH_ONLY.nds", ROOT / "staging.json"
PRIOR = Path("translations/editorial_checkpoints/SharedText_20261110_v1/damaged_save_observed_20261115_v1.json")
CALL = 0x020EE760
CHECKSUM_AND_MESSAGE = (0xEE67C, 0xEE7E0)


def patch(current, clean):
    for lo, hi in (CHECKSUM_AND_MESSAGE, (0xEE078, 0xEE0C4), (0xEEC78, 0xEED18)):
        assert current[lo:hi] == clean[lo:hi]
    assert current[OFFSET:OFFSET + CAPACITY] == formatted_suffix().encode("ascii").ljust(CAPACITY, b"\0")
    assert unpack_from("<I", current, 0xEE7D0) == (runtime.BASE + OFFSET,)
    assert unpack_from("<I", clean, 0xEE7D0) == (runtime.BASE + OFFSET,)
    section, = [s for s in runtime.MainCodeFile(current, runtime.BASE).sections if s.ramAddress == runtime.ITCM]
    helper = bytes(section.data[runtime.HELPER - runtime.ITCM:runtime.END - runtime.ITCM])
    assert helper.hex() == batch.load(runtime.HELPER_PROOF)["helper_hex"]
    start = CALL - runtime.BASE
    assert runtime.target(current, start) == runtime.NUMBER
    changed = runtime.assemble(f"bl {runtime.HELPER}", CALL)
    assert len(changed) == 4
    target = current[:start] + changed + current[start + 4:]
    assert runtime.target(target, start) == runtime.HELPER and runtime.cache_plan(target) == runtime.cache_plan(current)
    assert target[:start] + current[start:start+4] + target[start+4:] == current
    return target, dict(address=CALL, original_number_target=runtime.NUMBER, english_number_target=runtime.HELPER,
        previous_hex=current[start:start+4].hex(), target_hex=changed.hex(), suffix_offset=OFFSET,
        source_suffix_hex=clean[OFFSET:OFFSET + CAPACITY].hex(), current_suffix_hex=current[OFFSET:OFFSET + CAPACITY].hex())


def main():
    assert not ROOT.exists()
    prior = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == prior["candidate_sha256"] and base.digest(CLEAN) == prior["clean_input_sha256"]
    assert base.digest(base.REGISTRY) == prior["registry_sha256"]
    image, clean = map(batch.NdsImage.open, (parent.ROM, CLEAN))
    arm = image.read_file(ARM)
    assert batch.digest(arm) == prior["target_ARM9_sha256"]
    target, change = patch(arm, clean.read_file(ARM))
    before = batch.files(image)
    image.replace_file(ARM, target)
    after = batch.files(image)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {ARM}
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    delta, rebuilt = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
    runtime.make_xdelta(CLEAN, ROM, delta)
    runtime.apply_xdelta(CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == candidate
    batch.write(PROOF, dict(candidate_sha256=batch.digest(candidate), parent_sha256=prior["candidate_sha256"],
        clean_input_sha256=prior["clean_input_sha256"], clean_input_patch_sha256=base.digest(delta),
        target_ARM9_sha256=batch.digest(target), target_COMMON_sha256=prior["target_COMMON_sha256"],
        changed_call=change, whole_parent_inverse=True, clean_input_patch_byte_exact=True,
        prior_damaged_save_capture=str(PRIOR), prior_damaged_save_sha256=base.digest(PRIOR)))
    print("Staged regular digits for the Continue checksum warning.")


if __name__ == "__main__":
    main()
