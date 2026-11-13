"""Prepare immutable binding inputs only after all 373 logical drafts are sealed."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')


if __name__ == '__main__':
    target = ROOT / 'current_binding_source_v1.json'
    assert not target.exists()
    drafts_path = ROOT / 'complete_clean_English_drafts_v1.json'
    drafts = load(drafts_path)
    assert len(drafts['records']) == 373 and drafts['source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake']
    packet_path = ROOT / 'clean_source_packet.json'
    meanings = load(ROOT / 'complete_clean_meanings_before_English.json')
    rows = [deepcopy(r) for r in meanings['records'] if 'source_selector' in r]
    assert len(rows) == 352
    for row in rows:
        row['current_ROM_English_unconsulted'] = True
    save(target, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()),
        records=rows, meanings=352, all_drafts_sealed=str(drafts_path), all_drafts_sha256=sha(drafts_path.read_bytes()),
        no_blanket_prior_English_exposure_claim=True, new_credit=0))
    choices = deepcopy(load(ROOT / 'clean_choice_objects.json'))
    for row in choices['records']:
        row['earlier_English_unconsulted'] = True
    save(ROOT / 'choices_for_current_binding_v1.json', choices)
    save(ROOT / 'clean_no_style_objects_v1.json', dict(records=[], source_packet=str(packet_path),
        source_packet_sha256=sha(packet_path.read_bytes()), no_4100_source_commands=True, new_credit=0))
    print('Prepared 352 speeches/21 captions/zero styles for current binding after all 373 drafts were sealed.')
