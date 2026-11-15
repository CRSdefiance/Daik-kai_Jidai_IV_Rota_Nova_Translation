"""Save reviewed logical source-first drafts; current-English comparison stays pending."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_clean_20261102')


def save_part(label, drafts, contexts, notes, producer):
    output = ROOT / (label + '_clean_English_drafts_v1.json')
    assert not output.exists()
    meanings_path = ROOT / 'complete_clean_meanings_before_English.json'
    bindings_path = ROOT / 'native_identity_and_term_checkpoint_v1.json'
    meanings, bindings = load(meanings_path), load(bindings_path)
    speakers = {r['actor_ID']: next(c['text'] for c in r['current_consumers'] if c['consumer'] == 'progressive-nameplate')
        for r in bindings['records']}
    rows = []
    for block, texts in drafts.items():
        source = [r for r in meanings['records'] if r['block'] == block and r.get('source_selector') is not None]
        assert len(source) == len(texts), (block, len(source), len(texts))
        assert len(notes[block]) == len(texts)
        for original, english, note in zip(source, texts, notes[block], strict=True):
            assert isinstance(english, str) and english and english == english.strip()
            assert not any(t in english for t in ['\n', '{LB', '{ALIGN', '{PAD}', '  '])
            expected = {m: bytes.fromhex(original['source_hex'])[1:].count(m.encode('ascii')) for m in ['FI', 'FA', 'FO']}
            assert all(english.count('{MACRO:' + m + '}') == count for m, count in expected.items()), original['id']
            english.encode('cp932')
            selector = original['source_selector']
            speaker = speakers.get(selector, 'Unnamed woman in FE panel' if block == 179 else 'System panel')
            if selector == 254 and block == 187 and original['source_Japanese'] == 'バタンッ！':
                speaker = 'Sound effect in FE panel'
            incidental = original['id'] == 'DK4_MES_B188_R0022'
            rows.append(dict(id=original['id'], file_path=original['file_path'], block=block,
                source_reference=original['source_reference'], source_hex=original['source_hex'],
                source_Japanese=original['source_Japanese'], source_selector=selector,
                source_complete_preamble_hex=original['source_complete_preamble_hex'],
                source_meaning=original['source_meaning'], english=english, logical_English=english,
                speaker=speaker, context=contexts[block], exchange_context=contexts[block],
                localization_note=note, review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
                complete_clean_exchange_andemotional_progression_reviewed=True,
                source_first_meaning_reference=dict(path=str(meanings_path), sha256=sha(meanings_path.read_bytes()), id=original['id']),
                native_identity_reference=dict(path=str(bindings_path), sha256=sha(bindings_path.read_bytes()), actor_ID=selector if selector < 207 else None),
                incidental_earlier_user_tea_screenshot_exposure=incidental,
                draft_before_any_earlier_English_exposure_claimed=not incidental,
                current_ROM_English_conversation_comparison_pending=True,
                current_reference_pending=True, no_authored_ordinary_breaks_alignment_orpadding=True,
                formatting_visual_stored_gameplay_andregistered_release_pending=True,
                individual_draft_prose_gates_not_final_comparison_approval=True, new_credit=0))
    save(output, dict(format='dk4-source-first-logical-English-drafts-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        file_path='/data/SC1.DK4', blocks=list(drafts), records=rows,
        current_ROM_English_unconsulted=True, all_individual_fifth_gates_pending=True,
        incidental_screenshot_exposure_disclosed=any(r['incidental_earlier_user_tea_screenshot_exposure'] for r in rows),
        no_blanket_source_first_claim_for_incidental_exposure=True, new_credit=0, new_ROMs=0,
        evidence={str(p): sha(Path(p).read_bytes()) for p in [meanings_path, bindings_path, Path(producer), Path(__file__)]}))
    print('Saved', len(rows), 'logical drafts in complete exchanges', list(drafts), ';current comparison/display pending.')
