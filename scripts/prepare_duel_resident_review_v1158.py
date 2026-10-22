"""Prepare visual review and classify one source-contextual warning precisely."""
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_resident_review_v1158')


def main():
    assert not ROOT.exists()
    resident_path = Path('work/analysis/duel_resident_fonts_v1151/cache_resident_complete_fonts.json')
    escape_path = Path('work/analysis/duel_escape_fonts_v1157/native_escape_fonts.json')
    resident, escape = read(resident_path), read(escape_path)
    assert len(resident['cases']) == 1356 and len(escape['cases']) == 1417
    findings = escape['findings_requiring_review']
    assert len(findings) == 161
    for case in findings:
        assert case['message_ID'] == 1954 and case['weak_line_end_indices'] == [0]
        assert not case['short_or_orphan_final_row']
        assert len(case['lines']) == 2 and case['lines'][0].endswith('Come on,')
        assert case['lines'][1] == 'lads, cover them!'
    ROOT.mkdir(parents=True)
    previews = resident['research_previews']
    assert len(previews) == 12
    sheet = Image.new('RGB', (1728, 1188), '#263238')
    for index, row in enumerate(previews):
        path = Path(row['path'])
        assert sha(path.read_bytes()) == row['sha256']
        with Image.open(path) as image:
            sheet.paste(image.convert('RGB'), (index % 2*864, index//2*198))
    path = ROOT/'resident_native_research_sheet.png'
    sheet.save(path)
    sheets = [{'path': str(path), 'sha256': sha(path.read_bytes())}, *escape['review_sheets']]
    for row in sheets:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    save(ROOT/'visual_review_packet.json', {'resident_font_proof': str(resident_path),
        'resident_font_proof_sha256': sha(resident_path.read_bytes()),
        'escape_font_proof': str(escape_path), 'escape_font_proof_sha256': sha(escape_path.read_bytes()),
        'all_review_sheets': sheets, 'visual_review_pending': True,
        'contextual_boundary_warning': {'ID': 1954, 'cases': 161, 'scope': 'generated break after Come on,',
            'following_row_exact': 'lads, cover them!',
            'decision': 'Retain after visual review: on belongs to the complete interjection Come on, not a preposition awaiting its object. The comma is a natural spoken pause before the vocative lads. All161 flagged cases have exactly this boundary; no broken word, omitted fact, orphan row or authored break.',
            'general_weak_word_checker_and_other_records_not_waived': True},
        'CPU_research_not_guide_or_gameplay_screenshots': True,
        'all33_formatting_gates_remain_false_until_final_native_consumer_audit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(sheets)} sheets prepared;161 warnings are the same complete Come on, interjection. Visual review pending.')


if __name__ == '__main__':
    main()
