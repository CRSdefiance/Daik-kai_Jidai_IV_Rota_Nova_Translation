"""Save source-grounded logical prose; comparison and display gates remain pending."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

ROOT = Path('work/analysis/Hodram_B191_B210_clean_20261104')


def save_part(label, drafts, notes, producer):
    output = ROOT / (label + '_clean_English_drafts_v1.json')
    assert not output.exists()
    meanings_path = ROOT / 'complete_clean_meanings_before_English.json'
    bindings_path = ROOT / 'native_identity_checkpoint_v1.json'
    terms_path = ROOT / 'source_current_term_checkpoint_v1.json'
    meanings, bindings = map(load, [meanings_path, bindings_path])
    assert load(terms_path)['no_current_story_English_extraction']
    speakers = {r['actor_ID']: next(c['text'] for c in r['current_consumers'] if c['consumer'] == 'progressive-nameplate') for r in bindings['records']}
    rows = []
    for block, texts in drafts.items():
        source = [r for r in meanings['records'] if r['block'] == block and r.get('source_selector') is not None]
        assert len(source) == len(texts) == len(notes[block]), (block, len(source), len(texts), len(notes[block]))
        for original, english, note in zip(source, texts, notes[block], strict=True):
            assert english and english == english.strip() and note.strip()
            assert not any(t in english for t in ['\n', '{LB', '{ALIGN', '{PAD}', '  '])
            raw = bytes.fromhex(original['source_hex'])[1:]
            assert all(english.count('{MACRO:' + m + '}') == raw.count(m.encode('ascii')) for m in ['FI', 'FA', 'FO']), original['id']
            english.encode('cp932')
            selector = original['source_selector']
            speaker = speakers.get(selector, 'System panel')
            if selector == 254:
                if block == 202:
                    speaker = 'Unidentified Namahage voice'
                elif block == 208:
                    speaker = "Jam's letter in FE panel"
                elif block == 209:
                    speaker = 'Parrot or sound effect in FE panel'
                elif original['source_Japanese'] in ['どさっ！', 'ガタッ', 'パラッパラッ']:
                    speaker = 'Sound effect in FE panel'
            rows.append(dict(id=original['id'], file_path=original['file_path'], block=block,
                source_reference=original['source_reference'], source_hex=original['source_hex'],
                source_Japanese=original['source_Japanese'], source_selector=selector,
                source_complete_preamble_hex=original['source_complete_preamble_hex'], source_meaning=original['source_meaning'],
                english=english, logical_English=english, speaker=speaker,
                context=original['exchange_context'], exchange_context=original['exchange_context'], localization_note=note,
                review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
                complete_clean_exchange_andemotional_progression_reviewed=True,
                source_first_meaning_reference=dict(path=str(meanings_path), sha256=sha(meanings_path.read_bytes()), id=original['id']),
                native_identity_reference=dict(path=str(bindings_path), sha256=sha(bindings_path.read_bytes()), actor_ID=selector if selector < 207 else None),
                native_term_reference=dict(path=str(terms_path), sha256=sha(terms_path.read_bytes())),
                no_authored_ordinary_breaks_alignment_orpadding=True, no_blanket_before_any_historical_English_exposure_claim=True,
                current_ROM_English_conversation_comparison_pending=True, current_reference_pending=True,
                formatting_visual_stored_gameplay_andregistered_release_pending=True,
                individual_draft_prose_gates_not_final_comparison_approval=True, new_credit=0))
    save(output, dict(format='dk4-source-first-logical-English-drafts-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        file_path='/data/SC1.DK4', blocks=list(drafts), records=rows,
        current_ROM_English_dialogue_unconsulted_in_this_intake=True, all_individual_fifth_gates_pending=True,
        no_blanket_before_any_historical_English_exposure_claim=True, new_credit=0, new_ROMs=0,
        evidence={str(p): sha(Path(p).read_bytes()) for p in [meanings_path, bindings_path, terms_path, Path(producer), Path(__file__)]}))
    print('Saved', len(rows), 'logical drafts in complete exchanges', list(drafts), '; comparison/display pending.')
