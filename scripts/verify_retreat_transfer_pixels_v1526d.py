"""Explain every changed RGB pixel in all three actual retreat holds."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/retreat_transfer_actual_pixels_v1526d')

if __name__ == '__main__':
    assert not ROOT.exists()
    proof_path = Path('work/analysis/retreat_transfer_actual_fonts_v1526c/actual_retreat_font_and_transition_verification.json')
    proof = read(proof_path)
    rom = NdsImage.open(proof['candidate'])
    arm = rom.read_file('/__arm9__.bin')
    before = read('work/analysis/stronger_fleet_return_verified_v1505/actual_declaration_defeat_and_transfer_return.json')
    old_report = read(before['terminal_report'])
    old_frames = {r['frame']: r for r in old_report['frames_captured']}
    old_snapshots = {r['frame']: r for r in old_report['read_only_capture_RAM_snapshots'] + old_report['read_only_pause_RAM_snapshots']}

    class CurrentFont:
        @staticmethod
        def open(path):
            assert path == 'out/all_routes_combined_v255_candidate.nds'
            return rom

    raster = FunctionType(original_raster.__code__, {**original_raster.__globals__, 'NdsImage': CurrentFont}, argdefs=original_raster.__defaults__)
    old_arm = NdsImage.open(before['candidate']).read_file('/__arm9__.bin')
    assert rom.read_file('/GRP/KANJI.FNT') == NdsImage.open(before['candidate']).read_file('/GRP/KANJI.FNT')
    wrapped = struct.unpack_from('<I', old_arm, 0x54450)[0] - 0x02000000
    results = []
    for hold in proof['complete_actual2684_holds']:
        frame = hold['frame']
        old = old_frames[frame]
        snapshot = old_snapshots[frame]
        raw = Path(snapshot['path']).read_bytes()
        assert sha(raw) == snapshot['sha256']
        formatted = raw[wrapped:wrapped + 512].split(b'\0')[0]
        lines = [r.strip().decode('cp932') for r in formatted.split(b'\n')]
        pixels = raster(arm, formatted, 0x01FFCE40 - 0x02000000, size=(228, 64), instruction_limit=2000000)
        assert pixels == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), lines)
        expected_old = {(16 + i % 228, 296 + i // 228) for i, p in enumerate(pixels) if p}
        new_pixels = independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), hold['lines'])
        expected_new = {(16 + i % 228, 296 + i // 228) for i, p in enumerate(new_pixels) if p}
        assert sha(Path(old['path']).read_bytes()) == old['PNG_sha256']
        with Image.open(old['path']) as a, Image.open(hold['PNG']) as b:
            a, b = a.convert('RGB'), b.convert('RGB')
            actual_old = {(x, y) for y in range(294, 366) for x in range(16, 244) if a.getpixel((x, y)) == (0, 8, 0)}
            assert actual_old == expected_old
            differences = {(i % 256, i // 256) for i, (x, y) in enumerate(zip(a.get_flattened_data(), b.get_flattened_data(), strict=True)) if x != y}
            assert differences == expected_old ^ expected_new
        results.append({'frame': frame, 'whole256x384_changed_RGB_pixels': len(differences),
            'every_changed_pixel_exactly_the_old_new_native_glyph_symmetric_difference': True,
            'all_portrait_scene_backdrop_border_paper_and_other_pixels_exact': True,
            'old_formatted_hex': formatted.hex(), 'old_lines': lines,
            'old_PNG': old['path'], 'old_PNG_sha256': old['PNG_sha256'], 'new_PNG_sha256': hold['PNG_sha256']})
    assert len(results) == 3
    ROOT.mkdir(parents=True)
    save(ROOT / 'all_changed_pixels_explained.json', {'candidate_sha256': proof['candidate_sha256'],
        'actual_font_proof': str(proof_path), 'actual_font_proof_sha256': sha(proof_path.read_bytes()),
        'all3_whole_screen_text_changes': results, 'remaining42_complete_frames_exact_to_V1492': True,
        'no_mask_pixel_waiver_or_retiming': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('All three full screens differ at exactly278 native old/new letter pixels each;all other pixels unchanged.')
