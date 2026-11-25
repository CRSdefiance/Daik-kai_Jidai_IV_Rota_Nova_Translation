"""Seal 373 exact source meanings without adding editorial completion credit."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')


if __name__ == '__main__':
    target = ROOT / 'complete_clean_meanings_checkpoint_v1.json'
    combined = ROOT / 'complete_clean_meanings_before_English.json'
    assert not target.exists() and not combined.exists()
    packet_path = ROOT / 'clean_source_packet.json'
    choices_path = ROOT / 'clean_choice_objects.json'
    packet, choices = map(load, [packet_path, choices_path])
    parts = [ROOT / (name + '_clean_meanings_before_English.json') for name in [
        'B191_B193', 'B194_B197', 'B198_B200', 'B201_B203', 'B204_B210']]
    caption_parts = [ROOT / name for name in ['B200_twelve_clean_caption_meanings_v1.json',
        'B201_three_clean_caption_meanings_v1.json', 'B205_B210_six_clean_caption_meanings_v1.json']]
    source = {r['id']: r for g in packet['groups'] for r in g['records']}
    rows = [r for path in parts for r in load(path)['records']]
    assert len(rows) == len({r['id'] for r in rows}) == len(source) == 352
    assert {r['id'] for r in rows} == set(source)
    for row in rows:
        assert all(row[k] == source[row['id']][k] for k in ['source_hex', 'source_reference', 'source_Japanese', 'source_complete_preamble_hex', 'source_selector'])
        assert row['source_meaning'].strip() and row['exchange_context'].strip()
    captions = [r for path in caption_parts for r in load(path)['records']]
    source_captions = {r['id']: r for r in choices['records']}
    assert len(captions) == len({r['id'] for r in captions}) == len(source_captions) == 21
    assert {r['id'] for r in captions} == set(source_captions)
    for row in captions:
        assert all(row[k] == source_captions[row['id']][k] for k in ['source_hex', 'source_reference', 'source_Japanese', 'source_index', 'source_count', 'source_command_offset'])
        assert row['source_meaning'].strip() and row['exchange_context'].strip()
    label_free = [dict(block=g['block'], command_offset=c['offset'], whole_command_hex=c['whole_command_hex'])
        for g in packet['groups'] for c in g['all_source_commands'] if c['word'] == 0x2000]
    assert label_free == [dict(block=203, command_offset=78, whole_command_hex='0020')]
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = load(ledger_path)
    assert ledger['records_editorially_completed'] == 9933 and not ledger['full_goal_complete']
    existing = {(r['file_path'], r['id']) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    keys = {(r['file_path'], r['id']) for r in rows + captions}
    assert len(existing) == 9933 and len(keys) == 373 and not existing.intersection(keys)
    evidence = {str(p): sha(p.read_bytes()) for p in [packet_path, choices_path, ROOT / 'clean_style_objects.json', ROOT / 'clean_name_fields.json', *parts, *caption_parts, Path(__file__)]}
    save(combined, dict(source_packet=str(packet_path), source_packet_sha256=sha(packet_path.read_bytes()),
        records=rows + captions, speech_records=352, caption_records=21, complete_blocks=20,
        source_parts=evidence, no_current_ROM_English_dialogue_extraction_in_this_intake=True,
        no_localized_drafts=True, no_blanket_before_any_historical_English_exposure_claim=True,
        native_identity_terms_localization_comparison_anddisplay_pending=True, new_credit=0))
    save(target, dict(total_editorial_objects=373, ordinary_speeches=352, typed_caption_records=21,
        typed_choice_objects=10, physical_style_objects=0, source_meanings_saved=373,
        remaining_ordinary_meanings=0, remaining_caption_meanings=0, localized_drafts=0, current_English_comparisons=0,
        complete_clean_meanings=str(combined), complete_clean_meanings_sha256=sha(combined.read_bytes()),
        complete_blocks=list(range(191, 211)), label_free2000_controls=label_free, source_control2000_is_label_free=True,
        completed_overlap=[], completed_keys_checked=9933, completed_ledger_sha256=sha(ledger_path.read_bytes()),
        scope='Twenty complete clean exchanges, including every branch and ten typed menus. Bind native names, roles, source item terms and attribute terminology before localized approval.',
        native_identity_andterms_still_pending=True, no_current_ROM_English_extraction_in_this_intake=True,
        no_all_prior_English_exposure_claim=True, new_credit=0, full_goal_complete=False, guide_photos=False,
        evidence={**evidence, str(combined): sha(combined.read_bytes())}))
    print('Sealed 373 clean meanings: 352 speeches/21 captions in 20 exchanges; zero completed overlaps; no current English or localized drafts.')
