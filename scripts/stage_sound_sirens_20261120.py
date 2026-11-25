"""Localize the active Sirens title missed by the old SFX storage inventory."""

from pathlib import Path
from struct import unpack_from

from scripts import register_forces_chart_fields_20261120 as parent
from scripts import stage_ruin_discovery_display_20261120 as runtime


batch = runtime.batch
ROOT = Path('work/sound_sirens_20261120/staged_v1')
ROM, PROOF = ROOT / 'candidate.nds', ROOT / 'staging.json'
START, COUNT, INDEX = 0x16F158, 59, 32
SLOT, SIZE = 0x16EF8C, 12
JAPANESE, ENGLISH = 'セイレーン', 'Sirens'


def patch(arm, source):
    assert source[0x108E7C:0x108F6C] == arm[0x108E7C:0x108F6C]
    assert unpack_from('<I', arm, 0x108F60) == (runtime.BASE + START,)
    assert source[START:START + COUNT * 4] == arm[START:START + COUNT * 4]
    assert unpack_from('<I', arm, START + INDEX * 4) == (runtime.BASE + SLOT,)
    assert len(set(unpack_from(f'<{COUNT}I', arm, START))) == COUNT
    original = JAPANESE.encode('cp932').ljust(SIZE, b'\0')
    changed = ENGLISH.encode('ascii').ljust(SIZE, b'\0')
    assert source[SLOT:SLOT + SIZE] == arm[SLOT:SLOT + SIZE] == original
    amended = arm[:SLOT] + changed + arm[SLOT + SIZE:]
    assert runtime.cache_plan(amended) == runtime.cache_plan(arm)
    return amended, dict(offset=SLOT, size=SIZE, pointer_offset=START + INDEX * 4, selection_index=INDEX,
        clean_Japanese=JAPANESE, english=ENGLISH, original_hex=original.hex(), target_hex=changed.hex())


def main():
    assert not ROOT.exists()
    previous = batch.load(parent.RELEASE)
    assert parent.base.digest(parent.ROM) == previous['candidate_sha256']
    assert parent.base.digest(batch.CLEAN) == previous['clean_input_sha256']
    assert parent.base.digest(parent.base.REGISTRY) == previous['registry_sha256']
    rom, clean = map(batch.NdsImage.open, (parent.ROM, batch.CLEAN))
    raw = rom.read_file(batch.ARM)
    assert batch.digest(raw) == previous['target_ARM9_sha256']
    replacement, record = patch(raw, clean.read_file(batch.ARM))
    before = batch.files(rom)
    rom.replace_file(batch.ARM, replacement)
    after = batch.files(rom)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {batch.ARM}
    result = bytes(rom.rom.save())
    rom.replace_file(batch.ARM, raw)
    assert bytes(rom.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(result)
    delta, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    runtime.make_xdelta(batch.CLEAN, ROM, delta)
    runtime.apply_xdelta(batch.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == result
    batch.write(PROOF, dict(candidate_sha256=batch.digest(result), parent_sha256=previous['candidate_sha256'],
        target_ARM9_sha256=batch.digest(replacement), target_COMMON_sha256=previous['target_COMMON_sha256'],
        clean_input_sha256=previous['clean_input_sha256'], clean_input_patch_sha256=parent.base.digest(delta),
        whole_parent_inverse=True, clean_input_patch_byte_exact=True, slot=record))
    print('Staged Sirens in the original Sound Setup title slot.')


if __name__ == '__main__':
    main()
