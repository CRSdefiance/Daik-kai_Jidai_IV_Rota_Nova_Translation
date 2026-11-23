"""Localize punctuation in the original Market Info route chart."""

from pathlib import Path
from struct import unpack_from

from scripts import register_sound_sirens_20261120 as parent
from scripts import stage_ruin_discovery_display_20261120 as runtime


batch = runtime.batch
ROOT = Path('work/town_chart_punctuation_20261120/staged_v1')
ROM, PROOF = ROOT / 'candidate.nds', ROOT / 'staging.json'
FIELDS = (
    ('DK4_TOWN_CHART_COORDINATES', 0x8D840, 0x14C28C, 16, '%s（%s%d %s%d）', '%s (%s%d %s%d)'),
    ('DK4_TOWN_CHART_UNKNOWN', 0x8D844, 0x14C29C, 8, ' ？ ', ' ? '),
    ('DK4_TOWN_CHART_SHARE', 0x8D854, 0x14C2B4, 8, '%3s％', '%3s%%'),
)


def patch(arm, source):
    assert arm[0x8D594:0x8D764] == source[0x8D594:0x8D764]
    assert arm[0x8D9D4:0x8DA20] == source[0x8D9D4:0x8DA20]
    new, rows = bytearray(arm), []
    for name, word, offset, size, jp, english in FIELDS:
        assert unpack_from('<I', arm, word) == unpack_from('<I', source, word) == (runtime.BASE + offset,)
        old, value = [text.encode(coding) for text, coding in ((jp, 'cp932'), (english, 'ascii'))]
        assert len(old) < size and len(value) < size
        before, after = old.ljust(size, b'\0'), value.ljust(size, b'\0')
        assert arm[offset:offset + size] == source[offset:offset + size] == before
        new[offset:offset + size] = after
        rows.append(dict(id=name, offset=offset, slot_bytes=size, pointer_offset=word, clean_Japanese=jp,
                         english=english, current_hex=before.hex(), target_hex=after.hex()))
    assert runtime.cache_plan(new) == runtime.cache_plan(arm)
    return bytes(new), rows


def main():
    assert not ROOT.exists()
    previous = batch.load(parent.RELEASE)
    assert parent.base.digest(parent.ROM) == previous['candidate_sha256']
    assert parent.base.digest(batch.CLEAN) == previous['clean_input_sha256']
    assert parent.base.digest(parent.base.REGISTRY) == previous['registry_sha256']
    rom, clean = map(batch.NdsImage.open, (parent.ROM, batch.CLEAN))
    arm = rom.read_file(batch.ARM)
    assert batch.digest(arm) == previous['target_ARM9_sha256']
    amended, rows = patch(arm, clean.read_file(batch.ARM))
    before = batch.files(rom)
    rom.replace_file(batch.ARM, amended)
    after = batch.files(rom)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {batch.ARM}
    target = bytes(rom.rom.save())
    rom.replace_file(batch.ARM, arm)
    assert bytes(rom.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(target)
    delta, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    runtime.make_xdelta(batch.CLEAN, ROM, delta)
    runtime.apply_xdelta(batch.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == target
    batch.write(PROOF, dict(candidate_sha256=batch.digest(target), parent_sha256=previous['candidate_sha256'],
        target_ARM9_sha256=batch.digest(amended), target_COMMON_sha256=previous['target_COMMON_sha256'],
        clean_input_sha256=previous['clean_input_sha256'], clean_input_patch_sha256=parent.base.digest(delta),
        whole_parent_inverse=True, clean_input_patch_byte_exact=True, rows=rows))
    print('Staged three original town-chart slots with an exact clean patch.')


if __name__ == '__main__':
    main()
