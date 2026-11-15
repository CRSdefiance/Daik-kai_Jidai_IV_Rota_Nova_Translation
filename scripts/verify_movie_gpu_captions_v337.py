"""Check every edited M28 texture against existing controlled GPU captures."""
import json
from pathlib import Path

from PIL import Image

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_movie_gpu_fixture_v336 import PARENT
from scripts.verify_movie_gpu_fixtures_v336 import plane_locations, quantized

ROOT = Path('work/analysis/movie_gpu_caption_v337')

def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current = FlsArchive(NdsImage.open(PARENT).read_file('/FLS/M28.fls'))
    source = FlsArchive(NdsImage.open('work/clean.nds').read_file('/FLS/M28.fls'))
    report_path = Path('work/emulation_v193/movie_gpu_fixture_v336_m28/capture_report.json')
    report = json.loads(report_path.read_text(encoding='utf-8'))
    frames = []
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        if 2100 <= shot['frame'] <= 8700:
            frames.append((shot, quantized(Image.open(shot['path']).crop((0, 0, 256, 192)))))
    dense_path = Path('work/emulation_v193/movie_gpu_caption_v337/capture_report.json')
    dense = json.loads(dense_path.read_text(encoding='utf-8'))
    manifest = json.loads(Path('work/analysis/movie_gpu_fixture_v336/m28_fixture_manifest.json').read_text(encoding='utf-8'))
    assert dense['ROM_sha256'] == manifest['research_ROM_sha256'] == report['ROM_sha256']
    assert dense['cold_boot'] and not dense['savestate_loaded'] and not dense['callback_errors']
    assert dense['every_frame_capture_window'] == [3540, 3700]
    assert dense['scripted_input_schedule'] == report['scripted_input_schedule']
    dense_frames = []
    for shot in dense['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        if 3540 <= shot['frame'] <= 3700:
            dense_frames.append((shot, quantized(Image.open(shot['path']).crop((0, 0, 256, 192)))))
    assert [shot['frame'] for shot, _ in dense_frames] == list(range(3540, 3701))
    rows = []
    for index in range(1, len(current.records)):
        texture, original = current.texture(index), source.texture(index)
        if texture.indices == original.indices and texture.palette == original.palette:
            continue
        matches = []
        if index < 27:
            for shot, image in frames:
                for match in plane_locations(texture, image):
                    matches.append({'frame': shot['frame'], 'PNG': shot['path'], **match})
        else:
            points = [(i % texture.width, i // texture.width,
                       tuple(value >> 3 for value in texture.palette[color][:3]))
                      for i, color in enumerate(texture.indices) if color]
            for shot, image in dense_frames:
                pixels = image.load()
                if all(pixels[x + 12, y + 167] == value for x, y, value in points):
                    matches.append({'frame': shot['frame'], 'PNG': shot['path'],
                                    'origin': [12, 167], 'full_nonzero_source_pixels': len(points),
                                    'leading_internal_trailing_ink_and_source_shadows_included': True})
        row = {'texture': index, 'native_width': current.records[index][0] >> 16,
               'native_height': current.records[index][1] & 65535,
               'exact_full_ink_shadow_matches': matches,
               'all_nonzero_source_pixels': sum(bool(x) for x in texture.indices),
               'not_found_is_unverified_not_a_proven_defect': not matches}
        rows.append(row)
        print(json.dumps({'texture': index, 'matches': len(matches), 'first': matches[:1]}), flush=True)
    assert len(rows) == 22 and all(row['exact_full_ink_shadow_matches'] for row in rows)
    proof = {'candidate_sha256': sha(PARENT.read_bytes()), 'movie': '/FLS/M28.fls',
             'all_edited_textures_censused': len(rows), 'cases': rows,
             'capture_report_sha256': sha(report_path.read_bytes()),
             'dense_capture_report_sha256': sha(dense_path.read_bytes()),
             'ink_matches_do_not_identify_which_progressive_texture_is_bound': True,
             'controlled_substitution_not_normal_caller': True,
             'production_ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')

if __name__ == '__main__':
    main()
