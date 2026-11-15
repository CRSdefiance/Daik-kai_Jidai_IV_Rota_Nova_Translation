"""Bind the complete clean B241–B260 census and the first 50 drafts."""
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_rafael_B221_B240_contextual_v1 import RELEASE
from scripts.draft_rafael_B241_B244_clean_v1 import ROOT
from scripts.write_rafael_B221_B240_contextual_v1 import digest

OUT = ROOT/'clean_source_census_v1.json'
LEDGER = Path('translations/editorial_review_current_v1.json')
PRIOR = Path('translations/papal_trade_contextual_final_review_v1.json')
PATHS = tuple(ROOT/name for name in ('clean_source_packet.json', 'clean_choice_objects.json',
                                     'clean_style_objects.json', 'B241_B244_clean_drafts_v1.json'))


def main():
    assert not OUT.exists()
    packet, choices, styles, drafts = map(load, PATHS)
    assert packet['clean_only_no_prior_English_ornew_editorial_credit']
    assert choices['source_packet_sha256'] == styles['source_packet_sha256'] == digest(PATHS[0])
    blocks = [group['block'] for group in packet['groups']]
    assert blocks == list(range(241,261))
    controls = [group['block'] for group in packet['groups'] if not group['records']]
    assert controls == [244]
    ordinary = [row for group in packet['groups'] for row in group['records']]
    rows = ordinary + styles['records'] + choices['records']
    keys = {(row['file_path'], row['id']) for row in rows}
    assert (len(ordinary), len(styles['records']), len(choices['records']), len(rows), len(keys)) == (290,14,6,310,310)
    assert (styles['object_count'], styles['style_alias_slots'], choices['object_count']) == (2,16,3)
    assert not choices['label_free2000_controls']
    credited = {(row['file_path'], row['id']) for row in load(LEDGER)['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']}
    retained = [row for row in load(PRIOR)['records']
                if row['file_path'] == packet['file_path'] and row['block'] == 246]
    prior_by_id = {row['id']:row for row in retained}
    overlap = keys & credited
    assert len(prior_by_id) == 18 and overlap == {(packet['file_path'], ident) for ident in prior_by_id}
    clean_context = [row for row in rows if row['block'] == 246]
    assert {row['id'] for row in clean_context} == prior_by_id.keys()
    for row in clean_context:
        earlier = prior_by_id[row['id']]
        assert earlier['source_hex'] == row['source_hex'] and all(earlier['review'].values())
        assert all(earlier['source_reference'][key] == row['source_reference'][key]
                   for key in ('block','offset','record_index','header_offset'))
    history, current = map(load, (PRIOR, RELEASE))
    earlier_ROM, current_ROM = map(Path, (history['candidate'], current['candidate']))
    assert digest(earlier_ROM) == history['candidate_sha256'] and digest(current_ROM) == current['candidate_sha256']
    earlier_block, current_block = [
        IlnkContainer.parse(NdsImage.open(path).read_file(packet['file_path'])).blocks[246]
        for path in (earlier_ROM, current_ROM)]
    assert earlier_block == current_block
    assert drafts['complete_blocks'] == [241,242,243,244] and drafts['records_count'] == 50
    assert drafts['all_five_gates_pending'] and drafts['no_current_English_extracted_for_this_intake_before_drafts']
    assert {row['id'] for row in drafts['records']} == {row['id'] for row in rows if row['block'] <= 244}
    assert all(digest(Path(path)) == checksum for path, checksum in drafts['evidence'].items())
    save(OUT, dict(clean_objects=310, clean_speeches=290, physical_style_alternatives=14, native_style_slots=16,
        style_objects=2, typed_choice_captions=6, typed_choice_objects=3, control_only_blocks=controls,
        complete_blocks=blocks, independently_drafted_records=50, complete_draft_blocks=[241,242,243,244],
        prior_reviewed_context_only_blocks=[246], prior_reviewed_records=18, new_eligible_objects=292,
        remaining_clean_drafts=242, remaining_current_comparisons=292, no_duplicate_credit=True,
        prior_context_review=str(PRIOR), prior_context_review_sha256=digest(PRIOR),
        prior_completed_block_byte_identical_in_current_Rafael2952=True,
        all_individual_five_gates_pending=True, source_only_no_current_English_extracted=True,
        evidence={str(path):digest(path) for path in (*PATHS, PRIOR, RELEASE, Path(__file__))}, new_credit=0))
    print('310 clean objects, 18 preserved B246 reviews, and 50 new source-only drafts.')


if __name__ == '__main__':
    main()

