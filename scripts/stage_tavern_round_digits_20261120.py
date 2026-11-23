"""Use the registered narrow digit helper for the original Tavern round price."""

from pathlib import Path
from struct import unpack_from

from scripts import check_amsterdam_tavern_followup_20261120 as tavern
from scripts import register_hamburg_ceramics_cross_route_20261120 as parent
from scripts import stage_ruin_discovery_display_20261120 as runtime


base, batch = parent.base, runtime.batch
CLEAN, ARM, COMMON = batch.CLEAN, batch.ARM, batch.COMMON
ROOT = Path("work/tavern_round_digits_20261120_v2")
ROM, PROOF = ROOT / "Tavern_Round_Digits_RESEARCH_ONLY.nds", ROOT / "staging.json"
CALL, WRAPPER = 0x02058388, 0x02053CB0
VOICE_TABLE = 0x118400
TABLE = (852, -1, 853, 854, 855, 856, 857, 858)
REVISIONS = {
    853: b" Looks like it'll cost %s gold. Okay?",
    854: b" That'll cost %s gold. All right?",
    856: b" It looks like we'll need %s gold. Is that all right?",
    857: b" Looks like it'll cost %s gold. Sound okay?",
}


def deploy_text(common, arm):
    entries = batch.owned_entries(common, arm, batch.digest(arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    assert all(entries[n].text.startswith(b" ") and entries[n].text.count(b"%s") == 1 for n in REVISIONS)
    return batch.owned_deployment(common, arm, entries, REVISIONS)


def patch(current, clean):
    for lo, hi in ((0x58374, 0x58404), (0x53CB0, 0x53D48), (0x53F4C, 0x53F9C),
                   (VOICE_TABLE, VOICE_TABLE + 32)):
        assert current[lo:hi] == clean[lo:hi]
    assert unpack_from("<8i", current, VOICE_TABLE) == TABLE
    assert unpack_from("<I", current, 0x585FC) == (runtime.BASE + VOICE_TABLE,)
    assert runtime.target(current, 0x58398) == WRAPPER
    section, = [s for s in runtime.MainCodeFile(current, runtime.BASE).sections if s.ramAddress == runtime.ITCM]
    helper = bytes(section.data[runtime.HELPER - runtime.ITCM:runtime.END - runtime.ITCM])
    assert helper.hex() == batch.load(runtime.HELPER_PROOF)["helper_hex"]
    offset = CALL - runtime.BASE
    assert runtime.target(current, offset) == runtime.NUMBER
    encoded = runtime.assemble(f"bl {runtime.HELPER}", CALL)
    assert len(encoded) == 4
    target = current[:offset] + encoded + current[offset+4:]
    assert runtime.target(target, offset) == runtime.HELPER
    assert target[:offset] + current[offset:offset+4] + target[offset+4:] == current
    assert runtime.cache_plan(target) == runtime.cache_plan(current)
    return target, dict(address=CALL, original_number_target=runtime.NUMBER, english_number_target=runtime.HELPER,
        previous_hex=current[offset:offset+4].hex(), target_hex=encoded.hex(), dialogue_wrapper=WRAPPER,
        voice_table_address=runtime.BASE + VOICE_TABLE, original_voice_table=list(TABLE))


def main():
    assert not ROOT.exists()
    previous = base.load(parent.RELEASE)
    evidence = base.load(tavern.OUTPUT)
    assert base.digest(parent.ROM) == previous["candidate_sha256"]
    assert base.digest(base.REGISTRY) == previous["registry_sha256"]
    assert base.digest(CLEAN) == previous["clean_input_sha256"]
    assert evidence["candidate_sha256"] == previous["predecessor"]["candidate_sha256"]
    assert evidence["price_call"] == CALL and evidence["dialogue_wrapper"] == WRAPPER
    clean, image = map(base.NdsImage.open, (CLEAN, parent.ROM))
    arm = image.read_file(ARM)
    assert batch.digest(arm) == previous["target_ARM9_sha256"]
    target, call = patch(arm, clean.read_file(ARM))
    before = batch.files(image)
    deployed, _, allocations = deploy_text(before[COMMON], target)
    image.replace_file(ARM, target)
    image.replace_file(COMMON, deployed)
    after = batch.files(image)
    assert before.keys() == after.keys() and {n for n in before if before[n] != after[n]} == {ARM, COMMON}
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, before[COMMON])
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    delta, rebuilt = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
    runtime.make_xdelta(CLEAN, ROM, delta)
    runtime.apply_xdelta(CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == candidate
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), parent_sha256=previous["candidate_sha256"],
        clean_input_sha256=previous["clean_input_sha256"], clean_input_patch_sha256=base.digest(delta),
        target_ARM9_sha256=batch.digest(target), target_COMMON_sha256=batch.digest(deployed), changed_call=call,
        COMMON_allocations=allocations,
        whole_parent_inverse=True, clean_input_patch_byte_exact=True, prior_gameplay=str(tavern.OUTPUT),
        prior_gameplay_sha256=base.digest(tavern.OUTPUT)))
    print("Staged regular-width numbers for the original Tavern price voices.")


if __name__ == "__main__":
    main()
