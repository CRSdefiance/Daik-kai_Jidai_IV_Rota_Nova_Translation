"""Recheck photographed shop pitches in the current ROM; no new scene claim."""
from pathlib import Path

from dk4tool.patch.battle_declaration_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from types import FunctionType
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save



def raster(*args, **kwargs):
    class CurrentFont:
        @staticmethod
        def open(path):
            assert str(path) == 'out/all_routes_combined_v255_candidate.nds'
            return NdsImage.open('out/all_routes_combined_v997_candidate.nds')
    draw = FunctionType(original_raster.__code__,
                        {**original_raster.__globals__, 'NdsImage': CurrentFont}, argdefs=original_raster.__defaults__)
    return draw(*args, **kwargs)


def main():
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    original = read(ledger_path)
    candidate = ledger['current_integrated_candidate']
    path = Path(candidate['path'])
    assert sha(path.read_bytes()) == candidate['sha256']
    assert candidate['sha256'] == '0093915adb53c7c1034b696d54bf897079908aa598ea39bdced849107983660d'
    rom = NdsImage.open(path)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    assert sha(common) == candidate['MESFILE_sha256'] and sha(arm) == candidate['ARM9_sha256']
    reference_path = Path('work/analysis/dialogue_formatting_user_recheck_v809/COMMON676_677.json')
    reference = read(reference_path)
    entries, cpu, results = current_entries(common, arm), prepared(arm), []
    for row in reference['entries']:
        number = row['id']
        formatted, lines = native_layout(cpu, entries[number].text, number, ())
        assert formatted.hex() == row['native_formatted_hex'] and lines == row['lines']
        assert all(line == line.strip() and '  ' not in line for line in lines)
        assert 'Discover' not in ' '.join(lines) and len(lines) <= 4
        pixels = raster(arm, formatted, 0x01FFCE40 - 0x02000000,
                        size=(228, 64), instruction_limit=2000000)
        assert pixels == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), lines)
        results.append({'id': number, 'template_hex': entries[number].text.hex(),
                        'native_formatted_hex': formatted.hex(), 'lines': lines,
                        'exact_repaired_native_formatting_preserved': True,
                        'complete_native_glyph_plane_matches_independent_font': True})
    capture = Path(reference['earlier_actual_capture'])
    assert sha(capture.read_bytes()) == reference['earlier_actual_capture_sha256']
    proof = Path('work/analysis/dialogue_formatting_user_recheck_v1027c/COMMON676_677.json')
    assert not proof.exists()
    proof.parent.mkdir(parents=True, exist_ok=True)
    save(proof, {'candidate': str(path), 'candidate_sha256': candidate['sha256'],
                 'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm), 'entries': results,
                 'reference': str(reference_path), 'reference_sha256': sha(reference_path.read_bytes()),
                 'earlier_actual_capture': str(capture),
                 'earlier_actual_capture_sha256': sha(capture.read_bytes()),
                 'earlier_actual_capture_visually_reviewed': True,
                 'new_actual_shop_activation_claimed': False,
                 'scope': 'Current V997 native wrapping and complete font planes; earlier V747 actual cooking scene reviewed. Global audit remains open.',
                 'failed_predecessor': 'scripts/verify_user_formatting_v1027.py', 'failed_predecessor_sha256': '05ec02f2355a690e1c8baca31e8d9ec43f0c2f5efd53b8871b769be832942eb2', 'font_adapter': 'Exact current V997 KANJI font; historical V255 dependency removed from test only', 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_game_formatting_complete': False})
    watch = ledger['formatting_watchlist']
    watch['latest_reference_proof'] = str(proof)
    watch['latest_user_screenshot_recheck'] = {
        'proof': str(proof), 'candidate': str(path),
        'exact_repaired676_677_bytes_preserved': True,
        'complete_native_wrapping_and_glyph_planes_rechecked': True,
        'new_actual_shop_activation_claimed': False,
        'result': 'Aligned cooking pitch; no internal padding gap or stray Discover. Independent fashion pitch complete. Formatting audit remains open.'}
    assert {k: v for k, v in ledger.items() if k != 'formatting_watchlist'} == {
        k: v for k, v in original.items() if k != 'formatting_watchlist'}
    save(ledger_path, ledger)
    print('V997: both repaired pitches retain exact wrapping and complete native glyph planes; global audit stays open.')
    print(results[0]['lines'])


if __name__ == '__main__':
    main()
