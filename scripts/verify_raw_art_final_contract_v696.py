"""Check final comic preservation against actual later-stage corruptions."""

import struct
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.raw_art_contract import (
    FILE,
    MARK_BOX,
    MARK_FRAME,
    region,
    verify_final_raw_art,
)
from dk4tool.graphics.raw_bgr555_art import FORMAT, FRAME_BYTES, render_region_payload
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import verify_golden_content
from scripts.verify_plaque_final_contract_v687 import Overlay
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/raw_art_final_contract_v696')
ROM = Path('out/all_routes_combined_v692_candidate.nds')
REBUILT = Path('out/all_routes_combined_v692_raw_art_contract_rebuild.nds')


def main():
    ROOT.mkdir(exist_ok=True)
    pp = ROOT / 'preflight.json'
    if not pp.exists():
        frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
        paths = (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
                 Path('translations/release_stack.json'), Path('work/clean.nds'),
                 Path('out/raphael_natural_v2_accepted_base.nds'))
        save(pp, {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
            'release_hashes': {str(p): sha(p.read_bytes()) for p in paths},
            'all_original_audits_before': {n: read(Path('translations') / n) for n in frozen},
            'previous_goal_turn_classification': 'progress: V695 relocated sources and two embedded original UI atlases',
            'no_new_art_or_ROM_content_authoring': True})
    pre = read(pp)
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    stack = read('translations/release_stack.json')
    paths = [Path(p) for p in stack['profiles']['all-routes-unified-v692']['batches']]
    raw_paths = [p for p in paths if read(p).get('format') == FORMAT]
    assert len(raw_paths) == 1
    batch = read(raw_paths[0])
    current, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    baseline = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    passed = verify_final_raw_art(current, baseline, clean, paths)
    family, = passed['families']
    assert len(family['complete_caption_regions']) == 18 and len(family['untouched_frames']) == 11
    assert family['approved_brown_mark_bytes'] == 4320
    source = IlnkContainer.parse(baseline.read_file(FILE)).blocks[19]
    archive = IlnkContainer.parse(current.read_file(FILE))
    full = archive.blocks[19]
    mutations = []

    def add(name, altered):
        copied = IlnkContainer(list(archive.blocks))
        copied.blocks[19] = bytes(altered)
        mutations.append((name, copied.to_bytes()))

    row = batch['records'][0]
    assert row['english'] == 'Well done!'
    _, meta = render_region_payload(row, region(source, row['image_index'], row['box']), batch, source)
    l, t, r, _ = row['box']
    width = r - l
    for name, glyph in (('leading_letter_ink_deleted', meta['visible_characters'][0]),
                        ('final_punctuation_ink_deleted', meta['visible_characters'][-1])):
        x0, y0, x1, y1 = glyph['bbox']
        candidates = [row['image_index'] * FRAME_BYTES + ((t + y) * 320 + l + x) * 2
                      for y in range(y0, y1) for x in range(x0, x1)]
        at = min(candidates, key=lambda at: struct.unpack_from('<H', full, at)[0] & 32767)
        assert struct.unpack_from('<H', full, at)[0] & 32767 != 32767
        altered = bytearray(full)
        old = struct.unpack_from('<H', altered, at)[0]
        struct.pack_into('<H', altered, at, (old & 32768) | 32767)
        add(name, altered)
    altered = bytearray(full)
    for y in range(row['box'][1], row['box'][3]):
        at = row['image_index'] * FRAME_BYTES + (y * 320 + l) * 2
        altered[at:at + width * 2] = source[at:at + width * 2]
    add('whole_caption_reverted_to_Japanese_source', altered)
    altered = bytearray(full)
    at = MARK_FRAME * FRAME_BYTES + (MARK_BOX[1] * 320 + MARK_BOX[0]) * 2
    altered[at] ^= 1
    add('user_preserved_mark_region_changed', altered)
    altered = bytearray(full)
    altered[1] ^= 128
    add('original_high_color_bit_changed', altered)
    altered = bytearray(full)
    altered[0] ^= 1
    add('untouched_frame_source_art_changed', altered)
    row = next(r for r in batch['records'] if r['id'] == 'DK4_GALLERY_RECRUITMENT_TITLE_V1')
    _, meta = render_region_payload(row, region(source, row['image_index'], row['box']), batch, source)
    point = meta['restoration']['estimated_scenery_indices'][0]
    l, t, r, _ = row['box']
    x, y = point % (r - l) + l, point // (r - l) + t
    altered = bytearray(full)
    altered[row['image_index'] * FRAME_BYTES + (y * 320 + x) * 2] ^= 1
    add('reviewed_estimated_background_word_changed', altered)
    results = []
    for name, raw in mutations:
        altered = Overlay(current, {FILE: raw})
        verify_golden_content(baseline, altered)
        try:
            verify_final_raw_art(altered, baseline, clean, paths)
        except ValueError as error:
            results.append({'case': name, 'existing_menu_placeholder_gate_passes': True,
                'new_final_raw_art_gate_rejects': True, 'error': str(error),
                'in_memory_altered_archive_sha256': sha(raw)})
        else:
            raise AssertionError('Comic corruption escaped the final guard: ' + name)
    assert len(results) == 7
    other = IlnkContainer(list(archive.blocks))
    block0 = bytearray(other.blocks[0])
    block0[0] ^= 1
    other.blocks[0] = bytes(block0)
    assert verify_final_raw_art(Overlay(current, {FILE: other.to_bytes()}), baseline, clean, paths) == passed
    assert verify_final_raw_art(Overlay(current, {'/data/SC3.DK4': clean.read_file('/data/SC3.DK4')}),
                                baseline, clean, paths) == passed
    assert not verify_final_raw_art(clean, baseline, clean, [])['applicable']
    historical_paths = [Path(p) for p in stack['profiles']['all-routes-unified-v185']['batches']]
    historical = verify_final_raw_art(NdsImage.open('out/all_routes_combined_v185_candidate.nds'),
                                      baseline, clean, historical_paths)
    assert historical['applicable']
    save(ROOT / 'contract_proof.json', {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'final_contract': passed, 'seven_later_stage_corruptions_rejected': results,
        'unrelated_story_and_other_registered_archive_blocks_not_reinterpreted': True,
        'historical_V185_own_source_locked_raw_art_contract_passes': True,
        'profiles_without_raw_art_report_not_applicable': True,
        'all_mutations_in_memory_no_corrupt_ROM_written': True,
        'visual_restoration_and_unknown_parent_not_completed_by_this_guard': True,
        'gate_sha256': sha(Path('dk4tool/graphics/raw_art_contract.py').read_bytes()),
        'builder_sha256': sha(Path('scripts/build_integrated_release.py').read_bytes()),
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V696: all18 final comic regions,11 untouched frames and4320 preserved mark bytes pass; seven later-stage corruptions rejected; historical and unrelated controls pass.', flush=True)


if __name__ == '__main__':
    main()
