"""Seal all 373 source-grounded drafts before extracting current story English."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')


if __name__ == '__main__':
    output = ROOT / 'complete_clean_English_drafts_v1.json'
    captions_path = ROOT / 'all21_clean_caption_drafts_v1.json'
    assert not output.exists() and not captions_path.exists()
    meanings_path = ROOT / 'complete_clean_meanings_before_English.json'
    identities_path = ROOT / 'native_identity_checkpoint_v1.json'
    terms_path = ROOT / 'source_current_term_checkpoint_v1.json'
    meanings = load(meanings_path)
    parts = [ROOT / name for name in ['B191_B197_97_clean_English_drafts_v1.json',
        'B198_B203_107_clean_English_drafts_v1.json', 'B204_B210_148_clean_English_drafts_v1.json']]
    speeches = [r for path in parts for r in load(path)['records']]
    assert len(speeches) == len({r['id'] for r in speeches}) == 352
    captions = []
    for original in meanings['records']:
        if 'source_index' not in original:
            continue
        block, offset, index = original['block'], original['source_command_offset'], original['source_index']
        if block in [200, 205]:
            english = ['Buy', 'Pass'][index]
            note = ('Accept the current quoted price for the unnamed item.' if index == 0 else
                'Decline the current quoted price; subsequent bargaining or leaving follows the original branch, rather than renaming every decline Haggle.')
            if block == 205:
                note = ['Buy the rope at the final 100000 asking price; the caption does not repeat the preceding price.',
                    'Decline the rope and retain the original refusal branch.'][index]
        elif block == 201:
            english = ['Buy it', 'Pass', 'Let Ian decide'][index]
            note = ['Choose purchase at the stated 8500 price.', 'Decline the offered book.',
                'Delegate the decision to Ian without adding an instruction to pay from his personal funds.'][index]
        else:
            assert block == 210
            if offset == 956:
                english = ['I see.', 'So what?'][index]
                note = ['Acknowledge the information-gathering explanation without prematurely selecting the purchase.',
                    'Preserve the dismissive challenge to the explanation, distinct from a price refusal.'][index]
            else:
                assert offset == 1126
                english = ["I'll take them!", 'Too expensive...'][index]
                note = ['Use a natural buyer\'s acceptance for 買った, retaining the quoted 9000 price.',
                    'Object to the price rather than flatten this into the earlier So what question.'][index]
        assert english == english.strip() and not any(t in english for t in ['\n', '{LB', '{ALIGN', '{PAD}', '  '])
        english.encode('cp932')
        row = dict(original)
        row.update(english=english, logical_English=english, speaker='Player menu', context=original['exchange_context'],
            localization_note=note, kind='typed-choice-label',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
            complete_clean_exchange_andemotional_progression_reviewed=True,
            current_ROM_English_conversation_comparison_pending=True, current_reference_pending=True,
            no_authored_ordinary_breaks_alignment_orpadding=True, new_credit=0)
        captions.append(row)
    assert len(captions) == len({r['id'] for r in captions}) == 21
    source = {r['id']: r for r in meanings['records']}
    rows = speeches + captions
    assert len(rows) == len(source) == 373 and {r['id'] for r in rows} == set(source)
    for row in rows:
        assert all(row[k] == source[row['id']][k] for k in ['source_hex', 'source_reference', 'source_Japanese', 'source_meaning'])
        assert all(row['review'][k] for k in ['source', 'context', 'localization', 'naturalness']) and row['review']['formatting'] is False
    by_id = {r['id']: r for r in speeches}
    assert by_id['DK4_MES_B209_R0013']['english'] in by_id['DK4_MES_B209_R0009']['english']
    for first, echo in [(28, 32), (36, 40)]:
        assert by_id[f'DK4_MES_B209_R{first:04d}']['english'] == by_id[f'DK4_MES_B209_R{echo:04d}']['english']
    assert by_id['DK4_MES_B209_R0020']['english'] in by_id['DK4_MES_B209_R0017']['english']
    assert by_id['DK4_MES_B209_R0063']['english'] in by_id['DK4_MES_B209_R0059']['english']
    save(captions_path, dict(records=captions, complete_menus=10, caption_drafts=21,
        source_meanings=str(meanings_path), source_meanings_sha256=sha(meanings_path.read_bytes()),
        all_fifth_gates_pending=True, new_credit=0))
    save(output, dict(format='dk4-source-first-logical-English-drafts-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        file_path='/data/SC1.DK4', blocks=list(range(191, 211)), records=rows,
        speech_drafts=352, caption_drafts=21, complete_source_menus=10, scoped_actors=43,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        no_blanket_before_any_historical_English_exposure_claim=True, exact_source_keys_andmacro_counts_pass=True,
        no_authored_ordinary_wraps_orpadding=True, parrot_complete_call_andresponse_links_pass=True,
        individual_draft_prose_gates_not_final_existing_English_comparison=True,
        all_current_comparisons_andfresh_formatting_native_visual_storage_gameplay_release_pending=True,
        new_credit=0, new_ROMs=0, guide_photos=False,
        evidence={str(p): sha(p.read_bytes()) for p in [meanings_path, identities_path, terms_path, *parts, captions_path, Path(__file__)]}))
    print('Sealed all 373 logical drafts: 352 speeches/21 captions in 20 complete exchanges. All source keys/macros and parrot echoes pass; current comparison/display pending.')
