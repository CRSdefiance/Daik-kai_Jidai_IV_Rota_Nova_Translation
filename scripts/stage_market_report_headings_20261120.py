"""Repair the Market Info atlas consumer after the Town Summary Status expansion."""

from pathlib import Path
from struct import pack_into, unpack_from

from scripts import stage_town_chart_punctuation_20261120 as chart
from scripts.stage_town_summary_20261119 import validate_rectangles


batch, parent, runtime = chart.batch, chart.parent, chart.runtime
ROOT = chart.ROOT.with_name('staged_v2')
ROM, PROOF, CHART_PROOF = ROOT / 'candidate.nds', ROOT / 'staging.json', chart.PROOF
REPORT, POINTER, PACKED = 0x11AFF8, 0xBE3A0, 0x15692C
HEADINGS = ('Type', 'Status', 'Growth', 'Arms')
OLD = ((84, 24), (108, 24), (132, 36), (168, 36))
NEW = ((84, 24), (108, 36), (144, 36), (180, 36))


def rectangles(arm):
    return [unpack_from('<7i', arm, REPORT + i * 28) for i in range(15)]


def patch(prior, clean):
    staged, chart_rows = chart.patch(prior, clean)
    assert unpack_from('<I', prior, POINTER) == unpack_from('<I', clean, POINTER) == (runtime.BASE + REPORT,)
    assert prior[0xB60F4:0xB6118] == clean[0xB60F4:0xB6118]
    assert prior[PACKED:PACKED + 24] == b'TypeStatusGrowthArms\0\0\0\0'
    assert clean[PACKED:PACKED + 24] == '種類状態発展度武装度'.encode('cp932') + bytes(4)
    previous = rectangles(prior)
    assert previous[-4:] == rectangles(clean)[-4:]
    assert tuple((row[3], row[5]) for row in previous[-4:]) == OLD
    result, labels = bytearray(staged), []
    offset = PACKED
    for i, (label, (x, w)) in enumerate(zip(HEADINGS, NEW, strict=True), 11):
        descriptor = REPORT + i * 28
        pack_into('<i', result, descriptor + 12, x)
        pack_into('<i', result, descriptor + 20, w)
        final = unpack_from('<7i', result, descriptor)
        labels.append(dict(heading=label, text_offset=offset, descriptor_offset=descriptor,
            previous=previous[i], target=final, entire_English_copy=True))
        assert offset == PACKED + (x - 84) // 6 and len(label) * 6 <= w
        offset += len(label)
    assert validate_rectangles(previous) == validate_rectangles(rectangles(result)) == 15
    assert runtime.cache_plan(result) == runtime.cache_plan(prior)
    return bytes(result), chart_rows, labels


def main():
    assert not ROOT.exists()
    previous = batch.load(parent.RELEASE)
    staged = batch.load(CHART_PROOF)
    assert parent.base.digest(parent.ROM) == previous['candidate_sha256'] == staged['parent_sha256']
    assert parent.base.digest(batch.CLEAN) == previous['clean_input_sha256']
    assert parent.base.digest(parent.base.REGISTRY) == previous['registry_sha256']
    original, clean, chart_rom = map(batch.NdsImage.open, (parent.ROM, batch.CLEAN, chart.ROM))
    before = batch.files(original)
    target, chart_rows, headings = patch(before[batch.ARM], clean.read_file(batch.ARM))
    inverse = bytearray(target)
    for item in headings:
        at = item['descriptor_offset']
        inverse[at:at + 28] = before[batch.ARM][at:at + 28]
    assert bytes(inverse) == chart_rom.read_file(batch.ARM)
    original.replace_file(batch.ARM, target)
    after = batch.files(original)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {batch.ARM}
    candidate = bytes(original.rom.save())
    original.replace_file(batch.ARM, before[batch.ARM])
    assert bytes(original.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    delta, rebuilt = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    runtime.make_xdelta(batch.CLEAN, ROM, delta)
    runtime.apply_xdelta(batch.CLEAN, delta, rebuilt)
    assert rebuilt.read_bytes() == candidate
    batch.write(PROOF, dict(candidate_sha256=batch.digest(candidate), parent_sha256=previous['candidate_sha256'],
        chart_candidate_sha256=staged['candidate_sha256'], target_ARM9_sha256=batch.digest(target),
        target_COMMON_sha256=previous['target_COMMON_sha256'], clean_input_sha256=previous['clean_input_sha256'],
        clean_input_patch_sha256=parent.base.digest(delta), whole_parent_inverse=True,
        clean_input_patch_byte_exact=True, chart_rows=chart_rows, headings=headings))
    print('Staged the Market Info atlas correction with the three chart changes.')


if __name__ == '__main__':
    main()
