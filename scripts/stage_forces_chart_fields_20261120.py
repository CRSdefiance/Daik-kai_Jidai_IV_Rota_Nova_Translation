"""Localize the chart's no-home fallback and normalize its field punctuation."""

from pathlib import Path
from struct import unpack_from

from scripts import register_palace_contract_fee_20261120 as parent
from scripts import stage_ruin_discovery_display_20261120 as runtime


batch = runtime.batch
ROOT = Path('work/forces_chart_fields_20261120/staged_v1')
ROM, PROOF = ROOT / 'candidate.nds', ROOT / 'staging.json'
# Original entries for the leader, level, funds, power and hometown question marks
# are independent chart states. They happen to contain the same characters.
FIELDS = (
    ('UNKNOWN_LEADER', 0x8D7D0, 0x14C1E4, 4, '？', '?'),
    ('UNKNOWN_LEVEL', 0x8D7D8, 0x14C1F4, 4, '？', '?'),
    ('UNKNOWN_FUNDS', 0x8D7E4, 0x14C20C, 4, '？', '?'),
    ('UNKNOWN_POWER', 0x8D7EC, 0x14C214, 4, '？', '?'),
    ('REGIONAL_POWER', 0x8D7F0, 0x14C218, 16, '%d（%s：%d）', '%d (%s: %d)'),
    ('UNKNOWN_HOME', 0x8D7F8, 0x14C22C, 4, '？', '?'),
    ('NO_HOME', 0x8D7FC, 0x14C230, 8, '無し', 'None'),
    ('SELF_TIES', 0x8D800, 0x14C238, 4, '－', '-'),
)


def patch(arm, source):
    assert source[0x8CEE0:0x8D2F8] == arm[0x8CEE0:0x8D2F8]
    assert source[0x3CBFC:0x3CC80] == arm[0x3CBFC:0x3CC80]
    assert runtime.cache_plan(arm)
    output, records = bytearray(arm), []
    for identifier, literal, offset, length, jp, english in FIELDS:
        original = jp.encode('cp932')
        new = english.encode('ascii')
        assert len(original) < length and len(new) < length and original.count(b'%') == new.count(b'%')
        if identifier == 'REGIONAL_POWER':
            assert original.count(b'%d') == new.count(b'%d') == 2 and original.count(b'%s') == new.count(b'%s') == 1
        before, after = original.ljust(length, b'\0'), new.ljust(length, b'\0')
        assert source[offset:offset + length] == arm[offset:offset + length] == before
        assert unpack_from('<I', source, literal) == unpack_from('<I', arm, literal) == (runtime.BASE + offset,)
        output[offset:offset + length] = after
        records.append(dict(id=f'DK4_FORCES_{identifier}', literal_offset=literal, offset=offset, slot_bytes=length,
                            clean_Japanese=jp, english=english, source_and_current_hex=before.hex(), target_hex=after.hex()))
    assert runtime.cache_plan(output) == runtime.cache_plan(arm)
    return bytes(output), records


def main():
    assert not ROOT.exists()
    release = batch.load(parent.RELEASE)
    assert parent.base.digest(parent.ROM) == release['candidate_sha256']
    assert parent.base.digest(batch.CLEAN) == release['clean_input_sha256']
    assert parent.base.digest(parent.base.REGISTRY) == release['registry_sha256']
    prior, clean = map(batch.NdsImage.open, (parent.ROM, batch.CLEAN))
    original = prior.read_file(batch.ARM)
    assert batch.digest(original) == release['target_ARM9_sha256']
    arm, rows = patch(original, clean.read_file(batch.ARM))
    before = batch.files(prior)
    prior.replace_file(batch.ARM, arm)
    after = batch.files(prior)
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == {batch.ARM}
    candidate = bytes(prior.rom.save())
    prior.replace_file(batch.ARM, original)
    assert bytes(prior.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(candidate)
    delta, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    runtime.make_xdelta(batch.CLEAN, ROM, delta)
    runtime.apply_xdelta(batch.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == candidate
    batch.write(PROOF, dict(candidate_sha256=batch.digest(candidate), parent_sha256=release['candidate_sha256'],
        target_ARM9_sha256=batch.digest(arm), clean_input_sha256=release['clean_input_sha256'],
        clean_input_patch_sha256=parent.base.digest(delta), rows=rows, whole_parent_inverse=True,
        clean_input_patch_byte_exact=True, target_COMMON_sha256=release['target_COMMON_sha256']))
    print('Staged eight exact Forces chart slots with fixed pointers and a byte-exact clean patch.')


if __name__ == '__main__':
    main()
