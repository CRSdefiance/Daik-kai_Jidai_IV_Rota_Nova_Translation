"""Make immutable clean source inputs only after all435 drafts have been sealed."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.save_hodram_B171_B190_drafts import ROOT

if __name__ == '__main__':
    target = ROOT / 'current_binding_source_v1.json'
    assert not target.exists()
    drafts_path = ROOT / 'all435_clean_English_drafts_v2.json'
    drafts = load(drafts_path)
    assert len(drafts['records']) == 435 and drafts['all435_drafts_saved_before_current_ROM_dialogue_extraction']
    meanings_path = ROOT / 'complete_clean_meanings_before_English.json'
    meanings = load(meanings_path)
    packet_path = ROOT / 'clean_source_packet.json'
    rows = [deepcopy(r) for r in meanings['records'] if 'source_selector' in r]
    assert len(rows) == 433
    for row in rows:
        row['current_ROM_English_unconsulted'] = True
        row['earlier_user_tea_screenshot_incidental_exposure'] = row['id'] == 'DK4_MES_B188_R0022'
    save(target, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()),
        records=rows, meanings=433, all_drafts_sealed=str(drafts_path), all_drafts_sha256=sha(drafts_path.read_bytes()),
        incidental_earlier_screenshot_exposure_disclosed=True, no_blanket_prior_English_exposure_claim=True, new_credit=0))
    choices = deepcopy(load(ROOT / 'clean_choice_objects.json'))
    for row in choices['records']:
        row['earlier_English_unconsulted'] = True
    save(ROOT / 'choice_meanings_for_current_binding.json', choices)
    save(ROOT / 'clean_no_style_objects.json', dict(records=[], source_packet=str(packet_path),
        source_packet_sha256=sha(packet_path.read_bytes()), no_4100_source_commands=True, new_credit=0))
    print('Current-binding source prepared:433 speeches,two captions,zero styles;all435 drafts already sealed.')
