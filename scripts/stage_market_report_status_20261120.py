"""Match Market Info to the shared widened status atlas and fix its title slices."""

from struct import pack_into, unpack_from

from scripts import stage_market_report_headings_20261120 as headings
from scripts.stage_town_shortage_20261119 import TOWN_ROW
from scripts.stage_town_summary_20261119 import validate_rectangles


batch, parent, runtime = headings.batch, headings.parent, headings.runtime
ROOT = headings.ROOT.with_name('staged_v3')
ROM, PROOF = ROOT / 'candidate.nds', ROOT / 'staging.json'
VALUE = headings.REPORT + 2 * 28
STALE_COPY = headings.REPORT + 6 * 28
STATUS_HEADING = headings.REPORT + 12 * 28


def patch(prior, clean):
    base, chart_rows, label_rows = headings.patch(prior, clean)
    current = headings.rectangles(base)
    assert unpack_from('<7i', base, TOWN_ROW) == (-1, 68, 62, 120, 12, 48, 12)
    assert unpack_from('<7i', base, VALUE) == (-1, 192, 26, 24, 12, 36, 12)
    assert unpack_from('<7i', base, STALE_COPY) == (-1, 152, 112, 108, 12, 72, 12)
    assert unpack_from('<7i', base, STATUS_HEADING) == (-1, 160, 26, 108, 60, 36, 12)
    target = bytearray(base)
    pack_into('<4i', target, VALUE + 12, 120, 12, 48, 12)
    # The old second specialty rectangle overlaps the primary view's relocated
    # status glyphs on the shared bitmap and was drawing their ghost copy.
    pack_into('<4i', target, STALE_COPY + 12, 0, 0, 0, 0)
    pack_into('<i', target, STATUS_HEADING + 4, 148)
    assert validate_rectangles(headings.rectangles(target)) == 14
    status = unpack_from('<7i', target, STATUS_HEADING)
    value = unpack_from('<7i', target, VALUE)
    assert status[1] + status[5] == value[1] - 8 and value[1] + value[5] == 240
    for item in label_rows:
        if item['heading'] == 'Status':
            item['target'] = status
    changes = [dict(offset=off, prior_stage=list(old), target=list(unpack_from('<7i', target, off)))
               for off, old in ((VALUE, current[2]), (STALE_COPY, current[6]), (STATUS_HEADING, current[12]))]
    return bytes(target), chart_rows, label_rows, changes


def main():
    assert not ROOT.exists()
    previous = batch.load(parent.RELEASE)
    v2 = batch.load(headings.PROOF)
    assert parent.base.digest(parent.ROM) == previous['candidate_sha256'] == v2['parent_sha256']
    assert parent.base.digest(batch.CLEAN) == previous['clean_input_sha256']
    assert parent.base.digest(parent.base.REGISTRY) == previous['registry_sha256']
    prior, clean, comparison = map(batch.NdsImage.open, (parent.ROM, batch.CLEAN, headings.ROM))
    before = batch.files(prior)
    target, chart_rows, labels, status = patch(before[batch.ARM], clean.read_file(batch.ARM))
    inverse = bytearray(target)
    for row in status:
        pack_into('<7i', inverse, row['offset'], *row['prior_stage'])
    assert bytes(inverse) == comparison.read_file(batch.ARM)
    prior.replace_file(batch.ARM, target)
    after = batch.files(prior)
    assert before.keys() == after.keys() and {p for p in before if before[p] != after[p]} == {batch.ARM}
    candidate = bytes(prior.rom.save())
    prior.replace_file(batch.ARM, before[batch.ARM])
    assert bytes(prior.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(candidate)
    delta, reconstructed = ROOT / 'translation.xdelta', ROOT / 'clean_rebuilt.nds'
    runtime.make_xdelta(batch.CLEAN, ROM, delta)
    runtime.apply_xdelta(batch.CLEAN, delta, reconstructed)
    assert reconstructed.read_bytes() == candidate
    batch.write(PROOF, dict(candidate_sha256=batch.digest(candidate), parent_sha256=previous['candidate_sha256'],
        charts_only_sha256=v2['chart_candidate_sha256'], charts_and_headings_sha256=v2['candidate_sha256'],
        clean_input_sha256=previous['clean_input_sha256'], target_COMMON_sha256=previous['target_COMMON_sha256'],
        target_ARM9_sha256=batch.digest(target), clean_input_patch_sha256=parent.base.digest(delta),
        whole_parent_inverse=True, clean_input_patch_byte_exact=True, chart_rows=chart_rows, headings=labels,
        status_geometry=status))
    print('Staged the original report with complete headings and its full eight-letter Status value.')


if __name__ == '__main__':
    main()
