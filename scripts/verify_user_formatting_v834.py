"""Recheck the photographed shop pitch without claiming a fresh scene activation."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_dialogue_editorial import current_entries as pending_entries
from dk4tool.patch.refit_help_editorial import current_entries as current_entries
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save


def main():
    reference = Path('work/analysis/dialogue_formatting_user_recheck_v809/COMMON676_677.json')
    prior = read(reference)
    baseline = NdsImage.open(prior['candidate'])
    from dk4tool.patch.ceremony_editorial import current_entries as reference_entries
    old = reference_entries(baseline.read_file('/COMMON/MESFILE.DK4'), baseline.read_file('/__arm9__.bin'))
    results = []
    for version, parser in ((831, current_entries), (834, pending_entries)):
        path = Path(f'out/all_routes_combined_v{version}_candidate.nds')
        rom = NdsImage.open(path)
        common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
        digest = sha(path.read_bytes())
        assert digest == read(path.with_suffix('.manifest.json'))['candidate_sha256']
        entries, rows = parser(common, arm), []
        cpu = prepared(arm)
        for row in prior['entries']:
            number = row['id']
            assert entries[number].text == old[number].text
            formatted, lines = native_layout(cpu, entries[number].text, number, ())
            assert formatted.hex() == row['native_formatted_hex'] and lines == row['lines']
            assert 'Discover' not in ' '.join(lines)
            pixels = raster(arm, formatted, 0x01FFCE40 - 0x02000000,
                            size=(228, 64), instruction_limit=2000000)
            assert pixels == independent_font(arm, rom.read_file('/GRP/KANJI.FNT'), lines)
            rows.append({'id': number, 'template_hex': entries[number].text.hex(),
                         'native_formatted_hex': formatted.hex(), 'lines': lines,
                         'exact_repaired_text_and_native_formatting_preserved': True,
                         'complete_native_glyph_plane_matches_independent_font': True})
        results.append({'candidate': str(path), 'candidate_sha256': digest,
                        'COMMON_sha256': sha(common), 'ARM9_sha256': sha(arm), 'entries': rows,
                        'release_status': 'current editorial reference' if version == 831 else 'pending gameplay verification'})
    capture = Path(prior['earlier_actual_capture'])
    assert sha(capture.read_bytes()) == prior['earlier_actual_capture_sha256']
    proof = Path('work/analysis/dialogue_formatting_user_recheck_v834/COMMON676_677.json')
    proof.parent.mkdir(parents=True, exist_ok=True)
    save(proof, {'candidates': results, 'prior_reference': str(reference),
                 'prior_reference_sha256': sha(reference.read_bytes()),
                 'earlier_actual_capture': str(capture), 'earlier_actual_capture_sha256': sha(capture.read_bytes()),
                 'earlier_actual_capture_visually_reviewed': True,
                 'scope': 'Exact current and pending-build text, native wrapping and complete glyph planes. Earlier V747 actual scene reviewed; no fresh shop-scene activation claimed.',
                 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_game_formatting_complete': False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    watch = ledger['formatting_watchlist']
    watch['latest_reference_proof'] = str(proof)
    watch['latest_user_screenshot_recheck'] = {
        'proof': str(proof), 'versions_rechecked': [831, 834],
        'result': 'Repaired cooking and fashion pitches retain exact text, native wrapping and full glyph planes. Earlier actual cooking scene reviewed: aligned lines, no padding gap or stray Discover. No fresh shop-scene activation claimed. Audit remains open.'}
    save(ledger_path, ledger)
    print('V831 and pending V834: both repaired pitches retain exact text, wrapping and complete glyph planes.')
    print(results[-1]['entries'][0]['lines'])


if __name__ == '__main__':
    main()
