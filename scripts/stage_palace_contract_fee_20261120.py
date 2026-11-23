"""Use regular-width digits in both original Palace minimum-fee offers."""

from pathlib import Path
from struct import unpack_from

from scripts import register_ruin_discovery_display_20261120 as parent
from scripts import stage_ruin_discovery_display_20261120 as ruin


batch = ruin.batch
ROOT = Path('work/palace_contract_fee_20261120/staged_v1')
ROM, PROOF = ROOT / 'candidate.nds', ROOT / 'staging.json'
CALLS = {1149: (0x0205E06C, 0x5E1D8), 1156: (0x0205E098, 0x5E1E0)}


def patch(arm, source):
    assert arm[0x5E010:0x5E1F4] == source[0x5E010:0x5E1F4]
    assert ruin.cache_plan(arm)
    section, = [s for s in ruin.MainCodeFile(arm, ruin.BASE).sections if s.ramAddress == ruin.ITCM]
    assert bytes(section.data[ruin.HELPER - ruin.ITCM:ruin.END - ruin.ITCM]) == bytes.fromhex(
        batch.load(ruin.HELPER_PROOF)['helper_hex'])
    result, receipts = bytearray(arm), []
    for message, (address, literal) in CALLS.items():
        at = address - ruin.BASE
        assert ruin.target(arm, at) == ruin.NUMBER
        assert unpack_from('<I', source, literal)[0] == message
        assert unpack_from('<I', arm, at - 4)[0] == 0xE1A00006  # Preserve the original minimum fee in r6.
        assert unpack_from('<I', arm, at + 4)[0] == 0xE1A02000  # Same argument slot to original quote.
        assert ruin.target(arm, at + 16) == 0x02053FE4
        new = ruin.assemble(f'bl {ruin.HELPER}', address)
        assert len(new) == 4
        result[at:at + 4] = new
        assert ruin.target(result, at) == ruin.HELPER
        receipts.append(dict(message_ID=message, address=address, message_literal_offset=literal,
                             original_full_width_target=ruin.NUMBER, regular_width_target=ruin.HELPER,
                             before=arm[at:at + 4].hex(), after=new.hex()))
    assert ruin.cache_plan(result) == ruin.cache_plan(arm)
    return bytes(result), receipts


def main():
    assert not ROOT.exists()
    release = batch.load(parent.RELEASE)
    assert parent.base.digest(parent.ROM) == release['candidate_sha256']
    assert parent.base.digest(batch.CLEAN) == release['clean_input_sha256']
    assert parent.base.digest(parent.base.REGISTRY) == release['registry_sha256']
    prior, clean = map(batch.NdsImage.open, (parent.ROM, batch.CLEAN))
    original = prior.read_file(batch.ARM)
    arm, sites = patch(original, clean.read_file(batch.ARM))
    assert batch.digest(original) == release['target_ARM9_sha256']
    before = batch.files(prior)
    prior.replace_file(batch.ARM, arm)
    after = batch.files(prior)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {batch.ARM}
    candidate = bytes(prior.rom.save())
    prior.replace_file(batch.ARM, original)
    assert bytes(prior.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(candidate)
    delta, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    ruin.make_xdelta(batch.CLEAN, ROM, delta)
    ruin.apply_xdelta(batch.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == candidate
    finding = parent.VERIFY / parent.game.PALACE.name
    batch.write(PROOF, dict(candidate_sha256=batch.digest(candidate), parent_sha256=release['candidate_sha256'],
        clean_input_sha256=release['clean_input_sha256'], clean_input_patch_sha256=parent.base.digest(delta),
        target_ARM9_sha256=batch.digest(arm), target_COMMON_sha256=release['target_COMMON_sha256'],
        observed_display_defect=dict(path=str(finding), sha256=parent.base.digest(finding)),
        native_calls=sites, exact_parent_inverse=True, clean_input_patch_byte_exact=True))
    print('Staged both Palace quote branches with the original calculation and payment path preserved.')


if __name__ == '__main__':
    main()
