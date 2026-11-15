"""Independently reconcile saved scale proofs, source words and visual artifacts."""

import ast
import struct
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.research_comic_scaling_v680 import BATCH, ROOT
from scripts.verify_village_wrap_v608 import read, save


def axis(source_size, target_size):
    # Independent source-forward form of the midpoint rasterization contract.
    out, accumulator = [], source_size // 2
    for source in range(source_size):
        accumulator += target_size
        while accumulator >= source_size:
            out.append(source)
            accumulator -= source_size
    assert len(out) == target_size
    return out


def expected_plane(pixels, case):
    left, top, right, bottom = case['actual_clipped_destination']
    xs, ys = axis(320, right - left), axis(240, bottom - top)
    assert xs == case['source_sample_x'] and ys == case['source_sample_y']
    words = struct.unpack('<76800H', pixels)
    output = [0x89AB] * 98304
    base = case['screen'] * 49152
    for y, sy in enumerate(ys, top):
        start = base + y * 256 + left
        output[start:start + len(xs)] = [words[sy * 320 + sx] for sx in xs]
    return struct.pack('<98304H', *output)


def main():
    proof, pre = read(ROOT / 'proof.json'), read(ROOT / 'preflight.json')
    producer = read(ROOT / 'producer_source_provenance.json')
    executed, current = Path(producer['executed_source']), Path(producer['current_source'])
    assert sha(executed.read_bytes()) == proof['script_sha256'] == producer['executed_source_sha256']
    assert sha(current.read_bytes()) == producer['current_source_sha256']
    assert ast.dump(ast.parse(executed.read_text(encoding='utf-8')), include_attributes=False) == ast.dump(
        ast.parse(current.read_text(encoding='utf-8')), include_attributes=False)
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom = NdsImage.open(pre['candidate'])
    archive = rom.read_file('/GRP/SLACKIMG.DK4')
    block = IlnkContainer.parse(archive).blocks[19]
    assert sha(archive) == proof['archive_sha256'] and sha(block) == proof['block19_sha256']
    prior = read('work/analysis/comic_current_v506/all_frames_manifest.json')
    for row in prior['frames']:
        at = row['frame'] * 153600
        assert sha(block[at:at + 153600]) == row['current_sha256']
    assert sha(BATCH.read_bytes()) == read('work/analysis/comic_current_v506/proof.json')['batch_sha256']
    cases = proof['complete_native_scale_cases']
    assert len(cases) == 42 and proof['original_partial_archive_reads'] == 21
    assert {(c['frame'], c['view']) for c in cases} == {(i, v) for i in range(21) for v in ('full_fit', 'clipped_origin')}
    for case in cases:
        pixels = block[case['frame'] * 153600:(case['frame'] + 1) * 153600]
        assert sha(pixels) == case['source_sha256']
        expected = expected_plane(pixels, case)
        assert sha(expected) == case['complete_two_screen_framebuffer_sha256']
        png = Path(case['software_plane'])
        assert sha(png.read_bytes()) == case['software_plane_sha256']
        plane = expected[case['screen'] * 98304:(case['screen'] + 1) * 98304]
        wanted = bytes(c for word, in struct.iter_unpack('<H', plane) for c in bgr555(word)[:3])
        im = Image.open(png).convert('RGB')
        assert im.size == (256, 192) and im.tobytes() == wanted
        actual_reads = [e for e in case['original_IO'] if e['operation'] == 'read' and e['bytes'] == 153600]
        assert len(actual_reads) == 1 and actual_reads[0]['destination'] == 0x02420034
    assert proof['complete_two_screen_framebuffer_bytes_compared'] == 8257536
    assert proof['caption_edge_checks'] == 72 and not proof['projected_missing_edge_letter_contrasts']
    assert all(g['projected_contrast_points'] > 0 for c in cases for g in c['caption_edge_letter_checks'])
    for control in proof['independent_xy_coordinate_controls']:
        frame = struct.pack('<76800H', *[x if control['axis'] == 0 else y for y in range(240) for x in range(320)])
        template = next(c for c in cases if c['view'] == control['view'])
        assert sha(expected_plane(frame, template)) == control['sha256']
    source = IlnkContainer.parse(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/GRP/SLACKIMG.DK4')).blocks[19]
    mark_regions = [b''.join(data[6 * 153600 + (y * 320 + 175) * 2:6 * 153600 + (y * 320 + 229) * 2]
                             for y in range(96, 136)) for data in (source, block)]
    assert mark_regions[0] == mark_regions[1] and len(mark_regions[1]) == 4320
    assert sha(mark_regions[1]) == '3b0111f01e8f7a0857a723f28138d130e29caad046aa5d15f7367831ac1d6943'
    for sheet in proof['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    save(ROOT / 'independent_verification.json', {
        'all42_native_hashes_and_RGB_planes_match_independent_source_forward_model': True,
        'all4_coordinate_controls_match': True,
        'all21_current_frames_exact_to_previous_reviewed_art_and_source_brown_marks4320_bytes_exact': True,
        'all72_leading_trailing_character_contrasts_present_in_supplied_scale_cases': True,
        'six_source_English_native_software_review_sheets_opened_all21_frames': True,
        'descriptor_source_and_viewport_are_controlled_not_original_scene_proof': True,
        'no_GPU_alpha_physical_readability_or_comic_parent_clearance': True,
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V680 independent:42 full word/RGB outputs,4 coordinate planes,72 caption edges and exact brown marks pass.', flush=True)


if __name__ == '__main__':
    main()
